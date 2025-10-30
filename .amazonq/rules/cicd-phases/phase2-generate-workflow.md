# CICD Workflow Generation Phase 2: Generate Workflow Files

## Purpose

Render GitHub Actions workflow files (YAML) matched to detected code environments, ensuring all required CI/CD and code scanning steps are present, and provide user with a content preview.

## Steps

1. **Generate Workflows Per Detected Language/Tool:**

   - For each detected (Python/Terraform), generate corresponding `.github/workflows/{language}-ci.yml` file.
   - Workflows that upload SARIF results MUST declare permissions with at least:

     - Top-level or job-level `permissions` including `security-events: read`
     - Example (top-level):

       ```yaml
       permissions:
         contents: read
         security-events: read
       ```

2. **Python Workflow Jobs:**
   - Matrix build (3.10, 3.11, 3.12)
   - Setup Python with caching; install dependencies (`requirements.txt` if found)
   - Lint: Run Flake8 with SARIF output
   - Security: Run Bandit with SARIF output
   - Tests: If `tests/` exists, run `pytest` with coverage and upload report as artifact
   - Ensure SARIF files exist before upload; fail the job if missing
   - Upload SARIF using `github/codeql-action/upload-sarif@v3` (requires `security-events: read` permissions)
3. **Terraform Workflow Jobs:**
   - Pin Terraform version; cache plugins
   - `terraform fmt -check`, `init`, `validate`, and `plan`
   - Lint: Run `tflint`
   - Security: Run Checkov with SARIF output and write to `iac/terraform/checkov-results.sarif` (example: `checkov -d iac/terraform -o sarif > iac/terraform/checkov-results.sarif`)
   - Ensure `iac/terraform/checkov-results.sarif` exists before upload; fail if missing
   - Upload SARIF using `github/codeql-action/upload-sarif@v3` (requires `security-events: read` permissions)
   - Upload Terraform plan as artifact
4. **Present Workflow YAML Preview:**
   - Show actual (or summarized) YAML file contents to user
5. **Checkpoint:**
   - Prompt user to confirm: "Proceed to review and finalize workflow files?" Wait for confirmation.
