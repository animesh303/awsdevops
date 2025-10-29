# Phase 1: Analyze Code

**Assume the role** of a code analysis specialist

**Universal Phase**: Works with any input - current project code, project files, or mixed content

1. **Analyze Current Project Code**: Examine the code in the current project root:

   - Identify programming languages and frameworks used
   - Analyze project structure and dependencies
   - Review package management files (package.json, requirements.txt, etc.)
   - Identify build tools and scripts
   - Store analysis in `cicd-docs/analysis/code-analysis.md`

2. **Identify CI/CD Requirements**: Determine what CI/CD needs:

   - Build processes and commands
   - Testing frameworks and commands
   - Deployment targets and environments
   - Dependencies and environment variables

3. **Ask Clarifying Questions** (only if needed):

   - Create `cicd-docs/analysis/analysis-questions.md` with questions about unclear areas using [Answer]: tag format
   - Focus on build processes, testing requirements, and deployment needs
   - Request user to fill in all [Answer]: tags directly in the questions document
   - Wait for user answers in the document
   - **Mandatory** keep asking questions until analysis is complete

4. **Generate Code Analysis Document**:

   - Create or update `cicd-docs/analysis/code-analysis.md`
   - Include language, framework, dependencies, and CI/CD requirements
   - Incorporate user's answers to clarifying questions
   - Provide brief summary of analysis findings

5. **Log and Proceed**:
   - Log approval prompt with timestamp in `cicd-docs/audit.md`
   - Wait for explicit user approval before proceeding
   - Record approval response with timestamp
   - Update Phase 1 complete in cicd-state.md
