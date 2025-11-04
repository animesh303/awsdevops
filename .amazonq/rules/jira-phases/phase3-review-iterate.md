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
     - Log each iteration in `.jira-docs/audit.md` with timestamp
   - Repeat confirmation until user approves or iteration limit reached

3. **Update JIRA Ticket Description**: Add/update requirements in JIRA ticket:

   - **Use Ticket Number**: Use the ticket number determined in step 1
   - Read the current JIRA ticket details using `@atlassian-mcp-server/getJiraIssue` for ticket {TICKET-NUMBER}
   - **Error Handling**: If ticket fetch fails:
     - Log error in `.jira-docs/audit.md` with timestamp
     - Inform user: "Unable to fetch ticket details. Please check ticket permissions and try again."
     - Continue with workflow (requirements document is still valid)
   - Read the final requirements document from `.jira-docs/requirements/{TICKET-NUMBER}_requirements.md`
   - **Error Handling**: If requirements file not found:
     - Log error in `.jira-docs/audit.md`
     - Inform user: "Requirements document not found. Please regenerate requirements."
     - **DO NOT PROCEED** until requirements document exists
   - **Format Requirements for JIRA**:
     - Convert markdown headers to JIRA headers: `#` → `h1.`, `##` → `h2.`, `###` → `h3.`
     - Convert markdown lists to JIRA lists: `-` → `*`, numbered lists remain numbered
     - Convert markdown code blocks to JIRA code blocks: ` ``` ` → `{code}...{code}`
     - Convert markdown bold `**text**` to JIRA bold `*text*`
     - Convert markdown italic `*text*` to JIRA italic `_text_`
     - Preserve line breaks and structure
   - Update the JIRA ticket description using `@atlassian-mcp-server/editJiraIssue`:
     - **Append** the requirements section to existing description (preserve original content)
     - Add a clear separator: `----`
     - Include header: `h2. Technical Requirements Specification`
     - Include the full formatted requirements document
     - If description is too long, include a summary with note: "Full requirements available in repository at `.jira-docs/requirements/{TICKET-NUMBER}_requirements.md`"
   - **Error Handling**: If JIRA update fails:
     - Log error in `.jira-docs/audit.md` with timestamp and error details
     - Inform user: "Unable to update JIRA ticket description. Error: [error message]. Requirements document is saved locally."
     - Continue with workflow (don't block on JIRA update failure)

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
   - Log JIRA ticket update and status transition in `.jira-docs/audit.md`
   - **Update State (Graceful)**: Try to update Phase 3 complete in `jira-state.md`. If update fails, continue - artifacts are source of truth.
   - **Git Reminder**: Remind user to commit Phase 3 artifacts to git: "Please commit the final requirements and audit logs to git: `.jira-docs/requirements/`, `.jira-docs/audit.md`, and `.jira-docs/jira-state.md`"
   - Provide summary of final requirements document and JIRA ticket updates
