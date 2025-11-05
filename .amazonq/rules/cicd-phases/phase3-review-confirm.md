# CICD Workflow Generation Phase 3: Review & Confirm

## Purpose

Provide the user with final review of the generated/updated CI/CD workflow files for all detected code types, including multi-environment deployment pipelines, before confirming they are ready for commit and push (which happens in Phase 4).

## Steps

1. **Review Generated/Updated Workflows:**

   - Display comprehensive summary table:

     - Code type
     - Environment-specific workflow file names (`{code-type}-dev.yml`, `{code-type}-test.yml`, `{code-type}-prd.yml`)
     - CI jobs in each workflow (lint, test, security scan)
     - Deployment job per workflow
     - Environments (dev, test, prod)
     - Main jobs/steps in each generated YAML
     - Workflow modifications (created/modified/removed)

   - Show actual YAML content for each environment-specific workflow file:

     - `{code-type}-dev.yml` - Dev workflow (CI + Deploy to Dev)
     - `{code-type}-test.yml` - Test workflow (CI + Deploy to Test)
     - `{code-type}-prd.yml` - Prod workflow (CI + Deploy to Prod)

   - Present generated artifacts for review when available:

     - **Python**: Flake8 SARIF, Bandit SARIF, test reports/coverage artifacts
     - **Terraform**: Checkov SARIF, `tflint` output, Terraform plan artifact (if applicable)
     - **JavaScript/TypeScript**: ESLint SARIF, security scan results, test reports
     - **Java**: Build artifacts, lint SARIF, security scan results
     - **Go**: Build binaries, lint SARIF, security scan results
     - **Docker**: Container images, security scan results
     - **Kubernetes**: Manifest validation, security scan results
     - **CloudFormation**: Template validation, security scan results
     - **CDK**: Synthesis artifacts, security scan results

   - Provide quick highlights:

     - Counts of findings from SARIF where available
     - Environment-specific workflow structure (3 separate files per code type: dev/test/prd)
     - Branch-based deployment triggers (develop → dev, main → test/prod)
     - Environment protection rules and approvals

   - Use clickable file links (preferably `@filename` syntax for Cursor, or relative/absolute paths) when presenting workflow file paths for review

2. **Review Dependency Handling:**

   - Verify dependency relationships from requirements analysis are correctly implemented:
     - Upstream workflows (dependencies) build and upload artifacts
     - Downstream workflows (dependents) wait for upstream workflows via `workflow_run` triggers
     - Artifact download steps are correctly configured in downstream workflows
     - Artifact paths/URLs are correctly passed to deployment steps
   - Review dependency map: `{code-type} → depends on → {other-code-type}`
   - Verify artifact passing mechanisms (GitHub Actions artifacts, S3, container registry, etc.)
   - Confirm dependency order is correct (e.g., Python Lambda must be built before Terraform deployment)

3. **Review Multi-Environment Deployment Flow:**

   - Verify environment-specific workflow structure for each code type:
     - Dev workflow (`{code-type}-dev.yml`) triggers on pushes to `develop` branch (or waits for upstream dependencies)
     - Test workflow (`{code-type}-test.yml`) triggers via `workflow_run` after successful dev workflow on `main` branch (or waits for upstream dependencies)
     - Prod workflow (`{code-type}-prd.yml`) triggers via `workflow_run` after successful test workflow on `main` branch (or waits for upstream dependencies)
   - Confirm `workflow_run` triggers with `branches: [main]` filter are correctly configured for test and prod workflows
   - Verify `workflow_run` condition checks (`if: github.event.workflow_run.conclusion == 'success'`) are in place
   - Verify code checkout from triggering workflow branch (`ref: ${{ github.event.workflow_run.head_branch }}`)
   - Verify environment protection rules are in place
   - **Verify dependency-based triggers**: If workflows have dependencies, ensure they wait for upstream workflows appropriately

4. **Review Existing Workflow Changes:**

   - List workflows that were modified and explain changes
   - List workflows that were removed and explain why
   - **If this was a regeneration**: Clearly indicate that workflows were removed and regenerated fresh
   - Confirm all changes align with current codebase

5. **User Confirmation:**
   - Ask user: "Are these workflow files ready for commit and push to the repository?"
   - On positive confirmation, proceed to Phase 4 (Commit & Push Changes).
   - On decline, permit user to abort or suggest edits to the workflows before proceeding to Phase 4.

**Note:** This phase is for review and approval only. Actual commit, push, and finalization occur in Phase 4.
