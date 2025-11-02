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
   - **Terraform Cloud Remote Backend Limitation:** When Terraform Cloud is used as the remote backend, plan output files are NOT supported. Skip plan artifact upload/download and any actions that depend on plan files in workflows using Terraform Cloud.
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

   - **AWS Credentials Configuration (Mandatory):** If any workflow step requires AWS CLI credentials (e.g., Terraform CLI commands that interact with AWS), the workflow MUST include a step to configure AWS credentials via OIDC before any AWS-dependent operations:

     ```yaml
     - name: Configure AWS credentials via OIDC
       uses: aws-actions/configure-aws-credentials@v4
       with:
         role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
         aws-region: ${{ vars.AWS_REGION }}
     ```

     - Place this step as one of the first steps in any job that performs AWS operations
     - Require the workflow to declare `permissions: id-token: write` (for OIDC) at the job or workflow level

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

     - `tf-validate`: pin version/cache; run `init`, `validate`. While using `terraform fmt` do not include `check` option.
     - `tf-plan`: `needs: [tf-validate]`; run `plan` only (do NOT upload plan artifact if Terraform Cloud is the remote backend, as plan output is not supported)
     - `tf-security`: run Checkov with SARIF output. Set `continue-on-error: true` for the job.
     - `tf-upload-sarif`: `needs: [tf-security]`; download the SARIF. **Important:** upload `results_sarif.sarif` via CodeQL action. SARIF File name should always be `results_sarif.sarif`. Set `continue-on-error: true` for the job. Example:

       ```yaml
       tf-upload-sarif:
         runs-on: ubuntu-latest
         needs: [tf-security]
         continue-on-error: true
         steps:
           - uses: actions/checkout@v4

           - name: Download SARIF artifacts
             uses: actions/download-artifact@v4
             with:
               name: checkov-sarif
               path: ./

           - name: Verify SARIF file exists
             run: |
               if [ ! -f results_sarif.sarif ]; then
                 echo "SARIF file not found, skipping upload"
                 exit 0
               fi
               echo "SARIF file found at: results_sarif.sarif"

           - name: Upload SARIF to GitHub
             uses: github/codeql-action/upload-sarif@v3
             with:
               sarif_file: results_sarif.sarif
       ```

   - **Terraform Version Requirement (Mandatory):** If a workflow contains any Terraform CLI commands (`terraform init/validate/plan/apply`), the workflow MUST use Terraform version 1.1 or later. When using `hashicorp/setup-terraform@v3` or similar actions, specify `terraform_version: ~1.1` or `terraform_version: ^1.1` (minimum 1.1). Example:

     ```yaml
     - name: Setup Terraform
       uses: hashicorp/setup-terraform@v3
       with:
         terraform_version: ~1.1
     ```

     **Important:** Do NOT use `~1.0` or any version below 1.1. This applies to ALL Terraform jobs (CI and CD workflows).

   - **AWS Credentials:** Since Terraform workflows typically interact with AWS, ALL Terraform jobs MUST include the "Configure AWS credentials via OIDC" step (see Step 1) before any `terraform init/validate/plan/apply` commands. The job must declare `permissions: id-token: write` for OIDC to work.
   - For any Terraform CLI step (`terraform init/validate/plan/apply`), set the Terraform Cloud token environment variable and .terraformrc once the job level:

     ```yaml
     - name: Configure Terraform Cloud
       env:
         TFC_TOKEN: ${{ secrets.TFC_TOKEN }}
       run: |
         cat > $HOME/.terraformrc << EOF
         credentials "app.terraform.io" {
           token = "$TFC_TOKEN"
         }
         EOF
     ```

     Example:

     ```yaml
     - name: Configure Terraform Cloud
       env:
         TFC_TOKEN: ${{ secrets.TFC_TOKEN }}
       run: |
         cat > $HOME/.terraformrc << EOF
         credentials "app.terraform.io" {
           token = "$TFC_TOKEN"
         }
         EOF
     ```

   - Ensure `iac/terraform/checkov-results.sarif` exists before upload; fail if missing
   - Upload SARIF using `github/codeql-action/upload-sarif@v3` (requires `security-events: read` permissions). The artifact is uploaded with path iac/terraform/checkov-results.sarif, so when downloaded it preserves that structure. The file will be at iac/terraform/checkov-results.sarif.
   - **Terraform Plan Artifact:** Do NOT upload Terraform plan as artifact when Terraform Cloud is used as the remote backend (plan output is not supported by Terraform Cloud). Only upload plan artifacts if using other backends (e.g., S3, local).
   - Terraform CD Workflows (separate files):

     - Files: `terraform-deploy-dev.yml`, `terraform-deploy-test.yml`, `terraform-deploy-prod.yml`
     - Common conventions:
       - `on: workflow_run` with `workflows: ["Terraform CI"]` and `types: [completed]` for `dev`
       - `on: workflow_run` with `workflows: ["Terraform Deploy to dev"]` for `test`
       - `on: workflow_run` with `workflows: ["Terraform Deploy to test"]` for `prod`
       - Guard with `if: ${{ github.event.workflow_run.conclusion == 'success' }}`
       - `environment: dev|test|prod` and use environment-scoped secrets/state
       - `concurrency: deploy-terraform-${{ github.ref }}-${{ github.workflow }}-${{ github.environment }}`
       - **Plan Artifact Handling:** When Terraform Cloud is used as the remote backend, do NOT download plan artifacts (plan output is not supported). Run `terraform plan` and `terraform apply` directly without plan file dependencies. If using other backends (e.g., S3, local), download the plan artifact produced by CI and apply it; if plan artifact missing, fail early.
     - Example apply step for Terraform Cloud (no plan file):

       ```yaml
       - name: Terraform Plan
         env:
           TF_TOKEN_app_terraform_io: ${{ secrets.TFC_TOKEN }}
         run: terraform plan

       - name: Terraform Apply
         env:
           TF_TOKEN_app_terraform_io: ${{ secrets.TFC_TOKEN }}
         run: terraform apply -input=false -auto-approve
       ```

       **Note:** When using Terraform Cloud remote backend, plan output files are NOT supported. Do NOT use `terraform plan -out=filename` or `terraform apply filename`. Run `terraform plan` and `terraform apply` directly without plan file dependencies. Consider using Terraform Cloud's native plan/apply workflow (sentinel policies, run triggers) for advanced approval workflows.

     - Example apply step for non-Terraform Cloud backends (with plan file download):

       ```yaml
       - name: Download plan artifact
         uses: actions/download-artifact@v4
         with:
           name: terraform-plan

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
