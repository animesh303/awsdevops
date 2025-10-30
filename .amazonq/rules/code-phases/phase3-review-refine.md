# Phase 3: Review & Refine

**Assume the role** of a code review specialist

**Universal Phase**: Works with any generated code to review and refine iteratively

1. **Present Code Quality Validation**: Run validation checks first:

   - Run final linting and validation checks
   - Confirm security best practices are followed
   - Ensure code follows AWS best practices
   - Validate Terraform configuration is valid
   - Display code quality reports in chat

2. **Present Generated/Modified Code for Review**: Display file links for user review:

   - Present links to NEWLY GENERATED Terraform files (e.g., `{feature-name}-main.tf`, `{feature-name}-variables.tf`)
   - Present links to MODIFIED Terraform files (if existing files were updated)
   - Present links to NEWLY GENERATED Python Lambda code in `src/lambda-{feature-name}/`
   - Present links to MODIFIED Python Lambda files (if existing files were updated)
   - Ask: "Please review the newly generated/modified code using the provided links. What changes would you like to make?"

3. **Handle User Feedback and Updates**: Process user feedback directly:

   - Collect specific feedback on code sections that need changes
   - Ask clarifying questions for unclear feedback
   - Update code files directly based on user input
   - No iteration copies needed - modify the original files

4. **Iterative Refinement Process**: Continue until user approval:

   - Present links to ONLY the files that were updated in the current iteration
   - Re-run linting and quality checks after modifications
   - Display updated code quality reports in chat
   - Ask: "Are there any other changes needed to the code?"
   - Continue updating until user confirms satisfaction

5. **Generate Documentation**: Create implementation documentation:

   - Generate README.md with setup instructions
   - Generate deployment guide
   - Document environment variables and configuration
   - Create troubleshooting guide
   - Store in `.code-docs/documentation/{feature-name}/`

6. **Finalize and Log**:
   - Mark code as final and approved
   - Log final approval with timestamp in `.code-docs/audit.md`
   - Update Phase 3 complete in code-state.md
   - Provide summary of final implementation
