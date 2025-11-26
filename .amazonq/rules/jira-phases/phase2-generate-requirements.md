# Phase 2: Generate Requirements

Follow `jira-phases/blueprint.md#phase-2-%E2%80%93-generate-requirements`.

**Essentials**
- Analyze the selected ticket, capture ambiguities as questions, and draft `.jira-docs/requirements/{KEY}_requirements.md` using the standard template (no assumptions; unanswered items live in **Open Questions** with `[Answer]:` placeholders).
- Generate an AWS architecture diagram (via `mcp_awsdac`) whenever the ticket contains enough detail, embed it in the doc, and store the PNG beside the requirements file.
- Block progress until all **blocking** questions are answered, then log approval, create/update the Confluence page via Atlassian MCP, and store the page metadata for Phase 3.
- Update `jira-state.md`, log everything in `.jira-docs/audit.md`, and remind the user to commit the requirements artifacts (doc, diagram, state).

