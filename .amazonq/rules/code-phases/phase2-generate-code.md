# Phase 2: Generate Code

**Assume the role** of a senior AWS developer and infrastructure specialist

**Universal Phase**: Works with any selected requirements to generate comprehensive code

1. **Analyze Requirements**: Review and understand what needs to be implemented:

   - Read requirements from `.code-docs/requirements/{TICKET-NUMBER}_requirements.md`
   - Read analysis from `.code-docs/requirements/{TICKET-NUMBER}-analysis.md`
   - Identify all AWS services and components required
   - Plan code structure and organization

2. **Analyze Existing Codebase**: Understand what already exists:

   - Scan project directories (`iac/`, `src/`, `tests/`) for existing code
   - Check AWS resources tagged with `JiraId={TICKET-NUMBER}` to determine if this is a new implementation or modification
   - Identify existing resources that need updates vs. new resources to create
   - Store analysis in `.code-docs/requirements/{TICKET-NUMBER}-code-analysis.md`

3. **Generate Infrastructure as Code**: Create or update IaC configuration:

   - **New resources**: Generate feature-specific IaC files following project conventions
   - **Existing resources**: Update existing IaC files with required modifications
   - **Shared resources**: Generate or update shared configuration files as needed
   - **Backend configuration requirement**: Ensure `iac/terraform/backend.tf` exists to configure Terraform state backend

     - If `backend.tf` does not exist, create it with the following DUMMY configuration and request the user to update the configurations manually to the correct backend settings for their environment:

       ```hcl
       terraform {
         cloud {
           organization = "aws-devops-ai"
           workspaces {
             name = "ws-terraform"
           }
         }
       }
       ```

     - Do not proceed until the user confirms that `iac/terraform/backend.tf` is up to date and correct. Treat lack of confirmation as BLOCKING

   - Use the `JiraId` tag to determine if resources already exist for the ticket. If resources with `JiraId={TICKET-NUMBER}` are found, update those resources; if none are found, create new resources with the tag applied
   - After creating or modifying any Terraform files (and after backend confirmation), validate the entire Terraform configuration from the root IaC directory (e.g., `iac/terraform/`):
     - Run `terraform fmt -recursive`
     - Run `terraform init` (use `-backend=false` only if the backend is intentionally not configured for validation)
     - Run `terraform validate` and ensure it succeeds
     - Treat validation failures as BLOCKING. Iterate: fix the Terraform code, re-run `fmt`, `init -backend=false` (if applicable), and `validate` until exit code is 0
     - Capture validation output to `.code-docs/quality-reports/terraform-validate.log` for traceability
     - Example remediation: for DynamoDB tables, set `billing_mode` to one of `PROVISIONED` or `PAY_PER_REQUEST` (not `ON_DEMAND`)
   - Follow AWS security best practices and naming conventions
   - **Backend configuration**: Ensure backend configuration exists
     - If missing, create with placeholder configuration and request user confirmation
     - **BLOCKING**: Do not proceed until user confirms backend configuration is correct
   - **Tagging**: All AWS resources must include `JiraId = {TICKET-NUMBER}` and `ManagedBy = "terraform"` tags
   - **Validation**: After any changes, validate IaC configuration:
     - Run formatting (`terraform fmt -recursive`)
     - Run initialization (`terraform init` or `terraform init -backend=false` if backend not configured)
     - Run validation (`terraform validate`) - **BLOCKING**: Must pass with exit code 0
     - Save validation output to `.code-docs/quality-reports/terraform-validate.log`
     - Iterate until validation succeeds
   - Follow AWS security best practices, naming conventions, and least privilege IAM policies

4. **Generate Application Code**: Create or update application code:

   - **New code**: Create feature-specific code directories following project structure
     - Generate main application code files
     - Generate dependency files (`requirements.txt`, `package.json`, etc. as appropriate)
     - Include proper error handling
   - **Existing code**: Update existing code with new functionality
     - Modify relevant files
     - Update dependencies if needed
     - Add changelog entries for modifications
   - Follow language-specific best practices and AWS service guidelines

5. **Apply Security Standards**: Ensure security best practices:

   - Enable encryption at rest and in transit for all resources
   - Implement proper logging and monitoring
   - Add input validation and sanitization
   - Follow OWASP guidelines for application code
   - Use least privilege access policies

6. **Manage Version Control**: Ensure proper `.gitignore` configuration:

   - Check if `.gitignore` exists at project root
   - Create or update with appropriate ignores:
     - IaC-specific: `*.tfstate*`, `.terraform/`, `*.tfplan`
     - Language-specific: `__pycache__/`, `*.pyc`, `node_modules/`, `.pytest_cache/`
     - AWS-specific: `.aws/`, `*.pem`, `*.key`
     - IDE-specific: `.vscode/`, `.idea/`, `*.swp`
     - Environment files: `.env`, `*.env`, `terraform.tfvars`

7. **Perform Quality Validation**: Final quality checks:

   - Verify code follows AWS best practices (IaC validation completed in Step 3)
   - Check for security vulnerabilities in dependencies and code
   - Store quality reports in `.code-docs/quality-reports/`

8. **Log and Seek Approval**:
   - Log code generation with timestamp in `.code-docs/audit.md`
   - Wait for explicit user approval before proceeding
   - Record approval response with timestamp
   - Update Phase 2 complete status in `.code-docs/code-state.md`
