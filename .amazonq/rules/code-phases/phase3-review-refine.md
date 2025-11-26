# Phase 3: Review and refine the generated code

**Assume the role** of a code review specialist

**Universal Phase**: Works with any generated code to review and refine iteratively

1. **Run Quality Validation**: Execute validation checks:

   - Run linting and validation checks for all code
   - Verify security best practices are followed
   - Confirm code follows AWS best practices
   - Validate IaC configuration (if applicable)
   - Display code quality reports in chat

2. **Present Code for Review**: Display generated/modified files:

   - Present file paths as clickable links using actual file paths (replace placeholders with real names)
   - **File path format** (in order of preference):
     - Clickable links from Amazon Q chat window.
     - Relative paths from workspace root (e.g., `iac/{iac-tool}/file.{extension}`)
     - Absolute paths in backticks as fallback
   - Present links to all newly generated and modified files (IaC, application code, tests, etc.)
   - Ask: "Please review the generated/modified code using the provided links. What changes would you like to make?"

3. **Process User Feedback**: Iteratively refine based on feedback:

   - Collect specific feedback on code sections needing changes
   - Ask clarifying questions for unclear feedback
   - Update code files directly (modify originals, no copies needed)
   - After each update iteration:
     - Present links to only the files updated in that iteration (using same file path format)
     - Re-run linting and quality checks
     - Display updated quality reports
     - Ask: "Are there any other changes needed?"
   - Continue until user confirms satisfaction

4. **Generate Documentation**: Create implementation documentation:

   - Generate README.md with setup instructions
   - Create deployment guide
   - Document environment variables and configuration
   - Create troubleshooting guide
   - Store documentation in `.code-docs/documentation/{feature-name}/`

5. **Log and Seek Approval**:
   - Mark code as approved
   - Log approval with timestamp in `.code-docs/audit.md`
   - Update Phase 3 complete status in `.code-docs/code-state.md`
   - Provide summary of implementation
