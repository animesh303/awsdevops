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
- **Steps**:
  - Checkout code: `ref: ${{ github.event.workflow_run.head_branch }}` (if using workflow_run trigger)
  - **Download dependencies from upstream workflows** (if Terraform depends on other code types):
    ```yaml
    - name: Download Lambda package from upstream workflow
      uses: actions/download-artifact@v4
      with:
        name: lambda-package-dev
        run-id: ${{ github.event.workflow_run.id }}
        github-token: ${{ secrets.GITHUB_TOKEN }}
        path: ./lambda-package
    ```
    - Or download from S3/container registry if artifacts were stored there
  - Configure AWS credentials via OIDC (mandatory)
  - Configure Terraform Cloud (if applicable)
  - **Pass dependency artifacts to Terraform**:
    - Set environment variables or Terraform variables with artifact paths/URLs
    - Example: `TF_VAR_lambda_package_path=./lambda-package/lambda-package.zip`
  - **Plan Application**:
    - If NOT using Terraform Cloud: Download plan artifact and apply it
    - If using Terraform Cloud: Run `terraform plan` and `terraform apply -auto-approve` directly
  - Deploy to development environment

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
- **Steps**:
  - Checkout code: For push triggers use standard checkout, for workflow_run add `ref: ${{ github.event.workflow_run.head_branch }}`
  - **Download dependencies from upstream workflows** (if Terraform depends on other code types):
    ```yaml
    - name: Download Lambda package from upstream workflow
      uses: actions/download-artifact@v4
      with:
        name: lambda-package-test
        run-id: ${{ github.event.workflow_run.id }}
        github-token: ${{ secrets.GITHUB_TOKEN }}
        path: ./lambda-package
    ```
  - Configure AWS credentials via OIDC (mandatory)
  - Configure Terraform Cloud (if applicable)
  - Run CI jobs (validate, plan, security)
  - **Pass dependency artifacts to Terraform**:
    - Set environment variables or Terraform variables with artifact paths/URLs
    - Example: `TF_VAR_lambda_package_path=./lambda-package/lambda-package.zip`
  - **Plan Application**:
    - If NOT using Terraform Cloud: Download plan artifact and apply it
    - If using Terraform Cloud: Run `terraform plan` and `terraform apply -auto-approve` directly
  - Deploy to test environment

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
- **Steps**:
  - Checkout code: `ref: ${{ github.event.workflow_run.head_branch }}` (required for workflow_run triggers)
  - **Download dependencies from upstream workflows** (if Terraform depends on other code types):
    ```yaml
    - name: Download Lambda package from upstream workflow
      uses: actions/download-artifact@v4
      with:
        name: lambda-package-prod
        run-id: ${{ github.event.workflow_run.id }}
        github-token: ${{ secrets.GITHUB_TOKEN }}
        path: ./lambda-package
    ```
  - Configure AWS credentials via OIDC (mandatory)
  - Configure Terraform Cloud (if applicable)
  - Run CI jobs (validate, plan, security)
  - **Pass dependency artifacts to Terraform**:
    - Set environment variables or Terraform variables with artifact paths/URLs
    - Example: `TF_VAR_lambda_package_path=./lambda-package/lambda-package.zip`
  - **Plan Application**:
    - If NOT using Terraform Cloud: Download plan artifact and apply it
    - If using Terraform Cloud: Run `terraform plan` and `terraform apply -auto-approve` directly
  - Deploy to production environment
  - Protected with GitHub environment protection rules

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
