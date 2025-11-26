
# Phase 1: Analyze Changes

**Assume the role** of a senior code reviewer and software architect

**Universal Phase**: Works with any code changes to analyze and plan review

1. **Identify Code Changes**: Determine what code is being reviewed:

   - **If PR/Branch specified**: Analyze changes in PR or branch
     - **Use GitHub MCP Server**: Fetch PR details using `github-mcp-server`:
       - Get PR number, title, description
       - Get list of changed files via MCP
       - Get diff/change summary via MCP
       - Get commit history via MCP
     - **Use Git MCP Server**: Fetch branch and commit details using `git-mcp-server`:
       - Get branch information
       - Get commit history
       - Get file diffs
   - **If files specified**: Analyze specified files
     - Read changed files
     - Compare with base version (if available)
     - Use Git MCP to fetch base version if needed
   - **If no specification**: Analyze recent changes
     - **Use Git MCP Server**: Check git status for modified files
     - **Use Git MCP Server**: Check recent commits
   - Store change list in `.review-docs/changed-files.md`

2. **Analyze Change Scope**: Understand the scope of changes:

   - **File Analysis**:
     - Count files changed (added, modified, deleted)
     - Count lines changed (added, deleted, modified)
     - Identify file types (source code, config, tests, docs)
   - **Change Type Analysis**:
     - Identify if changes are: new feature, bug fix, refactoring, documentation, test
     - Identify affected modules/components
     - Identify dependencies and impact areas
   - Store analysis in `.review-docs/change-analysis.md`

3. **Understand Context**: Gather context about changes:

   - **PR Context** (if applicable):
     - Read PR description
     - Read PR comments and discussions
     - Understand PR purpose and requirements
   - **Commit Context**:
     - Read commit messages
     - Understand commit history and progression
   - **Related Code**:
     - Read related files that interact with changed code
     - Understand codebase structure and patterns
   - Store context in `.review-docs/review-context.md`

4. **Identify Review Scope**: Determine what to review:

   - **Code Quality**: Code structure, readability, maintainability
   - **Security**: Security vulnerabilities, security best practices
   - **Performance**: Performance implications, optimization opportunities
   - **Best Practices**: Language-specific patterns, AWS best practices
   - **Testing**: Test coverage, test quality
   - **Documentation**: Code comments, documentation updates
   - Store scope in `.review-docs/review-plan.md`

5. **Detect Languages and Frameworks**: Identify technologies used:

   - **Programming Languages**: Python, TypeScript, Java, Go, etc.
   - **Frameworks**: React, Django, Spring, etc.
   - **Infrastructure**: Terraform, CloudFormation, CDK
   - **Tools**: Build tools, testing frameworks
   - Store detection in `.review-docs/technology-stack.md`

6. **Create Review Plan**: Develop comprehensive review strategy:

   - **Review Categories**: Define categories to review
   - **Review Priorities**: Identify high-priority areas
   - **Review Checklist**: Create checklist based on languages/frameworks
   - **Review Standards**: Identify standards to apply (language-specific, AWS)
   - Store plan in `.review-docs/review-plan.md`

7. **Load Review Standards**: Load language-specific review standards:

   - **For each detected language**:
     - Read standards from `review-phases/{language}-review-standards.mdc`
     - Apply standards to review plan
     - Note any missing standards files

8. **Log and Seek Approval**:
   - Log change analysis with timestamp in `.review-docs/audit.md`
   - Present change analysis summary to user
   - Present review plan and scope
   - Wait for explicit user approval before proceeding
   - Record approval response with timestamp
   - Update Phase 1 complete status in `.review-docs/review-state.md`
