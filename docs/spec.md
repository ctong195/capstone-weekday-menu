# Product Specification: Weekday Random Menu App

## 1. Overview
This application offers a weekday lunch ordering experience. Each weekday, the system generates a random menu of 3 dishes. Patrons can purchase dishes at a fixed price, pay through supported digital wallets, and select a pickup time from controlled 15-minute slots.

## 2. Business Requirements
1. The app must generate exactly 3 random dishes each weekday.
2. Every dish must be priced at $15.95.
3. The app must support payment via Apple Pay, Google Pay, and PayPal.
4. Patrons must be able to choose pickup times in 15-minute increments.
5. Pickup slots must run from 10:30 AM to 2:30 PM.
6. Each pickup slot must have a maximum capacity of 15 meals.

## 3. Scope
### In Scope
- Daily weekday menu generation.
- Fixed price enforcement.
- Checkout with Apple Pay, Google Pay, and PayPal.
- Pickup slot booking with capacity tracking.
- Basic order confirmation.

### Out of Scope
- Weekend menu generation.
- Dynamic pricing.
- Delivery logistics.
- Loyalty points or promotions.

## 4. Functional Requirements

### 4.1 Menu Generation
1. The system generates a new menu at the start of each weekday (Monday-Friday).
2. The menu contains exactly 3 unique dishes.
3. Dishes are selected randomly from a predefined dish catalog.
4. The generated menu remains fixed for that day.

### 4.2 Pricing
1. Each menu dish price is fixed at $15.95.
2. Users cannot modify item prices in the UI.
3. Backend must validate pricing at order creation to prevent tampering.

### 4.3 Ordering Flow
1. Patron views the current weekday menu.
2. Patron selects one or more dishes.
3. Patron selects a pickup slot.
4. Patron completes payment via one of the supported providers.
5. Patron receives order confirmation including selected dishes, total amount, and pickup time.

### 4.4 Pickup Slot Rules
1. Slot interval is 15 minutes.
2. Slot schedule starts at 10:30 AM and ends at 2:30 PM.
3. Valid slot values are:
   - 10:30, 10:45
   - 11:00, 11:15, 11:30, 11:45
   - 12:00, 12:15, 12:30, 12:45
   - 1:00, 1:15, 1:30, 1:45
   - 2:00, 2:15, 2:30
4. Each slot supports at most 15 meals.
5. If a slot reaches 15 meals, it must be shown as unavailable.
6. Capacity counts meals, not orders. Example: one order with 3 dishes consumes 3 units of slot capacity.

### 4.5 Payment Integration
1. Supported payment methods:
   - Apple Pay
   - Google Pay
   - PayPal
2. Checkout must fail gracefully if provider authorization fails.
3. Orders are only confirmed after successful payment authorization/capture.
4. Payment transaction reference must be saved with order details.

## 5. Data Model (Conceptual)

### Dish
- id
- name
- price (must equal 15.95)
- is_active

### DailyMenu
- id
- menu_date
- dishes (exactly 3 dish ids)
- generated_at

### PickupSlot
- id
- date
- start_time
- end_time
- max_capacity (15)
- used_capacity (0-15)
- is_available

### Order
- id
- customer_name
- customer_contact
- menu_date
- selected_dish_ids
- meal_count
- pickup_slot_id
- total_amount
- payment_provider
- payment_status
- payment_reference
- created_at

## 6. API Contract (High-Level)

### Menu APIs
1. `GET /menu/today`
   - Returns the current weekday menu and pricing.
2. `POST /menu/generate`
   - Admin/system endpoint to generate menu for a date (weekday-only validation).

### Slot APIs
1. `GET /pickup-slots?date=YYYY-MM-DD`
   - Returns all slots with remaining capacity.
2. `POST /pickup-slots/reserve`
   - Temporarily reserves slot capacity for checkout.

### Order APIs
1. `POST /orders`
   - Validates menu, price, and slot capacity.
   - Initiates payment.
2. `POST /orders/{order_id}/confirm-payment`
   - Confirms provider callback and finalizes order.

## 7. Validation Rules
1. Orders cannot be created on weekends unless explicitly enabled later.
2. Menu must exist for selected date.
3. Selected dishes must belong to that date's generated menu.
4. Price must always be 15.95 per dish.
5. Slot capacity cannot exceed 15 meals.
6. Payment provider must be one of: `apple_pay`, `google_pay`, `paypal`.

## 8. Non-Functional Requirements
1. Availability: App should be available during ordering hours with graceful degradation.
2. Performance: Menu and slot queries should return in under 500 ms in normal load.
3. Security: Payment data handling must use provider tokens; no raw card data stored.
4. Observability: Log payment failures, slot over-capacity attempts, and order state transitions.

## 9. User Stories
1. As a patron, I want to see today's 3-dish menu so I can quickly choose lunch.
2. As a patron, I want a fixed and transparent price so checkout is predictable.
3. As a patron, I want to pay with my preferred wallet (Apple Pay, Google Pay, PayPal).
4. As a patron, I want to choose a pickup time so I can collect lunch conveniently.
5. As an operator, I want slot capacity limits so kitchen workload stays manageable.

## 10. Acceptance Criteria
1. On a weekday, the app displays exactly 3 menu dishes.
2. Every displayed dish is priced at $15.95.
3. Checkout displays Apple Pay, Google Pay, and PayPal options.
4. Pickup slot selector includes 15-minute slots from 10:30 to 2:30.
5. No slot accepts more than 15 meals.
6. A paid order decreases slot remaining capacity by selected meal count.
7. Attempting to exceed slot capacity returns a clear validation error.
8. Weekend menu generation requests are rejected with a validation message.

## 11. Open Decisions
1. Time zone source (single fixed zone vs location-based).
2. Whether slot reservation expires after a timeout before payment completion.
3. Whether partial refunds are supported when edits/cancellations are added.
4. Whether dish quantity per order should be capped.
