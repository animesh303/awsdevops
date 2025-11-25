# Python Testing Standards

## Test Framework

- **Primary Framework**: pytest
- **Coverage Tool**: pytest-cov
- **Mocking**: unittest.mock or pytest-mock
- **Fixtures**: pytest fixtures

## Test Structure

### File Organization

```
tests/
├── unit/
│   └── {feature-name}/
│       └── test_{module_name}.py
├── integration/
│   └── {feature-name}/
│       └── test_{service}_integration.py
├── e2e/
│   └── {feature-name}/
│       └── test_{workflow}_e2e.py
└── fixtures/
    └── {feature-name}/
        └── conftest.py
```

### Naming Conventions

- Test files: `test_{module_name}.py`
- Test functions: `test_{functionality}_should_{expected_behavior}`
- Test classes: `Test{ClassName}`
- Fixtures: `{resource}_fixture` or `{resource}_mock`

## Test Patterns

### Unit Test Pattern

```python
import pytest
from unittest.mock import Mock, patch
from src.module import function

def test_function_should_return_expected_result():
    # Arrange
    input_data = {"key": "value"}
    expected_output = {"result": "success"}
    
    # Act
    result = function(input_data)
    
    # Assert
    assert result == expected_output
    assert result["result"] == "success"

def test_function_should_handle_error_case():
    # Arrange
    invalid_input = None
    
    # Act & Assert
    with pytest.raises(ValueError):
        function(invalid_input)
```

### Integration Test Pattern

```python
import pytest
from src.service import Service

@pytest.fixture
def test_service():
    return Service(test_config=True)

def test_service_should_process_data(test_service):
    # Arrange
    test_data = {"input": "data"}
    
    # Act
    result = test_service.process(test_data)
    
    # Assert
    assert result.status == "success"
    assert result.data is not None
```

### E2E Test Pattern

```python
import pytest
from tests.utils.e2e_setup import setup_test_environment

@pytest.fixture(scope="module")
def e2e_env():
    env = setup_test_environment()
    yield env
    env.cleanup()

def test_complete_workflow_should_succeed(e2e_env):
    # Arrange
    workflow = e2e_env.create_workflow()
    
    # Act
    result = workflow.execute()
    
    # Assert
    assert result.completed
    assert result.final_state == "success"
```

## Best Practices

### Test Quality

- **AAA Pattern**: Always use Arrange-Act-Assert structure
- **Descriptive Names**: Test names should clearly describe what is being tested
- **One Assertion**: Prefer one assertion per test (when possible)
- **Independence**: Tests should be independent and runnable in any order
- **Deterministic**: Tests should produce consistent results

### Coverage

- **Target**: Minimum 80% code coverage
- **Critical Paths**: 100% coverage for critical business logic
- **Error Handling**: Test all error paths and edge cases
- **Boundary Conditions**: Test boundary values and limits

### Mocking

- **External Dependencies**: Mock external services, APIs, databases
- **Isolation**: Unit tests should not depend on external systems
- **Realistic Mocks**: Mocks should behave like real dependencies
- **Fixture Reuse**: Use pytest fixtures for common test setup

### Performance

- **Fast Execution**: Unit tests should run in milliseconds
- **Parallel Execution**: Use pytest-xdist for parallel test execution
- **Test Data**: Use minimal test data for unit tests
- **Cleanup**: Properly clean up test resources

## Configuration

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --cov=src
    --cov-report=html
    --cov-report=term
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
```

### requirements-test.txt

```
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0
pytest-xdist>=3.3.0
```

## CI/CD Integration

- Run unit tests on every push/PR
- Run integration tests on PR merge
- Run E2E tests on release
- Publish coverage reports
- Fail build if coverage below 80%
