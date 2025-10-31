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

   - Present file paths as clickable links. For maximum IDE compatibility (VS Code/Cursor), use one of these formats in order of preference:
     - **Best for Cursor**: Use `@filename.ext` syntax (e.g., `@iac/terraform/file.tf`) - this creates clickable file references that open directly in the IDE
     - **Alternative**: Relative path from workspace root: `iac/terraform/file.tf` (most IDEs auto-detect these as clickable if the file exists)
     - **Fallback**: Absolute path in backticks: `` `/Users/username/project/iac/terraform/file.tf` ``
   - **Critical**: Always use actual file paths that exist in the workspace (replace placeholders like `{feature-name}` with actual names). Use the workspace root path when available to construct correct relative paths.
   - Example: If a file was created at `iac/terraform/static-website-main.tf`, present it as `@iac/terraform/static-website-main.tf` or `iac/terraform/static-website-main.tf`, NOT as `{feature-name}-main.tf`
   - Present links to NEWLY GENERATED Terraform files using actual paths (e.g., if created `static-website-main.tf`, present as `@iac/terraform/static-website-main.tf` or `iac/terraform/static-website-main.tf`)
   - Present links to MODIFIED Terraform files using actual file paths (if existing files were updated)
   - Present links to NEWLY GENERATED Python Lambda code using actual paths (e.g., `@src/lambda-function-name/app.py` or `src/lambda-function-name/app.py`)
   - Present links to MODIFIED Python Lambda files using actual file paths (if existing files were updated)
   - Ask: "Please review the newly generated/modified code using the provided links. What changes would you like to make?"

3. **Handle User Feedback and Updates**: Process user feedback directly:

   - Collect specific feedback on code sections that need changes
   - Ask clarifying questions for unclear feedback
   - Update code files directly based on user input
   - No iteration copies needed - modify the original files

4. **Iterative Refinement Process**: Continue until user approval:

   - Present links to ONLY the files that were updated in the current iteration, using the same file path format as in step 2 (preferably `@filename` syntax for Cursor, or relative/absolute paths)
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
