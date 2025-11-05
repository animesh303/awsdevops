# Python CI/CD Workflow Standards

## Purpose

Define CI/CD workflow patterns and standards for Python code in unified workflow files.

## CI Jobs

### Lint Job

- **Name**: `python-lint`
- **Matrix**: Python versions (3.10, 3.11, 3.12)
- **Steps**:
  - Setup Python with matrix version
  - Cache pip dependencies
  - Install dependencies: `pip install -r requirements.txt`
  - Run Flake8:
    ```yaml
    - name: Run Flake8
      run: |
        pip install flake8
        flake8 .
    ```

### Security Job

- **Name**: `python-security`
- **Matrix**: Optional Python versions
- **Steps**:
  - Setup Python
  - Cache pip dependencies
  - Install dependencies
  - Run Bandit:
    ```yaml
    - name: Run Bandit
      run: |
        pip install bandit
        bandit -r . || true
    ```
  - Set `continue-on-error: true` for the job

### Tests Job

- **Name**: `python-tests`
- **Condition**: Only run if `tests/` directory exists
- **Matrix**: Python versions (3.10, 3.11, 3.12)
- **Steps**:
  - Setup Python with matrix version
  - Cache pip dependencies
  - Install dependencies including test requirements
  - Run pytest with coverage:
    ```yaml
    - name: Run tests
      run: |
        pytest tests/ --cov=. --cov-report=xml --cov-report=html
    ```
  - Upload coverage artifacts (coverage.xml, htmlcov/)


## Deployment Jobs

**Note**: Each environment has its own workflow file. The deployment job below applies to the corresponding environment workflow.

### Deploy to Dev (in `python-dev.yml`)

- **Name**: `deploy-dev`
- **Needs**: All CI jobs
- **Environment**: `dev`
- **Workflow Trigger**: `on.push.branches: [develop]`
- **Steps**:
  - Configure AWS credentials via OIDC (if needed)
  - Download build artifacts if needed
  - **Build Lambda deployment package** (if applicable):
    ```yaml
    - name: Build Lambda package
      run: |
        zip -r lambda-package.zip . -x "*.git*" "*.md" "tests/*"
    ```
  - Deploy to development environment
  - Use environment-specific secrets and variables
  - **Upload artifacts for downstream workflows** (if this Python code is a dependency):
    ```yaml
    - name: Upload Lambda package artifact
      uses: actions/upload-artifact@v4
      with:
        name: lambda-package-dev
        path: lambda-package.zip
        retention-days: 1
    ```
    - Or upload to S3/container registry for cross-workflow access
    - Export artifact location (path/URL) as workflow output or environment variable

### Deploy to Test (in `python-test.yml`)

- **Name**: `deploy-test`
- **Needs**: All CI jobs (within the test workflow)
- **Environment**: `test`
- **Workflow Trigger**: `push` to `main` branch
- **Steps**:
  - Checkout code (standard checkout for push trigger)
  - Configure AWS credentials via OIDC (if needed)
  - Run CI jobs (lint, security, tests)
  - **Build Lambda deployment package** (if applicable)
  - Download artifacts if needed
  - Deploy to test environment
  - Use environment-specific secrets and variables
  - **Upload artifacts for downstream workflows** (if this Python code is a dependency):
    ```yaml
    - name: Upload Lambda package artifact
      uses: actions/upload-artifact@v4
      with:
        name: lambda-package-test
        path: lambda-package.zip
        retention-days: 1
    ```

### Deploy to Prod (in `python-prd.yml`)

- **Name**: `deploy-prod`
- **Needs**: All CI jobs (within the prod workflow)
- **Environment**: `prod`
- **Workflow Trigger**: `workflow_run` on successful completion of `python-test.yml` with `branches: [main]`
- **Condition**: `if: ${{ github.event.workflow_run.conclusion == 'success' }}`
- **Steps**:
  - Checkout code: `ref: ${{ github.event.workflow_run.head_branch }}` (required for workflow_run triggers)
  - Configure AWS credentials via OIDC (if needed)
  - Run CI jobs (lint, security, tests)
  - **Build Lambda deployment package** (if applicable)
  - Download artifacts if needed
  - Deploy to production environment
  - Use environment-specific secrets and variables
  - **Upload artifacts for downstream workflows** (if this Python code is a dependency):
    ```yaml
    - name: Upload Lambda package artifact
      uses: actions/upload-artifact@v4
      with:
        name: lambda-package-prod
        path: lambda-package.zip
        retention-days: 1
    ```
  - Protected with GitHub environment protection rules

## Permissions

- **AWS Operations**: `id-token: write` (for OIDC)
- **Contents**: `read` (default)

## Common Patterns

- Cache pip dependencies for faster builds
- Use matrix strategy for multiple Python versions
- Conditional test execution based on `tests/` directory existence
- Artifact upload/download for deployment jobs
- Environment-specific configuration via GitHub environments

## Dependency Handling

**When Python code is a dependency for other code types** (e.g., Terraform needs Lambda package):

- **Build and Package**: Create Lambda deployment package (zip file) in deployment jobs
- **Upload Artifacts**: Upload packages using `actions/upload-artifact@v4` with environment-specific names
- **Artifact Naming**: Use standardized naming convention: `{artifact-type}-{environment}` (e.g., `lambda-package-dev`, `lambda-package-test`, `lambda-package-prod`)
- **Export Information**: Make artifact paths/URLs available to downstream workflows via workflow outputs or environment variables
