## Phase 2: Generate Workflows Errors

### Error: Standards File Missing

**Scenario**: Detected code type has no corresponding standards file (e.g., `go-standards.mdc` not found for Go code).

**Response**:

- Create standards file following pattern of existing standards files
- Use language-appropriate CI/CD patterns
- Document creation in plan: "Created {code-type}-standards.mdc"
- Proceed with workflow generation

### Error: Workflow Generation Fails

**Scenario**: Error occurs while generating workflow YAML (syntax error, missing fields, etc.).

**Response**:

- Log error details in audit.md
- Fix the error immediately if possible
- If error cannot be fixed: Skip that workflow, document in plan, inform user
- Continue generating other workflows
- Do not proceed to Phase 3 if critical workflows failed

### Error: Linting Errors Found

**Scenario**: Generated workflows have linting errors (invalid YAML, missing fields, etc.).

**Response**:

- **MANDATORY**: Fix all linting errors before proceeding
- Use `workflow-common-issues.mdc` for troubleshooting
- Validate fixes before continuing
- Do not proceed to Phase 3 until all workflows pass validation

### Error: Dependency Handling Fails

**Scenario**: Cannot implement dependency handling (upstream workflow not found, artifact download fails, etc.).

**Response**:

- Log error in audit.md
- For single dependency: Use fallback push trigger, document limitation
- For multiple dependencies: Use S3/Storage method, document in plan
- Inform user of dependency handling limitations
- Proceed with workflows (they may need manual dependency configuration)

---

## Phase 3: Review & Confirm Errors

### Error: Workflow Files Not Found

**Scenario**: Generated workflow files are missing or cannot be read.

**Response**:

- Check if files were generated in Phase 2
- If missing: Return to Phase 2, regenerate workflows
- If cannot read: Check file permissions, log error
- Do not proceed to Phase 4

### Error: User Rejects Workflows

**Scenario**: User reviews workflows and requests changes or rejects them.

**Response**:

- Document rejection reason in audit.md
- Ask user for specific changes needed
- Return to Phase 2 if changes are needed
- Allow user to abort if they want to start over
- Do not proceed to Phase 4 without approval

---

## Phase 4: Commit & Push Errors

### Error: Git Not Configured

**Scenario**: Git user identity not configured.

**Response**:

- Configure Git identity (as documented in Phase 4 steps)
- Use fallback: `git config user.name "automation-bot"` and `git config user.email "automation-bot@local"`
- Proceed with commit

### Error: Commit Fails

**Scenario**: `git commit` fails (no changes, invalid message, etc.).

**Response**:

- Check if there are actual changes to commit
- Verify commit message format
- Log error in audit.md
- Ask user for guidance
- Do not proceed with push if commit failed

### Error: Push Fails

**Scenario**: `git push` fails (authentication, permissions, remote not found, etc.).

**Response**:

- Log error details in audit.md
- Inform user of push failure
- Provide error message to user
- Do not retry automatically - require user intervention
- Workflows are committed locally but not pushed

### Error: Branch Conflicts

**Scenario**: Push fails due to branch conflicts or remote changes.

**Response**:

- Inform user: "Remote branch has changes. Please pull and merge before pushing."
- Do not force push automatically
- Allow user to resolve conflicts manually
- Document in audit.md

---

## General Error Handling

### Error: State File Corruption

**Scenario**: `cicd-state.md` is corrupted or unreadable.

**Response**:

- Attempt to read legacy state file if available
- If both corrupted: Start new session (treat as new generation)
- Log error in audit.md
- Inform user of state loss

### Error: Session Interrupted

**Scenario**: User session interrupted mid-phase (timeout, disconnect, etc.).

**Response**:

- State files should persist (already saved)
- On resume: Read `cicd-state.md` to determine current phase
- Follow `session-continuity.md` to resume
- Continue from last completed step

### Error: Disk Space or Permissions

**Scenario**: Cannot write files due to disk space or permission issues.

**Response**:

- Log error in audit.md
- Inform user of permission/space issue
- Do not proceed until resolved
- Provide clear error message

### Error: Invalid User Input

**Scenario**: User provides invalid input or rejects required confirmations.

**Response**:

- Clarify what is needed
- Re-prompt with clear instructions
- Log interaction in audit.md
- Do not proceed without valid confirmation

---

## Error Recovery Procedures

### Recovery: Restart Phase

**When to Use**: Phase failed but can be retried.

**Procedure**:

1. Log error in audit.md
2. Inform user of failure
3. Ask: "Would you like to retry this phase?"
4. If yes: Restart phase from beginning
5. If no: Allow user to abort or modify approach

### Recovery: Rollback Changes

**When to Use**: Changes made but need to be undone.

**Procedure**:

1. See `rollback-procedures.mdc` for detailed rollback scenarios and steps
2. Follow appropriate rollback scenario based on current phase and commit status
3. Log rollback in audit.md

### Recovery: Manual Intervention Required

**When to Use**: Error cannot be automatically resolved.

**Procedure**:

1. Log error with full details in audit.md
2. Inform user of issue and required manual steps
3. Provide clear instructions for resolution
4. Pause workflow generation until user resolves issue
5. Resume from current phase after resolution

---

## Error Logging Format

All errors should be logged in `.cicd-docs/audit.md` using this format:

```markdown
## Error: [Error Type]

**Timestamp**: 2025-01-28T14:32:15Z
**Phase**: [Phase Number and Name]
**Error**: [Brief error description]
**Details**: [Full error message or stack trace]
**Response**: [Action taken]
**Resolution**: [How error was resolved or pending resolution]
**User Notified**: [Yes/No]

---
```

---

## Best Practices

1. **Always log errors** in audit.md with timestamp
2. **Inform user immediately** of critical errors
3. **Do not proceed** to next phase if current phase has unresolved errors
4. **Provide clear error messages** to users
5. **Allow recovery options** when possible
6. **Document error patterns** for future reference
7. **Validate before proceeding** to avoid cascading errors
