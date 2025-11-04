# Phase 2: Generate Requirements Spec

**Assume the role** of a technical requirements specialist

**Universal Phase**: Works with any selected JIRA ticket to generate comprehensive requirements

1. **Analyze Selected JIRA Ticket**: Review the ticket details and extracted information:

   - Read ticket details from `.jira-docs/tickets/ticket-{TICKET-NUMBER}.md`
   - Review ticket description, acceptance criteria, and comments
   - Identify technical scope and complexity
   - Note any dependencies or linked tickets

2. **MANDATORY: Ambiguity Analysis**: Before generating requirements, analyze the JIRA ticket for:

   - **Missing Information**: Any critical details not present in the ticket
   - **Ambiguous Requirements**: Vague or unclear descriptions
   - **Unspecified Criteria**: Missing acceptance criteria or success metrics
   - **Technical Gaps**: Missing technical specifications needed for implementation
   - **Unclear Dependencies**: Ambiguous relationships with other tickets or systems
   - **Incomplete Context**: Missing business context or user needs

3. **Generate Technical Requirements Document**: Create comprehensive requirements spec:

   - Create `.jira-docs/requirements/{TICKET-NUMBER}_requirements.md`
   - Follow the standard requirements template structure
   - Include all mandatory sections as defined in requirements template
   - **CRITICAL: NO ASSUMPTIONS**: Only include information explicitly stated in the ticket or clearly inferable. For any missing or ambiguous information, add follow-up questions directly in the "Open Questions" section using the format:
     ```
     1. Question statement?
        [Answer]:
     ```

4. **MANDATORY: Add Follow-up Questions**: For ANY missing or ambiguous information identified in step 2, add specific follow-up questions to the requirements document:

   - Add questions in the "Open Questions" section using the format:
     ```
     1. Question statement?
        [Answer]:
     ```
   - Make questions specific and actionable
   - Do NOT make assumptions - ask instead
   - Each question should be structured with the question on one line, and `[Answer]:` on the next line with indentation, followed by empty space
   - Examples of good follow-up questions:

     ```
     1. You mentioned 'high performance' - what specific response time requirements do you need? (e.g., < 200ms for API calls)
        [Answer]:

     2. The ticket mentions 'scalable solution' - what is the expected traffic volume? (requests per second, concurrent users)
        [Answer]:

     3. The ticket doesn't specify authentication method - should this use API keys, OAuth, or another authentication mechanism?
        [Answer]:

     4. You mentioned 'integration with external system' - which system and what integration pattern? (REST API, message queue, event-driven)
        [Answer]:
     ```

5. **Requirements Document Structure**: Include these mandatory sections:

   - **Project Overview**: Brief description of the ticket and its purpose (only if clear from ticket)
   - **Functional Requirements**: Detailed functional specifications (only what is clear from ticket)
   - **Non-Functional Requirements**: Performance, security, scalability requirements (only if specified)
   - **Technical Specifications**: Technology stack, architecture, and implementation details (only if clear)
   - **Acceptance Criteria**: Clear, testable criteria for completion (from ticket or clarified)
   - **Dependencies**: Any dependencies on other tickets or systems (only if explicitly stated)
   - **Assumptions**: **MUST BE EMPTY** - No assumptions should be made. If information is missing, use Open Questions section.
   - **Risks**: Potential risks and mitigation strategies (only if can be identified from ticket)
   - **Open Questions**: **MANDATORY** - All ambiguous or missing information as questions with format:
     ```
     1. Question statement?
        [Answer]:
     ```

6. **Validate Requirements Quality**: Ensure requirements meet standards:

   - Check for completeness and clarity
   - Verify requirements are testable and measurable
   - Ensure technical specifications are detailed enough for implementation (or flagged as questions)
   - Validate that acceptance criteria align with JIRA ticket requirements
   - **CRITICAL**: Verify that no assumptions were made - all gaps must be in Open Questions section

7. **MANDATORY: Review Before Approval**: Before asking for user approval:

   - Check if Open Questions section has any questions with `[Answer]:` followed by empty space (not filled in)
   - **Categorize Questions**:
     - **Blocking Questions**: Questions about critical information needed for implementation (e.g., authentication method, data formats, API endpoints, performance requirements, security requirements, core functionality)
     - **Non-Blocking Questions**: Questions about optional features, nice-to-have details, or information that can be clarified during implementation (e.g., preferred UI styling, documentation format, deployment schedule preferences)
   - **If blocking questions exist**:
     - Present the requirements document to the user
     - Ask: "**Please review the requirements document and update the [Answer]: fields in the Open Questions section for all blocking questions. Edit the file `.jira-docs/requirements/{TICKET-NUMBER}_requirements.md` directly. Fill in the empty space after `[Answer]:` with your response.**"
     - **DO NOT PROCEED** until all blocking questions have `[Answer]:` filled in (not empty)
     - Verify that all blocking questions have been answered by checking the requirements document (look for text after `[Answer]:`)
   - **If only non-blocking questions exist**:
     - Present them to the user but allow proceeding with approval
     - Ask user if they want to answer non-blocking questions now or move them to a "Future Clarifications" section
     - If user wants to proceed, move non-blocking questions to "Future Clarifications" section
   - **After user updates**: Re-read the requirements document to verify answers
   - Remove or mark answered questions as complete in Open Questions section
   - **DO NOT PROCEED** to approval until all **blocking** questions have `[Answer]:` filled in (have text after the colon)

8. **Log and Proceed**:
   - Log requirements generation with timestamp in `.jira-docs/audit.md`
   - **Wait for explicit user approval** - only after all blocking questions are answered
   - Record approval response with timestamp
   - **Update State (Graceful)**: Try to update Phase 2 complete in `jira-state.md`. If update fails, continue - artifacts are source of truth.
   - **Git Reminder**: Remind user to commit Phase 2 artifacts to git: "Please commit the requirements document to git: `.jira-docs/requirements/{TICKET-NUMBER}_requirements.md` and updated `.jira-docs/jira-state.md`"
