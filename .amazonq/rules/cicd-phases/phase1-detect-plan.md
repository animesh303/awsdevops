# CICD Workflow Generation Phase 1: Detect & Plan

## Purpose

Scan repository for ALL code types (Python, Terraform, JavaScript, Java, Go, Docker, Kubernetes, etc.), load and analyze requirements files to understand dependencies, analyze existing workflows, and create a plan for a single production CI/CD workflow triggered by main branch changes.

## Plan Document Location

Plan documents are created in `.cicd-docs/` directory:

- Detection plan: `.cicd-docs/detection-plan.md`
- Workflow generation plan: `.cicd-docs/workflow-generation-plan.md`
- Review notes: `.cicd-docs/review-notes.md`

## Steps

1. **Load Requirements Files for Dependency Analysis:**

   - **Scan for Requirements Files**:

     - Check `.code-docs/requirements/` directory
     - Check `.requirements/` directory (alternative location)
     - Load all `*_requirements.md`, `*-analysis.md`, and `*-code-analysis.md` files

   - **Extract Dependency Information**:

     - Read requirements files to understand relationships between code artifacts
     - Identify dependencies: e.g., "Terraform infrastructure depends on Python Lambda deployment package"
     - Map dependencies using structured format: `{code-type: "terraform", depends_on: "python", artifacts: ["lambda-package.zip"]}`
     - For human-readable summaries, use arrow notation: `terraform → depends on → python`

   - **Document Dependencies**:
     - Create dependency map in the plan document
     - Store in cicd-state.md as array: `[{code-type: "terraform", depends_on: "python", artifacts: ["lambda-package.zip"]}, ...]`
     - Identify which workflows must wait for others to complete
     - Note artifact requirements

2. **Scan Project Root and Subdirectories for Code Types:**

   - **Python**: Detect `.py` files, `requirements.txt`, `setup.py`, `pyproject.toml`, `Pipfile`
   - **Terraform**: Detect `.tf`, `.tfvars` files, `terraform/` directories
   - **JavaScript/TypeScript**: Detect `.js`, `.jsx`, `.ts`, `.tsx` files, `package.json`, `node_modules/`
   - **Java**: Detect `.java` files, `pom.xml`, `build.gradle`, Maven/Gradle directories
   - **Go**: Detect `.go` files, `go.mod`, `go.sum`
   - **Docker**: Detect `Dockerfile`, `docker-compose.yml`, `.dockerignore`
   - **Kubernetes**: Detect `.yaml`/`.yml` files in `k8s/`, `kubernetes/`, `manifests/` directories
   - **CloudFormation**: Detect `.yaml`/`.yml` files with CloudFormation templates, `cfn/` directories
   - **CDK**: Detect `cdk.json`, `cdk/` directories, CDK code files
   - List specific subpaths for each detected code type

3. **Analyze Existing Workflows:**

   - Scan `.github/workflows/` directory for existing workflow files (if directory exists)
   - **If `.github/workflows/` directory exists and contains files**:
     - Document existing workflow patterns for reference
     - Note: These workflows will be replaced with newly generated workflows
   - **If `.github/workflows/` directory doesn't exist or is empty**: No existing workflows to analyze

4. **Identify Detected Code Types:**

   - Create a summary of all detected code types with their locations
   - Example: "Python detected in `src/`; Terraform detected in `iac/terraform/`"
   - Cross-reference with Requirements: Verify detected code types match requirements analysis
   - Validate Dependencies: Ensure dependency relationships from requirements are valid

5. **Analyze Code Dependencies:**

   - **Load Artifact Mapping** (PREFERRED METHOD):

     - **CRITICAL**: First check if `.code-docs/artifact-mappings.json` exists
     - If mapping file exists:
       - Read and parse the JSON file
       - Extract dependency information from `mappings` array
       - Use `lambda_functions` array to identify all Lambda functions
       - Use `terraform_resources` array to identify all Terraform resources that need artifacts
     - If mapping file does not exist, fall back to code analysis (below)

   - **Build Dependency Map**:

     - For each code type, identify what it depends on (from requirements analysis AND code analysis)
     - **CRITICAL - Two Types of Dependencies**:
       1. **Artifact Dependency**: Code type A needs an artifact from code type B's build job
          - Example: Terraform needs Lambda zip file from Python build
          - Job dependency: `A-deploy` needs `B-build` (not `B-deploy`)
       2. **Infrastructure Dependency**: Code type A's deploy needs infrastructure created by code type B's deploy
          - Example: Python deploy needs Lambda function to exist (created by Terraform deploy)
          - Job dependency: `A-deploy` needs `B-deploy`
     - **Code Analysis for Dependencies** (FALLBACK if mapping file not available):
       - **Terraform Code Analysis**: Scan all `.tf` files for artifact references:
         - Search for `filename = "lambda_function.zip"` or similar patterns
         - Search for `source = "*.zip"` or `archive_path = "*.zip"`
         - If Terraform references `.zip` files, Lambda packages, or other artifacts, mark as **artifact dependency**
       - **Python/Application Code Analysis**: Scan deploy logic for infrastructure requirements:
         - If deploy job updates/creates resources that Terraform creates (e.g., Lambda function), mark as **infrastructure dependency**
         - Example: Python deploy uses `aws lambda update-function-code` or `aws lambda create-function` → needs Terraform to create function first
       - **Docker Code Analysis**: Scan Dockerfiles for `COPY` or `ADD` commands referencing code artifacts
       - **Kubernetes Code Analysis**: Scan manifests for image references that need to be built
       - **General Pattern**:
         - If code type A references artifacts that code type B produces → **artifact dependency** (A-deploy needs B-build)
         - If code type A's deploy needs infrastructure that code type B's deploy creates → **infrastructure dependency** (A-deploy needs B-deploy)
     - **When Using Mapping File**: Extract dependency information directly from mapping
       - **Artifact Dependency Detection**:
         - If `terraform_resources` array contains entries with `depends_on_lambda` or `artifact_reference` → Terraform has artifact dependency on Python
         - Job dependency: `terraform-deploy` needs `python-build`
       - **Infrastructure Dependency Detection**:
         - If `lambda_functions` array exists AND Terraform creates those functions → Python deploy has infrastructure dependency on Terraform
         - Check if Python deploy job updates/creates Lambda functions that Terraform creates
         - Job dependency: `python-deploy` needs `terraform-deploy`
     - Document build order: e.g., "Python Lambda must be built before Terraform deployment"
     - Document infrastructure order: e.g., "Python deploy must wait for Terraform to create Lambda function"
     - Identify artifact requirements: what artifacts need to be produced and consumed
     - Identify infrastructure requirements: what infrastructure must exist before deployment

   - **Workflow Dependency Requirements**:
     - Determine which jobs must wait for others using `needs:` dependencies
     - **Artifact Dependencies**: Downstream deploy jobs need upstream build jobs (e.g., `terraform-deploy` needs `python-build`)
     - **Infrastructure Dependencies**: Deploy jobs need upstream deploy jobs (e.g., `python-deploy` needs `terraform-deploy`)
     - Identify which artifacts need to be uploaded/downloaded between jobs
     - **When Using Mapping File**: Use exact artifact names from mapping
     - Document artifact passing requirements (e.g., Lambda zip file path, Docker image tag)
     - Document infrastructure creation order (e.g., Terraform creates Lambda function before Python updates it)
     - **MANDATORY**: If dependencies are detected, they MUST be implemented as job dependencies in the unified workflow

6. **Draft Single Production Workflow Plan:**

   Plan **one unified production workflow file** (`.github/workflows/ci-cd.yml`) that contains jobs for ALL detected code types:

   - **Unified Production Workflow** (`ci-cd.yml`):
     - **Trigger**: Pushes to `main` branch (and `workflow_dispatch` for manual trigger)
     - **Environment**: Single production environment only
     - Contains jobs for each code type sequenced by dependencies
     - Each code type has: CI jobs (lint, security, test), build job, and deploy job
     - Uses GitHub `environment` for production secrets and protection rules

   **Document Dependency Handling:**

   - For each dependency relationship, specify:
     - **Artifact Dependencies**:
       - Which code type produces artifacts (upstream build job)
       - Which code type consumes artifacts (downstream deploy job)
       - What artifacts need to be passed (e.g., Lambda zip file, Docker image tag)
       - How artifacts will be passed (GitHub Actions artifacts within same workflow)
       - Example: "Terraform deploy job must wait for Python build job to complete and download Lambda zip artifact"
     - **Infrastructure Dependencies**:
       - Which code type creates infrastructure (upstream deploy job)
       - Which code type needs infrastructure to exist (downstream deploy job)
       - What infrastructure must exist first (e.g., Lambda function, S3 bucket)
       - Example: "Python deploy job must wait for Terraform deploy job to create Lambda function before updating function code"
   - **Calculate Execution Order**: Use topological sort to determine the order of code types
     - Code types with no dependencies run first
     - Dependent code types run after their dependencies

   Document workflow modifications:

   - List existing workflows that need modification
   - List existing workflows that should be removed
   - List new unified workflow that needs to be created (1 file: `ci-cd.yml`)
   - Document job dependencies using `needs:` to enforce execution order

7. **User Plan Review Checkpoint:**

   - Present summary of:
     - All detected code types with locations
     - Requirements and dependencies identified
     - Dependency map (which code types depend on others)
     - Job dependency order (which jobs must run before others)
     - Existing workflows analysis (keep/modify/remove)
     - Planned single production workflow (1 file: `ci-cd.yml` containing all code types)
     - Execution order of code types (based on dependencies)
     - Artifact passing strategy (how dependencies will be handled between jobs in same workflow)
     - **Environment**: Single production environment (triggered by main branch)
   - Ask: "Proceed to generate single production workflow as planned?"
   - Wait for confirmation to proceed.

8. **Persist Phase Results (State & Audit):**

   - Write detected code types, dependency map, existing workflow analysis, and the draft plan to `.cicd-docs/cicd-state.md`
   - Include dependency relationships and artifact requirements in the state file
   - Record the user confirmation decision with timestamp in `.cicd-docs/audit.md`
   - **Update plan checkboxes** - Mark completed steps [x] in `.cicd-docs/detection-plan.md`
   - **Update cicd-state.md** - Update Phase 1 status after completion
