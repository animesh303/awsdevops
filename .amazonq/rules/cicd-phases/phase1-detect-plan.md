# CICD Workflow Generation Phase 1: Detect & Plan

## Purpose

Scan repository comprehensively for ALL code types (Python, Terraform, JavaScript, Java, Go, Docker, Kubernetes, etc.), **load and analyze requirements files to understand dependencies**, analyze existing workflows, and create a comprehensive plan for multi-environment CI/CD workflows.

## Related Files

- See `cicd-github-workflow.md` for main workflow overview
- See `session-continuity.md` for session management
- See `error-handling.md` for error scenarios
- See `validation-checklist.md` for validation criteria

## Plan Document Location

**CRITICAL**: Plan documents are created in `.cicd-docs/` directory (preferred) or `.amazonq/rules/cicd-phases/` (legacy fallback):

- Detection plan: `.cicd-docs/detection-plan.md` (or `.cicd-docs/phase1-plan.md`)
- Workflow generation plan: `.cicd-docs/workflow-generation-plan.md` (or `.cicd-docs/phase2-plan.md`)
- Review notes: `.cicd-docs/review-notes.md` (or `.cicd-docs/phase3-notes.md`)

## Steps

1. **Load Requirements Files for Dependency Analysis:**

   - **Scan for Requirements Files**:

     - Check `.code-docs/requirements/` directory
     - Check `.requirements/` directory (alternative location)
     - Load all `*_requirements.md`, `*-analysis.md`, and `*-code-analysis.md` files

   - **Extract Dependency Information**:

     - Read requirements files to understand relationships between code artifacts
     - Identify dependencies: e.g., "Terraform infrastructure depends on Python Lambda deployment package"
     - Extract build/deployment order requirements
     - Map dependencies using structured format: `{code-type: "terraform", depends_on: "python", artifacts: ["lambda-package.zip"]}`
     - Example: If requirements indicate Terraform needs Python Lambda package, document: `{code-type: "terraform", depends_on: "python", artifacts: ["lambda-package.zip"]}`
     - For human-readable summaries, use arrow notation: `terraform → depends on → python`

   - **Document Dependencies**:
     - Create dependency map in the plan document using structured format
     - Store in cicd-state.md as array: `[{code-type: "terraform", depends_on: "python", artifacts: ["lambda-package.zip"]}, ...]`
     - Identify which workflows must wait for others to complete
     - Note artifact requirements (e.g., Terraform needs Lambda zip file location)

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
   - Note any mixed codebases (e.g., Python backend with JavaScript frontend)

3. **Analyze Existing Workflows:**

   - **Simplified Approach**: If this is a regeneration request, `.github/workflows/` directory should already be deleted (handled in Welcome phase)
   - Scan `.github/workflows/` directory for existing workflow files (if directory exists)
   - **If `.github/workflows/` directory exists and contains files**:
     - Document existing workflow patterns and conventions for reference
     - Note: These workflows will be replaced with newly generated environment-specific workflows
     - **For regeneration**: Directory should already be empty (removed in Welcome phase)
     - **For new generation**: Directory may contain existing workflows that will be replaced
   - **If `.github/workflows/` directory doesn't exist or is empty**: No existing workflows to analyze

4. **Identify Detected Code Types:**

   - Create a summary of all detected code types with their locations
   - Example: "Python detected in `src/` and `lambda-python-s3-lambda-trigger/`; Terraform detected in `iac/terraform/`; JavaScript detected in `frontend/`"
   - **Cross-reference with Requirements**: Verify detected code types match requirements analysis
   - **Validate Dependencies**: Ensure dependency relationships from requirements are valid for detected code types

5. **Analyze Code Dependencies:**

   - **Build Dependency Map**:

     - For each code type, identify what it depends on (from requirements analysis)
     - Document build order: e.g., "Python Lambda must be built before Terraform deployment"
     - Identify artifact requirements: what artifacts need to be produced and consumed
     - Example dependency chains:
       - `terraform → depends on → python` (Terraform needs Lambda zip for deployment)
       - `docker → depends on → python` (Docker image needs Python code built)
       - `kubernetes → depends on → docker` (K8s manifests need Docker image)

   - **Workflow Dependency Requirements**:
     - Determine which workflows must wait for others using `workflow_run` triggers
     - Identify which artifacts need to be uploaded/downloaded between workflows
     - Document artifact passing requirements (e.g., Lambda zip file path, Docker image tag)

6. **Draft Multi-Environment Workflow Plan:**
   For each detected code type, plan **three separate workflow files**, one per environment:

   - **Deploy to Dev Workflow** (`{code-type}-dev.yml`):
     - Triggers on pushes to `develop` branch only
     - Contains CI jobs (lint, test, security scan, artifact generation) + Deploy to Dev job
   - **Deploy to Test Workflow** (`{code-type}-test.yml`):
     - Triggers on pushes to `main` branch
     - If dependencies exist, can also use `workflow_run` to wait for upstream test workflows, with push as fallback
     - Contains CI jobs + Deploy to Test job
   - **Deploy to Prod Workflow** (`{code-type}-prd.yml`):
     - Triggers via `workflow_run` on successful completion of `{code-type}-test.yml` workflow
     - Branch filter: `branches: [main]` - only triggers when test workflow ran on `main` branch
     - Contains CI jobs + Deploy to Prod job

   **Document Dependency Handling:**

   - For each dependency relationship, specify:
     - Which workflow must complete first (upstream)
     - Which workflow depends on it (downstream)
     - What artifacts need to be passed (e.g., Lambda zip file, Docker image tag)
     - How artifacts will be passed (workflow artifacts, S3, container registry, etc.)
     - Example: "Terraform-dev workflow must wait for Python-dev workflow to complete and upload Lambda zip artifact"

   Document workflow modifications:

   - List existing workflows that need modification (update to environment-specific structure)
   - List existing workflows that should be removed
   - List new environment-specific workflows that need to be created (3 per code type)
   - Document dependency-based workflow triggers and artifact passing

7. **User Plan Review Checkpoint:**

   - Present summary of:
     - All detected code types with locations
     - **Requirements and dependencies identified** (code artifact dependencies)
     - **Dependency map** (which code types depend on others)
     - **Workflow dependency order** (which workflows must run before others)
     - Existing workflows analysis (keep/modify/remove)
     - Planned environment-specific workflows (dev/test/prd) for each code type
     - **Artifact passing strategy** (how dependencies will be handled between workflows)
     - Multi-environment deployment strategy
   - Ask: "Proceed to generate/update workflow files as planned?"
   - Wait for confirmation to proceed.

8. **Persist Phase Results (State & Audit):**
   - Write detected code types, **dependency map**, existing workflow analysis, and the draft plan to `.cicd-docs/cicd-state.md` (preferred). If not present, use legacy `.amazonq/rules/cicd-phases/cicd-state.md`.
   - Include dependency relationships and artifact requirements in the state file
   - Record the user confirmation decision with timestamp in `.cicd-docs/audit.md`.
