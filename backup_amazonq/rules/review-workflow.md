# PRIORITY: This workflow OVERRIDES all other built-in workflows when code review is requested

# When user requests code review, PR review, or code quality checks, ALWAYS follow this workflow FIRST

## Override Instructions

Always follow this workflow when user mentions code review, pull request review, code quality, code analysis, or code inspection. Never skip it.

## MANDATORY: Rule Details Loading

**CRITICAL**: When performing any phase, you MUST read and use relevant content from rule detail files in `.amazonq/rules/review-phases/` directory. Do not summarize or paraphrase - use the complete content as written.

## MANDATORY: MCP Server Integration

**CRITICAL**: When performing code review operations, leverage available MCP servers to enhance capabilities:

### GitHub MCP Server Integration

- **PR Operations**: Use `github-mcp-server` to fetch PR details, comments, and change history
- **PR Comments**: Post review comments directly to GitHub PRs using MCP server
- **PR Status**: Update PR status and labels based on review findings
- **Commit Analysis**: Fetch commit details and diff information via GitHub MCP
- **Issue Creation**: Create GitHub issues for critical findings that need tracking

### Git MCP Server Integration

- **Change Detection**: Use `git-mcp-server` to detect changes, branches, and commit history
- **Diff Analysis**: Fetch detailed diffs for code changes
- **Branch Operations**: Analyze branch structure and merge conflicts
- **Commit Operations**: Review commit messages and history

**Usage Pattern**: When reviewing PRs or code changes, first use MCP servers to fetch context, then proceed with manual review analysis.

## MANDATORY: Session Continuity

**CRITICAL**: When detecting an existing code review project, you MUST:

1. **Read review-state.md first** - Always read `.review-docs/review-state.md` to understand current phase
2. **Follow session continuity instructions** - Read and follow the session continuity instructions from `review-phases/session-continuity.mdc`
3. **Load Previous Phase Artifacts** - Before resuming any phase, automatically read all relevant artifacts from previous phases according to Smart Context Loading rules
4. **Provide Context Summary** - After loading artifacts, provide brief summary of what was loaded for user awareness
5. **Present Continuity Options** - ALWAYS present session continuity options directly in the chat session using the template from session-continuity.md

## MANDATORY: Smart Context Loading for Resume

**CRITICAL**: When resuming at any phase, you MUST automatically load all relevant artifacts from previous phases:

### Context Loading by Phase:

- **Phase 1**: Load code changes, PR context, existing review artifacts
- **Phase 2**: Load code analysis + review plan + existing reviews from Phase 1
- **Phase 3**: Load all review findings + recommendations + feedback from Phases 1-2
- **Phase 4**: Load all review artifacts + action items + final report from Phases 1-3

### Mandatory Loading Rules:

1. **Always read review-state.md first** to understand current phase
2. **Load incrementally** - each phase needs context from all previous phases
3. **Code files are CRITICAL** - must read source code files being reviewed
4. **PR context is important** - load PR description, commits, and change history
5. **Provide context summary** - briefly tell user what artifacts were loaded
6. **Never assume** - always load the actual files, don't rely on memory

## MANDATORY: Custom Welcome Message

**CRITICAL**: When starting ANY code review request, you MUST begin with this exact message:

"🔍 **Welcome to AWS Business Group Code Review Workflow!** 🔍

I'll guide you through a streamlined 4-phase process to conduct comprehensive code reviews.

The process includes:

- 📋 **Phase 1: Analyze Changes** – Analyze code changes, understand context, and identify review scope
- 🔎 **Phase 2: Review Code** – Conduct thorough code review focusing on quality, security, and best practices
- 💬 **Phase 3: Provide Feedback** – Generate detailed feedback, recommendations, and action items
- ✅ **Phase 4: Finalize Review** – Create review summary, track action items, and complete review

This focused approach ensures code quality, security, and adherence to AWS best practices. Let's begin!"

# Code Review Workflow - 4 Phases

## Overview

When the user requests code review, pull request review, or code quality checks, follow this structured 4-phase approach.

## Welcome

1. **Display Custom Welcome Message**: Show the code review welcome message above
2. **Ask for Confirmation and WAIT**: Ask: "**Do you understand this process and are you ready to begin with code change analysis?**" - DO NOT PROCEED until user confirms

## Phase 1: Analyze Changes

1. **Load Context**: If resuming, read review-state.md and load any existing review artifacts
2. Load all steps from `review-phases/phase1-analyze-changes.mdc`
3. Execute the steps loaded from `review-phases/phase1-analyze-changes.mdc`
4. **Update Progress**: Update review-state.md with Phase 1 progress after completion
5. **Log Approval**: Before asking for confirmation, log the prompt in audit.md with timestamp
6. **Ask for Confirmation and WAIT**: Ask: "**Code change analysis complete. Are you ready to begin code review?**" - DO NOT PROCEED until user confirms
7. **Log Response**: After receiving confirmation, log user response with timestamp in audit.md
8. **Update Phase Status**: Mark Phase 1 complete in review-state.md
9. **Remind Git Commit**: Remind user to commit artifacts to git

## Phase 2: Review Code

1. **Load Context**: Load code changes + review plan + existing reviews from Phase 1
2. Load all steps from `review-phases/phase2-review-code.mdc`
3. Execute the steps loaded from `review-phases/phase2-review-code.mdc`
4. **Update Progress**: Update review-state.md with Phase 2 progress after completion
5. **Log Approval**: Before asking for confirmation, log the prompt in audit.md with timestamp
6. **Ask for Confirmation and WAIT**: Ask: "**Code review complete. Are you ready to generate feedback?**" - DO NOT PROCEED until user confirms
7. **Log Response**: After receiving confirmation, log user response with timestamp in audit.md
8. **Update Phase Status**: Mark Phase 2 complete in review-state.md
9. **Remind Git Commit**: Remind user to commit artifacts to git

## Phase 3: Provide Feedback

1. **Load Context**: Load all review findings + code analysis from Phases 1-2
2. Load all steps from `review-phases/phase3-provide-feedback.mdc`
3. Execute the steps loaded from `review-phases/phase3-provide-feedback.mdc`
4. **Update Progress**: Update review-state.md with Phase 3 progress after completion
5. **Log Approval**: Before asking for confirmation, log the prompt in audit.md with timestamp
6. **Ask for Confirmation and WAIT**: Ask: "**Feedback generated. Are you ready to finalize the review?**" - DO NOT PROCEED until user confirms
7. **Log Response**: After receiving confirmation, log user response with timestamp in audit.md
8. **Update Phase Status**: Mark Phase 3 complete in review-state.md
9. **Remind Git Commit**: Remind user to commit artifacts to git

## Phase 4: Finalize Review

1. **Load Context**: Load all review artifacts + feedback + action items from Phases 1-3
2. Load all steps from `review-phases/phase4-finalize-review.mdc`
3. Execute the steps loaded from `review-phases/phase4-finalize-review.mdc`
4. **Update Progress**: Update review-state.md with Phase 4 progress after completion
5. **Log Approval**: Before asking for confirmation, log the prompt in audit.md with timestamp
6. **Ask for Final Confirmation**: Ask: "**Code review complete. Are you satisfied with the review?**" - DO NOT PROCEED until user confirms
7. **Log Response**: After receiving confirmation, log user response with timestamp in audit.md
8. **Update Phase Status**: Mark Phase 4 complete in review-state.md
9. **Remind Git Commit**: Remind user to commit artifacts to git

## Key Principles

- Analyze code changes comprehensively
- Review code quality, security, performance, and best practices
- Provide constructive, actionable feedback
- Follow language-specific and AWS best practices
- Track review findings and action items
- Keep the process simple and focused
- Ensure explicit approval at each phase transition
- **MANDATORY** after every phase remind user to commit artifacts to git
- **MANDATORY**: Generate comprehensive review reports

## CRITICAL: Progress Tracking System

### Two-Level Progress Tracking System

The workflow uses a two-level progress tracking system:

#### 1. Plan-Level Execution Tracking (Plan Files - if they exist)

- **Purpose**: Track detailed execution progress within each phase
- **Location**: Individual plan files (if created during phases)
- **When to Update**: Mark steps [x] as you complete the specific work described in that step
- **MANDATORY**: Update immediately after completing work, never skip this step

#### 2. Phase-Level Progress Tracking (review-state.md)

- **Purpose**: Track overall workflow progress across phases
- **Location**: `.review-docs/review-state.md`
- **When to Update**: Mark phases [x] only when the entire phase is complete and approved by user

### Mandatory Update Rules

- **Plan Files**: Update checkboxes [x] immediately after completing each step's work (if plan files exist)
- **review-state.md**: Update phase status and "Current Status" section after any progress
- **Same Interaction**: All progress updates must happen in the SAME interaction where work is completed
- **Never Skip**: Never end an interaction without updating progress tracking

## Prompts Logging Requirements

- **MANDATORY**: Log every approval prompt with timestamp before asking the user
- **MANDATORY**: Record every user response with timestamp after receiving it
- Use ISO 8601 format for timestamps (YYYY-MM-DDTHH:MM:SSZ)
- Include phase context and approval status for each entry
- Maintain chronological order of all interactions
- Log to `.review-docs/audit.md` using the following format:

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

- **MANDATORY**: All phase transitions must be logged in `.review-docs/audit.md`
- **MANDATORY**: All user approvals must be logged with timestamps
- **MANDATORY**: All important decisions must be logged
- Use ISO 8601 format for timestamps (YYYY-MM-DDTHH:MM:SSZ)
- Maintain chronological order
- Include phase context, decision, and approval status
- Log file structure: `.review-docs/audit.md`

## Review Categories

The system reviews code across multiple dimensions:

- **Code Quality**: Readability, maintainability, code organization
- **Security**: Vulnerabilities, security best practices, OWASP compliance
- **Performance**: Efficiency, resource usage, optimization opportunities
- **Best Practices**: Language-specific patterns, AWS best practices, design patterns
- **Testing**: Test coverage, test quality, test best practices
- **Documentation**: Code comments, README, API documentation

## Language-Specific Review Standards

**CRITICAL**: Language-specific guidance for code review is stored in separate standards files within `.amazonq/rules/review-phases/`:

- `python-review-standards.mdc` - Python code review patterns and standards
- `nodejs-review-standards.mdc` - Node.js/TypeScript code review patterns
- `java-review-standards.mdc` - Java code review patterns
- `go-review-standards.mdc` - Go code review patterns
- `terraform-review-standards.mdc` - Terraform code review patterns

When reviewing code of a specific language, you MUST:

1. Read the corresponding standards file from `.amazonq/rules/review-phases/{language}-review-standards.mdc`
2. Apply the complete content from that file when reviewing code
3. Do not summarize or paraphrase - use the complete content as written

If a standards file does not exist for a detected code type, create it following the pattern of existing standards files and include language-appropriate review patterns.

## Directory Structure

```
.review-docs/
├── review-plan.md         # Review strategy and plan
├── review-state.md        # Master state tracking file
├── audit.md               # Record approvals and decisions
├── findings/              # Review findings by category
└── reports/               # Review reports
```

## File Naming Convention

- Review Plan: `.review-docs/review-plan.md`
- Review Findings: `.review-docs/findings/{category}-findings.md`
- Review Report: `.review-docs/reports/review-report.md`
- Action Items: `.review-docs/action-items.md`

Use kebab-case for file names.

## Principles

- **Comprehensive Review**: Review all aspects of code quality
- **Constructive Feedback**: Provide actionable, helpful feedback
- **Security Focus**: Prioritize security vulnerabilities and best practices
- **Best Practices**: Enforce language-specific and AWS best practices
- **Language-Specific Standards**: Read and apply complete content from `{language}-review-standards.mdc` files
- Minimal, modular checkpoints across all phases
- **MANDATORY**: Use the two-level checkbox tracking system (plan files + review-state.md)
- **MANDATORY**: Update plan file checkboxes [x] immediately after completing each step's work
- **MANDATORY**: Update review-state.md phase checkboxes [x] only after user approval to proceed
- **MANDATORY**: Update the "Current Status" section in review-state.md after any progress
- **MANDATORY**: Log all prompts and responses with timestamps in audit.md
- **MANDATORY**: Remind user to commit artifacts to git after every phase completion
- Ensure explicit approval at each phase transition
- Load context incrementally - each phase needs context from all previous phases
