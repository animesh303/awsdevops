# Phase 2: Generate Code

**Assume the role** of a senior AWS developer and infrastructure specialist

**Universal Phase**: Works with any selected requirements to generate comprehensive code

1. **Analyze Selected Requirements**: Review the requirements document and analysis:

   - Read requirements from `.code-docs/requirements/{TICKET-NUMBER}_requirements.md`
   - Read analysis from `.code-docs/requirements/{TICKET-NUMBER}-analysis.md`
   - Identify all AWS services and components to implement
   - Plan code structure and organization

2. **Analyze Existing Code**: Examine current project structure and existing code:

   - Scan `iac/terraform/` directory for existing Terraform files
   - Scan `src/lambda-*/` directories for existing Python Lambda functions
   - Scan `tests/` directory for existing test files
   - Identify which resources already exist vs. need to be created
   - Determine if requirements involve creating new resources or modifying existing ones
   - Store analysis in `.code-docs/requirements/{TICKET-NUMBER}-code-analysis.md`

3. **Generate or Modify Terraform Infrastructure as Code**: Create or update Terraform configuration:

   - **If NEW resources needed**: Generate files in `iac/terraform/` directory
     - Generate `{feature-name}-main.tf` with feature-specific infrastructure
     - Generate `{feature-name}-variables.tf` with feature-specific parameters
     - Generate `{feature-name}-output.tf` with feature-specific outputs
     - Generate `{feature-name}-local.tf` with feature-specific local values
   - **If EXISTING resources need modification**: Update existing Terraform files
     - Modify existing `{feature-name}-main.tf` files
     - Update existing `{feature-name}-variables.tf` files
     - Update existing `{feature-name}-output.tf` files
     - Add changelog entries for all modifications
   - **If shared files needed**: Generate or update shared files: `shared-variables.tf`, `shared-outputs.tf`, `versions.tf`
   - Follow AWS security best practices and naming conventions

4. **Generate or Modify Python Lambda Code**: Create or update Python code:

   - **If NEW Lambda function needed**: Create `src/lambda-{feature-name}/` directory
     - Generate main Lambda function code
     - Generate `requirements.txt` with dependencies
     - Generate `lambda_handler.py` with proper error handling
   - **If EXISTING Lambda function needs modification**: Update existing code
     - Modify existing `src/lambda-{feature-name}/` directory
     - Update existing `lambda_handler.py` with new functionality
     - Update existing `requirements.txt` if new dependencies needed
     - Add changelog entries for all modifications
   - Follow Python best practices and AWS Lambda guidelines

5. **Apply Security Best Practices**: Implement security standards:

   - Use least privilege IAM policies
   - Enable encryption at rest and in transit
   - Implement proper logging and monitoring
   - Add input validation and sanitization
   - Follow OWASP guidelines for Python code

6. **Manage .gitignore File**: Ensure proper version control setup:

   - Check if `.gitignore` file exists at project root
   - If not exists, create `.gitignore` file with appropriate entries
   - If exists, update `.gitignore` file based on generated code
   - Include Terraform-specific ignores: `*.tfstate*`, `.terraform/`, `*.tfplan`
   - Include Python-specific ignores: `__pycache__/`, `*.pyc`, `.pytest_cache/`
   - Include AWS-specific ignores: `.aws/`, `*.pem`, `*.key`
   - Include IDE-specific ignores: `.vscode/`, `.idea/`, `*.swp`
   - Include environment files: `.env`, `*.env`, `terraform.tfvars`

7. **Perform Code Quality Checks**: Ensure code quality:

   - Run Python linting (flake8, black, isort)
   - Run Terraform validation (terraform fmt, validate)
   - Check for security vulnerabilities
   - Ensure code follows AWS best practices
   - Store quality reports in `.code-docs/quality-reports/`

8. **Log and Proceed**:
   - Log code generation with timestamp in `.code-docs/audit.md`
   - Wait for explicit user approval before proceeding
   - Record approval response with timestamp
   - Update Phase 2 complete in code-state.md
