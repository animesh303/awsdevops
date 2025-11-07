# Terraform CI/CD Workflow Standards

## Purpose

Define CI/CD workflow patterns and standards for Terraform code in unified workflow files.

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

## Deployment Jobs

**Note**: Each environment has its own workflow file. The deployment job below applies to the corresponding environment workflow.

### Deploy to Dev (in `terraform-dev.yml`)

- **Name**: `deploy-dev`
- **Needs**: All CI jobs
- **Environment**: `dev`
- **Workflow Trigger**: `on.push.branches: [develop]`
  - **If Terraform depends on other code types** (e.g., Python Lambda), add `workflow_run` trigger:
    ```yaml
    on:
      workflow_run:
        workflows: ["Python Dev"] # Wait for upstream workflow
        types: [completed]
        branches: [develop]
      push:
        branches: [develop] # Also trigger on direct push
    ```
- **MANDATORY Dependency Detection**:
  - **If Terraform code references artifacts** (e.g., `filename = "lambda_function.zip"` in any `.tf` file), Terraform HAS dependencies
  - **Dependency handling steps below are MANDATORY** - DO NOT SKIP even if orchestrator workflows are used
  - These steps ensure artifacts are available when Terraform runs
- **Steps** (CRITICAL ORDER - ALL STEPS MANDATORY IF DEPENDENCIES DETECTED):

  1. **CRITICAL - Checkout code**: For workflow_run triggers, ALL jobs MUST checkout with ref parameter:
     ```yaml
     - uses: actions/checkout@v4
       with:
         ref: ${{ github.event.workflow_run.head_branch }}
     ```
     For push triggers, use standard checkout:
     ```yaml
     - uses: actions/checkout@v4
     ```
  2. **Download dependencies from upstream workflows FIRST** (MANDATORY if Terraform depends on other code types):

     - **CRITICAL**: This step is MANDATORY if Terraform code references artifacts (e.g., `filename = "lambda_function.zip"`)
     - **DO NOT SKIP**: Even if orchestrator workflows are used, this step ensures artifacts are available
     - **PREFERRED - Use Artifact Mapping**: If `.code-docs/artifact-mappings.json` exists:
       - Read mapping file to get exact artifact names and paths
       - For each mapping entry in `mappings` array:
         - Use `environment_artifacts.dev` for artifact name (e.g., `lambda-package-dev`)
         - Use `artifact_destination_path` for final placement location
     - **FALLBACK - Manual Detection**: If mapping file does not exist, use code analysis to determine artifact names

     ```yaml
     # Example for single dependency (from mapping file or code analysis)
     - name: Download Lambda package from upstream workflow
       uses: actions/download-artifact@v4
       continue-on-error: true
       id: download-artifact
       with:
         name: lambda-package-dev # Use artifact name from mapping file (environment_artifacts.dev) or code analysis
         run-id: ${{ github.event.workflow_run.id }}
         github-token: ${{ secrets.GITHUB_TOKEN }}
         path: ./lambda-package # Downloads to ./lambda-package/lambda-package.zip

     - name: Verify artifact downloaded successfully
       if: steps.download-artifact.outcome != 'success'
       run: |
         echo "Error: Failed to download artifact 'lambda-package-dev' from upstream workflow"
         echo "Upstream workflow run ID: ${{ github.event.workflow_run.id }}"
         exit 1
     ```

     ```yaml
     # Example for multiple dependencies (from mapping file)
     - name: Download Lambda packages from upstream workflows
       uses: actions/download-artifact@v4
       continue-on-error: true
       id: download-artifact-1
       with:
         name: ${{ fromJSON(steps.read-mapping.outputs.mappings)[0].environment_artifacts.dev }}
         run-id: ${{ github.event.workflow_run.id }}
         github-token: ${{ secrets.GITHUB_TOKEN }}
         path: ./lambda-packages

     - name: Download second Lambda package
       uses: actions/download-artifact@v4
       continue-on-error: true
       id: download-artifact-2
       with:
         name: ${{ fromJSON(steps.read-mapping.outputs.mappings)[1].environment_artifacts.dev }}
         run-id: ${{ github.event.workflow_run.id }}
         github-token: ${{ secrets.GITHUB_TOKEN }}
         path: ./lambda-packages
     ```

     - **Note**: After download, the artifact will be at `./lambda-package/lambda-package.zip` (or the filename uploaded by upstream workflow)
     - **For single dependency**: Always use `actions/download-artifact@v4` with `run-id` (shown above)
     - **For multiple dependencies**:
       - **If mapping file exists**: Download each artifact using its specific `environment_artifacts.dev` name
       - **If mapping file does not exist**: Download from S3/container registry where each upstream workflow uploads independently
     - **For orchestrator workflows**: Artifacts may be passed via orchestrator, but this step provides fallback and verification

  3. **Place artifact in correct location** where Terraform code expects it (MANDATORY):
     - **CRITICAL**: This step is MANDATORY if Terraform code references artifacts
     - **PREFERRED - Use Artifact Mapping**: If `.code-docs/artifact-mappings.json` exists:
       - Read `artifact_destination_path` from mapping file for exact placement location
       - For multiple artifacts, use each mapping entry's `artifact_destination_path`
     - **FALLBACK - Path Detection**: If mapping file does not exist, analyze Terraform code to find exact path where artifact is expected
       - If Terraform uses: `filename = "lambda_function.zip"` → Place at `iac/terraform/lambda_function.zip` (relative to repo root)
       - If Terraform uses: `source = "./lambda_function.zip"` → Place in same directory as the `.tf` file
       - If Terraform uses variable: Check variable definition to determine path
     ```yaml
     # Example for single dependency (from mapping file)
     - name: Move Lambda package to Terraform directory
       run: |
         # Use artifact_destination_path from mapping file
         DEST_PATH="./iac/terraform/lambda_function.zip"
         mkdir -p $(dirname "$DEST_PATH")
         cp ./lambda-package/lambda-package.zip "$DEST_PATH"
         echo "TF_VAR_lambda_package_path=$(pwd)/$DEST_PATH" >> $GITHUB_ENV
     ```
     ```yaml
     # Example for multiple dependencies (from mapping file)
     - name: Move Lambda packages to Terraform directories
       run: |
         # For each mapping entry, place artifact at artifact_destination_path
         # Example: Place first Lambda at iac/terraform/lambda_function_1.zip
         #          Place second Lambda at iac/terraform/lambda_function_2.zip
         mkdir -p ./iac/terraform
         cp ./lambda-packages/lambda-package-1.zip ./iac/terraform/lambda_function_1.zip
         cp ./lambda-packages/lambda-package-2.zip ./iac/terraform/lambda_function_2.zip
         echo "TF_VAR_lambda_package_path_1=$(pwd)/iac/terraform/lambda_function_1.zip" >> $GITHUB_ENV
         echo "TF_VAR_lambda_package_path_2=$(pwd)/iac/terraform/lambda_function_2.zip" >> $GITHUB_ENV
     ```
     - **MANDATORY**: This step MUST be included if dependencies are detected
  4. **Verify artifact exists** before Terraform operations (MANDATORY):
     - **CRITICAL**: This verification step is MANDATORY to ensure Terraform has required artifacts
     - **PREFERRED - Use Artifact Mapping**: If `.code-docs/artifact-mappings.json` exists:
       - Verify artifact exists at `artifact_destination_path` from mapping file
       - For multiple artifacts, verify each one at its respective `artifact_destination_path`
     - **FALLBACK - Path Verification**: If mapping file does not exist, verify the exact path that Terraform code references (from step 3)
     ```yaml
     # Example for single dependency (from mapping file)
     - name: Verify Lambda package exists
       run: |
         # Use artifact_destination_path from mapping file
         TERRAFORM_LAMBDA_PATH="./iac/terraform/lambda_function.zip"
         if [ ! -f "$TERRAFORM_LAMBDA_PATH" ]; then
           echo "Error: Lambda package not found at: $TERRAFORM_LAMBDA_PATH"
           echo "Terraform code expects this file - deployment will fail without it"
           echo "Checking downloaded artifact location:"
           ls -la ./lambda-package/ || echo "lambda-package directory not found"
           echo "Current directory structure:"
           find . -name "*.zip" -o -name "lambda_function.zip" 2>/dev/null || echo "No zip files found"
           exit 1
         fi
         echo "✓ Lambda package verified at: $TERRAFORM_LAMBDA_PATH"
         ls -lh "$TERRAFORM_LAMBDA_PATH"
     ```
     ```yaml
     # Example for multiple dependencies (from mapping file)
     - name: Verify all Lambda packages exist
       run: |
         # Verify each artifact at its artifact_destination_path
         PATHS=(
           "./iac/terraform/lambda_function_1.zip"
           "./iac/terraform/lambda_function_2.zip"
         )
         for PATH in "${PATHS[@]}"; do
           if [ ! -f "$PATH" ]; then
             echo "Error: Lambda package not found at: $PATH"
             exit 1
           fi
           echo "✓ Lambda package verified at: $PATH"
         done
     ```
     - **MANDATORY**: This verification MUST be included if dependencies are detected
  5. Configure AWS credentials via OIDC (mandatory)
  6. Configure Terraform Cloud (if applicable)
  7. **Pass dependency artifacts to Terraform**:
     - Set environment variables or Terraform variables with artifact paths/URLs
     - Example: `TF_VAR_lambda_package_path=./iac/terraform/lambda_function.zip`
  8. **Plan Application**:
     - If NOT using Terraform Cloud (`USE_TFC=false`): Download plan artifact from CI job and apply it
     - If using Terraform Cloud (`USE_TFC=true`): Run `terraform plan` and `terraform apply -auto-approve` directly
  9. Deploy to development environment

### Deploy to Test (in `terraform-test.yml`)

- **Name**: `deploy-test`
- **Needs**: All CI jobs (within the test workflow)
- **Environment**: `test`
- **Workflow Trigger**: `push` to `main` branch
  - **If Terraform depends on other code types**, also wait for their test workflows using `workflow_run` trigger:
    ```yaml
    on:
      workflow_run:
        workflows: ["Python Test"] # Wait for upstream dependency's test workflow
        types: [completed]
        branches: [main]
      push:
        branches: [main] # Fallback trigger
    ```
    **Note**: For dependencies, test workflow can wait for upstream test workflow via workflow_run, with push as fallback
- **Condition**: If using `workflow_run`, add condition at job level: `if: ${{ github.event.workflow_run.conclusion == 'success' || github.event_name == 'push' }}`
- **MANDATORY Dependency Detection**:
  - **If Terraform code references artifacts** (e.g., `filename = "lambda_function.zip"` in any `.tf` file), Terraform HAS dependencies
  - **Dependency handling steps below are MANDATORY** - DO NOT SKIP even if orchestrator workflows are used
- **Steps** (CRITICAL ORDER - ALL STEPS MANDATORY IF DEPENDENCIES DETECTED):

  1. **CRITICAL - Checkout code**: For workflow_run triggers, ALL jobs MUST checkout with ref parameter:
     ```yaml
     - uses: actions/checkout@v4
       with:
         ref: ${{ github.event.workflow_run.head_branch }}
     ```
     For push triggers, use standard checkout:
     ```yaml
     - uses: actions/checkout@v4
     ```
  2. **Download dependencies from upstream workflows FIRST** (MANDATORY if Terraform depends on other code types):

     - **CRITICAL**: This step is MANDATORY if Terraform code references artifacts (e.g., `filename = "lambda_function.zip"`)
     - **DO NOT SKIP**: Even if orchestrator workflows are used, this step ensures artifacts are available

     ```yaml
     - name: Download Lambda package from upstream workflow
       uses: actions/download-artifact@v4
       continue-on-error: true
       id: download-artifact
       with:
         name: lambda-package-test
         run-id: ${{ github.event.workflow_run.id }}
         github-token: ${{ secrets.GITHUB_TOKEN }}
         path: ./lambda-package

     - name: Verify artifact downloaded successfully
       if: steps.download-artifact.outcome != 'success'
       run: |
         echo "Error: Failed to download artifact 'lambda-package-test' from upstream workflow"
         echo "Upstream workflow run ID: ${{ github.event.workflow_run.id }}"
         exit 1
     ```

     - **For single dependency**: Always use `actions/download-artifact@v4` with `run-id` (shown above)
     - **For multiple dependencies**: Download from S3/container registry where each upstream workflow uploads independently
     - **MANDATORY**: This step MUST be included if dependencies are detected

  3. **Place artifact in correct location** where Terraform code expects it (MANDATORY):
     - **CRITICAL**: This step is MANDATORY if Terraform code references artifacts
     - **Path Detection**: Analyze Terraform code to find exact path where artifact is expected
     ```yaml
     - name: Move Lambda package to Terraform directory
       run: |
         mkdir -p ./iac/terraform
         cp ./lambda-package/lambda-package.zip ./iac/terraform/lambda_function.zip
         echo "TF_VAR_lambda_package_path=$(pwd)/iac/terraform/lambda_function.zip" >> $GITHUB_ENV
     ```
     - **MANDATORY**: This step MUST be included if dependencies are detected
  4. **Verify artifact exists** before Terraform operations (MANDATORY):
     - **CRITICAL**: This verification step is MANDATORY to ensure Terraform has required artifacts
     ```yaml
     - name: Verify Lambda package exists
       run: |
         TERRAFORM_LAMBDA_PATH="./iac/terraform/lambda_function.zip"
         if [ ! -f "$TERRAFORM_LAMBDA_PATH" ]; then
           echo "Error: lambda_function.zip not found at expected location!"
           echo "Terraform code expects this file - deployment will fail without it"
           exit 1
         fi
         echo "Lambda package verified at: ./iac/terraform/lambda_function.zip"
     ```
     - **MANDATORY**: This verification MUST be included if dependencies are detected
  5. Configure AWS credentials via OIDC (mandatory)
  6. Configure Terraform Cloud (if applicable)
  7. Run CI jobs (validate, plan, security)
  8. **Pass dependency artifacts to Terraform**:
     - Set environment variables or Terraform variables with artifact paths/URLs
     - Example: `TF_VAR_lambda_package_path=./iac/terraform/lambda_function.zip`
  9. **Plan Application**:
     - If NOT using Terraform Cloud (`USE_TFC=false`): Download plan artifact from CI job and apply it
     - If using Terraform Cloud (`USE_TFC=true`): Run `terraform plan` and `terraform apply -auto-approve` directly
  10. Deploy to test environment

### Deploy to Prod (in `terraform-prd.yml`)

- **Name**: `deploy-prod`
- **Needs**: All CI jobs (within the prod workflow)
- **Environment**: `prod`
  - **Workflow Trigger**: `workflow_run` on successful completion of `terraform-test.yml` with `branches: [main]`
  - **If Terraform depends on other code types**, also wait for their prod workflows (same environment):
    ```yaml
    on:
      workflow_run:
        workflows: ["Terraform Test", "Python Prod"] # Wait for Terraform Test (self) and Python Prod (dependency)
        types: [completed]
        branches: [main]
    ```
    **Note**: For same-environment dependencies, prod workflow waits for dependency's prod workflow (e.g., "Python Prod"), not test workflow. This ensures Terraform Prod deploys only after Python Prod has successfully deployed in the same environment.
- **Condition**: `if: ${{ github.event.workflow_run.conclusion == 'success' }}`
- **MANDATORY Dependency Detection**:
  - **If Terraform code references artifacts** (e.g., `filename = "lambda_function.zip"` in any `.tf` file), Terraform HAS dependencies
  - **Dependency handling steps below are MANDATORY** - DO NOT SKIP even if orchestrator workflows are used
- **Steps** (CRITICAL ORDER - ALL STEPS MANDATORY IF DEPENDENCIES DETECTED):

  1. **CRITICAL - Checkout code**: For workflow_run triggers, ALL jobs MUST checkout with ref parameter:
     ```yaml
     - uses: actions/checkout@v4
       with:
         ref: ${{ github.event.workflow_run.head_branch }}
     ```
     This is required because `workflow_run` triggers don't automatically checkout code.
  2. **Download dependencies from upstream workflows FIRST** (MANDATORY if Terraform depends on other code types):

     - **CRITICAL**: This step is MANDATORY if Terraform code references artifacts (e.g., `filename = "lambda_function.zip"`)
     - **DO NOT SKIP**: Even if orchestrator workflows are used, this step ensures artifacts are available

     ```yaml
     - name: Download Lambda package from upstream workflow
       uses: actions/download-artifact@v4
       continue-on-error: true
       id: download-artifact
       with:
         name: lambda-package-prod
         run-id: ${{ github.event.workflow_run.id }}
         github-token: ${{ secrets.GITHUB_TOKEN }}
         path: ./lambda-package

     - name: Verify artifact downloaded successfully
       if: steps.download-artifact.outcome != 'success'
       run: |
         echo "Error: Failed to download artifact 'lambda-package-prod' from upstream workflow"
         echo "Upstream workflow run ID: ${{ github.event.workflow_run.id }}"
         exit 1
     ```

     - **For single dependency**: Always use `actions/download-artifact@v4` with `run-id` (shown above)
     - **For multiple dependencies**: Download from S3/container registry where each upstream workflow uploads independently
     - **MANDATORY**: This step MUST be included if dependencies are detected

  3. **Place artifact in correct location** where Terraform code expects it (MANDATORY):
     - **CRITICAL**: This step is MANDATORY if Terraform code references artifacts
     - **Path Detection**: Analyze Terraform code to find exact path where artifact is expected
     ```yaml
     - name: Move Lambda package to Terraform directory
       run: |
         mkdir -p ./iac/terraform
         cp ./lambda-package/lambda-package.zip ./iac/terraform/lambda_function.zip
         echo "TF_VAR_lambda_package_path=$(pwd)/iac/terraform/lambda_function.zip" >> $GITHUB_ENV
     ```
     - **MANDATORY**: This step MUST be included if dependencies are detected
  4. **Verify artifact exists** before Terraform operations (MANDATORY):
     - **CRITICAL**: This verification step is MANDATORY to ensure Terraform has required artifacts
     ```yaml
     - name: Verify Lambda package exists
       run: |
         TERRAFORM_LAMBDA_PATH="./iac/terraform/lambda_function.zip"
         if [ ! -f "$TERRAFORM_LAMBDA_PATH" ]; then
           echo "Error: lambda_function.zip not found at expected location!"
           echo "Terraform code expects this file - deployment will fail without it"
           exit 1
         fi
         echo "Lambda package verified at: ./iac/terraform/lambda_function.zip"
     ```
     - **MANDATORY**: This verification MUST be included if dependencies are detected
  5. Configure AWS credentials via OIDC (mandatory)
  6. Configure Terraform Cloud (if applicable)
  7. Run CI jobs (validate, plan, security)
  8. **Pass dependency artifacts to Terraform**:
     - Set environment variables or Terraform variables with artifact paths/URLs
     - Example: `TF_VAR_lambda_package_path=./iac/terraform/lambda_function.zip`
  9. **Plan Application**:
     - If NOT using Terraform Cloud (`USE_TFC=false`): Download plan artifact from CI job and apply it
     - If using Terraform Cloud (`USE_TFC=true`): Run `terraform plan` and `terraform apply -auto-approve` directly
  10. Deploy to production environment
  11. Protected with GitHub environment protection rules

## Permissions

- **AWS Operations**: `id-token: write` (for OIDC, mandatory)
- **Contents**: `read`

## Important Notes

- **Terraform Version**: MUST use version 1.1 or later (specify `terraform_version: ~1.1`)
- **Terraform Cloud Backend**: When using Terraform Cloud, plan output files are NOT supported. Skip plan artifact upload/download.
- **AWS Credentials**: OIDC configuration is MANDATORY for all Terraform jobs that interact with AWS
- **Concurrency**: Use concurrency groups to prevent overlapping deployments per environment

## Dependency Handling

**When Terraform depends on other code types** (e.g., Python Lambda package):

- **MANDATORY Detection**: Dependencies are detected from:
  1. Requirements files (`.code-docs/requirements/` or `.requirements/`)
  2. **Code Analysis** (MANDATORY): Scan Terraform `.tf` files for artifact references:
     - `filename = "lambda_function.zip"` → Terraform depends on Python Lambda
     - `source = "*.zip"` → Terraform depends on artifact-producing code type
     - Any reference to `.zip`, Lambda packages, or other build artifacts → Dependency exists
- **MANDATORY Implementation**: If dependencies are detected (from requirements OR code analysis):
  - **Workflow Triggers**: Add `workflow_run` triggers to wait for upstream workflows to complete
  - **Download Artifacts**: Use `actions/download-artifact@v4` with `run-id` and `github-token` to download from upstream workflows (MANDATORY step)
  - **Place Artifacts**: Place artifacts in correct location where Terraform code expects them (MANDATORY step)
  - **Verify Artifacts**: Verify artifacts exist before Terraform operations (MANDATORY step)
  - **Artifact Passing**: Pass artifact paths/URLs to Terraform via environment variables or Terraform variables
- **DO NOT SKIP**: Dependency handling steps are MANDATORY, not optional - they ensure Terraform has required artifacts
- **Multiple Dependencies**: If Terraform depends on multiple code types, wait for all upstream workflows
- **Artifact Sources**: Download from GitHub Actions artifacts, S3, or container registries based on where upstream workflows store artifacts
