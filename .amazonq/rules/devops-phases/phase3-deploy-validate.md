# Phase 3: Deploy & Validate

**Assume the role** of a CI/CD validation specialist

**Prerequisites**: Code analysis and GitHub Actions generation must be completed

1. **Deploy GitHub Actions**: Deploy the generated workflows:

   - Commit GitHub Actions files to the repository
   - Set up required secrets and environment variables
   - Trigger initial workflow runs
   - Create `cicd-docs/validation/deployment-log.md`

2. **Validate Pipeline**: Test and validate the CI/CD pipeline:

   - Monitor workflow executions
   - Verify build processes work correctly
   - Test deployment procedures
   - Validate error handling and rollback procedures

3. **Ask Validation Clarifying Questions** (if needed):

   - Create `cicd-docs/validation/validation-questions.md` with questions about validation requirements using [Answer]: tag format
   - Focus on testing procedures, monitoring, and success criteria
   - Request user to fill in all [Answer]: tags directly in the questions document
   - Wait for user answers in the document
   - **Mandatory** keep asking questions until validation approach is clear

4. **Generate Validation Report**:

   - Create or update `cicd-docs/validation/validation-report.md`
   - Include deployment status, test results, and validation outcomes
   - Incorporate user's answers to validation questions
   - Provide brief summary of CI/CD pipeline status

5. **Log and Complete**:
   - Log completion with timestamp in `cicd-docs/audit.md`
   - Record final approval response with timestamp
   - Update Phase 3 complete in cicd-state.md
   - Mark entire CI/CD process as complete
