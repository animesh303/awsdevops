# JIRA Task Management Session Continuity

## Welcome Back Prompt Template

When a user returns to continue work on an existing JIRA task management project, present this prompt DIRECTLY IN CHAT:

**Welcome back! I can see you have an existing JIRA task management project in progress.**

Here's your current status:

- **Selected Ticket**: [TICKET-NUMBER] - [TICKET-TITLE]
- **Current Phase**: [Phase X: Phase Name]
- **Requirements Status**: [Generated/In Review/Approved]
- **Last Completed**: [Last completed step]
- **Next Step**: [Next step to work on]

> _Status detected from [state file | artifacts]_ (show which method was used)

**What would you like to work on today?**

A) Continue where you left off ([Next step description])
B) Review the selected JIRA ticket details
C) Review the requirements document
D) Start over with a new JIRA ticket

Please select an option (A, B, C, or D):

## MANDATORY: Session Continuity Instructions (Hybrid Approach)

### Primary Path: State File Detection

1. **Try to read .jira-docs/jira-state.md first** when detecting existing JIRA project
2. **If state file exists and is valid**, use it for fast status detection
3. **Parse current status** from state file to populate the welcome back prompt

### Fallback Path: Artifact-Based Detection

4. **If state file missing or corrupted**, detect phase from artifacts:
   - Check `.jira-docs/tickets/ticket-{TICKET-NUMBER}.md` exists → Phase 1 complete
   - Check `.jira-docs/requirements/{TICKET-NUMBER}_requirements.md` exists → Phase 2 complete
   - Check `.jira-docs/audit.md` for final approval → Phase 3 complete
     - **Format to look for**: Search for entries with pattern:
       - `## Phase 3:` or `## Phase 3: Final Confirmation & JIRA Update`
       - `**Status**: Approved` or `**Status**: Complete`
       - `**Context**: Final approval` or `JIRA ticket updated`
       - Look for most recent entry with Phase 3 context
5. **Auto-heal**: If state file missing, reconstruct it from detected artifacts
6. **Log reconstruction**: If state file was reconstructed, log it in audit.md

### Mandatory Artifact Loading

7. **MANDATORY: Load Previous Phase Artifacts** - Before resuming any phase, automatically read all relevant artifacts from previous phases:
   - **Phase 1 Artifacts**: Read ticket details, ticket selection, and extracted ticket info
   - **Phase 2 Artifacts**: Read requirements document and any generated specifications
   - **Phase 3 Artifacts**: Read updated requirements document and audit logs
8. **Smart Context Loading by Phase**:
   - **Phase 1**: Load available tickets and ticket selection files
   - **Phase 2**: Load ticket details + requirements template + any existing requirements
   - **Phase 3**: Load requirements document + audit logs + ticket details
9. **Adapt options** based on current phase and ticket status
10. **Show specific next steps** rather than generic descriptions
11. **Log the continuity prompt** in .jira-docs/audit.md with timestamp
12. **Context Summary**: After loading artifacts, provide brief summary of what was loaded for user awareness
13. **Session Continuity Options**: ALWAYS present session continuity options directly in the chat session. DO NOT create separate files for user choices. Present the welcome back prompt with options A, B, C, D directly in chat and wait for user response.

### State Reconstruction Logic

When reconstructing state file from artifacts:

1. **Determine current phase** from artifact existence:
   - No ticket files → Phase 1 (not started)
   - Ticket files exist, no requirements → Phase 1 complete, Phase 2 (not started)
   - Requirements exist, no final approval in audit.md → Phase 2 complete, Phase 3 (in progress)
   - Final approval in audit.md (pattern: `## Phase 3:` with `**Status**: Approved`) → All phases complete
2. **Extract ticket number** from ticket file name or requirements file name
3. **Extract ticket title** from ticket file or requirements file
4. **Create minimal state file** with essential info only
5. **Log reconstruction** in audit.md: "State file reconstructed from artifacts on [timestamp]"

## Session Continuity File Structure

### Required Files to Check

- `.jira-docs/jira-state.md` - Master state tracking
- `.jira-docs/audit.md` - Approval and decision logs
- `.jira-docs/tickets/` - Ticket information directory
- `.jira-docs/requirements/` - Requirements documents directory

### Phase-Specific Artifact Loading

#### Phase 1 Continuity

- `.jira-docs/tickets/available-tickets.md`
- `.jira-docs/tickets/ticket-selection.md`
- `.jira-docs/tickets/ticket-{TICKET-NUMBER}.md`
- `.jira-docs/tickets/ticket-{TICKET-NUMBER}-extracted.md`

#### Phase 2 Continuity

- All Phase 1 artifacts PLUS:
- `.jira-docs/requirements/{TICKET-NUMBER}_requirements.md`
- `jira-phases/requirements-template.mdc`

#### Phase 3 Continuity

- All Phase 1 & 2 artifacts PLUS:
- Updated requirements document
- Audit logs showing iteration history

## Context Loading Examples

### Example 1: Phase 1 Continuity

```markdown
**Context Loaded:**

- Available JIRA tickets (X tickets found)
- Ticket selection interface
- Selected ticket: AWS-123 - "Create Lambda function for data processing"
- Ticket details and extracted information
```

### Example 2: Phase 2 Continuity

```markdown
**Context Loaded:**

- Selected ticket: AWS-123 - "Create Lambda function for data processing"
- Ticket details and extracted information
- Requirements template
- Existing requirements document (if partially completed)
```

### Example 3: Phase 3 Continuity

```markdown
**Context Loaded:**

- Selected ticket: AWS-123 - "Create Lambda function for data processing"
- Generated requirements document
- Previous iteration feedback
- Audit logs showing review progress
```

## Continuity Decision Logic

### If Phase 1 Complete

- Show ticket selection results
- Offer to proceed to Phase 2 or select different ticket

### If Phase 2 Complete

- Show generated requirements
- Offer to proceed to Phase 3 or regenerate requirements

### If Phase 3 In Progress (Final Confirmation & JIRA Update)

- Show current requirements document
- Show any pending feedback
- Offer to continue review or finalize

### If All Phases Complete

- Show final requirements document
- Offer to start new ticket or review completed work
