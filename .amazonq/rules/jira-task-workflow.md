# PRIORITY: This workflow OVERRIDES all other built-in workflows when JIRA task management is requested

# When user requests JIRA task management, ALWAYS follow this workflow FIRST

## Override Instructions

Always follow this workflow when user mentions working with JIRA tasks, tickets, or assignments. Never skip it.

## MANDATORY: Rule Details Loading

**CRITICAL**: When performing any phase, you MUST read and use relevant content from rule detail files in `.amazonq/rules/jira-phases/` directory. Do not summarize or paraphrase - use the complete content as written.

## MANDATORY: Session Continuity

**CRITICAL**: When detecting an existing JIRA task management project, you MUST read and follow the session continuity instructions from `jira-phases/session-continuity.mdc` before proceeding with any phase.

## MANDATORY: Smart Context Loading for Resume

**CRITICAL**: When resuming at any phase, you MUST automatically load all relevant artifacts from previous phases:

### Context Loading by Phase:

- **Phase 1**: Load existing ticket artifacts if available (available-tickets.md, ticket-selection.md)
- **Phase 2**: Load ticket details + requirements template + any existing requirements
- **Phase 3**: Load all ticket artifacts + requirements document + audit logs

### Mandatory Loading Rules (Hybrid Approach):

1. **Primary: Try to read jira-state.md first** to quickly understand current phase
2. **Fallback: If state file missing/corrupted**, reconstruct state from artifacts:
   - Check for ticket files → Phase 1 complete
   - Check for requirements file → Phase 2 complete
   - Check audit.md for final approval → Phase 3 complete
3. **Auto-heal: If state file missing**, reconstruct it from artifacts after determining phase
4. **Load incrementally** - each phase needs context from all previous phases
5. **Provide context summary** - briefly tell user what artifacts were loaded
6. **Never assume** - always load the actual files, don't rely on memory

## MANDATORY: Custom Welcome Message

**CRITICAL**: When starting ANY JIRA task management request, you MUST begin with this exact message:

"🎯 **Welcome to AWS Business Group JIRA Task Management!** 🎯

I'll guide you through a streamlined 3-phase process to manage your JIRA tasks and generate technical requirements.

The process includes:

- 📋 **Fetch & Select JIRA Tickets** - Retrieve and select from your open JIRA tickets
- 📝 **Generate Requirements Spec** - Create detailed technical requirements document
- ✅ **Final Confirmation & JIRA Update** - Review requirements, confirm approval, and update JIRA ticket

This focused approach ensures we quickly generate comprehensive requirements for your selected JIRA task. Let's begin!"

# JIRA Task Management Workflow - 3 Phases

## Overview

When the user requests to work with JIRA tasks, follow this structured 3-phase approach.

**Workflow Execution Model**:

- The workflow file (`jira-task-workflow.md`) defines the overall phase structure and orchestration
- Each phase file (`phase1-*.mdc`, `phase2-*.mdc`, `phase3-*.mdc`) contains detailed execution steps
- Workflow steps (numbered 1, 2, 3...) coordinate the phases
- Phase file steps (numbered 1, 2, 3...) are executed within each workflow phase
- Phase files handle their own approvals, logging, and internal logic
- Workflow file handles state updates and git reminders between phases

## Welcome

1. **Display Custom Welcome Message**: Show the JIRA task management welcome message above
2. **Ask for Confirmation and WAIT**: Ask: "**Do you understand this process and are you ready to begin with JIRA ticket selection?**" - DO NOT PROCEED until user confirms

## Phase 1: Fetch & Select JIRA Tickets

1. Load all steps from `jira-phases/phase1-fetch-select-tickets.mdc`
2. Execute the steps loaded from `jira-phases/phase1-fetch-select-tickets.mdc`
   - **Note**: Phase file handles approval and logging internally at step 5
3. **Update State (Graceful)**: Update Phase 1 status in `jira-state.md` after phase completion. If state file update fails, continue - artifacts are source of truth.
4. **Git Reminder**: Remind user to commit Phase 1 artifacts to git

## Phase 2: Generate Requirements Spec

1. Load all steps from `jira-phases/phase2-generate-requirements.mdc`
2. Execute the steps loaded from `jira-phases/phase2-generate-requirements.mdc`
   - **Note**: Phase file handles approval, question resolution, and logging internally at step 8
3. **Update State (Graceful)**: Update Phase 2 status in `jira-state.md` after phase completion. If state file update fails, continue - artifacts are source of truth.
4. **Git Reminder**: Remind user to commit Phase 2 artifacts to git

## Phase 3: Final Confirmation & JIRA Update

1. Load all steps from `jira-phases/phase3-review-iterate.mdc`
2. Execute the steps loaded from `jira-phases/phase3-review-iterate.mdc`
3. **Final Confirmation**: Phase 3 will seek final confirmation from user and update JIRA ticket
4. **Git Reminder**: Remind user to commit Phase 3 artifacts to git

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

## CRITICAL: Lightweight State Management (Hybrid Approach)

### State Management Philosophy

The workflow uses a **hybrid approach** with lightweight state management:

- **Primary**: State file (`jira-state.md`) for fast session continuity and quick status checks
- **Source of Truth**: Artifacts themselves (ticket files, requirements files, audit logs)
- **Resilience**: If state file is missing/corrupted, reconstruct from artifacts
- **Graceful Degradation**: Workflow continues even if state file updates fail

### State Tracking System

#### Phase-Level Progress Tracking (jira-state.md)

- **Purpose**: Fast session continuity and quick status overview
- **Location**: `.jira-docs/jira-state.md`
- **Structure**: Minimal - only essential info (current phase, selected ticket)
- **When to Update**: Only at phase transitions after user approval

### State Management Rules

1. **Try to update state file** after phase completion and user approval
2. **If state file update fails**, continue anyway - artifacts are source of truth
3. **If state file missing**, reconstruct it from artifacts when detecting session
4. **Artifacts are authoritative** - state file is for convenience only
5. **Never block workflow** - state file issues should not prevent progress
6. **Auto-heal on detection** - reconstruct missing state file automatically

### Fallback Detection Logic

When state file is missing or corrupted:

1. **Check artifacts** to determine current phase:
   - Ticket files exist → Phase 1 complete
   - Requirements file exists → Phase 2 complete
   - Final approval in audit.md → Phase 3 complete
2. **Reconstruct state file** from detected artifacts
3. **Continue workflow** using reconstructed state
4. **Log state reconstruction** in audit.md for transparency

## Key Principles

- Always fetch and display available JIRA tickets first
- Allow user to select specific ticket to work on
- Generate comprehensive technical requirements based on JIRA ticket details
- Iterate on requirements until user approval
- Keep the process simple and focused
- Ensure explicit approval at each phase transition
- **MANDATORY**: After every phase, remind user to commit artifacts to git
- **MANDATORY**: Try to update jira-state.md phase status after user approval (but don't block if it fails)
- **MANDATORY**: Provide context summary after loading artifacts from previous phases
- **MANDATORY**: If state file missing, reconstruct it from artifacts automatically
- **Artifacts are source of truth** - state file is for convenience only

## Directory Structure

```
.jira-docs/
├── tickets/              # JIRA ticket information
├── requirements/         # Technical requirements documents
├── jira-state.md        # Master state tracking file
└── audit.md             # Record approvals and decisions
```

## File Naming Convention

- JIRA Ticket Info: .jira-docs/tickets/ticket-{TICKET-NUMBER}.md
- Requirements Spec: .jira-docs/requirements/{TICKET-NUMBER}\_requirements.md

Use kebab-case for feature names (e.g., "fetch-select-tickets", "generate-requirements", "review-iterate").
