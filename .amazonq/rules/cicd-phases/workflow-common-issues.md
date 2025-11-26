## Issue 1: hashFiles() Used at Job Level (CRITICAL ERROR)

**Problem**: `hashFiles()` function is used at job level (`jobs.<job>.if`), which is NOT supported by GitHub Actions.

**Error Example**:

```yaml
jobs:
  python-test:
    if: ${{ hashFiles('tests/**') != '' }} # ❌ ERROR: hashFiles() not available at job level
    runs-on: ubuntu-latest
    steps:
      - run: pytest
```

**Error Message**: `Unrecognized function: 'hashFiles'. Located at position 1 within expression: hashFiles('tests/**') != ''`

**Solution**: Move `hashFiles()` condition to step level:

```yaml
jobs:
  python-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install test dependencies
        if: ${{ hashFiles('tests/**') != '' }} # ✓ Correct - hashFiles at step level
        run: pip install pytest
      - name: Run tests
        if: ${{ hashFiles('tests/**') != '' }} # ✓ Correct - hashFiles at step level
        run: pytest tests/
```

**Key Points**:

- `hashFiles()` is ONLY available in step-level `if` conditions (`jobs.<job>.steps[*].if`)
- `hashFiles()` is NOT available at job level (`jobs.<job>.if`)
- Always apply conditions to individual steps, not the entire job

**Validation**: Always scan generated workflows for job-level `if:` fields containing `hashFiles` before proceeding.

---

## Issue 2: Missing `${{ }}` Wrapper for GitHub Actions Functions

**Problem**: GitHub Actions functions like `hashFiles()`, `always()`, `success()` must be wrapped in `${{ }}` syntax.

**Error Example**:

```yaml
if: hashFiles('tests/**') != '' # ❌ Error: Unrecognized function
```

**Solution**: Always wrap GitHub Actions functions in `${{ }}`:

```yaml
if: ${{ hashFiles('tests/**') != '' }} # ✓ Correct
```

---

## Issue 3: Missing Checkout Step in Jobs

**Problem**: Jobs don't automatically checkout code, causing "file not found" errors.

**Error Example**:

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: terraform apply # ❌ Error: No code checked out
```

**Solution**: Always include checkout as the first step:

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: terraform apply # ✓ Correct
```

---

## Issue 4: Incorrect Artifact Download for Job Dependencies

**Problem**: Attempting to download artifacts from upstream jobs without proper configuration.

**Error Example**:

```yaml
- uses: actions/download-artifact@v4
  with:
    name: artifact-name
    # ❌ Missing path or incorrect artifact name
```

**Solution**: For jobs within the same workflow, use simple artifact download:

```yaml
- uses: actions/download-artifact@v4
  with:
    name: artifact-name
    path: ./artifacts
```

**Note**: For single production workflow, all artifact passing happens within the same workflow. No cross-workflow downloads needed.

**See Also**: `workflow-dependency-handling.mdc` for comprehensive dependency patterns

---

## Issue 5: Circular Job Dependencies

**Problem**: Jobs that depend on each other create circular dependencies, causing workflow failures.

**Error Example**:

```yaml
jobs:
  job-a:
    needs: [job-b]
  job-b:
    needs: [job-a] # ❌ Circular dependency
```

**Solution**: Restructure jobs to remove circular dependencies, or combine dependent jobs:

```yaml
jobs:
  job-a:
    # No dependencies
  job-b:
    needs: [job-a] # ✓ Correct: One-way dependency
```

---

## Issue 6: Invalid YAML Syntax

**Problem**: YAML syntax errors cause workflow validation failures.

**Common Causes**:

- Incorrect indentation (must use spaces, not tabs)
- Missing colons after keys
- Incorrect list formatting
- Unquoted special characters

**Solution**:

- Use YAML linter to validate syntax
- Ensure consistent indentation (2 spaces recommended)
- Quote values containing special characters
- Validate with GitHub Actions workflow validator

---

## Issue 7: Missing Required Fields

**Problem**: Workflows fail validation due to missing required fields.

**Required Fields**:

- `name`: Workflow name
- `on`: Trigger events
- `jobs`: Job definitions
- Each job must have `runs-on`

**Solution**: Ensure all required fields are present. See `phase2-generate-workflow.mdc` for workflow structure requirements.

---

## Issue 8: Incorrect Environment Names

**Problem**: Using incorrect environment names causes deployment failures.

**Required Environment Name**:

- `production` - Production environment (single environment only)

**Solution**: Always use exact environment name: `production` (lowercase, no variations). All deploy jobs in the single production workflow use `environment: production`.

---

## Issue 9: Invalid Workflow Trigger Syntax

**Problem**: Incorrect workflow trigger syntax causes workflows not to trigger.

**Required Trigger**:

- `push` to `main` branch only
- `workflow_dispatch` for manual execution

**Common Errors**:

- Using other branch names (should be `main` only)
- Missing `workflow_dispatch` for manual triggers
- Using `workflow_run` triggers (not needed for single workflow)

**Solution**: Follow exact syntax from `phase2-generate-workflow.mdc` workflow structure examples. Single production workflow triggers on `main` branch push only.

---

## Issue 10: Artifact Path Mismatch

**Problem**: Artifacts downloaded but not found at expected paths.

**Solution**:

- Verify artifact upload path matches download path
- Check artifact name matches exactly (case-sensitive)
- Ensure artifact was uploaded before download attempt
- See `workflow-dependency-handling.mdc` for artifact passing patterns
