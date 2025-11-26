## Phase Files

### `phase1-detect-plan.mdc`

**Purpose**: Phase 1 execution steps - Detect code types and plan workflows  
**Contains**:

- Code detection steps
- Requirements file loading
- Dependency analysis
- Workflow planning

**Related**: `cicd-state.mdc`, `session-continuity.mdc`

### `phase2-generate-workflow.mdc`

**Purpose**: Phase 2 execution steps - Generate workflow YAML files  
**Contains**:

- Workflow generation steps
- Workflow structure requirements
- Language-specific standards application

**Related**: `workflow-common-issues.mdc`, `workflow-dependency-handling.mdc`, `{code-type}-standards.mdc`

### `phase3-review-confirm.mdc`

**Purpose**: Phase 3 execution steps - Review and confirm workflows  
**Contains**:

- Review procedures
- Validation checks
- User approval process

**Related**: `validation-checklist.mdc`

### `phase4-commit-push.mdc`

**Purpose**: Phase 4 execution steps - Commit and push workflows  
**Contains**:

- Git operations
- Commit message format
- Push procedures

**Related**: `rollback-procedures.mdc`

---

## Supporting Documents

### `session-continuity.mdc`

**Purpose**: Session management and resumption  
**Contains**:

- Session detection
- Resume logic
- Welcome back prompts
- State file management

**Use When**: Resuming interrupted session or detecting existing session

### `workflow-common-issues.mdc`

**Purpose**: Common issues and solutions when generating workflows  
**Contains**:

- `hashFiles()` limitations
- Checkout step requirements
- Artifact download issues
- Circular dependencies
- YAML syntax errors

**Use When**: Troubleshooting workflow generation errors

### `workflow-dependency-handling.mdc`

**Purpose**: Comprehensive dependency handling patterns  
**Contains**:

- Single dependency patterns
- Multiple dependency patterns
- Artifact passing methods (5 methods)
- Single environment considerations
- Best practices

**Use When**: Implementing dependencies between code artifacts

### `error-handling.mdc`

**Purpose**: Error scenarios and response procedures  
**Contains**:

- Phase-specific error handling
- Error recovery procedures
- Error logging format
- Best practices

**Use When**: Encountering errors during workflow generation

### `rollback-procedures.mdc`

**Purpose**: Rollback and undo procedures  
**Contains**:

- Rollback scenarios (5 scenarios)
- Before/after commit rollback
- Regeneration procedures
- Partial rollback
- Recovery after rollback

**Use When**: Need to undo changes or start over

### `validation-checklist.mdc`

**Purpose**: Comprehensive validation criteria  
**Contains**:

- Phase 1 validation checklist
- Phase 2 validation checklist
- Phase 3 validation checklist
- Phase 4 validation checklist
- Comprehensive checklist

**Use When**: Validating workflows before proceeding to next phase

### `cicd-state.mdc`

**Purpose**: State file template  
**Contains**:

- State file structure
- Field definitions
- Update procedures
- Phase checkboxes

**Use When**: Creating or updating state files

---

## Standards Files

### `python-standards.mdc`

**Purpose**: Python CI/CD workflow patterns  
**Contains**:

- Python lint job patterns
- Python security job patterns
- Python test job patterns
- Python deployment patterns
- Dependency handling for Python

**Use When**: Generating workflows for Python code

### `terraform-standards.mdc`

**Purpose**: Terraform CI/CD workflow patterns  
**Contains**:

- Terraform validate job patterns
- Terraform plan job patterns
- Terraform security job patterns
- Terraform deployment patterns
- Dependency handling for Terraform

**Use When**: Generating workflows for Terraform code

### `{code-type}-standards.mdc`

**Purpose**: Language-specific CI/CD patterns  
**Pattern**: One file per code type (e.g., `javascript-standards.mdc`, `java-standards.mdc`)  
**Use When**: Generating workflows for specific code types

---

## Quick Reference Guide

### Starting Workflow Generation

1. Read `cicd-github-workflow.mdc` (main file)
2. Follow Welcome process
3. Execute phases in order

### During Workflow Generation

- **Phase 1**: Follow `phase1-detect-plan.mdc`
- **Phase 2**: Follow `phase2-generate-workflow.mdc`, reference `workflow-common-issues.mdc`, `workflow-dependency-handling.mdc`
- **Phase 3**: Follow `phase3-review-confirm.mdc`, use `validation-checklist.mdc`
- **Phase 4**: Follow `phase4-commit-push.mdc`

### Troubleshooting

- **Workflow errors**: See `workflow-common-issues.mdc`
- **Dependency issues**: See `workflow-dependency-handling.mdc`
- **General errors**: See `error-handling.mdc`
- **Need to rollback**: See `rollback-procedures.mdc`

### Resuming Session

- See `session-continuity.mdc` for session detection and resumption

### Validation

- Use `validation-checklist.mdc` before proceeding to next phase

---

## File Organization

```
.amazonq/rules/
├── cicd-github-workflow.mdc          # Main orchestrator
└── cicd-phases/
    ├── INDEX.mdc                      # This file
    ├── phase1-detect-plan.mdc         # Phase 1
    ├── phase2-generate-workflow.mdc   # Phase 2
    ├── phase3-review-confirm.mdc      # Phase 3
    ├── phase4-commit-push.mdc         # Phase 4
    ├── session-continuity.mdc         # Session management
    ├── workflow-common-issues.mdc    # Common issues
    ├── workflow-dependency-handling.mdc # Dependencies
    ├── error-handling.mdc             # Error handling
    ├── rollback-procedures.mdc        # Rollback procedures
    ├── validation-checklist.mdc      # Validation checklist
    ├── cicd-state.mdc                 # State template
    ├── python-standards.mdc           # Python patterns
    ├── terraform-standards.mdc        # Terraform patterns
    └── {code-type}-standards.mdc      # Other language patterns
```

---

## Related Project Files

### `.cicd-docs/` Directory

- `cicd-state.md` - Current session state (preferred location)
- `audit.md` - Approval and interaction logs
- `detection-plan.md` - Phase 1 plan document
- `workflow-generation-plan.md` - Phase 2 plan document
- `review-notes.md` - Phase 3 review notes

### `.github/workflows/` Directory

- `ci-cd.yml` - Single production workflow containing all code types (triggered by main branch, jobs sequenced by dependencies)

---

## Getting Help

1. **Start with main file**: `cicd-github-workflow.mdc`
2. **Check phase file**: For phase-specific steps
3. **Reference supporting docs**: For detailed patterns and troubleshooting
4. **Use validation checklist**: Before proceeding
5. **Check error handling**: If issues occur

---

## Version Information

**Last Updated**: 2025-01-28  
**Version**: 2.0 (After improvements and reorganization)
