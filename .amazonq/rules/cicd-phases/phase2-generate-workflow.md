# CICD Workflow Generation Phase 2: Generate Workflow Files

## Purpose

Render GitHub Actions workflow files (YAML) for ALL detected code types as **three separate workflow files per environment** (dev, test, prd). Each workflow contains CI jobs and deployment job for that specific environment. **Handle dependencies between code artifacts** (from requirements analysis) by enforcing workflow execution order and artifact passing. Ensure all required CI/CD and code scanning steps are present. Handle existing workflows by modifying or removing as needed.

## Plan Document Location

**CRITICAL**: Plan documents are created in `.cicd-docs/` directory (preferred) or `.amazonq/rules/cicd-phases/` (legacy fallback):

- Workflow generation plan: `.cicd-docs/workflow-generation-plan.md` (or `.cicd-docs/phase2-plan.md`)

## MANDATORY: GitHub Actions Expression Syntax

**CRITICAL**: When using GitHub Actions functions like `hashFiles`, `always()`, `success()`, etc., they MUST always be wrapped in `${{ }}` expression syntax.

- **Correct**: `if: ${{ hashFiles('tests/**') != '' }}`
- **Incorrect**: `if: hashFiles('tests/**') != ''` (will cause "Unrecognized function" error)

**All GitHub Actions expressions must use `${{ }}` syntax**, including:

- `hashFiles()` - Check if files exist or have changed
- `always()`, `success()`, `failure()`, `cancelled()` - Job status checks
- `github.event.*` - Event context access
- Any other GitHub Actions context functions

**CRITICAL - `hashFiles()` Context Limitation**: The `hashFiles()` function is **ONLY available in step-level `if` conditions** (`jobs.<job>.steps[*].if`), **NOT at the job level** (`jobs.<job>.if`).

- **Correct (Step Level)**:
  ```yaml
  jobs:
    tests:
      runs-on: ubuntu-latest
      steps:
        - name: Run tests
          if: ${{ hashFiles('tests/**') != '' }}
          run: pytest
  ```
- **Incorrect (Job Level)**:
  ```yaml
  jobs:
    tests:
      if: ${{ hashFiles('tests/**') != '' }} # ❌ hashFiles() not available here
      runs-on: ubuntu-latest
      steps:
        - run: pytest
  ```

If you need to conditionally run an entire job based on file existence, either:

1. Always run the job but skip steps conditionally using step-level `if` conditions
2. Use a separate job to check file existence and set an output, then reference that output in the job's `if` condition

## MANDATORY: Workflow Linting and Validation

**CRITICAL**: All generated CICD workflow files MUST be free of linting errors. Before finalizing any workflow:

1. **Validate YAML syntax**: Ensure all YAML is valid and properly formatted
2. **Validate GitHub Actions syntax**: Verify all expressions use correct `${{ }}` syntax
3. **Check for common errors**:
   - Missing required fields (name, on, jobs, runs-on, etc.)
   - Invalid job dependencies (circular dependencies, missing job references)
   - Incorrect workflow trigger syntax
   - Missing or incorrect environment names
   - Invalid artifact names or paths
   - Incorrect condition syntax
4. **Test workflow structure**: Verify workflow structure is valid GitHub Actions YAML
5. **Fix any linting errors immediately** - DO NOT proceed to Phase 3 if workflows have linting errors

**Workflows with linting errors will fail in GitHub Actions and must be fixed before deployment.**

## Reference Documents

**CRITICAL**: When generating workflows, reference these supporting documents:

- **`workflow-common-issues.md`**: Common issues and solutions when generating GitHub Actions workflows
- **`workflow-dependency-handling.md`**: Comprehensive patterns for handling dependencies between code artifacts
- **`orchestrator-workflow-patterns.md`**: Orchestrator workflow patterns for managing complex dependencies

## Steps

1. **Load Dependency Information from Phase 1:**

   - **Read Dependency Map**:

     - Load dependency relationships from Phase 1 plan document
     - Load dependency map from `.cicd-docs/cicd-state.md` if available
     - Understand which code types depend on others (e.g., `terraform → depends on → python`)

   - **Identify Artifact Requirements**:
     - For each dependency, identify what artifacts need to be passed
     - Example: Terraform needs Python Lambda zip file location
     - Example: Kubernetes needs Docker image tag
     - Document artifact types: zip files, Docker images, build artifacts, etc.

2. **Verify Clean State (Simplified Approach):**

   - **For regeneration requests**: `.github/workflows/` directory should already be deleted (handled in Welcome phase), so no existing workflows to manage
   - **For new generation**: If `.github/workflows/` directory exists with files, they will be replaced with newly generated workflows
   - **No complex removal logic needed**: Simply generate new workflow files - they will overwrite any existing files with the same names
   - Document that new environment-specific workflows are being generated (3 per code type: dev/test/prd)

3. **Read Language-Specific Standards:**

   - For each detected code type, read the corresponding standards file:
     - `.amazonq/rules/cicd-phases/{code-type}-standards.md`
   - If standards file does not exist, create it following the pattern of existing standards files
   - **CRITICAL**: Use the complete content from the standards file - do not summarize or paraphrase

4. **Generate Orchestrator Workflows:**

   **CRITICAL**: ALWAYS generate orchestrator workflows for ALL scenarios to maintain consistency and simplify dependency management.

   - **Read Orchestrator Patterns**: Read `orchestrator-workflow-patterns.md` for detailed patterns

   - **Build Execution Order**:

     - Use topological sort algorithm to determine correct execution order
     - Start with code types that have no dependencies (leaf nodes)
     - Process code types in order: dependencies first, dependents after
     - Example: If `terraform → python` and `kubernetes → docker → python`, order is: `[python, docker, terraform, kubernetes]`

   - **Generate Orchestrator Workflows** (one per environment):

     **Orchestrator Dev** (`.github/workflows/orchestrator-dev.yml`):

     - **Trigger**: Push to `develop` branch (and `workflow_dispatch` for manual trigger)
     - **Structure**: Single job with sequential steps, one step per code type in dependency order
     - **Each Step**: Uses `uses: ./.github/workflows/{code-type}-{env}.yml` to call reusable workflows
     - **Execution**: Steps execute sequentially, automatically waiting for previous step to complete
     - **Pattern**: Follow patterns from `orchestrator-workflow-patterns.md`

     **Orchestrator Test** (`.github/workflows/orchestrator-test.yml`):

     - **Trigger**: Push to `main` branch (and `workflow_dispatch` for manual trigger)
     - **Same structure as dev**, but for test environment

     **Orchestrator Prod** (`.github/workflows/orchestrator-prd.yml`):

     - **Trigger**: `workflow_run` after successful `orchestrator-test.yml` completion on `main` branch (and `workflow_dispatch` for manual trigger)
     - **Same structure as dev/test**, but for prod environment
     - More strict error handling

   - **Orchestrator Workflow Structure**:

     ```yaml
     name: Orchestrator Dev

     on:
       push:
         branches: [develop]
       workflow_dispatch:

     permissions:
       contents: read
       id-token: write

     jobs:
       orchestrate:
         runs-on: ubuntu-latest
         steps:
           - name: Run {code-type-1} Dev Workflow
             uses: ./.github/workflows/{code-type-1}-dev.yml

           - name: Run {code-type-2} Dev Workflow
             uses: ./.github/workflows/{code-type-2}-dev.yml

           - name: Run {code-type-3} Dev Workflow
             uses: ./.github/workflows/{code-type-3}-dev.yml
     ```

   - **Reference**: See `orchestrator-workflow-patterns.md` for complete patterns and implementation details

5. **Generate Environment-Specific Workflows Per Detected Code Type:**

   **IMPORTANT**: When generating workflows, orchestrator workflows manage dependency order. Individual code type workflows:

   - Support `workflow_call` trigger for orchestrator invocation
   - Can still be triggered independently via push triggers
   - Download artifacts from upstream workflows when needed (handled within workflow jobs)
   - Reference artifact locations (paths, URLs, tags) from upstream workflows

   For each detected code type, generate **three separate workflow files**:

   **Deploy to Dev Workflow** (`.github/workflows/{code-type}-dev.yml`):

   - **Workflow Trigger**:
     - **Always use orchestrators**: Trigger on push to `develop` branch AND support `workflow_call` for orchestrator invocation
       ```yaml
       on:
         workflow_call: # Required for reusable workflows (orchestrator pattern)
         push:
           branches: [develop]
       ```
     - **Note**: GitHub Actions doesn't support conditions at workflow trigger level. Conditions must be at job level. If using `workflow_run`, add condition check at job level: `if: ${{ github.event.workflow_run.conclusion == 'success' || github.event_name == 'push' }}`
   - **CI Jobs**:

     - Lint, test, security scan, artifact generation
     - Organize workflow logic into multiple jobs with clear dependencies using `needs:`
     - Prefer fast-fail by running independent jobs in parallel
     - Build and upload artifacts
     - Follow patterns from `{code-type}-standards.md`
     - **Note**: SARIF upload steps should be skipped/omitted

   - **Deploy to Dev Job**:
     - **Needs**: All CI jobs must succeed
     - **Dependency Handling** (CRITICAL - MANDATORY if dependencies detected):
       - **MANDATORY CHECK**: If Phase 1 detected dependencies for this code type (from mapping file OR requirements OR code analysis), dependency handling steps MUST be included
       - **Load Artifact Mapping** (PREFERRED):
         - **CRITICAL**: Read `.code-docs/artifact-mappings.json` if it exists
         - Extract dependency information from `mappings` array
         - For each mapping entry:
           - Use `artifact_name` from `environment_artifacts.dev` for artifact download
           - Use `artifact_destination_path` for artifact placement
           - Use `terraform_resource` to identify which Terraform resource needs the artifact
           - Use `lambda_function` to identify which Lambda function produces the artifact
       - **For Terraform workflows**: If Terraform code references artifacts (e.g., `filename = "lambda_function.zip"`) OR mapping file indicates dependencies, dependency handling is MANDATORY
       - **Steps MUST include** (in this exact order):
         1. **Download artifacts from upstream workflows FIRST** (e.g., Lambda zip from Python workflow)
            - **If mapping file exists**: Use exact artifact name from `environment_artifacts.dev` (e.g., `lambda-package-dev`)
            - **If mapping file does not exist**: Use patterns from `terraform-standards.md` or `workflow-dependency-handling.md`
            - For Terraform: Follow exact patterns from `terraform-standards.md` section "Deploy to Dev" steps 2-4
         2. **Place artifacts in correct location** where deployment code expects them
            - **If mapping file exists**: Use exact path from `artifact_destination_path` field
            - **If mapping file does not exist**: For Terraform, if code references `lambda_function.zip`, place it where Terraform expects it (e.g., `iac/terraform/lambda_function.zip`)
            - Follow patterns from `terraform-standards.md` for exact paths
         3. **Verify artifacts exist** before proceeding with deployment operations
            - **If mapping file exists**: Verify artifact exists at `artifact_destination_path`
            - Use verification steps from `terraform-standards.md`
         4. **Pass artifact information** to deployment steps (environment variables, Terraform variables, etc.)
       - **Multiple Dependencies**: If mapping file indicates multiple Lambda functions:
         - Download each artifact using its specific `environment_artifacts.dev` name
         - Place each artifact at its specific `artifact_destination_path`
         - Verify all artifacts exist before proceeding
       - **DO NOT SKIP**: If dependencies are detected, these steps are MANDATORY, not optional
     - Deploys to Development environment
     - Uses GitHub `environment: dev` for secrets and protection rules
     - Downloads CI artifacts if needed for deployment
     - **Upload deployment artifacts** for downstream workflows (if this code type is a dependency)
     - Follow patterns from `{code-type}-standards.md` - **CRITICAL**: For Terraform, use complete dependency handling patterns from `terraform-standards.md`

   **Deploy to Test Workflow** (`.github/workflows/{code-type}-test.yml`):

   - **Workflow Trigger**:
     - **Always use orchestrators**: Trigger on push to `main` branch AND support `workflow_call` for orchestrator invocation
       ```yaml
       on:
         workflow_call: # Required for reusable workflows (orchestrator pattern)
         push:
           branches: [main]
       ```
     - **Note**: GitHub Actions doesn't support conditions at workflow trigger level. Conditions must be at job level. If using `workflow_run`, add condition check at job level: `if: ${{ github.event.workflow_run.conclusion == 'success' || github.event_name == 'push' }}`
   - **CI Jobs**:

     - Lint, test, security scan, artifact generation
     - Organize workflow logic into multiple jobs with clear dependencies using `needs:`
     - Prefer fast-fail by running independent jobs in parallel
     - Build and upload artifacts
     - Follow patterns from `{code-type}-standards.md`
     - **CRITICAL - Checkout Step**:
       - **For push triggers**: Standard checkout is sufficient: `- uses: actions/checkout@v4`
       - **For workflow_run triggers**: ALL jobs (CI and deployment) MUST include checkout with ref parameter:
       ```yaml
       - uses: actions/checkout@v4
           with:
             ref: ${{ github.event.workflow_run.head_branch }}
       ```
       - **Rule**: If workflow has `workflow_run` trigger, ALL jobs must use checkout with ref parameter, regardless of whether push trigger also exists

   - **Deploy to Test Job**:
     - **Needs**: All CI jobs must succeed
     - **Dependency Handling** (CRITICAL - must be done BEFORE deployment operations):
       - If this code type depends on others, ensure upstream workflows completed successfully
       - **Download artifacts from upstream workflows FIRST** (e.g., Lambda zip from Python workflow)
       - **Place artifacts in correct location** where deployment code expects them
       - **Verify artifacts exist** before proceeding with deployment operations
       - Pass artifact information to deployment steps
     - Deploys to Test environment
     - Uses GitHub `environment: test` for secrets and protection rules
     - Downloads CI artifacts if needed for deployment
     - **Upload deployment artifacts** for downstream workflows (if this code type is a dependency)
     - Follow patterns from `{code-type}-standards.md`

   **Deploy to Prod Workflow** (`.github/workflows/{code-type}-prd.yml`):

   - **Workflow Trigger**:
     - **Always use orchestrators**: Trigger via `workflow_run` after successful test workflow AND support `workflow_call` for orchestrator invocation
     ```yaml
     on:
       workflow_call: # Required for reusable workflows (orchestrator pattern)
       workflow_run:
         workflows: ["{Code Type} Test"]
         types: [completed]
         branches: [main]
     ```
   - **Condition Check**:
     ```yaml
     jobs:
       deploy:
         if: ${{ github.event.workflow_run.conclusion == 'success' }}
     ```
   - **CI Jobs**:

     - Lint, test, security scan, artifact generation
     - Organize workflow logic into multiple jobs with clear dependencies using `needs:`
     - Prefer fast-fail by running independent jobs in parallel
     - Build and upload artifacts
     - Follow patterns from `{code-type}-standards.md`
     - **CRITICAL - Checkout Step**: EVERY job (CI and deployment) MUST have checkout as the FIRST step with ref parameter:
       ```yaml
       - uses: actions/checkout@v4
         with:
           ref: ${{ github.event.workflow_run.head_branch }}
       ```
       This is required because `workflow_run` triggers don't automatically checkout code

   - **Deploy to Prod Job**:
     - **Needs**: All CI jobs must succeed
     - **Dependency Handling** (CRITICAL - must be done BEFORE deployment operations):
       - If this code type depends on others, ensure upstream workflows completed successfully
       - **Download artifacts from upstream workflows FIRST** (e.g., Lambda zip from Python workflow)
       - **Place artifacts in correct location** where deployment code expects them
       - **Verify artifacts exist** before proceeding with deployment operations
       - Pass artifact information to deployment steps
     - Deploys to Production environment
     - Uses GitHub `environment: prod` with protection rules/approvals for promotion gates
     - Downloads CI artifacts if needed for deployment
     - **Upload deployment artifacts** for downstream workflows (if this code type is a dependency)
     - Follow patterns from `{code-type}-standards.md`
     - Protected with GitHub environment protection rules

6. **Workflow Structure Requirements:**

   **CRITICAL**: Remember that all GitHub Actions expressions (including `hashFiles`) MUST be wrapped in `${{ }}` syntax.

   - **Dev Workflow Structure Example:**

     ```yaml
     name: {Code Type} Dev

     on:
       push:
         branches: [develop]

     permissions:
       contents: read
       id-token: write  # For OIDC if needed

     jobs:
       # CI Jobs
       lint:
         runs-on: ubuntu-latest
         steps:
           # ... lint steps from standards file

       security:
         runs-on: ubuntu-latest
         steps:
           # ... security scan steps from standards file

      tests:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - name: Run tests
            if: ${{ hashFiles('tests/**') != '' }}
            run: |
              # ... test steps from standards file

       # Deployment Job
       deploy-dev:
         needs: [lint, security, tests]
         runs-on: ubuntu-latest
         environment: dev
         steps:
           # ... deployment steps from standards file
     ```

   - **Test Workflow Structure Example:**

     ```yaml
     name: {Code Type} Test

     on:
       push:
         branches: [main]

     permissions:
       contents: read
       id-token: write  # For OIDC if needed

     jobs:
       # CI Jobs (must be separate jobs, not steps)
       lint:
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v4
           # ... lint steps from standards file

       security:
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v4
           # ... security scan steps from standards file

      tests:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - name: Run tests
            if: ${{ hashFiles('tests/**') != '' }}
            run: |
              # ... test steps from standards file

       # Deployment Job
       deploy-test:
         needs: [lint, security, tests]
         runs-on: ubuntu-latest
         environment: test
         steps:
           - uses: actions/checkout@v4
           # ... deployment steps from standards file
     ```

   - **Prod Workflow Structure Example:**

     ```yaml
     name: {Code Type} Prod

     on:
       workflow_run:
         workflows: ["{Code Type} Test"]
         types: [completed]
         branches: [main]

     permissions:
       contents: read
       id-token: write  # For OIDC if needed

     jobs:
       # CI Jobs (must be separate jobs, not steps)
       lint:
         if: ${{ github.event.workflow_run.conclusion == 'success' }}
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v4
             with:
               ref: ${{ github.event.workflow_run.head_branch }}
           # ... lint steps from standards file

       security:
         if: ${{ github.event.workflow_run.conclusion == 'success' }}
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v4
             with:
               ref: ${{ github.event.workflow_run.head_branch }}
           # ... security scan steps from standards file

      tests:
        if: ${{ github.event.workflow_run.conclusion == 'success' }}
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
            with:
              ref: ${{ github.event.workflow_run.head_branch }}
          - name: Run tests
            if: ${{ hashFiles('tests/**') != '' }}
            run: |
              # ... test steps from standards file

       # Deployment Job
       deploy-prod:
         if: ${{ github.event.workflow_run.conclusion == 'success' }}
         needs: [lint, security, tests]
         runs-on: ubuntu-latest
         environment: prod
         steps:
           - uses: actions/checkout@v4
             with:
               ref: ${{ github.event.workflow_run.head_branch }}
           # ... deployment steps from standards file
     ```

   - **AWS Credentials Configuration (Mandatory for AWS-related workflows):**
     If any workflow step requires AWS CLI credentials, include OIDC configuration:

     ```yaml
     - name: Configure AWS credentials via OIDC
       uses: aws-actions/configure-aws-credentials@v4
       with:
         role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
         aws-region: ${{ vars.AWS_REGION }}
     ```

     - Place this step as one of the first steps in any job that performs AWS operations
     - Require `permissions: id-token: write` at the workflow level

   - **Path Filters:**
     If a workflow uses `paths` filters, always include the workflow file itself:

     ```yaml
     on:
       push:
         branches: [develop]
         paths:
           - "src/**"
           - ".github/workflows/{code-type}-dev.yml"
     ```

   - **Concurrency Control:**
     Use concurrency groups to avoid overlapping deployments per environment:

     ```yaml
     concurrency:
       group: deploy-{code-type}-${{ github.ref }}-{environment}
       cancel-in-progress: false
     ```

     Note: Replace `{environment}` with the actual environment name (dev, test, or prod)

   - **Automation of Manual Steps (Mandatory):**
     All manual steps that can be automated MUST be included:

     - Uploading files to S3 buckets
     - Syncing content between storage locations
     - Copying or transferring files between services
     - Running deployment scripts or commands
     - Any repetitive operational tasks

   - **Dependency Handling Patterns:**

     **CRITICAL**: For comprehensive dependency handling patterns, see `workflow-dependency-handling.md`. This document includes:

     - Single dependency patterns (upstream/downstream workflows)
     - Multiple dependencies patterns
     - Artifact passing methods (decision tree and all 5 methods)
     - Environment-specific considerations
     - Best practices and troubleshooting

     **Quick Reference**: When implementing dependencies:

     1. Use `workflow_run` triggers to wait for upstream workflows
     2. Download artifacts BEFORE deployment operations
     3. Place artifacts where deployment code expects them
     4. Verify artifacts exist before using them
     5. Follow patterns from `workflow-dependency-handling.md` for specific implementation details

7. **Apply Language-Specific Standards:**

   - For each detected code type, read and apply the complete content from `{code-type}-standards.md`
   - Use the exact job names, steps, and patterns specified in the standards file
   - Do not modify or summarize the standards - use them as written
   - **CRITICAL - For Terraform Workflows**:
     - **MANDATORY Dependency Check**: Before generating deployment job, check if Terraform has dependencies:
       - Review Phase 1 dependency map
       - Scan Terraform `.tf` files for artifact references (e.g., `filename = "lambda_function.zip"`)
       - If dependencies exist, deployment job MUST include dependency handling steps from `terraform-standards.md`
     - **MANDATORY Steps**: If dependencies detected, deployment job MUST include (in order):
       1. Download artifacts step (from `terraform-standards.md` step 2)
       2. Place artifacts step (from `terraform-standards.md` step 3)
       3. Verify artifacts step (from `terraform-standards.md` step 4)
     - **DO NOT SKIP**: These steps are mandatory, not optional - they ensure Terraform has required artifacts
   - If a standards file is missing, create it with appropriate CI/CD patterns for that code type

8. **Document Dependency Handling:**

   - For each dependency relationship identified in Phase 1:
     - Document which upstream workflow must complete first
     - Document which downstream workflow waits for it
     - Document what artifacts are passed between workflows
     - Document how artifacts are passed (GitHub Actions artifacts, S3, etc.)
   - Example: "Terraform-dev workflow waits for Python-dev workflow to complete and download lambda-package-dev artifact"

9. **Validate Workflow Linting and Dependency Handling (MANDATORY):**

   - **CRITICAL**: Before presenting preview, validate all generated workflow files for linting errors:
     - Check YAML syntax validity
     - Verify all GitHub Actions expressions use `${{ }}` syntax (especially `hashFiles`)
     - Verify no missing required fields (name, on, jobs, runs-on, etc.)
     - Check for valid job dependencies (no circular dependencies, all referenced jobs exist)
     - Verify workflow trigger syntax is correct
     - Check environment names are valid
     - Verify artifact paths and names are correct
   - **CRITICAL - Dependency Handling Validation** (MANDATORY for Terraform workflows):
     - **For each Terraform workflow generated**:
       - Check if Terraform code references artifacts (scan `.tf` files for `filename = "*.zip"`, `source = "*.zip"`, etc.)
       - Check Phase 1 dependency map for Terraform dependencies
       - **If dependencies detected**: Verify deployment job includes ALL mandatory dependency handling steps:
         1. Download artifacts step (from `terraform-standards.md`)
         2. Place artifacts step (from `terraform-standards.md`)
         3. Verify artifacts step (from `terraform-standards.md`)
       - **If dependencies detected but steps missing**: Add missing steps immediately - DO NOT proceed without them
       - **Validation Rule**: If Terraform code has `filename = "lambda_function.zip"` or similar, dependency handling steps MUST be present
   - **If linting errors are found**: Fix them immediately before proceeding
   - **If dependency handling steps are missing**: Add them immediately before proceeding
   - **DO NOT proceed to preview if workflows have linting errors OR missing dependency handling steps**

10. **Present Workflow YAML Preview:**

    - Show summarized YAML contents for all generated workflow files:
      - **If orchestrators were generated**:
        - `orchestrator-dev.yml`, `orchestrator-test.yml`, `orchestrator-prd.yml`
        - Show execution order and how orchestrators manage dependencies
    - `{code-type}-dev.yml` for each detected code type
    - `{code-type}-test.yml` for each detected code type
    - `{code-type}-prd.yml` for each detected code type

- Include key jobs (CI jobs + deployment job), triggers, environments, permissions, and artifact passing
- **Highlight dependency handling**:
- Show how orchestrator manages execution order and artifact passing
  - Show artifact download/upload steps
  - Show how artifacts are passed to deployment steps
- List any workflows that were modified or removed
- Highlight the environment-specific structure (3 files per code type, plus orchestrators)
  - **Show dependency graph**: Visual representation of which workflows depend on others
- **Show execution order**: Show the execution order determined by topological sort
  - **Confirm linting validation**: State that all workflows have been validated and are free of linting errors

11. **Checkpoint:**
    - Prompt user to confirm: "Proceed to generate/update environment-specific CI/CD workflows (dev/test/prd) with dependency handling and protections for all detected code types?"
    - Wait for confirmation.
