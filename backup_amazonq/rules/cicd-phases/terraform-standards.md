
# Terraform CI/CD Workflow Standards

## Purpose

Define CI/CD workflow patterns and standards for Terraform code in single production workflow (triggered by main branch).

## CI Jobs

### Validate Job

- **Name**: `tf-validate`
- **Steps**:
  - Setup Terraform (minimum version 1.1): `terraform_version: ~1.1`
  - Cache Terraform plugins
  - Configure AWS credentials via OIDC (mandatory):
    ```yaml
    - name: Configure AWS credentials via OIDC
      uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
        aws-region: ${{ vars.AWS_REGION }}
    ```
  - Configure Terraform Cloud (if applicable):
    ```yaml
    - name: Configure Terraform Cloud
      env:
        TFC_TOKEN: ${{ secrets.TFC_TOKEN }}
      run: |
        cat > $HOME/.terraformrc << EOF
        credentials "app.terraform.io" {
          token = "$TFC_TOKEN"
        }
        EOF
    ```
    **Important:** Assume TFC_TOKEN is already set. Do not check for its existence using statements such as `if: ${{ secrets.TFC_TOKEN }}`.
  - Run `terraform init -backend=false`
  - Run `terraform validate`
  - Run `terraform fmt` (without `check` option)

### Plan Job

- **Name**: `tf-plan`
- **Needs**: `[tf-validate]`
- **Steps**:
  - Setup Terraform
  - Cache Terraform plugins
  - Configure AWS credentials via OIDC
  - Configure Terraform Cloud (if applicable)
  - Run `terraform init`
  - **Detect Terraform Cloud Backend**:
    ```yaml
    - name: Detect Terraform Cloud backend
      id: detect-tfc
      run: |
        if grep -q "cloud" backend.tf 2>/dev/null || [ -n "$TFC_TOKEN" ]; then
          echo "USE_TFC=true" >> $GITHUB_ENV
          echo "Terraform Cloud backend detected"
        else
          echo "USE_TFC=false" >> $GITHUB_ENV
          echo "Standard backend detected"
        fi
    ```
  - Run `terraform plan`
  - **Plan Artifact Handling**:
    - If NOT using Terraform Cloud backend (`USE_TFC=false`): Upload plan as artifact
    - If using Terraform Cloud backend (`USE_TFC=true`): Skip plan artifact (plan output not supported)

### Security Job

- **Name**: `tf-security`
- **Steps**:
  - Install Checkov
  - Run Checkov:
    ```yaml
    - name: Run Checkov
      run: |
        pip install checkov
        checkov -d . || true
    ```
  - Set `continue-on-error: true` for the job

## Build and Deployment Jobs

**Note**: These jobs are part of the single production workflow (`ci-cd.yml`). Job names follow the pattern: `terraform-{job-type}`.

### Build Job (Optional - if artifacts need to be built)

- **Name**: `terraform-build`
- **Needs**: `[terraform-lint, terraform-security, terraform-validate]`
- **Steps**:
  - Setup Terraform
  - Cache Terraform plugins
  - Configure AWS credentials via OIDC
  - Run `terraform init`
  - Run `terraform plan` (if plan artifacts needed)
  - Upload plan artifacts if applicable

### Deploy Job (in unified workflow `ci-cd.yml`)

**CRITICAL - Job Structure Decision**: When Terraform depends on Python Lambda artifacts, choose ONE of these patterns:

#### Option 1: MOST PREFERRED - Combined Build and Deploy Job

**For tightly coupled dependencies where Terraform manages Lambda and no separate Python deploy is needed:**

- **Name**: `terraform-deploy` (combines Python build + Terraform deploy)
- **Needs**: 
  - Python CI jobs: `[python-lint, python-security, python-test]`
  - Terraform CI jobs: `[terraform-lint, terraform-security, terraform-validate]`
  - Example: `needs: [python-lint, python-security, python-test, terraform-security, terraform-validate]`
- **Environment**: `production`
- **Steps**: 
  1. Checkout code
  2. **Python Build Steps**: Set up Python, install dependencies, build Lambda package directly in `iac/terraform/lambda_function.zip`
  3. **Terraform Deploy Steps**: Verify artifact exists, configure Terraform, init/plan/apply
- **Benefits**: 
  - No artifact passing needed (same runner)
  - Simplest workflow (fewer jobs)
  - No upload/download overhead
- **See**: `workflow-dependency-handling.mdc` for complete combined job pattern

#### Option 2: Separate Jobs with Local Build Placement

- **Name**: `terraform-deploy`
- **Needs**:
  - All CI jobs: `[terraform-lint, terraform-security, terraform-validate]`
  - Build job (if exists): `terraform-build`
  - **CRITICAL - Artifact Dependencies**: If Terraform needs artifacts from other code types
    - Wait for upstream **build jobs** that produce artifacts (e.g., `python-build` for Lambda package)
    - Example: `needs: [terraform-lint, terraform-security, terraform-validate, python-build]`
    - **DO NOT** wait for upstream deploy jobs for artifact dependencies
- **Environment**: `production`
- **MANDATORY Dependency Detection**:
  - **If Terraform code references artifacts** (e.g., `filename = "lambda_function.zip"` in any `.tf` file), Terraform HAS dependencies
  - **Decision Point**: Choose Option 1 (Combined Job) if Terraform manages Lambda and no separate Python deploy needed
  - **If Option 2 (Separate Jobs)**: Dependency handling steps below are MANDATORY - DO NOT SKIP
  - These steps ensure artifacts are available when Terraform runs

**For Option 1 (Combined Job) - Steps**:
  1. Checkout code
  2. **Python Build Steps** (build artifact where Terraform expects it):
     - Set up Python
     - Install dependencies
     - Build Lambda package in `iac/terraform/lambda_function.zip`
  3. **Terraform Deploy Steps** (use artifact from same runner):
     - Verify artifact exists
     - Configure AWS credentials
     - Configure Terraform Cloud (if applicable)
     - Terraform init/plan/apply

**For Option 2 (Separate Jobs) - Steps** (CRITICAL ORDER - ALL STEPS MANDATORY IF DEPENDENCIES DETECTED):

  1. **CRITICAL - Checkout code**: Standard checkout (unified workflow uses push trigger):
     ```yaml
     - uses: actions/checkout@v4
     ```
  2. **Dependency Handling Steps** (MANDATORY if Terraform depends on other code types):

     - **CRITICAL**: Follow the dependency handling pattern from `workflow-dependency-handling.mdc`
     - **PREFERRED - Local Build Placement**: For Lambda functions and similar artifacts, the PREFERRED approach is to build artifacts directly in the location where Terraform expects them, eliminating the need for artifact upload/download:
       - **Python Lambda Example**: Build Lambda package directly in Terraform directory (e.g., `iac/terraform/lambda_function.zip`)
       - **Benefits**: Simpler workflow, no artifact upload/download, fewer path issues, Terraform deploys source directly
       - **Implementation**: Upstream build job (e.g., `python-build`) builds artifact directly in Terraform directory, Terraform deploy job uses it directly
       - **See**: `workflow-dependency-handling.mdc` for local build placement patterns
     - **ALTERNATIVE - Artifact Upload/Download**: If local build placement is not feasible, use artifact upload/download:
       - **PREFERRED - Use Artifact Mapping**: If `.code-docs/artifact-mappings.json` exists:
         - Read mapping file to get exact artifact names (`artifact_name`) and destination paths (`artifact_destination_path`)
         - Use these values in dependency handling steps
       - **FALLBACK - Manual Detection**: If mapping file does not exist, use code analysis to determine artifact names and paths

     **Required Steps** (see `workflow-dependency-handling.mdc` for complete examples):

     **For Local Build Placement (PREFERRED)**:

     1. Upstream build job builds artifact directly in Terraform directory (e.g., `iac/terraform/lambda_function.zip`)
     2. Verify artifact exists before Terraform operations
     3. Pass artifact paths to Terraform via environment variables (if needed)

     **For Artifact Upload/Download (ALTERNATIVE)**:

     1. Download artifacts from upstream build jobs using `actions/download-artifact@v4`
     2. Place artifacts in correct location (use `artifact_destination_path` from mapping if available)
     3. Verify artifacts exist before Terraform operations
     4. Pass artifact paths to Terraform via environment variables

     **See**: `workflow-dependency-handling.mdc` for complete dependency handling patterns and code examples

  3. Configure AWS credentials via OIDC (mandatory)
  4. Configure Terraform Cloud (if applicable)
  5. **Pass dependency artifacts to Terraform**:
     - Set environment variables or Terraform variables with artifact paths/URLs
     - Example: `TF_VAR_lambda_package_path=./iac/terraform/lambda_function.zip`
  6. **Plan Application**:
     - If NOT using Terraform Cloud (`USE_TFC=false`): Download plan artifact from CI job and apply it
     - If using Terraform Cloud (`USE_TFC=true`): Run `terraform plan` and `terraform apply -auto-approve` directly
  7. Deploy to environment

## Job Naming Convention

For single production workflow, use these job names:

- `terraform-lint` - Lint job (optional, can use validate instead)
- `terraform-security` - Security scan job
- `terraform-validate` - Validate job
- `terraform-build` - Build job (optional)
- `terraform-deploy` - Deploy job

---

## Permissions

- **AWS Operations**: `id-token: write` (for OIDC, mandatory)
- **Contents**: `read`

## Deployment Job

- **Name**: `terraform-deploy`
- **Needs**: All CI jobs (`terraform-lint`, `terraform-security`, `terraform-validate`) AND upstream deploy jobs (if dependencies exist)
- **Environment**: `production`
- **Workflow Trigger**: `push` to `main` branch only
- **MANDATORY Dependency Detection**:
  - **If Terraform code references artifacts** (e.g., `filename = "lambda_function.zip"` in any `.tf` file), Terraform HAS dependencies
  - **Dependency handling steps below are MANDATORY** - DO NOT SKIP if dependencies are detected
- **Steps** (CRITICAL ORDER - ALL STEPS MANDATORY IF DEPENDENCIES DETECTED):

  1. **Checkout code**:
     ```yaml
     - uses: actions/checkout@v4
     ```
  2. **Dependency Handling Steps** (MANDATORY if Terraform depends on other code types):

     - **CRITICAL**: Follow the dependency handling pattern from `workflow-dependency-handling.mdc`
     - **PREFERRED - Local Build Placement**: For Lambda functions and similar artifacts, the PREFERRED approach is to build artifacts directly in the location where Terraform expects them, eliminating the need for artifact upload/download:
       - **Python Lambda Example**: Build Lambda package directly in Terraform directory (e.g., `iac/terraform/lambda_function.zip`)
       - **Benefits**: Simpler workflow, no artifact upload/download, fewer path issues, Terraform deploys source directly
       - **Implementation**: Upstream build job (e.g., `python-build`) builds artifact directly in Terraform directory, Terraform deploy job uses it directly
       - **See**: `workflow-dependency-handling.mdc` for local build placement patterns
     - **ALTERNATIVE - Artifact Upload/Download**: If local build placement is not feasible, use artifact upload/download:
       - **PREFERRED - Use Artifact Mapping**: If `.code-docs/artifact-mappings.json` exists:
         - Read mapping file to get exact artifact names (`artifact_name`) and destination paths (`artifact_destination_path`)
         - Use these values in dependency handling steps
       - **FALLBACK - Manual Detection**: If mapping file does not exist, use code analysis to determine artifact names and paths

     **Required Steps** (see `workflow-dependency-handling.mdc` for complete examples):

     **For Local Build Placement (PREFERRED)**:

     1. Upstream build job builds artifact directly in Terraform directory (e.g., `iac/terraform/lambda_function.zip`)
     2. Verify artifact exists before Terraform operations
     3. Pass artifact paths to Terraform via environment variables (if needed)

     **For Artifact Upload/Download (ALTERNATIVE)**:

     1. Download artifacts from upstream build jobs using `actions/download-artifact@v4`
     2. Place artifacts in correct location (use `artifact_destination_path` from mapping if available)
     3. Verify artifacts exist before Terraform operations
     4. Pass artifact paths to Terraform via environment variables

     **See**: `workflow-dependency-handling.mdc` for complete dependency handling patterns and code examples

  3. Configure AWS credentials via OIDC (mandatory)
  4. Configure Terraform Cloud (if applicable)
  5. **Pass dependency artifacts to Terraform**:
     - Set environment variables or Terraform variables with artifact paths/URLs
     - Example: `TF_VAR_lambda_package_path=./iac/terraform/lambda_function.zip`
  6. **Plan Application**:
     - If NOT using Terraform Cloud (`USE_TFC=false`): Download plan artifact from CI job and apply it
     - If using Terraform Cloud (`USE_TFC=true`): Run `terraform plan` and `terraform apply -auto-approve` directly
  7. Deploy to production environment
  8. Protected with GitHub environment protection rules

## Permissions

- **AWS Operations**: `id-token: write` (for OIDC, mandatory)
- **Contents**: `read`

## Important Notes

- **Terraform Version**: MUST use version 1.1 or later (specify `terraform_version: ~1.1`)
- **Terraform Cloud Backend**: When using Terraform Cloud, plan output files are NOT supported. Skip plan artifact upload/download.
- **AWS Credentials**: OIDC configuration is MANDATORY for all Terraform jobs that interact with AWS
- **Concurrency**: Use concurrency groups to prevent overlapping deployments
- **Workflow Trigger**: Single production workflow triggers on `main` branch push only
- **Environment**: All deploy jobs use `environment: production`

## Dependency Handling

**When Terraform depends on other code types** (e.g., Python Lambda package):

- **MANDATORY Detection**: Dependencies are detected from:
  1. Requirements files (`.code-docs/requirements/` or `.requirements/`)
  2. Artifact mapping file (`.code-docs/artifact-mappings.json`)
  3. **Code Analysis** (MANDATORY): Scan Terraform `.tf` files for artifact references:
     - `filename = "lambda_function.zip"` → Terraform depends on Python Lambda
     - `source = "*.zip"` → Terraform depends on artifact-producing code type
     - Any reference to `.zip`, Lambda packages, or other build artifacts → Dependency exists
- **MANDATORY Implementation**: If dependencies are detected (from requirements OR code analysis):
  - **Artifact Dependencies**: Use `needs:` to wait for upstream **build jobs** that produce artifacts
    - Example: `needs: [terraform-lint, terraform-security, terraform-validate, python-build]`
    - **CRITICAL**: Wait for build jobs, NOT deploy jobs, for artifact dependencies
  - **PREFERRED - Local Build Placement**: For Lambda functions and similar artifacts, build directly where Terraform expects them:
    - **Python Lambda Example**: Build Lambda package in `iac/terraform/lambda_function.zip` during Python build job
    - **Benefits**: Terraform deploys Lambda source directly, no artifact upload/download needed, simpler workflow
    - **Implementation**: Upstream build job builds artifact in Terraform directory, Terraform deploy job uses it directly
    - **See**: `workflow-dependency-handling.mdc` for local build placement patterns
  - **ALTERNATIVE - Artifact Upload/Download**: If local build placement is not feasible, use artifact upload/download:
    - **Follow Dependency Pattern**: Implement dependency handling steps as documented in `workflow-dependency-handling.mdc`
    - **Artifact Passing**: Pass artifact paths/URLs to Terraform via environment variables or Terraform variables
- **DO NOT SKIP**: Dependency handling steps are MANDATORY, not optional - they ensure Terraform has required artifacts
- **Multiple Dependencies**: If Terraform depends on multiple code types, wait for all upstream build jobs via `needs:` array
- **CRITICAL - Terraform Deploys Lambda Source**: When Terraform manages Lambda functions, Terraform itself should deploy the Lambda source code. The `source_code_hash` attribute in Terraform automatically detects changes to the zip file and updates the Lambda function code when `terraform apply` runs. This eliminates the need for separate Python deploy jobs that update Lambda function code.
- **See**: `workflow-dependency-handling.mdc` for complete dependency handling patterns, code examples, and best practices
