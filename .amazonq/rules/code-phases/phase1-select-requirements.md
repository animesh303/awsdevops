# Phase 1: Select Requirements

**Assume the role** of a requirements analysis specialist

**Universal Phase**: Works with any requirements documents to allow user selection

1. **Validate Requirements Source**: Check for JIRA requirements directory:

   - Check if `.jira-docs/requirements/` directory exists
   - If directory doesn't exist or is empty, END workflow with message:
     "No requirements found. Please use the JIRA task management workflow to fetch and generate requirements first before proceeding with code generation."
   - If directory exists and contains requirements, proceed to scan

2. **Scan Available Requirements**: Search for requirements documents:

   - Scan `.jira-docs/requirements/` directory (single source of truth)
   - Identify all available requirements documents
   - Store list in `.code-docs/requirements/available-requirements.md`

3. **Display Requirements Selection Interface**: Present requirements in a user-friendly format:

   - Show ticket number, title, and brief description for each requirement
   - Number each requirement for easy selection
   - Store formatted list in `.code-docs/requirements/requirements-selection.md`
   - Ask user to select requirement by number or ticket key

4. **Handle Requirements Selection**: Process user's requirements selection:

   - Validate the selected requirement exists in the available list
   - Copy selected requirements document to `.code-docs/requirements/{TICKET-NUMBER}_requirements.md`
   - Read and analyze the selected requirements document
   - Extract key technical specifications for code generation

5. **Analyze Requirements for Code Generation**: Parse selected requirements:

   - Identify AWS services to be implemented
   - Extract programming language requirements
   - Note infrastructure requirements (Terraform)
   - Identify testing requirements
   - Generate feature name based on requirements (e.g., "data-processing", "user-authentication")
   - Store analysis in `.code-docs/requirements/{TICKET-NUMBER}-analysis.md`

6. **Log and Proceed**:
   - Log requirements selection with timestamp in `.code-docs/audit.md`
   - Wait for explicit user approval before proceeding
   - Record approval response with timestamp
   - Update Phase 1 complete in code-state.md
