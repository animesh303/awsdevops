# Workflow Dependency Handling Patterns

## Purpose

This document provides comprehensive patterns for handling dependencies between code artifacts in GitHub Actions workflows. Use these patterns when generating workflows for code types that depend on other code types.

## Related Files

- See `phase2-generate-workflow.md` for workflow generation steps
- See `workflow-common-issues.md` for troubleshooting common issues
- See `orchestrator-workflow-patterns.md` for orchestrator workflow patterns (recommended for complex dependencies)
- See `{code-type}-standards.md` for language-specific dependency examples

---

## Overview

When code artifacts have dependencies (e.g., Terraform depends on Python Lambda package), workflows must:

1. **Wait for upstream workflows** to complete using `workflow_run` triggers OR use orchestrator workflows
2. **Download artifacts** from upstream workflows
3. **Place artifacts** in correct locations where deployment code expects them
4. **Verify artifacts** exist before proceeding with deployment
5. **Pass artifact information** to deployment steps

**Dependency Management Approach**:

- **Orchestrator Workflows** (Always Used): Orchestrator workflows are ALWAYS generated to manage execution order and artifact passing. This ensures consistency and simplifies dependency management. See `orchestrator-workflow-patterns.md` for details.

**Note**: The patterns below (direct `workflow_run` triggers) are provided for reference only. In practice, orchestrator workflows are always used for consistency.

---

## Single Dependency Pattern

**When Code Type A depends on Code Type B** (e.g., Terraform depends on Python Lambda):

### Upstream Workflow (Code Type B - Python)

- Build and package artifacts (e.g., Lambda zip file)
- Upload artifacts using `actions/upload-artifact@v4`:
  ```yaml
  - name: Upload Lambda package
    uses: actions/upload-artifact@v4
    with:
      name: lambda-package-dev # Environment-specific naming
      path: lambda-package.zip
      retention-days: 1
  ```
- Or upload to S3/container registry for cross-workflow access
- Export artifact information (paths, URLs, tags) as workflow outputs or environment variables

### Downstream Workflow (Code Type A - Terraform)

- Add `workflow_run` trigger to wait for upstream workflow:
  ```yaml
  on:
    workflow_run:
      workflows: ["Python Dev"] # Wait for Python workflow
      types: [completed]
      branches: [develop]
    push:
      branches: [develop] # Fallback trigger
  ```
- **CRITICAL**: Download artifacts from upstream workflow BEFORE any Terraform operations (with error handling):

  ```yaml
  - name: Download Lambda package from upstream workflow
    uses: actions/download-artifact@v4
    continue-on-error: true
    id: download-artifact
    with:
      name: lambda-package-dev
      run-id: ${{ github.event.workflow_run.id }}
      github-token: ${{ secrets.GITHUB_TOKEN }}
      path: ./lambda-package

  - name: Verify artifact downloaded successfully
    if: steps.download-artifact.outcome != 'success'
    run: |
      echo "Error: Failed to download artifact 'lambda-package-dev' from upstream workflow"
      echo "Upstream workflow run ID: ${{ github.event.workflow_run.id }}"
      exit 1
  ```

- **Place artifact in correct location** where Terraform expects it:
  ```yaml
  - name: Move Lambda package to Terraform directory
    run: |
      # CRITICAL: Check the actual path referenced in Terraform code
      # If Terraform uses: filename = "lambda_function.zip" in the same directory
      # Place it where Terraform expects it (e.g., iac/terraform/lambda_function.zip)
      mkdir -p ./iac/terraform
      cp ./lambda-package/lambda-package.zip ./iac/terraform/lambda_function.zip
      # Adjust path based on actual Terraform code location and filename
      echo "TF_VAR_lambda_package_path=$(pwd)/iac/terraform/lambda_function.zip" >> $GITHUB_ENV
  ```
- **Verify artifact exists** before Terraform operations:
  ```yaml
  - name: Verify Lambda package exists
    run: |
      # Verify the exact path that Terraform code references
      TERRAFORM_LAMBDA_PATH="./iac/terraform/lambda_function.zip"
      if [ ! -f "$TERRAFORM_LAMBDA_PATH" ]; then
        echo "Error: Lambda package not found at: $TERRAFORM_LAMBDA_PATH"
        echo "Downloaded artifacts location:"
        ls -la ./lambda-package/ || echo "lambda-package directory not found"
        exit 1
      fi
      echo "✓ Lambda package verified at: $TERRAFORM_LAMBDA_PATH"
  ```
- **Order of operations**: Checkout → Download artifacts → Place artifacts → Verify artifacts → Configure credentials → Terraform init/plan/apply

---

## Multiple Dependencies Pattern

If a code type depends on multiple others, use `workflow_run` triggers for all upstream workflows:

```yaml
on:
  workflow_run:
    workflows: ["Python Dev", "Docker Dev"] # Wait for all upstream workflows
    types: [completed]
    branches: [develop]
  push:
    branches: [develop] # Fallback trigger
```

**Important**: When multiple `workflow_run` triggers exist, `github.event.workflow_run.id` refers to the workflow that triggered this run. To download artifacts from specific upstream workflows:

- **Option 1**: Use workflow outputs/environment variables from upstream workflows to pass artifact information
- **Option 2**: Store artifacts in S3/container registry with predictable naming and download from there (RECOMMENDED for multiple dependencies)
- **Option 3**: Use GitHub API to find the specific workflow run ID for each dependency

Download artifacts from all upstream workflows and combine as needed for deployment.

---

## Artifact Passing Methods

**Decision Tree for Artifact Passing**:

- **Single dependency with workflow_run trigger**: Use Cross-Workflow Artifacts (Method 2)
- **Multiple dependencies**: Use S3/Storage (Method 3)
- **Docker images**: Use Container Registry (Method 4)
- **Same workflow run**: Use GitHub Actions Artifacts (Method 1)
- **Artifact metadata only**: Use Environment Variables/Workflow Outputs (Method 5)

### Method 1: GitHub Actions Artifacts (For same-run dependencies)

- Use `actions/upload-artifact@v4` and `actions/download-artifact@v4`
- Works within same workflow run (jobs in same workflow)
- Limited retention (default 1 day, configurable up to 90 days)
- Use when: Artifacts are consumed by jobs within the same workflow run

### Method 2: Cross-Workflow Artifacts (MANDATORY for workflow_run triggers with single dependency)

- Use `actions/download-artifact@v4` with `run-id` and `github-token`
- Works for `workflow_run` triggers when downloading from the triggering workflow
- **CRITICAL**: For single dependency, ALWAYS use this method with `run-id: ${{ github.event.workflow_run.id }}`
- **Limitation**: When multiple dependencies exist, `github.event.workflow_run.id` only refers to one workflow - use S3/Storage method instead
- Use when: Single upstream dependency AND workflow_run trigger exists

### Method 3: S3/Storage (MANDATORY for multiple dependencies or long retention)

- Upload to S3 bucket with predictable naming (e.g., `{artifact-name}-{environment}-{commit-sha}`)
- Download from S3 in downstream workflow
- Better for multiple dependencies as each workflow can upload independently
- Use when: Multiple dependencies exist OR artifacts need longer retention OR multiple workflows depend on same artifact

### Method 4: Container Registry (For Docker images)

- Push Docker images with tags to registry (ECR, Docker Hub, etc.)
- Reference image tags in downstream workflows
- Use when: Artifact is a Docker/container image

### Method 5: Environment Variables/Workflow Outputs (For artifact metadata)

- Pass artifact paths/URLs via workflow outputs or GitHub secrets
- Use when: Only artifact location/URL needs to be passed (not the artifact itself)
- Combine with artifact storage methods above

---

## Environment-Specific Considerations

### Dev Environment

- Artifact names should include environment: `lambda-package-dev`
- Workflow triggers: `workflow_run` on `develop` branch OR `push` to `develop` branch
- Use shorter retention for artifacts (1 day typically sufficient)

### Test Environment

- Artifact names should include environment: `lambda-package-test`
- Workflow triggers: `workflow_run` on `main` branch OR `push` to `main` branch
- Use moderate retention for artifacts (3-7 days)

### Prod Environment

- Artifact names should include environment: `lambda-package-prod`
- Workflow triggers: `workflow_run` after successful test workflow on `main` branch
- Use longer retention for artifacts (7-30 days) or S3 storage
- **CRITICAL**: Prod workflows should wait for dependency's prod workflow (same environment), not test workflow

---

## Best Practices

1. **Always verify artifacts exist** before using them in deployment steps
2. **Use environment-specific artifact naming** to avoid conflicts
3. **Handle errors gracefully** with `continue-on-error` and verification steps
4. **Document artifact paths** in workflow comments for maintainability
5. **Use S3/Storage for multiple dependencies** to avoid complexity
6. **Test artifact passing** in dev environment before deploying to prod

---

## Troubleshooting

- **Artifact not found**: Check artifact name matches exactly (case-sensitive)
- **Download fails**: Verify `run-id` and `github-token` are provided for cross-workflow downloads
- **Path mismatch**: Verify artifact is placed where deployment code expects it
- **Multiple dependencies**: Use S3/Storage method instead of cross-workflow artifacts

See `workflow-common-issues.md` for more troubleshooting guidance.

---

## Orchestrator Workflow Pattern (Always Used)

**Always Used**: Orchestrator workflows are ALWAYS generated for ALL scenarios to maintain consistency and simplify dependency management.

**Benefits**:

- Simplified dependency management (dependencies managed in one place)
- Clear execution order (topological sort ensures correct order)
- Centralized error handling and reporting
- Reusable code type workflows (can still be triggered independently)

**Pattern**:

1. **Generate Orchestrator Workflows** (one per environment):

   - `orchestrator-dev.yml` - Orchestrates all code type workflows for dev
   - `orchestrator-test.yml` - Orchestrates all code type workflows for test
   - `orchestrator-prd.yml` - Orchestrates all code type workflows for prod

2. **Orchestrator Structure**:

   - Triggers on branch push (develop for dev, main for test/prd)
   - Contains jobs that invoke code type workflows in dependency order
   - Uses topological sort to determine execution order
   - Handles artifact passing between workflows
   - Provides centralized error handling

3. **Code Type Workflows**:
   - Support `workflow_call` trigger for orchestrator invocation (required for reusable workflows)
   - Can still be triggered independently via push triggers
   - Upload artifacts with consistent naming

**See**: `orchestrator-workflow-patterns.md` for complete orchestrator patterns and implementation details.
