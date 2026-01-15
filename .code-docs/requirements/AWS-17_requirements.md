# Technical Requirements Specification

## Document Information

- **Ticket Number**: AWS-17
- **Ticket Title**: S3 bucket notification demo
- **Created Date**: 2026-01-15
- **Last Updated**: 2025-01-28
- **Status**: To Do

## 1. Project Overview

**Business Objective**: Demonstrate AWS S3 event-driven architecture by implementing a simple notification system that triggers Lambda function execution when files are uploaded to an S3 bucket.

**Solution Summary**: Create an S3 bucket configured with event notifications that automatically triggers an AWS Lambda function whenever any file is uploaded. The Lambda function will execute a simple "hello world" operation and log the event details.

**Scope**: 
- **Included**: S3 bucket creation, Lambda function implementation, event notification configuration, IAM roles and permissions, CloudWatch logging
- **Excluded**: Complex file processing logic, multiple Lambda functions, advanced event filtering, cross-region replication, file type validation

## 2. Functional Requirements

### 2.1 Core Functionality

- **FR-1**: S3 bucket must accept file uploads of any extension without restrictions
- **FR-2**: S3 bucket must trigger Lambda function automatically on any object creation event (s3:ObjectCreated:*)
- **FR-3**: Lambda function must execute successfully and log "Hello World" message along with event details
- **FR-4**: Lambda execution logs must be visible in CloudWatch Logs

### 2.2 User Interactions

- **UI-1**: User uploads file to S3 bucket via AWS Console, CLI, or SDK
- **API-1**: S3 invokes Lambda function synchronously via event notification
- **Data-1**: Lambda receives S3 event payload containing bucket name, object key, and event metadata

### 2.3 Data Requirements

**Data Input**: Files of any type/extension uploaded to S3 bucket

**Data Processing**: Lambda function receives S3 event notification payload and logs event details

**Data Output**: CloudWatch Logs containing Lambda execution logs with "Hello World" message and S3 event details

**Data Volume**: Demo/proof-of-concept - expected low volume (< 100 files per day)

## 3. Non-Functional Requirements

### 3.1 Performance

- **Response Time**: Lambda function should execute within 3 seconds of file upload
- **Throughput**: Support at least 10 concurrent file uploads
- **Scalability**: Lambda auto-scales based on S3 event volume

### 3.2 Security

- **Authentication**: AWS IAM-based authentication for all services
- **Authorization**: Least privilege IAM policies - Lambda execution role with minimal S3 read permissions
- **Data Protection**: S3 bucket encryption at rest (AES-256), HTTPS for data in transit
- **Audit**: CloudWatch Logs for Lambda execution, CloudTrail for S3 API calls

### 3.3 Reliability

- **Availability**: 99.9% availability (leveraging AWS managed services SLA)
- **Disaster Recovery**: Not required for demo (single region deployment)
- **Backup**: Not required for demo

### 3.4 Operational

- **Monitoring**: CloudWatch Logs for Lambda execution, CloudWatch Metrics for invocation count and errors
- **Logging**: Lambda logs all invocations with timestamp, event details, and execution status
- **Alerting**: CloudWatch Alarm for Lambda errors (threshold: > 5 errors in 5 minutes)

## 4. Technical Specifications

### 4.1 Architecture

**Architecture Approach**: Event-driven serverless architecture using AWS managed services

**Architecture Diagram**: Visual representation of the AWS architecture:

![Architecture Diagram](./AWS-17-architecture-diagram.png)

**Figure 1: AWS Architecture Diagram**

**Technology Stack**:
- **Programming Language**: Python 3.12
- **Framework**: AWS Lambda runtime
- **Infrastructure as Code**: Terraform

### 4.2 AWS Services

- **Compute**: AWS Lambda (Python 3.12 runtime)
- **Storage**: Amazon S3 (standard storage class)
- **Security**: IAM (roles and policies), AWS KMS (S3 encryption)
- **Monitoring**: CloudWatch Logs, CloudWatch Metrics, CloudWatch Alarms

### 4.3 Integration Points

**External Systems**: None

**API Contracts**: 
- S3 Event Notification → Lambda (AWS-managed integration)
- Event payload format: S3 Event Notification JSON schema

**Data Formats**: JSON (S3 event notification payload)

### 4.4 Environment Requirements

- **Environments**: Single environment (development/demo)
- **Deployment**: Terraform for infrastructure provisioning, AWS CLI/Console for testing

## 5. Acceptance Criteria

### 5.1 Functional Acceptance

- [x] S3 bucket created with event notifications enabled
- [x] Lambda function created with hello world code
- [x] S3 event notification configured to trigger Lambda on object creation
- [x] IAM role created with Lambda execution permissions and S3 event invocation permissions
- [x] Test: Upload file to S3 successfully triggers Lambda
- [x] Lambda execution logs visible in CloudWatch with "Hello World" message

### 5.2 Non-Functional Acceptance

- [x] Lambda executes within 3 seconds of file upload
- [x] S3 bucket encryption enabled
- [x] CloudWatch Logs configured for Lambda
- [x] CloudWatch Alarm configured for Lambda errors
- [x] Infrastructure deployed via Terraform

## 6. Dependencies

### 6.1 Technical Dependencies

- **Other JIRA Tickets**: None
- **External Services**: None
- **Infrastructure**: AWS account with permissions to create S3, Lambda, IAM, CloudWatch resources

### 6.2 Team Dependencies

- **Other Teams**: None
- **Coordination**: None

## 7. Assumptions

> **IMPORTANT**: This section should be **EMPTY** during initial requirements generation. No assumptions should be made. If information is missing or ambiguous, add it as a question in the "Open Questions" section using `[Answer]:` tags.

- AWS region: us-east-1 (default region for demo)
- Lambda runtime: Python 3.12 (latest stable version)
- S3 bucket naming: s3-lambda-trigger-demo-{random-suffix}
- Lambda function naming: s3-lambda-trigger-hello-world

## 8. Risks

- **RISK-1**: S3 event notification delivery delays during high load
  - **Impact**: Low (demo environment with low volume)
  - **Mitigation**: Monitor CloudWatch metrics for Lambda invocation delays

- **RISK-2**: Lambda cold start latency on first invocation
  - **Impact**: Low (acceptable for demo)
  - **Mitigation**: Document expected cold start behavior

- **RISK-3**: IAM permission misconfigurations preventing Lambda invocation
  - **Impact**: Medium (blocks functionality)
  - **Mitigation**: Use AWS-managed policies where possible, test permissions after deployment

## 9. Open Questions

> **CRITICAL**: This section is **MANDATORY** for identifying ambiguities. All missing or unclear information must be documented here using the format shown below. Requirements approval should not proceed until all blocking questions have `[Answer]:` filled in.

1. What AWS region should be used for deployment?
   [Answer]: us-east-1 (default region)

2. What should be the Lambda function timeout value?
   [Answer]: 30 seconds (sufficient for hello world demo)

3. What should be the Lambda memory allocation?
   [Answer]: 128 MB (minimum, sufficient for hello world)

4. Should S3 bucket be publicly accessible or private?
   [Answer]: Private (no public access, uploads via authenticated AWS credentials only)

5. What S3 storage class should be used?
   [Answer]: STANDARD (default storage class for demo)

6. Should S3 versioning be enabled?
   [Answer]: No (not required for demo)

7. What CloudWatch Logs retention period should be configured?
   [Answer]: 7 days (sufficient for demo/testing)
