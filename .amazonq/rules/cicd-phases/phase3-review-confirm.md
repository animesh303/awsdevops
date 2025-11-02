# CICD Workflow Generation Phase 3: Review & Confirm

## Purpose

Provide the user with final review of the generated CI/CD workflow files and their key steps before confirming they are ready for commit and push (which happens in Phase 4).

## Steps

1. **Review Generated Workflows:**

   - Display summary table: file names, environments, and main jobs/steps in each generated YAML.
   - Show actual YAML content for each workflow file.
   - Present generated artifacts for review when available:
     - Python: Flake8 SARIF, Bandit SARIF, test reports/coverage artifacts
     - Terraform: Checkov SARIF, `tflint` output, Terraform plan artifact
   - Provide quick highlights (e.g., counts of findings from SARIF where available)
   - Use clickable file links (preferably `@filename` syntax for Cursor, or relative/absolute paths) when presenting workflow file paths for review

2. **User Confirmation:**
   - Ask user: "Are these workflow files ready for commit and push to the repository?"
   - On positive confirmation, proceed to Phase 4 (Commit & Push Changes).
   - On decline, permit user to abort or suggest edits to the workflows before proceeding to Phase 4.

**Note:** This phase is for review and approval only. Actual commit, push, and finalization occur in Phase 4.
