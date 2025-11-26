
## Phase 2: Generate Workflows Validation

### YAML Syntax Validation

- [ ] All workflow files have valid YAML syntax
- [ ] No YAML linting errors
- [ ] Proper indentation (2 spaces, consistent)
- [ ] No syntax errors (missing colons, brackets, etc.)

### GitHub Actions Syntax Validation

- [ ] All expressions use `${{ }}` syntax
- [ ] No missing expression wrappers
- [ ] **CRITICAL**: `hashFiles()` used ONLY in step-level `if` conditions (NOT at job level)
- [ ] **MANDATORY CHECK**: Scanned workflow file for job-level `if:` fields containing `hashFiles` - NONE found
- [ ] All GitHub Actions functions properly wrapped
- [ ] **Validation Method**: Read workflow YAML, parse structure, verify no `jobs.<job>.if` contains `hashFiles`

### Workflow Structure Validation

- [ ] Single production workflow has required fields:
  - [ ] `name` field present (should be "CI/CD" or similar)
  - [ ] `on` trigger defined (push to `main` branch only and `workflow_dispatch`)
  - [ ] `jobs` section present
  - [ ] Each job has `runs-on`
- [ ] Workflow file named correctly: `ci-cd.yml`
- [ ] All code types have jobs in the unified workflow

### Trigger Validation

- [ ] Production workflow triggers on `main` branch push only
- [ ] `workflow_dispatch` trigger present for manual execution
- [ ] No `workflow_run` triggers (not needed for single workflow)
- [ ] No other branch triggers (only main branch)

### Job Structure Validation

- [ ] For each code type, CI jobs defined (lint, security, test)
- [ ] For each code type, build job defined
- [ ] For each code type, deploy job defined
- [ ] Job dependencies correct (`needs:` array)
- [ ] No circular job dependencies
- [ ] All referenced jobs exist
- [ ] Jobs sequenced correctly based on dependencies (upstream jobs complete before downstream)

### Environment Validation

- [ ] All deploy jobs use `environment: production` (single production environment)
- [ ] Environment protection rules referenced (if needed)
- [ ] Secrets/variables configured for production environment
- [ ] No multiple environment configurations

### Checkout Step Validation

- [ ] All jobs have checkout step
- [ ] Standard checkout used (`actions/checkout@v4`)
- [ ] Checkout is first step in each job

### Dependency Handling Validation

- [ ] Job dependencies (`needs:`) correctly configured for dependencies
- [ ] Artifact download steps present in downstream deploy jobs (if dependencies exist)
- [ ] Artifact verification steps present
- [ ] Artifact placement steps correct
- [ ] Artifacts passed between jobs in same workflow (not cross-workflow)
- [ ] Error handling for artifact downloads

### AWS Credentials Validation

- [ ] OIDC configuration present (if AWS operations needed)
- [ ] `permissions: id-token: write` set (if OIDC used)
- [ ] AWS region configured correctly
- [ ] Role-to-assume secret referenced

### Language-Specific Validation

- [ ] Standards file applied correctly for each code type
- [ ] Job names match standards file
- [ ] Steps match standards file patterns
- [ ] Language-specific tools configured (e.g., Terraform version, Python version)

### Artifact Handling Validation

- [ ] Artifacts uploaded with correct names (simple, consistent naming)
- [ ] Artifact names are consistent (e.g., `lambda-package`, not environment-specific)
- [ ] Artifact retention configured appropriately
- [ ] Artifact paths correct for download
- [ ] Artifacts uploaded in build jobs
- [ ] Artifacts downloaded in deploy jobs that need them

### Permissions Validation

- [ ] Required permissions set at workflow level
- [ ] `contents: read` present (default)
- [ ] `id-token: write` present (if OIDC needed)
- [ ] No excessive permissions

### Concurrency Validation

- [ ] Concurrency groups configured (if needed)
- [ ] Concurrency group name is simple (e.g., `ci-cd-${{ github.ref }}`)
- [ ] `cancel-in-progress` set appropriately

---

## Phase 3: Review & Confirm Validation

### Workflow File Existence Validation

- [ ] Single production workflow generated
- [ ] Workflow file exists: `.github/workflows/ci-cd.yml`
- [ ] File name matches planned name (`ci-cd.yml`)
- [ ] No extra workflow files (old workflows removed if regenerating)
- [ ] No orchestrator workflows (not needed for single workflow)

### Content Review Validation

- [ ] Single production workflow YAML content reviewed
- [ ] All code types have jobs present and correct
- [ ] Triggers configured correctly (push to `main` branch only, `workflow_dispatch`)
- [ ] All deploy jobs use `environment: production`
- [ ] Dependency handling implemented correctly (job dependencies via `needs:`)

### Dependency Graph Validation

- [ ] Dependency relationships correct
- [ ] Upstream jobs identified (code types with no dependencies)
- [ ] Downstream jobs wait correctly (via `needs:` dependencies)
- [ ] Artifact passing verified (between jobs in same workflow)
- [ ] Execution order correct (topological sort applied)

### Linting Final Validation

- [ ] All workflows pass YAML validation
- [ ] All workflows pass GitHub Actions validation
- [ ] No linting errors reported
- [ ] Workflow structure valid

### User Approval Validation

- [ ] User reviewed all workflows
- [ ] User approved workflows
- [ ] Approval logged in audit.md
- [ ] Ready to proceed to Phase 4

---

## Phase 4: Commit & Push Validation

### Pre-Commit Validation

- [ ] All workflow files staged
- [ ] No sensitive files included
- [ ] Commit message formatted correctly
- [ ] Git identity configured

### Commit Validation

- [ ] Commit successful
- [ ] Commit message includes relevant information
- [ ] Commit hash recorded (if needed)

### Push Validation

- [ ] Push successful
- [ ] Branch pushed to remote
- [ ] No conflicts
- [ ] Workflows available in repository

---

## Comprehensive Validation Checklist

### Before Proceeding to Phase 3

- [ ] All Phase 2 validations passed
- [ ] No linting errors
- [ ] Single production workflow generated (`ci-cd.yml`)
- [ ] Workflow triggers on main branch only
- [ ] All code types have jobs in unified workflow
- [ ] All deploy jobs use `environment: production`
- [ ] Dependency handling implemented (job dependencies via `needs:`)

### Before Proceeding to Phase 4

- [ ] All Phase 3 validations passed
- [ ] User approved workflows
- [ ] All workflows reviewed
- [ ] No outstanding issues

### Before Finalizing

- [ ] All phases completed
- [ ] All validations passed
- [ ] Single production workflow committed and pushed
- [ ] Workflow triggers on main branch only
- [ ] State files updated
- [ ] Audit log complete

---

## Validation Tools

### Automated Validation

- YAML linter (yamllint, GitHub Actions validator)
- GitHub Actions workflow validator
- Syntax checkers

### Manual Validation

- Review workflow structure
- Verify trigger logic
- Check dependency handling
- Validate environment assignments

---

## Validation Failure Response

If validation fails:

1. **Document failure** in audit.md
2. **Fix issues** before proceeding
3. **Re-validate** after fixes
4. **Do not proceed** until all validations pass
5. **Inform user** of validation status

---

## Best Practices

1. **Validate early and often** - Don't wait until Phase 3
2. **Use automated tools** when possible
3. **Review manually** for logic and correctness
4. **Document validation results** in audit.md
5. **Fix issues immediately** - Don't accumulate errors
