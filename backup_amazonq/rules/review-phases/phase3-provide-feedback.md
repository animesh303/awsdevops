
# Phase 3: Provide Feedback

**Assume the role** of a senior code reviewer and technical mentor

**Universal Phase**: Works with any review findings to generate actionable feedback

1. **Review Findings**: Consolidate all review findings:

   - Read findings from `.review-docs/findings/` directory
   - Understand severity and impact of each finding
   - Group related findings together
   - Prioritize findings by severity and impact

2. **Generate Constructive Feedback**: Create actionable feedback:

   - **For each finding**:
     - **Issue Description**: Clear description of the issue
     - **Impact**: Explain why it matters
     - **Recommendation**: Specific recommendation to fix
     - **Example**: Provide code example if helpful
     - **Priority**: Critical/High/Medium/Low
   - **Feedback Format**:
     - Be constructive and helpful
     - Focus on improvement, not criticism
     - Provide specific, actionable suggestions
     - Include positive feedback for good practices
   - Store feedback in `.review-docs/feedback.md`

3. **Create Action Items**: Generate actionable items:

   - **For each critical/high priority finding**:
     - Create specific action item
     - Assign priority
     - Provide clear acceptance criteria
   - **Action Item Format**:
     - Title: Clear, concise description
     - Priority: Critical/High/Medium/Low
     - Description: Detailed explanation
     - Acceptance Criteria: How to verify completion
     - File/Line Reference: Where the issue is located
   - Store action items in `.review-docs/action-items.md`

4. **Generate Recommendations**: Provide improvement recommendations:

   - **Code Improvements**: Suggestions for code improvements
   - **Architecture Improvements**: Suggestions for architecture improvements
   - **Best Practices**: Recommendations for best practices
   - **Performance Optimizations**: Performance improvement suggestions
   - **Security Enhancements**: Security improvement suggestions
   - Store recommendations in `.review-docs/recommendations.md`

5. **Create Review Comments**: Generate inline review comments (if applicable):

   - **For specific code locations**:
     - Create inline comments with file and line references
     - Provide context and explanation
     - Suggest specific fixes
   - **Use GitHub MCP Server**: Post comments to GitHub PR (if PR review):
     - Post inline comments using `github-mcp-server` for specific file/line locations
     - Post general comments using `github-mcp-server` for overall feedback
     - Update PR status based on review findings
   - Store comments in `.review-docs/inline-comments.md`

6. **Summarize Review**: Create review summary:

   - **Overall Assessment**: High-level assessment of code quality
   - **Key Findings**: Summary of most important findings
   - **Recommendations**: Top recommendations
   - **Next Steps**: Suggested next steps
   - Store summary in `.review-docs/review-summary.md`

7. **Categorize Feedback**: Organize feedback by category:

   - **Must Fix**: Critical issues that must be addressed
   - **Should Fix**: Important issues that should be addressed
   - **Nice to Have**: Suggestions for improvement
   - **Positive Feedback**: Acknowledge good practices
   - Store categorization in `.review-docs/feedback-categories.md`

8. **Validate Feedback Quality**: Ensure feedback is helpful:

   - **Actionable**: All feedback should be actionable
   - **Specific**: Feedback should be specific, not vague
   - **Constructive**: Feedback should be helpful and constructive
   - **Prioritized**: Feedback should be prioritized appropriately

9. **Log and Seek Approval**:
   - Log feedback generation with timestamp in `.review-docs/audit.md`
   - Present feedback summary to user
   - Present action items to user
   - Wait for explicit user approval before proceeding
   - Record approval response with timestamp
   - Update Phase 3 complete status in `.review-docs/review-state.md`
