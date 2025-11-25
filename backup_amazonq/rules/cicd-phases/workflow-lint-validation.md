
# Workflow Linting Validation Procedures

## Purpose

Provide automated validation procedures to catch linting errors in generated GitHub Actions workflows, with special focus on blocking errors like `hashFiles()` at job level.

## MANDATORY: Pre-Generation Validation

Before generating workflow files, validate standards files:

1. **Check Standards Files**:
   - Read all `{code-type}-standards.mdc` files
   - Search for job-level `if:` patterns containing `hashFiles`
   - If found, fix standards file before proceeding

## MANDATORY: Post-Generation Validation

After generating workflow file, perform these validation checks:

### Step 1: Read Generated Workflow File

```bash
# Read the workflow file
cat .github/workflows/ci-cd.yml
```

### Step 2: Check for hashFiles() at Job Level (BLOCKING CHECK)

**Pattern to Detect**:
- Job definition line: `^\s+[a-z-]+:\s*$`
- Followed by `if:` at same indentation level as `runs-on:`
- `if:` line contains `hashFiles`

**Validation Command** (conceptual - adapt to available tools):

```bash
# Check for job-level if with hashFiles
# Pattern: job name, then if: line with hashFiles
grep -B 1 "if:.*hashFiles" .github/workflows/ci-cd.yml | grep -E "^\s+[a-z-]+:\s*$"
```

**If Pattern Found**: This is a CRITICAL BLOCKING ERROR

### Step 3: Fix Job-Level hashFiles() Usage

**Invalid Pattern**:
```yaml
python-test:
  if: ${{ hashFiles('tests/**') != '' }}  # ❌ INVALID
  runs-on: ubuntu-latest
  steps:
    - run: pytest
```

**Valid Pattern**:
```yaml
python-test:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Install test dependencies
      if: ${{ hashFiles('tests/**') != '' }}  # ✓ VALID
      run: pip install pytest
    - name: Run tests
      if: ${{ hashFiles('tests/**') != '' }}  # ✓ VALID
      run: pytest tests/
```

### Step 4: Re-Validate After Fix

- Re-read workflow file
- Re-run validation checks
- Confirm no job-level `hashFiles()` usage

## Validation Checklist

- [ ] Workflow file exists
- [ ] YAML syntax is valid
- [ ] No job-level `if:` fields contain `hashFiles`
- [ ] All `hashFiles()` usage is at step level only
- [ ] All expressions use `${{ }}` syntax
- [ ] All required fields present (name, on, jobs, runs-on)
- [ ] No circular job dependencies
- [ ] All referenced jobs exist

## Enforcement Rules

1. **BLOCKING**: Job-level `hashFiles()` usage blocks workflow generation
2. **MANDATORY**: Validation MUST be performed after every workflow generation
3. **NO EXCEPTIONS**: Cannot proceed to Phase 3 if validation fails
4. **AUTOMATED**: Use pattern matching to detect issues automatically
5. **FIX IMMEDIATELY**: Fix errors before presenting preview to user

## Integration Points

- **Phase 2, Step 9**: Perform validation before presenting preview
- **Phase 3, Step 5**: Re-validate before final approval
- **Validation Checklist**: Use this file as reference for validation steps
