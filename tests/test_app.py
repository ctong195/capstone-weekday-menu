from datetime import date, timedelta

from fastapi.testclient import TestClient

from src.app import DISH_CATALOG, FALLBACK_DISH_IMAGE_URL, app, state


client = TestClient(app)


def next_weekday(start: date) -> date:
    current = start
    while current.weekday() >= 5:
        current += timedelta(days=1)
    return current


def next_saturday(start: date) -> date:
    current = start
    while current.weekday() != 5:
        current += timedelta(days=1)
    return current


def setup_function() -> None:
    state.daily_menus.clear()
    state.slot_usage.clear()
    state.orders.clear()


def test_generate_menu_has_three_items_and_fixed_price() -> None:
    weekday = next_weekday(date.today())
    response = client.post(f"/menu/generate?menu_date={weekday.isoformat()}")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["dishes"]) == 3
    assert all(dish["price"] == 15.95 for dish in payload["dishes"])
    assert all(dish["image_url"] for dish in payload["dishes"])


def test_menu_uses_fallback_when_catalog_images_are_missing(monkeypatch) -> None:
    for dish in DISH_CATALOG:
        monkeypatch.setitem(dish, "image_url", "")

    weekday = next_weekday(date.today())
    response = client.post(f"/menu/generate?menu_date={weekday.isoformat()}")

    assert response.status_code == 200
    assert all(
        dish["image_url"] == FALLBACK_DISH_IMAGE_URL
        for dish in response.json()["dishes"]
    )


def test_frontend_fallback_image_is_available() -> None:
    response = client.get(FALLBACK_DISH_IMAGE_URL)

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/svg+xml"


def test_weekend_menu_generation_rejected() -> None:
    saturday = next_saturday(date.today())
    response = client.post(f"/menu/generate?menu_date={saturday.isoformat()}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Menu generation is weekday-only."


def test_slot_capacity_is_limited_by_meal_count() -> None:
    weekday = next_weekday(date.today())
    date_key = weekday.isoformat()

    generate_response = client.post(f"/menu/generate?menu_date={date_key}")
    dishes = generate_response.json()["dishes"]
    dish_ids = [dish["id"] for dish in dishes]

    order_payload = {
        "customer_name": "Casey",
        "customer_contact": "casey@example.com",
        "order_date": date_key,
        "pickup_slot": "10:30",
        "dish_ids": dish_ids,
        "payment_provider": "paypal",
    }

    for _ in range(5):
        response = client.post("/orders", json=order_payload)
        assert response.status_code == 200

    overflow_response = client.post("/orders", json=order_payload)
    assert overflow_response.status_code == 400
    assert overflow_response.json()["detail"] == "Pickup slot capacity exceeded."
