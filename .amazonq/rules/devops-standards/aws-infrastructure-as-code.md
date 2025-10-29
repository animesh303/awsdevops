# AWS Infrastructure as Code (IaC)

## Purpose

Ensures consistent, secure, and maintainable AWS infrastructure using Infrastructure as Code principles with Terraform and CloudFormation.

## Instructions

- ALWAYS use Terraform as the primary IaC tool for new projects, with HCL (HashiCorp Configuration Language) (ID: USE_TERRAFORM)
- When Terraform is not suitable, use CloudFormation with YAML format, never JSON (ID: CLOUDFORMATION_YAML)
- ALWAYS organize Terraform modules in a hierarchical structure: modules/[service]/[component] (ID: TERRAFORM_STRUCTURE)
- ALWAYS include comprehensive comments explaining the purpose and configuration of each resource (ID: DOCUMENT_RESOURCES)
- ALWAYS use environment-specific configurations (dev/staging/prod) with separate Terraform workspaces or directories (ID: ENVIRONMENT_SEPARATION)
- ALWAYS implement proper tagging strategy with mandatory tags: Environment, Project, Owner, CostCenter (ID: MANDATORY_TAGS)
- ALWAYS use Terraform best practices: variable validation, output exports, and module composition (ID: TERRAFORM_BEST_PRACTICES)
- ALWAYS implement least privilege IAM policies with explicit permissions (ID: LEAST_PRIVILEGE_IAM)
- ALWAYS use latest Terraform AWS provider version and avoid deprecated resources (ID: USE_LATEST_TERRAFORM)
- ALWAYS include cost optimization measures: auto-scaling, spot instances where appropriate, and resource lifecycle policies (ID: COST_OPTIMIZATION)
- ALWAYS implement proper error handling and rollback strategies in Terraform configurations (ID: ERROR_HANDLING)
- ALWAYS validate Terraform code with `terraform plan` and `terraform validate` before deployment (ID: TERRAFORM_VALIDATION)
- ALWAYS use Terraform variables and locals for environment-specific configurations (ID: TERRAFORM_VARIABLES)
- ALWAYS implement proper resource naming conventions: {Project}-{Environment}-{Service}-{Resource} (ID: RESOURCE_NAMING)
- ALWAYS include monitoring and logging configuration for all resources (ID: MONITORING_CONFIG)
- ALWAYS use Terraform data sources and remote state for cross-module references (ID: TERRAFORM_DATA_SOURCES)

## Priority

Critical

## Error Handling

- If Terraform is not available, fall back to CloudFormation with YAML format
- If HCL is not preferred, use Terraform with JSON syntax but document the reason
- If environment separation is not possible, use Terraform variables with clear documentation
- If mandatory tags cannot be applied, create a separate tagging policy and document the exception
- If cost optimization measures conflict with requirements, document the trade-offs and get approval
