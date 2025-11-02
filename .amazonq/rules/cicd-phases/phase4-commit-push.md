# CICD Workflow Generation Phase 4: Commit & Push Changes

## Purpose

Safely commit and push generated/updated GitHub Actions workflow files after explicit user approval, ensuring traceability and adherence to repository conventions.

## Preconditions

- Phase 1–3 are complete and approved by the user.
- Working tree contains generated/updated files under `.github/workflows/` and any supporting docs.

## Steps

1. **Checkpoint: Explicit User Approval (Mandatory)**

   - Ask: "Ready to commit and push the workflow changes to the repository?"
   - WAIT for user confirmation. Do not proceed without approval.

2. **Configure Git Identity (if needed)**

   - Ensure Git user identity is set (fallback if not configured):
     - `git config user.name "automation-bot"`
     - `git config user.email "automation-bot@local"`

3. **Stage Changes**

   - Stage all repository changes (respects `.gitignore`):
     - `git add -A`

4. **Commit Changes with Structured Message**

   - Commit message format:
     - `ci(workflows): generate/refresh GitHub Actions for Python/Terraform`
     - Include references such as JIRA ID if available: `Refs: {TICKET-NUMBER}`
     - Example full message:
       - Subject: `ci(workflows): add Python and Terraform CI with SARIF uploads`
       - Body (bullets):
         - Ensure `security-events: read` permission
         - Add Flake8/Bandit SARIF, tflint, Checkov SARIF
         - Validate Terraform config (`fmt`, `init -backend=false`, `validate`)
         - Tag resources with `JiraId` where applicable

5. **Push Changes**

   - Push to origin: `git push -u origin <branch>`
   - If push fails due to auth or permissions, report the error and stop.

6. **Optional: Open Pull Request (If Supported/Requested)**
   - If repository tooling allows, propose opening a PR from the branch to the default branch and include the commit summary.
   - Otherwise, instruct the user on opening a PR manually.

## Validation & Safety Checks

- Ensure no uncommitted sensitive files are included (respect `.gitignore`).
- Verify that SARIF paths referenced in workflows exist or jobs guard against missing files.
- Confirm that Terraform validation guidance has been followed in Phase 2 before committing.

## Outputs

- Branch pushed to remote containing all generated workflow changes.
- Commit with structured message linking to relevant ticket (if available).
