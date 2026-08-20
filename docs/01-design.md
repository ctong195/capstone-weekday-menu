# 01 Design Discovery

## Goal
Define the product shape before coding so the app stays aligned with the spec.

## Questions to Resolve
1. What is the primary user journey from landing page to completed order?
2. How should the 3-dish daily menu be displayed with images, price, and availability?
3. What data does the frontend need to request from the backend for menu, slots, and checkout?
4. How should pickup slots be shown when capacity approaches 15 meals?
5. What payment states should the UI reflect during checkout?

## Proposed UI Sections
1. Header and brand area.
2. Daily menu card with three dishes, pictures, and fixed pricing.
3. Pickup slot selector with remaining capacity.
4. Checkout section with Apple Pay, Google Pay, and PayPal.
5. Confirmation and error message area.

## Proposed Data Model Inputs
- Menu date
- Dish id, name, price, and image URL
- Pickup slot label and remaining capacity
- Payment provider
- Order total

## Design Decisions to Lock
1. Menu cards should use image-first layout.
2. Slot availability should be visible before checkout.
3. Payment provider options should be clearly separated from order details.
4. The UI should work as a responsive browser-based frontend.

## Output of This Step
- A simple wireframe or section map.
- A list of API fields required by the frontend.
- A confirmed interaction flow for ordering.
- Update [progress.md](progress.md) with design status, key decisions, and next actions.
