# Code Generation Phase 4: Commit & Push Changes

## Purpose

Provide an optional, user-confirmed step to commit and push the generated/updated code (IAC, application code, tests, docs). Allow the user to skip.

## Preconditions

- Phases 1–3 are complete and approved by the user.
- Working tree contains generated/updated files.

## Steps

1. **Checkpoint: Explicit User Approval (Mandatory)**

   - Prompt: "Do you want me to commit and push the generated code changes now?"
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
     - `feat(codegen): add/refresh generated {iac-tool} and {runtime-type} code`
     - Include JIRA reference when available: `Refs: {TICKET-NUMBER}`
     - Suggested body bullets:
       - Validate IAC configuration (tool-specific validation) passed
       - Apply resource tags: `JiraId`, `ManagedBy={iac-tool}`
       - Include lint and security checks outputs where applicable
       - **Note**: Replace {iac-tool} and {runtime-type} with actual values read from `.code-docs/requirements/{TICKET-NUMBER}-analysis.md`

5. **Push Changes**

   - Push to origin: `git push -u origin <branch>`
   - If push fails due to auth/permissions, report the error and stop.

## Safety Checks

- Respect `.gitignore`; avoid committing secrets or build outputs.
- Confirm IAC validation passes (Phase 2 requirements, tool-specific) before committing.
- Ensure SARIF/report paths referenced in CI exist or are guarded.

## Outputs

- Branch pushed with committed changes.
