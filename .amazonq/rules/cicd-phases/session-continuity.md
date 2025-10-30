# CICD Session Continuity

## Purpose

Ensure CICD GitHub workflow generation can resume seamlessly if interrupted or already in progress.

## State Files

- Preferred (project-scoped): `.cicd-docs/cicd-state.md` and `.cicd-docs/audit.md`
  - Tracks: current phase, detected environments, generated files, decisions/approvals with timestamps
- Legacy fallback: `.amazonq/rules/cicd-phases/cicd-state.md` (read/write only if project-scoped files are absent)

## Detect Existing Session

1. Check for `.cicd-docs/cicd-state.md` (preferred). If not found, check `.amazonq/rules/cicd-phases/cicd-state.md` (legacy).
2. If present, read:
   - `current_phase` (detect-plan | generate-workflow | review-confirm | complete)
   - `detected_envs` (python, terraform)
   - `generated_files` (list of workflow file paths)
   - `pending_confirmation` (boolean/message)
3. If absent, initialize `.cicd-docs/cicd-state.md` with `current_phase: detect-plan` and empty fields. Also create `.cicd-docs/audit.md`.

## Resume Logic

- If `current_phase: detect-plan` → proceed with Phase 1 steps; on completion, set `current_phase: generate-workflow`.
- If `current_phase: generate-workflow` → proceed with Phase 2; on completion, set `current_phase: review-confirm`.
- If `current_phase: review-confirm` → proceed with Phase 3; on approval, set `current_phase: complete`.
- If `current_phase: complete` → inform user CICD workflows are already finalized; offer to re-run or modify.

## Update State on Each Phase

- After each phase completes and the user confirms:
  - Update `current_phase` to the next phase
  - Persist `detected_envs` (Phase 1)
  - Persist `generated_files` (Phase 2)
  - Persist confirmations/decisions (Phase 1-3) to `.cicd-docs/audit.md`

## Confirmations

- Enforce explicit confirmation before advancing phases. Record confirmation text and timestamp in `.cicd-docs/audit.md`.

## Welcome Back Prompt Template (In-Chat)

When a user returns to continue CICD workflow generation, present this prompt DIRECTLY IN CHAT:

**Welcome back! I can see you have an existing CICD workflow generation in progress.**

Based on your cicd-state.md, here's your current status:

- **Detected Environments**: [python/terraform]
- **Current Phase**: [Phase X: Phase Name]
- **Generated Files**: [list]
- **Last Completed**: [Last completed step]
- **Next Step**: [Next step to work on]

What would you like to do next?

A) Continue where you left off ([Next step description])
B) Review detected environments and the plan
C) Review generated workflow files
D) Start over (re-run detection and planning)

Please select an option (A, B, C, or D):

## Failure/Abort Handling

- On errors, record error details and last successful step in `.cicd-docs/audit.md` and update `.cicd-docs/cicd-state.md`.
- Allow user to retry current phase or roll back changes from Phase 2 if needed.

## Example cicd-state.md (minimal)

```
current_phase: generate-workflow
Detected envs: [python, terraform]
Generated files:
- .github/workflows/python-ci.yml
- .github/workflows/terraform-ci.yml
Pending confirmation: "Workflows generated. Ready to review and confirm?"
Last updated: 2025-10-30T12:34:56Z
```
