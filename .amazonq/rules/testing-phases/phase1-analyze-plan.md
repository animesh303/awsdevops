# Phase 1: Analyze & Plan

**Assume the role** of a senior test engineer and quality assurance specialist

**Universal Phase**: Works with any codebase to analyze and plan comprehensive testing

1. **Analyze Codebase Structure**: Scan repository for code to test:

   - Scan `src/` directory for application code
   - Scan `iac/` directory for infrastructure code
   - Identify programming languages and frameworks:
     - **Python**: `.py` files, `requirements.txt`, `pytest.ini`
     - **TypeScript/JavaScript**: `.ts`, `.tsx`, `.js`, `.jsx` files, `package.json`, `jest.config.js`
     - **Java**: `.java` files, `pom.xml`, `build.gradle`
     - **Go**: `.go` files, `go.mod`
     - **Terraform**: `.tf` files
   - Count files by type and language
   - Store analysis in `.test-docs/codebase-analysis.md`

2. **Identify Existing Tests**: Check for existing test infrastructure:

   - Scan `tests/` directory for existing test files
   - Identify test frameworks in use:
     - Python: pytest, unittest, nose2
     - TypeScript/JavaScript: Jest, Mocha, Jasmine
     - Java: JUnit, TestNG
     - Go: testing package, testify
     - Terraform: Terratest, Kitchen-Terraform
   - Analyze test coverage of existing tests
   - Store inventory in `.test-docs/existing-tests-inventory.md`

3. **Determine Test Requirements**: Analyze code to identify test needs:

   - **Unit Tests**: Identify functions, classes, modules that need unit tests
   - **Integration Tests**: Identify service interactions, API endpoints, database operations
   - **E2E Tests**: Identify complete user workflows and system interactions
   - **Performance Tests**: Identify performance-critical components
   - **Security Tests**: Identify security-sensitive code paths
   - Store requirements in `.test-docs/test-requirements.md`

4. **Create Test Strategy**: Develop comprehensive test plan:

   - Define test pyramid (unit > integration > E2E ratio)
   - Set coverage targets (minimum 80% code coverage)
   - Identify test frameworks and tools for each language
   - Plan test data requirements
   - Plan mock/stub requirements
   - Plan CI/CD integration approach
   - Store strategy in `.test-docs/test-plan.md`

5. **Identify Test Dependencies**: Determine what's needed for testing:

   - External services and APIs to mock
   - Test databases or data stores
   - Test infrastructure requirements
   - Environment variables and configuration
   - Store dependency list in `.test-docs/test-dependencies.md`

6. **Validate Test Plan**: Review and validate test strategy:

   - Ensure all code types have appropriate test coverage
   - Verify test frameworks are compatible with codebase
   - Check test data and mocking strategy is feasible
   - Validate CI/CD integration approach
   - Update test plan with any adjustments

7. **Log and Seek Approval**:
   - Log test analysis with timestamp in `.test-docs/audit.md`
   - Present test plan summary to user
   - Wait for explicit user approval before proceeding
   - Record approval response with timestamp
   - Update Phase 1 complete status in `.test-docs/test-state.md`
