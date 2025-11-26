# CI/CD Phase Blueprint

Use this file as the compact reference for `cicd-phases/phaseN-*.md`. Supporting docs (validation checklist, dependency guide, error handling, rollback) remain available for deep dives.

## Phase 1 – Detect & Plan
**Goal:** discover languages/environments, audit existing workflows, and capture a plan.  
**Outputs:** `.cicd-docs/detection-plan.md`, updated `.cicd-docs/cicd-state.md`, detection summary in `audit.md`.

**Checklist**
1. Load `.cicd-docs/cicd-state.md` (or legacy fallback) and `.code-docs/requirements/` + `.code-docs/artifact-mappings.json` when present.
2. Detect code types, build tools, tests, deploy targets, secrets, and environments. Use the dependency guide for cross-artifact relationships.
3. Record findings + intended workflow architecture (single `ci-cd.yml`) in the detection plan with checkbox updates.
4. Log the Phase‑1 prompt in `.cicd-docs/audit.md`, present the summary to the user, wait for approval, update `cicd-state.md`, and remind them to commit artifacts.

## Phase 2 – Generate Workflow
**Goal:** author `.github/workflows/ci-cd.yml` reflecting the detection plan.  
**Outputs:** workflow file, plan updates, quality/validation notes, updated state.

**Checklist**
1. Reload the detection plan, artifact mapping, requirements, and existing workflows (if any). Summarize context per guardrails.
2. Generate a single workflow triggered on `push` to `main` + `workflow_dispatch`, adding lint/scan/test/build/deploy jobs per code type with `needs:` enforcing dependencies and `environment: production` on deploy steps.
3. Reference standards in `cicd-phases/{code-type}-standards.md`, apply secrets/permissions, artifact uploads/downloads, and branch protections as needed.
4. Run validation (`workflow-lint-validation.md`) and document results.
5. Log the Phase‑2 prompt, wait for approval, update plan/state, remind the user to commit.

## Phase 3 – Review & Confirm
**Goal:** walk through the generated workflow, address feedback, and secure approval.  
**Outputs:** review notes, resolved issues, approval log.

**Checklist**
1. Reload all artifacts (plan, workflow file, validation checklist) and summarize them for the user.
2. Highlight job ordering, dependency handling, secrets usage, rollback/error handling per the supporting docs.
3. Capture requested changes, update the workflow, rerun lint/validation, and document adjustments in `.cicd-docs/review-notes.md`.
4. Log the Phase‑3 prompt, wait for final approval, update `cicd-state.md`, and remind about committing artifacts.

## Phase 4 – Commit & Push (Optional)
**Goal:** commit/push workflow updates only if the user says yes.  
**Outputs:** git commit/push or manual instructions if skipped.

**Checklist**
1. Ask “Ready for me to commit and push the workflow changes to the repository?” and proceed only on approval.
2. Ensure git identity exists, stage `.github/workflows/ci-cd.yml` plus `.cicd-docs/`, commit with a descriptive message, and push to the working branch.
3. On failure or skip, document the manual steps. Always log the interaction and update `cicd-state.md`.

