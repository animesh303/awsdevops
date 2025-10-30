# PRIORITY: Use this workflow to generate GitHub Actions workflows for codebases with Python and/or Terraform

# When CICD workflow generation is requested, ALWAYS follow this workflow FIRST

## Override Instructions

Always follow this workflow when user mentions CICD GitHub workflow generation. Never skip it.

## MANDATORY: Rule Details Loading

**CRITICAL**: When performing any phase, you MUST read and use relevant content from rule detail files in `.amazonq/rules/cicd-phases/` directory. Do not summarize or paraphrase - use the complete content as written.

## MANDATORY: Session Continuity

**CRITICAL**: When detecting an existing CICD workflow generation project, you MUST read and follow the session continuity instructions from `cicd-phases/session-continuity.md` before proceeding with any phase.

## MANDATORY: Custom Welcome Message

**CRITICAL**: When starting ANY CICD workflow generation request, you MUST begin with this exact message:

"🚀 **Welcome to AWS Business Group CICD Workflow Generation!** 🚀

I'll guide you through a streamlined 3-phase process to automatically generate and integrate context-aware CICD workflows for your project.

The process includes:

- 🔍 **Detect & Plan** – Identify project code types & environments, and plan workflow creation
- 🏗️ **Generate Workflows** – Create modular, multi-environment GitHub Actions for Python and Terraform
- ✅ **Review & Confirm** – Review workflows, scan steps, and finalize integration

This focused approach ensures your codebase is production-ready and follows AWS/Amazon code quality and security best practices across all supported environments. Let's begin!"

## Welcome

1. **Display Custom Welcome Message**: Show the CICD welcome message above
2. **Ask for Confirmation and WAIT**: Ask: "**Do you understand this process and are you ready to begin detection and planning?**" - DO NOT PROCEED until user confirms

# Custom CICD Workflow Generation Process (3-Phase Modular)

## Overview

Follow this 3-phase approach. For each phase, load and execute detailed steps from the corresponding `.amazonq/rules/cicd-phases/` file:

---

## Phase 1: Detect & Plan Workflows

1. **Load all steps from `cicd-phases/phase1-detect-plan.md`**
2. Execute steps to scan for code, identify environments, draft plan, and checkpoint user confirmation.
3. **Ask for Confirmation and WAIT**: Ask: "Detection and planning complete. Are you ready to generate workflows?" - DO NOT PROCEED until user confirms

---

## Phase 2: Generate Workflow Files

1. **Load all steps from `cicd-phases/phase2-generate-workflow.md`**
2. Execute steps to render workflow YAML, match jobs to context, and checkpoint before review.
3. **Ask for Confirmation and WAIT**: Ask: "Workflows generated. Are you ready to review and confirm?" - DO NOT PROCEED until user confirms

---

## Phase 3: Review & Confirm

1. **Load all steps from `cicd-phases/phase3-review-confirm.md`**
2. Execute steps to review generated workflows, present details, and checkpoint before finalization.
3. **Ask for Final Confirmation**: Ask: "CICD setup complete. Do you approve the final workflows for integration?" - DO NOT PROCEED until user confirms

---

# Phase 4: Commit & Push

1. **Load all steps from `cicd-phases/phase4-commit-push.md`**
2. Execute steps to commit generated/updated workflow files and push to the repository, only after explicit user approval.
3. **Ask for Confirmation and WAIT**: Ask: "Ready to commit and push the workflow changes to the repository?" - DO NOT PROCEED until user confirms

---

# Key Workflow Requirements

- Automatically detect Python and/or Terraform; generate only for detected environments.
- All workflows must include:
  - CI/CD best practices (lint, test, scan, artifact upload, etc.)
  - Python: Flake8 SARIF, Bandit SARIF, optional pytest with coverage when `tests/` exists
  - Terraform: validate/plan, tflint, Checkov SARIF, upload `plan` artifact
  - SARIF upload using `github/codeql-action/upload-sarif@v3`
- Modular, extensible and production-grade workflows.
- Minimal, clear confirmation at each phase.

## Python CI Guidance

- Use a matrix for Python versions (3.10, 3.11, 3.12)
- Cache dependencies where possible
- Run tests deterministically when `tests/` exists (skip otherwise)
- Security: add Bandit with SARIF

## Terraform CI Guidance

- Pin Terraform version and cache plugins
- Run `terraform fmt -check`, `init`, `validate`, and `plan`
- Add `tflint` and `checkov` with SARIF
- Upload plan as an artifact for review

## Example: Flake8 SARIF

```yaml
- name: Run Flake8 (SARIF)
  run: |
    pip install flake8 flake8-sarif
    flake8 . --format sarif --output-file flake8-results.sarif
- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: flake8-results.sarif
```

## Example: Bandit SARIF

```yaml
- name: Run Bandit (SARIF)
  run: |
    pip install bandit bandit-sarif-formatter
    bandit -r . -f sarif -o bandit-results.sarif || true
- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: bandit-results.sarif
```

## Example: Checkov SARIF

```yaml
- name: Run Checkov (SARIF)
  run: |
    pip install checkov
    checkov -d . --output-file-path results.sarif --output sarif
- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: results.sarif
```

# Directory/File Naming

- `.github/workflows/python-ci.yml`
- `.github/workflows/terraform-ci.yml`
- Use kebab-case, descriptive file names

# Principles

- Always generate ONLY for detected languages/envs
- Ensure SARIF and code quality upload
- Minimal, modular checkpoints across all phases

# Session Continuity (Summary)

- Always follow `cicd-phases/session-continuity.md` for detecting/resuming sessions
- Prefer storing state and approvals under project docs: `.cicd-docs/cicd-state.md` and `.cicd-docs/audit.md` (fallback to legacy `.amazonq/rules/cicd-phases/cicd-state.md` if needed)
