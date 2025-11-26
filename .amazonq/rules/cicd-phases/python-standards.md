# Python CI/CD Workflow Standards

## Purpose

Define CI/CD workflow patterns and standards for Python code in single production workflow (triggered by main branch).

## CI Jobs

### Lint Job

- **Name**: `python-lint`
- **Matrix**: Python versions (3.10, 3.11, 3.12)
- **Continue on Error**: `continue-on-error: true` (job level) - allows workflow to continue even if linting fails
- **Steps**:
  - Setup Python with matrix version
  - Cache pip dependencies
  - Install dependencies: `pip install -r requirements.txt`
  - Run Flake8:
    ```yaml
    - name: Run Flake8
      run: |
        pip install flake8
        flake8 . || true  # Continue even if flake8 finds issues
    ```

### Security Job

- **Name**: `python-security`
- **Matrix**: Optional Python versions
- **Continue on Error**: `continue-on-error: true` (job level) - allows workflow to continue even if security scan finds issues
- **Steps**:
  - Setup Python
  - Cache pip dependencies
  - Install dependencies
  - Run Bandit:
    ```yaml
    - name: Run Bandit
      run: |
        pip install bandit
        bandit -r . || true  # Continue even if bandit finds security issues
    ```

### Tests Job

- **Name**: `python-tests`
- **Condition**: Only run if `tests/` directory exists
- **Matrix**: Python versions (3.10, 3.11, 3.12)
- **Continue on Error**: `continue-on-error: true` (job level) - allows workflow to continue even if tests fail
- **CRITICAL - hashFiles() Usage**:
  - **DO NOT** use `hashFiles()` at job level (`jobs.<job>.if`) - this is INVALID
  - **MUST** use `hashFiles()` at step level (`jobs.<job>.steps[*].if`) only
  - Apply condition to test-related steps (install test dependencies, run tests)
- **Steps**:
  - Setup Python with matrix version
  - Cache pip dependencies
  - Install dependencies including test requirements
  - Install test dependencies (with step-level condition):
    ```yaml
    - name: Install test dependencies
      if: ${{ hashFiles('tests/**') != '' }}
      run: |
        pip install pytest pytest-cov
    ```
  - Run pytest with coverage (with step-level condition):
    ```yaml
    - name: Run tests
      if: ${{ hashFiles('tests/**') != '' }}
      run: |
        pytest tests/ --cov=. --cov-report=xml --cov-report=html || true  # Continue even if tests fail
    ```
  - Upload coverage artifacts (coverage.xml, htmlcov/) - use `if: always()` to upload even if tests fail

## Build Job

**CRITICAL - Job Structure Decision**: When Terraform depends on Python Lambda artifacts, choose ONE of these patterns:

### Option 1: MOST PREFERRED - Combined Build and Deploy Job

**For tightly coupled dependencies where Terraform manages Lambda and no separate Python deploy is needed:**

- **No separate `python-build` job needed**
- Python build steps are included in `terraform-deploy` job
- Build happens in same runner as Terraform deploy
- **Benefits**: No artifact passing needed, simplest workflow, fewer jobs
- **See**: `workflow-dependency-handling.md` for complete combined job pattern

### Option 2: Separate Build Job

- **Name**: `python-build`
- **Needs**: All CI jobs (`python-lint`, `python-security`, `python-test`)
- **Steps**:
  - Setup Python
  - Cache pip dependencies
  - Install dependencies
  - **Build Lambda deployment package** (if applicable):
    - **PREFERRED - Local Build Placement**: If Terraform manages the Lambda function, build the package directly where Terraform expects it:
      ```yaml
      - name: Build Lambda package for Terraform
        run: |
          mkdir -p ./iac/terraform
          zip -r ./iac/terraform/lambda_function.zip . -x "*.git*" "*.md" "tests/*" "*.tf*" "iac/**"
          echo "✓ Lambda package built at: ./iac/terraform/lambda_function.zip"
      ```
      - **Benefits**: Terraform deploys Lambda source directly, no artifact upload/download needed, simpler workflow
      - **Note**: Terraform's `source_code_hash` attribute automatically detects changes and updates Lambda function code
      - **Note**: This still requires artifact passing between jobs. For simplest solution, use Option 1 (Combined Job)
    - **ALTERNATIVE - Artifact Upload**: If local build placement is not feasible (e.g., multiple consumers), use artifact upload:
      ```yaml
      - name: Build Lambda package
        run: |
          zip -r lambda-package.zip . -x "*.git*" "*.md" "tests/*"
      - name: Upload Lambda package artifact
        uses: actions/upload-artifact@v4
        with:
          name: lambda-package
          path: lambda-package.zip
          retention-days: 1
      ```

## Deployment Job

- **Name**: `python-deploy`
- **Needs**:
  - Build job (`python-build`) and all CI jobs
  - **CRITICAL - Infrastructure Dependencies**: If Python deploy needs infrastructure created by other code types
    - Example: Python deploy updates Lambda function that Terraform creates → `python-deploy` needs `terraform-deploy`
    - Wait for upstream **deploy jobs** that create required infrastructure
    - Example: `needs: [python-build, terraform-deploy]`
- **Condition**: `if: always()` - runs even if CI jobs fail (since CI jobs use `continue-on-error: true`)
- **Environment**: `production`
- **Workflow Trigger**: `push` to `main` branch only
- **Infrastructure Dependency Detection**:
  - **MANDATORY**: Check if Python deploy job updates/creates resources that other code types (e.g., Terraform) create
  - If deploy uses `aws lambda update-function-code` or `aws lambda create-function` for functions created by Terraform → infrastructure dependency exists
  - Load artifact-mappings.json: If `lambda_functions` array exists AND Terraform creates those functions → infrastructure dependency
- **Steps**:
  - Checkout code
  - Configure AWS credentials via OIDC (if needed)
  - Download build artifacts if needed (from build job)
  - Deploy to production environment
  - Use production environment secrets and variables
  - Protected with GitHub environment protection rules

## Permissions

- **AWS Operations**: `id-token: write` (for OIDC)
- **Contents**: `read` (default)

## Common Patterns

- Cache pip dependencies for faster builds
- Use matrix strategy for multiple Python versions
- Conditional test execution based on `tests/` directory existence
- Artifact upload in build job, download in deploy job (within same workflow)
- Production environment configuration via GitHub environments
- **Non-blocking CI jobs**: All CI jobs (lint, security, tests) use `continue-on-error: true` to allow workflow to proceed even if CI checks fail
- **Deployment always runs**: Deployment job uses `if: always()` condition to ensure it runs regardless of CI job outcomes

## Dependency Handling

**When Python code is a dependency for other code types** (e.g., Terraform needs Lambda package):

- **PREFERRED - Local Build Placement**: If Terraform manages the Lambda function, build the package directly where Terraform expects it:
  - **Build Location**: Build Lambda package directly in Terraform directory (e.g., `iac/terraform/lambda_function.zip`)
  - **Benefits**:
    - Terraform deploys Lambda source directly via `terraform apply`
    - No artifact upload/download needed
    - Simpler workflow with fewer steps
    - Terraform's `source_code_hash` automatically detects changes and updates Lambda function code
  - **Implementation**: Build job creates package in Terraform directory, Terraform deploy job uses it directly
  - **No Separate Deploy Job Needed**: When Terraform manages Lambda, no separate `python-deploy` job is needed - Terraform handles both infrastructure and Lambda source code deployment
- **ALTERNATIVE - Artifact Upload/Download**: If local build placement is not feasible (e.g., multiple consumers or complex dependency chains):
  - **Build and Package**: Create Lambda deployment package (zip file) in build job
  - **Upload Artifacts**: Upload packages using `actions/upload-artifact@v4` in build job
  - **Artifact Naming**: Use simple, consistent naming: `lambda-package` (no environment suffix needed for single workflow)
  - **Download in Downstream Jobs**: Downstream deploy jobs (e.g., `terraform-deploy`) download artifacts from build job using `actions/download-artifact@v4`
  - **Artifact Passing**: All artifact passing happens within the same workflow using GitHub Actions artifacts
