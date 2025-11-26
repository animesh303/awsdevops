# PRIORITY: Code generation workflow overrides other rules when implementing requirements (usually sourced from JIRA) or producing new code artifacts.

## When to use
- Trigger on requests to implement JIRA tickets, build features, or generate IaC/application code.
- Continue through Commit & Push even if commits are optional—the prompt still needs explicit approval.

## Combine with shared guardrails
- Use alongside `common-workflow-guardrails.md` for session continuity, approvals, and git reminders.
- Execute `.amazonq/rules/code-phases/phaseN-*.md` instructions verbatim.

## Welcome message (must use)
> "🚀 **AWS Business Group Code Generation Workflow**  
> Phases: 1) Select requirements 2) Generate code 3) Review & refine 4) Commit & push.  
> Confirm you understand the workflow and are ready to start Phase 1 (Select Requirements)."

Wait for confirmation before starting Phase 1.

## Phase overview
| Phase | Detail file | Focus | Required prompt |
| --- | --- | --- | --- |
| 1. Select Requirements | `code-phases/phase1-select-requirements.md` | List available tickets, pick scope, choose IaC/runtime stack. | "Requirements selected. Generate code?" |
| 2. Generate Code | `code-phases/phase2-generate-code.md` | Produce IaC + app code + tests, create `.code-docs/artifact-mappings.json`. | "Code generated. Review & refine?" |
| 3. Review & Refine | `code-phases/phase3-review-refine.md` | Lint, test, document, address feedback until ready. | "Implementation reviewed. Finalize?" |
| 4. Commit & Push | `code-phases/phase4-commit-push.md` | With approval, commit/push changes; otherwise document manual steps. | "Ready for me to commit and push?" |

## Context loading highlights
- Read `.code-docs/code-state.md` first. If missing, reconstruct using `.code-docs/requirements/*.md`, generated code, and audit entries.
- Requirements source of truth lives under `.jira-docs/requirements/`; always load those files plus selection artefacts (`available-requirements.md`, `requirements-selection.md`).
- When resuming later phases, load generated code (`iac/`, `src/`, `tests/`), quality reports, and the artifact mapping file.
- Summarize what was loaded before proceeding.

## MCP usage
- `aws-mcp-server`: inspect existing AWS resources, validate IaC against quotas/best practices, optionally deploy when user approves.
- `terraform-mcp-server`: read/plan/apply Terraform state as part of validation.
- `git-mcp-server`: manage feature branches, review diffs, craft commits/pushes when Phase 4 is approved.
- Use MCP servers before finalizing changes to ensure recommendations align with actual infrastructure and repo state.

## Deliverables & conventions
- Requirements + analysis → `.code-docs/requirements/{TICKET-ID}_requirements.md`.
- Artifact dependency map → `.code-docs/artifact-mappings.json` (mandatory during Phase 2 for later CI/CD automation).
- IaC code under `iac/{tool}/`, application code under `src/{runtime}-{feature}/`, tests under `tests/{feature}/`.
- Feature names derive from requirement intent, converted to kebab-case (e.g., `user-authentication`).
- Follow runtime/tool standards stored in `code-phases/{language|iac-tool}-standards.md`. Create the file if a new stack appears.
