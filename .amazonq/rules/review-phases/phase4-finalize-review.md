# Phase 4: Finalize Review

**Assume the role** of a senior code reviewer and project manager

**Universal Phase**: Works with any review to finalize and track completion

1. **Consolidate Review**: Consolidate all review artifacts:

   - Read all findings from `.review-docs/findings/`
   - Read feedback from `.review-docs/feedback.md`
   - Read action items from `.review-docs/action-items.md`
   - Read recommendations from `.review-docs/recommendations.md`
   - Create comprehensive review document

2. **Create Final Review Report**: Generate comprehensive review report:

   - **Executive Summary**: High-level review summary
   - **Review Statistics**: Counts of findings by category and severity
   - **Key Findings**: Most important findings
   - **Recommendations**: Top recommendations
   - **Action Items**: Complete list of action items
   - **Review Status**: Overall review status (Approved/Changes Requested/Blocked)
   - Store report in `.review-docs/reports/final-review-report.md`

3. **Determine Review Status**: Determine overall review status:

   - **Approved**: No critical issues, code is ready
   - **Changes Requested**: Some issues need to be addressed
   - **Blocked**: Critical issues prevent approval
   - Store status in `.review-docs/review-status.md`

4. **Track Action Items**: Set up action item tracking:

   - **Action Item List**: Complete list of all action items
   - **Status Tracking**: Track status of each action item
   - **Priority**: Maintain priority for each action item
   - **Assignment**: Assign action items (if applicable)
   - Store tracking in `.review-docs/action-items-tracking.md`

5. **Create Review Checklist**: Create checklist for follow-up:

   - **Must Fix Items**: Critical items that must be fixed
   - **Should Fix Items**: Important items that should be fixed
   - **Verification**: How to verify fixes
   - Store checklist in `.review-docs/review-checklist.md`

6. **Generate Review Summary**: Create concise review summary:

   - **Review Overview**: Brief overview of review
   - **Key Metrics**: Review statistics and metrics
   - **Status**: Review status and next steps
   - **Timeline**: Review timeline and milestones
   - Store summary in `.review-docs/review-summary.md`

7. **Update Review State**: Update review state tracking:

   - Mark Phase 4 as complete
   - Update overall review status
   - Record completion timestamp
   - Update `.review-docs/review-state.md`

8. **Prepare for Follow-up**: Prepare for review follow-up:

   - **Action Items**: Ensure all action items are tracked
   - **Follow-up Plan**: Plan for follow-up review if needed
   - **Communication**: Prepare communication for stakeholders

9. **Log and Seek Final Approval**:
   - Log review finalization with timestamp in `.review-docs/audit.md`
   - Present final review report to user
   - Present review status and action items
   - Wait for explicit user approval
   - Record approval response with timestamp
   - Update Phase 4 complete status in `.review-docs/review-state.md`
