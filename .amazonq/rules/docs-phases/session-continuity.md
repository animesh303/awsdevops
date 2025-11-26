# Documentation Workflow Session Continuity

## Welcome Back Prompt Template

When a user returns to continue work on an existing documentation project, present this prompt DIRECTLY IN CHAT:

**Welcome back! I can see you have an existing documentation project in progress.**

Based on your docs-state.md, here's your current status:

- **Current Phase**: [Phase X: Phase Name]
- **Documentation Types**: [API/README/Architecture/Code Docs]
- **Docs Generated**: [X documentation files]
- **Documentation Status**: [In Progress/Complete]
- **Last Completed**: [Last completed step]
- **Next Step**: [Next step to work on]

**What would you like to work on today?**

A) Continue where you left off ([Next step description])
B) Review the documentation plan
C) Review generated documentation
D) Publish documentation
E) Start over with new documentation analysis

Please select an option (A, B, C, D, or E):

## MANDATORY: Session Continuity Instructions

1. **Always read .docs-docs/docs-state.md first** when detecting existing documentation project
2. **Parse current status** from the state file to populate the prompt
3. **MANDATORY: Load Previous Phase Artifacts** - Before resuming any phase, automatically read all relevant artifacts from previous phases:
   - **Phase 1 Artifacts**: Read documentation plan, codebase analysis, documentation requirements
   - **Phase 2 Artifacts**: Read generated documentation files
   - **Phase 3 Artifacts**: Read review feedback, refined documentation
   - **Phase 4 Artifacts**: Read published documentation, integration status
4. **Smart Context Loading by Phase**:
   - **Phase 1**: Load codebase structure, existing documentation, documentation requirements
   - **Phase 2**: Load documentation plan + codebase analysis + existing docs
   - **Phase 3**: Load all generated documentation + review feedback
   - **Phase 4**: Load all documentation artifacts + final review + integration status
5. **Adapt options** based on current phase and documentation status
6. **Show specific next steps** rather than generic descriptions
7. **Log the continuity prompt** in .docs-docs/audit.md with timestamp
8. **Context Summary**: After loading artifacts, provide brief summary of what was loaded for user awareness
9. **Session Continuity Options**: ALWAYS present session continuity options directly in the chat session. DO NOT create separate files for user choices. Present the welcome back prompt with options A, B, C, D, E directly in chat and wait for user response.

## Session Continuity File Structure

### Required Files to Check

- `.docs-docs/docs-state.md` - Master state tracking
- `.docs-docs/audit.md` - Approval and decision logs
- `.docs-docs/docs-plan.md` - Documentation strategy and plan
- `docs/` - Documentation directory
- `README.md` - Main project README

### Phase-Specific Artifact Loading

#### Phase 1 Continuity

- `.docs-docs/docs-plan.md`
- Codebase structure analysis
- Existing documentation inventory

#### Phase 2 Continuity

- All Phase 1 artifacts PLUS:
- Generated documentation files in `docs/`
- API documentation files
- Architecture documentation

#### Phase 3 Continuity

- All Phase 1 & 2 artifacts PLUS:
- Review feedback and refinements
- Updated documentation files

#### Phase 4 Continuity

- All Phase 1-3 artifacts PLUS:
- Published documentation
- Integration status
- Documentation maintenance plan

## Context Loading Examples

### Example 1: Phase 1 Continuity

```markdown
**Context Loaded:**

- Documentation plan and strategy
- Codebase analysis (X APIs, Y components)
- Existing documentation inventory
- Documentation requirements
```

### Example 2: Phase 2 Continuity

```markdown
**Context Loaded:**

- Documentation plan and requirements
- Generated API documentation (X files)
- Generated README and guides (Y files)
- Architecture documentation
```

### Example 3: Phase 3 Continuity

```markdown
**Context Loaded:**

- All generated documentation
- Review feedback and refinements
- Updated documentation files
- Documentation quality assessment
```

### Example 4: Phase 4 Continuity

```markdown
**Context Loaded:**

- Complete documentation suite
- Published documentation status
- Integration into project structure
- Documentation maintenance plan
```

## Continuity Decision Logic

### If Phase 1 Complete

- Show documentation plan
- Offer to proceed to Phase 2 or regenerate plan

### If Phase 2 Complete

- Show generated documentation summary
- Offer to proceed to Phase 3 or regenerate docs

### If Phase 3 In Progress

- Show review feedback and refinements
- Offer to continue review or proceed to Phase 4

### If Phase 4 In Progress

- Show publication status
- Offer to continue publishing or complete review

### If All Phases Complete

- Show final documentation suite
- Offer to start new documentation or review completed work
