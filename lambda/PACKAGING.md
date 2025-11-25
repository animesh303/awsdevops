# Lambda Deployment Package

This directory contains scripts to create a deployment package for the IAM User Monitor Lambda function.

## Overview

The Lambda deployment package includes:
- All Lambda function Python modules (lambda_function.py, iam_scanner.py, etc.)
- Production dependencies from requirements.txt (boto3, etc.)
- Proper file structure for AWS Lambda execution

Test files and test-only dependencies (hypothesis, moto) are excluded from the package.

## Packaging Scripts

Two packaging scripts are provided:

### 1. Bash Script (package.sh)

**Usage:**
```bash
cd lambda
./package.sh
```

**Requirements:**
- Bash shell
- Python 3.x with pip
- zip utility

### 2. Python Script (package.py)

**Usage:**
```bash
cd lambda
python3 package.py
```

**Requirements:**
- Python 3.x with pip

## Output

Both scripts create `lambda_deployment.zip` in the lambda directory.

**Typical package size:** ~22-23 MB

**Package structure:**
```
lambda_deployment.zip
├── lambda_function.py          # Main handler
├── iam_scanner.py              # IAM scanning logic
├── dynamodb_writer.py          # DynamoDB operations
├── metrics_emitter.py          # CloudWatch metrics
├── logger_config.py            # Structured logging
├── concurrency_lock.py         # Concurrency control
├── boto3/                      # AWS SDK
├── botocore/                   # AWS SDK core
└── [other dependencies]
```

## Deployment

The generated ZIP file can be deployed to AWS Lambda using:

1. **AWS Console:** Upload the ZIP file directly
2. **AWS CLI:**
   ```bash
   aws lambda update-function-code \
     --function-name iam-user-monitor \
     --zip-file fileb://lambda_deployment.zip
   ```
3. **Terraform:** Reference the ZIP file in the Lambda function resource

## Package Optimization

The packaging scripts automatically:
- Remove `__pycache__` directories
- Remove `.dist-info` directories
- Remove test directories
- Remove `.pyc` and `.pyo` files
- Exclude test-only dependencies (hypothesis, moto)

## Troubleshooting

### Package too large

If the package exceeds Lambda's 50 MB limit (uncompressed):
- Review dependencies in requirements.txt
- Consider using Lambda Layers for large dependencies
- Use AWS Lambda's container image support for larger packages

### Missing dependencies

If the Lambda function fails with import errors:
- Verify all required modules are in requirements.txt
- Check that pip install completed successfully
- Ensure the package.sh or package.py script ran without errors

### Permission errors

If you encounter permission errors:
- Ensure the scripts are executable: `chmod +x package.sh package.py`
- Check write permissions in the lambda directory
- Run with appropriate user permissions

## CI/CD Integration

The Python script (package.py) is recommended for CI/CD pipelines as it's more portable and provides better error handling.

**Example GitHub Actions workflow:**
```yaml
- name: Package Lambda function
  run: |
    cd lambda
    python3 package.py
    
- name: Deploy to AWS
  run: |
    aws lambda update-function-code \
      --function-name iam-user-monitor \
      --zip-file fileb://lambda/lambda_deployment.zip
```
