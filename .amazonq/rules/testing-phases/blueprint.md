# Testing Phase Blueprint

Each `phaseX-*.md` file now links to this blueprint to keep rules concise.

## Phase 1 – Analyze & Plan
**Goal:** capture test requirements, strategy, and targets.  
**Inputs:** `.test-docs/test-state.md`, source files, existing tests/coverage.  
**Outputs:** `test-plan.md`, detection summary, updated state.

**Checklist**
1. Load repo context (code structure, existing tests, coverage reports) plus the latest state file.
2. Identify languages, frameworks, environments, and required test types (unit/integration/E2E/perf/security).
3. Define coverage targets, tooling, data/setup needs, and gating criteria; document in `test-plan.md`.
4. Note required standards files in `testing-phases/{language}-testing-standards.md` and create any missing ones.
5. Log the Phase‑1 approval prompt, wait for confirmation, update `test-state.md`, remind about committing artifacts.

## Phase 2 – Generate Tests
**Goal:** produce the suites defined in the plan.  
**Outputs:** tests under `tests/{type}/`, plan checkboxes updated, artifact list recorded.

**Checklist**
1. Reload the plan, standards, and relevant source files; summarize context per guardrails.
2. Generate tests per language/framework conventions with clear arrange/act/assert patterns and fixtures/mocks where needed.
3. Store new files under the proper directory (`tests/unit`, `tests/integration`, `tests/e2e`, `tests/performance`, etc.) and record locations in the plan.
4. Update `test-plan.md` checkboxes, log the Phase‑2 prompt in `audit.md`, wait for approval, update `test-state.md`, and remind the user to commit tests.

## Phase 3 – Execute & Validate
**Goal:** run suites, capture coverage, and triage failures.  
**Outputs:** execution logs, coverage reports in `.test-docs/coverage-reports/`, updated results summary.

**Checklist**
1. Load all tests plus tooling configs; ensure dependencies are installed or document prerequisites.
2. Run the planned suites (unit/integration/E2E/perf) and capture output + exit codes.
3. Generate coverage (per language tooling) and store artifacts under `.test-docs/coverage-reports/{language}-coverage.<ext>`.
4. Document pass/fail status, flake triage, and remediation notes in the plan/results doc.
5. Log the Phase‑3 prompt, obtain approval, update `test-state.md`, and remind about committing logs/reports.

## Phase 4 – Review & Integrate
**Goal:** package results, integrate with CI/CD, and finalize recommendations.  
**Outputs:** summary report, CI/CD integration notes, updated action items.

**Checklist**
1. Reload all prior artifacts plus CI/CD context (existing workflows, required env vars/secrets).
2. Summarize coverage, failures, gaps, and next steps in the plan or a short `.test-docs/testing-summary.md`.
3. Outline integration steps (workflow updates, scripts, docs) and flag any follow-up tickets/action items.
4. Log the final prompt, capture approval, mark Phase 4 complete in `test-state.md`, and remind the user to commit/push all testing artifacts.

