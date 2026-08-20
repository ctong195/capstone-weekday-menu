# Progress Tracker

Use this file to track work across design, implementation, and testing.

## Status Legend
- Not Started
- In Progress
- Blocked
- Done

## Current Phase
- Phase: Discovery Documentation Completed, Build Iteration Ongoing
- Owner: Chin Tong
- Last Updated: 2026-08-20

## Milestones
| Milestone | Status | Notes | Updated On |
| --- | --- | --- | --- |
| 01 Design Discovery | Done | Created [01-design.md](01-design.md) with UX, data, and decision checkpoints. | 2026-08-20 |
| 02 Implementation Discovery | Done | Created [02-implementation.md](02-implementation.md) with backend/frontend responsibilities and build order. | 2026-08-20 |
| 03 Testing Discovery | Done | Created [03-testing.md](03-testing.md) with test layers, core cases, and release gate. | 2026-08-20 |

## Task Log
| Date | Area | Update | Next Step | Blockers |
| --- | --- | --- | --- | --- |
| 2026-08-05 | Repository Setup | Created local repo and pushed GitHub repository: https://github.com/ctong195/capstone-weekday-menu. | Continue refining product documentation and implementation priorities. | None |
| 2026-08-05 | Product Spec | Created [spec.md](spec.md) with core requirements: weekday random 3-dish menu, fixed 15.95 pricing, wallet payments, pickup slots, and 15-meal slot cap. | Add non-functional and acceptance details as requirements evolve. | None |
| 2026-08-05 | Spec Enhancements | Added requirements for deployable web frontend, test suite expectations, encrypted transactions, and dish images in frontend. | Keep acceptance criteria aligned with implementation milestones. | None |
| 2026-08-20 | Progressive Discovery Docs | Added [README.md](README.md), [01-design.md](01-design.md), [02-implementation.md](02-implementation.md), and [03-testing.md](03-testing.md). | Use docs sequence for planning and execution reviews. | None |
| 2026-08-20 | Progress Tracking | Added this [progress.md](progress.md) tracker and updated discovery docs to require progress updates each phase. | Maintain this file whenever scope, status, or blockers change. | None |

## Decisions Log
| Date | Decision | Reason |
| --- | --- | --- |
| 2026-08-05 | Build backend with Python/FastAPI and frontend as web UI. | Fast iteration for API logic, validation, and browser deployability. |
| 2026-08-05 | Keep fixed dish price at 15.95 and enforce in backend validation. | Prevent pricing tampering and preserve business rule consistency. |
| 2026-08-05 | Capacity is counted by meal count, not by order count. | Align throughput controls with kitchen workload realities. |
| 2026-08-05 | Require encrypted payment-related transactions. | Protect payment information and align with secure handling expectations. |
| 2026-08-20 | Use progressive discovery docs with mandatory progress tracking. | Improve visibility, handoff clarity, and delivery accountability. |
