# CICD Workflow Generation Phase 2: Generate Workflow Files

## Purpose

Generate a **single unified production GitHub Actions workflow file** (YAML) that contains jobs for ALL detected code types. The workflow triggers on pushes to `main` branch and deploys to a single production environment. Jobs are sequenced based on dependencies - code types with no dependencies run first, followed by dependent code types. Handle dependencies between code artifacts by enforcing job execution order and artifact passing within the same workflow. Ensure all required CI/CD and code scanning steps are present.

## Plan Document Location

Plan documents are created in `.cicd-docs/` directory:

- Workflow generation plan: `.cicd-docs/workflow-generation-plan.md`

## MANDATORY: GitHub Actions Expression Syntax

**CRITICAL**: When using GitHub Actions functions like `hashFiles`, `always()`, `success()`, etc., they MUST always be wrapped in `${{ }}` expression syntax.

- **Correct**: `if: ${{ hashFiles('tests/**') != '' }}`
- **Incorrect**: `if: hashFiles('tests/**') != ''` (will cause "Unrecognized function" error)

**All GitHub Actions expressions must use `${{ }}` syntax**, including:

- `hashFiles()` - Check if files exist or have changed
- `always()`, `success()`, `failure()`, `cancelled()` - Job status checks
- `github.event.*` - Event context access

**CRITICAL - `hashFiles()` Context Limitation**: The `hashFiles()` function is **ONLY available in step-level `if` conditions** (`jobs.<job>.steps[*].if`), **NOT at the job level** (`jobs.<job>.if`).

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

## Steps

1. **Load Dependency Information from Phase 1:**

   - **Read Dependency Map**:

     - Load dependency relationships from Phase 1 plan document
     - Load dependency map from `.cicd-docs/cicd-state.md` if available
     - Understand which code types depend on others (e.g., `terraform → depends on → python`)

   - **Identify Artifact Requirements**:
     - For each dependency, identify what artifacts need to be passed
     - Example: Terraform needs Python Lambda zip file location
     - Document artifact types: zip files, Docker images, build artifacts, etc.

2. **Verify Clean State:**

   - **For regeneration requests**: `.github/workflows/` directory should already be deleted (handled in Welcome phase), so no existing workflows to manage
   - **For new generation**: If `.github/workflows/` directory exists with files, they will be replaced with newly generated workflows
   - **No complex removal logic needed**: Simply generate a single unified workflow file - it will overwrite any existing workflow file with the same name
   - Document that a single unified workflow is being generated containing all code types

3. **Read Language-Specific Standards:**

   - For each detected code type, read the corresponding standards file:
     - `.amazonq/rules/cicd-phases/{code-type}-standards.mdc`
   - If standards file does not exist, create it following the pattern of existing standards files
   - **CRITICAL**: Use the complete content from the standards file - do not summarize or paraphrase

4. **Calculate Execution Order Based on Dependencies:**

   - **Build Dependency Graph**:
     - Use topological sort to determine correct execution order
     - Start with code types that have no dependencies (leaf nodes)
     - Process code types in order: dependencies first, dependents after
     - Example: If `terraform → python` and `kubernetes → docker → python`, order is: `[python, docker, terraform, kubernetes]`
   - **Document Execution Order**: Store the ordered list of code types in the plan document

5. **Generate Single Production Workflow:**

   Generate **one production workflow file** (`.github/workflows/ci-cd.yml`) that contains jobs for ALL detected code types:

   **Workflow Structure** (`.github/workflows/ci-cd.yml`):

   - **Workflow Trigger** (main branch only):
     ```yaml
     on:
       push:
         branches: [main]
       workflow_dispatch:
     ```
   - **Environment**: Single production environment (all deploy jobs use same environment)

   - **For Each Code Type (in dependency order)**, create job groups:
     - **CI Jobs** (run in parallel for each code type):
       - `{code-type}-lint` - Lint job
       - `{code-type}-security` - Security scan job
       - `{code-type}-test` - Test job
       - These jobs can run in parallel (no dependencies between them)
     - **Build Job** (runs after CI jobs):
       - `{code-type}-build` - Build and package artifacts
       - **Needs**: All CI jobs for this code type (`needs: [{code-type}-lint, {code-type}-security, {code-type}-test]`)
       - Uploads artifacts using `actions/upload-artifact@v4`
     - **Deploy Job** (runs after build and upstream dependencies):
       - `{code-type}-deploy` - Deploy to environment
       - **Needs**:
         - All CI jobs for this code type
         - Build job for this code type
         - **CRITICAL - Two Types of Dependencies**:
           1. **Artifact Dependencies**: If this code type needs artifacts from other code types
              - Example: Terraform needs Python Lambda package → `terraform-deploy` needs `python-build` (NOT `python-deploy`)
              - Wait for upstream **build jobs** that produce required artifacts
           2. **Infrastructure Dependencies**: If this code type's deploy needs infrastructure created by other code types
              - Example: Python deploy needs Lambda function to exist (created by Terraform) → `python-deploy` needs `terraform-deploy`
              - Wait for upstream **deploy jobs** that create required infrastructure
         - **Dependency Detection from Phase 1**:
           - Use dependency map from Phase 1 to determine correct job dependencies
           - If artifact-mappings.json shows Terraform needs Python artifact → `terraform-deploy` needs `python-build`
           - If Python deploy updates Lambda functions that Terraform creates → `python-deploy` needs `terraform-deploy`
         - **Dependency Handling** (CRITICAL - MANDATORY if dependencies detected):
         - **MANDATORY CHECK**: If Phase 1 detected dependencies for this code type, dependency handling steps MUST be included
         - **PREFERRED - Local Build Placement**: For Lambda functions and similar artifacts, the PREFERRED approach is to build artifacts directly where Terraform expects them:
           - **Python Lambda Example**: Build Lambda package directly in Terraform directory (e.g., `iac/terraform/lambda_function.zip`) during Python build job
           - **Benefits**: Terraform deploys Lambda source directly, no artifact upload/download needed, simpler workflow
           - **Implementation**: Upstream build job builds artifact in Terraform directory, Terraform deploy job verifies and uses it directly
           - **Terraform Deploys Source**: Terraform's `source_code_hash` automatically detects changes and updates Lambda function code
           - **No Separate Deploy Job**: When Terraform manages Lambda, no separate `python-deploy` job is needed
         - **ALTERNATIVE - Artifact Upload/Download**: If local build placement is not feasible, use artifact upload/download:
           - **Load Artifact Mapping** (PREFERRED):
             - **CRITICAL**: Read `.code-docs/artifact-mappings.json` if it exists
             - Extract dependency information from `mappings` array
             - For each mapping entry:
               - Use `artifact_name` for artifact download
               - Use `artifact_destination_path` for artifact placement
           - **For Terraform workflows**: If Terraform code references artifacts OR mapping file indicates dependencies, dependency handling is MANDATORY
           - **Steps MUST include** (in this exact order):
             1. **Download artifacts from upstream build jobs FIRST** (e.g., Lambda zip from Python build job)
                - Use `actions/download-artifact@v4` with artifact name from upstream build job
                - **If mapping file exists**: Use exact artifact name from mapping
                - **If mapping file does not exist**: Use patterns from `terraform-standards.mdc` or `workflow-dependency-handling.mdc`
             2. **Place artifacts in correct location** where deployment code expects them
                - **If mapping file exists**: Use exact path from `artifact_destination_path` field
                - **If mapping file does not exist**: For Terraform, if code references `lambda_function.zip`, place it where Terraform expects it
             3. **Verify artifacts exist** before proceeding with deployment operations
             4. **Pass artifact information** to deployment steps (environment variables, Terraform variables, etc.)
         - **DO NOT SKIP**: If dependencies are detected, these steps are MANDATORY, not optional
       - Deploys to environment
       - Uses GitHub `environment` for secrets and protection rules
       - Follow patterns from `{code-type}-standards.mdc`

6. **Workflow Structure Requirements:**

   **CRITICAL**: Remember that all GitHub Actions expressions (including `hashFiles`) MUST be wrapped in `${{ }}` syntax.

   - **Unified Workflow Structure Example**:

     ```yaml
     name: CI/CD

     on:
       push:
         branches: [main]
       workflow_dispatch:

     permissions:
       contents: read
       id-token: write # For OIDC if needed

     jobs:
       # Python Code Type Jobs
       python-lint:
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v4
           # ... lint steps from python-standards.mdc

       python-security:
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v4
           # ... security scan steps from python-standards.mdc

       python-test:
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v4
           - name: Run tests
             if: ${{ hashFiles('tests/**') != '' }}
             run: |
               # ... test steps from python-standards.mdc

       python-build:
         needs: [python-lint, python-security, python-test]
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v4
           # ... build steps from python-standards.mdc
           - name: Upload Lambda package
             uses: actions/upload-artifact@v4
             with:
               name: lambda-package
               path: lambda-package.zip

       python-deploy:
         needs: [python-build]
         runs-on: ubuntu-latest
         environment: production
         steps:
           - uses: actions/checkout@v4
           - uses: actions/download-artifact@v4
             with:
               name: lambda-package
           # ... deployment steps from python-standards.mdc

       # Terraform Code Type Jobs (depends on Python)
       terraform-lint:
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v4
           # ... lint steps from terraform-standards.mdc

       terraform-security:
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v4
           # ... security scan steps from terraform-standards.mdc

       terraform-validate:
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v4
           # ... validate steps from terraform-standards.mdc

       terraform-deploy:
         needs:
           [
             terraform-lint,
             terraform-security,
             terraform-validate,
             python-deploy,
           ]
         runs-on: ubuntu-latest
         environment: production
         steps:
           - uses: actions/checkout@v4
           - name: Download Lambda package from Python build
             uses: actions/download-artifact@v4
             with:
               name: lambda-package
           - name: Place Lambda package for Terraform
             run: |
               mkdir -p ./iac/terraform
               cp ./lambda-package/lambda-package.zip ./iac/terraform/lambda_function.zip
           - name: Verify Lambda package exists
             run: |
               if [ ! -f "./iac/terraform/lambda_function.zip" ]; then
                 echo "Error: Lambda package not found"
                 exit 1
               fi
           # ... deployment steps from terraform-standards.mdc
     ```

   - **AWS Credentials Configuration** (Mandatory for AWS-related workflows):
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

   - **Path Filters**:
     If a workflow uses `paths` filters, always include the workflow file itself:

     ```yaml
     on:
       push:
         branches: [main]
         paths:
           - "src/**"
           - ".github/workflows/ci-cd.yml"
     ```

   - **Concurrency Control**:
     Use concurrency groups to avoid overlapping deployments:

     ```yaml
     concurrency:
       group: ci-cd-${{ github.ref }}
       cancel-in-progress: false
     ```

7. **Apply Language-Specific Standards:**

   - For each detected code type, read and apply the complete content from `{code-type}-standards.mdc`
   - Use the exact job names, steps, and patterns specified in the standards file
   - Do not modify or summarize the standards - use them as written
   - **CRITICAL - For Terraform Workflows with Dependencies**:
     - **MANDATORY Dependency Check**: Before generating deployment job, check if Terraform has dependencies
     - **MOST PREFERRED - Combined Job Pattern**: If Terraform depends on Python Lambda and Terraform manages the Lambda function:
       - **DO NOT** create separate `python-build` job
       - **DO** combine Python build steps and Terraform deploy steps in a single `terraform-deploy` job
       - Job waits for both Python CI jobs AND Terraform CI jobs
       - Python build steps create artifact directly where Terraform expects it (same runner)
       - Terraform deploy steps use artifact from same runner (no download needed)
       - **Benefits**: No artifact passing needed, simplest workflow, fewer jobs
       - **See**: `workflow-dependency-handling.mdc` for complete combined job pattern
     - **ALTERNATIVE - Separate Jobs**: If combined job is not feasible (e.g., build used by multiple consumers):
       - Create separate `python-build` job
       - Create `terraform-deploy` job that waits for `python-build`
       - Include dependency handling steps from `terraform-standards.mdc`
       - Use artifact upload/download or local build placement pattern
   - If a standards file is missing, create it with appropriate CI/CD patterns for that code type

8. **Document Dependency Handling:**

   - For each dependency relationship identified in Phase 1:
     - Document which upstream job must complete first
     - Document which downstream job waits for it
     - Document what artifacts are passed between jobs
     - Document how artifacts are passed (GitHub Actions artifacts within same workflow)

9. **Validate Workflow Linting and Dependency Handling (MANDATORY):**

   - **CRITICAL**: Before presenting preview, validate all generated workflow files for linting errors:
     - Check YAML syntax validity
     - Verify all GitHub Actions expressions use `${{ }}` syntax (especially `hashFiles`)
     - Verify no missing required fields (name, on, jobs, runs-on, etc.)
     - Check for valid job dependencies (no circular dependencies, all referenced jobs exist)
     - Verify workflow trigger syntax is correct
     - Check environment names are valid
     - Verify artifact paths and names are correct
   - **CRITICAL - Dependency Handling Validation** (MANDATORY for Terraform jobs):
     - **For Terraform deploy job**:
       - Check if Terraform code references artifacts (scan `.tf` files for `filename = "*.zip"`, etc.)
       - Check Phase 1 dependency map for Terraform dependencies
       - **If dependencies detected**: Verify deploy job includes ALL mandatory dependency handling steps AND has correct `needs:` dependencies
       - **If dependencies detected but steps missing**: Add missing steps immediately - DO NOT proceed without them
       - **Verify job dependencies**: Ensure `needs:` includes upstream deploy jobs (e.g., `terraform-deploy` needs `python-deploy`)
   - **MANDATORY - Pre-Validation Check**: Before generating workflow, ensure standards files do NOT use `hashFiles()` at job level
     - Check `python-standards.mdc` and other standards files for job-level `hashFiles()` usage
     - If found in standards, fix the standards file first
   - **MANDATORY - Post-Generation Validation (BLOCKING)**: After generating workflow file, perform these checks:
     - **STEP 1**: Read the generated workflow file (e.g., `.github/workflows/ci-cd.yml`)
     - **STEP 2**: Use grep or pattern matching to find all job definitions: `grep -E "^\s+[a-z-]+:\s*$" .github/workflows/ci-cd.yml`
     - **STEP 3**: For each job, check the next few lines for `if:` at same indentation as `runs-on:`
     - **STEP 4**: Pattern to detect: Job name line followed by `if:` line containing `hashFiles`
     - **STEP 5**: If detected, this is a CRITICAL BLOCKING ERROR
     - **STEP 6**: Fix by:
       - Remove job-level `if:` line
       - Add step-level `if: ${{ hashFiles('tests/**') != '' }}` to relevant steps (install test deps, run tests)
     - **STEP 7**: Re-read workflow file and verify fix
     - **STEP 8**: DO NOT proceed to preview until this validation passes
     - **Example detection pattern**:
       ```bash
       # Check for job-level if with hashFiles
       grep -A 2 "^\s\+[a-z-]*:\s*$" .github/workflows/ci-cd.yml | grep -B 1 "if:.*hashFiles"
       ```
     - **If found**: This is a BLOCKING ERROR - fix immediately
   - **If linting errors are found**: Fix them immediately before proceeding
   - **If dependency handling steps are missing**: Add them immediately before proceeding
   - **DO NOT proceed to preview if workflows have linting errors OR missing dependency handling steps**
   - **CRITICAL**: Job-level `hashFiles()` usage is a BLOCKING error - workflow will fail GitHub Actions validation
   - **ENFORCEMENT**: This validation MUST be performed after every workflow generation - no exceptions

10. **Present Workflow YAML Preview:**

    - Show summarized YAML contents for the single unified workflow file:
      - `ci-cd.yml` - Single unified workflow containing all code types
    - Include key jobs for each code type (CI jobs + build job + deployment job), triggers, environments, permissions, and artifact passing
    - **Highlight dependency handling**:
      - Show artifact download/upload steps between jobs
      - Show how artifacts are passed from upstream build jobs to downstream deploy jobs
      - Show job dependencies using `needs:` to enforce execution order
    - List any workflows that were modified or removed
    - **Show dependency graph**: Visual representation of which code types depend on others
    - **Show execution order**: Show the execution order of code types determined by dependencies
    - **Show job structure**: Show how each code type has lint/security/test jobs (parallel), build job (after CI), and deploy job (after build and upstream deploys)
    - **Confirm linting validation**: State that the workflow has been validated and is free of linting errors

11. **Checkpoint:**
    - Prompt user to confirm: "Proceed to generate single production CI/CD workflow (triggered by main branch) for all detected code types?"
    - Wait for confirmation.
    - **Update plan checkboxes** - Mark completed steps [x] in `.cicd-docs/workflow-generation-plan.md`
    - **Update cicd-state.md** - Update Phase 2 status and generated files list (should show: `.github/workflows/ci-cd.yml`)
