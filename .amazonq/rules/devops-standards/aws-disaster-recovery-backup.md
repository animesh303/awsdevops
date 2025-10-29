# AWS Disaster Recovery and Backup

## Purpose

Ensures robust disaster recovery and backup strategies for AWS applications and data to minimize downtime and data loss in case of failures.

## Instructions

- ALWAYS implement cross-region backup for critical data using AWS Backup (ID: CROSS_REGION_BACKUP)
- ALWAYS use AWS Backup for centralized backup management and policy enforcement (ID: USE_AWS_BACKUP)
- ALWAYS implement proper RTO (Recovery Time Objective) and RPO (Recovery Point Objective) based on business requirements (ID: RTO_RPO_DEFINITION)
- ALWAYS use AWS DRS (Disaster Recovery Service) for EC2 instance replication (ID: USE_AWS_DRS)
- ALWAYS implement proper backup encryption using AWS KMS (ID: BACKUP_ENCRYPTION)
- ALWAYS use AWS S3 Cross-Region Replication for critical data redundancy (ID: S3_CRR)
- ALWAYS implement proper backup testing and recovery procedures (ID: BACKUP_TESTING)
- ALWAYS use AWS RDS automated backups with point-in-time recovery (ID: RDS_BACKUP)
- ALWAYS implement proper DynamoDB global tables for multi-region replication (ID: DYNAMODB_GLOBAL_TABLES)
- ALWAYS use Terraform workspaces or modules for multi-region infrastructure deployment (ID: TERRAFORM_MULTI_REGION)
- ALWAYS implement proper backup retention policies based on compliance requirements (ID: BACKUP_RETENTION)
- ALWAYS use AWS Route 53 health checks for failover routing (ID: ROUTE53_HEALTH_CHECKS)
- ALWAYS implement proper disaster recovery runbooks and procedures (ID: DR_RUNBOOKS)
- ALWAYS use AWS CloudEndure for application-level disaster recovery (ID: USE_CLOUDENDURE)
- ALWAYS implement proper backup monitoring and alerting (ID: BACKUP_MONITORING)
- ALWAYS use AWS S3 versioning and MFA delete for critical data protection (ID: S3_VERSIONING)
- ALWAYS implement proper database backup strategies for different database types (ID: DATABASE_BACKUP_STRATEGIES)
- ALWAYS use AWS Backup Vault for secure backup storage (ID: USE_BACKUP_VAULT)
- ALWAYS implement proper disaster recovery testing schedules and procedures (ID: DR_TESTING_SCHEDULE)
- ALWAYS use Terraform for infrastructure as code disaster recovery (ID: TERRAFORM_DR)
- ALWAYS implement proper backup compliance and audit logging (ID: BACKUP_COMPLIANCE)
- ALWAYS use AWS S3 Glacier for long-term backup storage (ID: S3_GLACIER)
- ALWAYS implement proper disaster recovery communication and notification procedures (ID: DR_COMMUNICATION)
- ALWAYS use AWS Backup with proper IAM roles and permissions (ID: BACKUP_IAM)
- ALWAYS implement proper disaster recovery cost optimization strategies (ID: DR_COST_OPTIMIZATION)

## Priority

High

## Error Handling

- If cross-region backup is not feasible, implement alternative redundancy strategies and document the risk
- If AWS Backup is not available, use alternative backup solutions but maintain AWS integration
- If RTO/RPO requirements cannot be met, document the limitation and implement the best possible solution
- If disaster recovery testing cannot be performed, implement alternative validation methods
- If backup encryption is not possible, implement additional security controls and document the risk
