# Phase 1: Selecting JIRA Requirement for code generation

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
   - Extract programming language requirements from requirements document
   - Identify infrastructure requirements
   - Identify testing requirements
   - Generate feature name based on requirements (e.g., "data-processing", "user-authentication")
   - Store initial analysis in `.code-docs/requirements/{TICKET-NUMBER}-analysis.md`

6. **Select Infrastructure as Code (IAC) Tool**: Determine IAC tool based on requirements:

   - If requirements specify IAC tool, use that specification
   - If not specified, analyze requirements and recommend appropriate tool:
     - **Terraform**: General purpose, multi-cloud, declarative
     - **AWS CDK**: TypeScript/JavaScript/Python preferred, programmatic infrastructure
     - **CloudFormation**: AWS-native, YAML/JSON templates
     - **Pulumi**: General purpose, supports multiple languages
   - Present options to user if unclear: "Based on requirements, I recommend [TOOL]. Should I proceed with [TOOL] or would you prefer [ALTERNATIVE]?"
   - Store selected IAC tool in analysis document: `.code-docs/requirements/{TICKET-NUMBER}-analysis.md`
   - Format: `IAC Tool: {selected-tool}` (e.g., "terraform", "cdk", "cloudformation", "pulumi")
   - **Validation**: Check if `code-phases/{iac-tool}-standards.mdc` exists. If not, warn user that standards file is missing and proceed

7. **Select Application Runtime/Language**: Determine application runtime and language:

   - If requirements specify runtime/language, use that specification
   - If not specified, analyze requirements and recommend appropriate runtime:
     - **Lambda Runtimes**: python3.x, nodejs20.x, java17, go1.x, dotnet8, etc.
     - **Container Runtimes**: python, node, java, go, dotnet, etc.
     - **Application Type**: Determine if Lambda, containerized, or other compute service
   - Present options to user if unclear: "Based on requirements, I recommend [RUNTIME] for [REASON]. Should I proceed with [RUNTIME] or would you prefer [ALTERNATIVE]?"
   - Store selected runtime/language in analysis document
   - Format: `Application Runtime: {runtime-type}` (e.g., "lambda-python", "lambda-nodejs", "container-python", "lambda-java")
   - Extract language name for standards file mapping: `lambda-python` → `python`, `lambda-nodejs` → `nodejs`, etc.
   - **Validation**: Check if `code-phases/{language}-standards.mdc` exists. If not, warn user that standards file is missing and proceed
   - Update analysis document: `.code-docs/requirements/{TICKET-NUMBER}-analysis.md`

8. **Log and Proceed**:
   - Log requirements selection with timestamp in `.code-docs/audit.md`
   - Log selected IAC tool and application runtime/language decisions
   - Wait for explicit user approval before proceeding
   - Record approval response with timestamp
   - Update Phase 1 complete in code-state.md
