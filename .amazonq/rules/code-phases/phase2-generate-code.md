# Phase 2: Generate Code

See `code-phases/blueprint.md#phase-2-%E2%80%93-generate-code` for the condensed checklist.

**Essentials**
- Reload the selected requirement + analysis, inspect existing IaC/app/tests, and summarize context before coding.
- Follow tool/language standards, leverage MCP servers for discovery/validation, tag resources (`JiraId`, `ManagedBy`), and capture validation logs under `.code-docs/quality-reports/`.
- Maintain `.code-docs/artifact-mappings.json` so CI/CD knows how artifacts map to IaC resources, and rerun linters/security scans until clean.
- Log the Phase‑2 prompt in `.code-docs/audit.md`, wait for approval, update `.code-docs/code-state.md`, and remind the user to commit updated code + reports.

