# Workflow Generation Plan

## Generated Environment-Specific Workflows

- [x] **Python Dev** (`python-dev.yml`): CI + Deploy to Dev (triggers on develop branch)
- [x] **Python Test** (`python-test.yml`): CI + Deploy to Test (triggers on main branch)  
- [x] **Python Prod** (`python-prd.yml`): CI + Deploy to Prod (workflow_run after Python Test)
- [x] **Terraform Dev** (`terraform-dev.yml`): CI + Deploy to Dev (workflow_run after Python Dev + push fallback)
- [x] **Terraform Test** (`terraform-test.yml`): CI + Deploy to Test (workflow_run after Python Test + push fallback)
- [x] **Terraform Prod** (`terraform-prd.yml`): CI + Deploy to Prod (workflow_run after Terraform Test + Python Prod)

## Dependency Handling Implementation

- [x] **Python Workflows**: Build and upload Lambda deployment packages as `lambda-package-{environment}` artifacts
- [x] **Terraform Workflows**: Download Lambda packages from upstream Python workflows using `actions/download-artifact@v4`
- [x] **Artifact Placement**: Move downloaded packages to `./iac/terraform/lambda_function.zip` where Terraform expects them
- [x] **Verification Steps**: Verify artifacts exist before Terraform operations
- [x] **Workflow Triggers**: Terraform workflows wait for Python workflows via `workflow_run` triggers

## Multi-Environment Strategy Implementation

- [x] **Dev Environment**: Python Dev (develop branch) → Terraform Dev (workflow_run + push fallback)
- [x] **Test Environment**: Python Test (main branch) → Terraform Test (workflow_run + push fallback)
- [x] **Prod Environment**: Python Test → Python Prod → Terraform Test + Python Prod → Terraform Prod

## CI/CD Standards Applied

- [x] **Python Standards**: Lint (Flake8), Security (Bandit), Tests (pytest), Lambda packaging
- [x] **Terraform Standards**: Validate, Plan, Security (Checkov), AWS OIDC, Terraform Cloud support
- [x] **GitHub Actions Best Practices**: Proper checkout, artifact handling, environment protection

## Workflow Linting Validation

- [x] **YAML Syntax**: All workflows have valid YAML syntax
- [x] **GitHub Actions Expressions**: All expressions use `${{ }}` syntax (hashFiles, conditions, etc.)
- [x] **Required Fields**: All workflows have name, on, jobs, runs-on fields
- [x] **Job Dependencies**: Valid needs relationships, no circular dependencies
- [x] **Workflow Triggers**: Correct workflow_run and push trigger syntax
- [x] **Environment Names**: Valid environment names (dev, test, prod)

## Generation Complete

All 6 environment-specific workflow files generated with dependency handling and linting validation passed.