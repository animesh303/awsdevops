# Phase 1: Detection and Planning

## Code Type Detection

- [x] Scan for Python code (.py files, requirements.txt) - **DETECTED**: `src/lambda-python-s3-lambda-trigger/`
- [x] Scan for Terraform code (.tf files, terraform/ directories) - **DETECTED**: `iac/terraform/`
- [x] Scan for JavaScript/TypeScript code (.js, .jsx, .ts, .tsx files, package.json) - **NOT FOUND**
- [x] Scan for Java code (.java files, pom.xml, build.gradle) - **NOT FOUND**
- [x] Scan for Go code (.go files, go.mod, go.sum) - **NOT FOUND**
- [x] Scan for Docker code (Dockerfile, docker-compose.yml) - **NOT FOUND**
- [x] Scan for Kubernetes code (.yaml/.yml files in k8s/, kubernetes/, manifests/) - **NOT FOUND**
- [x] Scan for CloudFormation code (.yaml/.yml CloudFormation templates) - **NOT FOUND**
- [x] Scan for CDK code (cdk.json, cdk/ directories) - **NOT FOUND**

## Requirements Analysis

- [x] Load requirements files from .code-docs/requirements/
- [x] Extract dependency information between code artifacts
- [x] Build dependency map (code-type → depends on → other-code-type)
- [x] Document artifact requirements (e.g., Lambda zip file paths)

**Dependency Map**: `terraform → depends on → python (artifacts: ["lambda-package.zip"])`

## Existing Workflow Analysis

- [x] Scan .github/workflows/ directory for existing workflows - **EMPTY** (regeneration)
- [x] Document existing workflow patterns and conventions - **N/A** (fresh start)
- [x] Determine workflows to keep/modify/remove - **N/A** (fresh start)

## Multi-Environment Workflow Planning

- [x] Plan dev workflows (trigger on develop branch)
- [x] Plan test workflows (trigger on main branch)  
- [x] Plan prod workflows (trigger via workflow_run after test completion)
- [x] Document dependency handling strategy
- [x] Plan orchestrator workflows for dependency management

**Planned Workflows:**
- **Orchestrator Workflows**: 3 files (dev/test/prd) to manage dependencies
- **Python Workflows**: 3 files (python-dev.yml, python-test.yml, python-prd.yml)
- **Terraform Workflows**: 3 files (terraform-dev.yml, terraform-test.yml, terraform-prd.yml)

**Dependency Strategy**: Terraform workflows wait for Python workflows to complete and download Lambda zip artifacts

## User Approval

- [ ] Present detection results and plan to user
- [ ] Get user confirmation to proceed to workflow generation