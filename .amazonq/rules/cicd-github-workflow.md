# PRIORITY: Use this workflow to generate or regenerate GitHub Actions workflows for codebases

# When CICD workflow generation or regeneration is requested, ALWAYS follow this workflow FIRST

## Navigation

**Main Workflow**: This file (`cicd-github-workflow.mdc`)

**Phase Files**:

- `phase1-detect-plan.mdc` - Phase 1: Detect & Plan
- `phase2-generate-workflow.mdc` - Phase 2: Generate Workflows
- `phase3-review-confirm.mdc` - Phase 3: Review & Confirm
- `phase4-commit-push.mdc` - Phase 4: Commit & Push

**Supporting Documents**:

- `session-continuity.mdc` - Session management and resumption
- `workflow-common-issues.mdc` - Common issues and solutions
- `workflow-dependency-handling.mdc` - Dependency handling patterns
- `error-handling.mdc` - Error scenarios and responses
- `rollback-procedures.mdc` - Rollback and undo procedures
- `validation-checklist.mdc` - Comprehensive validation criteria
- `cicd-state.mdc` - State file template

**Standards Files**:

- `python-standards.mdc` - Python CI/CD patterns
- `terraform-standards.mdc` - Terraform CI/CD patterns
- `{code-type}-standards.mdc` - Language-specific patterns

**See Also**: `INDEX.mdc` for complete file index and navigation guide

## Override Instructions

Always follow this workflow when user mentions CICD GitHub workflow generation. Never skip it.

## MANDATORY: Rule Details Loading

**CRITICAL**: When performing any phase, you MUST read and use relevant content from rule detail files in `.amazonq/rules/cicd-phases/` directory. Do not summarize or paraphrase - use the complete content as written.

## MANDATORY: MCP Server Integration

**CRITICAL**: When performing CI/CD workflow generation, leverage available MCP servers to enhance capabilities:

### GitHub MCP Server Integration

- **Workflow Management**: Use `github-mcp-server` to check existing GitHub Actions workflows
- **Repository Analysis**: Analyze repository structure, branches, and settings via GitHub MCP
- **Workflow Deployment**: Create or update GitHub Actions workflows using MCP server
- **Workflow Execution**: Trigger workflow runs and check workflow status via MCP
- **Secrets Management**: Check GitHub secrets availability for CI/CD workflows

### AWS MCP Server Integration

- **Resource Validation**: Validate AWS resources referenced in workflows exist and are accessible
- **IAM Roles**: Verify IAM roles and permissions needed for CI/CD workflows
- **Environment Setup**: Check AWS environments and configurations via MCP
- **Deployment Validation**: Validate deployment targets and environments

### Docker MCP Server Integration

- **Container Operations**: Use `docker-mcp-server` for container build and push operations in workflows
- **Image Management**: Manage Docker images and registries via MCP
- **Container Validation**: Validate container configurations and dependencies

**Usage Pattern**: When generating CI/CD workflows, use MCP servers to validate GitHub repository settings, AWS resources, and Docker configurations before finalizing workflows.

## MANDATORY: Smart Context Loading for Resume

**CRITICAL**: When resuming at any phase, you MUST automatically load all relevant artifacts from previous phases:

### Context Loading by Phase:

- **Phase 1**: Load existing codebase structure, detect languages/environments, check for existing workflows, **load requirements files** (`.code-docs/requirements/*.md` or `.requirements/` directory), **load artifact mapping file** (`.code-docs/artifact-mappings.json` if exists)
- **Phase 2**: Load Phase 1 detection results + workflow plan + existing workflow files (if any) + **requirements files with dependency analysis** + **artifact mapping file** (`.code-docs/artifact-mappings.json` if exists)
- **Phase 3**: Load all detection results + generated workflow files + plan documents + existing workflows + **requirements and dependency mappings** + **artifact mapping file**
- **Phase 4**: Load all previous artifacts + review feedback + approval records

### Mandatory Loading Rules:

1. **Always read cicd-state.md first** to understand current phase (prefer `.cicd-docs/cicd-state.md`, fallback to `.amazonq/rules/cicd-phases/cicd-state.mdc`)
2. **Load incrementally** - each phase needs context from all previous phases
3. **Workflow files are special** - must read existing workflow files in `.github/workflows/` in addition to all artifacts
4. **Requirements files are CRITICAL** - must load requirements files to understand dependencies between code artifacts
5. **Artifact mapping file is PREFERRED** - must load `.code-docs/artifact-mappings.json` if it exists (generated during code generation Phase 2) to get exact artifact names and paths
6. **Provide context summary** - briefly tell user what artifacts were loaded
7. **Never assume** - always load the actual files, don't rely on memory

## MANDATORY: Requirements and Dependency Analysis

**CRITICAL**: When generating CICD workflows, you MUST:

1. **Load Requirements Files**:

   - Scan for requirements files in `.code-docs/requirements/` or `.requirements/` directories
   - Load all `*_requirements.md`, `*-analysis.md`, and `*-code-analysis.md` files
   - Extract dependency information between code artifacts (e.g., Terraform depends on Python Lambda code)

2. **Analyze Dependencies**:

   - Identify which code types depend on others (e.g., Terraform infrastructure depends on Python Lambda deployment package)
   - Map dependencies: `{code-type} → depends on → {other-code-type}`
   - Document build/deployment order requirements

3. **Handle Dependencies in Workflows**:
   - Ensure dependent code artifacts are built/deployed before dependent workflows
   - Use workflow dependencies (`workflow_run` triggers) or job dependencies (`needs:`) to enforce order
   - Download artifacts from upstream workflows when needed
   - Example: Terraform deployment must wait for Python Lambda package to be built and uploaded

## MANDATORY: Session Continuity and Re-generation

**CRITICAL**: When detecting an existing CICD workflow generation project, you MUST read and follow the session continuity instructions from `cicd-phases/session-continuity.mdc` before proceeding with any phase.

**Re-generation Support**: If the user explicitly requests to "regenerate", "re-generate", "refresh", or "update" workflows, you MUST:

1. **Remove existing CICD artifacts** (simplified approach):
   - Delete the entire `.cicd-docs/` directory (removes all state, plans, and audit logs)
   - Delete the entire `.github/workflows/` directory (removes all existing workflow files)
   - **Note**: This ensures a completely fresh start with no legacy artifacts
2. Start from Phase 1 (detect and plan) with a clean slate
3. Create new `.cicd-docs/` directory and initialize fresh state files as needed
4. Log the regeneration request in the new `.cicd-docs/audit.md` with timestamp

## MANDATORY: Custom Welcome Message

**CRITICAL**: When starting ANY CICD workflow generation request, you MUST begin with this exact message:

"🚀 **Welcome to AWS Business Group CICD Workflow Generation!** 🚀

I'll guide you through a streamlined 4-phase process to automatically generate and integrate context-aware CICD workflows for your project.

The process includes:

- 🔍 **Phase 1: Detect & Plan** – Scan repository for all code types (Python, Terraform, JavaScript, Java, Go, Docker, etc.) and plan single production deployment workflow
- 🏗️ **Phase 2: Generate Workflows** – Create single unified production GitHub Actions workflow with deployment pipeline:
  - **Production**: Deploy to production environment when changes are pushed to `main` branch
- ✅ **Phase 3: Review & Confirm** – Review workflows, scan steps, and finalize integration
- 🚀 **Phase 4: Commit & Push** – Commit and push workflow files to repository with explicit approval

This focused approach ensures your codebase is production-ready with automated single production deployment following AWS/Amazon code quality and security best practices. Let's begin!"

## Welcome

1. **Check for Re-generation Request**:
   - If user explicitly mentions "regenerate", "re-generate", "refresh", "update", or "recreate" workflows, treat as regeneration request
   - **Regeneration Request**:
     - Delete `.cicd-docs/` directory (removes all state, plans, audit logs)
     - Delete `.github/workflows/` directory (removes all existing workflow files)
     - Start completely fresh from Phase 1
   - After cleanup, log regeneration request in new `.cicd-docs/audit.md` with timestamp and reason
2. **Display Custom Welcome Message**: Show the CICD welcome message above
3. **Check for Existing Session**: Before proceeding, check for existing CICD workflow generation session by reading `.cicd-docs/cicd-state.md` (preferred) or `.amazonq/rules/cicd-phases/cicd-state.mdc` (legacy)
   - **If Regeneration Request**: Skip existing session check (folders already removed), proceed directly to new session
4. **If Existing Session Detected (and NOT regeneration)**: Follow session continuity instructions from `cicd-phases/session-continuity.mdc` and present "Welcome Back" prompt
5. **If New Session or Regeneration**: Proceed with initial welcome, mention that this is a fresh start (regeneration) or new session
6. **Log prompt with timestamp** - Record approval prompt in `.cicd-docs/audit.md` before asking
7. **Ask for Confirmation and WAIT**: Ask: "**Do you understand this process and are you ready to begin detection and planning?**" - DO NOT PROCEED until user confirms
8. **Log response with timestamp** - Record user response in `.cicd-docs/audit.md` after receiving it

# Custom CICD Workflow Generation Process (4-Phase Modular)

## Overview

Follow this 4-phase approach. For each phase, load and execute detailed steps from the corresponding `.amazonq/rules/cicd-phases/` file:

---

## Phase 1: Detect & Plan Workflows

1. **Load all steps from `cicd-phases/phase1-detect-plan.mdc`**
2. Execute steps to scan for code, identify dependencies, draft plan, and checkpoint user confirmation.
3. **Update plan checkboxes** - Mark completed steps [x] in plan document `.cicd-docs/detection-plan.md` (or `.cicd-docs/phase1-plan.md`) as work progresses
4. **Update cicd-state.md** - Update Phase 1 status and detected code types after completion
5. **Log prompt with timestamp** - Record approval prompt in `.cicd-docs/audit.md` before asking
6. **Ask for Confirmation and WAIT**: Ask: "Detection and planning complete. Proceed to generate single production workflow as planned?" - DO NOT PROCEED until user confirms
7. **Log response with timestamp** - Record user response in `.cicd-docs/audit.md` after receiving it
8. **MANDATORY**: Remind user to commit artifacts to git after phase completion

---

## Phase 2: Generate Workflow Files

1. **Load all steps from `cicd-phases/phase2-generate-workflow.mdc`**
2. Execute steps to render workflow YAML, match jobs to context, and checkpoint before review.
3. **Update plan checkboxes** - Mark completed steps [x] in plan document `.cicd-docs/workflow-generation-plan.md` (or `.cicd-docs/phase2-plan.md`) as work progresses
4. **Update cicd-state.md** - Update Phase 2 status and generated files list after completion
5. **Log prompt with timestamp** - Record approval prompt in `.cicd-docs/audit.md` before asking
6. **Ask for Confirmation and WAIT**: Ask: "Single production workflow generated. Are you ready to review and confirm?" - DO NOT PROCEED until user confirms
7. **Log response with timestamp** - Record user response in `.cicd-docs/audit.md` after receiving it
8. **MANDATORY**: Remind user to commit artifacts to git after phase completion

---

## Phase 3: Review & Confirm

1. **Load all steps from `cicd-phases/phase3-review-confirm.mdc`**
2. Execute steps to review generated workflows, present details, and checkpoint before finalization.
3. **Update plan checkboxes** - Mark completed steps [x] in plan document `.cicd-docs/review-notes.md` (or `.cicd-docs/phase3-notes.md`) as work progresses
4. **Update cicd-state.md** - Update Phase 3 status and review notes after completion
5. **Log prompt with timestamp** - Record approval prompt in `.cicd-docs/audit.md` before asking
6. **Ask for Final Confirmation**: Ask: "Single production CICD workflow complete. Do you approve the final workflow for integration?" - DO NOT PROCEED until user confirms
7. **Log response with timestamp** - Record user response in `.cicd-docs/audit.md` after receiving it
8. **MANDATORY**: Remind user to commit artifacts to git after phase completion

---

# Phase 4: Commit & Push

1. **Load all steps from `cicd-phases/phase4-commit-push.mdc`**
2. Execute steps to commit generated/updated workflow files and push to the repository, only after explicit user approval.
3. **Update plan checkboxes** - Mark completed steps [x] in plan document `.cicd-docs/review-notes.md` (or `.cicd-docs/phase3-notes.md`) as work progresses
4. **Update cicd-state.md** - Update Phase 4 status and mark overall workflow as complete
5. **Log prompt with timestamp** - Record approval prompt in `.cicd-docs/audit.md` before asking
6. **Ask for Confirmation and WAIT**: Ask: "Ready to commit and push the workflow changes to the repository?" - DO NOT PROCEED until user confirms
7. **Log response with timestamp** - Record user response in `.cicd-docs/audit.md` after receiving it

---

# Key Workflow Requirements

## Language-Agnostic Detection

- Automatically scan repository for ALL code types (Python, Terraform, JavaScript/TypeScript, Java, Go, Docker, Kubernetes, etc.)
- Detect code presence by file extensions and directory patterns
- Generate workflows ONLY for detected code types
- If existing workflows exist, analyze them and modify/remove as needed based on current codebase

## Single Production CI/CD Workflow Architecture

### Unified Single Workflow Architecture

Generate **one unified production workflow file** (`.github/workflows/ci-cd.yml`) that contains jobs for ALL detected code types:

**Single Production Workflow** (`.github/workflows/ci-cd.yml`):

- **Trigger**:
  - Runs on pushes to `main` branch only
  - Supports `workflow_dispatch` trigger for manual execution
- **Environment**: Single production environment (all deploy jobs use `environment: production`)
- **Structure**: Contains jobs for each code type sequenced by dependencies
- **Job Structure for Each Code Type**:
  - **CI Jobs** (run in parallel): lint, security scan, test
  - **Build Job** (runs after CI jobs): Build and package artifacts
  - **Deploy Job** (runs after build and upstream dependencies): Deploy to production
- **Dependency Handling**: Job dependencies (`needs:`) enforce execution order within the same workflow
- **Artifact Passing**: Artifacts are passed between jobs using GitHub Actions artifacts within the same workflow

**Workflow Structure:**

- Single workflow file contains all code types
- Jobs are sequenced by dependencies using `needs:` dependencies
- Code types with no dependencies run first
- Dependent code types wait for upstream deploy jobs to complete
- All deploy jobs use `environment: production`
- **Trigger Logic**: `main` branch push only (no other branch triggers)
- **Dependency Handling**: Job dependencies within the same workflow manage execution order

## Workflow Requirements

**CRITICAL**: All generated workflow files MUST be free of linting errors. Workflows must:

- Have valid YAML syntax
- Use correct GitHub Actions expression syntax (`${{ }}` for all functions)
- Have no missing required fields
- Have valid job dependencies and workflow triggers
- Pass GitHub Actions workflow validation

- All workflows must include:
  - CI/CD best practices (lint, test, scan, artifact upload, etc.)
  - Language-appropriate security scanning
  - Proper permissions and AWS credential configuration when needed
- Modular, extensible and production-grade workflows
- Minimal, clear confirmation at each phase
- Existing workflow management: modify existing workflows or remove obsolete ones

## Code Type Detection Patterns

The system scans for common code types using file patterns and directory structures:

- **Python**: `.py` files, `requirements.txt`, `setup.py`, `pyproject.toml`, `Pipfile`
- **Terraform**: `.tf` files, `.tfvars` files, `terraform/` directories
- **JavaScript/TypeScript**: `.js`, `.jsx`, `.ts`, `.tsx` files, `package.json`, `node_modules/`
- **Java**: `.java` files, `pom.xml`, `build.gradle`, `Maven`, `Gradle` directories
- **Go**: `.go` files, `go.mod`, `go.sum`
- **Docker**: `Dockerfile`, `docker-compose.yml`, `.dockerignore`
- **Kubernetes**: `.yaml`/`.yml` files in `k8s/`, `kubernetes/`, `manifests/` directories
- **CloudFormation**: `.yaml`/`.yml` files with CloudFormation templates, `cfn/` directories
- **CDK**: `cdk.json`, `cdk/` directories, TypeScript/Python/Java CDK code

## Language-Specific CI/CD Standards

**CRITICAL**: Language-specific guidance for CI/CD workflows is stored in separate standards files within `.amazonq/rules/cicd-phases/`:

- `python-standards.mdc` - Python CI/CD workflow patterns and standards
- `terraform-standards.mdc` - Terraform CI/CD workflow patterns and standards
- `javascript-standards.mdc` - JavaScript/TypeScript CI/CD workflow patterns and standards
- `java-standards.mdc` - Java CI/CD workflow patterns and standards
- `go-standards.mdc` - Go CI/CD workflow patterns and standards
- `docker-standards.mdc` - Docker CI/CD workflow patterns and standards
- `kubernetes-standards.mdc` - Kubernetes CI/CD workflow patterns and standards
- `cloudformation-standards.mdc` - CloudFormation CI/CD workflow patterns and standards
- `cdk-standards.mdc` - CDK CI/CD workflow patterns and standards

When generating workflows for a detected code type, you MUST:

1. Read the corresponding standards file from `.amazonq/rules/cicd-phases/{code-type}-standards.mdc`
2. Apply the complete content from that file when generating the workflow
3. Do not summarize or paraphrase - use the complete content as written

If a standards file does not exist for a detected code type, create it following the pattern of existing standards files and include language-appropriate CI/CD patterns.

## CRITICAL: Plan-Level Checkbox Enforcement

### MANDATORY RULES FOR PLAN EXECUTION

1. **NEVER complete any work without updating plan checkboxes**
2. **IMMEDIATELY after completing ANY step described in a plan file, mark that step [x]**
3. **This must happen in the SAME interaction where the work is completed**
4. **Example**: When generating workflow files, mark "Generate python-ci.yml workflow" as [x] in the workflow generation plan
5. **NO EXCEPTIONS**: Every plan step completion MUST be tracked with checkbox updates

### Two-Level Checkbox Tracking System

The workflow uses a two-level checkbox tracking system:

#### 1. Plan-Level Execution Tracking (Plan Files)

- **Purpose**: Track detailed execution progress within each phase
- **Location**: Individual plan files in `.cicd-docs/` directory (preferred) or `.amazonq/rules/cicd-phases/` (legacy fallback)
- **Plan Documents**:
  - **Phase 1**: `.cicd-docs/detection-plan.md` (or `.cicd-docs/phase1-plan.md`)
  - **Phase 2**: `.cicd-docs/workflow-generation-plan.md` (or `.cicd-docs/phase2-plan.md`)
  - **Phase 3**: `.cicd-docs/review-notes.md` (or `.cicd-docs/phase3-notes.md`)
- **When to Update**: Mark steps [x] as you complete the specific work described in that step
- **MANDATORY**: Update immediately after completing work, never skip this step

#### 2. Phase-Level Progress Tracking (cicd-state.md)

- **Purpose**: Track overall workflow progress across phases
- **Location**: `.cicd-docs/cicd-state.md` (preferred) or `.amazonq/rules/cicd-phases/cicd-state.mdc` (legacy fallback)
- **When to Update**: Mark phases [x] only when the entire phase is complete and approved by user

### Mandatory Update Rules

- **Plan Files**: Update checkboxes [x] immediately after completing each step's work
- **cicd-state.md**: Update phase checkboxes [x] only after user approval to proceed
- **Current Status**: Always update the "Current Status" section in cicd-state.md after any progress
- **Same Interaction**: All progress updates must happen in the SAME interaction where work is completed
- **Never Skip**: Never end an interaction without updating progress tracking

## Prompts Logging Requirements

- **MANDATORY**: Log every approval prompt with timestamp before asking the user
- **MANDATORY**: Record every user response with timestamp after receiving it
- Use ISO 8601 format for timestamps (YYYY-MM-DDTHH:MM:SSZ)
- Include phase context and approval status for each entry
- Maintain chronological order of all interactions
- Use the following format for each entry:

```markdown
## Phase X: [Phase Name]

**Timestamp**: 2025-01-28T14:32:15Z
**Prompt**: "[Exact prompt text asked to user]"
**Response**: "[User's exact response]"
**Status**: [Approved/Rejected/Pending]
**Context**: [Additional context if needed]

---
```

# Directory/File Naming

## Workflow Files

**Single Production Workflow File**:

- `.github/workflows/ci-cd.yml` - Single unified production workflow containing all code types
  - Triggers on `main` branch push only
  - Contains jobs for all detected code types sequenced by dependencies
  - All deploy jobs use `environment: production`

Use kebab-case for workflow file name: `ci-cd.yml`

## Directory Structure

```
.cicd-docs/                    # Preferred location for project-scoped CICD artifacts
├── cicd-state.md              # Master state tracking file with phase checkboxes
└── audit.md                   # Record approvals from users with timestamp for each CICD phase

.github/
└── workflows/                 # Generated GitHub Actions workflow files
    └── ci-cd.yml                  # Single production workflow (triggered by main branch)

.amazonq/rules/cicd-phases/    # CI/CD workflow generation rules
├── cicd-state.mdc              # Legacy state file (only if .cicd-docs/ doesn't exist)
├── {code-type}-standards.mdc   # Language-specific CI/CD standards (one per code type)
└── [phase files]              # Phase execution instructions
```

# Principles

- **Language-Agnostic Detection**: Scan for ALL code types in the repository, not just Python/Terraform
- **Simplified Re-generation**: For regeneration requests, simply delete `.cicd-docs/` and `.github/workflows/` directories before starting - ensures completely clean start
- **Existing Workflow Management**: For new generation (not regeneration), existing workflows in `.github/workflows/` will be replaced by the newly generated single production workflow
- Always generate ONLY for detected code types
- **Single Production Workflow**: Generate one unified workflow file containing all code types:
  - `ci-cd.yml` - Single production workflow (triggers on `main` branch push only)
  - Contains jobs for all detected code types sequenced by dependencies
  - All deploy jobs use `environment: production`
- **No Orchestrator Workflows**: Not needed for single workflow architecture - dependencies managed via job `needs:` within the same workflow
- **No Multi-Environment Workflows**: Single production environment only - no dev/test/prod separation
- **Branch-Based Deployment Trigger**:
  - Main branch push → Single production workflow (direct push trigger)
  - No other branch triggers
- **Language-Specific Standards**: Read and apply complete content from `{code-type}-standards.mdc` files in `cicd-phases/` directory
- Minimal, modular checkpoints across all phases
- **MANDATORY**: Use the two-level checkbox tracking system (plan files + cicd-state.md)
- **MANDATORY**: Update plan file checkboxes [x] immediately after completing each step's work
- **MANDATORY**: Update cicd-state.md phase checkboxes [x] only after user approval to proceed
- **MANDATORY**: Update the "Current Status" section in cicd-state.md after any progress
- **MANDATORY**: Log all prompts and responses with timestamps in audit.md
- **MANDATORY**: Remind user to commit artifacts to git after every phase completion
- Ensure explicit approval at each phase transition
- Load context incrementally - each phase needs context from all previous phases

# Session Continuity (Summary)

- Always follow `cicd-phases/session-continuity.mdc` for detecting/resuming sessions
- Prefer storing state and approvals under project docs: `.cicd-docs/cicd-state.md` and `.cicd-docs/audit.md` (fallback to legacy `.amazonq/rules/cicd-phases/cicd-state.mdc` if needed)
- Always read cicd-state.md first to understand current phase before proceeding
- Provide context summary when resuming sessions
