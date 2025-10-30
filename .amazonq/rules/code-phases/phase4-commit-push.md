# Code Generation Phase 4: Commit & Push Changes (Optional)

## Purpose

Provide an optional, user-confirmed step to commit and push the generated/updated code (Terraform, Lambdas, tests, docs). Allow the user to skip.

## Preconditions

- Phases 1–3 are complete and approved by the user.
- Working tree contains generated/updated files.

## Steps

1. **Checkpoint: Ask to Commit & Push or Skip**

   - Prompt: "Do you want me to commit and push the generated code changes now, or skip this step?"
   - If user chooses skip: stop here with a short confirmation message.
   - If user chooses commit: continue.

2. **Configure Git Identity (if needed)**

   - Ensure Git user identity is set (fallback if not configured):
     - `git config user.name "automation-bot"`
     - `git config user.email "automation-bot@local"`

3. **Stage Changes**

   - Stage all repository changes (respects `.gitignore`):
     - `git add -A`

4. **Commit Changes with Structured Message**

   - Commit message format:
     - `feat(codegen): add/refresh generated Terraform and Lambda code`
     - Include JIRA reference when available: `Refs: {TICKET-NUMBER}`
     - Suggested body bullets:
       - Validate Terraform (`fmt`, `init -backend=false`, `validate`) passed
       - Apply resource tags: `JiraId`, `ManagedBy=terraform`
       - Include lint and security checks outputs where applicable

5. **Push Changes**

   - Push to origin: `git push -u origin <branch>`
   - If push fails due to auth/permissions, report the error and stop.

## Safety Checks

- Respect `.gitignore`; avoid committing secrets or build outputs.
- Confirm Terraform validation passes (Phase 2 requirements) before committing.
- Ensure SARIF/report paths referenced in CI exist or are guarded.

## Outputs

- Either: Skipped commit/push per user choice, or branch pushed with committed changes.


