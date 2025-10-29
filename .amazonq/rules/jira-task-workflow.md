# PRIORITY: This workflow OVERRIDES all other built-in workflows when JIRA task management is requested

# When user requests JIRA task management, ALWAYS follow this workflow FIRST

## Override Instructions

Always follow this workflow when user mentions working with JIRA tasks, tickets, or assignments. Never skip it.

## MANDATORY: Rule Details Loading

**CRITICAL**: When performing any phase, you MUST read and use relevant content from rule detail files in `.amazonq/rules/jira-phases/` directory. Do not summarize or paraphrase - use the complete content as written.

## MANDATORY: Session Continuity

**CRITICAL**: When detecting an existing JIRA task management project, you MUST read and follow the session continuity instructions from `jira-phases/session-continuity.md` before proceeding with any phase.

## MANDATORY: Custom Welcome Message

**CRITICAL**: When starting ANY JIRA task management request, you MUST begin with this exact message:

"🎯 **Welcome to Accenture AWS Business Group JIRA Task Management!** 🎯

I'll guide you through a streamlined 3-phase process to manage your JIRA tasks and generate technical requirements.

The process includes:

- 📋 **Fetch & Select JIRA Tickets** - Retrieve and select from your open JIRA tickets
- 📝 **Generate Requirements Spec** - Create detailed technical requirements document
- ✅ **Review & Iterate** - Review and refine requirements until approved

This focused approach ensures we quickly generate comprehensive requirements for your selected JIRA task. Let's begin!"

# JIRA Task Management Workflow - 3 Phases

## Overview

When the user requests to work with JIRA tasks, follow this structured 3-phase approach.

## Welcome

1. **Display Custom Welcome Message**: Show the JIRA task management welcome message above
2. **Ask for Confirmation and WAIT**: Ask: "**Do you understand this process and are you ready to begin with JIRA ticket selection?**" - DO NOT PROCEED until user confirms

## Phase 1: Fetch & Select JIRA Tickets

1. Load all steps from `jira-phases/phase1-fetch-select-tickets.md`
2. Execute the steps loaded from `jira-phases/phase1-fetch-select-tickets.md`
3. **Ask for Confirmation and WAIT**: Ask: "**JIRA ticket selected. Are you ready to generate technical requirements?**" - DO NOT PROCEED until user confirms

## Phase 2: Generate Requirements Spec

1. Load all steps from `jira-phases/phase2-generate-requirements.md`
2. Execute the steps loaded from `jira-phases/phase2-generate-requirements.md`
3. **Ask for Confirmation and WAIT**: Ask: "**Requirements generated. Are you ready to review and iterate?**" - DO NOT PROCEED until user confirms

## Phase 3: Review & Iterate

1. Load all steps from `jira-phases/phase3-review-iterate.md`
2. Execute the steps loaded from `jira-phases/phase3-review-iterate.md`
3. **Ask for Final Confirmation**: Ask: "**Requirements specification complete. Are you satisfied with the final requirements document?**" - DO NOT PROCEED until user confirms

## Key Principles

- Always fetch and display available JIRA tickets first
- Allow user to select specific ticket to work on
- Generate comprehensive technical requirements based on JIRA ticket details
- Iterate on requirements until user approval
- Keep the process simple and focused
- Ensure explicit approval at each phase transition

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
