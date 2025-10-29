# AWS Programming Languages

## Purpose

Defines programming language standards and best practices for AWS development to ensure consistency, maintainability, and optimal performance.

## Instructions

- ALWAYS use Python as the primary language for AWS Lambda functions and data processing (ID: USE_PYTHON)
- ALWAYS use TypeScript for AWS CDK and complex frontend applications (ID: USE_TYPESCRIPT)
- ALWAYS use Node.js for serverless applications and API development (ID: USE_NODEJS)
- ALWAYS use Go for high-performance microservices and CLI tools (ID: USE_GO)
- ALWAYS use Java for enterprise applications and Spring Boot services (ID: USE_JAVA)
- ALWAYS use proper code formatting using Black for Python (ID: PYTHON_FORMATTING)
- ALWAYS use proper linting with flake8 or pylint for Python (ID: PYTHON_LINTING)
- ALWAYS use proper type hints with mypy for Python (ID: PYTHON_TYPE_HINTS)
- ALWAYS implement proper code formatting using Prettier for TypeScript/JavaScript (ID: CODE_FORMATTING)
- ALWAYS use proper linting with ESLint for TypeScript/JavaScript (ID: TYPESCRIPT_LINTING)
- ALWAYS use proper type checking with TypeScript strict mode (ID: TYPESCRIPT_STRICT)
- ALWAYS implement proper error handling and logging in all languages (ID: ERROR_HANDLING)
- ALWAYS use proper dependency management with package.json for Node.js (ID: NODEJS_DEPENDENCIES)
- ALWAYS use proper dependency management with requirements.txt for Python (ID: PYTHON_DEPENDENCIES)
- ALWAYS use proper dependency management with go.mod for Go (ID: GO_DEPENDENCIES)
- ALWAYS use proper dependency management with pom.xml for Java (ID: JAVA_DEPENDENCIES)
- ALWAYS implement proper unit testing for all code (ID: UNIT_TESTING)
- ALWAYS use proper integration testing for AWS services (ID: INTEGRATION_TESTING)
- ALWAYS implement proper code documentation and comments (ID: CODE_DOCUMENTATION)
- ALWAYS use proper version control with Git and semantic versioning (ID: VERSION_CONTROL)
- ALWAYS implement proper code review processes and guidelines (ID: CODE_REVIEW)
- ALWAYS use proper security scanning and vulnerability assessment (ID: SECURITY_SCANNING)
- ALWAYS implement proper performance optimization and profiling (ID: PERFORMANCE_OPTIMIZATION)
- ALWAYS use proper AWS SDK best practices for each language (ID: AWS_SDK_BEST_PRACTICES)
- ALWAYS implement proper environment-specific configuration management (ID: ENVIRONMENT_CONFIG)
- ALWAYS use proper logging and monitoring for all applications (ID: LOGGING_MONITORING)
- ALWAYS implement proper error handling and recovery mechanisms (ID: ERROR_RECOVERY)
- ALWAYS use proper code organization and modular design (ID: CODE_ORGANIZATION)

## Priority

Medium

## Error Handling

- If Python is not suitable, use Node.js or TypeScript with proper linting and type checking
- If Python is not available, use alternative languages but maintain AWS SDK compatibility
- If Node.js is not suitable, use alternative runtime environments with proper AWS integration
- If Go is not feasible, use alternative high-performance languages
- If Java is not suitable, use alternative enterprise languages with proper AWS support
