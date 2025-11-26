# Terraform Coding Standards

## File Organization

- **{feature-name}-main.tf**: Feature-specific infrastructure resources
- **{feature-name}-variables.tf**: Feature-specific input variables with descriptions
- **{feature-name}-output.tf**: Feature-specific output values with descriptions
- **{feature-name}-local.tf**: Feature-specific local values and data sources
- **shared-variables.tf**: Shared variables across features
- **shared-outputs.tf**: Shared outputs across features
- **versions.tf**: Provider version constraints
- **terraform.tfvars.example**: Example variable values

## Naming Conventions

- Use snake_case for resource names
- Use descriptive names: `aws_s3_bucket_data_storage`
- Include environment prefix: `prod_`, `staging_`, `dev_`
- Use consistent tagging strategy

## Security Best Practices

- Use least privilege IAM policies
- Enable encryption at rest and in transit
- Use VPC endpoints where appropriate
- Implement proper logging and monitoring
- Use AWS Secrets Manager for sensitive data

## Code Quality

- Use consistent indentation (2 spaces)
- Add comments for complex logic
- Use data sources instead of hardcoded values
- Implement proper error handling
- Use terraform fmt and validate

## Changelog Requirements

- **MANDATORY**: Include changelog history at the top of each .tf file as comments
- Format: `# Changelog: [JIRA-TICKET-NUMBER] - [Description] - [Date]`
- Include all changes made to the file with JIRA ticket references
- Example:
  ```hcl
  # Changelog:
  # AWS-123 - Initial S3 bucket creation - 2024-01-15
  # AWS-124 - Added encryption configuration - 2024-01-16
  # AWS-125 - Updated tags and monitoring - 2024-01-17
  ```

## Example Structure

```hcl
# data-processing-main.tf
# Changelog:
# AWS-123 - Initial S3 bucket creation - 2024-01-15
# AWS-124 - Added encryption configuration - 2024-01-16

resource "aws_s3_bucket" "data_storage" {
  bucket = var.bucket_name
  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

# data-processing-variables.tf
variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

# data-processing-output.tf
output "bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.data_storage.arn
}

# shared-variables.tf
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}
```
