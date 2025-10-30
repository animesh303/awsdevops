# CICD Workflow Generation Phase 1: Detect & Plan

## Purpose

Identify what languages/infrastructure are present (Python, Terraform), summarize the planned CI/CD workflows, and ensure the plan matches repo context before proceeding.

## Steps

1. **Scan Project Root and Subdirectories:**
   - Detect any `.py` or `.tf` files to confirm the presence of Python and/or Terraform code. List specific subpaths if possible.
2. **Identify Detected Environments:**
   - Summarize findings (e.g., "Python detected in src/; Terraform detected in iac/").
3. **Draft Workflow Plan:**
   - List which GitHub Actions workflow files will be generated (e.g., `python-ci.yml`, `terraform-ci.yml`). For each, list main CI jobs (setup, lint, test, SARIF scan/upload).
4. **User Plan Review Checkpoint:**
   - Present summary of detected environments and draft plan. Ask: "Proceed to generate workflow files as planned?" Wait for confirmation to proceed.
5. **Persist Phase Results (State & Audit):**
   - Write detected environments and the draft plan to `.cicd-docs/cicd-state.md` (preferred). If not present, use legacy `.amazonq/rules/cicd-phases/cicd-state.md`.
   - Record the user confirmation decision with timestamp in `.cicd-docs/audit.md`.
