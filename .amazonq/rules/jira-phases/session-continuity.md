# JIRA Task Management Session Continuity

## Welcome Back Prompt Template

When a user returns to continue work on an existing JIRA task management project, present this prompt:

```markdown
**Welcome back! I can see you have an existing JIRA task management project in progress.**

Based on your jira-state.md, here's your current status:

- **Selected Ticket**: [TICKET-NUMBER] - [TICKET-TITLE]
- **Current Phase**: [Phase X: Phase Name]
- **Requirements Status**: [Generated/In Review/Approved]
- **Last Completed**: [Last completed step]
- **Next Step**: [Next step to work on]

**What would you like to work on today?**

A) Continue where you left off ([Next step description])
B) Review the selected JIRA ticket details
C) Review the requirements document
D) Start over with a new JIRA ticket

[Answer]:
```

## MANDATORY: Session Continuity Instructions

1. **Always read jira-state.md first** when detecting existing JIRA project
2. **Parse current status** from the workflow file to populate the prompt
3. **MANDATORY: Load Previous Phase Artifacts** - Before resuming any phase, automatically read all relevant artifacts from previous phases:
   - **Phase 1 Artifacts**: Read ticket details, ticket selection, and extracted ticket info
   - **Phase 2 Artifacts**: Read requirements document and any generated specifications
   - **Phase 3 Artifacts**: Read updated requirements document and audit logs
4. **Smart Context Loading by Phase**:
   - **Phase 1**: Load available tickets and ticket selection files
   - **Phase 2**: Load ticket details + requirements template + any existing requirements
   - **Phase 3**: Load requirements document + audit logs + ticket details
5. **Adapt options** based on current phase and ticket status
6. **Show specific next steps** rather than generic descriptions
7. **Log the continuity prompt** in audit.md with timestamp
8. **Context Summary**: After loading artifacts, provide brief summary of what was loaded for user awareness
9. **Asking questions**: ALWAYS ask clarification or user feedback questions by placing them in .md files. DO NOT place the multiple-choice questions in-line in the chat session.

## Session Continuity File Structure

### Required Files to Check

- `jira-docs/jira-state.md` - Master state tracking
- `jira-docs/audit.md` - Approval and decision logs
- `jira-docs/tickets/` - Ticket information directory
- `jira-docs/requirements/` - Requirements documents directory

### Phase-Specific Artifact Loading

#### Phase 1 Continuity

- `jira-docs/tickets/available-tickets.md`
- `jira-docs/tickets/ticket-selection.md`
- `jira-docs/tickets/ticket-{TICKET-NUMBER}.md`
- `jira-docs/tickets/ticket-{TICKET-NUMBER}-extracted.md`

#### Phase 2 Continuity

- All Phase 1 artifacts PLUS:
- `jira-docs/requirements/{TICKET-NUMBER}_requirements.md`
- `jira-phases/requirements-template.md`

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

### If Phase 3 In Progress

- Show current requirements document
- Show any pending feedback
- Offer to continue review or finalize

### If All Phases Complete

- Show final requirements document
- Offer to start new ticket or review completed work
