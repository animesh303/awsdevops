# Simple CI/CD Rules for Amazon Q Developer

This directory contains a streamlined CI/CD process framework that guides Amazon Q Developer through a simple 3-phase process: analyze code, generate GitHub Actions, and deploy & validate.

## Overview

The CI/CD process framework is designed to be bare minimal and focused. It follows a simple 3-phase approach: analyze code → generate GitHub Actions → deploy & validate.

## Process Structure

### Introduction

- **devops-introduction/process-overview.md** - Simple CI/CD workflow overview
- **devops-introduction/session-continuity.md** - Session state management

### Phases

- **devops-phases/phase1-analyze-code.md** - Analyze code repository and requirements
- **devops-phases/phase2-generate-github-actions.md** - Generate GitHub Actions workflows
- **devops-phases/phase3-deploy-validate.md** - Deploy and validate CI/CD pipeline

### Standards

- **devops-standards/aws-infrastructure-as-code.md** - Terraform/CloudFormation standards
- **devops-standards/aws-project-structure.md** - Project organization and folder structure
- **devops-standards/aws-security-compliance.md** - Security best practices and compliance
- **devops-standards/aws-monitoring-observability.md** - Monitoring and observability standards
- **devops-standards/aws-cicd-pipeline.md** - CI/CD pipeline standards and practices
- **devops-standards/aws-cost-optimization.md** - Cost optimization strategies
- **devops-standards/aws-disaster-recovery-backup.md** - Disaster recovery and backup strategies
- **devops-standards/aws-networking-vpc.md** - VPC and networking configuration
- **devops-standards/aws-lambda-serverless.md** - Lambda and serverless best practices (Python-focused)
- **devops-standards/aws-database-rds.md** - Database and RDS configuration
- **devops-standards/aws-programming-languages.md** - Programming language standards (Python-prioritized)

### Workflow

- **cicd-workflow.md** - Main workflow file for the simple 3-phase process

## How to Use

1. **Automatic Loading**: The CI/CD workflow is automatically triggered when Amazon Q Developer detects CI/CD-related requests
2. **Phase Progression**: Each phase must be completed and approved before proceeding to the next
3. **Context Loading**: Each phase automatically loads relevant artifacts from previous phases
4. **Rule Integration**: Standards rules are automatically applied during each phase
5. **Progress Tracking**: Simple checkbox system tracks progress

## Process Flow

```
Analyze Code → Generate GitHub Actions → Deploy & Validate
```

## Key Features

- **Bare Minimal**: Only 3 phases for maximum simplicity
- **Code-Focused**: Starts with code analysis to understand requirements
- **GitHub Actions**: Generates appropriate workflows based on code analysis
- **Quick Validation**: Fast deployment and validation of CI/CD pipeline
- **Team Collaboration**: Simple approval process at each phase

## Phase Details

### Phase 1: Analyze Code

- Analyze current project root code structure
- Identify programming languages and frameworks
- Determine build and test requirements
- Understand deployment needs

### Phase 2: Generate GitHub Actions

- Create build workflows
- Generate test workflows
- Design deployment workflows
- Set up environment variables and secrets

### Phase 3: Deploy & Validate

- Deploy GitHub Actions to repository
- Test workflow execution
- Validate CI/CD pipeline functionality
- Monitor and report results

## Customization

You can customize the simple CI/CD process by:

1. Modifying phase requirements to match your needs
2. Adding specific GitHub Actions templates
3. Adjusting validation criteria
4. Customizing the workflow progression

## Best Practices

1. **Start with Code**: Always analyze the code first to understand requirements
2. **Follow the Process**: Complete each phase in order for best results
3. **Test Thoroughly**: Validate the generated workflows work correctly
4. **Keep It Simple**: Focus on essential CI/CD functionality
5. **Document Decisions**: Maintain clear documentation of choices made

## Troubleshooting

If the CI/CD process isn't working as expected:

1. Check that all phase files are present and properly formatted
2. Verify code analysis is complete before generating workflows
3. Ensure GitHub Actions files are properly formatted
4. Test workflows in a safe environment first
5. Check Amazon Q Developer logs for process issues

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [AWS Best Practices](https://aws.amazon.com/architecture/well-architected/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest)
