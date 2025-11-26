# Shared Workflow Guardrails

This file removes repeated boilerplate from every domain workflow. Each workflow now links here for the core control-plane rules (session detection, logging, approvals, etc.). Use the workflow-specific file for domain nuances, but always combine it with this shared baseline.

## Directory + Artifact Map

| Workflow file               | Phase directory    | Project docs root | State file                         | Audit file                | Session continuity                      |
| --------------------------- | ------------------ | ----------------- | ---------------------------------- | ------------------------- | --------------------------------------- |
| `generate-code-workflow.md` | `code-phases/`     | `.code-docs/`     | `.code-docs/code-state.md`         | `.code-docs/audit.md`     | `code-phases/session-continuity.md`     |
| `review-workflow.md`        | `review-phases/`   | `.review-docs/`   | `.review-docs/review-state.md`     | `.review-docs/audit.md`   | `review-phases/session-continuity.md`   |
| `testing-workflow.md`       | `testing-phases/`  | `.test-docs/`     | `.test-docs/test-state.md`         | `.test-docs/audit.md`     | `testing-phases/session-continuity.md`  |
| `docs-workflow.md`          | `docs-phases/`     | `.docs-docs/`     | `.docs-docs/docs-state.md`         | `.docs-docs/audit.md`     | `docs-phases/session-continuity.md`     |
| `security-workflow.md`      | `security-phases/` | `.security-docs/` | `.security-docs/security-state.md` | `.security-docs/audit.md` | `security-phases/session-continuity.md` |
| `cicd-github-workflow.md`   | `cicd-phases/`     | `.cicd-docs/`     | `.cicd-docs/cicd-state.md`         | `.cicd-docs/audit.md`     | `cicd-phases/session-continuity.md`     |
| `jira-task-workflow.md`     | `jira-phases/`     | `.jira-docs/`     | `.jira-docs/jira-state.md`         | `.jira-docs/audit.md`     | `jira-phases/session-continuity.md`     |

> **Tip:** If a project does not yet contain the docs root shown above, create it before writing state/audit files.

## Session Continuity Base Rules

1. **Detect sessions first.** Look for the docs root in the table above. If it exists, read the state file before doing anything else.
2. **Always read the workflow’s `session-continuity.md`** (from the phase directory) and follow the options/template it defines.
3. **If the state file is missing or corrupted**, reconstruct the status from the artifacts the workflow cares about (requirements, tickets, generated assets, etc.), regenerate the state file, and log that action.
4. **Provide a context summary** describing which artifacts were loaded whenever you resume work.

## Smart Context Loading Pattern

Regardless of workflow, every phase resumes by:

1. Loading the docs root + state file to know the phase.
2. Reading any artifacts produced by previous phases (plans, generated assets, reports).
3. Reading the relevant `phaseN-*.md` file from the phase directory.
4. Loading source files referenced by the phase (code, tests, IaC, documentation) rather than relying on memory.
5. Listing the loaded items back to the user before proceeding.

Each workflow may call out additional artifacts (e.g., `.code-docs/requirements/*.md`, `.github/workflows/*`). Follow those specifics as well.

## Phase Execution Loop

For **every** phase across all workflows:

1. Load the associated `phaseN-*.md` instructions and execute them verbatim.
2. Update any plan/checkbox files for that phase within the docs root.
3. Update the state file’s phase checklist and “Current Status” block **in the same interaction** that the work happened.
4. Log the approval prompt in the audit file **before** asking the user.
5. Ask the phase hand-off question and wait for an explicit “yes/approve”.
6. Log the user response with timestamp and approval status.
7. Remind the user to commit artifacts to git after each phase completes.

## Progress Tracking

- **Plan-level tracking**: Any checklist/plan file that exists for the phase must be updated immediately after the corresponding work is done. Do not skip checkboxes.
- **Phase-level tracking**: Only mark the phase complete in the state file after the user approves moving forward. Always refresh the “Current Status” section when anything changes.
- **No silent progress**: Never finish an interaction without updating the relevant plan + state files.

## Audit + Approval Logging

All workflows share a single audit entry format. Record entries in the audit file listed in the table above using ISO‑8601 timestamps.

```
## Phase X: <Phase Name>

**Timestamp**: 2025-01-28T14:32:15Z
**Prompt**: "<Exact text asked to the user>"
**Response**: "<User's exact reply>"
**Status**: Approved | Rejected | Pending
**Context**: <Optional notes>

---
```

Log every approval prompt and response. If a workflow asks additional approval questions inside a phase file, those also belong in the audit log.

## Git + Artifact Hygiene

- After each phase, remind the user to commit/push the generated artifacts (plans, documents, code, workflows, reports, etc.).
- Use workflow-specific naming conventions (documented in each workflow file) when creating new artifacts.
- Keep artifacts under the docs root listed in the table unless the workflow’s file states otherwise.

## Applying Shared + Domain Rules Together

1. Read this file once per session to internalize the guardrails.
2. Read the workflow-specific file to learn triggers, welcome text, unique artifact requirements, MCP usage, and phase table.
3. Execute the workflow by combining both sources—shared control-plane rules from here, domain logic from the workflow file.
4. If a workflow introduces an exception (e.g., JIRA’s “artifacts are the source of truth”), follow that exception but still honor the rest of the shared guardrails.
