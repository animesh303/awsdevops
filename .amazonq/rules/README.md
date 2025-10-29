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

### Workflows

- **cicd-workflow.md** - Main workflow file for the simple 3-phase CI/CD process
- **jira-task-workflow.md** - JIRA task management workflow for requirements generation
- **generate-code-workflow.md** - Code generation workflow for implementing requirements

## How to Use

1. **Automatic Loading**: The CI/CD workflow is automatically triggered when Amazon Q Developer detects CI/CD-related requests
2. **Phase Progression**: Each phase must be completed and approved before proceeding to the next
3. **Context Loading**: Each phase automatically loads relevant artifacts from previous phases
4. **Rule Integration**: Standards rules are automatically applied during each phase
5. **Progress Tracking**: Simple checkbox system tracks progress

## Process Flows

### CI/CD Process Flow

```
Analyze Code → Generate GitHub Actions → Deploy & Validate
```

### JIRA Task Management Flow

```
Fetch & Select JIRA Tickets → Generate Requirements Spec → Review & Iterate
```

### Code Generation Flow

```
Select Requirements → Generate Code → Review & Refine
```

### Session Continuity

- **jira-phases/session-continuity.md** - Session continuity for JIRA task management
- **code-phases/session-continuity.md** - Session continuity for code generation

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

## JIRA Task Management Process

The JIRA task management workflow provides a structured approach to working with JIRA tickets and generating technical requirements.

### Phase 1: Fetch & Select JIRA Tickets

- Connect to JIRA using MCP integration
- Fetch all open tickets for the user
- Display tickets in a user-friendly format
- Allow user to select specific ticket to work on
- Extract detailed ticket information

### Phase 2: Generate Requirements Spec

- Analyze selected JIRA ticket details
- Generate comprehensive technical requirements document
- Use standardized requirements template
- Include functional and non-functional requirements
- Create acceptance criteria and technical specifications

### Phase 3: Review & Iterate

- Present requirements document for user review
- Handle user feedback and requested changes
- Iterate on requirements until user approval
- Maintain complete change history
- Finalize approved requirements document

### Session Continuity Features

- **Smart Context Loading**: Automatically loads relevant artifacts based on current phase
- **Resume Capability**: Continue from where you left off in any phase
- **Context Awareness**: Shows current status and next steps
- **Artifact Management**: Tracks all generated documents and progress

## Code Generation Process

The code generation workflow provides a structured approach to implementing requirements and generating production-ready code.

### Phase 1: Select Requirements

- Scan for available requirements documents
- Display requirements in user-friendly format
- Allow user to select specific requirements to implement
- Analyze requirements for code generation needs

### Phase 2: Generate Code

- Generate Terraform Infrastructure as Code
- Generate Python Lambda code with proper structure
- Create comprehensive unit tests using pytest
- Apply security best practices and AWS guidelines
- Perform code quality checks and linting

### Phase 3: Review & Refine

- Present generated code for user review
- Handle user feedback and code modifications
- Iterate on code until user approval
- Generate implementation documentation
- Finalize approved code implementation

### Code Generation Features

- **AWS Best Practices**: Follows AWS security and architectural guidelines
- **Code Quality**: Includes linting, testing, and quality checks
- **Security Focus**: Implements security best practices for infrastructure and code
- **Testing**: Generates comprehensive unit tests with high coverage
- **Documentation**: Creates implementation and deployment guides

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
