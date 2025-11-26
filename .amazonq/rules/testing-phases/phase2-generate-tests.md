# Phase 2: Generate Tests

**Assume the role** of a senior test engineer and test automation specialist

**Universal Phase**: Works with any codebase to generate comprehensive test suites

1. **Review Test Plan**: Understand testing requirements:

   - Read test plan from `.test-docs/test-plan.md`
   - Read codebase analysis from `.test-docs/codebase-analysis.md`
   - Read test requirements from `.test-docs/test-requirements.md`
   - Understand test strategy and coverage targets

2. **Set Up Test Infrastructure**: Create test framework configuration:

   - **Python**: Create `pytest.ini` or `setup.cfg` with pytest configuration
   - **TypeScript/JavaScript**: Create `jest.config.js` or `vitest.config.ts`
   - **Java**: Configure `pom.xml` or `build.gradle` with test dependencies
   - **Go**: Ensure test package structure follows Go conventions
   - **Terraform**: Set up Terratest or Kitchen-Terraform configuration
   - Store configurations in appropriate locations

3. **Generate Unit Tests**: Create unit tests for all identified units:

   - **Read language testing standards**: Load standards from `testing-phases/{language}-testing-standards.mdc`
     - Extract language name from code type: `python` → `python-testing-standards.mdc`
     - Examples: `python-testing-standards.mdc`, `nodejs-testing-standards.mdc`, `java-testing-standards.mdc`
   - **For each function/class/module**:
     - Create test file following naming convention: `test_{module_name}.py` (Python) or `{module_name}.test.ts` (TypeScript)
     - Write test cases for:
       - Happy path scenarios
       - Edge cases and boundary conditions
       - Error handling and exception cases
       - Input validation
   - **Test Structure**:
     - Arrange-Act-Assert (AAA) pattern
     - Descriptive test names
     - Proper setup and teardown
     - Mock external dependencies
   - Store unit tests in `tests/unit/{feature-name}/` directory

4. **Generate Integration Tests**: Create integration tests for service interactions:

   - **For each service/API endpoint**:
     - Create integration test file
     - Test service-to-service communication
     - Test database operations
     - Test external API integrations (with mocks)
   - **Test Structure**:
     - Test real service interactions
     - Use test databases or containers
     - Verify data flow and transformations
     - Test error scenarios
   - Store integration tests in `tests/integration/{feature-name}/` directory

5. **Generate E2E Tests**: Create end-to-end tests for complete workflows:

   - **For each user workflow**:
     - Create E2E test file
     - Test complete user journeys
     - Test system interactions end-to-end
     - Verify business logic flows
   - **Test Structure**:
     - Test complete workflows
     - Use realistic test data
     - Verify system state changes
     - Test error recovery
   - Store E2E tests in `tests/e2e/{feature-name}/` directory

6. **Generate Performance Tests** (if applicable): Create performance tests:

   - **For performance-critical components**:
     - Create load tests
     - Create stress tests
     - Create benchmark tests
   - Store performance tests in `tests/performance/{feature-name}/` directory

7. **Generate Test Utilities**: Create reusable test utilities:

   - Test fixtures and factories
   - Mock helpers and utilities
   - Test data generators
   - Common test setup/teardown utilities
   - Store utilities in `tests/utils/` or `tests/fixtures/` directory

8. **Apply Testing Best Practices**: Ensure tests follow best practices:

   - **Test Quality**:
     - Tests are independent and isolated
     - Tests are deterministic (no flaky tests)
     - Tests have clear, descriptive names
     - Tests follow AAA pattern
   - **Coverage**:
     - Aim for minimum 80% code coverage
     - Focus on critical paths and business logic
     - Don't test implementation details unnecessarily
   - **Maintainability**:
     - Tests are readable and well-documented
     - Tests follow DRY principle (use fixtures/utilities)
     - Tests are organized logically

9. **Validate Generated Tests**: Run basic validation:

   - Check test file syntax (language-specific)
   - Verify test imports and dependencies
   - Ensure test framework configuration is correct
   - Store validation results in `.test-docs/test-generation-validation.md`

10. **Log and Seek Approval**:
    - Log test generation with timestamp in `.test-docs/audit.md`
    - Present summary of generated tests to user
    - Wait for explicit user approval before proceeding
    - Record approval response with timestamp
    - Update Phase 2 complete status in `.test-docs/test-state.md`
