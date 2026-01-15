# Workflow Generation Plan

## Generated Workflow

**File**: `.github/workflows/ci-cd.yml`

### Workflow Structure

**Name**: CI/CD
**Triggers**: 
- `push` to `main` branch
- `workflow_dispatch` (manual execution)

**Permissions**:
- `id-token: write` (OIDC)
- `contents: read`

### Jobs Generated

#### Python CI Jobs (Parallel, Non-blocking)

1. **python-lint**
   - Matrix: Python 3.10, 3.11, 3.12
   - Continue on error: true
   - Steps: Checkout, setup Python, install deps, run Flake8

2. **python-security**
   - Python 3.12
   - Continue on error: true
   - Steps: Checkout, setup Python, install deps, run Bandit

3. **python-test**
   - Matrix: Python 3.10, 3.11, 3.12
   - Continue on error: true
   - Steps: Checkout, setup Python, install deps, run pytest with coverage
   - Conditional test execution using step-level `hashFiles()`
   - Upload coverage artifacts

#### Terraform CI Jobs (Parallel, Non-blocking)

4. **terraform-security**
   - Continue on error: true
   - Steps: Checkout, run Checkov

5. **terraform-validate**
   - Steps: Checkout, setup Terraform, configure AWS OIDC, configure TFC, init, validate, format

#### Combined Deploy Job

6. **terraform-deploy**
   - Needs: All CI jobs (python-lint, python-security, python-test, terraform-security, terraform-validate)
   - Environment: production
   - Condition: `if: always()` (runs even if CI fails)
   - Steps:
     1. Checkout code
     2. **Python Build**: Setup Python, install deps, build Lambda zip in `iac/terraform/lambda_function.zip`
     3. **Terraform Deploy**: Setup Terraform, configure AWS OIDC, configure TFC, verify artifact, init, plan, apply

### Dependency Handling

**Pattern**: Combined Build and Deploy Job (MOST PREFERRED)
- Python build steps included in terraform-deploy job
- Lambda package built directly where Terraform expects it
- No artifact upload/download needed
- Terraform deploys both infrastructure AND Lambda source code

### Standards Applied

- [x] Python standards: CI jobs with matrix, continue-on-error, step-level hashFiles()
- [x] Terraform standards: OIDC, TFC config, version ~1.1, combined job pattern
- [x] Single production workflow on main branch
- [x] All deploy jobs use environment: production

## Validation Checklist

- [x] YAML syntax valid
- [x] No job-level hashFiles() usage
- [x] All expressions use ${{ }} syntax
- [x] Workflow has required fields (name, on, jobs, runs-on)
- [x] Single production workflow (ci-cd.yml)
- [x] Triggers on main branch only + workflow_dispatch
- [x] All code types have jobs (Python, Terraform)
- [x] Job dependencies correct (needs array)
- [x] No circular dependencies
- [x] All deploy jobs use environment: production
- [x] Checkout step in all jobs
- [x] OIDC configuration present
- [x] Permissions set correctly
- [x] Dependency handling implemented (combined job pattern)
- [x] Language-specific standards applied

## Phase 2 Checklist

- [x] Load detection plan and standards
- [x] Generate single production workflow
- [x] Apply Python standards (CI jobs, matrix, continue-on-error)
- [x] Apply Terraform standards (OIDC, TFC, combined job)
- [x] Implement dependency handling (combined build-deploy job)
- [x] Validate workflow structure
- [x] Document workflow in plan
- [ ] User approval to proceed to Phase 3
