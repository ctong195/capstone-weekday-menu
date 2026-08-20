# 03 Testing Discovery

## Goal
Define the minimum test suite needed to prove the app works and stays safe to change.

## Test Layers
1. Unit tests for business rules.
2. API tests for request and response behavior.
3. Frontend behavior checks for menu display and ordering flow.
4. Payment-flow tests using mocks or sandbox responses.
5. Regression tests for bugs that have already been fixed.

## Core Cases to Cover
1. Weekday menu generation returns exactly 3 dishes.
2. Weekend menu generation is rejected.
3. All dishes use the fixed 15.95 price.
4. Pickup slots only allow 15 meals per slot.
5. Slot capacity is reduced by meal count.
6. Unsupported payment providers are rejected.
7. Payment-related communication requires encryption.
8. Dish images or fallback images render in the frontend.

## Suggested Tooling
- `pytest` for backend and API tests.
- Mocked payment provider responses for checkout flows.
- Browser-based checks for the UI if the frontend grows more complex.

## Acceptance for Test Quality
1. Tests run in one command.
2. Tests cover the critical business rules from the spec.
3. Tests fail when slot limits, pricing, or payment rules are broken.
4. New features must include tests before merge.

## Release Gate
Do not treat the app as ready unless the critical business rules and payment paths are covered by automated tests.

## Progress Tracking Requirement
Before closing the testing phase, update [progress.md](progress.md) with test coverage status, open defects, and release readiness.
