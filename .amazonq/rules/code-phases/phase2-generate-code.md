# Phase 2: Generate Code

**Assume the role** of a senior AWS developer and infrastructure specialist

**Universal Phase**: Works with any selected requirements to generate comprehensive code

1. **Analyze Requirements**: Review and understand what needs to be implemented:

   - Read requirements from `.code-docs/requirements/{TICKET-NUMBER}_requirements.md`
   - Read analysis from `.code-docs/requirements/{TICKET-NUMBER}-analysis.md`
   - **Extract selected IAC tool** from analysis document (e.g., "terraform", "cdk", "cloudformation", "pulumi")
   - **Extract selected application runtime** from analysis document (e.g., "lambda-python", "lambda-nodejs", "container-python")
   - Identify all AWS services and components required
   - Plan code structure and organization based on selected tools/runtimes

2. **Analyze Existing Codebase**: Understand what already exists:

   - Scan project directories (`iac/{iac-tool}/`, `src/`, `tests/`) for existing code using selected IAC tool directory
   - Check AWS resources tagged with `JiraId={TICKET-NUMBER}` to determine if this is a new implementation or modification
   - Identify existing resources that need updates vs. new resources to create
   - Store analysis in `.code-docs/requirements/{TICKET-NUMBER}-code-analysis.md`

3. **Generate Infrastructure as Code**: Create or update IaC configuration using selected IAC tool:

   - **Read IAC tool standards**: Load standards from `code-phases/{iac-tool}-standards.md`
     - Map tool name directly: `terraform` → `terraform-standards.md`, `cdk` → `cdk-standards.md`, `cloudformation` → `cloudformation-standards.md`, `pulumi` → `pulumi-standards.md`
     - If standards file doesn't exist, warn user and proceed with AWS best practices
   - **New resources**: Generate feature-specific IaC files following project conventions and tool-specific standards
   - **Existing resources**: Update existing IaC files with required modifications
   - **Shared resources**: Generate or update shared configuration files as needed
   - **Tool-specific configuration**:
     - **For Terraform**:
       - Ensure `iac/terraform/backend.tf` exists. If missing, create with DUMMY configuration and request user confirmation (BLOCKING)
         - Example:
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
       - After creating/modifying files, validate from `iac/terraform/` directory: `terraform fmt -recursive`, `terraform init -backend=false`, `terraform validate` (BLOCKING)
       - Treat validation failures as BLOCKING. Iterate: fix the Terraform code, re-run `fmt`,
         `init -backend=false` (if applicable), and `validate` until exit code is 0
       - Save validation output to `.code-docs/quality-reports/terraform-validate.log`
     - **For AWS CDK**:
       - Ensure `cdk.json` exists. If missing, create with default configuration
       - After creating/modifying files, validate from project root or CDK app directory: `cdk synth` (BLOCKING)
       - Save validation output to `.code-docs/quality-reports/cdk-synth.log`
     - **For CloudFormation**:
       - Validate templates from `iac/cloudformation/` directory: Use `aws cloudformation validate-template --template-body file://{template-file}.yaml` (BLOCKING)
       - Save validation output to `.code-docs/quality-reports/cloudformation-validate.log`
     - **For Pulumi**:
       - Validate configuration from directory containing `Pulumi.yaml`: `pulumi preview` (BLOCKING)
       - Save validation output to `.code-docs/quality-reports/pulumi-validate.log`
     - **For other IAC tools**: Follow tool-specific validation requirements
   - Use the `JiraId` tag to determine if resources already exist. If resources with `JiraId={TICKET-NUMBER}` are found, update those resources; if none are found, create new resources with the tag applied
   - **Tagging**: All AWS resources must include `JiraId = {TICKET-NUMBER}` and `ManagedBy = "{iac-tool}"` tags
   - Follow AWS security best practices, naming conventions, and least privilege IAM policies
   - Follow tool-specific standards from `code-phases/{iac-tool}-standards.md`

4. **Generate Application Code**: Create or update application code using selected runtime/language:

   - **Read language standards**: Load standards from `code-phases/{language}-standards.md`
     - Extract language name from runtime type: `lambda-python` → `python`, `lambda-nodejs` → `nodejs`, `container-python` → `python`, `lambda-java` → `java`
     - Examples: `python-standards.md`, `nodejs-standards.md`, `java-standards.md`, `go-standards.md`, `dotnet-standards.md`
   - **New code**: Create feature-specific code directories following project structure
     - Use directory structure: `src/{runtime-type}-{feature-name}/` (e.g., `src/lambda-python-{feature-name}/`)
     - Generate main application code files following language standards
     - Generate dependency files based on runtime:
       - Python: `requirements.txt`, `Pipfile`, `pyproject.toml`
       - Node.js: `package.json`, `package-lock.json`
       - Java: `pom.xml`, `build.gradle`
       - Go: `go.mod`, `go.sum`
       - .NET: `*.csproj`, `*.sln`
     - Include proper error handling following language-specific patterns
   - **Existing code**: Update existing code with new functionality
     - Modify relevant files
     - Update dependencies if needed
     - Add changelog entries for modifications following language standards
   - Follow language-specific best practices and AWS service guidelines from `code-phases/{language}-standards.md`

5. **Apply Security Standards**: Ensure security best practices:

   - Enable encryption at rest and in transit for all resources
   - Implement proper logging and monitoring
   - Add input validation and sanitization
   - Follow OWASP guidelines for application code
   - Use least privilege access policies

6. **Manage Version Control**: Ensure proper `.gitignore` configuration:

   - Check if `.gitignore` exists at project root
   - Create or update with appropriate ignores based on selected tools:
     - **IAC-specific** (based on selected tool):
       - Terraform: `*.tfstate*`, `.terraform/`, `*.tfplan`
       - CDK: `cdk.out/`, `.cdk.staging/`, `node_modules/`
       - CloudFormation: `*.template`, `.aws-sam/`
       - Pulumi: `.pulumi/`, `Pulumi.*.yaml` (except `Pulumi.yaml`)
     - **Language-specific** (based on selected runtime):
       - Python: `__pycache__/`, `*.pyc`, `.pytest_cache/`, `*.egg-info/`, `venv/`, `.venv/`
       - Node.js: `node_modules/`, `.npm/`, `dist/`
       - Java: `target/`, `.classpath`, `.project`
       - Go: `vendor/`, `*.exe`
       - .NET: `bin/`, `obj/`, `*.dll`, `*.exe`
     - **AWS-specific**: `.aws/`, `*.pem`, `*.key`
     - **IDE-specific**: `.vscode/`, `.idea/`, `*.swp`
     - **Environment files**: `.env`, `*.env`, `*.tfvars`, `*.pulumi.yaml`

7. **Perform Quality Validation**: Final quality checks:

   - Verify code follows AWS best practices (IaC validation completed in Step 3 based on selected tool)
   - Check for security vulnerabilities in dependencies and code:
     - **Python**: Use `safety check` or `pip-audit` for dependency vulnerabilities
     - **Node.js**: Use `npm audit` for dependency vulnerabilities
     - **Java**: Use Maven/Gradle security plugins
     - **Go**: Use `govulncheck` for dependency vulnerabilities
     - **Other languages**: Use appropriate security scanning tools
   - Run language-specific linting and formatting:
     - Follow standards from `code-phases/{language}-standards.md`
     - Run tool-specific linters (e.g., `flake8`, `eslint`, `golangci-lint`)
   - Store quality reports in `.code-docs/quality-reports/`

8. **Log and Seek Approval**:
   - Log code generation with timestamp in `.code-docs/audit.md`
   - Wait for explicit user approval before proceeding
   - Record approval response with timestamp
   - Update Phase 2 complete status in `.code-docs/code-state.md`
