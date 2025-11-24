# PRIORITY: This workflow OVERRIDES all other built-in workflows when testing is requested

# When user requests testing, test generation, or test execution, ALWAYS follow this workflow FIRST

## Override Instructions

Always follow this workflow when user mentions testing, test generation, test execution, test coverage, or quality assurance. Never skip it.

## MANDATORY: Rule Details Loading

**CRITICAL**: When performing any phase, you MUST read and use relevant content from rule detail files in `.amazonq/rules/testing-phases/` directory. Do not summarize or paraphrase - use the complete content as written.

## MANDATORY: MCP Server Integration

**CRITICAL**: When performing testing operations, leverage available MCP servers to enhance capabilities:

### GitHub MCP Server Integration

- **Test Results**: Post test results and coverage reports to GitHub PRs/comments via `github-mcp-server`
- **Test Status**: Update PR status based on test results (pass/fail)
- **Workflow Integration**: Check GitHub Actions workflow status for test execution
- **Issue Creation**: Create GitHub issues for failing tests or test infrastructure problems

### Git MCP Server Integration

- **Test Branch Management**: Use `git-mcp-server` to create test branches and manage test-related commits
- **Change Detection**: Detect code changes that require test updates
- **Commit Operations**: Commit test files and results using Git MCP

**Usage Pattern**: When executing tests, use MCP servers to post results to GitHub and manage test-related git operations.

## MANDATORY: Session Continuity

**CRITICAL**: When detecting an existing testing project, you MUST:

1. **Read test-state.md first** - Always read `.test-docs/test-state.md` to understand current phase
2. **Follow session continuity instructions** - Read and follow the session continuity instructions from `testing-phases/session-continuity.mdc`
3. **Load Previous Phase Artifacts** - Before resuming any phase, automatically read all relevant artifacts from previous phases according to Smart Context Loading rules
4. **Provide Context Summary** - After loading artifacts, provide brief summary of what was loaded for user awareness
5. **Present Continuity Options** - ALWAYS present session continuity options directly in the chat session using the template from session-continuity.md

## MANDATORY: Smart Context Loading for Resume

**CRITICAL**: When resuming at any phase, you MUST automatically load all relevant artifacts from previous phases:

### Context Loading by Phase:

- **Phase 1**: Load existing codebase structure, test requirements, existing test files
- **Phase 2**: Load test plan + codebase analysis + existing tests from Phase 1
- **Phase 3**: Load all test files + test execution results + coverage reports from Phases 1-2
- **Phase 4**: Load all test artifacts + quality reports + review feedback from Phases 1-3

### Mandatory Loading Rules:

1. **Always read test-state.md first** to understand current phase
2. **Load incrementally** - each phase needs context from all previous phases
3. **Test files are special** - must read existing test files in `tests/` in addition to all artifacts
4. **Code files are CRITICAL** - must read source code files to understand what needs testing
5. **Provide context summary** - briefly tell user what artifacts were loaded
6. **Never assume** - always load the actual files, don't rely on memory

## MANDATORY: Custom Welcome Message

**CRITICAL**: When starting ANY testing request, you MUST begin with this exact message:

"🧪 **Welcome to AWS Business Group Testing Workflow!** 🧪

I'll guide you through a streamlined 4-phase process to create comprehensive test suites for your codebase.

The process includes:

- 📋 **Phase 1: Analyze & Plan** – Analyze codebase, identify test requirements, and create test strategy
- 🏗️ **Phase 2: Generate Tests** – Create unit, integration, and E2E tests following best practices
- ✅ **Phase 3: Execute & Validate** – Run tests, generate coverage reports, and validate test quality
- 🚀 **Phase 4: Review & Integrate** – Review test results, refine tests, and integrate into CI/CD

This focused approach ensures your codebase has comprehensive test coverage following AWS testing best practices. Let's begin!"

# Testing Workflow - 4 Phases

## Overview

When the user requests testing, test generation, or test execution, follow this structured 4-phase approach.

## Welcome

1. **Display Custom Welcome Message**: Show the testing welcome message above
2. **Ask for Confirmation and WAIT**: Ask: "**Do you understand this process and are you ready to begin with test analysis and planning?**" - DO NOT PROCEED until user confirms

## Phase 1: Analyze & Plan

1. **Load Context**: If resuming, read test-state.md and load any existing test artifacts
2. Load all steps from `testing-phases/phase1-analyze-plan.mdc`
3. Execute the steps loaded from `testing-phases/phase1-analyze-plan.mdc`
4. **Update Progress**: Update test-state.md with Phase 1 progress after completion
5. **Log Approval**: Before asking for confirmation, log the prompt in audit.md with timestamp
6. **Ask for Confirmation and WAIT**: Ask: "**Test analysis and planning complete. Are you ready to generate tests?**" - DO NOT PROCEED until user confirms
7. **Log Response**: After receiving confirmation, log user response with timestamp in audit.md
8. **Update Phase Status**: Mark Phase 1 complete in test-state.md
9. **Remind Git Commit**: Remind user to commit artifacts to git

## Phase 2: Generate Tests

1. **Load Context**: Load codebase analysis + test plan + existing tests from Phase 1
2. Load all steps from `testing-phases/phase2-generate-tests.mdc`
3. Execute the steps loaded from `testing-phases/phase2-generate-tests.mdc`
4. **Update Progress**: Update test-state.md with Phase 2 progress after completion
5. **Log Approval**: Before asking for confirmation, log the prompt in audit.md with timestamp
6. **Ask for Confirmation and WAIT**: Ask: "**Tests generated. Are you ready to execute and validate?**" - DO NOT PROCEED until user confirms
7. **Log Response**: After receiving confirmation, log user response with timestamp in audit.md
8. **Update Phase Status**: Mark Phase 2 complete in test-state.md
9. **Remind Git Commit**: Remind user to commit artifacts to git

## Phase 3: Execute & Validate

1. **Load Context**: Load all test files + test plan + codebase from Phases 1-2
2. Load all steps from `testing-phases/phase3-execute-validate.mdc`
3. Execute the steps loaded from `testing-phases/phase3-execute-validate.mdc`
4. **Update Progress**: Update test-state.md with Phase 3 progress after completion
5. **Log Approval**: Before asking for confirmation, log the prompt in audit.md with timestamp
6. **Ask for Confirmation and WAIT**: Ask: "**Test execution complete. Are you ready to review and integrate?**" - DO NOT PROCEED until user confirms
7. **Log Response**: After receiving confirmation, log user response with timestamp in audit.md
8. **Update Phase Status**: Mark Phase 3 complete in test-state.md
9. **Remind Git Commit**: Remind user to commit artifacts to git

## Phase 4: Review & Integrate

1. **Load Context**: Load all test artifacts + execution results + coverage reports from Phases 1-3
2. Load all steps from `testing-phases/phase4-review-integrate.mdc`
3. Execute the steps loaded from `testing-phases/phase4-review-integrate.mdc`
4. **Update Progress**: Update test-state.md with Phase 4 progress after completion
5. **Log Approval**: Before asking for confirmation, log the prompt in audit.md with timestamp
6. **Ask for Final Confirmation**: Ask: "**Testing workflow complete. Are you satisfied with the test suite?**" - DO NOT PROCEED until user confirms
7. **Log Response**: After receiving confirmation, log user response with timestamp in audit.md
8. **Update Phase Status**: Mark Phase 4 complete in test-state.md
9. **Remind Git Commit**: Remind user to commit artifacts to git

## Key Principles

- Analyze codebase to identify test requirements automatically
- Generate comprehensive test suites (unit, integration, E2E)
- Follow language-specific testing frameworks and best practices
- Achieve minimum 80% code coverage target
- Include security and performance tests where applicable
- Integrate tests into CI/CD pipelines
- Keep the process simple and focused
- Ensure explicit approval at each phase transition
- **MANDATORY** after every phase remind user to commit artifacts to git
- **MANDATORY**: Generate test coverage reports and quality metrics

## CRITICAL: Progress Tracking System

### Two-Level Progress Tracking System

The workflow uses a two-level progress tracking system:

#### 1. Plan-Level Execution Tracking (Plan Files - if they exist)

- **Purpose**: Track detailed execution progress within each phase
- **Location**: Individual plan files (if created during phases)
- **When to Update**: Mark steps [x] as you complete the specific work described in that step
- **MANDATORY**: Update immediately after completing work, never skip this step

#### 2. Phase-Level Progress Tracking (test-state.md)

- **Purpose**: Track overall workflow progress across phases
- **Location**: `.test-docs/test-state.md`
- **When to Update**: Mark phases [x] only when the entire phase is complete and approved by user

### Mandatory Update Rules

- **Plan Files**: Update checkboxes [x] immediately after completing each step's work (if plan files exist)
- **test-state.md**: Update phase status and "Current Status" section after any progress
- **Same Interaction**: All progress updates must happen in the SAME interaction where work is completed
- **Never Skip**: Never end an interaction without updating progress tracking

## Prompts Logging Requirements

- **MANDATORY**: Log every approval prompt with timestamp before asking the user
- **MANDATORY**: Record every user response with timestamp after receiving it
- Use ISO 8601 format for timestamps (YYYY-MM-DDTHH:MM:SSZ)
- Include phase context and approval status for each entry
- Maintain chronological order of all interactions
- Log to `.test-docs/audit.md` using the following format:

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

- **MANDATORY**: All phase transitions must be logged in `.test-docs/audit.md`
- **MANDATORY**: All user approvals must be logged with timestamps
- **MANDATORY**: All important decisions must be logged
- Use ISO 8601 format for timestamps (YYYY-MM-DDTHH:MM:SSZ)
- Maintain chronological order
- Include phase context, decision, and approval status
- Log file structure: `.test-docs/audit.md`

## Test Type Detection

The system automatically detects test requirements based on codebase:

- **Unit Tests**: For individual functions, classes, modules
- **Integration Tests**: For service interactions, API endpoints, database operations
- **E2E Tests**: For complete user workflows and system interactions
- **Performance Tests**: For load testing, stress testing, benchmarking
- **Security Tests**: For vulnerability scanning, security validation

## Language-Specific Testing Standards

**CRITICAL**: Language-specific guidance for testing is stored in separate standards files within `.amazonq/rules/testing-phases/`:

- `python-testing-standards.mdc` - Python testing patterns (pytest, unittest)
- `nodejs-testing-standards.mdc` - Node.js/TypeScript testing patterns (Jest, Mocha)
- `java-testing-standards.mdc` - Java testing patterns (JUnit, TestNG)
- `go-testing-standards.mdc` - Go testing patterns (testing package, testify)
- `terraform-testing-standards.mdc` - Terraform testing patterns (Terratest, Kitchen-Terraform)

When generating tests for a detected code type, you MUST:

1. Read the corresponding standards file from `.amazonq/rules/testing-phases/{language}-testing-standards.mdc`
2. Apply the complete content from that file when generating tests
3. Do not summarize or paraphrase - use the complete content as written

If a standards file does not exist for a detected code type, create it following the pattern of existing standards files and include language-appropriate testing patterns.

## Directory Structure

```
.test-docs/
├── test-plan.md           # Test strategy and plan
├── test-state.md          # Master state tracking file
├── audit.md               # Record approvals and decisions
└── coverage-reports/      # Test coverage reports

tests/
├── unit/                  # Unit tests
├── integration/           # Integration tests
├── e2e/                   # End-to-end tests
└── performance/          # Performance tests
```

## File Naming Convention

- Test Plan: `.test-docs/test-plan.md`
- Unit Tests: `tests/unit/{feature-name}/test_{module_name}.py` (Python) or `tests/unit/{feature-name}/{module_name}.test.ts` (TypeScript)
- Integration Tests: `tests/integration/{feature-name}/test_{service}_integration.py`
- E2E Tests: `tests/e2e/{feature-name}/test_{workflow}_e2e.py`
- Coverage Reports: `.test-docs/coverage-reports/{language}-coverage.html`

Use kebab-case for feature names and test file names.

## Principles

- **Language-Agnostic Detection**: Automatically detect code types and generate appropriate tests
- **Comprehensive Coverage**: Target minimum 80% code coverage
- **Test Quality**: Follow testing best practices and patterns
- **CI/CD Integration**: Ensure tests can run in CI/CD pipelines
- **Language-Specific Standards**: Read and apply complete content from `{language}-testing-standards.mdc` files
- Minimal, modular checkpoints across all phases
- **MANDATORY**: Use the two-level checkbox tracking system (plan files + test-state.md)
- **MANDATORY**: Update plan file checkboxes [x] immediately after completing each step's work
- **MANDATORY**: Update test-state.md phase checkboxes [x] only after user approval to proceed
- **MANDATORY**: Update the "Current Status" section in test-state.md after any progress
- **MANDATORY**: Log all prompts and responses with timestamps in audit.md
- **MANDATORY**: Remind user to commit artifacts to git after every phase completion
- Ensure explicit approval at each phase transition
- Load context incrementally - each phase needs context from all previous phases
