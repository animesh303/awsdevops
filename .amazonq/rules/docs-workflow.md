# PRIORITY: Documentation workflow overrides other rules when the user requests documentation, README/API docs, architecture notes, or any technical writing deliverable.

## When to use
- Trigger on documentation, doc generation, changelog/release notes, or writing guidance.
- Stay in this workflow through the Publish & Integrate phase.

## Combine with shared guardrails
- Use this file with `common-workflow-guardrails.md` (for session continuity, logging, approvals, git reminders).
- Execute the detailed instructions in `.amazonq/rules/docs-phases/phaseN-*.md` verbatim.

## Welcome message (exact text)
> "📚 **AWS Business Group Documentation Workflow**  
> Phases: 1) Analyze & plan 2) Generate docs 3) Review & refine 4) Publish & integrate.  
> Confirm you understand the workflow and are ready to start Phase 1 (Analyze & Plan)."

Do not continue until the user confirms.

## Phase overview
| Phase | Detail file | Focus | Required prompt |
| --- | --- | --- | --- |
| 1. Analyze & Plan | `docs-phases/phase1-analyze-plan.md` | Audit existing docs, define audiences, build doc plan. | "Planning complete. Generate docs?" |
| 2. Generate Documentation | `docs-phases/phase2-generate-docs.md` | Write README/API/architecture/content per plan. | "Draft docs ready. Review & refine?" |
| 3. Review & Refine | `docs-phases/phase3-review-refine.md` | Edit for clarity, accuracy, completeness, QA checklists. | "Review done. Publish & integrate?" |
| 4. Publish & Integrate | `docs-phases/phase4-publish-integrate.md` | Final approvals, publishing, repo/CI hooks. | "Documentation workflow complete. Satisfied?" |

## Context loading highlights
- Read `.docs-docs/docs-state.md` before each session; reconstruct state from `.docs-docs/` artifacts if missing.
- Load any existing plans, drafts, READMEs, architecture docs, and code files referenced by the documentation.
- When resuming, summarize which documents were pulled in (plan, drafts, reviews, etc.).

## MCP usage
- `github-mcp-server`: open/update doc PRs, post release notes, sync wiki pages, open issues for doc follow-ups.
- `git-mcp-server`: branch + commit doc updates, compare doc revisions.
- Use MCP tooling before editing so the doc set reflects the current repository.

## Documentation deliverables
- Plans live in `.docs-docs/docs-plan.md`; drafts and generated files belong in `.docs-docs/generated/` until finalized.
- Repo-facing outputs go into `docs/` (api, architecture, guides) plus top-level `README.md`.
- Follow kebab-case naming for new files (e.g., `docs/guides/onboarding-guide.md`).
- Capture doc types: README, API reference (OpenAPI or markdown), architecture notes, user/developer guides, inline comments/docstrings as specified by the phase files.
