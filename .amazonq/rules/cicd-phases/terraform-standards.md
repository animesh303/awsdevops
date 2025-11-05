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
  - Run `terraform plan`
  - **Plan Artifact Handling**:
    - If NOT using Terraform Cloud backend: Upload plan as artifact
    - If using Terraform Cloud backend: Skip plan artifact (plan output not supported)

### Security Job

- **Name**: `tf-security`
- **Steps**:
  - Install Checkov
  - Run Checkov with SARIF output:
    ```yaml
    - name: Run Checkov (SARIF)
      run: |
        pip install checkov
        checkov -d . --output-file-path results_sarif.sarif --output sarif
    ```
  - Upload SARIF artifact with name `checkov-sarif`
  - Set `continue-on-error: true` for the job

### Upload SARIF Job

- **Name**: `tf-upload-sarif`
- **Needs**: `[tf-security]`
- **Steps**:
  - Download SARIF artifact (`checkov-sarif`)
  - Verify `results_sarif.sarif` file exists
  - Upload using `github/codeql-action/upload-sarif@v3`:
    ```yaml
    - name: Upload SARIF to GitHub
      uses: github/codeql-action/upload-sarif@v3
      with:
        sarif_file: results_sarif.sarif
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
- **Steps** (CRITICAL ORDER):
  1. **Checkout code**: `ref: ${{ github.event.workflow_run.head_branch }}` (if using workflow_run trigger) OR standard checkout (for push trigger)
  2. **Download dependencies from upstream workflows FIRST** (if Terraform depends on other code types):
     ```yaml
     - name: Download Lambda package from upstream workflow
       uses: actions/download-artifact@v4
       with:
         name: lambda-package-dev # Must match the artifact name uploaded by Python workflow
         run-id: ${{ github.event.workflow_run.id }}
         github-token: ${{ secrets.GITHUB_TOKEN }}
         path: ./lambda-package # Downloads to ./lambda-package/lambda-package.zip
     ```
     - **Note**: After download, the artifact will be at `./lambda-package/lambda-package.zip` (or the filename uploaded by upstream workflow)
     - Or download from S3/container registry if artifacts were stored there
  3. **Place artifact in correct location** where Terraform code expects it:
     ```yaml
     - name: Move Lambda package to Terraform directory
       run: |
         # CRITICAL: Check the actual path referenced in Terraform code (e.g., in s3-lambda-trigger-main.tf)
         # If Terraform code uses: filename = "lambda_function.zip"
         # Place it in the same directory as the Terraform file that references it
         # Example: If Terraform code is in iac/terraform/ and references lambda_function.zip
         mkdir -p ./iac/terraform
         cp ./lambda-package/lambda-package.zip ./iac/terraform/lambda_function.zip
         # Or if Terraform uses a variable or different path, adjust accordingly:
         # cp ./lambda-package/lambda-package.zip ./path/that/terraform/expects/lambda_function.zip
         # Set environment variable if Terraform uses TF_VAR:
         echo "TF_VAR_lambda_package_path=$(pwd)/iac/terraform/lambda_function.zip" >> $GITHUB_ENV
     ```
  4. **Verify artifact exists** before Terraform operations:
     ```yaml
     - name: Verify Lambda package exists
       run: |
         # CRITICAL: Verify the exact path that Terraform code references
         # Check your Terraform code to find the exact filename and path expected
         TERRAFORM_LAMBDA_PATH="./iac/terraform/lambda_function.zip"
         if [ ! -f "$TERRAFORM_LAMBDA_PATH" ]; then
           echo "Error: Lambda package not found at: $TERRAFORM_LAMBDA_PATH"
           echo "Checking downloaded artifact location:"
           ls -la ./lambda-package/ || echo "lambda-package directory not found"
           echo "Current directory structure:"
           find . -name "*.zip" -o -name "lambda_function.zip" 2>/dev/null || echo "No zip files found"
           exit 1
         fi
         echo "✓ Lambda package verified at: $TERRAFORM_LAMBDA_PATH"
         ls -lh "$TERRAFORM_LAMBDA_PATH"
     ```
  5. Configure AWS credentials via OIDC (mandatory)
  6. Configure Terraform Cloud (if applicable)
  7. **Pass dependency artifacts to Terraform**:
     - Set environment variables or Terraform variables with artifact paths/URLs
     - Example: `TF_VAR_lambda_package_path=./iac/terraform/lambda_function.zip`
  8. **Plan Application**:
     - If NOT using Terraform Cloud: Download plan artifact and apply it
     - If using Terraform Cloud: Run `terraform plan` and `terraform apply -auto-approve` directly
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
- **Steps** (CRITICAL ORDER):
  1. **Checkout code**: For push triggers use standard checkout, for workflow_run add `ref: ${{ github.event.workflow_run.head_branch }}`
  2. **Download dependencies from upstream workflows FIRST** (if Terraform depends on other code types):
     ```yaml
     - name: Download Lambda package from upstream workflow
       uses: actions/download-artifact@v4
       with:
         name: lambda-package-test
         run-id: ${{ github.event.workflow_run.id }}
         github-token: ${{ secrets.GITHUB_TOKEN }}
         path: ./lambda-package
     ```
     - Or download from S3/container registry if artifacts were stored there
  3. **Place artifact in correct location** where Terraform code expects it:
     ```yaml
     - name: Move Lambda package to Terraform directory
       run: |
         mkdir -p ./iac/terraform
         cp ./lambda-package/lambda-package.zip ./iac/terraform/lambda_function.zip
         echo "TF_VAR_lambda_package_path=$(pwd)/iac/terraform/lambda_function.zip" >> $GITHUB_ENV
     ```
  4. **Verify artifact exists** before Terraform operations:
     ```yaml
     - name: Verify Lambda package exists
       run: |
         if [ ! -f "./iac/terraform/lambda_function.zip" ]; then
           echo "Error: lambda_function.zip not found at expected location!"
           exit 1
         fi
         echo "Lambda package verified at: ./iac/terraform/lambda_function.zip"
     ```
  5. Configure AWS credentials via OIDC (mandatory)
  6. Configure Terraform Cloud (if applicable)
  7. Run CI jobs (validate, plan, security)
  8. **Pass dependency artifacts to Terraform**:
     - Set environment variables or Terraform variables with artifact paths/URLs
     - Example: `TF_VAR_lambda_package_path=./iac/terraform/lambda_function.zip`
  9. **Plan Application**:
     - If NOT using Terraform Cloud: Download plan artifact and apply it
     - If using Terraform Cloud: Run `terraform plan` and `terraform apply -auto-approve` directly
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
    **Note**: For same-environment dependencies, prod workflow waits for dependency's prod workflow (e.g., "Python Prod"), not test workflow
- **Condition**: `if: ${{ github.event.workflow_run.conclusion == 'success' }}`
- **Steps** (CRITICAL ORDER):
  1. **Checkout code**: `ref: ${{ github.event.workflow_run.head_branch }}` (required for workflow_run triggers)
  2. **Download dependencies from upstream workflows FIRST** (if Terraform depends on other code types):
     ```yaml
     - name: Download Lambda package from upstream workflow
       uses: actions/download-artifact@v4
       with:
         name: lambda-package-prod
         run-id: ${{ github.event.workflow_run.id }}
         github-token: ${{ secrets.GITHUB_TOKEN }}
         path: ./lambda-package
     ```
     - Or download from S3/container registry if artifacts were stored there
  3. **Place artifact in correct location** where Terraform code expects it:
     ```yaml
     - name: Move Lambda package to Terraform directory
       run: |
         mkdir -p ./iac/terraform
         cp ./lambda-package/lambda-package.zip ./iac/terraform/lambda_function.zip
         echo "TF_VAR_lambda_package_path=$(pwd)/iac/terraform/lambda_function.zip" >> $GITHUB_ENV
     ```
  4. **Verify artifact exists** before Terraform operations:
     ```yaml
     - name: Verify Lambda package exists
       run: |
         if [ ! -f "./iac/terraform/lambda_function.zip" ]; then
           echo "Error: lambda_function.zip not found at expected location!"
           exit 1
         fi
         echo "Lambda package verified at: ./iac/terraform/lambda_function.zip"
     ```
  5. Configure AWS credentials via OIDC (mandatory)
  6. Configure Terraform Cloud (if applicable)
  7. Run CI jobs (validate, plan, security)
  8. **Pass dependency artifacts to Terraform**:
     - Set environment variables or Terraform variables with artifact paths/URLs
     - Example: `TF_VAR_lambda_package_path=./iac/terraform/lambda_function.zip`
  9. **Plan Application**:
     - If NOT using Terraform Cloud: Download plan artifact and apply it
     - If using Terraform Cloud: Run `terraform plan` and `terraform apply -auto-approve` directly
  10. Deploy to production environment
  11. Protected with GitHub environment protection rules

## Permissions

- **SARIF Upload**: `security-events: read`
- **AWS Operations**: `id-token: write` (for OIDC, mandatory)
- **Contents**: `read`

## Important Notes

- **Terraform Version**: MUST use version 1.1 or later (specify `terraform_version: ~1.1`)
- **Terraform Cloud Backend**: When using Terraform Cloud, plan output files are NOT supported. Skip plan artifact upload/download.
- **AWS Credentials**: OIDC configuration is MANDATORY for all Terraform jobs that interact with AWS
- **Concurrency**: Use concurrency groups to prevent overlapping deployments per environment

## Dependency Handling

**When Terraform depends on other code types** (e.g., Python Lambda package):

- **Workflow Triggers**: Add `workflow_run` triggers to wait for upstream workflows to complete
- **Download Artifacts**: Use `actions/download-artifact@v4` with `run-id` and `github-token` to download from upstream workflows
- **Artifact Passing**: Pass artifact paths/URLs to Terraform via environment variables or Terraform variables
- **Multiple Dependencies**: If Terraform depends on multiple code types, wait for all upstream workflows
- **Artifact Sources**: Download from GitHub Actions artifacts, S3, or container registries based on where upstream workflows store artifacts
