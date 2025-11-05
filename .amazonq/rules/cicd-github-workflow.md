# PRIORITY: Use this workflow to generate or regenerate GitHub Actions workflows for codebases

# When CICD workflow generation or regeneration is requested, ALWAYS follow this workflow FIRST

## Override Instructions

Always follow this workflow when user mentions CICD GitHub workflow generation. Never skip it.

## MANDATORY: Rule Details Loading

**CRITICAL**: When performing any phase, you MUST read and use relevant content from rule detail files in `.amazonq/rules/cicd-phases/` directory. Do not summarize or paraphrase - use the complete content as written.

## MANDATORY: Smart Context Loading for Resume

**CRITICAL**: When resuming at any phase, you MUST automatically load all relevant artifacts from previous phases:

### Context Loading by Phase:

- **Phase 1**: Load existing codebase structure, detect languages/environments, check for existing workflows, **load requirements files** (`.code-docs/requirements/*.md` or `.requirements/` directory)
- **Phase 2**: Load Phase 1 detection results + workflow plan + existing workflow files (if any) + **requirements files with dependency analysis**
- **Phase 3**: Load all detection results + generated workflow files + plan documents + existing workflows + **requirements and dependency mappings**
- **Phase 4**: Load all previous artifacts + review feedback + approval records

### Mandatory Loading Rules:

1. **Always read cicd-state.md first** to understand current phase (prefer `.cicd-docs/cicd-state.md`, fallback to `.amazonq/rules/cicd-phases/cicd-state.md`)
2. **Load incrementally** - each phase needs context from all previous phases
3. **Workflow files are special** - must read existing workflow files in `.github/workflows/` in addition to all artifacts
4. **Requirements files are CRITICAL** - must load requirements files to understand dependencies between code artifacts
5. **Provide context summary** - briefly tell user what artifacts were loaded
6. **Never assume** - always load the actual files, don't rely on memory

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

**CRITICAL**: When detecting an existing CICD workflow generation project, you MUST read and follow the session continuity instructions from `cicd-phases/session-continuity.md` before proceeding with any phase.

**Re-generation Support**: If the user explicitly requests to "regenerate", "re-generate", "refresh", or "update" workflows, you MUST:

1. Create a new session (reset state files or create new session)
2. Start from Phase 1 (detect and plan) regardless of existing session state
3. Allow removal of previous workflows if they don't match current codebase
4. Log the regeneration request in audit.md with timestamp

## MANDATORY: Custom Welcome Message

**CRITICAL**: When starting ANY CICD workflow generation request, you MUST begin with this exact message:

"🚀 **Welcome to AWS Business Group CICD Workflow Generation!** 🚀

I'll guide you through a streamlined 4-phase process to automatically generate and integrate context-aware CICD workflows for your project.

The process includes:

- 🔍 **Phase 1: Detect & Plan** – Scan repository for all code types (Python, Terraform, JavaScript, Java, Go, Docker, etc.) and plan multi-environment deployment workflows
- 🏗️ **Phase 2: Generate Workflows** – Create modular, multi-environment GitHub Actions with deployment pipelines:
  - **Development**: Deploy to dev environment when changes are pushed to `develop` branch
  - **Test**: Deploy to test environment when changes are pushed to `main` branch
  - **Production**: Automatically deploy to prod environment after successful test deployment completion
- ✅ **Phase 3: Review & Confirm** – Review workflows, scan steps, and finalize integration
- 🚀 **Phase 4: Commit & Push** – Commit and push workflow files to repository with explicit approval

This focused approach ensures your codebase is production-ready with automated multi-environment deployments following AWS/Amazon code quality and security best practices. Let's begin!"

## Welcome

1. **Check for Re-generation Request**:
   - If user explicitly mentions "regenerate", "re-generate", "refresh", "update", or "recreate" workflows, treat as regeneration request
   - **Regeneration Request**: Create new session, reset/archive existing state, start fresh from Phase 1
   - Log regeneration request in `.cicd-docs/audit.md` with timestamp and reason
2. **Display Custom Welcome Message**: Show the CICD welcome message above
3. **Check for Existing Session**: Before proceeding, check for existing CICD workflow generation session by reading `.cicd-docs/cicd-state.md` (preferred) or `.amazonq/rules/cicd-phases/cicd-state.md` (legacy)
   - **If Regeneration Request**: Skip existing session check, proceed directly to new session
4. **If Existing Session Detected (and NOT regeneration)**: Follow session continuity instructions from `cicd-phases/session-continuity.md` and present "Welcome Back" prompt
5. **If New Session or Regeneration**: Proceed with initial welcome, mention that previous workflows may be removed if they don't match current codebase
6. **Log prompt with timestamp** - Record approval prompt in `.cicd-docs/audit.md` before asking
7. **Ask for Confirmation and WAIT**: Ask: "**Do you understand this process and are you ready to begin detection and planning?**" - DO NOT PROCEED until user confirms
8. **Log response with timestamp** - Record user response in `.cicd-docs/audit.md` after receiving it

# Custom CICD Workflow Generation Process (4-Phase Modular)

## Overview

Follow this 4-phase approach. For each phase, load and execute detailed steps from the corresponding `.amazonq/rules/cicd-phases/` file:

---

## Phase 1: Detect & Plan Workflows

1. **Load all steps from `cicd-phases/phase1-detect-plan.md`**
2. Execute steps to scan for code, identify environments, draft plan, and checkpoint user confirmation.
3. **Update plan checkboxes** - Mark completed steps [x] in any plan document as work progresses
4. **Update cicd-state.md** - Update Phase 1 status and detected environments after completion
5. **Log prompt with timestamp** - Record approval prompt in `.cicd-docs/audit.md` before asking
6. **Ask for Confirmation and WAIT**: Ask: "Detection and planning complete. Are you ready to generate workflows?" - DO NOT PROCEED until user confirms
7. **Log response with timestamp** - Record user response in `.cicd-docs/audit.md` after receiving it
8. **MANDATORY**: Remind user to commit artifacts to git after phase completion

---

## Phase 2: Generate Workflow Files

1. **Load all steps from `cicd-phases/phase2-generate-workflow.md`**
2. Execute steps to render workflow YAML, match jobs to context, and checkpoint before review.
3. **Update plan checkboxes** - Mark completed steps [x] in any plan document as work progresses
4. **Update cicd-state.md** - Update Phase 2 status and generated files list after completion
5. **Log prompt with timestamp** - Record approval prompt in `.cicd-docs/audit.md` before asking
6. **Ask for Confirmation and WAIT**: Ask: "Workflows generated. Are you ready to review and confirm?" - DO NOT PROCEED until user confirms
7. **Log response with timestamp** - Record user response in `.cicd-docs/audit.md` after receiving it
8. **MANDATORY**: Remind user to commit artifacts to git after phase completion

---

## Phase 3: Review & Confirm

1. **Load all steps from `cicd-phases/phase3-review-confirm.md`**
2. Execute steps to review generated workflows, present details, and checkpoint before finalization.
3. **Update plan checkboxes** - Mark completed steps [x] in any plan document as work progresses
4. **Update cicd-state.md** - Update Phase 3 status and review notes after completion
5. **Log prompt with timestamp** - Record approval prompt in `.cicd-docs/audit.md` before asking
6. **Ask for Final Confirmation**: Ask: "CICD setup complete. Do you approve the final workflows for integration?" - DO NOT PROCEED until user confirms
7. **Log response with timestamp** - Record user response in `.cicd-docs/audit.md` after receiving it
8. **MANDATORY**: Remind user to commit artifacts to git after phase completion

---

# Phase 4: Commit & Push

1. **Load all steps from `cicd-phases/phase4-commit-push.md`**
2. Execute steps to commit generated/updated workflow files and push to the repository, only after explicit user approval.
3. **Update plan checkboxes** - Mark completed steps [x] in any plan document as work progresses
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

## Environment-Specific CI/CD Workflow Architecture

For each detected code type, generate **three separate workflow files**, one per environment:

**Deploy to Dev Workflow** (`.github/workflows/{code-type}-dev.yml`):

- **Trigger**: Runs ONLY on pushes to `develop` branch
- **CI Jobs**: lint, test, security scan, artifact generation
  - Runs as separate parallel jobs where possible
  - Uploads build artifacts
- **Deploy to Dev Job**:
  - **Requires**: Successful completion of all CI jobs
  - Deploys to Development environment
  - Uses GitHub `environment: dev` for secrets and protection rules

**Deploy to Test Workflow** (`.github/workflows/{code-type}-test.yml`):

- **Trigger**: Runs on pushes to `main` branch
- **CI Jobs**: lint, test, security scan, artifact generation
  - Runs as separate parallel jobs where possible
  - Uploads build artifacts
- **Deploy to Test Job**:
  - **Requires**: Successful completion of all CI jobs
  - Deploys to Test environment
  - Uses GitHub `environment: test` for secrets and protection rules

**Deploy to Prod Workflow** (`.github/workflows/{code-type}-prd.yml`):

- **Trigger**: `workflow_run` on successful completion of `{code-type}-test.yml` workflow
  - **Branch Requirement**: MUST only trigger when test workflow ran on `main` branch
  - Uses `branches: [main]` filter in `workflow_run` trigger
- **CI Jobs**: lint, test, security scan, artifact generation
  - Runs as part of the workflow
  - Uploads build artifacts
- **Deploy to Prod Job**:
  - **Requires**: Successful completion of all CI jobs
  - Deploys to Production environment
  - Uses GitHub `environment: prod` with protection rules/approvals
  - Protected with GitHub environment protection rules

**Workflow Structure:**

- Each environment has its own workflow file
- Each workflow contains CI jobs + deployment job for that environment
- Branch-based triggers: `develop` branch for dev (push trigger), `main` branch for test (push trigger), prod (workflow_run trigger after successful test)

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

- `python-standards.md` - Python CI/CD workflow patterns and standards
- `terraform-standards.md` - Terraform CI/CD workflow patterns and standards
- `javascript-standards.md` - JavaScript/TypeScript CI/CD workflow patterns and standards
- `java-standards.md` - Java CI/CD workflow patterns and standards
- `go-standards.md` - Go CI/CD workflow patterns and standards
- `docker-standards.md` - Docker CI/CD workflow patterns and standards
- `kubernetes-standards.md` - Kubernetes CI/CD workflow patterns and standards
- `cloudformation-standards.md` - CloudFormation CI/CD workflow patterns and standards
- `cdk-standards.md` - CDK CI/CD workflow patterns and standards

When generating workflows for a detected code type, you MUST:

1. Read the corresponding standards file from `.amazonq/rules/cicd-phases/{code-type}-standards.md`
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
- **Location**: Individual plan files (detection-plan.md, workflow-generation-plan.md, etc.)
- **When to Update**: Mark steps [x] as you complete the specific work described in that step
- **MANDATORY**: Update immediately after completing work, never skip this step

#### 2. Phase-Level Progress Tracking (cicd-state.md)

- **Purpose**: Track overall workflow progress across phases
- **Location**: `.cicd-docs/cicd-state.md` (preferred) or `.amazonq/rules/cicd-phases/cicd-state.md` (legacy fallback)
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

Workflow files follow the pattern: `{code-type}-{environment}.yml`

For each detected code type, three environment-specific workflow files (unified CI + CD):

- `.github/workflows/{code-type}-dev.yml` - CI + Deploy to dev (triggers on `develop` branch push)
- `.github/workflows/{code-type}-test.yml` - CI + Deploy to test (triggers on `main` branch push)
- `.github/workflows/{code-type}-prd.yml` - CI + Deploy to prod (triggers via workflow_run after successful test completion)

Use kebab-case, descriptive file names based on detected code types

## Directory Structure

```
.cicd-docs/                    # Preferred location for project-scoped CICD artifacts
├── cicd-state.md              # Master state tracking file with phase checkboxes
└── audit.md                   # Record approvals from users with timestamp for each CICD phase

.github/
└── workflows/                 # Generated GitHub Actions workflow files
    ├── {code-type}-dev.yml         # Dev environment workflow (CI + Deploy to Dev)
    ├── {code-type}-test.yml        # Test environment workflow (CI + Deploy to Test)
    └── {code-type}-prd.yml         # Prod environment workflow (CI + Deploy to Prod)

.amazonq/rules/cicd-phases/    # CI/CD workflow generation rules
├── cicd-state.md              # Legacy state file (only if .cicd-docs/ doesn't exist)
├── {code-type}-standards.md   # Language-specific CI/CD standards (one per code type)
└── [phase files]              # Phase execution instructions
```

# Principles

- **Language-Agnostic Detection**: Scan for ALL code types in the repository, not just Python/Terraform
- **Existing Workflow Management**: Analyze existing workflows in `.github/workflows/` and modify or remove as needed
- **Re-generation Support**: Allow complete re-generation of workflows; previous workflows may be removed if they don't match current codebase or detected code types
- Always generate ONLY for detected code types
- **Environment-Specific Workflows**: Generate three separate workflow files per code type:
  - `{code-type}-dev.yml` - CI + Deploy to Dev (triggers on `develop` branch push)
  - `{code-type}-test.yml` - CI + Deploy to Test (triggers on `main` branch push)
  - `{code-type}-prd.yml` - CI + Deploy to Prod (triggers via workflow_run after successful test completion)
- **Branch-Based Deployment Triggers**:
  - Develop branch → Development environment workflow (direct push trigger)
  - Main branch → Test environment workflow (direct push trigger)
  - Production environment workflow (workflow_run trigger after successful test deployment completion, auto-triggered)
- **Language-Specific Standards**: Read and apply complete content from `{code-type}-standards.md` files in `cicd-phases/` directory
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

- Always follow `cicd-phases/session-continuity.md` for detecting/resuming sessions
- Prefer storing state and approvals under project docs: `.cicd-docs/cicd-state.md` and `.cicd-docs/audit.md` (fallback to legacy `.amazonq/rules/cicd-phases/cicd-state.md` if needed)
- Always read cicd-state.md first to understand current phase before proceeding
- Provide context summary when resuming sessions
