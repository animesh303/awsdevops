# PRIORITY: Testing workflow overrides other rules whenever the user asks for testing, test generation, test execution, coverage goals, or QA automation.

## When to use

- Trigger on requests about tests, coverage, validation, or QA suites.
- Stay in this workflow until the Review & Integrate phase is accepted.

## Combine with shared guardrails

- Pair this file with `common-workflow-guardrails.md` for session continuity, logging, approvals, and git reminders.
- Phase instructions live in `.amazonq/rules/testing-phases/phaseN-*.md`; execute them verbatim.

## Welcome message (use exactly)

> "🧪 **AWS Business Group Testing Workflow** – Phases:
> 1. Analyze & plan
> 2. Generate tests
> 3. Execute & validate
> 4. Review & integrate
>
> Confirm you understand the flow and are ready to begin Phase 1 (Analyze & Plan)."

Wait for confirmation before starting Phase 1.

## Phase overview

| Phase                 | Detail file                                 | Focus                                                           | Required prompt                         |
| --------------------- | ------------------------------------------- | --------------------------------------------------------------- | --------------------------------------- |
| 1. Analyze & Plan     | `testing-phases/phase1-analyze-plan.md`     | Inspect codebase, draft strategy, define coverage targets.      | "Analysis complete. Generate tests?"    |
| 2. Generate Tests     | `testing-phases/phase2-generate-tests.md`   | Produce unit/integration/E2E/perf tests per language standards. | "Tests drafted. Execute & validate?"    |
| 3. Execute & Validate | `testing-phases/phase3-execute-validate.md` | Run suites, capture coverage + results, triage failures.        | "Execution done. Review & integrate?"   |
| 4. Review & Integrate | `testing-phases/phase4-review-integrate.md` | Summarize quality, integrate into CI/CD, capture follow-ups.    | "Testing workflow complete. Satisfied?" |

## Context loading highlights

- Always read `.test-docs/test-state.md` (or reconstruct from artifacts) before resuming.
- Load existing coverage reports, plans, and test assets from `.test-docs/` and `tests/`.
- Include updated source files so generated tests reflect current code paths.
- When resuming, summarize which artifacts (plans, tests, reports) were loaded.

## MCP usage

- `github-mcp-server`: post results/coverage to PRs, check workflow runs, open issues for failures.
- `git-mcp-server`: create branches for test work, commit new test suites, detect files needing updates.
- Use MCP context before generating or executing tests, so automated tooling reflects the repository state.

## Test deliverables

- Test plan: `.test-docs/test-plan.md`.
- Coverage artifacts: `.test-docs/coverage-reports/{language}-coverage.<ext>`.
- Tests go under `tests/{unit|integration|e2e|performance}/`.
- Target ≥80 % statement coverage unless the user sets a different goal. Call out gaps explicitly.

## Language-specific standards

- For every detected runtime, read the matching file in `testing-phases/{language}-testing-standards.md` (python, nodejs, java, go, terraform, etc.) before creating or updating tests.
- Add a new standards file if the runtime is missing.
