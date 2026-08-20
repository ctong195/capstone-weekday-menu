# Copilot App Handoff

## Project
- Repository: https://github.com/ctong195/capstone-weekday-menu
- Branch: main

## What Is Completed
1. Initial capstone repository created and pushed.
2. Core product specification created and expanded to include:
   - Weekday random 3-dish menu
   - Fixed dish price of 15.95
   - Apple Pay, Google Pay, PayPal support
   - Pickup slots every 15 minutes from 10:30 to 2:30
   - Capacity cap of 15 meals per slot
   - Web frontend deployability
   - Testing suite requirement
   - Encryption requirements for payment-related transactions
   - Frontend dish image requirement with fallback image
3. Progressive discovery docs created:
   - docs/01-design.md
   - docs/02-implementation.md
   - docs/03-testing.md
   - docs/README.md
4. Progress tracker created and backfilled:
   - docs/progress.md

## Key Files to Start With
1. docs/spec.md
2. docs/progress.md
3. docs/01-design.md
4. docs/02-implementation.md
5. docs/03-testing.md

## Recommended Next Work
1. Add image fields to the backend menu model and API response.
2. Update frontend to render dish images and fallback images.
3. Add tests for image field behavior and fallback rendering paths.
4. Define deployment target and add deployment configuration.

## Suggested Prompt for GitHub Copilot App
Use this project context:
- Read docs/spec.md and docs/progress.md first.
- Follow docs/README.md progressive flow.
- Implement next milestone: dish image support end-to-end (backend model, API, frontend rendering, tests).
- Keep changes small, tested, and aligned with acceptance criteria.
