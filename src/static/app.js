const menuList = document.getElementById("menu-list");
const dishOptions = document.getElementById("dish-options");
const orderForm = document.getElementById("order-form");
const orderDateInput = document.getElementById("order-date");
const pickupSlotSelect = document.getElementById("pickup-slot");
const result = document.getElementById("result");
const fallbackDishImage = "/static/images/dish-fallback.svg";

let currentMenu = [];

function todayIso() {
  return new Date().toISOString().split("T")[0];
}

async function loadMenu() {
  const response = await fetch("/menu/today");
  const data = await response.json();

  if (!response.ok) {
    menuList.textContent = data.detail || "Unable to load menu";
    return;
  }

  currentMenu = data.dishes;
  menuList.innerHTML = "";
  dishOptions.innerHTML = "";

  data.dishes.forEach((dish) => {
    const article = document.createElement("article");
    article.className = "dish-card";

    const image = document.createElement("img");
    image.className = "dish-image";
    image.src = dish.image_url || fallbackDishImage;
    image.alt = dish.name;
    image.addEventListener("error", () => {
      if (!image.src.endsWith(fallbackDishImage)) {
        image.src = fallbackDishImage;
      }
    });

    const details = document.createElement("div");
    details.className = "dish-details";

    const name = document.createElement("h3");
    name.textContent = dish.name;

    const price = document.createElement("p");
    price.className = "dish-price";
    price.textContent = `$${dish.price.toFixed(2)}`;

    details.append(name, price);
    article.append(image, details);
    menuList.appendChild(article);

    const label = document.createElement("label");
    label.className = "dish-option";

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = dish.id;
    checkbox.name = "dish_ids";

    label.appendChild(checkbox);
    label.appendChild(document.createTextNode(` ${dish.name}`));
    dishOptions.appendChild(label);
  });
}

async function loadSlots(slotDate) {
  const response = await fetch(`/pickup-slots?slot_date=${slotDate}`);
  const data = await response.json();

  pickupSlotSelect.innerHTML = "";
  if (!response.ok) {
    const option = document.createElement("option");
    option.value = "";
    option.textContent = data.detail || "No slots available";
    pickupSlotSelect.appendChild(option);
    return;
  }

  data.slots.forEach((slot) => {
    const option = document.createElement("option");
    option.value = slot.slot;
    option.textContent = `${slot.slot} (${slot.remaining_capacity} meals left)`;
    option.disabled = !slot.is_available;
    pickupSlotSelect.appendChild(option);
  });
}

orderForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const selectedDishIds = Array.from(
    document.querySelectorAll('input[name="dish_ids"]:checked')
  ).map((input) => input.value);

  if (!selectedDishIds.length) {
    result.textContent = "Select at least one dish.";
    return;
  }

  const payload = {
    customer_name: document.getElementById("customer-name").value,
    customer_contact: document.getElementById("customer-contact").value,
    order_date: orderDateInput.value,
    pickup_slot: pickupSlotSelect.value,
    dish_ids: selectedDishIds,
    payment_provider: document.getElementById("payment-provider").value,
  };

  const response = await fetch("/orders", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json();
  result.textContent = JSON.stringify(data, null, 2);

  if (response.ok) {
    await loadSlots(orderDateInput.value);
  }
});

orderDateInput.value = todayIso();
orderDateInput.addEventListener("change", () => loadSlots(orderDateInput.value));

loadMenu().then(() => loadSlots(orderDateInput.value));
