# Phase 3: Final Confirmation & JIRA Update

**Assume the role** of a requirements review specialist

**Universal Phase**: Works with any generated requirements document to seek final confirmation and update JIRA ticket

1. **Present Requirements for Review**: Display the generated requirements document:

   - **Get Ticket Number**: Retrieve ticket number from one of:
     - Selected ticket stored in `.jira-docs/jira-state.md` (Selected Ticket field)
     - Ticket file name pattern: `ticket-{TICKET-NUMBER}.md` in `.jira-docs/tickets/`
     - Requirements file name pattern: `{TICKET-NUMBER}_requirements.md` in `.jira-docs/requirements/`
   - Read the complete requirements document from `.jira-docs/requirements/{TICKET-NUMBER}_requirements.md`
   - Present the requirements document to the user in a clear, formatted way
   - Highlight key sections: Functional Requirements, Non-Functional Requirements, Technical Specifications, Acceptance Criteria

2. **Seek Final Confirmation**: Ask for user approval:

   - Ask: "**Please review the requirements document above. Are you satisfied with these requirements and ready to proceed?**"
   - **DO NOT PROCEED** until user confirms approval
   - **Iteration Handling**: If user requests changes:
     - **Maximum 3 iterations**: Allow up to 3 rounds of feedback and updates
     - After each change, ask: "Are there any other changes needed?"
     - After 3 iterations, if user still requests changes:
       - Inform user: "We've completed 3 iterations. Please review the current requirements. If additional changes are needed, we can proceed to Phase 3 and update the requirements document, or you can manually edit it."
       - Ask: "Would you like to proceed with the current requirements, or do you need more time to review?"
       - Allow user to proceed or pause
     - Ask them to specify what needs to be modified
     - Update the requirements document based on user feedback
     - **MANDATORY: Update Confluence Page**: After updating requirements document, update the Confluence page:
       - Get Confluence page ID from `.jira-docs/jira-state.md` or ticket file
       - Read updated requirements document from `.jira-docs/requirements/{TICKET-NUMBER}_requirements.md`
       - Use `@atlassian-mcp-server/updateConfluencePage` to update the page with new content
       - Log Confluence update in `.jira-docs/audit.md` with timestamp
     - Log each iteration in `.jira-docs/audit.md` with timestamp
   - Repeat confirmation until user approves or iteration limit reached

3. **Add Confluence Page Link to JIRA Ticket**: Add a comment to the JIRA ticket with the Confluence page link:

   - **Use Ticket Number**: Use the ticket number determined in step 1
   - **Get Confluence Page Information**: Retrieve Confluence page details from:
     - `.jira-docs/jira-state.md` (Confluence Page URL, Page ID)
     - Or `.jira-docs/tickets/ticket-{TICKET-NUMBER}.md` (if stored there)
   - **Error Handling**: If Confluence page information not found:
     - Log warning in `.jira-docs/audit.md` with timestamp
     - Inform user: "Confluence page information not found. Please ensure Phase 2 completed successfully and Confluence page was created."
     - **DO NOT PROCEED** to comment if Confluence page URL is not available
   - **Read Current Ticket**: Read the current JIRA ticket details using `@atlassian-mcp-server/getJiraIssue` for ticket {TICKET-NUMBER}
   - **Error Handling**: If ticket fetch fails:
     - Log error in `.jira-docs/audit.md` with timestamp
     - Inform user: "Unable to fetch ticket details. Please check ticket permissions and try again."
     - Continue with workflow (requirements document is still valid)
   - **Add Comment to JIRA Ticket**: Add a comment with Confluence page link using `@atlassian-mcp-server/addCommentToJiraIssue`:

     - `cloudId`: Get from `@atlassian-mcp-server/getAccessibleAtlassianResources` if needed
     - `issueIdOrKey`: {TICKET-NUMBER}
     - `commentBody`: Use markdown format:

       ```
       Technical Requirements Specification has been generated and published to Confluence.

       **Confluence Page**: [Technical Requirements: {TICKET-NUMBER} - {TICKET-TITLE}]({CONFLUENCE_PAGE_URL})

       The requirements document includes:
       * Functional Requirements
       * Non-Functional Requirements
       * Technical Specifications
       * Architecture Diagram
       * Acceptance Criteria
       * Dependencies and Risks

       Please review the requirements in Confluence and provide feedback if needed.
       ```

     - Replace placeholders: {TICKET-NUMBER}, {TICKET-TITLE}, {CONFLUENCE_PAGE_URL} with actual values

   - **Error Handling**: If comment addition fails:
     - Log error in `.jira-docs/audit.md` with timestamp and error details
     - Inform user: "Unable to add comment to JIRA ticket. Error: [error message]. Confluence page is available at: {CONFLUENCE_PAGE_URL}"
     - Continue with workflow (don't block on comment failure)
   - **Log Comment Status**: Log comment addition status in `.jira-docs/audit.md` with timestamp

4. **Transition JIRA Ticket to "In Progress"**: Update ticket status:

   - **Use Ticket Number**: Use the ticket number determined in step 1
   - Read current ticket status using `@atlassian-mcp-server/getJiraIssue` for ticket {TICKET-NUMBER}
   - **Check Current Status**: If ticket is already "In Progress" or "In Review", skip transition and log in audit.md
   - **Validate Transitions**: Get available transitions for the ticket using `@atlassian-mcp-server/getTransitionsForJiraIssue` for ticket {TICKET-NUMBER}
   - **Find Transition**: Identify the transition ID for "In Progress" status (check transition names: "In Progress", "Start Progress", "Begin Work")
   - **Transition Ticket**: If "In Progress" transition is available:
     - Transition the ticket using `@atlassian-mcp-server/transitionJiraIssue`:
       - Use the transition ID for "In Progress"
       - Add a comment: "Requirements specification complete. Moving ticket to In Progress."
   - **Handle Missing Transition**: If "In Progress" transition is not available:
     - Log available transitions in `.jira-docs/audit.md` with timestamp
     - Inform user: "Ticket cannot transition to 'In Progress'. Available transitions: [list]. Current status: [status]"
     - Continue with workflow (don't block)
   - **Error Handling**: If transition fails for other reasons:
     - Log error in `.jira-docs/audit.md` with timestamp and error details
     - Inform user: "Unable to transition ticket. Error: [error message]. Requirements are complete and approved."
     - Continue with workflow (don't block on transition failure)

5. **Finalize and Log**:
   - Mark requirements as final and approved
   - Log final approval with timestamp in `.jira-docs/audit.md`
   - Log JIRA ticket comment with Confluence link and status transition in `.jira-docs/audit.md`
   - **Update State (Graceful)**: Try to update Phase 3 complete in `jira-state.md`. If update fails, continue - artifacts are source of truth.
   - **Git Reminder**: Remind user to commit Phase 3 artifacts to git: "Please commit the final requirements and audit logs to git: `.jira-docs/requirements/`, `.jira-docs/audit.md`, and `.jira-docs/jira-state.md`"
   - Provide summary of Confluence page link added to JIRA ticket comment and ticket status updates
