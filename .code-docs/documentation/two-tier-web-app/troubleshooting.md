# Troubleshooting Guide

## Common Issues

### 1. Terraform Init Fails

**Problem**: Backend configuration error
```
Error: Failed to configure the backend
```

**Solution**: 
- Verify Terraform Cloud organization and workspace names
- Check authentication with `terraform login`

### 2. Resource Creation Fails

**Problem**: Insufficient permissions
```
Error: AccessDenied
```

**Solution**:
- Verify AWS credentials: `aws sts get-caller-identity`
- Ensure IAM user/role has required permissions

### 3. Load Balancer Health Check Fails

**Problem**: Instances marked unhealthy
```
Target health check failed
```

**Solution**:
- Check security group rules
- Verify Apache is running on web tier instances
- Check instance logs: `sudo tail -f /var/log/httpd/error_log`

### 4. S3 Access Issues

**Problem**: EC2 instances cannot access S3
```
AccessDenied: Access Denied
```

**Solution**:
- Verify IAM instance profile is attached
- Check S3 bucket policy and IAM role permissions

## Validation Commands

### Check Infrastructure
```bash
# Verify VPC
aws ec2 describe-vpcs --filters "Name=tag:Name,Values=two-tier-web-app-vpc"

# Check instances
aws ec2 describe-instances --filters "Name=tag:JiraId,Values=AWS-3"

# Test load balancer
curl -I $(terraform output -raw load_balancer_url)
```

### Check Logs
```bash
# CloudWatch logs
aws logs describe-log-groups --log-group-name-prefix "/aws/ec2/two-tier-web-app"

# Instance logs (SSH to instance)
sudo tail -f /var/log/cloud-init-output.log
```

## Support

For additional support:
1. Check AWS CloudTrail for API errors
2. Review Terraform state: `terraform show`
3. Validate configuration: `terraform validate`