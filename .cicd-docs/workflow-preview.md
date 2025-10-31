# Generated Workflow Preview

## Python CI Workflow (`python-ci.yml`)

### Triggers
- Push to `main`, `develop` branches
- Pull requests to `main` branch
- Path filters: `src/**`, `tests/**`, `requirements.txt`, workflow file

### Jobs Overview
1. **python-lint**: Matrix testing (Python 3.10, 3.11, 3.12)
   - Flake8 SARIF linting
   - Upload SARIF to GitHub Security tab
2. **python-security**: Security scanning
   - Bandit SARIF security analysis
   - Upload SARIF to GitHub Security tab
3. **python-tests**: Unit testing with coverage
   - pytest with coverage reports
   - Upload coverage artifacts

### Key Features
- Matrix strategy for multiple Python versions
- Dependency caching for faster builds
- SARIF uploads for security integration
- Coverage reporting and artifacts

## Terraform CI Workflow (`terraform-ci.yml`)

### Triggers
- Push to `main`, `develop` branches
- Pull requests to `main` branch
- Path filters: `iac/terraform/**`, workflow file

### Jobs Overview
1. **tf-validate**: Format and validation
   - `terraform fmt -check`
   - `terraform init` and `terraform validate`
   - AWS OIDC authentication
2. **tf-plan**: Plan generation
   - Terraform plan execution
   - Terraform Cloud integration
3. **tf-lint**: Code quality
   - TFLint analysis
4. **tf-security**: Security scanning
   - Checkov SARIF security analysis
   - Upload SARIF to GitHub Security tab

### Key Features
- Terraform Cloud backend support
- AWS OIDC authentication
- Security scanning with SARIF
- No plan artifacts (Terraform Cloud limitation)

## Required Secrets & Variables

### Secrets
- `TFC_TOKEN`: Terraform Cloud API token
- `AWS_ROLE_TO_ASSUME`: AWS IAM role ARN for OIDC

### Variables
- `AWS_REGION`: AWS region for deployments

## Security Features
- SARIF uploads for GitHub Security tab integration
- OIDC authentication for AWS
- Secure secret management
- Comprehensive security scanning (Bandit, Checkov)