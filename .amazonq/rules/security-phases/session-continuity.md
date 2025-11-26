
# Security Scanning Workflow Session Continuity

## Welcome Back Prompt Template

When a user returns to continue work on an existing security scanning project, present this prompt DIRECTLY IN CHAT:

**Welcome back! I can see you have an existing security scanning project in progress.**

Based on your security-state.md, here's your current status:

- **Current Phase**: [Phase X: Phase Name]
- **Vulnerabilities Found**: [X critical, Y high, Z medium]
- **Remediation Status**: [In Progress/Complete]
- **Last Completed**: [Last completed step]
- **Next Step**: [Next step to work on]

**What would you like to work on today?**

A) Continue where you left off ([Next step description])
B) Review scan results
C) Review vulnerabilities and remediation plan
D) Verify fixes
E) Start over with new security scan

Please select an option (A, B, C, D, or E):

## MANDATORY: Session Continuity Instructions

1. **Always read .security-docs/security-state.md first** when detecting existing security scanning project
2. **Parse current status** from the state file to populate the prompt
3. **MANDATORY: Load Previous Phase Artifacts** - Before resuming any phase, automatically read all relevant artifacts from previous phases:
   - **Phase 1 Artifacts**: Read scan results, vulnerability analysis
   - **Phase 2 Artifacts**: Read vulnerability assessment, prioritization, remediation plan
   - **Phase 3 Artifacts**: Read remediation fixes, updated code
   - **Phase 4 Artifacts**: Read verification results, final security report
4. **Smart Context Loading by Phase**:
   - **Phase 1**: Load codebase structure, existing scan results, security requirements
   - **Phase 2**: Load scan results + vulnerability analysis + existing assessments
   - **Phase 3**: Load all vulnerabilities + remediation plans + fixes
   - **Phase 4**: Load all security artifacts + verification results + final report
5. **Adapt options** based on current phase and security status
6. **Show specific next steps** rather than generic descriptions
7. **Log the continuity prompt** in .security-docs/audit.md with timestamp
8. **Context Summary**: After loading artifacts, provide brief summary of what was loaded for user awareness
9. **Session Continuity Options**: ALWAYS present session continuity options directly in the chat session. DO NOT create separate files for user choices. Present the welcome back prompt with options A, B, C, D, E directly in chat and wait for user response.

## Session Continuity File Structure

### Required Files to Check

- `.security-docs/security-state.md` - Master state tracking
- `.security-docs/audit.md` - Approval and decision logs
- `.security-docs/scan-results/` - Security scan results directory
- `.security-docs/vulnerabilities/` - Vulnerability details directory
- `.security-docs/remediation/` - Remediation plans directory

### Phase-Specific Artifact Loading

#### Phase 1 Continuity

- `.security-docs/scan-results/` (all scan result files)
- Codebase structure analysis
- Security scan configuration

#### Phase 2 Continuity

- All Phase 1 artifacts PLUS:
- Vulnerability assessment documents
- Prioritization and risk analysis
- Remediation plan

#### Phase 3 Continuity

- All Phase 1 & 2 artifacts PLUS:
- Remediation fixes and code changes
- Updated security configurations

#### Phase 4 Continuity

- All Phase 1-3 artifacts PLUS:
- Verification scan results
- Final security report
- Compliance status

## Context Loading Examples

### Example 1: Phase 1 Continuity

```markdown
**Context Loaded:**

- Security scan results (X vulnerabilities found)
- Scan configuration and scope
- Codebase structure analysis
- Previous scan history
```

### Example 2: Phase 2 Continuity

```markdown
**Context Loaded:**

- Scan results and vulnerability details
- Risk assessment and prioritization
- Remediation plan (X critical, Y high priority items)
- Security posture analysis
```

### Example 3: Phase 3 Continuity

```markdown
**Context Loaded:**

- All vulnerabilities and remediation plan
- Remediation fixes applied (X fixes)
- Updated code and configurations
- Remediation progress status
```

### Example 4: Phase 4 Continuity

```markdown
**Context Loaded:**

- Complete remediation fixes
- Verification scan results
- Final security report
- Compliance and security posture status
```

## Continuity Decision Logic

### If Phase 1 Complete

- Show scan results summary
- Offer to proceed to Phase 2 or re-run scans

### If Phase 2 Complete

- Show vulnerability assessment
- Offer to proceed to Phase 3 or review prioritization

### If Phase 3 In Progress

- Show remediation progress
- Offer to continue remediation or proceed to Phase 4

### If Phase 4 In Progress

- Show verification results
- Offer to continue verification or complete review

### If All Phases Complete

- Show final security report
- Offer to start new scan or review completed work
