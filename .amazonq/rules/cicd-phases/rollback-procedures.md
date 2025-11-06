# CICD Workflow Generation Rollback Procedures

## Purpose

This document provides procedures for rolling back or undoing changes made during CICD workflow generation. Use these procedures when workflows need to be reverted or when starting over is required.

## Related Files

- See `error-handling.md` for error recovery procedures
- See `session-continuity.md` for session management

---

## Rollback Scenarios

### Scenario 1: Rollback Before Phase 4 (Commit)

**When to Use**: Workflows generated but not yet committed to repository.

**Procedure**:

1. **Delete generated workflow files**:
   - Remove all files from `.github/workflows/` directory
   - Or delete specific workflow files that need rollback
2. **Reset state files** (optional):
   - Delete `.cicd-docs/` directory to start completely fresh
   - Or edit `cicd-state.md` to reset phase to `detect-plan`
3. **Log rollback** in audit.md (if it exists):
   ```markdown
   ## Rollback: Before Commit

   **Timestamp**: 2025-01-28T14:32:15Z
   **Reason**: [User requested rollback / Error occurred]
   **Files Removed**: [List of workflow files removed]
   **State**: [Reset to Phase X / Deleted state files]
   ```
4. **Inform user**: "Rollback complete. Workflows removed. Ready to start fresh or modify approach."

---

### Scenario 2: Rollback After Phase 4 (After Commit)

**When to Use**: Workflows committed but need to be removed or reverted.

**Procedure**:

1. **Check git status**:
   ```bash
   git status
   ```
2. **Revert commit** (if last commit):
   ```bash
   git revert HEAD
   git push
   ```
3. **Or delete workflow files and commit**:
   ```bash
   rm .github/workflows/*.yml
   git add .github/workflows/
   git commit -m "ci(workflows): remove generated workflows (rollback)"
   git push
   ```
4. **Delete state files** (optional):
   - Delete `.cicd-docs/` directory
5. **Log rollback** in audit.md:
   ```markdown
   ## Rollback: After Commit

   **Timestamp**: 2025-01-28T14:32:15Z
   **Reason**: [User requested rollback / Error discovered]
   **Commit Reverted**: [Commit hash or "Files deleted"]
   **State**: [Reset / Deleted]
   ```
6. **Inform user**: "Rollback complete. Workflows removed from repository."

---

### Scenario 3: Regeneration (Complete Reset)

**When to Use**: User wants to completely regenerate workflows from scratch.

**Procedure**:

1. **Delete CICD artifacts**:
   ```bash
   rm -rf .cicd-docs/
   rm -rf .github/workflows/
   ```
2. **Or use regeneration request**:
   - User requests "regenerate" workflows
   - System automatically deletes `.cicd-docs/` and `.github/workflows/` directories
   - Start fresh from Phase 1
3. **Log regeneration** in new audit.md:
   ```markdown
   ## Regeneration Request

   **Timestamp**: 2025-01-28T14:32:15Z
   **Reason**: [User requested regeneration]
   **Previous State**: [Archived if available]
   **Action**: Deleted .cicd-docs/ and .github/workflows/ directories
   ```
4. **Inform user**: "Regeneration started. All previous workflows and state removed. Starting fresh from Phase 1."

---

### Scenario 4: Partial Rollback (Specific Workflows)

**When to Use**: Only specific workflows need to be removed, not all.

**Procedure**:

1. **Identify workflows to remove**:
   - List specific workflow files (e.g., `python-dev.yml`, `terraform-test.yml`)
2. **Delete specific files**:
   ```bash
   rm .github/workflows/python-dev.yml
   rm .github/workflows/terraform-test.yml
   ```
3. **Update state file**:
   - Remove entries from `generated_files` in `cicd-state.md`
   - Update phase status if needed
4. **Commit changes** (if already committed):
   ```bash
   git add .github/workflows/
   git commit -m "ci(workflows): remove specific workflows (partial rollback)"
   git push
   ```
5. **Log partial rollback** in audit.md
6. **Inform user**: "Partial rollback complete. Specific workflows removed."

---

### Scenario 5: Rollback Due to Error

**When to Use**: Error occurred and workflows are in invalid state.

**Procedure**:

1. **Assess error severity**:
   - Critical: Delete all generated workflows
   - Minor: Fix specific workflows
2. **For critical errors**:
   - Follow Scenario 1 (Rollback Before Commit) or Scenario 3 (Regeneration)
   - Document error in audit.md
   - Fix underlying issue before regenerating
3. **For minor errors**:
   - Fix specific workflows
   - Re-validate
   - Continue from current phase
4. **Log error and rollback** in audit.md
5. **Inform user**: "Error detected. Rollback performed. [Next steps]"

---

## Rollback Best Practices

1. **Always log rollbacks** in audit.md with timestamp and reason
2. **Inform user immediately** when rollback is performed
3. **Preserve state files** if rollback is temporary (unless user requests complete reset)
4. **Use git revert** when possible (preserves history)
5. **Document rollback reason** for future reference
6. **Ask for confirmation** before destructive rollbacks (deleting all workflows)

---

## Prevention Strategies

To minimize need for rollbacks:

1. **Validate workflows** before committing (Phase 2 linting)
2. **Review thoroughly** in Phase 3 before approval
3. **Test workflows** in dev environment first
4. **Use regeneration** for major changes instead of manual edits
5. **Document decisions** in plan files and audit.md

---

## Recovery After Rollback

After performing rollback:

1. **Assess what went wrong** (if applicable)
2. **Fix underlying issues** (if any)
3. **Start fresh** from appropriate phase:
   - Complete rollback: Start from Phase 1
   - Partial rollback: Continue from current phase
   - Regeneration: Start from Phase 1
4. **Learn from rollback** - document patterns to avoid

---

## Rollback Logging Format

All rollbacks should be logged in `.cicd-docs/audit.md`:

```markdown
## Rollback: [Scenario Name]

**Timestamp**: 2025-01-28T14:32:15Z
**Phase**: [Phase where rollback occurred]
**Reason**: [Why rollback was needed]
**Files Removed**: [List of files/directories removed]
**State Changes**: [What state files were modified]
**User Confirmed**: [Yes/No]
**Next Steps**: [What happens next]

---
```
