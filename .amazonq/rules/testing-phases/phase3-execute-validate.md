# Phase 3: Execute & Validate

See `testing-phases/blueprint.md#phase-3-%E2%80%93-execute-%26-validate` for the full checklist.

**Highlights**
- Load all generated tests plus tooling configs, install dependencies, and summarize the environment/context.
- Run the suites defined in the plan (unit/integration/E2E/perf/etc.), capture logs, exit codes, and triage notes; store coverage artifacts under `.test-docs/coverage-reports/{language}-coverage.<ext>`.
- Document pass/fail status, flaky cases, remediation ideas, and gating results in the plan or a lightweight results file.
- Log the Phase‑3 prompt in `.test-docs/audit.md`, wait for approval, update `.test-docs/test-state.md`, and remind the user to commit execution logs + coverage reports.

