# AWS Security and Compliance

## Purpose

Ensures all AWS resources and applications follow security best practices, compliance requirements, and data protection standards.

## Instructions

- ALWAYS encrypt data at rest using AWS KMS with customer-managed keys (ID: ENCRYPT_AT_REST)
- ALWAYS encrypt data in transit using TLS 1.2 or higher (ID: ENCRYPT_IN_TRANSIT)
- ALWAYS implement least privilege access using IAM roles and policies (ID: LEAST_PRIVILEGE_ACCESS)
- ALWAYS use IAM roles instead of access keys for AWS service access (ID: USE_IAM_ROLES)
- ALWAYS enable CloudTrail logging for all AWS API calls (ID: ENABLE_CLOUDTRAIL)
- ALWAYS enable VPC Flow Logs for network monitoring (ID: ENABLE_VPC_FLOW_LOGS)
- ALWAYS implement proper network segmentation using VPCs, subnets, and security groups (ID: NETWORK_SEGMENTATION)
- ALWAYS use AWS Secrets Manager or Parameter Store for sensitive configuration (ID: USE_SECRETS_MANAGER)
- ALWAYS enable AWS Config for resource compliance monitoring (ID: ENABLE_AWS_CONFIG)
- ALWAYS implement proper backup and recovery procedures with encryption (ID: SECURE_BACKUP)
- ALWAYS use AWS WAF for web application protection (ID: USE_AWS_WAF)
- ALWAYS enable AWS GuardDuty for threat detection (ID: ENABLE_GUARDDUTY)
- ALWAYS implement proper logging and monitoring for security events (ID: SECURITY_LOGGING)
- ALWAYS use AWS Certificate Manager for SSL/TLS certificates (ID: USE_ACM)
- ALWAYS implement proper input validation and sanitization (ID: INPUT_VALIDATION)
- ALWAYS use AWS IAM Identity Center for centralized identity management (ID: USE_IAM_IDENTITY_CENTER)
- ALWAYS implement proper session management and timeout policies (ID: SESSION_MANAGEMENT)
- ALWAYS use AWS KMS for key management with proper rotation policies (ID: KMS_KEY_ROTATION)
- ALWAYS implement proper error handling without exposing sensitive information (ID: SECURE_ERROR_HANDLING)
- ALWAYS use AWS Security Hub for centralized security findings (ID: USE_SECURITY_HUB)
- ALWAYS implement proper data classification and handling procedures (ID: DATA_CLASSIFICATION)
- ALWAYS use AWS CloudHSM for high-security key management when required (ID: USE_CLOUDHSM)
- ALWAYS implement proper vulnerability scanning and patch management (ID: VULNERABILITY_MANAGEMENT)
- ALWAYS use AWS Shield for DDoS protection (ID: USE_AWS_SHIELD)
- ALWAYS implement proper audit logging for compliance requirements (ID: AUDIT_LOGGING)

## Priority

Critical

## Error Handling

- If encryption cannot be enabled, document the security risk and get explicit approval
- If least privilege cannot be implemented, document the business justification and implement compensating controls
- If compliance requirements conflict, prioritize based on regulatory requirements and document the decision
- If security tools are not available, implement alternative security measures and document the gap
- If sensitive data must be stored unencrypted, implement additional security controls and get approval
