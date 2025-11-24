# Phase 2: Review Code

**Assume the role** of a senior code reviewer and security specialist

**Universal Phase**: Works with any codebase to conduct comprehensive review

1. **Review Code Quality**: Analyze code structure and quality:

   - **Readability**:
     - Code clarity and naming conventions
     - Code organization and structure
     - Comments and documentation
   - **Maintainability**:
     - Code complexity (cyclomatic complexity)
     - Code duplication
     - Code organization and modularity
   - **Best Practices**:
     - Language-specific patterns and idioms
     - Design patterns usage
     - Code style consistency
   - Store findings in `.review-docs/findings/code-quality-findings.md`

2. **Review Security**: Analyze security aspects:

   - **Vulnerabilities**:
     - SQL injection risks
     - XSS vulnerabilities
     - Authentication/authorization issues
     - Input validation issues
     - Secret management (API keys, passwords)
   - **Security Best Practices**:
     - Encryption usage
     - Secure communication (HTTPS, TLS)
     - Least privilege principles
     - Security logging and monitoring
   - **OWASP Compliance**: Check against OWASP Top 10
   - Store findings in `.review-docs/findings/security-findings.md`

3. **Review Performance**: Analyze performance implications:

   - **Efficiency**:
     - Algorithm efficiency
     - Database query optimization
     - API call optimization
     - Resource usage (memory, CPU)
   - **Optimization Opportunities**:
     - Caching opportunities
     - Lazy loading opportunities
     - Batch processing opportunities
   - **Scalability**: Consider scalability implications
   - Store findings in `.review-docs/findings/performance-findings.md`

4. **Review AWS Best Practices**: Check AWS-specific best practices:

   - **Service Usage**: Appropriate AWS service selection
   - **Resource Configuration**: Proper resource configuration
   - **Cost Optimization**: Cost-effective resource usage
   - **Security**: AWS security best practices (IAM, encryption, etc.)
   - **Monitoring**: CloudWatch, logging, metrics
   - **Infrastructure**: Terraform/CDK best practices
   - Store findings in `.review-docs/findings/aws-best-practices-findings.md`

5. **Review Testing**: Analyze test coverage and quality:

   - **Test Coverage**: Check if changes have adequate test coverage
   - **Test Quality**: Review test quality and best practices
   - **Test Organization**: Check test structure and organization
   - Store findings in `.review-docs/findings/testing-findings.md`

6. **Review Documentation**: Check documentation:

   - **Code Comments**: Inline code comments
   - **API Documentation**: API documentation completeness
   - **README**: README updates if needed
   - **Architecture Docs**: Architecture documentation
   - Store findings in `.review-docs/findings/documentation-findings.md`

7. **Run Automated Analysis**: Run automated code analysis tools:

   - **Linting**: Run language-specific linters
   - **Static Analysis**: Run static analysis tools
   - **Security Scanning**: Run security scanners
   - **Dependency Scanning**: Check for vulnerable dependencies
   - Store results in `.review-docs/automated-analysis-results.md`

8. **Categorize Findings**: Organize findings by severity:

   - **Critical**: Security vulnerabilities, breaking changes
   - **High**: Performance issues, major bugs
   - **Medium**: Code quality issues, best practices
   - **Low**: Minor improvements, suggestions
   - Store categorization in `.review-docs/findings-summary.md`

9. **Log and Seek Approval**:
   - Log code review with timestamp in `.review-docs/audit.md`
   - Present review findings summary to user
   - Wait for explicit user approval before proceeding
   - Record approval response with timestamp
   - Update Phase 2 complete status in `.review-docs/review-state.md`
