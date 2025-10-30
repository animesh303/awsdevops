# Changelog:
# AWS-2 - Enhanced tagging strategy with local values - 2025-01-27

locals {
  # Common tags applied to all resources
  common_tags = {
    Project         = var.project_name
    Environment     = var.environment
    CostCenter      = var.cost_center
    Owner           = var.owner
    ManagedBy       = "terraform"
    BackupRequired  = var.backup_required
    ComplianceLevel = var.compliance_level
    CreatedDate     = formatdate("YYYY-MM-DD", timestamp())
    JiraTicket      = "AWS-2"
  }

  # Resource-specific tag combinations
  s3_tags = merge(local.common_tags, {
    ResourceType = "storage"
    Service      = "s3"
    Purpose      = "static-website-hosting"
    PublicAccess = "enabled"
  })

  dynamodb_tags = merge(local.common_tags, {
    ResourceType = "database"
    Service      = "dynamodb"
    Purpose      = "data-storage"
    BillingMode  = "on-demand"
  })

  sqs_tags = merge(local.common_tags, {
    ResourceType = "messaging"
    Service      = "sqs"
    Purpose      = "message-queuing"
    Encryption   = "enabled"
  })

  cloudwatch_tags = merge(local.common_tags, {
    ResourceType  = "monitoring"
    Service       = "cloudwatch"
    Purpose       = "logging-monitoring"
    RetentionDays = "14"
  })
}