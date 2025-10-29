# Phase 1: Fetch & Select JIRA Tickets

**Assume the role** of a JIRA integration specialist

**Universal Phase**: Works with any JIRA project - fetches open tickets and allows user selection

1. **Connect to JIRA and Fetch Open Tickets**: Use MCP JIRA integration to retrieve tickets:

   - Use `@atlassian-mcp-server/searchJiraIssuesUsingJql` to fetch open tickets
   - Query: `status in (Open, "In Progress", "To Do", "New") ORDER BY updated DESC`
   - Store ticket list in `jira-docs/tickets/available-tickets.md`
   - Include ticket key, summary, status, assignee, and priority for each ticket

2. **Display Ticket Selection Interface**: Present tickets in a user-friendly format:

   - Show ticket key, summary, status, assignee, and priority
   - Number each ticket for easy selection
   - Store formatted list in `jira-docs/tickets/ticket-selection.md`
   - Ask user to select ticket by number or ticket key

3. **Handle Ticket Selection**: Process user's ticket selection:

   - Validate the selected ticket exists in the fetched list
   - Fetch detailed ticket information using `@atlassian-mcp-server/getJiraIssue`
   - Store complete ticket details in `jira-docs/tickets/ticket-{TICKET-NUMBER}.md`
   - Include all ticket fields, comments, and attachments information

4. **Extract Key Information**: Parse selected ticket for requirements generation:

   - Extract ticket title, description, acceptance criteria
   - Identify ticket type (Story, Bug, Task, Epic)
   - Note any linked tickets or dependencies
   - Store extracted info in `jira-docs/tickets/ticket-{TICKET-NUMBER}-extracted.md`

5. **Log and Proceed**:
   - Log ticket selection with timestamp in `jira-docs/audit.md`
   - Wait for explicit user approval before proceeding
   - Record approval response with timestamp
   - Update Phase 1 complete in jira-state.md
