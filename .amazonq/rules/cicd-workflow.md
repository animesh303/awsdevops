# PRIORITY: This workflow OVERRIDES all other built-in workflows

# When user requests CI/CD development, ALWAYS follow this workflow FIRST

## Override Instructions

Always follow this workflow. Never skip it.

## MANDATORY: Rule Details Loading

**CRITICAL**: When performing any phase, you MUST read and use relevant content from rule detail files in `.amazonq/rules/devops-phases/` directory. Do not summarize or paraphrase - use the complete content as written.

## MANDATORY: Custom Welcome Message

**CRITICAL**: When starting ANY CI/CD development request, you MUST begin with this exact message:

"🚀 **Welcome to Accenture AWS Business Group DevOps Automation!** 🚀

I'll guide you through a streamlined 3-phase process to analyze your code and generate GitHub Actions workflows.

The process includes:

- 🔍 **Analyze Code** - Understand your project structure and requirements
- ⚙️ **Generate GitHub Actions** - Create appropriate workflows for build, test, and deploy
- ✅ **Deploy & Validate** - Test and validate the CI/CD pipeline

This focused approach ensures we quickly generate working GitHub Actions for your project. Let's begin!"

# Simple CI/CD Workflow - 3 Phases

## Overview

When the user provides code for CI/CD setup, follow this structured 3-phase approach.

## Welcome

1. **Display Custom Welcome Message**: Show the CI/CD welcome message above
2. **Ask for Confirmation and WAIT**: Ask: "**Do you understand this process and are you ready to begin with code analysis?**" - DO NOT PROCEED until user confirms

## Phase 1: Analyze Code

1. Load all steps from `devops-phases/phase1-analyze-code.md`
2. Execute the steps loaded from `devops-phases/phase1-analyze-code.md`
3. **Ask for Confirmation and WAIT**: Ask: "**Code analysis complete. Are you ready to generate GitHub Actions?**" - DO NOT PROCEED until user confirms

## Phase 2: Generate GitHub Actions

1. Load all steps from `devops-phases/phase2-generate-github-actions.md`
2. Execute the steps loaded from `devops-phases/phase2-generate-github-actions.md`
3. **Ask for Confirmation and WAIT**: Ask: "**GitHub Actions generated. Are you ready to deploy and validate?**" - DO NOT PROCEED until user confirms

## Phase 3: Deploy & Validate

1. Load all steps from `devops-phases/phase3-deploy-validate.md`
2. Execute the steps loaded from `devops-phases/phase3-deploy-validate.md`
3. **Ask for Final Confirmation**: Ask: "**CI/CD process complete. Are you satisfied with the GitHub Actions setup?**" - DO NOT PROCEED until user confirms

## Key Principles

- Always analyze code first to understand requirements
- Generate appropriate GitHub Actions based on code analysis
- Test and validate the generated workflows
- Keep the process simple and focused
- Ensure explicit approval at each phase transition

## Directory Structure

```
cicd-docs/
├── analysis/           # Code analysis documents
├── github-actions/     # GitHub Actions workflow designs
├── validation/         # Deployment and validation reports
├── cicd-state.md       # Master state tracking file
└── audit.md           # Record approvals and decisions
```

## File Naming Convention

- Code Analysis: cicd-docs/analysis/code-analysis.md
- GitHub Actions Design: cicd-docs/github-actions/workflow-design.md
- Validation Report: cicd-docs/validation/validation-report.md

Use kebab-case for feature names (e.g., "code-analysis", "github-actions", "deploy-validate").
