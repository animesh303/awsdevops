# Phase 4: Commit & Push

Follow `code-phases/blueprint.md#phase-4-%E2%80%93-commit-%26-push` for the precise flow.

**Reminders**
- This phase is optional and must start with the explicit approval prompt (“Do you want me to commit and push…?”). Stop immediately if the user declines.
- On approval: ensure git identity is configured, stage changes, craft the structured commit message (`feat(codegen): …`, `Refs: {TICKET}`), and push to the current branch. Report failures with actionable guidance.
- Always log the interaction in `.code-docs/audit.md`, update `.code-docs/code-state.md`, and remind the user to commit manually if automation is skipped.

