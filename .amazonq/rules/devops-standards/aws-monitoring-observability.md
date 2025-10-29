# AWS Monitoring and Observability

## Purpose

Ensures comprehensive monitoring, logging, and observability for AWS applications and infrastructure to enable proactive issue detection and resolution.

## Instructions

- ALWAYS implement CloudWatch metrics for all AWS resources and custom applications (ID: CLOUDWATCH_METRICS)
- ALWAYS set up CloudWatch alarms for critical metrics with appropriate thresholds (ID: CLOUDWATCH_ALARMS)
- ALWAYS use structured logging with JSON format and consistent log levels (ID: STRUCTURED_LOGGING)
- ALWAYS implement distributed tracing using AWS X-Ray for microservices (ID: XRAY_TRACING)
- ALWAYS create CloudWatch dashboards for key performance indicators (ID: CLOUDWATCH_DASHBOARDS)
- ALWAYS implement log aggregation using CloudWatch Logs with proper log groups (ID: LOG_AGGREGATION)
- ALWAYS set up SNS notifications for critical alerts with appropriate escalation (ID: SNS_NOTIFICATIONS)
- ALWAYS implement custom metrics for business-specific KPIs (ID: CUSTOM_METRICS)
- ALWAYS use CloudWatch Insights for log analysis and troubleshooting (ID: CLOUDWATCH_INSIGHTS)
- ALWAYS implement proper log retention policies based on compliance requirements (ID: LOG_RETENTION)
- ALWAYS use AWS CloudWatch Synthetics for synthetic monitoring (ID: SYNTHETIC_MONITORING)
- ALWAYS implement proper error tracking and alerting (ID: ERROR_TRACKING)
- ALWAYS use AWS CloudWatch Container Insights for containerized applications (ID: CONTAINER_INSIGHTS)
- ALWAYS implement proper performance monitoring for databases and storage (ID: PERFORMANCE_MONITORING)
- ALWAYS use AWS CloudWatch RUM for real user monitoring (ID: RUM_MONITORING)
- ALWAYS implement proper capacity monitoring and auto-scaling based on metrics (ID: CAPACITY_MONITORING)
- ALWAYS use AWS CloudWatch Lambda Insights for serverless monitoring (ID: LAMBDA_INSIGHTS)
- ALWAYS implement proper health checks and status endpoints (ID: HEALTH_CHECKS)
- ALWAYS use AWS CloudWatch Contributor Insights for log analysis (ID: CONTRIBUTOR_INSIGHTS)
- ALWAYS implement proper SLA monitoring and reporting (ID: SLA_MONITORING)
- ALWAYS use AWS CloudWatch Anomaly Detection for proactive monitoring (ID: ANOMALY_DETECTION)
- ALWAYS implement proper cost monitoring and budget alerts (ID: COST_MONITORING)
- ALWAYS use AWS CloudWatch ServiceLens for service topology visualization (ID: SERVICE_LENS)
- ALWAYS implement proper security monitoring and threat detection (ID: SECURITY_MONITORING)
- ALWAYS use AWS CloudWatch Logs Insights for advanced log analysis (ID: LOGS_INSIGHTS)

## Priority

High

## Error Handling

- If CloudWatch is not available, implement alternative monitoring solutions and document the approach
- If X-Ray tracing cannot be implemented, use alternative distributed tracing solutions
- If custom metrics are not feasible, focus on standard AWS metrics and document the limitation
- If log retention policies conflict with cost constraints, implement tiered retention and document the trade-off
- If monitoring tools are not available, implement basic logging and alerting and plan for future enhancement
