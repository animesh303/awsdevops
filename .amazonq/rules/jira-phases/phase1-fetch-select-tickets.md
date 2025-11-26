# Phase 1: Fetch & Select Tickets

Use `jira-phases/blueprint.md#phase-1-%E2%80%93-fetch-%26-select-tickets` for the concise checklist.

**Key reminders**
- Query JIRA via the Atlassian MCP (default JQL: open/to-do statuses) and log any connection errors in `.jira-docs/audit.md` before retrying.
- Store the numbered ticket list in `.jira-docs/tickets/available-tickets.md` and `ticket-selection.md`, prompt the user for a choice, then fetch/store the chosen ticket under `.jira-docs/tickets/`.
- Extract highlights for future phases, log the action, update `jira-state.md` (best effort), and remind the user to commit the ticket artifacts.

