# CI/CD Detection Plan

## Detection Summary

**Timestamp**: 2025-01-28T15:30:00Z

### Code Types Detected

- [x] **Python** (Lambda function)
  - Location: `src/lambda-python-s3-trigger/`
  - Runtime: Python 3.12
  - Build tool: pip
  - Tests: pytest (`tests/s3-trigger/`)

- [x] **Terraform** (Infrastructure)
  - Location: `iac/terraform/`
  - Version: ~1.1
  - Resources: S3, Lambda, IAM, CloudWatch
  - Backend: Terraform Cloud (detected from standards)

### Dependency Analysis

**Terraform depends on Python Lambda package**:
- Terraform manages Lambda function creation
- Lambda source: `iac/terraform/lambda_function.zip`
- Build location: Package built directly in Terraform directory
- Deployment: Terraform deploys both infrastructure AND Lambda source code via `source_code_hash`

**Dependency Pattern**: Combined Build and Deploy Job (PREFERRED)
- Single `terraform-deploy` job includes Python build steps
- No separate `python-deploy` job needed
- No artifact upload/download required

### Existing Workflows

- No existing workflows found in `.github/workflows/`

### Secrets & Environment Variables

**Required Secrets**:
- `AWS_ROLE_TO_ASSUME` - OIDC role ARN
- `TFC_TOKEN` - Terraform Cloud token

**Required Variables**:
- `AWS_REGION` - AWS region (default: us-east-1)

### Workflow Architecture

**Single Production Workflow**: `.github/workflows/ci-cd.yml`
- Trigger: `push` to `main` branch + `workflow_dispatch`
- Environment: `production` (single environment)

**Job Structure**:
1. **Python CI Jobs**: lint, security, test (parallel, continue-on-error)
2. **Terraform CI Jobs**: validate, security (parallel, continue-on-error)
3. **Terraform Deploy Job**: Combined Python build + Terraform deploy
   - Builds Lambda package in `iac/terraform/lambda_function.zip`
   - Runs Terraform init/plan/apply
   - Terraform deploys Lambda source automatically

## Phase 1 Checklist

- [x] Load state file and requirements
- [x] Detect code types (Python, Terraform)
- [x] Analyze dependencies (Terraform → Python artifact)
- [x] Identify build tools and test frameworks
- [x] Check for existing workflows
- [x] Document secrets and environment variables
- [x] Define workflow architecture (single production workflow)
- [x] Record findings in detection plan
- [ ] User approval to proceed to Phase 2
