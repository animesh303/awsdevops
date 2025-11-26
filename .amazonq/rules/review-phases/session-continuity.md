# Code Review Workflow Session Continuity

## Welcome Back Prompt Template

When a user returns to continue work on an existing code review project, present this prompt DIRECTLY IN CHAT:

**Welcome back! I can see you have an existing code review project in progress.**

Based on your review-state.md, here's your current status:

- **Current Phase**: [Phase X: Phase Name]
- **Files Under Review**: [List of files]
- **Issues Found**: [X issues by category]
- **Review Status**: [In Progress/Changes Requested/Approved]
- **Last Completed**: [Last completed step]
- **Next Step**: [Next step to work on]

**What would you like to work on today?**

A) Continue where you left off ([Next step description])
B) Review the code changes
C) Review findings and feedback
D) Update action items
E) Start over with new code review

Please select an option (A, B, C, D, or E):

## MANDATORY: Session Continuity Instructions

1. **Always read .review-docs/review-state.md first** when detecting existing code review project
2. **Parse current status** from the state file to populate the prompt
3. **MANDATORY: Load Previous Phase Artifacts** - Before resuming any phase, automatically read all relevant artifacts from previous phases:
   - **Phase 1 Artifacts**: Read code changes, review plan, change analysis
   - **Phase 2 Artifacts**: Read review findings, code analysis results
   - **Phase 3 Artifacts**: Read feedback, recommendations, action items
   - **Phase 4 Artifacts**: Read review summary, final report, action items tracking
4. **Smart Context Loading by Phase**:
   - **Phase 1**: Load code changes, PR context, existing review artifacts
   - **Phase 2**: Load code analysis + review plan + existing reviews
   - **Phase 3**: Load all review findings + recommendations + feedback
   - **Phase 4**: Load all review artifacts + action items + final report
5. **Adapt options** based on current phase and review status
6. **Show specific next steps** rather than generic descriptions
7. **Log the continuity prompt** in .review-docs/audit.md with timestamp
8. **Context Summary**: After loading artifacts, provide brief summary of what was loaded for user awareness
9. **Session Continuity Options**: ALWAYS present session continuity options directly in the chat session. DO NOT create separate files for user choices. Present the welcome back prompt with options A, B, C, D, E directly in chat and wait for user response.

## Session Continuity File Structure

### Required Files to Check

- `.review-docs/review-state.md` - Master state tracking
- `.review-docs/audit.md` - Approval and decision logs
- `.review-docs/review-plan.md` - Review strategy and plan
- `.review-docs/findings/` - Review findings directory
- Source code files being reviewed

### Phase-Specific Artifact Loading

#### Phase 1 Continuity

- `.review-docs/review-plan.md`
- Code change analysis
- PR context and commit history

#### Phase 2 Continuity

- All Phase 1 artifacts PLUS:
- Review findings in `.review-docs/findings/`
- Code analysis results

#### Phase 3 Continuity

- All Phase 1 & 2 artifacts PLUS:
- Feedback documents
- Recommendations and action items

#### Phase 4 Continuity

- All Phase 1-3 artifacts PLUS:
- Review summary and final report
- Action items tracking

## Context Loading Examples

### Example 1: Phase 1 Continuity

```markdown
**Context Loaded:**

- Code changes (X files changed, Y lines added/deleted)
- Review plan and scope
- PR context and commit history
- Change analysis summary
```

### Example 2: Phase 2 Continuity

```markdown
**Context Loaded:**

- Code changes and review plan
- Review findings (X code quality, Y security, Z performance issues)
- Code analysis results
- Review progress status
```

### Example 3: Phase 3 Continuity

```markdown
**Context Loaded:**

- All review findings
- Feedback and recommendations
- Action items (X items)
- Review status and next steps
```

### Example 4: Phase 4 Continuity

```markdown
**Context Loaded:**

- Complete review findings and feedback
- Review summary and final report
- Action items tracking
- Review completion status
```

## Continuity Decision Logic

### If Phase 1 Complete

- Show code change analysis
- Offer to proceed to Phase 2 or re-analyze changes

### If Phase 2 Complete

- Show review findings summary
- Offer to proceed to Phase 3 or review findings in detail

### If Phase 3 In Progress

- Show feedback and action items
- Offer to continue feedback generation or proceed to Phase 4

### If Phase 4 In Progress

- Show review summary and action items
- Offer to continue finalization or complete review

### If All Phases Complete

- Show final review report
- Offer to start new review or review completed work
