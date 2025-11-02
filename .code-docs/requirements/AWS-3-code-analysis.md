# AWS-3 Code Analysis

## Existing Codebase Analysis

### Current Structure
- **iac/**: Directory does not exist - will create new
- **src/**: Empty directory - will create new application code
- **tests/**: Empty directory - will create new tests
- **.gitignore**: Exists - will update with Terraform and Python ignores

### Implementation Plan
- **New Implementation**: No existing AWS-3 resources found
- **Feature Name**: two-tier-web-app
- **Resources to Create**: All infrastructure and application code from scratch

### Tagging Strategy
- All resources will be tagged with `JiraId = "AWS-3"` and `ManagedBy = "terraform"`

## Code Generation Plan

### Infrastructure (Terraform)
- Create `iac/terraform/` directory structure
- Generate VPC, subnets, security groups, EC2, ALB, S3, IAM resources
- Implement two-tier architecture (Web + App tiers)

### Application Code (Python)
- Create `src/lambda-two-tier-web-app/` directory
- Generate Python application code for web and app tiers
- Include requirements.txt and proper error handling

### Testing
- Create `tests/two-tier-web-app/` directory
- Generate unit tests for application code
- Include infrastructure validation tests