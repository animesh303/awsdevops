# Code Generation Session Continuity

## Welcome Back Prompt Template

When a user returns to continue work on an existing code generation project, present this prompt DIRECTLY IN CHAT:

**Welcome back! I can see you have an existing code generation project in progress.**

Based on your code-state.md, here's your current status:

- **Selected Requirements**: [TICKET-NUMBER] - [REQUIREMENTS-TITLE]
- **Current Phase**: [Phase X: Phase Name]
- **Code Status**: [Generated/In Review/Approved]
- **Last Completed**: [Last completed step]
- **Next Step**: [Next step to work on]

**What would you like to work on today?**

A) Continue where you left off ([Next step description])
B) Review the selected requirements
C) Review the generated code
D) Start over with new requirements

Please select an option (A, B, C, or D):

## MANDATORY: Session Continuity Instructions

1. **Always read .code-docs/code-state.md first** when detecting existing code generation project
2. **Parse current status** from the workflow file to populate the prompt
3. **MANDATORY: Load Previous Phase Artifacts** - Before resuming any phase, automatically read all relevant artifacts from previous phases:
   - **Phase 1 Artifacts**: Read requirements selection, analysis, and IAC tool/runtime selections
   - **Phase 2 Artifacts**: Read generated code and quality reports
   - **Phase 3 Artifacts**: Read updated code, documentation, and review feedback
4. **Smart Context Loading by Phase**:
   - **Phase 1**: Load available requirements and selection files
   - **Phase 2**: Load requirements + generated code + quality reports
   - **Phase 3**: Load all code files + documentation + audit logs
5. **Adapt options** based on current phase and code status
6. **Show specific next steps** rather than generic descriptions
7. **Log the continuity prompt** in .code-docs/audit.md with timestamp
8. **Context Summary**: After loading artifacts, provide brief summary of what was loaded for user awareness
9. **Session Continuity Options**: ALWAYS present session continuity options directly in the chat session. DO NOT create separate files for user choices. Present the welcome back prompt with options A, B, C, D directly in chat and wait for user response.

## Session Continuity File Structure

### Required Files to Check

- `.code-docs/code-state.md` - Master state tracking
- `.code-docs/audit.md` - Approval and decision logs
- `.code-docs/requirements/` - Requirements documents directory (includes IAC tool and runtime selections)
- `iac/{iac-tool}/` - IAC code by tool (terraform, cdk, cloudformation, pulumi, etc.)
- `src/{runtime-type}-{feature-name}/` - Application code by runtime/type (lambda-python, lambda-nodejs, container-\*, etc.)

### Phase-Specific Artifact Loading

#### Phase 1 Continuity

- `.code-docs/requirements/available-requirements.md`
- `.code-docs/requirements/requirements-selection.md`
- `.code-docs/requirements/{TICKET-NUMBER}_requirements.md`
- `.code-docs/requirements/{TICKET-NUMBER}-analysis.md`

#### Phase 2 Continuity

- All Phase 1 artifacts PLUS:
- IAC tool and runtime selections from analysis document
- `iac/{iac-tool}/` (all IAC files for selected tool)
- `src/{runtime-type}-{feature-name}/` (all application code files by runtime)
- `.code-docs/quality-reports/` (quality check results)

#### Phase 3 Continuity

- All Phase 1 & 2 artifacts PLUS:
- Updated code files
- Documentation files
- Review feedback and audit logs

## Context Loading Examples

### Example 1: Phase 1 Continuity

```markdown
**Context Loaded:**

- Available requirements (X requirements found)
- Requirements selection interface
- Selected requirements: AWS-123 - "Create Lambda function for data processing"
- Requirements analysis and technical specifications
```

### Example 2: Phase 2 Continuity

```markdown
**Context Loaded:**

- Selected requirements: AWS-123 - "Create Lambda function for data processing"
- Selected IAC tool: [terraform/cdk/cloudformation/pulumi]
- Selected runtime: [lambda-python/lambda-nodejs/etc.]
- Generated IAC infrastructure code (using selected tool)
- Generated application code (using selected runtime)
- Quality reports
- Security and best practices implementation
```

### Example 3: Phase 3 Continuity

```markdown
**Context Loaded:**

- Selected requirements: AWS-123 - "Create Lambda function for data processing"
- Generated and updated code files
- Code quality reports
- Documentation and review feedback
- Previous iteration changes
```

## Continuity Decision Logic

### If Phase 1 Complete

- Show requirements selection results
- Offer to proceed to Phase 2 or select different requirements

### If Phase 2 Complete

- Show generated code and quality reports
- Offer to proceed to Phase 3 or regenerate code

### If Phase 3 In Progress

- Show current code and any pending feedback
- Offer to continue review or finalize

### If All Phases Complete

- Show final implementation
- Offer to start new requirements or review completed work
