# CICD Workflow Generation Phase 2: Generate Workflow Files

## Purpose

Render GitHub Actions workflow files (YAML) matched to detected code environments, ensuring all required CI/CD and code scanning steps are present. Generate a comprehensive set of workflows covering Continuous Integration (CI) and Continuous Delivery (CD) to `dev`, `test`, and `prod` with explicit dependencies between stages. Provide a content preview.

## Steps

1. **Generate Workflows Per Detected Language/Tool:**

   - For each detected (Python/Terraform), generate a CI workflow and separate CD workflows per environment:
     - CI: `.github/workflows/{stack}-ci.yml`
     - CD: `.github/workflows/{stack}-deploy-dev.yml`, `.github/workflows/{stack}-deploy-test.yml`, `.github/workflows/{stack}-deploy-prod.yml`
   - Organize workflow logic into multiple jobs with clear dependencies using `needs:`; avoid one giant job. Prefer fast-fail by running independent jobs in parallel
   - Enforce cross-workflow stage order using `workflow_run` triggers and environment gates:
     - `*-deploy-dev.yml` runs on successful completion of `{stack} CI`
     - `*-deploy-test.yml` runs on successful completion of `{stack} Deploy to dev`
     - `*-deploy-prod.yml` runs on successful completion of `{stack} Deploy to test`
   - Use GitHub `environments` (`dev`, `test`, `prod`) with protection rules/approvals for promotion gates
   - Prefer using CI-produced artifacts (e.g., Terraform plan, build artifacts, container images) and download them in CD workflows
   - Workflows that upload SARIF results MUST declare permissions with at least:

     - Top-level or job-level `permissions` including `security-events: read`
     - Example (top-level):

       ```yaml
       permissions:
         contents: read
         security-events: read
       ```

   - If a workflow uses `paths` filters under `on.push`/`on.pull_request`, always include the workflow file itself to trigger on workflow edits. Example:

     ```yaml
     on:
       push:
         branches: [main, develop]
         paths:
           - "iac/terraform/**"
           - ".github/workflows/terraform-ci.yml"
       pull_request:
         branches: [main]
         paths:
           - "iac/terraform/**"
           - ".github/workflows/terraform-ci.yml"
     ```

2. **Python Workflow Jobs:**
   - Define separate jobs (examples below) and run them in parallel when possible:
     - `python-lint` (matrix: 3.10, 3.11, 3.12): setup + Flake8 SARIF
     - `python-security` (matrix optional): setup + Bandit SARIF
     - `python-tests` (conditional on `tests/`): setup + pytest + coverage artifact
     - `python-upload-sarif`: `needs: [python-lint, python-security]`, upload SARIF files
   - Ensure SARIF files exist before upload; fail the job if missing
   - Upload SARIF using `github/codeql-action/upload-sarif@v3` (requires `security-events: read` permissions)
   - Python CD Workflows (if deployment is applicable):
     - Files: `python-deploy-dev.yml`, `python-deploy-test.yml`, `python-deploy-prod.yml`
     - Triggers:
       - `deploy-dev` uses `workflow_run` on `{stack} CI` success
       - `deploy-test` uses `workflow_run` on `{stack} Deploy to dev` success
       - `deploy-prod` uses `workflow_run` on `{stack} Deploy to test` success
     - Use `environment: dev|test|prod` for approvals and secrets scoping
     - Typical steps (adapt to project): download build artifact, build/push image (if applicable), deploy to target (e.g., Kubernetes, VM, serverless)
     - Set `concurrency` to avoid overlapping deploys per environment
3. **Terraform Workflow Jobs:**

   - Define separate jobs and link with `needs:` where appropriate:
     - `tf-validate`: pin version/cache; run `fmt -check`, `init`, `validate`
     - `tf-plan`: `needs: [tf-validate]`; run `plan` and upload plan artifact
     - `tf-lint`: run `tflint`
     - `tf-security`: run Checkov SARIF → `iac/terraform/checkov-results.sarif`
     - `tf-upload-sarif`: `needs: [tf-security]`; ensure SARIF exists, then upload via CodeQL action
   - For any Terraform CLI step (`terraform init/validate/plan/apply`), set the Terraform Cloud token environment variable:

     ```yaml
     env:
       TF_TOKEN_app_terraform_io: ${{ secrets.TFC_TOKEN }}
     ```

     Example:

     ```yaml
     - name: Terraform Init
       env:
         TF_TOKEN_app_terraform_io: ${{ secrets.TFC_TOKEN }}
       run: terraform init
     ```

   - Ensure `iac/terraform/checkov-results.sarif` exists before upload; fail if missing
   - Upload SARIF using `github/codeql-action/upload-sarif@v3` (requires `security-events: read` permissions)
   - Upload Terraform plan as artifact
   - Terraform CD Workflows (separate files):

     - Files: `terraform-deploy-dev.yml`, `terraform-deploy-test.yml`, `terraform-deploy-prod.yml`
     - Common conventions:
       - `on: workflow_run` with `workflows: ["Terraform CI"]` and `types: [completed]` for `dev`
       - `on: workflow_run` with `workflows: ["Terraform Deploy to dev"]` for `test`
       - `on: workflow_run` with `workflows: ["Terraform Deploy to test"]` for `prod`
       - Guard with `if: ${{ github.event.workflow_run.conclusion == 'success' }}`
       - `environment: dev|test|prod` and use environment-scoped secrets/state
       - `concurrency: deploy-terraform-${{ github.ref }}-${{ github.workflow }}-${{ github.environment }}`
       - Download the plan artifact produced by CI and apply it; if plan artifact missing, fail early
     - Example apply step environment variable requirement (Terraform Cloud token):

       ```yaml
       - name: Terraform Apply
         env:
           TF_TOKEN_app_terraform_io: ${{ secrets.TFC_TOKEN }}
         run: terraform apply -input=false "${{ env.TF_PLAN_PATH }}"
       ```

4. **Present Workflow YAML Preview:**
   - Show summarized YAML contents for all generated files, e.g.:
     - `{stack}-ci.yml`
     - `{stack}-deploy-dev.yml`
     - `{stack}-deploy-test.yml`
     - `{stack}-deploy-prod.yml`
   - Include key triggers, environments, permissions, and artifact passing
5. **Checkpoint:**
   - Prompt user to confirm: "Proceed to generate CI and CD workflows (dev → test → prod) with the described dependencies and protections?" Wait for confirmation.
