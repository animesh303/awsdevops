# CICD Workflow Generation Phase 3: Review & Confirm

## Purpose

Provide the user with final review of the generated CI/CD workflow files and their key steps before confirming integration.

## Steps

1. **Review Generated Workflows:**
   - Display summary table: file names, environments, and main jobs/steps in each generated YAML.
   - Show actual YAML content for each workflow file.
   - Present generated artifacts for review when available:
     - Python: Flake8 SARIF, Bandit SARIF, test reports/coverage artifacts
     - Terraform: Checkov SARIF, `tflint` output, Terraform plan artifact
   - Provide quick highlights (e.g., counts of findings from SARIF where available)
2. **User Confirmation:**
   - Ask user: "Approve integration of these workflow files and settings?"
   - On positive confirmation, proceed to save/workflows to repo.
   - On decline, permit user to abort or suggest edits.
3. **Finalization:**
   - After approval, mark workflow as integrated.
   - Optionally log/record outcome as needed.
