# Deployment Guide

## Step-by-Step Deployment

### 1. Prepare Lambda Package

```bash
cd src/lambda-python-s3-lambda-trigger
zip -r ../../iac/terraform/lambda_function.zip .
```

### 2. Deploy Infrastructure

```bash
cd iac/terraform
terraform init
terraform plan
terraform apply
```

### 3. Verify Deployment

```bash
# Check S3 bucket
aws s3 ls s3://demobucketforawsaidevops

# Check Lambda function
aws lambda get-function --function-name hello_world

# Test the trigger
echo "Hello World Test" > test.txt
aws s3 cp test.txt s3://demobucketforawsaidevops/
aws logs tail /aws/lambda/hello_world --follow
```

## Environment-Specific Deployment

### Development
- Uses default variables
- 14-day log retention
- Basic monitoring

### Production
- Update variables in `terraform.tfvars`
- Extended log retention
- Enhanced monitoring and alerting

## Troubleshooting

### Common Issues

1. **Lambda package not found**
   - Ensure `lambda_function.zip` exists in `iac/terraform/`
   - Re-run the package creation step

2. **S3 permissions error**
   - Verify IAM role has S3 read permissions
   - Check bucket policy and ACLs

3. **Lambda not triggering**
   - Verify S3 event notification configuration
   - Check Lambda permissions for S3 invocation