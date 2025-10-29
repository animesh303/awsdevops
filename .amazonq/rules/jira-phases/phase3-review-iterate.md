# Phase 3: Review & Iterate

**Assume the role** of a requirements review specialist

**Universal Phase**: Works with any generated requirements document to verify and update iteratively

1. **Present Requirements for Review**: Display the generated requirements document:

   - Show the complete requirements document from `jira-docs/requirements/{TICKET-NUMBER}_requirements.md`
   - Ask: "Please review the requirements document. What changes would you like to make?"

2. **Handle User Feedback and Updates**: Process user feedback directly:

   - Collect specific feedback on sections that need changes
   - Ask clarifying questions for unclear feedback
   - Update the requirements document directly based on user input
   - No iteration copies needed - modify the original document

3. **Iterative Refinement Process**: Continue until user approval:

   - Present updated requirements after each change
   - Ask: "Are there any other changes needed to the requirements?"
   - Continue updating the same document until user confirms satisfaction

4. **Final Validation**: Ensure requirements are complete and approved:

   - Verify all user feedback has been addressed
   - Confirm requirements align with original JIRA ticket
   - Ensure technical specifications are implementation-ready
   - Validate acceptance criteria are clear and testable

5. **Finalize and Log**:
   - Mark requirements as final and approved
   - Log final approval with timestamp in `jira-docs/audit.md`
   - Update Phase 3 complete in jira-state.md
   - Provide summary of final requirements document
