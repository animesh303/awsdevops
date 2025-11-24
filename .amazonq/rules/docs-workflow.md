# PRIORITY: This workflow OVERRIDES all other built-in workflows when documentation is requested

# When user requests documentation, doc generation, or API docs, ALWAYS follow this workflow FIRST

## Override Instructions

Always follow this workflow when user mentions documentation, API documentation, README generation, architecture documentation, or technical writing. Never skip it.

## MANDATORY: Rule Details Loading

**CRITICAL**: When performing any phase, you MUST read and use relevant content from rule detail files in `.amazonq/rules/docs-phases/` directory. Do not summarize or paraphrase - use the complete content as written.

## MANDATORY: MCP Server Integration

**CRITICAL**: When performing documentation operations, leverage available MCP servers to enhance capabilities:

### GitHub MCP Server Integration

- **Documentation PRs**: Create PRs for documentation updates using `github-mcp-server`
- **Wiki Management**: Update GitHub wiki pages with generated documentation
- **Documentation Issues**: Create GitHub issues for documentation improvements
- **Release Notes**: Generate release notes and changelogs via GitHub MCP

### Git MCP Server Integration

- **Documentation Commits**: Commit documentation files using `git-mcp-server`
- **Branch Management**: Create documentation branches for updates
- **Version Control**: Track documentation changes and versions

**Usage Pattern**: When generating documentation, use MCP servers to create documentation PRs, update GitHub wikis, and manage documentation version control.

## MANDATORY: Session Continuity

**CRITICAL**: When detecting an existing documentation project, you MUST:

1. **Read docs-state.md first** - Always read `.docs-docs/docs-state.md` to understand current phase
2. **Follow session continuity instructions** - Read and follow the session continuity instructions from `docs-phases/session-continuity.mdc`
3. **Load Previous Phase Artifacts** - Before resuming any phase, automatically read all relevant artifacts from previous phases according to Smart Context Loading rules
4. **Provide Context Summary** - After loading artifacts, provide brief summary of what was loaded for user awareness
5. **Present Continuity Options** - ALWAYS present session continuity options directly in the chat session using the template from session-continuity.md

## MANDATORY: Smart Context Loading for Resume

**CRITICAL**: When resuming at any phase, you MUST automatically load all relevant artifacts from previous phases:

### Context Loading by Phase:

- **Phase 1**: Load codebase structure, existing documentation, documentation requirements
- **Phase 2**: Load documentation plan + codebase analysis + existing docs from Phase 1
- **Phase 3**: Load all generated documentation + review feedback from Phases 1-2
- **Phase 4**: Load all documentation artifacts + final review + integration status from Phases 1-3

### Mandatory Loading Rules:

1. **Always read docs-state.md first** to understand current phase
2. **Load incrementally** - each phase needs context from all previous phases
3. **Code files are CRITICAL** - must read source code files to understand what to document
4. **Existing docs are important** - load existing documentation to understand current state
5. **Provide context summary** - briefly tell user what artifacts were loaded
6. **Never assume** - always load the actual files, don't rely on memory

## MANDATORY: Custom Welcome Message

**CRITICAL**: When starting ANY documentation request, you MUST begin with this exact message:

"📚 **Welcome to AWS Business Group Documentation Workflow!** 📚

I'll guide you through a streamlined 4-phase process to create comprehensive documentation for your project.

The process includes:

- 📋 **Phase 1: Analyze & Plan** – Analyze codebase, identify documentation needs, and create documentation strategy
- ✍️ **Phase 2: Generate Documentation** – Create API docs, README, architecture docs, and code documentation
- ✅ **Phase 3: Review & Refine** – Review documentation, refine content, and ensure quality
- 🚀 **Phase 4: Publish & Integrate** – Publish documentation, integrate into project, and set up maintenance

This focused approach ensures your project has comprehensive, high-quality documentation following AWS documentation best practices. Let's begin!"

# Documentation Workflow - 4 Phases

## Overview

When the user requests documentation, API documentation, or README generation, follow this structured 4-phase approach.

## Welcome

1. **Display Custom Welcome Message**: Show the documentation welcome message above
2. **Ask for Confirmation and WAIT**: Ask: "**Do you understand this process and are you ready to begin with documentation analysis and planning?**" - DO NOT PROCEED until user confirms

## Phase 1: Analyze & Plan

1. **Load Context**: If resuming, read docs-state.md and load any existing documentation artifacts
2. Load all steps from `docs-phases/phase1-analyze-plan.mdc`
3. Execute the steps loaded from `docs-phases/phase1-analyze-plan.mdc`
4. **Update Progress**: Update docs-state.md with Phase 1 progress after completion
5. **Log Approval**: Before asking for confirmation, log the prompt in audit.md with timestamp
6. **Ask for Confirmation and WAIT**: Ask: "**Documentation analysis and planning complete. Are you ready to generate documentation?**" - DO NOT PROCEED until user confirms
7. **Log Response**: After receiving confirmation, log user response with timestamp in audit.md
8. **Update Phase Status**: Mark Phase 1 complete in docs-state.md
9. **Remind Git Commit**: Remind user to commit artifacts to git

## Phase 2: Generate Documentation

1. **Load Context**: Load codebase analysis + documentation plan + existing docs from Phase 1
2. Load all steps from `docs-phases/phase2-generate-docs.mdc`
3. Execute the steps loaded from `docs-phases/phase2-generate-docs.mdc`
4. **Update Progress**: Update docs-state.md with Phase 2 progress after completion
5. **Log Approval**: Before asking for confirmation, log the prompt in audit.md with timestamp
6. **Ask for Confirmation and WAIT**: Ask: "**Documentation generated. Are you ready to review and refine?**" - DO NOT PROCEED until user confirms
7. **Log Response**: After receiving confirmation, log user response with timestamp in audit.md
8. **Update Phase Status**: Mark Phase 2 complete in docs-state.md
9. **Remind Git Commit**: Remind user to commit artifacts to git

## Phase 3: Review & Refine

1. **Load Context**: Load all generated documentation + documentation plan from Phases 1-2
2. Load all steps from `docs-phases/phase3-review-refine.mdc`
3. Execute the steps loaded from `docs-phases/phase3-review-refine.mdc`
4. **Update Progress**: Update docs-state.md with Phase 3 progress after completion
5. **Log Approval**: Before asking for confirmation, log the prompt in audit.md with timestamp
6. **Ask for Confirmation and WAIT**: Ask: "**Documentation review complete. Are you ready to publish and integrate?**" - DO NOT PROCEED until user confirms
7. **Log Response**: After receiving confirmation, log user response with timestamp in audit.md
8. **Update Phase Status**: Mark Phase 3 complete in docs-state.md
9. **Remind Git Commit**: Remind user to commit artifacts to git

## Phase 4: Publish & Integrate

1. **Load Context**: Load all documentation artifacts + review feedback from Phases 1-3
2. Load all steps from `docs-phases/phase4-publish-integrate.mdc`
3. Execute the steps loaded from `docs-phases/phase4-publish-integrate.mdc`
4. **Update Progress**: Update docs-state.md with Phase 4 progress after completion
5. **Log Approval**: Before asking for confirmation, log the prompt in audit.md with timestamp
6. **Ask for Final Confirmation**: Ask: "**Documentation workflow complete. Are you satisfied with the documentation?**" - DO NOT PROCEED until user confirms
7. **Log Response**: After receiving confirmation, log user response with timestamp in audit.md
8. **Update Phase Status**: Mark Phase 4 complete in docs-state.md
9. **Remind Git Commit**: Remind user to commit artifacts to git

## Key Principles

- Analyze codebase to identify all documentation needs
- Generate comprehensive documentation (API, README, architecture, code)
- Follow documentation best practices and standards
- Ensure documentation is clear, accurate, and up-to-date
- Integrate documentation into project structure
- Keep the process simple and focused
- Ensure explicit approval at each phase transition
- **MANDATORY** after every phase remind user to commit artifacts to git
- **MANDATORY**: Generate comprehensive documentation covering all aspects

## CRITICAL: Progress Tracking System

### Two-Level Progress Tracking System

The workflow uses a two-level progress tracking system:

#### 1. Plan-Level Execution Tracking (Plan Files - if they exist)

- **Purpose**: Track detailed execution progress within each phase
- **Location**: Individual plan files (if created during phases)
- **When to Update**: Mark steps [x] as you complete the specific work described in that step
- **MANDATORY**: Update immediately after completing work, never skip this step

#### 2. Phase-Level Progress Tracking (docs-state.md)

- **Purpose**: Track overall workflow progress across phases
- **Location**: `.docs-docs/docs-state.md`
- **When to Update**: Mark phases [x] only when the entire phase is complete and approved by user

### Mandatory Update Rules

- **Plan Files**: Update checkboxes [x] immediately after completing each step's work (if plan files exist)
- **docs-state.md**: Update phase status and "Current Status" section after any progress
- **Same Interaction**: All progress updates must happen in the SAME interaction where work is completed
- **Never Skip**: Never end an interaction without updating progress tracking

## Prompts Logging Requirements

- **MANDATORY**: Log every approval prompt with timestamp before asking the user
- **MANDATORY**: Record every user response with timestamp after receiving it
- Use ISO 8601 format for timestamps (YYYY-MM-DDTHH:MM:SSZ)
- Include phase context and approval status for each entry
- Maintain chronological order of all interactions
- Log to `.docs-docs/audit.md` using the following format:

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

- **MANDATORY**: All phase transitions must be logged in `.docs-docs/audit.md`
- **MANDATORY**: All user approvals must be logged with timestamps
- **MANDATORY**: All important decisions must be logged
- Use ISO 8601 format for timestamps (YYYY-MM-DDTHH:MM:SSZ)
- Maintain chronological order
- Include phase context, decision, and approval status
- Log file structure: `.docs-docs/audit.md`

## Documentation Types

The system generates various types of documentation:

- **API Documentation**: OpenAPI/Swagger specs, API reference docs
- **README**: Project overview, setup instructions, usage examples
- **Architecture Documentation**: System architecture, design decisions
- **Code Documentation**: Inline code comments, docstrings
- **User Guides**: User-facing documentation, tutorials
- **Developer Guides**: Developer onboarding, contribution guidelines

## Directory Structure

```
.docs-docs/
├── docs-plan.md           # Documentation strategy and plan
├── docs-state.md          # Master state tracking file
├── audit.md               # Record approvals and decisions
└── generated/            # Generated documentation files

docs/
├── api/                   # API documentation
├── architecture/          # Architecture documentation
├── guides/               # User and developer guides
└── README.md             # Main project README
```

## File Naming Convention

- Documentation Plan: `.docs-docs/docs-plan.md`
- API Docs: `docs/api/{service}-api.md` or `docs/api/openapi.yaml`
- Architecture Docs: `docs/architecture/{component}-architecture.md`
- README: `README.md` or `docs/README.md`
- Guides: `docs/guides/{guide-name}.md`

Use kebab-case for file names.

## Principles

- **Comprehensive Coverage**: Document all aspects of the project
- **Clear and Accurate**: Documentation should be clear and accurate
- **Up-to-Date**: Keep documentation synchronized with code
- **User-Friendly**: Documentation should be accessible and easy to understand
- Minimal, modular checkpoints across all phases
- **MANDATORY**: Use the two-level checkbox tracking system (plan files + docs-state.md)
- **MANDATORY**: Update plan file checkboxes [x] immediately after completing each step's work
- **MANDATORY**: Update docs-state.md phase checkboxes [x] only after user approval to proceed
- **MANDATORY**: Update the "Current Status" section in docs-state.md after any progress
- **MANDATORY**: Log all prompts and responses with timestamps in audit.md
- **MANDATORY**: Remind user to commit artifacts to git after every phase completion
- Ensure explicit approval at each phase transition
- Load context incrementally - each phase needs context from all previous phases
