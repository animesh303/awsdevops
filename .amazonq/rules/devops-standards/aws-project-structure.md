# AWS Project Structure

## Purpose

Defines standard folder structure and organization for AWS-based projects to ensure consistency, maintainability, and team collaboration.

## Instructions

- ALWAYS organize projects with the following structure:
  ` ```
  project-root/
  ├── infrastructure/ # Terraform/CloudFormation code
  │ ├── modules/ # Terraform modules
  │ ├── environments/ # Environment-specific configurations
  │ │ ├── dev/ # Development environment
  │ │ ├── staging/ # Staging environment
  │ │ └── prod/ # Production environment
  │ ├── main.tf # Main Terraform configuration
  │ ├── variables.tf # Variable definitions
  │ ├── outputs.tf # Output definitions
  │ └── terraform.tfvars # Variable values
  ├── src/ # Application source code
  │ ├── functions/ # Lambda functions
  │ ├── layers/ # Lambda layers
  │ └── shared/ # Shared utilities
  ├── tests/ # Test files
  │ ├── unit/ # Unit tests
  │ ├── integration/ # Integration tests
  │ └── e2e/ # End-to-end tests
  ├── docs/ # Documentation
  ├── scripts/ # Deployment and utility scripts
  ├── .github/ # GitHub Actions workflows
  ├── .aws/ # AWS CLI configuration
  └── .amazonq/ # Amazon Q rules
  ```(ID: STANDARD_STRUCTURE)

  ```
- ALWAYS use kebab-case for all folder and file names (ID: NAMING_CONVENTION)
- ALWAYS separate Lambda functions by service/feature in the functions directory (ID: LAMBDA_ORGANIZATION)
- ALWAYS include a README.md in the root with project overview, setup instructions, and deployment guide (ID: ROOT_README)
- ALWAYS include environment-specific configuration files (.env.dev, .env.staging, .env.prod) (ID: ENV_CONFIGS)
- ALWAYS use consistent naming for Terraform resources: {ProjectName}-{Environment}-{Service} (ID: TERRAFORM_NAMING)
- ALWAYS include a .gitignore file with AWS-specific exclusions (ID: GITIGNORE_AWS)
- ALWAYS organize documentation by feature/service in the docs directory (ID: DOCS_ORGANIZATION)
- ALWAYS include deployment scripts in the scripts directory with clear naming (ID: DEPLOYMENT_SCRIPTS)
- ALWAYS use consistent package.json structure for Node.js projects (ID: PACKAGE_JSON_STRUCTURE)
- ALWAYS include TypeScript configuration files (tsconfig.json) for all TypeScript projects (ID: TYPESCRIPT_CONFIG)
- ALWAYS organize test files to mirror the source code structure (ID: TEST_STRUCTURE)
- ALWAYS include a .editorconfig file for consistent code formatting (ID: EDITOR_CONFIG)
- ALWAYS use consistent import/export patterns throughout the project (ID: IMPORT_EXPORT_PATTERNS)
- ALWAYS include a CHANGELOG.md for tracking project changes (ID: CHANGELOG)
- ALWAYS organize Terraform modules by AWS service in the modules directory (ID: TERRAFORM_MODULE_ORGANIZATION)

## Priority

High

## Error Handling

- If the standard structure doesn't fit the project needs, document the deviations and reasons
- If multiple programming languages are used, create language-specific subdirectories
- If the project is a monorepo, adapt the structure to support multiple services
- If Terraform is not used, replace infrastructure/ with appropriate IaC tool structure
- If documentation is extensive, consider using a docs-as-code approach with separate repositories
