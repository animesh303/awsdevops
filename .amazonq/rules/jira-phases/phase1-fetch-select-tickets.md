# Phase 1: Fetch & Select JIRA Tickets

**Assume the role** of a JIRA integration specialist

**Universal Phase**: Works with any JIRA project - fetches open tickets and allows user selection

1. **Connect to JIRA and Fetch Open Tickets**: Use MCP JIRA integration to retrieve tickets:

   - Use `@atlassian-mcp-server/searchJiraIssuesUsingJql` to fetch open tickets
   - Query: `status in (Open, "In Progress", "To Do", "New") ORDER BY updated DESC`
   - **Error Handling**: If JIRA API call fails:
     - Check network connectivity and JIRA server availability
     - Verify authentication credentials are configured
     - Log error in `.jira-docs/audit.md` with timestamp and error details
     - Inform user: "Unable to connect to JIRA. Please check your connection and credentials."
     - **DO NOT PROCEED** until JIRA connection is established
   - Store ticket list in `.jira-docs/tickets/available-tickets.md`
   - Include ticket key, summary, status, assignee, and priority for each ticket

2. **Display Ticket Selection Interface**: Present tickets in a user-friendly format:

   - Show ticket key, summary, status, assignee, and priority
   - Number each ticket for easy selection
   - Store formatted list in `.jira-docs/tickets/ticket-selection.md`
   - Ask user to select ticket by number or ticket key

3. **Handle Ticket Selection**: Process user's ticket selection:

   - Validate the selected ticket exists in the fetched list
   - **Error Handling**: If ticket not found:
     - Inform user: "Ticket {TICKET-NUMBER} not found in available tickets. Please select a valid ticket."
     - Return to step 2 to allow re-selection
   - Fetch detailed ticket information using `@atlassian-mcp-server/getJiraIssue`
   - **Error Handling**: If ticket fetch fails:
     - Log error in `.jira-docs/audit.md` with timestamp
     - Inform user: "Unable to fetch ticket details. Please try again or check ticket permissions."
     - **DO NOT PROCEED** until ticket details are successfully retrieved
   - Store complete ticket details in `.jira-docs/tickets/ticket-{TICKET-NUMBER}.md`
   - **Error Handling**: If file write fails:
     - Log error in `.jira-docs/audit.md`
     - Inform user but continue (ticket details are in memory)
   - Include all ticket fields, comments, and attachments information

4. **Extract Key Information**: Parse selected ticket for requirements generation:

   - Extract ticket title, description, acceptance criteria
   - Identify ticket type (Story, Bug, Task, Epic)
   - Note any linked tickets or dependencies
   - Store extracted info in `.jira-docs/tickets/ticket-{TICKET-NUMBER}-extracted.md`

5. **Log and Proceed**:
   - Log ticket selection with timestamp in `.jira-docs/audit.md`
   - Wait for explicit user approval before proceeding
   - Record approval response with timestamp
   - **Update State (Graceful)**: Try to update Phase 1 complete in `jira-state.md`. If update fails, continue - artifacts are source of truth.
   - **Git Reminder**: Remind user to commit Phase 1 artifacts to git: "Please commit the ticket selection artifacts to git: `.jira-docs/tickets/` and `.jira-docs/jira-state.md`"
