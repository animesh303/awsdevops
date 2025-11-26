# PRIORITY: Use this workflow whenever the user wants help with JIRA tickets, requirements intake, or JIRA updates. It overrides other workflows until completion.

## Pair with shared guardrails

- Always combine this file with `common-workflow-guardrails.md` for session continuity, logging, approvals, and git reminders.
- Execute detailed steps from `.amazonq/rules/jira-phases/phaseN-*.md` exactly as written.

## Welcome message (verbatim)

> "🎯 **AWS Business Group JIRA Task Workflow** – Phases:
>
> 1. Fetch & select tickets
> 2. Generate requirements spec
> 3. Final confirmation & JIRA update
>
> Confirm you understand the process and are ready to begin Phase 1 (ticket selection)."

Wait for confirmation before Phase 1.

## Phase overview

| Phase                               | Detail file                                   | Output                                              | Notes                                                  |
| ----------------------------------- | --------------------------------------------- | --------------------------------------------------- | ------------------------------------------------------ |
| 1. Fetch & Select Tickets           | `jira-phases/phase1-fetch-select-tickets.md`  | Ticket inventory + selected ticket file.            | Phase file handles its own approval logging at step 5. |
| 2. Generate Requirements            | `jira-phases/phase2-generate-requirements.md` | `{TICKET}_requirements.md` + clarified questions.   | Phase file manages approvals/questions at step 8.      |
| 3. Final Confirmation & JIRA Update | `jira-phases/phase3-review-iterate.md`        | Approved requirements + JIRA status update summary. | Gather final confirmation before closing.              |

State updates remain “best effort”: update `.jira-docs/jira-state.md` after each phase, but artifacts are the source of truth if the file is missing.

## Context loading rules (hybrid model)

1. Try to read `.jira-docs/jira-state.md` first.
2. If missing/corrupted, infer progress from artifacts: ticket files → Phase 1 done, requirements file → Phase 2 done, audit entry with approval → Phase 3 done. Rebuild the state file immediately and log the reconstruction in `.jira-docs/audit.md`.
3. Load artifacts incrementally per phase: tickets → requirements drafts → audit history. Summarize what you loaded before proceeding.

## Logging & approvals

- Each phase file already specifies where to log prompts/responses; ensure all entries follow the ISO 8601 template in `common-workflow-guardrails.md`.
- After every phase remind the user to commit artifacts (tickets, requirements, audit updates).

## Deliverables & structure

- `.jira-docs/tickets/ticket-{KEY}.md` for ticket summaries pulled from JIRA.
- `.jira-docs/requirements/{KEY}_requirements.md` for the technical spec.
- `.jira-docs/jira-state.md` for lightweight state (current phase + selected ticket).
- `.jira-docs/audit.md` for approvals, clarifications, and state-rebuild notes.
- Additional artifacts (question lists, decisions) live under `.jira-docs/` following kebab-case names.

## Key principles

- Show available tickets first, let the user pick, and confirm selection before writing specs.
- Requirements must be complete, testable, and aligned with the ticket’s acceptance criteria.
- Iterate on open questions within Phase 2 until the user approves the spec.
- Final confirmation (Phase 3) must capture readiness to update JIRA plus any follow-up tasks.
