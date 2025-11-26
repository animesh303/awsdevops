# Review Phase Blueprint

Use this single reference for all review phases. Each `phaseX-*.md` file simply points here to keep context overhead low.

## Phase 1 – Analyze Changes

**Goal:** understand what changed and define the review surface.  
**Inputs:** PR/branch/files list, `.review-docs/review-state.md`.  
**Outputs:** `changed-files.md`, `change-analysis.md`, `review-plan.md`, `technology-stack.md`.

**Checklist**

1. Gather change set via MCP (`github` for PR metadata, `git` for diffs/branches). Record file + line deltas in `changed-files.md`.
2. Classify scope (feature/bug/refactor/etc), modules touched, and dependency blast radius. Capture metrics in `change-analysis.md`.
3. Load PR description, comments, commit history, and related files for context. Summaries go to `review-context.md`.
4. Define review categories (quality, security, performance, best practices, testing, docs) plus priorities in `review-plan.md`.
5. Detect languages/frameworks/IaC tools and note them in `technology-stack.md`.
6. Load language standards from `review-phases/{language}-review-standards.md`; note gaps if a runtime lacks coverage.
7. Log the plan in `.review-docs/audit.md`, ask the Phase‑1 handoff question, wait for approval, then update `review-state.md`.

## Phase 2 – Review Code

**Goal:** execute the technical review using the plan + standards.  
**Outputs:** Findings in `.review-docs/findings/{category}-findings.md`, inline notes, updated plan checkboxes.

**Checklist**

1. Reload artifacts from Phase 1 plus the actual code under review (source/tests/IaC). Summarize context per guardrails.
2. Work category by category: document issues (ID, severity, recommendation, evidence) in the appropriate findings file.
3. Use MCP to fetch extra diffs, blame data, or repository metadata when needed.
4. Keep the plan/checklist updated as items are covered; capture partial results in `review-plan.md`.
5. Log approval prompt in `audit.md`, present review summary, wait for confirmation, update `review-state.md`, remind user to commit artifacts.

## Phase 3 – Provide Feedback

**Goal:** convert findings into actionable feedback and action items.  
**Outputs:** `reports/review-report.md`, `action-items.md`, updated findings with statuses.

**Checklist**

1. Load all findings + context from Phases 1–2. Consolidate duplicates and mark severities.
2. Draft the review report: overview, key issues, risk assessment, remediation guidance, testing recommendations.
3. Populate `action-items.md` with owner, due date, and status for each required fix.
4. Prepare PR-appropriate messaging (summary bullets + blocking items). Note if GitHub issues/comments are required.
5. Log the feedback handoff prompt in `audit.md`, wait for approval, update `review-state.md`, and remind about git commits.

## Phase 4 – Finalize Review

**Goal:** secure final approval decision, share artifacts, and close the workflow.  
**Outputs:** Finalized `review-report.md`, updated audit log, state file marked complete.

**Checklist**

1. Reload everything from prior phases plus any follow-up responses. Confirm action items are tracked.
2. Present final verdict (approve/changes requested/blocked) and highlight outstanding tasks.
3. If GitHub actions are required (review comments, labels, issues), execute via MCP with user approval.
4. Capture final confirmation in `audit.md`, mark Phase 4 complete in `review-state.md`, remind user to commit/push artifacts, and archive references if needed.
