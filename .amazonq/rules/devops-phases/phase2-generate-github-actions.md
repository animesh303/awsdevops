# Phase 2: Generate GitHub Actions

**Assume the role** of a GitHub Actions specialist

**Prerequisites**: Code analysis must be completed

1. **Design GitHub Actions Workflows**: Create workflow designs based on code analysis:

   - Plan build workflow for the identified language/framework
   - Design test workflow with appropriate testing commands
   - Plan deployment workflow for target environments
   - Create `cicd-docs/github-actions/workflow-design.md`

2. **Generate GitHub Actions Files**: Create actual workflow files:

   - Generate `.github/workflows/build.yml` for build process
   - Generate `.github/workflows/test.yml` for testing
   - Generate `.github/workflows/deploy.yml` for deployment
   - Include appropriate environment variables and secrets

3. **Ask GitHub Actions Clarifying Questions** (if needed):

   - Create `cicd-docs/github-actions/actions-questions.md` with questions about workflow requirements using [Answer]: tag format
   - Focus on build steps, test commands, and deployment targets
   - Request user to fill in all [Answer]: tags directly in the questions document
   - Wait for user answers in the document
   - **Mandatory** keep asking questions until workflow design is clear

4. **Generate GitHub Actions Files**:

   - Create actual `.github/workflows/` files in the project
   - Include comprehensive workflows for build, test, and deploy
   - Incorporate user's answers to workflow questions
   - Provide brief summary of generated workflows

5. **Log and Proceed**:
   - Log approval prompt with timestamp in `cicd-docs/audit.md`
   - Wait for explicit user approval before proceeding
   - Record approval response with timestamp
   - Update Phase 2 complete in cicd-state.md
