# PRIORITY: Security scanning workflow overrides other instructions whenever the user requests security scans, vulnerability analysis, SAST/DAST, or remediation guidance.

## When to use
- Trigger on security scanning, dependency audits, secret scanning, IAM/security posture reviews.
- Stay in this workflow through Verify & Report unless the user explicitly cancels.

## Combine with shared guardrails
- Use with `common-workflow-guardrails.md` for session continuity, approvals, and git reminders.
- Execute `.amazonq/rules/security-phases/phaseN-*.md` instructions exactly.

## Welcome message (exact text)

> "🔒 **AWS Business Group Security Workflow** – Phases:
> 1. Scan & analyze
> 2. Assess & prioritize
> 3. Remediate & fix
> 4. Verify & report
>
> Confirm you understand the process and are ready to begin Phase 1 (Scan & Analyze)."

Wait for the confirmation before Phase 1.

## Phase overview
| Phase | Detail file | Focus | Required prompt |
| --- | --- | --- | --- |
| 1. Scan & Analyze | `security-phases/phase1-scan-analyze.md` | Run SAST/DAST/dependency/secret/IaC scans, capture posture. | "Scanning complete. Assess & prioritize?" |
| 2. Assess & Prioritize | `security-phases/phase2-assess-prioritize.md` | Rate severity, map risk to assets, plan remediation. | "Assessment done. Remediate issues?" |
| 3. Remediate & Fix | `security-phases/phase3-remediate-fix.md` | Apply fixes, improve configs, verify mitigation locally. | "Remediation applied. Verify & report?" |
| 4. Verify & Report | `security-phases/phase4-verify-report.md` | Re-test, finalize reports, integrate with CI/CD/governance. | "Security workflow complete. Satisfied?" |

## Context loading highlights
- Read `.security-docs/security-state.md` at the start of every session. If missing, reconstruct via scan results, remediation files, and audit history.
- Load prior artifacts: scan outputs under `.security-docs/scan-results/`, vulnerability lists, remediation plans, and previous reports.
- Always include actual source/IaC files tied to the vulnerabilities when reviewing or fixing issues.

## MCP usage
- `github-mcp-server`: check Dependabot/security alerts, post scan results to PRs, create advisories or issues for critical findings.
- `aws-mcp-server`: inspect IAM, security groups, resource policies, and compliance posture before recommending fixes.
- `git-mcp-server`: scan history for secrets, inspect commits implicated in vulnerabilities, enforce branch protection guidance.

## Deliverables & conventions
- Store scan artifacts under `.security-docs/scan-results/{scan-type}-results.<ext>`.
- Track vulnerabilities in `.security-docs/vulnerabilities/{severity}-vulnerabilities.md` and remediation work in `.security-docs/remediation/*.md`.
- Final summary reports live at `.security-docs/security-report.md`.
- Cover scan types: SAST, DAST, dependency, secret, infrastructure, container. Specify which ran and why.
