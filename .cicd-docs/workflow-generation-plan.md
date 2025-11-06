# Phase 2: Workflow Generation Plan

## Workflow Generation Tasks

### Python Workflows
- [x] Generate `python-dev.yml` - CI + Deploy to Dev (triggers on `develop` branch)
- [x] Generate `python-test.yml` - CI + Deploy to Test (triggers on `main` branch)
- [x] Generate `python-prd.yml` - CI + Deploy to Prod (triggers via workflow_run after test)

### Terraform Workflows  
- [x] Generate `terraform-dev.yml` - CI + Deploy to Dev (waits for Python dev via workflow_run)
- [x] Generate `terraform-test.yml` - CI + Deploy to Test (waits for Python test via workflow_run)
- [x] Generate `terraform-prd.yml` - CI + Deploy to Prod (waits for Python prod via workflow_run)

### Dependency Implementation
- [x] Add workflow_run triggers for Terraform workflows to wait for Python
- [x] Add artifact upload steps in Python workflows (lambda-package-{env})
- [x] Add artifact download steps in Terraform workflows
- [x] Add artifact verification before Terraform operations
- [x] Configure checkout with ref parameter for workflow_run triggers

### Validation
- [x] Validate all workflow YAML syntax
- [x] Verify GitHub Actions expressions use ${{ }} syntax
- [x] Check workflow triggers and dependencies
- [x] Validate environment configurations
- [x] Confirm artifact passing implementation

## Standards Application
- [x] Apply Python standards from `python-standards.md`
- [x] Apply Terraform standards from `terraform-standards.md`
- [x] Follow AWS security best practices
- [x] Include proper permissions and OIDC configuration