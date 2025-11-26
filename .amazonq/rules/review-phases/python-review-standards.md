# Python Code Review Standards

## Code Quality Standards

### Readability

- **Naming Conventions**: Follow PEP 8 naming conventions
  - Functions: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`
  - Private: `_leading_underscore`
- **Line Length**: Maximum 88 characters (Black default) or 79 characters (PEP 8)
- **Imports**: Organize imports (stdlib, third-party, local) with blank lines
- **Docstrings**: Use docstrings for all functions, classes, and modules (Google or NumPy style)

### Code Structure

- **Functions**: Single responsibility, maximum 50 lines
- **Classes**: Cohesive, focused responsibility
- **Modules**: Logical organization, clear module purpose
- **DRY Principle**: Don't repeat yourself, extract common logic

### Best Practices

- **Type Hints**: Use type hints for function parameters and return types
- **Error Handling**: Use specific exceptions, not bare `except`
- **Resource Management**: Use context managers (`with` statements)
- **List Comprehensions**: Prefer comprehensions over loops when readable
- **Generator Expressions**: Use generators for large datasets

## Security Standards

### Input Validation

- **Validate All Inputs**: Never trust user input
- **Sanitize Inputs**: Sanitize inputs before processing
- **Type Checking**: Validate types, not just values
- **Boundary Checking**: Check bounds and limits

### Secret Management

- **No Hardcoded Secrets**: Never commit secrets to code
- **Environment Variables**: Use environment variables for secrets
- **AWS Secrets Manager**: Use AWS Secrets Manager for production secrets
- **Secret Rotation**: Implement secret rotation

### Security Vulnerabilities

- **SQL Injection**: Use parameterized queries, never string concatenation
- **XSS**: Sanitize user inputs, use template escaping
- **CSRF**: Use CSRF tokens for forms
- **Authentication**: Implement proper authentication and authorization

## Performance Standards

### Efficiency

- **Algorithm Complexity**: Choose appropriate algorithms (O(n) vs O(n²))
- **Database Queries**: Optimize queries, use indexes, avoid N+1 queries
- **Caching**: Use caching for expensive operations
- **Lazy Loading**: Use lazy loading for large datasets

### Resource Usage

- **Memory**: Avoid memory leaks, use generators for large datasets
- **CPU**: Optimize CPU-intensive operations
- **I/O**: Minimize I/O operations, use async I/O when appropriate

## AWS Best Practices

### Service Usage

- **Appropriate Services**: Use appropriate AWS services for use case
- **Service Configuration**: Configure services according to best practices
- **Cost Optimization**: Use cost-effective services and configurations

### Security

- **IAM**: Use least privilege IAM policies
- **Encryption**: Enable encryption at rest and in transit
- **VPC**: Use VPC for network isolation
- **CloudWatch**: Enable logging and monitoring

## Testing Standards

### Test Coverage

- **Minimum Coverage**: 80% code coverage
- **Critical Paths**: 100% coverage for critical business logic
- **Test Types**: Unit, integration, and E2E tests

### Test Quality

- **Test Structure**: Arrange-Act-Assert pattern
- **Test Names**: Descriptive test names
- **Test Independence**: Tests should be independent
- **Mocking**: Mock external dependencies

## Documentation Standards

### Code Comments

- **Docstrings**: Use docstrings for all public functions, classes, modules
- **Inline Comments**: Use comments to explain "why", not "what"
- **TODO Comments**: Track TODOs and technical debt

### API Documentation

- **API Docs**: Document all public APIs
- **Examples**: Include usage examples
- **Parameters**: Document all parameters and return values

## Common Issues to Check

### Code Smells

- **Long Functions**: Functions longer than 50 lines
- **Complex Functions**: High cyclomatic complexity
- **Code Duplication**: Repeated code blocks
- **Magic Numbers**: Unnamed constants

### Anti-patterns

- **God Objects**: Classes with too many responsibilities
- **Spaghetti Code**: Unclear control flow
- **Premature Optimization**: Optimizing before profiling
- **Over-engineering**: Unnecessary complexity

## Review Checklist

- [ ] Code follows PEP 8 style guide
- [ ] Functions have type hints
- [ ] All functions have docstrings
- [ ] No hardcoded secrets
- [ ] Input validation implemented
- [ ] Error handling is proper
- [ ] Tests have adequate coverage
- [ ] Code is readable and maintainable
- [ ] AWS best practices followed
- [ ] Security best practices followed
