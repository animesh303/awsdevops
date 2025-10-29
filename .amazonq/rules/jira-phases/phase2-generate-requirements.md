# Phase 2: Generate Requirements Spec

**Assume the role** of a technical requirements specialist

**Universal Phase**: Works with any selected JIRA ticket to generate comprehensive requirements

1. **Analyze Selected JIRA Ticket**: Review the ticket details and extracted information:

   - Read ticket details from `jira-docs/tickets/ticket-{TICKET-NUMBER}.md`
   - Review ticket description, acceptance criteria, and comments
   - Identify technical scope and complexity
   - Note any dependencies or linked tickets

2. **Generate Technical Requirements Document**: Create comprehensive requirements spec:

   - Create `jira-docs/requirements/{TICKET-NUMBER}_requirements.md`
   - Follow the standard requirements template structure
   - Include all mandatory sections as defined in requirements template
   - Ensure requirements are specific, measurable, and testable

3. **Requirements Document Structure**: Include these mandatory sections:

   - **Project Overview**: Brief description of the ticket and its purpose
   - **Functional Requirements**: Detailed functional specifications
   - **Non-Functional Requirements**: Performance, security, scalability requirements
   - **Technical Specifications**: Technology stack, architecture, and implementation details
   - **Acceptance Criteria**: Clear, testable criteria for completion
   - **Dependencies**: Any dependencies on other tickets or systems
   - **Assumptions**: Key assumptions made during requirements gathering
   - **Risks**: Potential risks and mitigation strategies

4. **Validate Requirements Quality**: Ensure requirements meet standards:

   - Check for completeness and clarity
   - Verify requirements are testable and measurable
   - Ensure technical specifications are detailed enough for implementation
   - Validate that acceptance criteria align with JIRA ticket requirements

5. **Log and Proceed**:
   - Log requirements generation with timestamp in `jira-docs/audit.md`
   - Wait for explicit user approval before proceeding
   - Record approval response with timestamp
   - Update Phase 2 complete in jira-state.md
