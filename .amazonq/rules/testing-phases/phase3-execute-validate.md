# Phase 3: Execute & Validate

**Assume the role** of a senior test engineer and quality assurance specialist

**Universal Phase**: Works with any test suite to execute and validate test quality

1. **Review Test Suite**: Understand what tests are available:

   - Read test plan from `.test-docs/test-plan.md`
   - Review generated test files in `tests/` directory
   - Understand test structure and organization
   - Identify test execution order and dependencies

2. **Set Up Test Environment**: Prepare environment for test execution:

   - **Install Test Dependencies**:
     - Python: `pip install -r requirements-test.txt` or `pip install pytest pytest-cov`
     - TypeScript/JavaScript: `npm install` or `yarn install`
     - Java: `mvn test-compile` or `./gradlew testClasses`
     - Go: `go mod download`
   - **Configure Test Environment**:
     - Set up test databases or containers
     - Configure environment variables for testing
     - Set up test data fixtures
     - Configure test infrastructure (if needed)

3. **Execute Unit Tests**: Run unit test suite:

   - **Python**: `pytest tests/unit/ -v --cov=src --cov-report=html`
   - **TypeScript/JavaScript**: `npm test` or `jest tests/unit`
   - **Java**: `mvn test` or `./gradlew test`
   - **Go**: `go test ./tests/unit/... -v -cover`
   - Capture test execution output
   - Store results in `.test-docs/test-results/unit-test-results.txt`
   - Store coverage reports in `.test-docs/coverage-reports/unit-coverage.html`

4. **Execute Integration Tests**: Run integration test suite:

   - **Python**: `pytest tests/integration/ -v`
   - **TypeScript/JavaScript**: `npm run test:integration` or `jest tests/integration`
   - **Java**: `mvn verify -Dtest=*IntegrationTest`
   - **Go**: `go test ./tests/integration/... -v`
   - Ensure test services/infrastructure are running
   - Capture test execution output
   - Store results in `.test-docs/test-results/integration-test-results.txt`

5. **Execute E2E Tests**: Run end-to-end test suite:

   - **Python**: `pytest tests/e2e/ -v`
   - **TypeScript/JavaScript**: `npm run test:e2e` or `jest tests/e2e`
   - **Java**: `mvn verify -Dtest=*E2ETest`
   - **Go**: `go test ./tests/e2e/... -v`
   - Ensure full system is deployed and running
   - Capture test execution output
   - Store results in `.test-docs/test-results/e2e-test-results.txt`

6. **Execute Performance Tests** (if applicable): Run performance test suite:

   - Execute load tests and stress tests
   - Capture performance metrics (response time, throughput, resource usage)
   - Store results in `.test-docs/test-results/performance-test-results.txt`

7. **Generate Coverage Reports**: Create comprehensive coverage reports:

   - **Python**: `pytest --cov=src --cov-report=html --cov-report=term`
   - **TypeScript/JavaScript**: `jest --coverage`
   - **Java**: `mvn jacoco:report`
   - **Go**: `go test -coverprofile=coverage.out && go tool cover -html=coverage.out`
   - Generate HTML coverage reports
   - Generate coverage summary (percentage by file/module)
   - Store reports in `.test-docs/coverage-reports/`
   - Store summary in `.test-docs/coverage-summary.md`

8. **Analyze Test Results**: Review test execution results:

   - **Test Pass Rate**: Calculate pass/fail ratio
   - **Coverage Analysis**: Analyze code coverage by module/file
   - **Failed Tests**: Identify and document failing tests
   - **Flaky Tests**: Identify any non-deterministic tests
   - **Performance Metrics**: Analyze performance test results
   - **Use GitHub MCP Server**: Post test results to GitHub (if PR context):
     - Post test summary as PR comment via `github-mcp-server`
     - Upload coverage reports as PR artifacts
     - Update PR status based on test results
   - Store analysis in `.test-docs/test-analysis.md`

9. **Validate Test Quality**: Ensure tests meet quality standards:

   - **Coverage Target**: Verify minimum 80% code coverage achieved
   - **Test Reliability**: Ensure no flaky tests
   - **Test Performance**: Ensure tests run in reasonable time
   - **Test Maintainability**: Review test code quality
   - Store quality validation in `.test-docs/test-quality-validation.md`

10. **Generate Test Report**: Create comprehensive test report:

    - **Executive Summary**: High-level test results and coverage
    - **Detailed Results**: Test execution results by category
    - **Coverage Report**: Code coverage analysis
    - **Quality Metrics**: Test quality assessment
    - **Recommendations**: Suggestions for improvement
    - Store report in `.test-docs/test-report.md`

11. **Log and Seek Approval**:
    - Log test execution with timestamp in `.test-docs/audit.md`
    - Present test results and coverage summary to user
    - Wait for explicit user approval before proceeding
    - Record approval response with timestamp
    - Update Phase 3 complete status in `.test-docs/test-state.md`
