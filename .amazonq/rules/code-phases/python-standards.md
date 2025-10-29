# Python Coding Standards

## File Organization

- **lambda_handler.py**: Main Lambda function entry point
- **requirements.txt**: Python dependencies
- **utils/**: Utility functions and helpers
- **tests/**: Unit tests using pytest

## Code Style

- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Use descriptive variable and function names
- Keep functions small and focused (single responsibility)
- Use docstrings for all functions and classes

## Security Best Practices

- Validate and sanitize all inputs
- Use environment variables for configuration
- Implement proper error handling and logging
- Use AWS Secrets Manager for sensitive data
- Follow OWASP guidelines for Python

## Error Handling

- Use specific exception types
- Log errors with appropriate levels
- Return meaningful error messages
- Implement retry logic for transient failures
- Use structured logging (JSON format)

## Testing Standards

- Write unit tests for all functions
- Aim for 80%+ code coverage
- Use pytest fixtures for test data
- Mock external dependencies
- Test both success and failure scenarios

## Changelog Requirements

- **MANDATORY**: Include changelog history at the top of each .py file as comments
- Format: `# Changelog: [JIRA-TICKET-NUMBER] - [Description] - [Date]`
- Include all changes made to the file with JIRA ticket references
- Example:
  ```python
  # Changelog:
  # AWS-123 - Initial Lambda function creation - 2024-01-15
  # AWS-124 - Added error handling and logging - 2024-01-16
  # AWS-125 - Updated input validation - 2024-01-17
  ```

## Example Structure

```python
# lambda_handler.py
# Changelog:
# AWS-123 - Initial Lambda function creation - 2024-01-15
# AWS-124 - Added error handling and logging - 2024-01-16

import json
import logging
from typing import Dict, Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda function handler.

    Args:
        event: Lambda event data
        context: Lambda context object

    Returns:
        Dict containing response data
    """
    try:
        # Process the event
        result = process_event(event)

        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except Exception as e:
        logger.error(f"Error processing event: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }

def process_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Process the incoming event."""
    # Implementation here
    pass
```

## Linting Configuration

- Use flake8 for style checking
- Use black for code formatting
- Use isort for import sorting
- Use mypy for type checking
