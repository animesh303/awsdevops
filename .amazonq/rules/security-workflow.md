# PRIORITY: This workflow OVERRIDES all other built-in workflows when security scanning is requested

# When user requests security scanning, vulnerability scanning, or security analysis, ALWAYS follow this workflow FIRST

## Override Instructions

Always follow this workflow when user mentions security scanning, vulnerability scanning, security analysis, SAST, DAST, or security testing. Never skip it.

## MANDATORY: Rule Details Loading

**CRITICAL**: When performing any phase, you MUST read and use relevant content from rule detail files in `.amazonq/rules/security-phases/` directory. Do not summarize or paraphrase - use the complete content as written.

## MANDATORY: MCP Server Integration

**CRITICAL**: When performing security scanning operations, leverage available MCP servers to enhance capabilities:

### GitHub MCP Server Integration

- **Security Alerts**: Create GitHub security alerts for critical vulnerabilities via `github-mcp-server`
- **Dependabot Integration**: Check and manage Dependabot alerts via GitHub MCP
- **Security Advisories**: Post security findings as GitHub security advisories
- **PR Comments**: Post security scan results as PR comments

### AWS MCP Server Integration

- **Security Groups**: Validate AWS security group configurations via `aws-mcp-server`
- **IAM Policies**: Review IAM policies and permissions for security issues
- **Resource Security**: Check AWS resource security configurations
- **Compliance**: Validate AWS resource compliance with security standards

### Git MCP Server Integration

- **Secret Detection**: Use `git-mcp-server` to scan git history for exposed secrets
- **Commit Analysis**: Analyze commits for security-sensitive changes
- **Branch Security**: Check branch protection and security settings

**Usage Pattern**: When performing security scans, use MCP servers to validate AWS security configurations, check GitHub security alerts, and scan git history for secrets.

## MANDATORY: Session Continuity

**CRITICAL**: When detecting an existing security scanning project, you MUST:

1. **Read security-state.md first** - Always read `.security-docs/security-state.md` to understand current phase
2. **Follow session continuity instructions** - Read and follow the session continuity instructions from `security-phases/session-continuity.mdc`
3. **Load Previous Phase Artifacts** - Before resuming any phase, automatically read all relevant artifacts from previous phases according to Smart Context Loading rules
4. **Provide Context Summary** - After loading artifacts, provide brief summary of what was loaded for user awareness
5. **Present Continuity Options** - ALWAYS present session continuity options directly in the chat session using the template from session-continuity.md

## MANDATORY: Smart Context Loading for Resume

**CRITICAL**: When resuming at any phase, you MUST automatically load all relevant artifacts from previous phases:

### Context Loading by Phase:

- **Phase 1**: Load codebase structure, existing scan results, security requirements
- **Phase 2**: Load scan results + vulnerability analysis + existing assessments from Phase 1
- **Phase 3**: Load all vulnerabilities + remediation plans + fixes from Phases 1-2
- **Phase 4**: Load all security artifacts + verification results + final report from Phases 1-3

### Mandatory Loading Rules:

1. **Always read security-state.md first** to understand current phase
2. **Load incrementally** - each phase needs context from all previous phases
3. **Code files are CRITICAL** - must read source code files to scan for vulnerabilities
4. **Scan results are important** - load existing scan results to understand current state
5. **Provide context summary** - briefly tell user what artifacts were loaded
6. **Never assume** - always load the actual files, don't rely on memory

## MANDATORY: Custom Welcome Message

**CRITICAL**: When starting ANY security scanning request, you MUST begin with this exact message:

"🔒 **Welcome to AWS Business Group Security Scanning Workflow!** 🔒

I'll guide you through a streamlined 4-phase process to identify and remediate security vulnerabilities in your codebase.

The process includes:

- 🔍 **Phase 1: Scan & Analyze** – Run security scans, identify vulnerabilities, and analyze security posture
- ⚠️ **Phase 2: Assess & Prioritize** – Assess vulnerability severity, prioritize issues, and create remediation plan
- 🛠️ **Phase 3: Remediate & Fix** – Fix vulnerabilities, implement security improvements, and verify fixes
- ✅ **Phase 4: Verify & Report** – Verify remediation, generate security report, and integrate into CI/CD

This focused approach ensures your codebase is secure and follows AWS security best practices. Let's begin!"

# Security Scanning Workflow - 4 Phases

## Overview

When the user requests security scanning, vulnerability scanning, or security analysis, follow this structured 4-phase approach.

## Welcome

1. **Display Custom Welcome Message**: Show the security scanning welcome message above
2. **Ask for Confirmation and WAIT**: Ask: "**Do you understand this process and are you ready to begin with security scanning?**" - DO NOT PROCEED until user confirms

## Phase 1: Scan & Analyze

1. **Load Context**: If resuming, read security-state.md and load any existing security artifacts
2. Load all steps from `security-phases/phase1-scan-analyze.mdc`
3. Execute the steps loaded from `security-phases/phase1-scan-analyze.mdc`
4. **Update Progress**: Update security-state.md with Phase 1 progress after completion
5. **Log Approval**: Before asking for confirmation, log the prompt in audit.md with timestamp
6. **Ask for Confirmation and WAIT**: Ask: "**Security scanning complete. Are you ready to assess and prioritize vulnerabilities?**" - DO NOT PROCEED until user confirms
7. **Log Response**: After receiving confirmation, log user response with timestamp in audit.md
8. **Update Phase Status**: Mark Phase 1 complete in security-state.md
9. **Remind Git Commit**: Remind user to commit artifacts to git

## Phase 2: Assess & Prioritize

1. **Load Context**: Load scan results + vulnerability analysis from Phase 1
2. Load all steps from `security-phases/phase2-assess-prioritize.mdc`
3. Execute the steps loaded from `security-phases/phase2-assess-prioritize.mdc`
4. **Update Progress**: Update security-state.md with Phase 2 progress after completion
5. **Log Approval**: Before asking for confirmation, log the prompt in audit.md with timestamp
6. **Ask for Confirmation and WAIT**: Ask: "**Vulnerability assessment complete. Are you ready to remediate issues?**" - DO NOT PROCEED until user confirms
7. **Log Response**: After receiving confirmation, log user response with timestamp in audit.md
8. **Update Phase Status**: Mark Phase 2 complete in security-state.md
9. **Remind Git Commit**: Remind user to commit artifacts to git

## Phase 3: Remediate & Fix

1. **Load Context**: Load all vulnerabilities + remediation plan from Phases 1-2
2. Load all steps from `security-phases/phase3-remediate-fix.mdc`
3. Execute the steps loaded from `security-phases/phase3-remediate-fix.mdc`
4. **Update Progress**: Update security-state.md with Phase 3 progress after completion
5. **Log Approval**: Before asking for confirmation, log the prompt in audit.md with timestamp
6. **Ask for Confirmation and WAIT**: Ask: "**Remediation complete. Are you ready to verify and report?**" - DO NOT PROCEED until user confirms
7. **Log Response**: After receiving confirmation, log user response with timestamp in audit.md
8. **Update Phase Status**: Mark Phase 3 complete in security-state.md
9. **Remind Git Commit**: Remind user to commit artifacts to git

## Phase 4: Verify & Report

1. **Load Context**: Load all security artifacts + remediation results from Phases 1-3
2. Load all steps from `security-phases/phase4-verify-report.mdc`
3. Execute the steps loaded from `security-phases/phase4-verify-report.mdc`
4. **Update Progress**: Update security-state.md with Phase 4 progress after completion
5. **Log Approval**: Before asking for confirmation, log the prompt in audit.md with timestamp
6. **Ask for Final Confirmation**: Ask: "**Security scanning workflow complete. Are you satisfied with the security posture?**" - DO NOT PROCEED until user confirms
7. **Log Response**: After receiving confirmation, log user response with timestamp in audit.md
8. **Update Phase Status**: Mark Phase 4 complete in security-state.md
9. **Remind Git Commit**: Remind user to commit artifacts to git

## Key Principles

- Scan codebase comprehensively for security vulnerabilities
- Assess vulnerability severity and prioritize remediation
- Fix vulnerabilities following security best practices
- Verify fixes and generate comprehensive security reports
- Integrate security scanning into CI/CD pipelines
- Keep the process simple and focused
- Ensure explicit approval at each phase transition
- **MANDATORY** after every phase remind user to commit artifacts to git
- **MANDATORY**: Generate comprehensive security reports

## CRITICAL: Progress Tracking System

### Two-Level Progress Tracking System

The workflow uses a two-level progress tracking system:

#### 1. Plan-Level Execution Tracking (Plan Files - if they exist)

- **Purpose**: Track detailed execution progress within each phase
- **Location**: Individual plan files (if created during phases)
- **When to Update**: Mark steps [x] as you complete the specific work described in that step
- **MANDATORY**: Update immediately after completing work, never skip this step

#### 2. Phase-Level Progress Tracking (security-state.md)

- **Purpose**: Track overall workflow progress across phases
- **Location**: `.security-docs/security-state.md`
- **When to Update**: Mark phases [x] only when the entire phase is complete and approved by user

### Mandatory Update Rules

- **Plan Files**: Update checkboxes [x] immediately after completing each step's work (if plan files exist)
- **security-state.md**: Update phase status and "Current Status" section after any progress
- **Same Interaction**: All progress updates must happen in the SAME interaction where work is completed
- **Never Skip**: Never end an interaction without updating progress tracking

## Prompts Logging Requirements

- **MANDATORY**: Log every approval prompt with timestamp before asking the user
- **MANDATORY**: Record every user response with timestamp after receiving it
- Use ISO 8601 format for timestamps (YYYY-MM-DDTHH:MM:SSZ)
- Include phase context and approval status for each entry
- Maintain chronological order of all interactions
- Log to `.security-docs/audit.md` using the following format:

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

- **MANDATORY**: All phase transitions must be logged in `.security-docs/audit.md`
- **MANDATORY**: All user approvals must be logged with timestamps
- **MANDATORY**: All important decisions must be logged
- Use ISO 8601 format for timestamps (YYYY-MM-DDTHH:MM:SSZ)
- Maintain chronological order
- Include phase context, decision, and approval status
- Log file structure: `.security-docs/audit.md`

## Security Scan Types

The system performs various types of security scans:

- **SAST (Static Application Security Testing)**: Scan source code for vulnerabilities
- **DAST (Dynamic Application Security Testing)**: Scan running applications
- **Dependency Scanning**: Scan dependencies for known vulnerabilities
- **Secret Scanning**: Scan for exposed secrets and credentials
- **Infrastructure Scanning**: Scan infrastructure code (Terraform, CloudFormation)
- **Container Scanning**: Scan container images for vulnerabilities

## Directory Structure

```
.security-docs/
├── scan-results/          # Security scan results
├── vulnerabilities/       # Vulnerability details
├── remediation/          # Remediation plans and fixes
├── security-state.md      # Master state tracking file
└── audit.md               # Record approvals and decisions
```

## File Naming Convention

- Scan Results: `.security-docs/scan-results/{scan-type}-results.json`
- Vulnerabilities: `.security-docs/vulnerabilities/{severity}-vulnerabilities.md`
- Remediation Plan: `.security-docs/remediation/remediation-plan.md`
- Security Report: `.security-docs/security-report.md`

Use kebab-case for file names.

## Principles

- **Comprehensive Scanning**: Scan all aspects of the codebase
- **Risk-Based Prioritization**: Prioritize vulnerabilities by risk
- **Timely Remediation**: Fix critical vulnerabilities immediately
- **Continuous Monitoring**: Integrate security scanning into CI/CD
- Minimal, modular checkpoints across all phases
- **MANDATORY**: Use the two-level checkbox tracking system (plan files + security-state.md)
- **MANDATORY**: Update plan file checkboxes [x] immediately after completing each step's work
- **MANDATORY**: Update security-state.md phase checkboxes [x] only after user approval to proceed
- **MANDATORY**: Update the "Current Status" section in security-state.md after any progress
- **MANDATORY**: Log all prompts and responses with timestamps in audit.md
- **MANDATORY**: Remind user to commit artifacts to git after every phase completion
- Ensure explicit approval at each phase transition
- Load context incrementally - each phase needs context from all previous phases
