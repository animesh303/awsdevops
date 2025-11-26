# JIRA Phase Blueprint

Each `phaseX-*.md` file now points here to minimize context size. Use the supporting template (`requirements-template.md`) when drafting specs.

## Phase 1 – Fetch & Select Tickets
**Goal:** list open tickets, let the user choose, and capture details.  
**Outputs:** `.jira-docs/tickets/available-tickets.md`, `ticket-selection.md`, `ticket-{KEY}.md`, updated `jira-state.md`.

**Checklist**
1. Use the Atlassian MCP (`searchJiraIssuesUsingJql`) to fetch open tickets; handle errors by logging to `.jira-docs/audit.md` and pausing until resolved.
2. Present a numbered list (key, summary, status, assignee, priority), store it in `ticket-selection.md`, and prompt the user for a choice.
3. Validate the selection, fetch full details (`getJiraIssue`), and save them under `.jira-docs/tickets/`.
4. Extract highlights (description, acceptance criteria, dependencies) into `ticket-{KEY}-extracted.md`, log the action, update `jira-state.md`, and remind the user to commit artifacts.

## Phase 2 – Generate Requirements
**Goal:** create a complete requirements spec (plus architecture diagram + Confluence page) for the selected ticket.  
**Outputs:** `.jira-docs/requirements/{KEY}_requirements.md`, optional architecture diagram PNG, Confluence page link, updated state.

**Checklist**
1. Analyze the ticket (details + extracted summary) for scope, dependencies, and missing info. Record ambiguities as questions.
2. Draft the requirements doc using the standard template: functional/non-functional specs, technical stack, risks, acceptance criteria, and **Open Questions** list with the `[Answer]:` placeholders.
3. Generate an AWS architecture diagram via `mcp_awsdac` when the ticket provides enough detail; embed the image reference in the requirements doc.
4. Block progress until all **blocking** questions (critical gaps) have answers. Non-blocking questions can move to a “Future Clarifications” section if the user prefers.
5. After approval, create or update the Confluence page via Atlassian MCP, store the page ID/URL in state or the ticket file, and log everything in `.jira-docs/audit.md`.
6. Remind the user to commit requirements artifacts (doc, diagram, updated state).

## Phase 3 – Review & Iterate / JIRA Update
**Goal:** capture any follow-up edits, finalize the requirements, and update the ticket.  
**Outputs:** polished requirements doc, updated Confluence page (if needed), JIRA comment/status updates, updated state.

**Checklist**
1. Reload the ticket, requirements doc, Confluence metadata, and audit history; summarize context per the guardrails.
2. Apply user revisions, confirm that Confluence reflects the latest content (update if necessary), and ensure any remaining questions are addressed or tracked.
3. Use Atlassian MCP to comment on the JIRA ticket and/or transition its status per user direction.
4. Log the final confirmation in `.jira-docs/audit.md`, update `.jira-docs/jira-state.md`, and remind the user to commit the latest artifacts.

