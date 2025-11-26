# PRIORITY: Code Review workflow overrides all other rules when code review, PR review, or code quality checks are requested.

## When to use

- User asks for code review, PR review, code analysis, or code inspection.
- Continue to use this workflow until the final review phase is completed and logged.

## Combine with shared guardrails

- Read this file together with `common-workflow-guardrails.md` for session continuity, logging, approval, and git reminders.
- Detailed steps live in `.amazonq/rules/review-phases/phaseN-*.md`. Always load the relevant file before acting.

## Welcome message (must use verbatim)

> "🔍 **AWS Business Group Code Review Workflow**  
> Phases: 1) Analyze changes 2) Review code 3) Provide feedback 4) Finalize review.  
> Confirm that you understand the process and are ready to start with Phase 1 (Analyze Changes)."

Do not advance until the user explicitly confirms.

## Phase overview

| Phase               | Detail file                                | Focus                                               | Required prompt                            |
| ------------------- | ------------------------------------------ | --------------------------------------------------- | ------------------------------------------ |
| 1. Analyze Changes  | `review-phases/phase1-analyze-changes.md`  | Understand diff scope, load PR context, draft plan. | "Analysis complete. Start code review?"    |
| 2. Review Code      | `review-phases/phase2-review-code.md`      | Deep review using standards + findings capture.     | "Code review complete. Generate feedback?" |
| 3. Provide Feedback | `review-phases/phase3-provide-feedback.md` | Produce findings, recommendations, action items.    | "Feedback generated. Finalize review?"     |
| 4. Finalize Review  | `review-phases/phase4-finalize-review.md`  | Consolidate reports, approvals, close session.      | "Code review complete. Are you satisfied?" |

Use the shared phase loop for logging, approvals, and git reminders.

## Context loading specifics

- Always read `.review-docs/review-state.md` first; reconstruct state from artifacts if needed.
- Load prior artifacts incrementally: code changes → analysis outputs → findings → reports.
- Read PR data (description, commits, comments) plus the actual code files under review—never rely on memory.
- Present a short summary of what was loaded before proceeding.

## MCP usage

- `github-mcp-server`: fetch PR metadata, commits, review comments, post findings, update labels/status, or open issues when high-severity defects exist.
- `git-mcp-server`: inspect diffs/branches, obtain commit history, and analyze conflicts before giving guidance.
- Usage order: fetch context through MCP first, then run manual/static review steps from the phase files.

## Review dimensions & artifacts

- Cover code quality, security, performance, best practices, testing, and documentation; ensure findings are categorized accordingly.
- Findings and reports live under `.review-docs/` (`findings/*.md`, `reports/review-report.md`, `action-items.md`).
- Review plan is `.review-docs/review-plan.md`; update it whenever new scope is identified.

## Language-specific standards

- Read the relevant file from `review-phases/{language}-review-standards.md` (python, nodejs, java, go, terraform, etc.) whenever that language appears.
- If the language file does not exist, create it following the existing patterns before reviewing that code.
