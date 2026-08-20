# 02 Implementation Discovery

## Goal
Turn the approved design into a working app with clear backend and frontend responsibilities.

## Backend Responsibilities
1. Generate the weekday menu.
2. Enforce fixed pricing at 15.95.
3. Validate pickup slot capacity.
4. Validate supported payment providers.
5. Encrypt payment-related data in transit and at rest where stored.
6. Expose API endpoints for menu, slots, and orders.

## Frontend Responsibilities
1. Display the daily menu and dish pictures.
2. Allow patrons to choose dishes and a pickup slot.
3. Show remaining slot capacity.
4. Submit orders to the API.
5. Render success and failure messages clearly.

## Suggested Build Order
1. Implement menu and slot data structures.
2. Add order creation and validation logic.
3. Build the menu UI and order form.
4. Wire the frontend to the API.
5. Add payment provider placeholders or sandbox integrations.
6. Add deployment configuration for browser access.

## Implementation Checkpoints
1. Menu generation returns exactly 3 dishes.
2. Slot capacity is reduced by meal count.
3. Frontend loads and renders current menu data.
4. Order submission succeeds only when all validation passes.
5. Secure transport is required for payment flows.

## Definition of Done
- The app can be opened in a browser.
- Orders can be created from the frontend.
- Slot limits and payment validation are enforced.
- The implementation matches the spec.
- [progress.md](progress.md) is updated with implementation status, blockers, and next steps.
