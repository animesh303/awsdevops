# Testing Workflow Session Continuity

## Welcome Back Prompt Template

When a user returns to continue work on an existing testing project, present this prompt DIRECTLY IN CHAT:

**Welcome back! I can see you have an existing testing project in progress.**

Based on your test-state.md, here's your current status:

- **Current Phase**: [Phase X: Phase Name]
- **Code Types**: [List detected languages/frameworks]
- **Tests Generated**: [X unit, Y integration, Z E2E tests]
- **Coverage Achieved**: XX%
- **Last Completed**: [Last completed step]
- **Next Step**: [Next step to work on]

**What would you like to work on today?**

A) Continue where you left off ([Next step description])
B) Review the test plan
C) Review generated tests
D) Execute tests and view results
E) Start over with new test analysis

Please select an option (A, B, C, D, or E):

## MANDATORY: Session Continuity Instructions

1. **Always read .test-docs/test-state.md first** when detecting existing testing project
2. **Parse current status** from the state file to populate the prompt
3. **MANDATORY: Load Previous Phase Artifacts** - Before resuming any phase, automatically read all relevant artifacts from previous phases:
   - **Phase 1 Artifacts**: Read test plan, codebase analysis, test requirements
   - **Phase 2 Artifacts**: Read generated test files and test structure
   - **Phase 3 Artifacts**: Read test execution results and coverage reports
   - **Phase 4 Artifacts**: Read review feedback and integration status
4. **Smart Context Loading by Phase**:
   - **Phase 1**: Load codebase structure, existing test files, test requirements
   - **Phase 2**: Load test plan + codebase analysis + existing tests
   - **Phase 3**: Load all test files + test execution results + coverage reports
   - **Phase 4**: Load all test artifacts + quality reports + review feedback
5. **Adapt options** based on current phase and test status
6. **Show specific next steps** rather than generic descriptions
7. **Log the continuity prompt** in .test-docs/audit.md with timestamp
8. **Context Summary**: After loading artifacts, provide brief summary of what was loaded for user awareness
9. **Session Continuity Options**: ALWAYS present session continuity options directly in the chat session. DO NOT create separate files for user choices. Present the welcome back prompt with options A, B, C, D, E directly in chat and wait for user response.

## Session Continuity File Structure

### Required Files to Check

- `.test-docs/test-state.md` - Master state tracking
- `.test-docs/audit.md` - Approval and decision logs
- `.test-docs/test-plan.md` - Test strategy and plan
- `tests/` - Test files directory
- `src/` or `iac/` - Source code directories

### Phase-Specific Artifact Loading

#### Phase 1 Continuity

- `.test-docs/test-plan.md`
- Codebase structure analysis
- Existing test files inventory

#### Phase 2 Continuity

- All Phase 1 artifacts PLUS:
- Generated test files in `tests/unit/`, `tests/integration/`, `tests/e2e/`
- Test framework configuration files

#### Phase 3 Continuity

- All Phase 1 & 2 artifacts PLUS:
- Test execution results
- Coverage reports in `.test-docs/coverage-reports/`
- Test quality metrics

#### Phase 4 Continuity

- All Phase 1-3 artifacts PLUS:
- Review feedback
- CI/CD integration status
- Final test reports

## Context Loading Examples

### Example 1: Phase 1 Continuity

```markdown
**Context Loaded:**

- Codebase analysis (X Python files, Y TypeScript files, Z Terraform files)
- Test plan document
- Existing test inventory (X unit tests, Y integration tests)
- Test requirements identified
```

### Example 2: Phase 2 Continuity

```markdown
**Context Loaded:**

- Test plan and strategy
- Codebase analysis
- Generated unit tests (X files)
- Generated integration tests (Y files)
- Generated E2E tests (Z files)
- Test framework configurations
```

### Example 3: Phase 3 Continuity

```markdown
**Context Loaded:**

- All generated test files
- Test execution results (X passed, Y failed)
- Coverage reports (XX% coverage)
- Test quality metrics
- Performance test results
```

### Example 4: Phase 4 Continuity

```markdown
**Context Loaded:**

- All test files and execution results
- Coverage reports (XX% final coverage)
- Review feedback and refinements
- CI/CD integration status
- Final test quality report
```

## Continuity Decision Logic

### If Phase 1 Complete

- Show test plan and requirements
- Offer to proceed to Phase 2 or regenerate plan

### If Phase 2 Complete

- Show generated test files
- Offer to proceed to Phase 3 or regenerate tests

### If Phase 3 In Progress

- Show test execution results and coverage
- Offer to continue validation or proceed to Phase 4

### If Phase 4 In Progress

- Show review feedback and integration status
- Offer to continue review or finalize

### If All Phases Complete

- Show final test suite and coverage
- Offer to start new test analysis or review completed work
