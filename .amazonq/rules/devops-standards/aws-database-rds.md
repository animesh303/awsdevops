# AWS Database and RDS

## Purpose

Defines best practices for AWS database services including RDS, DynamoDB, and other database solutions to ensure performance, security, and reliability.

## Instructions

- ALWAYS use AWS RDS for relational databases with proper instance sizing (ID: USE_RDS)
- ALWAYS implement proper database encryption at rest using AWS KMS (ID: DATABASE_ENCRYPTION)
- ALWAYS use proper database backup and point-in-time recovery (ID: DATABASE_BACKUP)
- ALWAYS implement proper database security groups and network access control (ID: DATABASE_SECURITY)
- ALWAYS use proper database parameter groups for optimization (ID: DATABASE_PARAMETER_GROUPS)
- ALWAYS implement proper database monitoring using CloudWatch (ID: DATABASE_MONITORING)
- ALWAYS use proper database read replicas for read-heavy workloads (ID: DATABASE_READ_REPLICAS)
- ALWAYS implement proper database connection pooling and management (ID: DATABASE_CONNECTION_POOLING)
- ALWAYS use proper database maintenance windows and updates (ID: DATABASE_MAINTENANCE)
- ALWAYS implement proper database performance insights and optimization (ID: DATABASE_PERFORMANCE)
- ALWAYS use proper database multi-AZ deployment for high availability (ID: DATABASE_MULTI_AZ)
- ALWAYS implement proper database security scanning and vulnerability assessment (ID: DATABASE_SECURITY_SCANNING)
- ALWAYS use proper database cost optimization and right-sizing (ID: DATABASE_COST_OPTIMIZATION)
- ALWAYS implement proper database compliance and audit logging (ID: DATABASE_COMPLIANCE)
- ALWAYS use proper database migration strategies and tools (ID: DATABASE_MIGRATION)
- ALWAYS implement proper database disaster recovery and failover procedures (ID: DATABASE_DR)
- ALWAYS use proper database scaling and auto-scaling configuration (ID: DATABASE_SCALING)
- ALWAYS implement proper database security best practices (ID: DATABASE_SECURITY_BEST_PRACTICES)
- ALWAYS use proper database networking and VPC configuration (ID: DATABASE_NETWORKING)
- ALWAYS implement proper database monitoring and alerting (ID: DATABASE_ALERTING)
- ALWAYS use proper database backup and recovery testing (ID: DATABASE_BACKUP_TESTING)
- ALWAYS implement proper database performance tuning and optimization (ID: DATABASE_PERFORMANCE_TUNING)
- ALWAYS use proper database security and access control (ID: DATABASE_ACCESS_CONTROL)
- ALWAYS implement proper database compliance and governance (ID: DATABASE_GOVERNANCE)
- ALWAYS use proper database monitoring and observability (ID: DATABASE_OBSERVABILITY)

## Priority

High

## Error Handling

- If RDS is not suitable, use alternative database solutions but maintain AWS integration
- If database encryption cannot be implemented, document the security risk and implement alternative controls
- If database backup cannot be implemented, implement alternative data protection strategies
- If database monitoring tools are not available, implement basic logging and plan for enhancement
- If database security scanning is not feasible, implement alternative security measures
