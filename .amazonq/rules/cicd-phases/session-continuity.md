# CICD Session Continuity

## Purpose

Ensure CICD GitHub workflow generation can resume seamlessly if interrupted or already in progress. Supports language-agnostic detection and single production workflow (triggered by main branch) generation.

## State Files

- Preferred (project-scoped): `.cicd-docs/cicd-state.md` and `.cicd-docs/audit.md`
  - Tracks: current phase, detected code types, existing workflows, generated files (single production workflow: `ci-cd.yml`), decisions/approvals with timestamps
  - Legacy fallback: `.amazonq/rules/cicd-phases/cicd-state.mdc` (read/write only if project-scoped files are absent)

## Detect Existing Session

1. **Check for Re-generation Request First**:

   - If user explicitly requests "regenerate", "re-generate", "refresh", "update", or "recreate" workflows:
     - **Delete `.cicd-docs/` directory** (removes all state files, plan documents, and audit logs)
     - **Delete `.github/workflows/` directory** (removes all existing workflow files)
     - This ensures a completely clean start with no legacy artifacts
     - After cleanup, create new `.cicd-docs/` directory and initialize fresh `.cicd-docs/cicd-state.md` with `current_phase: detect-plan` and empty fields
     - Log regeneration request in new `.cicd-docs/audit.md` with timestamp
     - Proceed as new session (skip existing session detection)

2. **Normal Session Detection**:
   - Check for `.cicd-docs/cicd-state.md` (preferred). If not found, check `.amazonq/rules/cicd-phases/cicd-state.mdc` (legacy).
   - If present, read:
     - `current_phase` (detect-plan | generate-workflow | review-confirm | complete)
     - `detected_code_types` (list of all detected code types: python, terraform, javascript, java, go, docker, kubernetes, etc.)
     - `existing_workflows` (list of existing workflow files and their status: keep/modify/remove)
     - `generated_files` (list of workflow file paths: single unified workflow, e.g., `ci-cd.yml`)
     - `pending_confirmation` (boolean/message)
   - If absent, initialize `.cicd-docs/cicd-state.md` with `current_phase: detect-plan` and empty fields. Also create `.cicd-docs/audit.md`.

## Resume Logic

- If `current_phase: detect-plan` → proceed with Phase 1 steps; on completion, set `current_phase: generate-workflow`.
- If `current_phase: generate-workflow` → proceed with Phase 2; on completion, set `current_phase: review-confirm`.
- If `current_phase: review-confirm` → proceed with Phase 3; on approval, set `current_phase: complete`.
- If `current_phase: complete` → inform user CICD workflows are already finalized; offer to re-run, modify, or regenerate.
- If user selects option E (Regenerate) or explicitly requests regeneration → delete `.cicd-docs/` and `.github/workflows/` directories, create new session, start from Phase 1.

## Update State on Each Phase

- After each phase completes and the user confirms:
  - Update `current_phase` to the next phase
  - Persist `detected_code_types` (Phase 1)
  - Persist `existing_workflows` analysis (Phase 1)
  - Persist `generated_files` (Phase 2) - includes single unified workflow (`ci-cd.yml`)
  - Persist confirmations/decisions (Phase 1-3) to `.cicd-docs/audit.md`

## Confirmations

- Enforce explicit confirmation before advancing phases. Record confirmation text and timestamp in `.cicd-docs/audit.md`.

## Welcome Back Prompt Template (In-Chat)

When a user returns to continue CICD workflow generation, present this prompt DIRECTLY IN CHAT:

**Welcome back! I can see you have an existing CICD workflow generation in progress.**

Based on your cicd-state.md, here's your current status:

- **Detected Code Types**: [python, terraform, javascript, etc.]
- **Existing Workflows**: [list of existing workflows and their status]
- **Current Phase**: [Phase X: Phase Name]
- **Generated Files**: [unified workflow: ci-cd.yml]
- **Last Completed**: [Last completed step]
- **Next Step**: [Next step to work on]

What would you like to do next?

A) Continue where you left off ([Next step description])
B) Review detected code types and the plan
C) Review generated workflow files
D) Start over (re-run detection and planning)
E) Regenerate workflows (create new session, previous workflows may be removed)

Please select an option (A, B, C, D, or E):

## Failure/Abort Handling

- On errors, record error details and last successful step in `.cicd-docs/audit.md` and update `.cicd-docs/cicd-state.md`.
- Allow user to retry current phase or roll back changes from Phase 2 if needed.

## Example cicd-state.md (minimal)

```
current_phase: generate-workflow
Detected code types: [python, terraform, javascript]
Requirements Files Loaded: [".code-docs/requirements/AWS-5_requirements.md", ".code-docs/requirements/AWS-5-analysis.md"]
Dependency Map: [{code-type: "terraform", depends_on: "python", artifacts: ["lambda-package.zip"]}]
Existing workflows:
- .github/workflows/python-ci.yml (modify)
- .github/workflows/old-workflow.yml (remove)
Generated files:
- .github/workflows/ci-cd.yml
Pending confirmation: "Workflows generated. Ready to review and confirm?"
Last updated: 2025-10-30T12:34:56Z
```
