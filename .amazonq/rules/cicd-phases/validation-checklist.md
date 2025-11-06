# CICD Workflow Generation Validation Checklist

## Purpose

This comprehensive checklist ensures all generated workflows meet quality and correctness standards before proceeding to the next phase or committing to repository.

## Related Files

- See `phase2-generate-workflow.md` for workflow generation steps
- See `phase3-review-confirm.md` for review procedures
- See `workflow-common-issues.md` for troubleshooting

---

## Phase 1: Detect & Plan Validation

### Code Detection Validation

- [ ] All code types detected correctly (Python, Terraform, JavaScript, etc.)
- [ ] Code locations documented accurately
- [ ] No false positives (detected code that doesn't exist)
- [ ] No missed code types (code exists but not detected)

### Requirements Files Validation

- [ ] All requirements files loaded (if they exist)
- [ ] Requirements files parsed correctly
- [ ] Dependency information extracted accurately
- [ ] Dependency map format is correct (structured format)

### Dependency Analysis Validation

- [ ] Dependency relationships identified correctly
- [ ] Artifact requirements documented
- [ ] Build order determined correctly
- [ ] No circular dependencies

### Workflow Planning Validation

- [ ] Three workflows planned per code type (dev/test/prd)
- [ ] Workflow triggers planned correctly
- [ ] Environment assignments correct (dev/test/prod)
- [ ] Dependency handling strategy documented

---

## Phase 2: Generate Workflows Validation

### YAML Syntax Validation

- [ ] All workflow files have valid YAML syntax
- [ ] No YAML linting errors
- [ ] Proper indentation (2 spaces, consistent)
- [ ] No syntax errors (missing colons, brackets, etc.)

### GitHub Actions Syntax Validation

- [ ] All expressions use `${{ }}` syntax
- [ ] No missing expression wrappers
- [ ] `hashFiles()` used only in step-level `if` conditions
- [ ] All GitHub Actions functions properly wrapped

### Workflow Structure Validation

- [ ] All workflows have required fields:
  - [ ] `name` field present
  - [ ] `on` trigger defined
  - [ ] `jobs` section present
  - [ ] Each job has `runs-on`
- [ ] Workflow names follow pattern: `{code-type}-{environment}`
- [ ] Workflow files named correctly: `{code-type}-{environment}.yml`

### Trigger Validation

- [ ] Dev workflows trigger on `develop` branch (or `workflow_run` if dependencies)
- [ ] Test workflows trigger on `main` branch (or `workflow_run` if dependencies)
- [ ] Prod workflows use `workflow_run` trigger with `branches: [main]`
- [ ] `workflow_run` triggers have `types: [completed]`
- [ ] Branch filters correct for each environment

### Job Structure Validation

- [ ] CI jobs defined (lint, test, security scan)
- [ ] Deployment job defined for each environment
- [ ] Job dependencies correct (`needs:` array)
- [ ] No circular job dependencies
- [ ] All referenced jobs exist

### Environment Validation

- [ ] Environment names correct: `dev`, `test`, `prod` (lowercase)
- [ ] Environment protection rules referenced (for prod)
- [ ] Environment-specific secrets/variables configured

### Checkout Step Validation

- [ ] All jobs have checkout step
- [ ] `workflow_run` triggered jobs use `ref: ${{ github.event.workflow_run.head_branch }}`
- [ ] Push triggered jobs use standard checkout
- [ ] Checkout is first step in each job

### Dependency Handling Validation

- [ ] `workflow_run` triggers added for dependencies
- [ ] Artifact download steps present (if dependencies exist)
- [ ] Artifact verification steps present
- [ ] Artifact placement steps correct
- [ ] Artifact passing method appropriate (single vs multiple dependencies)
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

- [ ] Artifacts uploaded with correct names
- [ ] Artifact names include environment (e.g., `lambda-package-dev`)
- [ ] Artifact retention configured appropriately
- [ ] Artifact paths correct for download

### Permissions Validation

- [ ] Required permissions set at workflow level
- [ ] `contents: read` present (default)
- [ ] `id-token: write` present (if OIDC needed)
- [ ] No excessive permissions

### Concurrency Validation

- [ ] Concurrency groups configured (if needed)
- [ ] Concurrency group names include environment
- [ ] `cancel-in-progress` set appropriately

---

## Phase 3: Review & Confirm Validation

### Workflow File Existence Validation

- [ ] All planned workflows generated
- [ ] Workflow files exist in `.github/workflows/`
- [ ] File names match planned names
- [ ] No missing workflow files

### Content Review Validation

- [ ] Workflow YAML content reviewed
- [ ] All jobs present and correct
- [ ] Triggers configured correctly
- [ ] Environments assigned correctly
- [ ] Dependency handling implemented correctly

### Dependency Graph Validation

- [ ] Dependency relationships correct
- [ ] Upstream workflows identified
- [ ] Downstream workflows wait correctly
- [ ] Artifact passing verified

### Multi-Environment Validation

- [ ] Three workflows per code type (dev/test/prd)
- [ ] Environment-specific configurations correct
- [ ] Branch triggers correct for each environment
- [ ] Environment protection rules in place (prod)

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
- [ ] All workflows generated
- [ ] Dependency handling implemented

### Before Proceeding to Phase 4

- [ ] All Phase 3 validations passed
- [ ] User approved workflows
- [ ] All workflows reviewed
- [ ] No outstanding issues

### Before Finalizing

- [ ] All phases completed
- [ ] All validations passed
- [ ] Workflows committed and pushed
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
