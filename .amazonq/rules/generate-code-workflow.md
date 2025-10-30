# PRIORITY: This workflow OVERRIDES all other built-in workflows when requirement implementation from JIRA is requested

# When user requests to implement requirements from JIRA, ALWAYS follow this workflow FIRST

## Override Instructions

Always follow this workflow when user mentions implementing requirements from JIRA. Never skip it.

## MANDATORY: Rule Details Loading

**CRITICAL**: When performing any phase, you MUST read and use relevant content from rule detail files in `.amazonq/rules/code-phases/` directory. Do not summarize or paraphrase - use the complete content as written.

## MANDATORY: Session Continuity

**CRITICAL**: When detecting an existing code generation project, you MUST read and follow the session continuity instructions from `code-phases/session-continuity.md` before proceeding with any phase.

## MANDATORY: Custom Welcome Message

**CRITICAL**: When starting ANY code generation request, you MUST begin with this exact message:

"🚀 **Welcome to AWS Business Group Code Generation!** 🚀

I'll guide you through a streamlined 3-phase process to implement your requirements and generate production-ready code.

The process includes:

- 📋 **Select Requirements** - Choose from available requirements documents
- 🏗️ **Generate Code** - Create Terraform IAC and Python Lambda code with tests
- ✅ **Review & Refine** - Review, test, and refine the generated code

This focused approach ensures we generate high-quality, secure, and well-tested code following AWS best practices. Let's begin!"

# Code Generation Workflow - 3 Phases

## Overview

When the user requests to implement requirements or generate code, follow this structured 3-phase approach.

## Welcome

1. **Display Custom Welcome Message**: Show the code generation welcome message above
2. **Ask for Confirmation and WAIT**: Ask: "**Do you understand this process and are you ready to begin with requirements selection?**" - DO NOT PROCEED until user confirms

## Phase 1: Select Requirements

1. Load all steps from `code-phases/phase1-select-requirements.md`
2. Execute the steps loaded from `code-phases/phase1-select-requirements.md`
3. **Ask for Confirmation and WAIT**: Ask: "**Requirements selected. Are you ready to generate code?**" - DO NOT PROCEED until user confirms

## Phase 2: Generate Code

1. Load all steps from `code-phases/phase2-generate-code.md`
2. Execute the steps loaded from `code-phases/phase2-generate-code.md`
3. **Ask for Confirmation and WAIT**: Ask: "**Code generated. Are you ready to review and refine?**" - DO NOT PROCEED until user confirms

## Phase 3: Review & Refine

1. Load all steps from `code-phases/phase3-review-refine.md`
2. Execute the steps loaded from `code-phases/phase3-review-refine.md`
3. **Ask for Final Confirmation**: Ask: "**Code generation complete. Are you satisfied with the final implementation?**" - DO NOT PROCEED until user confirms

## Phase 4: Commit & Push (Optional)

1. Load all steps from `code-phases/phase4-commit-push.md`
2. Ask the user: "Do you want me to commit and push the generated code changes now, or skip this step?"
3. If user selects commit: execute commit/push steps. If user selects skip: end the workflow without git operations.

## Key Principles

- Use `.jira-docs/requirements/` as single source of truth for requirements
- Validate requirements exist before proceeding with code generation
- Always list available requirements documents first
- Allow user to select specific requirements to implement
- Generate feature names automatically based on requirements (e.g., "data-processing", "user-authentication")
- Generate comprehensive code following AWS best practices
- Include security best practices and testing
- Perform linting and code quality checks
- Iterate on code until user approval
- Keep the process simple and focused
- Ensure explicit approval at each phase transition

## Feature Name Generation

Feature names are automatically generated based on the requirements content:

- Extract key functionality from requirements
- Convert to kebab-case (e.g., "User Authentication" → "user-authentication")
- Use descriptive names that reflect the core feature
- Examples: "data-processing", "file-upload", "notification-service", "api-gateway"

## Directory Structure

```
.code-docs/
├── requirements/         # Selected requirements documents
├── code-state.md        # Master state tracking file
└── audit.md             # Record approvals and decisions

iac/
└── terraform/           # All Terraform IAC code (single folder)

src/
└── lambda-{feature-name}/  # Python Lambda code by feature

tests/
└── {feature-name}/      # Unit tests by feature
```

## File Naming Convention

- Requirements: .code-docs/requirements/{TICKET-NUMBER}\_requirements.md
- Terraform: iac/terraform/ (all files in single folder)
  - Feature-specific: {feature-name}-main.tf, {feature-name}-variables.tf, {feature-name}-output.tf, {feature-name}-local.tf
  - Shared: shared-variables.tf, shared-outputs.tf, versions.tf
- Python: src/lambda-{feature-name}/
- Tests: tests/{feature-name}/

Use kebab-case for feature names (e.g., "select-requirements", "generate-code", "review-refine").
