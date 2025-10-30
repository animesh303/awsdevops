# AWS Technical Requirements Specification

## Document Information

- **Ticket Number**: AWS-2
- **Ticket Title**: I want to set up a AWS S3 website bucket with a sample hello world webpage hosted on it. Also I need to have a DynamoDb and a SQS Queue.
- **Created Date**: 2025-01-27
- **Last Updated**: 2025-01-27
- **Status**: Final

## 1. Functional Overview

This ticket aims to establish a foundational AWS infrastructure consisting of three core services: S3 static website hosting, DynamoDB for data storage, and SQS for message queuing. The implementation will include a sample hello world webpage hosted on S3 and follow AWS best practices for security, monitoring, and cost optimization.

## 2. AWS Services Required

### 2.1 Compute Services

- [ ] AWS Lambda (not required for this implementation)
- [ ] EC2 instances (not required)
- [ ] ECS/EKS (not required)
- [ ] Other compute services (none)

### 2.2 Storage Services

- [x] S3 buckets (for static website hosting)
- [x] DynamoDB tables (for NoSQL data storage)
- [ ] RDS instances (not required)
- [ ] EFS (not required)
- [ ] Other storage services (none)

### 2.3 API & Networking

- [ ] API Gateway (not required for static website)
- [ ] VPC configuration (default VPC acceptable)
- [ ] Load Balancers (not required)
- [x] CloudFront (recommended for S3 website distribution)
- [ ] Other networking services (none)

### 2.4 Security & Access

- [x] IAM roles and policies (for service access)
- [ ] Cognito (not required)
- [ ] Secrets Manager (not required for this scope)
- [x] KMS (for encryption at rest)
- [ ] Other security services (none)

### 2.5 Monitoring & Logging

- [x] CloudWatch (for monitoring and logging)
- [ ] X-Ray (not required)
- [ ] CloudTrail (not required)
- [ ] Other monitoring services (none)

## 3. Technical Specifications

### 3.1 Programming Language

- [ ] Python
- [ ] Node.js
- [ ] Java
- [ ] Go
- [x] Other: **HTML/CSS/JavaScript (for static webpage)**

### 3.2 Data Requirements

- **Data Input**: Static HTML content, potential form submissions or user interactions
- **Data Processing**: No server-side processing required for static website
- **Data Output**: HTML webpage served via S3, data stored in DynamoDB
- **Data Volume**: Minimal - single webpage, low traffic expected

### 3.3 API Requirements

- **Endpoints**: No API endpoints required for static website
- **Authentication**: Public read access for S3 website
- **Rate Limiting**: Default S3 limits acceptable
- **Response Format**: HTML for webpage content

## 4. Infrastructure Requirements

### 4.1 Environment Configuration

- **Development Environment**: Single environment acceptable for this scope
- **Staging Environment**: Not required for initial implementation
- **Production Environment**: Single production deployment

### 4.2 Resource Sizing

- **Lambda Memory**: Not applicable
- **Lambda Timeout**: Not applicable
- **Database Capacity**: DynamoDB on-demand pricing for minimal usage
- **Network Bandwidth**: Standard S3 bandwidth limits

### 4.3 High Availability

- **Multi-AZ Deployment**: S3 provides built-in redundancy
- **Backup Strategy**: S3 versioning enabled, DynamoDB point-in-time recovery
- **Disaster Recovery**: Cross-region replication not required for initial scope

## 5. Acceptance Criteria

### 5.1 Functional Requirements

- [x] S3 bucket configured for static website hosting
- [x] Hello world webpage accessible via S3 website URL
- [x] DynamoDB table created and accessible
- [x] SQS queue created and functional
- [x] All resources follow AWS best practices

### 5.2 Non-Functional Requirements

- [x] S3 bucket has appropriate security policies (public read for website)
- [x] DynamoDB table has encryption at rest enabled
- [x] SQS queue has appropriate access policies
- [x] CloudWatch monitoring enabled for all services
- [x] Cost optimization through appropriate service configurations

## 6. Dependencies

- **Other JIRA Tickets**: None
- **External Services**: None
- **Team Dependencies**: None

## 7. Implementation Notes

- **Terraform Modules**: Use standard AWS provider modules for S3, DynamoDB, and SQS
- **Code Structure**: 
  - `iac/terraform/` - Infrastructure as Code
  - `src/website/` - Static website files
- **Testing Strategy**: 
  - Terraform plan/apply validation
  - Website accessibility testing
  - Service connectivity testing
- **Deployment Strategy**: Single-step Terraform deployment

## 8. Detailed Technical Specifications

### 8.1 S3 Static Website Configuration

- **Bucket Name**: Unique bucket name with website hosting enabled
- **Index Document**: index.html
- **Error Document**: error.html
- **Public Access**: Enabled for website hosting
- **Versioning**: Enabled for content management
- **Encryption**: Server-side encryption with S3 managed keys

### 8.2 DynamoDB Table Configuration

- **Table Name**: sample-data-table
- **Partition Key**: id (String)
- **Billing Mode**: On-demand
- **Encryption**: Enabled with AWS managed keys
- **Point-in-time Recovery**: Enabled

### 8.3 SQS Queue Configuration

- **Queue Name**: sample-message-queue
- **Queue Type**: Standard queue
- **Message Retention**: 14 days (default)
- **Visibility Timeout**: 30 seconds
- **Encryption**: Enabled with SQS managed keys

### 8.4 Security Best Practices

- **S3 Bucket Policy**: Allow public read access only for website content
- **IAM Roles**: Least privilege access for any service interactions
- **Encryption**: All services configured with encryption at rest
- **Access Logging**: S3 access logging enabled