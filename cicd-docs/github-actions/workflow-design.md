# GitHub Actions Workflow Design

## Workflow Strategy
Based on code analysis, implementing 3 core workflows:
1. **Build & Test** - Terraform validation and Lambda testing
2. **Deploy to Staging** - Automated deployment to staging environment  
3. **Deploy to Production** - Manual approval deployment to production

## Workflow 1: Build and Test (.github/workflows/build-test.yml)

### Triggers
- Push to main branch
- Pull requests to main branch

### Jobs
1. **terraform-validate**
   - Terraform format check
   - Terraform validation
   - Terraform plan (dry run)

2. **lambda-test**
   - Node.js setup
   - Lambda function linting
   - Unit tests (when implemented)

### Environment Variables
- AWS_REGION
- TF_VAR_project_name

## Workflow 2: Deploy Staging (.github/workflows/deploy-staging.yml)

### Triggers
- Push to main branch (after build-test passes)

### Jobs
1. **deploy-infrastructure**
   - Terraform apply to staging environment
   - Post-deployment validation
   - Health checks

### Environment Variables
- AWS_ACCESS_KEY_ID (secret)
- AWS_SECRET_ACCESS_KEY (secret)
- TF_VAR_environment=staging

## Workflow 3: Deploy Production (.github/workflows/deploy-production.yml)

### Triggers
- Manual workflow dispatch
- Release tags (v*.*.*)

### Jobs
1. **deploy-with-approval**
   - Manual approval gate
   - Terraform apply to production
   - Rollback capability

### Environment Variables
- AWS_ACCESS_KEY_ID (secret)
- AWS_SECRET_ACCESS_KEY (secret)
- TF_VAR_environment=production

## Required GitHub Secrets
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- TF_VAR_key_pair_name

## Additional Files Needed
- package.json for Lambda development
- Terraform backend configuration
- Environment-specific tfvars files