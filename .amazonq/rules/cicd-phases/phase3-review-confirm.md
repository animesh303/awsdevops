# CICD Workflow Generation Phase 3: Review & Confirm

## Purpose

Provide the user with final review of the generated/updated single production CI/CD workflow file for all detected code types, triggered by main branch changes, before confirming it is ready for commit and push (which happens in Phase 4).

## Steps

1. **Review Generated/Updated Workflows:**

   - Display comprehensive summary table:

     - Code types detected
     - Production workflow file name (`ci-cd.yml`)
     - Trigger: main branch push
     - Environment: production (single environment)
     - Jobs for each code type (lint, security, test, build, deploy)
     - Job dependencies and execution order
     - Main jobs/steps in the unified workflow
     - Workflow modifications (created/modified/removed)

   - Show actual YAML content for the unified workflow file:

     - `ci-cd.yml` - Unified workflow containing all code types

   - Present generated artifacts for review when available:

     - **Python**: Lint results, security scan results, test reports/coverage artifacts
     - **Terraform**: Security scan results, `tflint` output, Terraform plan artifact (if applicable)
     - **JavaScript/TypeScript**: Lint results, security scan results, test reports
     - **Java**: Build artifacts, lint results, security scan results
     - **Go**: Build binaries, lint results, security scan results
     - **Docker**: Container images, security scan results
     - **Kubernetes**: Manifest validation, security scan results
     - **CloudFormation**: Template validation, security scan results
     - **CDK**: Synthesis artifacts, security scan results

   - Provide quick highlights:

     - Single production workflow structure (1 file containing all code types)
     - Trigger: main branch push only
     - Jobs sequenced by dependencies
     - Single production environment
     - Environment protection rules and approvals

   - Use clickable file links (preferably `@filename` syntax for AmazonQ, or relative/absolute paths) when presenting workflow file paths for review

2. **Review Dependency Handling:**

   - Verify dependency relationships from requirements analysis are correctly implemented:
     - Upstream jobs (dependencies) build and upload artifacts
     - Downstream jobs (dependents) wait for upstream jobs via `needs:` dependencies
     - Artifact download steps are correctly configured in downstream deploy jobs
     - Artifact paths/URLs are correctly passed to deployment steps
   - Review dependency map: `{code-type} → depends on → {other-code-type}`
   - Verify artifact passing mechanisms (GitHub Actions artifacts)
   - Confirm dependency order is correct (e.g., Python Lambda must be built before Terraform deployment)

3. **Review Deployment Flow:**

   - Verify single production workflow structure:
     - Workflow (`ci-cd.yml`) triggers on pushes to `main` branch only
     - All deploy jobs use `environment: production`
     - Jobs are sequenced correctly based on dependencies using `needs:`
     - Code types with no dependencies run first
     - Dependent code types wait for upstream deploy jobs to complete
   - Verify job dependencies are correctly configured using `needs:` array
   - Verify production environment protection rules are in place
   - **Verify dependency-based job sequencing**: If code types have dependencies, ensure deploy jobs wait for upstream deploy jobs via `needs:`

4. **Review Workflow Generation Context:**

   - **If this was a regeneration**:
     - Indicate that `.github/workflows/` directory was deleted and the single production workflow was regenerated fresh
     - The workflow is newly generated (no modifications to existing workflows)
   - **If this was a new generation**:
     - Indicate that a new single production workflow was generated
     - Any existing workflow with matching name was replaced
   - Confirm the generated workflow aligns with current codebase and detected code types
   - Confirm workflow triggers on main branch and deploys to production environment

5. **Validate Workflow Linting:**

   - **CRITICAL**: Verify all generated workflow files have no linting errors
   - **MANDATORY - BLOCKING CHECK: hashFiles() at Job Level**:
     - Read the generated workflow file
     - Search for job-level `if:` fields (same indentation as `runs-on:`)
     - If any job-level `if:` contains `hashFiles`, this is a BLOCKING ERROR
     - Fix immediately by moving condition to step level
     - Re-validate after fix
     - DO NOT proceed to Phase 4 until this is fixed
   - Check YAML syntax validity
   - Verify all GitHub Actions expressions use correct `${{ }}` syntax
   - Verify no missing required fields
   - Check for valid job dependencies and workflow triggers
   - **If linting errors are found**: Fix them immediately before proceeding to Phase 4
   - **CRITICAL**: Job-level `hashFiles()` will cause workflow validation failure - must be fixed
   - Report any linting errors found and confirm they are resolved

6. **User Confirmation:**
   - Ask user: "Are these workflow files ready for commit and push to the repository?"
   - On positive confirmation, proceed to Phase 4 (Commit & Push Changes).
   - On decline, permit user to abort or suggest edits to the workflows before proceeding to Phase 4.
   - **Update plan checkboxes** - Mark completed steps [x] in `.cicd-docs/review-notes.md`
   - **Update cicd-state.md** - Update Phase 3 status

**Note:** This phase is for review and approval only. Actual commit, push, and finalization occur in Phase 4.
