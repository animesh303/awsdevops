# Generated Workflow Summary

## Workflow Files Generated

### 1. terraform-ci.yml
- **File**: `.github/workflows/terraform-ci.yml`
- **Purpose**: Terraform CI pipeline with validation, planning, and security scanning
- **Environments**: Terraform only (Python not detected)

## Workflow Details

### Triggers
- **Push**: main, develop branches
- **Pull Request**: main branch
- **Path Filters**: iac/terraform/**, .github/workflows/terraform-ci.yml

### Jobs Overview
1. **tf-validate** - Format check, init, validate
2. **tf-plan** - Terraform planning (depends on tf-validate)
3. **tf-security** - Checkov security scanning (parallel)
4. **tf-upload-sarif** - Upload security results (depends on tf-security)

### Security Features
- AWS OIDC authentication
- Checkov SARIF security scanning
- Terraform Cloud backend support
- Proper permissions (contents:read, security-events:write, id-token:write)

### Required Configuration
- **Secrets**: AWS_ROLE_TO_ASSUME, TFC_TOKEN
- **Variables**: AWS_REGION
- **Terraform Version**: 1.1+

## Artifacts Generated
- Checkov SARIF results uploaded to GitHub Security tab
- Terraform plan output (displayed in logs)

## Key Benefits
- Automated security scanning
- Infrastructure validation
- Multi-environment support
- Terraform Cloud integration
- SARIF security reporting