# CI/CD Session Continuity

## Purpose

Ensures seamless continuation of CI/CD processes across sessions by maintaining state and context.

## Session State Management

- **Current Phase Tracking**: Always track which CI/CD phase is currently active
- **Artifact Loading**: Load all relevant artifacts from previous phases
- **Context Preservation**: Maintain pipeline decisions and configurations
- **Progress Tracking**: Track completion status of each phase

## Context Loading Rules

1. **Always read cicd-state.md first** to understand current phase
2. **Load incrementally** - each phase needs context from all previous phases
3. **Pipeline phases are special** - must read existing pipeline configuration files
4. **Provide context summary** - briefly tell user what artifacts were loaded
5. **Never assume** - always load the actual files, don't rely on memory

## Phase-Specific Context Loading

- **Phase 1**: Load existing code analysis if available
- **Phase 2**: Load code analysis + GitHub Actions designs
- **Phase 3**: Load ALL cicd artifacts + existing GitHub Actions files

## State Persistence

- **cicd-state.md**: Master state tracking file with phase checkboxes
- **cicd-audit.md**: Record approvals and decisions with timestamps
- **Artifact Storage**: All planning documents and pipeline configurations
- **Progress Tracking**: Checkbox system for phase completion

## Resume Instructions

When resuming a CI/CD session:

1. Load cicd-state.md to understand current phase
2. Load all relevant artifacts from previous phases
3. Provide context summary to user
4. Continue from current phase with full context
5. Update progress tracking as phases complete
