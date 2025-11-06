# GitHub Actions Workflow Common Issues and Solutions

## Purpose

This document provides solutions to common issues encountered when generating GitHub Actions workflows. Reference this document when troubleshooting workflow generation errors.

## Related Files

- See `phase2-generate-workflow.md` for workflow generation steps
- See `workflow-dependency-handling.md` for dependency patterns

---

## Issue 1: `hashFiles()` Not Available at Job Level

**Problem**: Attempting to use `hashFiles()` in a job-level `if` condition causes an error because `hashFiles()` is only available in step-level contexts.

**Error Example**:

```yaml
jobs:
  tests:
    if: ${{ hashFiles('tests/**') != '' }} # ❌ Error: hashFiles() not available
    runs-on: ubuntu-latest
    steps:
      - run: pytest
```

**Solution**: Move the `hashFiles()` check to step-level `if` conditions:

```yaml
jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run tests
        if: ${{ hashFiles('tests/**') != '' }}
        run: pytest
```

**Alternative Solution**: If you need to conditionally skip the entire job, use a separate job to check file existence:

```yaml
jobs:
  check-tests:
    runs-on: ubuntu-latest
    outputs:
      has-tests: ${{ steps.check.outputs.exists }}
    steps:
      - uses: actions/checkout@v4
      - id: check
        run: |
          if [ -n "$(find tests -type f 2>/dev/null)" ]; then
            echo "exists=true" >> $GITHUB_OUTPUT
          else
            echo "exists=false" >> $GITHUB_OUTPUT
          fi

  tests:
    needs: check-tests
    if: ${{ needs.check-tests.outputs.has-tests == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest
```

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

## Issue 3: Missing Checkout Step in `workflow_run` Triggered Jobs

**Problem**: Jobs triggered by `workflow_run` events don't automatically checkout code, causing "file not found" errors.

**Error Example**:

```yaml
on:
  workflow_run:
    workflows: ["Upstream Workflow"]
    types: [completed]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: terraform apply # ❌ Error: No code checked out
```

**Solution**: Always include checkout as the first step with the `ref` parameter:

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.workflow_run.head_branch }}
      - run: terraform apply # ✓ Correct
```

---

## Issue 4: Incorrect Artifact Download for Cross-Workflow Dependencies

**Problem**: Attempting to download artifacts from upstream workflows without proper authentication or run-id.

**Error Example**:

```yaml
- uses: actions/download-artifact@v4
  with:
    name: artifact-name
    # ❌ Missing run-id and github-token for cross-workflow downloads
```

**Solution**: For `workflow_run` triggers, always include `run-id` and `github-token`:

```yaml
- uses: actions/download-artifact@v4
  with:
    name: artifact-name
    run-id: ${{ github.event.workflow_run.id }}
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

**See Also**: `workflow-dependency-handling.md` for comprehensive dependency patterns

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

**Solution**: Ensure all required fields are present. See `phase2-generate-workflow.md` for workflow structure requirements.

---

## Issue 8: Incorrect Environment Names

**Problem**: Using incorrect environment names causes deployment failures.

**Required Environment Names**:

- `dev` - Development environment
- `test` - Test environment
- `prod` - Production environment

**Solution**: Always use exact environment names: `dev`, `test`, `prod` (lowercase, no variations).

---

## Issue 9: Invalid Workflow Trigger Syntax

**Problem**: Incorrect `workflow_run` trigger syntax causes workflows not to trigger.

**Common Errors**:

- Missing `types: [completed]`
- Incorrect workflow name (must match exact workflow name)
- Missing `branches` filter for prod workflows

**Solution**: Follow exact syntax from `phase2-generate-workflow.md` workflow structure examples.

---

## Issue 10: Artifact Path Mismatch

**Problem**: Artifacts downloaded but not found at expected paths.

**Solution**:

- Verify artifact upload path matches download path
- Check artifact name matches exactly (case-sensitive)
- Ensure artifact was uploaded before download attempt
- See `workflow-dependency-handling.md` for artifact passing patterns
