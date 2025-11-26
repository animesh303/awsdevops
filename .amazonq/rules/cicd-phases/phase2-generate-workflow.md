# Phase 2: Generate Workflow

Reference `cicd-phases/blueprint.md#phase-2-%E2%80%93-generate-workflow` for the full checklist.

**Highlights**
- Reload the detection plan, artifact mapping, requirements, and existing workflows. Summarize the context for the user.
- Author a single `.github/workflows/ci-cd.yml` triggered by `push` to `main` + `workflow_dispatch`, adding lint/scan/test/build/deploy jobs per code type, `needs:` for ordering, and `environment: production` on deploy steps.
- Apply standards (`cicd-phases/{code-type}-standards.md`), secrets, permissions, artifact uploads/downloads, and run validations from `workflow-lint-validation.md`.
- Log the Phase‑2 prompt in `.cicd-docs/audit.md`, wait for approval, update `.cicd-docs/cicd-state.md`, and remind the user to commit the workflow + docs.

