# Code Generation Phase Blueprint

Use this file as the single reference for all code-phases steps. The individual `phaseX-*.md` files now point here.

## Phase 1 – Select Requirements
**Goal:** choose a requirement, capture technical decisions, and prepare for build work.  
**Outputs:** `available-requirements.md`, `requirements-selection.md`, `{TICKET}_requirements.md`, `{TICKET}-analysis.md`, updated `code-state.md`.

**Checklist**
1. Verify `.jira-docs/requirements/` exists; if empty, instruct the user to finish the JIRA workflow first.
2. List available tickets (id, title, summary) and store the list in `.code-docs/requirements/available-requirements.md`.
3. Present options in chat, capture the user’s selection, copy the chosen file into `.code-docs/requirements/{TICKET}_requirements.md`, and extract key details into `{TICKET}-analysis.md`.
4. Decide on the IAC tool and runtime/language; document the reasoning, confirm the relevant standards files exist, and flag any gaps.
5. Generate a kebab-case feature name plus tags (`JiraId`, `ManagedBy`) and update `code-state.md`. Log the Phase‑1 approval prompt in `.code-docs/audit.md` and wait for confirmation.

## Phase 2 – Generate Code
**Goal:** implement IaC, application code, and supporting assets that satisfy the requirement.  
**Outputs:** new/updated `iac/{tool}/`, `src/{runtime-feature}/`, `tests/{feature}/`, `.code-docs/artifact-mappings.json`, quality reports, updated `code-state.md`.

**Checklist**
1. Reload requirement + analysis docs, inspect existing code, and summarize context.
2. Implement IaC following `code-phases/{iac-tool}-standards.md`, using MCP servers (`aws`, `terraform`) for discovery, validation, and tagging. Capture validation logs under `.code-docs/quality-reports/`.
3. Implement application code/tests following `code-phases/{language}-standards.md`; include dependency manifests, environment configuration, and error handling.
4. Build/update `.code-docs/artifact-mappings.json` so CI/CD knows how artifacts relate to IaC resources.
5. Run linters, security scans, and tooling validations; store outputs in `quality-reports/`. Log the Phase‑2 prompt in `.code-docs/audit.md`, wait for approval, update `code-state.md`, and remind the user to commit artifacts.

## Phase 3 – Review & Refine
**Goal:** iterate on the generated code until it meets quality expectations.  
**Outputs:** resolved issues, updated docs (README/deployment guide/troubleshooting), refreshed quality reports.

**Checklist**
1. Re-run lint/test/security checks; present key findings and clickable file links for review.
2. Capture user feedback, make targeted updates (IaC, app code, tests, docs), and rerun validations after each iteration.
3. Store documentation (README, deploy steps, env vars, troubleshooting) under `.code-docs/documentation/{feature}/`.
4. Log the Phase‑3 prompt in `.code-docs/audit.md`, wait for user approval, update `code-state.md`, and remind them to commit artifacts.

## Phase 4 – Commit & Push (Optional)
**Goal:** commit/push changes only when the user explicitly authorizes it.  
**Outputs:** git commit + push (if approved) or documented manual steps (if declined).

**Checklist**
1. Ask: “Do you want me to commit and push the generated code changes now?” and proceed only on approval.
2. Ensure git identity exists, stage changes, craft a structured commit message (`feat(codegen): …`, `Refs: {TICKET}`), and push to the active branch.
3. If the user declines or push fails, provide clear next steps. Always log the interaction in `.code-docs/audit.md` and update `code-state.md`.

