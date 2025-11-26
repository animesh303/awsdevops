# Phase 2: Generate Tests

Detailed guidance lives in `testing-phases/blueprint.md#phase-2-%E2%80%93-generate-tests`.

**Essentials**
- Reload the approved test plan, language standards, and relevant source files; summarize context per the guardrails.
- Create tests under `tests/{unit|integration|e2e|performance|security}/` following runtime conventions, leverage fixtures/utilities, and record locations plus coverage deltas in `.test-docs/test-plan.md`.
- Keep suites deterministic (AAA pattern, clear naming, ≥80 % coverage target) and document any helper configs or generators you add.
- Log the Phase‑2 prompt in `.test-docs/audit.md`, wait for approval, update `.test-docs/test-state.md`, and remind the user to commit the new tests and support files.

