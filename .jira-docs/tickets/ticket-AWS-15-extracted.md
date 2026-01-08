# AWS-15 Extracted Information

## Key Requirements

- **Objective**: Setup S3 bucket with lifecycle policy
- **Bucket Configuration**: Private, encrypted (SSE-S3), no versioning
- **Lifecycle Rules**: 
  - 30 days → Standard-IA
  - 90 days → Glacier
  - 365 days → Delete

## Technical Stack

- **IaC Tool**: Terraform
- **AWS Services**: S3, IAM, CloudWatch
- **Region**: us-east-1

## Status

Requirements specification already exists and is approved. Ready for code generation phase.
