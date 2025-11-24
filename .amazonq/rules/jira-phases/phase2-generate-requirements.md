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

3a. **MANDATORY: Generate AWS Architecture Diagram**: After creating the initial requirements document, generate an AWS architecture diagram:

- **Analyze Requirements for Architecture**: Review the generated requirements document, especially:
  - Section 4 (Technical Specifications) - AWS Services, Architecture Approach
  - Section 2 (Functional Requirements) - Core functionality and data flow
  - Section 3 (Non-Functional Requirements) - Security, networking, storage needs
- **Extract Architecture Components**: Identify AWS services and components mentioned or implied:
  - Compute services (Lambda, EC2, ECS, EKS, etc.)
  - Storage services (S3, DynamoDB, RDS, etc.)
  - Networking (API Gateway, VPC, Load Balancer, CloudFront, etc.)
  - Security (IAM, Cognito, Secrets Manager, KMS, etc.)
  - Integration points and data flow
- **Generate Diagram YAML**: Create a diagram-as-code YAML specification based on the requirements:
  - Use `mcp_awsdac-mcp-server_getDiagramAsCodeFormat` to get format specification if needed
  - Construct YAML following diagram-as-code format with:
    - DefinitionFiles section referencing AWS icon definitions
    - Resources section with hierarchical AWS resource structure
    - Canvas as root container
    - Links section for relationships and data flow
  - Map requirements to appropriate AWS resource types
  - Include logical groupings (VPC, subnets, security groups, etc.)
- **Generate Diagram Image**: Use MCP server to generate the diagram at `.jira-docs/requirements/` directory:
  - Call `mcp_awsdac-mcp-server_generateDiagramToFile` with:
    - `yamlContent`: The complete diagram-as-code YAML specification
    - `outputFilePath`: `.jira-docs/requirements/{TICKET-NUMBER}-architecture-diagram.png`
  - If diagram generation fails or requirements are too ambiguous, add a note in the requirements document that diagram generation was skipped due to insufficient architecture details
  - **Note**: ALWAYS verify that the architecture digram is file is successfully generated at `project-root/.jira-docs/requirements/` directory.
- **Embed Diagram in Requirements**: After successful generation, embed the diagram in the requirements document:
  - Add the diagram image reference in Section 4.1 (Architecture) of the requirements document
  - Use markdown image syntax: `![Architecture Diagram](./{TICKET-NUMBER}-architecture-diagram.png)`
  - Add a caption: "**Figure 1: AWS Architecture Diagram**"
  - Place the diagram after the "Architecture Approach" description and before "Technology Stack"
- **Note**: If the requirements don't contain enough information to generate a meaningful architecture diagram (e.g., no AWS services specified, too vague), skip diagram generation and add a note in the Open Questions section asking for architecture details

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

8. **Log and Request Approval**:

   - Log requirements generation with timestamp in `.jira-docs/audit.md`
   - **Wait for explicit user approval** - only after all blocking questions are answered
   - Ask: "**Requirements document is ready. Please review and confirm if you're satisfied with the requirements, or if any changes are needed before we proceed to create the Confluence page.**"
   - Record approval response with timestamp
   - **DO NOT PROCEED** to Confluence creation until user approves

9. **MANDATORY: Create or Update Confluence Page**: After user approval, create or update a Confluence page with the requirements content:

   - **Get Atlassian Cloud ID**: Use `@atlassian-mcp-server/getAccessibleAtlassianResources` to get the cloudId
   - **Get Confluence Space**: Use `@atlassian-mcp-server/getConfluenceSpaces` to get available spaces:
     - If a space key is specified in environment/config, use that space
     - Otherwise, search for a space with key matching pattern (e.g., current repository name, "REQ", "REQUIREMENTS", "DOCS", or ask user to specify)
     - If no suitable space found, use the first available space or ask user to specify space key
   - **Read Requirements Document**: Read the complete requirements document from `.jira-docs/requirements/{TICKET-NUMBER}_requirements.md`
   - **Prepare Confluence Content**: Convert markdown to Confluence-compatible markdown format:
     - Confluence markdown supports most standard markdown syntax
     - Keep the same structure and formatting
     - Note: Architecture diagram image reference will need to be handled separately (Confluence doesn't support relative image paths from markdown)
   - **Check for Existing Page**: Try to find existing page with title matching pattern:
     - Search for pages with title: "Technical Requirements: {TICKET-NUMBER}" or "{TICKET-NUMBER} Requirements"
     - Use `@atlassian-mcp-server/searchConfluenceUsingCql` with CQL: `space = "{SPACE_KEY}" AND title ~ "{TICKET-NUMBER} Requirements"`
     - Or check if page ID was previously stored in `.jira-docs/jira-state.md` or ticket file
   - **Create or Update Page**:
     - **If page exists**: Use `@atlassian-mcp-server/updateConfluencePage`:
       - `cloudId`: From step above
       - `pageId`: From search or stored ID
       - `body`: Requirements document content (markdown format)
       - `title`: "Technical Requirements: {TICKET-NUMBER} - {TICKET-TITLE}" (optional update)
     - **If page does not exist**: Use `@atlassian-mcp-server/createConfluencePage`:
       - `cloudId`: From step above
       - `spaceId`: Numerical space ID from getConfluenceSpaces
       - `title`: "Technical Requirements: {TICKET-NUMBER} - {TICKET-TITLE}"
       - `body`: Requirements document content (markdown format)
   - **Get Page URL**: After creating/updating, get the Confluence page URL:
     - Extract URL from the page response object if available (check for `_links.webui` or `url` field)
     - If not in response, construct URL using format: `https://{site-name}.atlassian.net/wiki/spaces/{SPACE_KEY}/pages/{PAGE_ID}/{PAGE_TITLE_SLUG}`
     - To get site name, extract from cloudId or use `getAccessibleAtlassianResources` response
     - Page title slug: URL-encode the page title (replace spaces with `+` or `-`)
   - **Store Page Information**: Store Confluence page details for Phase 3:
     - Update `.jira-docs/jira-state.md` with:
       - `Confluence Page ID`: {PAGE_ID}
       - `Confluence Page URL`: {PAGE_URL}
       - `Confluence Space Key`: {SPACE_KEY}
     - Or store in ticket file: `.jira-docs/tickets/ticket-{TICKET-NUMBER}.md`
   - **Error Handling**: If Confluence page creation/update fails:
     - Log error in `.jira-docs/audit.md` with timestamp and error details
     - Inform user: "Unable to create/update Confluence page. Error: [error message]. Requirements document is saved locally and ready for manual Confluence page creation."
     - Continue with workflow (don't block on Confluence failure)
   - **Log Confluence Status**: Log Confluence page creation/update status in `.jira-docs/audit.md` with timestamp

10. **Finalize Phase 2**:

- **Update State (Graceful)**: Try to update Phase 2 complete in `jira-state.md`. If update fails, continue - artifacts are source of truth.
- **Git Reminder**: Remind user to commit Phase 2 artifacts to git: "Please commit the requirements document and architecture diagram to git: `.jira-docs/requirements/{TICKET-NUMBER}_requirements.md`, `.jira-docs/requirements/{TICKET-NUMBER}-architecture-diagram.png` (if generated), and updated `.jira-docs/jira-state.md`"
