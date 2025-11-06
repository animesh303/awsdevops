# CICD Workflow Generation Rules Index

## Purpose

This index provides navigation and overview of all CICD workflow generation rule files. Use this to quickly find relevant documentation.

---

## Main Entry Point

### `cicd-github-workflow.md`

**Purpose**: Main orchestrator file - start here for CICD workflow generation  
**Contains**:

- Welcome process
- 4-phase workflow overview
- Key requirements and principles
- Directory structure

**Read First**: When starting CICD workflow generation

---

## Phase Files

### `phase1-detect-plan.md`

**Purpose**: Phase 1 execution steps - Detect code types and plan workflows  
**Contains**:

- Code detection steps
- Requirements file loading
- Dependency analysis
- Workflow planning

**Related**: `cicd-state.md`, `session-continuity.md`

### `phase2-generate-workflow.md`

**Purpose**: Phase 2 execution steps - Generate workflow YAML files  
**Contains**:

- Workflow generation steps
- Workflow structure requirements
- Language-specific standards application

**Related**: `workflow-common-issues.md`, `workflow-dependency-handling.md`, `{code-type}-standards.md`

### `phase3-review-confirm.md`

**Purpose**: Phase 3 execution steps - Review and confirm workflows  
**Contains**:

- Review procedures
- Validation checks
- User approval process

**Related**: `validation-checklist.md`

### `phase4-commit-push.md`

**Purpose**: Phase 4 execution steps - Commit and push workflows  
**Contains**:

- Git operations
- Commit message format
- Push procedures

**Related**: `rollback-procedures.md`

---

## Supporting Documents

### `session-continuity.md`

**Purpose**: Session management and resumption  
**Contains**:

- Session detection
- Resume logic
- Welcome back prompts
- State file management

**Use When**: Resuming interrupted session or detecting existing session

### `workflow-common-issues.md`

**Purpose**: Common issues and solutions when generating workflows  
**Contains**:

- `hashFiles()` limitations
- Checkout step requirements
- Artifact download issues
- Circular dependencies
- YAML syntax errors

**Use When**: Troubleshooting workflow generation errors

### `workflow-dependency-handling.md`

**Purpose**: Comprehensive dependency handling patterns  
**Contains**:

- Single dependency patterns
- Multiple dependency patterns
- Artifact passing methods (5 methods)
- Environment-specific considerations
- Orchestrator workflow pattern (always used)
- Best practices

**Use When**: Implementing dependencies between code artifacts

### `orchestrator-workflow-patterns.md`

**Purpose**: Orchestrator workflow patterns (always used for consistency)  
**Contains**:

- Two-tier architecture (orchestrator + code type workflows)
- Dependency resolution using topological sort
- Orchestrator workflow structure and patterns
- Code type workflow modifications for orchestrator compatibility
- Environment-specific orchestrators (dev/test/prd)
- Benefits of always using orchestrators
- Implementation checklist

**Use When**: Generating workflows (orchestrators are always generated for consistency)

### `error-handling.md`

**Purpose**: Error scenarios and response procedures  
**Contains**:

- Phase-specific error handling
- Error recovery procedures
- Error logging format
- Best practices

**Use When**: Encountering errors during workflow generation

### `rollback-procedures.md`

**Purpose**: Rollback and undo procedures  
**Contains**:

- Rollback scenarios (5 scenarios)
- Before/after commit rollback
- Regeneration procedures
- Partial rollback
- Recovery after rollback

**Use When**: Need to undo changes or start over

### `validation-checklist.md`

**Purpose**: Comprehensive validation criteria  
**Contains**:

- Phase 1 validation checklist
- Phase 2 validation checklist
- Phase 3 validation checklist
- Phase 4 validation checklist
- Comprehensive checklist

**Use When**: Validating workflows before proceeding to next phase

### `cicd-state.md`

**Purpose**: State file template  
**Contains**:

- State file structure
- Field definitions
- Update procedures
- Phase checkboxes

**Use When**: Creating or updating state files

---

## Standards Files

### `python-standards.md`

**Purpose**: Python CI/CD workflow patterns  
**Contains**:

- Python lint job patterns
- Python security job patterns
- Python test job patterns
- Python deployment patterns
- Dependency handling for Python

**Use When**: Generating workflows for Python code

### `terraform-standards.md`

**Purpose**: Terraform CI/CD workflow patterns  
**Contains**:

- Terraform validate job patterns
- Terraform plan job patterns
- Terraform security job patterns
- Terraform deployment patterns
- Dependency handling for Terraform

**Use When**: Generating workflows for Terraform code

### `{code-type}-standards.md`

**Purpose**: Language-specific CI/CD patterns  
**Pattern**: One file per code type (e.g., `javascript-standards.md`, `java-standards.md`)  
**Use When**: Generating workflows for specific code types

---

## Quick Reference Guide

### Starting Workflow Generation

1. Read `cicd-github-workflow.md` (main file)
2. Follow Welcome process
3. Execute phases in order

### During Workflow Generation

- **Phase 1**: Follow `phase1-detect-plan.md`
- **Phase 2**: Follow `phase2-generate-workflow.md`, reference `workflow-common-issues.md`, `workflow-dependency-handling.md`, and `orchestrator-workflow-patterns.md`
- **Phase 3**: Follow `phase3-review-confirm.md`, use `validation-checklist.md`
- **Phase 4**: Follow `phase4-commit-push.md`

### Troubleshooting

- **Workflow errors**: See `workflow-common-issues.md`
- **Dependency issues**: See `workflow-dependency-handling.md` and `orchestrator-workflow-patterns.md`
- **General errors**: See `error-handling.md`
- **Need to rollback**: See `rollback-procedures.md`

### Resuming Session

- See `session-continuity.md` for session detection and resumption

### Validation

- Use `validation-checklist.md` before proceeding to next phase

---

## File Organization

```
.amazonq/rules/
├── cicd-github-workflow.md          # Main orchestrator
└── cicd-phases/
    ├── INDEX.md                      # This file
    ├── phase1-detect-plan.md         # Phase 1
    ├── phase2-generate-workflow.md   # Phase 2
    ├── phase3-review-confirm.md      # Phase 3
    ├── phase4-commit-push.md         # Phase 4
    ├── session-continuity.md         # Session management
    ├── workflow-common-issues.md    # Common issues
    ├── workflow-dependency-handling.md # Dependencies
    ├── orchestrator-workflow-patterns.md # Orchestrator patterns
    ├── error-handling.md             # Error handling
    ├── rollback-procedures.md        # Rollback procedures
    ├── validation-checklist.md      # Validation checklist
    ├── cicd-state.md                 # State template
    ├── python-standards.md           # Python patterns
    ├── terraform-standards.md        # Terraform patterns
    └── {code-type}-standards.md      # Other language patterns
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

- `orchestrator-dev.yml` - Orchestrator for dev environment (if dependencies exist)
- `orchestrator-test.yml` - Orchestrator for test environment (if dependencies exist)
- `orchestrator-prd.yml` - Orchestrator for prod environment (if dependencies exist)
- `{code-type}-dev.yml` - Dev environment workflows
- `{code-type}-test.yml` - Test environment workflows
- `{code-type}-prd.yml` - Prod environment workflows

---

## Getting Help

1. **Start with main file**: `cicd-github-workflow.md`
2. **Check phase file**: For phase-specific steps
3. **Reference supporting docs**: For detailed patterns and troubleshooting
4. **Use validation checklist**: Before proceeding
5. **Check error handling**: If issues occur

---

## Version Information

**Last Updated**: 2025-01-28  
**Version**: 2.0 (After improvements and reorganization)
