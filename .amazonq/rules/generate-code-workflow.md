# PRIORITY: This workflow OVERRIDES all other built-in workflows when coding of requirement from JIRA is requested

# When user requests to implement requirements from JIRA or coding of requirements from JIRA, ALWAYS follow this workflow FIRST

## Override Instructions

Always follow this workflow when user mentions implementing requirements from JIRA or coding requirements from JIRA. Never skip it.

## MANDATORY: Rule Details Loading

**CRITICAL**: When performing any phase, you MUST read and use relevant content from rule detail files in `.amazonq/rules/code-phases/` directory. Do not summarize or paraphrase - use the complete content as written.

## MANDATORY: Session Continuity

**CRITICAL**: When detecting an existing code generation project, you MUST:

1. **Read code-state.md first** - Always read `.code-docs/code-state.md` to understand current phase
2. **Follow session continuity instructions** - Read and follow the session continuity instructions from `code-phases/session-continuity.md`
3. **Load Previous Phase Artifacts** - Before resuming any phase, automatically read all relevant artifacts from previous phases according to Smart Context Loading rules
4. **Provide Context Summary** - After loading artifacts, provide brief summary of what was loaded for user awareness
5. **Present Continuity Options** - ALWAYS present session continuity options directly in the chat session using the template from session-continuity.md

## MANDATORY: Smart Context Loading for Resume

**CRITICAL**: When resuming at any phase, you MUST automatically load all relevant artifacts from previous phases:

### Context Loading by Phase:

- **Phase 1**: Load existing requirements artifacts if available (.code-docs/requirements/available-requirements.md, requirements-selection.md)
- **Phase 2**: Load requirements + selected requirements document + analysis from Phase 1
- **Phase 3**: Load all requirements artifacts + generated code files + quality reports from Phases 1-2
- **Phase 4**: Load ALL artifacts + existing code files from workspace + audit logs

### Mandatory Loading Rules:

1. **Always read code-state.md first** to understand current phase
2. **Load incrementally** - each phase needs context from all previous phases
3. **Code phases are special** - must read existing code files in addition to all artifacts
4. **Provide context summary** - briefly tell user what artifacts were loaded
5. **Never assume** - always load the actual files, don't rely on memory

## MANDATORY: Custom Welcome Message

**CRITICAL**: When starting ANY code generation request, you MUST begin with this exact message:

"🚀 **Welcome to AWS Business Group Code Generation!** 🚀

I'll guide you through a streamlined workflow to implement your requirements and generate production-ready code.

The process includes:

- 📋 **Select Requirements** - Choose from available requirements documents and select IAC tool/runtime
- 🏗️ **Generate Code** - Create Infrastructure as Code and application code with tests
- ✅ **Review & Refine** - Review, test, and refine the generated code
- 🚀 **Commit & Push** - (Optional) Commit and push changes to version control

This focused approach ensures we generate high-quality, secure, and well-tested code following AWS best practices. Let's begin!"

# Code Generation Workflow - 4 Phases

## Overview

When the user requests to implement requirements or generate code, follow this structured 4-phase approach.

## Welcome

1. **Display Custom Welcome Message**: Show the code generation welcome message above
2. **Ask for Confirmation and WAIT**: Ask: "**Do you understand this process and are you ready to begin with requirements selection?**" - DO NOT PROCEED until user confirms

## Phase 1: Select Requirements

1. **Load Context**: If resuming, read code-state.md and load any existing requirements artifacts
2. Load all steps from `code-phases/phase1-select-requirements.md`
3. Execute the steps loaded from `code-phases/phase1-select-requirements.md`
4. **Update Progress**: Update code-state.md with Phase 1 progress after completion
5. **Log Approval**: Before asking for confirmation, log the prompt in audit.md with timestamp
6. **Ask for Confirmation and WAIT**: Ask: "**Requirements selected. Are you ready to generate code?**" - DO NOT PROCEED until user confirms
7. **Log Response**: After receiving confirmation, log user response with timestamp in audit.md
8. **Update Phase Status**: Mark Phase 1 complete in code-state.md
9. **Remind Git Commit**: Remind user to commit artifacts to git

## Phase 2: Generate Code

1. **Load Context**: Load requirements + selected requirements document + analysis from Phase 1
2. Load all steps from `code-phases/phase2-generate-code.md`
3. Execute the steps loaded from `code-phases/phase2-generate-code.md`
4. **Update Progress**: Update code-state.md with Phase 2 progress after completion
5. **Log Approval**: Before asking for confirmation, log the prompt in audit.md with timestamp
6. **Ask for Confirmation and WAIT**: Ask: "**Code generated. Are you ready to review and refine?**" - DO NOT PROCEED until user confirms
7. **Log Response**: After receiving confirmation, log user response with timestamp in audit.md
8. **Update Phase Status**: Mark Phase 2 complete in code-state.md
9. **Remind Git Commit**: Remind user to commit artifacts to git

## Phase 3: Review & Refine

1. **Load Context**: Load all requirements artifacts + generated code files + quality reports from Phases 1-2
2. Load all steps from `code-phases/phase3-review-refine.md`
3. Execute the steps loaded from `code-phases/phase3-review-refine.md`
4. **Update Progress**: Update code-state.md with Phase 3 progress after completion
5. **Log Approval**: Before asking for confirmation, log the prompt in audit.md with timestamp
6. **Ask for Final Confirmation**: Ask: "**Code generation complete. Are you satisfied with the final implementation?**" - DO NOT PROCEED until user confirms
7. **Log Response**: After receiving confirmation, log user response with timestamp in audit.md
8. **Update Phase Status**: Mark Phase 3 complete in code-state.md
9. **Remind Git Commit**: Remind user to commit artifacts to git

## Phase 4: Commit & Push

1. **Load Context**: Load all artifacts + existing code files from workspace + audit logs
2. Load all steps from `code-phases/phase4-commit-push.md`
3. **Log Approval**: Before asking for confirmation, log the prompt in audit.md with timestamp
4. Ask the user: "Do you want me to commit and push the generated code changes now?"
5. WAIT for explicit approval, then execute commit and push steps. Do not proceed without approval.
6. **Log Response**: After receiving confirmation, log user response with timestamp in audit.md
7. **Update Progress**: Update code-state.md with Phase 4 completion status

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
- **MANDATORY** after every phase remind user to commit artifacts to git

## CRITICAL: Progress Tracking System

### Two-Level Progress Tracking System

The workflow uses a two-level progress tracking system:

#### 1. Plan-Level Execution Tracking (Plan Files - if they exist)

- **Purpose**: Track detailed execution progress within each phase
- **Location**: Individual plan files (if created during phases)
- **When to Update**: Mark steps [x] as you complete the specific work described in that step
- **MANDATORY**: Update immediately after completing work, never skip this step

#### 2. Phase-Level Progress Tracking (code-state.md)

- **Purpose**: Track overall workflow progress across phases
- **Location**: `.code-docs/code-state.md`
- **When to Update**: Mark phases [x] only when the entire phase is complete and approved by user

### Mandatory Update Rules

- **Plan Files**: Update checkboxes [x] immediately after completing each step's work (if plan files exist)
- **code-state.md**: Update phase status and "Current Status" section after any progress
- **Same Interaction**: All progress updates must happen in the SAME interaction where work is completed
- **Never Skip**: Never end an interaction without updating progress tracking

## Prompts Logging Requirements

- **MANDATORY**: Log every approval prompt with timestamp before asking the user
- **MANDATORY**: Record every user response with timestamp after receiving it
- Use ISO 8601 format for timestamps (YYYY-MM-DDTHH:MM:SSZ)
- Include phase context and approval status for each entry
- Maintain chronological order of all interactions
- Log to `.code-docs/audit.md` using the following format:

```markdown
## Phase X: [Phase Name]

**Timestamp**: 2025-01-28T14:32:15Z
**Prompt**: "[Exact prompt text asked to user]"
**Response**: "[User's exact response]"
**Status**: [Approved/Rejected/Pending]
**Context**: [Additional context if needed]

---
```

## Audit Logging Requirements

- **MANDATORY**: All phase transitions must be logged in `.code-docs/audit.md`
- **MANDATORY**: All user approvals must be logged with timestamps
- **MANDATORY**: All important decisions must be logged
- Use ISO 8601 format for timestamps (YYYY-MM-DDTHH:MM:SSZ)
- Maintain chronological order
- Include phase context, decision, and approval status
- Log file structure: `.code-docs/audit.md`

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
└── {iac-tool}/          # IAC code by tool (terraform, cdk, cloudformation, pulumi, etc.)

src/
└── {runtime-type}-{feature-name}/  # Application code by runtime/type (lambda-python, lambda-nodejs, container-{lang}, etc.)

tests/
└── {feature-name}/      # Unit tests by feature
```

**Note**: Specific IAC tool and application runtime/language are determined in Phase 1 based on requirements analysis.

## File Naming Convention

- Requirements: .code-docs/requirements/{TICKET-NUMBER}\_requirements.md
- IAC Code: iac/{iac-tool}/ (all files in single folder, tool-specific naming)
  - Tool-specific conventions are defined in `code-phases/{iac-tool}-standards.md` (e.g., terraform-standards.md)
  - Examples:
    - Terraform: {feature-name}-main.tf, {feature-name}-variables.tf, {feature-name}-output.tf
    - CDK: {feature-name}-stack.ts, {feature-name}-construct.ts
    - CloudFormation: {feature-name}-template.yaml
- Application Code: src/{runtime-type}-{feature-name}/
  - Runtime-specific conventions are defined in `code-phases/{language}-standards.md` (e.g., python-standards.md)
  - Runtime to language mapping: Extract language name from runtime type (e.g., `lambda-python` → `python`, `lambda-nodejs` → `nodejs`, `container-python` → `python`, `lambda-java` → `java`)
  - Examples:
    - Lambda Python: src/lambda-python-{feature-name}/ → uses python-standards.md
    - Lambda Node.js: src/lambda-nodejs-{feature-name}/ → uses nodejs-standards.md
    - Container Python: src/container-python-{feature-name}/ → uses python-standards.md
- Tests: tests/{feature-name}/

**Note**: IAC tool and application runtime/language are selected in Phase 1. Use kebab-case for feature names (e.g., "select-requirements", "generate-code", "review-refine").
