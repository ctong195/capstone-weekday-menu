from __future__ import annotations

from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from pathlib import Path
import random
import uuid

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

PRICE_PER_DISH = Decimal("15.95")
MAX_MEALS_PER_SLOT = 15
PAYMENT_PROVIDERS = {"apple_pay", "google_pay", "paypal"}

DISH_CATALOG = [
    {"id": "dish_1", "name": "Lemongrass Chicken Bowl"},
    {"id": "dish_2", "name": "Roasted Veggie Pasta"},
    {"id": "dish_3", "name": "Miso Salmon Rice"},
    {"id": "dish_4", "name": "Chipotle Tofu Wrap"},
    {"id": "dish_5", "name": "Turkey Pesto Panini"},
    {"id": "dish_6", "name": "Herb Falafel Plate"},
    {"id": "dish_7", "name": "Korean Beef Noodles"},
    {"id": "dish_8", "name": "Mediterranean Grain Bowl"},
    {"id": "dish_9", "name": "Coconut Curry Chickpeas"},
]


def is_weekday(value: date) -> bool:
    return value.weekday() < 5


def parse_iso_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.") from exc


def slot_labels() -> list[str]:
    labels: list[str] = []
    current = datetime.combine(date.today(), time(10, 30))
    end = datetime.combine(date.today(), time(14, 30))
    while current <= end:
        labels.append(current.strftime("%H:%M"))
        current += timedelta(minutes=15)
    return labels


def generate_daily_menu(menu_date: date) -> list[dict[str, str | float]]:
    if not is_weekday(menu_date):
        raise HTTPException(status_code=400, detail="Menu generation is weekday-only.")

    seed = int(menu_date.strftime("%Y%m%d"))
    rng = random.Random(seed)
    selected = rng.sample(DISH_CATALOG, k=3)

    return [
        {"id": dish["id"], "name": dish["name"], "price": float(PRICE_PER_DISH)}
        for dish in selected
    ]


def authorize_payment(provider: str, amount: Decimal) -> str:
    if provider not in PAYMENT_PROVIDERS:
        raise HTTPException(status_code=400, detail="Unsupported payment provider.")
    if amount <= Decimal("0"):
        raise HTTPException(status_code=400, detail="Invalid payment amount.")

    return f"{provider}_{uuid.uuid4().hex[:16]}"


class OrderRequest(BaseModel):
    customer_name: str = Field(min_length=1, max_length=120)
    customer_contact: str = Field(min_length=1, max_length=120)
    order_date: str = Field(description="YYYY-MM-DD")
    dish_ids: list[str] = Field(min_length=1)
    pickup_slot: str = Field(description="HH:MM")
    payment_provider: str


class AppState:
    def __init__(self) -> None:
        self.daily_menus: dict[str, list[dict[str, str | float]]] = {}
        self.slot_usage: dict[str, dict[str, int]] = {}
        self.orders: list[dict[str, str | int | float | list[str]]] = []

    def ensure_slots_for_date(self, date_key: str) -> None:
        if date_key not in self.slot_usage:
            self.slot_usage[date_key] = {label: 0 for label in slot_labels()}


state = AppState()
app = FastAPI(title="Weekday Menu App", version="0.1.0")

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(static_dir / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/menu/today")
def get_today_menu() -> dict[str, str | list[dict[str, str | float]]]:
    today = date.today()
    if not is_weekday(today):
        raise HTTPException(status_code=400, detail="No menu on weekends.")

    date_key = today.isoformat()
    if date_key not in state.daily_menus:
        state.daily_menus[date_key] = generate_daily_menu(today)

    return {"date": date_key, "dishes": state.daily_menus[date_key]}


@app.post("/menu/generate")
def generate_menu_for_date(menu_date: str = Query(..., description="YYYY-MM-DD")) -> dict[str, str | list[dict[str, str | float]]]:
    parsed_date = parse_iso_date(menu_date)
    date_key = parsed_date.isoformat()
    state.daily_menus[date_key] = generate_daily_menu(parsed_date)
    state.ensure_slots_for_date(date_key)
    return {"date": date_key, "dishes": state.daily_menus[date_key]}


@app.get("/pickup-slots")
def get_pickup_slots(slot_date: str = Query(..., description="YYYY-MM-DD")) -> dict[str, str | list[dict[str, str | int | bool]]]:
    parsed_date = parse_iso_date(slot_date)
    if not is_weekday(parsed_date):
        raise HTTPException(status_code=400, detail="Pickup slots are weekday-only.")

    date_key = parsed_date.isoformat()
    state.ensure_slots_for_date(date_key)

    slots = []
    for label, used in state.slot_usage[date_key].items():
        remaining = MAX_MEALS_PER_SLOT - used
        slots.append(
            {
                "slot": label,
                "used_capacity": used,
                "remaining_capacity": remaining,
                "is_available": remaining > 0,
            }
        )

    return {"date": date_key, "slots": slots}


@app.post("/orders")
def create_order(payload: OrderRequest) -> dict[str, str | int | float | list[str]]:
    parsed_date = parse_iso_date(payload.order_date)
    if not is_weekday(parsed_date):
        raise HTTPException(status_code=400, detail="Orders are weekday-only.")

    date_key = parsed_date.isoformat()
    if date_key not in state.daily_menus:
        state.daily_menus[date_key] = generate_daily_menu(parsed_date)

    state.ensure_slots_for_date(date_key)

    if payload.pickup_slot not in state.slot_usage[date_key]:
        raise HTTPException(status_code=400, detail="Invalid pickup slot.")

    today_menu_dish_ids = {dish["id"] for dish in state.daily_menus[date_key]}
    if any(dish_id not in today_menu_dish_ids for dish_id in payload.dish_ids):
        raise HTTPException(status_code=400, detail="Selected dishes must be from that day's menu.")

    meal_count = len(payload.dish_ids)
    used_capacity = state.slot_usage[date_key][payload.pickup_slot]
    if used_capacity + meal_count > MAX_MEALS_PER_SLOT:
        raise HTTPException(status_code=400, detail="Pickup slot capacity exceeded.")

    total_amount = PRICE_PER_DISH * meal_count
    payment_reference = authorize_payment(payload.payment_provider, total_amount)

    state.slot_usage[date_key][payload.pickup_slot] += meal_count

    order = {
        "order_id": uuid.uuid4().hex,
        "customer_name": payload.customer_name,
        "customer_contact": payload.customer_contact,
        "order_date": date_key,
        "dish_ids": payload.dish_ids,
        "meal_count": meal_count,
        "pickup_slot": payload.pickup_slot,
        "total_amount": float(total_amount),
        "payment_provider": payload.payment_provider,
        "payment_status": "paid",
        "payment_reference": payment_reference,
        "created_at": datetime.now(UTC).isoformat(),
    }
    state.orders.append(order)
    return order
