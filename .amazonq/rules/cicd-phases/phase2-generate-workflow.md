# CICD Workflow Generation Phase 2: Generate Workflow Files

## Purpose

Render GitHub Actions workflow files (YAML) for ALL detected code types as **three separate workflow files per environment** (dev, test, prd). Each workflow contains CI jobs and deployment job for that specific environment. **Handle dependencies between code artifacts** (from requirements analysis) by enforcing workflow execution order and artifact passing. Ensure all required CI/CD and code scanning steps are present. Handle existing workflows by modifying or removing as needed.

## Plan Document Location

**CRITICAL**: Plan documents are created in `.cicd-docs/` directory (preferred) or `.amazonq/rules/cicd-phases/` (legacy fallback):

- Workflow generation plan: `.cicd-docs/workflow-generation-plan.md` (or `.cicd-docs/phase2-plan.md`)

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

2. **Analyze and Manage Existing Workflows:**

   - Review existing workflows in `.github/workflows/` directory
   - **If this is a regeneration request**: Remove all existing workflows that match the pattern `{code-type}-{environment}.yml` (dev/test/prd) for detected code types, then regenerate them fresh
   - For each existing workflow:
     - **Keep and Modify**: If it matches a detected code type and environment, AND this is NOT a regeneration request, update it to follow the new environment-specific structure
     - **Remove**: If it doesn't match any detected code type, is obsolete, OR if this is a regeneration request (will be replaced with new workflows)
   - **Removal Strategy**:
     - For regeneration: Remove matching workflows first, then generate new ones
     - For normal generation: Remove only obsolete workflows, modify existing ones
   - Document all changes (modifications/removals) in the plan, including whether this is a regeneration

3. **Read Language-Specific Standards:**

   - For each detected code type, read the corresponding standards file:
     - `.amazonq/rules/cicd-phases/{code-type}-standards.md`
   - If standards file does not exist, create it following the pattern of existing standards files
   - **CRITICAL**: Use the complete content from the standards file - do not summarize or paraphrase

4. **Generate Environment-Specific Workflows Per Detected Code Type:**

   **IMPORTANT**: When generating workflows, respect dependency order. Workflows that depend on others must:

   - Use `workflow_run` triggers to wait for upstream workflows to complete
   - Download artifacts from upstream workflows when needed
   - Reference artifact locations (paths, URLs, tags) from upstream workflows

   For each detected code type, generate **three separate workflow files**:

   **Deploy to Dev Workflow** (`.github/workflows/{code-type}-dev.yml`):

   - **Workflow Trigger**:
     - **If no dependencies**: Trigger on push to `develop` branch
       ```yaml
       on:
         push:
           branches: [develop]
       ```
     - **If has dependencies**: Trigger via `workflow_run` to wait for upstream workflows, OR allow push trigger as fallback
       ```yaml
       on:
         workflow_run:
           workflows: ["{Upstream Code Type} Dev"] # Wait for upstream
           types: [completed]
           branches: [develop]
         push:
           branches: [develop] # Fallback trigger
       ```
     - **Note**: GitHub Actions doesn't support conditions at workflow trigger level. Conditions must be at job level. If using `workflow_run`, add condition check at job level: `if: ${{ github.event.workflow_run.conclusion == 'success' || github.event_name == 'push' }}`
   - **CI Jobs**:

     - Lint, test, security scan, artifact generation
     - Organize workflow logic into multiple jobs with clear dependencies using `needs:`
     - Prefer fast-fail by running independent jobs in parallel
     - Upload SARIF results and build artifacts
     - Follow patterns from `{code-type}-standards.md`

   - **Deploy to Dev Job**:
     - **Needs**: All CI jobs must succeed
     - **Dependency Handling**:
       - If this code type depends on others, add `workflow_run` trigger to wait for upstream workflows
       - Download artifacts from upstream workflows (e.g., Lambda zip from Python workflow)
       - Pass artifact information (paths, URLs, tags) to deployment steps
     - Deploys to Development environment
     - Uses GitHub `environment: dev` for secrets and protection rules
     - Downloads CI artifacts if needed for deployment
     - **Upload deployment artifacts** for downstream workflows (if this code type is a dependency)
     - Follow patterns from `{code-type}-standards.md`

   **Deploy to Test Workflow** (`.github/workflows/{code-type}-test.yml`):

   - **Workflow Trigger**:
     - **If no dependencies**: Trigger on push to `main` branch
       ```yaml
       on:
         push:
           branches: [main]
       ```
     - **If has dependencies**: Trigger via `workflow_run` to wait for upstream workflows, OR allow push trigger as fallback
       ```yaml
       on:
         workflow_run:
           workflows: ["{Upstream Code Type} Test"] # Wait for upstream
           types: [completed]
           branches: [main]
         push:
           branches: [main] # Fallback trigger
       ```
     - **Note**: GitHub Actions doesn't support conditions at workflow trigger level. Conditions must be at job level. If using `workflow_run`, add condition check at job level: `if: ${{ github.event.workflow_run.conclusion == 'success' || github.event_name == 'push' }}`
   - **CI Jobs**:

     - Lint, test, security scan, artifact generation
     - Organize workflow logic into multiple jobs with clear dependencies using `needs:`
     - Prefer fast-fail by running independent jobs in parallel
     - Upload SARIF results and build artifacts
     - Follow patterns from `{code-type}-standards.md`
     - **Checkout Step**: For push triggers, standard checkout is sufficient. For workflow_run triggers, checkout from triggering workflow branch:
       ```yaml
       - uses: actions/checkout@v4
         # For workflow_run: add with: ref: ${{ github.event.workflow_run.head_branch }}
       ```

   - **Deploy to Test Job**:
     - **Needs**: All CI jobs must succeed
     - **Dependency Handling**:
       - If this code type depends on others, ensure upstream workflows completed successfully
       - Download artifacts from upstream workflows (e.g., Lambda zip from Python workflow)
       - Pass artifact information to deployment steps
     - Deploys to Test environment
     - Uses GitHub `environment: test` for secrets and protection rules
     - Downloads CI artifacts if needed for deployment
     - **Upload deployment artifacts** for downstream workflows (if this code type is a dependency)
     - Follow patterns from `{code-type}-standards.md`

   **Deploy to Prod Workflow** (`.github/workflows/{code-type}-prd.yml`):

   - **Workflow Trigger**:
     ```yaml
     on:
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
     - Upload SARIF results and build artifacts
     - Follow patterns from `{code-type}-standards.md`
     - **CRITICAL - Checkout Step**: EVERY job (CI and deployment) MUST have checkout as the FIRST step:
       ```yaml
       - uses: actions/checkout@v4
         with:
           ref: ${{ github.event.workflow_run.head_branch }}
       ```
       This is required because `workflow_run` triggers don't automatically checkout code

   - **Deploy to Prod Job**:
     - **Needs**: All CI jobs must succeed
     - **Dependency Handling**:
       - If this code type depends on others, ensure upstream workflows completed successfully
       - Download artifacts from upstream workflows (e.g., Lambda zip from Python workflow)
       - Pass artifact information to deployment steps
     - Deploys to Production environment
     - Uses GitHub `environment: prod` with protection rules/approvals for promotion gates
     - Downloads CI artifacts if needed for deployment
     - **Upload deployment artifacts** for downstream workflows (if this code type is a dependency)
     - Follow patterns from `{code-type}-standards.md`
     - Protected with GitHub environment protection rules

5. **Workflow Structure Requirements:**

   - **Dev Workflow Structure Example:**

     ```yaml
     name: {Code Type} Dev

     on:
       push:
         branches: [develop]

     permissions:
       contents: read
       security-events: read
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
         if: hashFiles('tests/**') != ''
         steps:
           # ... test steps from standards file

       upload-sarif:
         needs: [lint, security]
         runs-on: ubuntu-latest
         steps:
           # ... SARIF upload steps from standards file

       # Deployment Job
       deploy-dev:
         needs: [lint, security, tests, upload-sarif]
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
       security-events: read
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
         if: hashFiles('tests/**') != ''
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v4
           # ... test steps from standards file

       upload-sarif:
         needs: [lint, security]
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v4
           # ... SARIF upload steps from standards file

       # Deployment Job
       deploy-test:
         needs: [lint, security, tests, upload-sarif]
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
       security-events: read
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
         if: ${{ github.event.workflow_run.conclusion == 'success' && hashFiles('tests/**') != '' }}
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v4
             with:
               ref: ${{ github.event.workflow_run.head_branch }}
           # ... test steps from standards file

       upload-sarif:
         if: ${{ github.event.workflow_run.conclusion == 'success' }}
         needs: [lint, security]
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v4
             with:
               ref: ${{ github.event.workflow_run.head_branch }}
           # ... SARIF upload steps from standards file

       # Deployment Job
       deploy-prod:
         if: ${{ github.event.workflow_run.conclusion == 'success' }}
         needs: [lint, security, tests, upload-sarif]
         runs-on: ubuntu-latest
         environment: prod
         steps:
           - uses: actions/checkout@v4
             with:
               ref: ${{ github.event.workflow_run.head_branch }}
           # ... deployment steps from standards file
     ```

   - **Permissions for SARIF Upload:**
     Workflows that upload SARIF results MUST declare permissions:

     ```yaml
     permissions:
       contents: read
       security-events: read
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
       group: deploy-{code-type}-${{ github.ref }}-${{ github.environment }}
       cancel-in-progress: false
     ```

   - **Automation of Manual Steps (Mandatory):**
     All manual steps that can be automated MUST be included:

     - Uploading files to S3 buckets
     - Syncing content between storage locations
     - Copying or transferring files between services
     - Running deployment scripts or commands
     - Any repetitive operational tasks

   - **Dependency Handling Patterns:**

     **When Code Type A depends on Code Type B** (e.g., Terraform depends on Python Lambda):

     **Upstream Workflow (Code Type B - Python)**:

     - Build and package artifacts (e.g., Lambda zip file)
     - Upload artifacts using `actions/upload-artifact@v4`:
       ```yaml
       - name: Upload Lambda package
         uses: actions/upload-artifact@v4
         with:
           name: lambda-package
           path: lambda-package.zip
           retention-days: 1
       ```
     - Or upload to S3/container registry for cross-workflow access
     - Export artifact information (paths, URLs, tags) as workflow outputs or environment variables

     **Downstream Workflow (Code Type A - Terraform)**:

     - Add `workflow_run` trigger to wait for upstream workflow:
       ```yaml
       on:
         workflow_run:
           workflows: ["Python Dev"] # Wait for Python workflow
           types: [completed]
           branches: [develop]
       ```
     - Download artifacts from upstream workflow:
       ```yaml
       - name: Download Lambda package from upstream workflow
         uses: actions/download-artifact@v4
         with:
           name: lambda-package
           run-id: ${{ github.event.workflow_run.id }}
           github-token: ${{ secrets.GITHUB_TOKEN }}
       ```
     - Or download from S3/container registry if artifacts were stored there
     - Use artifact information in deployment steps (e.g., pass Lambda zip path to Terraform)

     **Multiple Dependencies**:

     - If a code type depends on multiple others, use `workflow_run` triggers for all upstream workflows:
       ```yaml
       on:
         workflow_run:
           workflows: ["Python Dev", "Docker Dev"] # Wait for all upstream workflows
           types: [completed]
           branches: [develop]
       ```
     - **Important**: When multiple `workflow_run` triggers exist, `github.event.workflow_run.id` refers to the workflow that triggered this run. To download artifacts from specific upstream workflows:
       - Option 1: Use workflow outputs/environment variables from upstream workflows to pass artifact information
       - Option 2: Store artifacts in S3/container registry with predictable naming and download from there
       - Option 3: Use GitHub API to find the specific workflow run ID for each dependency
     - Download artifacts from all upstream workflows
     - Combine artifacts as needed for deployment

     **Artifact Passing Methods** (prioritized by use case):

     1. **GitHub Actions Artifacts** (Preferred for same-run dependencies):

        - Use `actions/upload-artifact@v4` and `actions/download-artifact@v4`
        - Works within same workflow run
        - Limited retention (default 1 day, configurable up to 90 days)
        - Use when artifacts are consumed within short time window

     2. **Cross-Workflow Artifacts** (Preferred for workflow_run triggers with single dependency):

        - Use `actions/download-artifact@v4` with `run-id` and `github-token`
        - Works for `workflow_run` triggers when downloading from the triggering workflow
        - **Limitation**: When multiple dependencies exist, `github.event.workflow_run.id` only refers to one workflow
        - Use when single upstream dependency and artifacts consumed quickly

     3. **S3/Storage** (Preferred for multiple dependencies or long retention):

        - Upload to S3 bucket with predictable naming (e.g., `{artifact-name}-{environment}-{commit-sha}`)
        - Download from S3 in downstream workflow
        - Better for multiple dependencies as each workflow can upload independently
        - Use when artifacts need longer retention or multiple workflows depend on same artifact

     4. **Container Registry** (For Docker images):

        - Push Docker images with tags to registry (ECR, Docker Hub, etc.)
        - Reference image tags in downstream workflows
        - Use for containerized applications

     5. **Environment Variables/Workflow Outputs** (For artifact metadata):
        - Pass artifact paths/URLs via workflow outputs or GitHub secrets
        - Use when artifact location/URL needs to be passed between workflows
        - Combine with artifact storage methods above

6. **Apply Language-Specific Standards:**

   - For each detected code type, read and apply the complete content from `{code-type}-standards.md`
   - Use the exact job names, steps, and patterns specified in the standards file
   - Do not modify or summarize the standards - use them as written
   - If a standards file is missing, create it with appropriate CI/CD patterns for that code type

7. **Document Dependency Handling:**

   - For each dependency relationship identified in Phase 1:
     - Document which upstream workflow must complete first
     - Document which downstream workflow waits for it
     - Document what artifacts are passed between workflows
     - Document how artifacts are passed (GitHub Actions artifacts, S3, etc.)
   - Example: "Terraform-dev workflow waits for Python-dev workflow to complete and download lambda-package-dev artifact"

8. **Present Workflow YAML Preview:**

   - Show summarized YAML contents for all generated environment-specific workflow files:
     - `{code-type}-dev.yml` for each detected code type
     - `{code-type}-test.yml` for each detected code type
     - `{code-type}-prd.yml` for each detected code type
   - Include key jobs (CI jobs + deployment job), triggers, environments, permissions, and artifact passing
   - **Highlight dependency handling**:
     - Show `workflow_run` triggers for dependent workflows
     - Show artifact download/upload steps
     - Show how artifacts are passed to deployment steps
   - List any workflows that were modified or removed
   - Highlight the environment-specific structure (3 files per code type)
   - **Show dependency graph**: Visual representation of which workflows depend on others

9. **Checkpoint:**
   - Prompt user to confirm: "Proceed to generate/update environment-specific CI/CD workflows (dev/test/prd) with dependency handling and protections for all detected code types?"
   - Wait for confirmation.
