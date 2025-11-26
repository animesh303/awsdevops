# PRIORITY: This CI/CD workflow overrides all other rules whenever the user asks to create, update, or regenerate GitHub Actions workflows.

## Pair with shared guardrails

- Always read `common-workflow-guardrails.md` first for session detection, approvals, checkbox tracking, audit logging, and git reminders.
- For implementation details execute `.amazonq/rules/cicd-phases/phaseN-*.md` files verbatim.

## Welcome + regeneration

1. If the user says “regenerate/refresh/update/recreate workflows,” delete `.cicd-docs/` and `.github/workflows/`, log the request in the new `.cicd-docs/audit.md`, then start at Phase 1.
2. Otherwise read `.cicd-docs/cicd-state.md` (fallback `cicd-phases/cicd-state.md`) and follow `cicd-phases/session-continuity.md`.
3. Send this message verbatim and wait for confirmation before Phase 1:
   > "🚀 **AWS Business Group CI/CD Workflow Generation** – Phases:
   >
   > 1. Detect & plan
   > 2. Generate workflow
   > 3. Review & confirm
   > 4. Commit & push
   >
   > Confirm you understand the process and are ready to begin Phase 1 (Detect & Plan)."

## Phase summary

| Phase                | Detail file                               | Output                                                         | Required prompt                                     |
| -------------------- | ----------------------------------------- | -------------------------------------------------------------- | --------------------------------------------------- |
| 1. Detect & Plan     | `cicd-phases/phase1-detect-plan.md`       | Updated detection plan + code type inventory + dependency map. | "Detection & planning complete. Generate workflow?" |
| 2. Generate Workflow | `cicd-phases/phase2-generate-workflow.md` | `.github/workflows/ci-cd.yml` plus plan/state updates.         | "Workflow generated. Review & confirm?"             |
| 3. Review & Confirm  | `cicd-phases/phase3-review-confirm.md`    | Reviewed jobs, validation checklist, dependency notes.         | "Workflow reviewed. Approve integration?"           |
| 4. Commit & Push     | `cicd-phases/phase4-commit-push.md`       | Commit/push (with approval) or manual handoff notes.           | "Ready for me to commit and push?"                  |

Plan checklists live in `.cicd-docs/detection-plan.md`, `workflow-generation-plan.md`, and `review-notes.md`. Update checkboxes immediately after completing each step; update `.cicd-docs/cicd-state.md` only after approvals.

## Context loading checklist

- Load `.cicd-docs/cicd-state.md`, prior plans, and audit entries at the start of every session.
- Load `.code-docs/requirements/*.md` plus `.code-docs/artifact-mappings.json` to understand dependencies.
- Inspect current `.github/workflows/*.yml` files before replacing them.
- Summarize the artifacts you loaded before continuing.

## Workflow contract

- Produce exactly one workflow: `.github/workflows/ci-cd.yml` (kebab-case).
- Triggers: `push` on `main` and `workflow_dispatch`.
- For each detected code type add lint/scan/test → build → deploy jobs. Use `needs:` to enforce ordering; pass artifacts between jobs when dependencies exist (e.g., Terraform waits for Lambda package).
- All deploy jobs use `environment: production`. No additional workflows or environments.
- Validate YAML structure, `${{ }}` expressions, required permissions, and ensure the file passes `gh workflow lint`.

## MCP integration

- `github-mcp-server`: inspect repo settings, secrets, existing workflows; trigger runs; post review comments or PR statuses.
- `aws-mcp-server`: verify IAM roles, deployment targets, and environment readiness referenced in jobs.
- `docker-mcp-server`: validate container build/push steps and registry credentials.

## Dependency analysis

- Use requirements + artifact mapping files to build a dependency graph (e.g., Lambda build → Terraform deploy).
- Reflect dependencies inside the single workflow via `needs:` or artifact downloads. Document the order in review summaries.

## Language-specific standards

- Before generating jobs for any code type, read `cicd-phases/{code-type}-standards.md` (python, terraform, javascript, java, go, docker, kubernetes, cloudformation, cdk, etc.).
- If a standards file is missing, create it following the existing style before writing workflow steps for that stack.

## Required artifacts

- `.cicd-docs/` → `cicd-state.md`, `audit.md`, and all plan/checklist files (Phase 1–3). Keep them updated in-place.
- `.github/workflows/ci-cd.yml` → final workflow file (single production pipeline).
- Reference supporting docs (`workflow-dependency-handling.md`, `validation-checklist.md`, `error-handling.md`, `rollback-procedures.md`) instead of copying their content.
