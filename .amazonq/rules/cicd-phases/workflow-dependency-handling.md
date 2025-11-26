## Dependency Types

**CRITICAL**: There are TWO types of dependencies that require different job dependency patterns:

1. **Artifact Dependency**: Code type A needs an artifact from code type B's build job

   - Example: Terraform needs Lambda zip file from Python build
   - Job dependency: `A-deploy` needs `B-build` (NOT `B-deploy`)

2. **Infrastructure Dependency**: Code type A's deploy needs infrastructure created by code type B's deploy
   - Example: Python deploy needs Lambda function to exist (created by Terraform deploy)
   - Job dependency: `A-deploy` needs `B-deploy`

## Single Dependency Pattern - Artifact Dependency

**When Code Type A needs an artifact from Code Type B** (e.g., Terraform needs Python Lambda package):

### MOST PREFERRED Method: Combined Build and Deploy Job

**For tightly coupled dependencies where Terraform manages the Lambda function, combine Python build and Terraform deploy in a single job:**

#### Combined Job Pattern

- **When to Use**:

  - Terraform manages the Lambda function (creates and deploys it)
  - Python build artifact is ONLY needed by Terraform
  - No separate Python deploy job is needed
  - This eliminates artifact passing entirely since both run in the same runner

- **Benefits**:

  - **No artifact passing needed**: Build and deploy happen in same runner environment
  - **Simplest workflow**: Fewer jobs, fewer dependencies, no upload/download steps
  - **No path issues**: Artifact is built exactly where Terraform expects it
  - **Faster execution**: No artifact upload/download overhead

- **Job Structure**:

  ```yaml
  terraform-deploy:
    name: Build Lambda and Deploy Terraform
    needs:
      [
        python-lint,
        python-security,
        python-test,
        terraform-security,
        terraform-validate,
      ]
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4

      # Python Build Steps (build artifact where Terraform expects it)
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"
      - name: Install Python dependencies
        working-directory: src/lambda-python-{feature-name}
        run: |
          if [ -f requirements.txt ] && [ -s requirements.txt ]; then
            pip install -r requirements.txt
          fi
      - name: Build Lambda package for Terraform
        run: |
          mkdir -p ./iac/terraform
          cd src/lambda-python-{feature-name}
          zip -r ../../iac/terraform/lambda_function.zip . -x "*.git*" "*.md" "tests/*" "*.tf*" "iac/**"
          cd ../..
          echo "✓ Lambda package built at: ./iac/terraform/lambda_function.zip"
          ls -lh ./iac/terraform/lambda_function.zip

      # Terraform Deploy Steps (use artifact built above)
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ~1.1
      - name: Configure AWS credentials via OIDC
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
          aws-region: ${{ vars.AWS_REGION }}
      - name: Configure Terraform Cloud
        working-directory: iac/terraform
        env:
          TFC_TOKEN: ${{ secrets.TFC_TOKEN }}
        run: |
          if [ -n "$TFC_TOKEN" ]; then
            cat > $HOME/.terraformrc << EOF
          credentials "app.terraform.io" {
            token = "$TFC_TOKEN"
          }
          EOF
          fi
      - name: Verify Lambda package exists
        run: |
          TERRAFORM_LAMBDA_PATH="./iac/terraform/lambda_function.zip"
          if [ ! -f "$TERRAFORM_LAMBDA_PATH" ]; then
            echo "Error: Lambda package not found at: $TERRAFORM_LAMBDA_PATH"
            exit 1
          fi
          echo "✓ Lambda package verified at: $TERRAFORM_LAMBDA_PATH"
          ls -lh "$TERRAFORM_LAMBDA_PATH"
      - name: Terraform Init
        working-directory: iac/terraform
        run: terraform init
      - name: Terraform Plan
        id: terraform-plan
        working-directory: iac/terraform
        run: terraform plan -out=tfplan
        continue-on-error: true
      - name: Terraform Apply
        working-directory: iac/terraform
        run: |
          if [ "${{ steps.terraform-plan.outcome }}" == "success" ]; then
            terraform apply tfplan
          else
            terraform apply -auto-approve
          fi
  ```

- **Key Points**:
  - Single job combines Python build and Terraform deploy
  - Job waits for both Python CI jobs AND Terraform CI jobs
  - Build step creates artifact directly where Terraform expects it
  - Deploy step uses artifact from same runner (no download needed)
  - No separate `python-build` job needed
  - No artifact upload/download steps needed

### PREFERRED Method: Local Build Placement (Separate Jobs)

**For Lambda functions and similar artifacts, build artifacts directly where Terraform expects them. Use this when you need separate jobs (e.g., for parallelization or when build is used by multiple consumers):**

#### Upstream Job (Code Type B - Python Build)

- Build Lambda package directly in Terraform directory:
  ```yaml
  python-build:
    needs: [python-lint, python-security, python-test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        working-directory: src/lambda-python-{feature-name}
        run: |
          if [ -f requirements.txt ] && [ -s requirements.txt ]; then
            pip install -r requirements.txt
          fi
      - name: Build Lambda package for Terraform
        run: |
          mkdir -p ./iac/terraform
          cd src/lambda-python-{feature-name}
          zip -r ../../iac/terraform/lambda_function.zip . -x "*.git*" "*.md" "tests/*"
          cd ../..
          echo "✓ Lambda package built at: ./iac/terraform/lambda_function.zip"
          ls -lh ./iac/terraform/lambda_function.zip
  ```

**Benefits of Local Build Placement (Separate Jobs):**

- **Simpler workflow**: No artifact upload/download steps needed
- **Terraform deploys source directly**: Terraform's `source_code_hash` automatically detects changes and updates Lambda function code
- **Fewer path issues**: Artifact is already where Terraform expects it
- **No separate deploy job needed**: When Terraform manages Lambda, no separate `python-deploy` job is needed
- **Note**: This still requires artifact passing between jobs (via checkout or artifacts). For simplest solution, use Combined Build and Deploy Job pattern above.

#### Downstream Job (Code Type A - Terraform Deploy)

- **CRITICAL**: Configure job dependency using `needs:` to wait for upstream **build job**:

  ```yaml
  terraform-deploy:
    needs:
      [terraform-lint, terraform-security, terraform-validate, python-build]
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - name: Verify Lambda package exists
        run: |
          TERRAFORM_LAMBDA_PATH="./iac/terraform/lambda_function.zip"
          if [ ! -f "$TERRAFORM_LAMBDA_PATH" ]; then
            echo "Error: Lambda package not found at: $TERRAFORM_LAMBDA_PATH"
            exit 1
          fi
          echo "✓ Lambda package verified at: $TERRAFORM_LAMBDA_PATH"
          ls -lh "$TERRAFORM_LAMBDA_PATH"
      # ... Terraform init/plan/apply steps
  ```

- **Order of operations**: Checkout → Verify artifact exists → Configure credentials → Terraform init/plan/apply
- **Terraform automatically deploys**: When `terraform apply` runs, Terraform detects the zip file change via `source_code_hash` and updates the Lambda function code

### ALTERNATIVE Method: Artifact Upload/Download

**Use this method only if local build placement is not feasible (e.g., multiple consumers or complex dependency chains):**

#### Upstream Job (Code Type B - Python Build)

- Build and package artifacts (e.g., Lambda zip file)
- Upload artifacts using `actions/upload-artifact@v4`:
  ```yaml
  - name: Upload Lambda package
    uses: actions/upload-artifact@v4
    with:
      name: lambda-package
      path: lambda-package.zip
      retention-days: 1
  ```

#### Downstream Job (Code Type A - Terraform Deploy)

- **CRITICAL**: Configure job dependency using `needs:` to wait for upstream **build job** (NOT deploy job):
  ```yaml
  terraform-deploy:
  needs: [terraform-lint, terraform-security, terraform-validate, python-build]
  runs-on: ubuntu-latest
  environment: production
  steps:
    - uses: actions/checkout@v4
  ```
- **CRITICAL**: Download artifacts from upstream build job BEFORE any Terraform operations (with error handling):

  ```yaml
  - name: Download Lambda package from Python build job
    uses: actions/download-artifact@v4
    continue-on-error: true
    id: download-artifact
    with:
      name: lambda-package
      path: ./lambda-package

  - name: Verify artifact downloaded successfully
    if: steps.download-artifact.outcome != 'success'
    run: |
      echo "Error: Failed to download artifact 'lambda-package' from Python build job"
      exit 1
  ```

- **Place artifact in correct location** where Terraform expects it:
  ```yaml
  - name: Move Lambda package to Terraform directory
    run: |
      # CRITICAL: Check the actual path referenced in Terraform code
      # If Terraform uses: filename = "lambda_function.zip" in the same directory
      # Place it where Terraform expects it (e.g., iac/terraform/lambda_function.zip)
      mkdir -p ./iac/terraform
      PACKAGE_FILE=$(find ./lambda-package -name "*.zip" -type f | head -n 1)
      if [ -z "$PACKAGE_FILE" ]; then
        echo "Error: Lambda package zip file not found in downloaded artifact"
        exit 1
      fi
      cp "$PACKAGE_FILE" ./iac/terraform/lambda_function.zip
      echo "TF_VAR_lambda_package_path=$(pwd)/iac/terraform/lambda_function.zip" >> $GITHUB_ENV
  ```
- **Verify artifact exists** before Terraform operations:
  ```yaml
  - name: Verify Lambda package exists
    run: |
      # Verify the exact path that Terraform code references
      TERRAFORM_LAMBDA_PATH="./iac/terraform/lambda_function.zip"
      if [ ! -f "$TERRAFORM_LAMBDA_PATH" ]; then
        echo "Error: Lambda package not found at: $TERRAFORM_LAMBDA_PATH"
        echo "Downloaded artifacts location:"
        ls -la ./lambda-package/ || echo "lambda-package directory not found"
        exit 1
      fi
      echo "✓ Lambda package verified at: $TERRAFORM_LAMBDA_PATH"
  ```
- **Order of operations**: Checkout → Download artifacts → Place artifacts → Verify artifacts → Configure credentials → Terraform init/plan/apply

---

## Combined Dependencies Pattern (Artifact + Infrastructure)

**When a code type has both artifact and infrastructure dependencies** (e.g., Terraform needs Python artifact, Python deploy needs Terraform infrastructure):

```yaml
# Terraform deploy needs Python build artifact
terraform-deploy:
  needs: [terraform-lint, terraform-security, terraform-validate, python-build]
  runs-on: ubuntu-latest
  environment: production
  steps:
    - uses: actions/checkout@v4
    - name: Download Lambda package from Python build
      uses: actions/download-artifact@v4
      with:
        name: lambda-package
        path: ./lambda-package
    # ... Terraform deployment steps

# Python deploy needs Terraform to create Lambda function first
python-deploy:
  needs: [python-build, terraform-deploy]
  runs-on: ubuntu-latest
  environment: production
  steps:
    - uses: actions/checkout@v4
    - name: Download Lambda package
      uses: actions/download-artifact@v4
      with:
        name: lambda-package
    # ... Python deployment steps (updates Lambda function code)
```

**Execution Order**:

1. Python build → produces artifact
2. Terraform deploy → uses Python artifact, creates Lambda function
3. Python deploy → updates Lambda function code (function must exist)

## Multiple Dependencies Pattern

If a code type depends on multiple others, configure job dependencies using `needs:` to wait for all required upstream jobs (build jobs for artifacts, deploy jobs for infrastructure):

```yaml
kubernetes-deploy:
needs:
  [
    kubernetes-lint,
    kubernetes-security,
    kubernetes-validate,
    python-deploy,
    docker-deploy,
  ]
runs-on: ubuntu-latest
environment: production
steps:
  - uses: actions/checkout@v4
  # Download artifacts from all upstream build jobs
  - name: Download Lambda package from Python build
    uses: actions/download-artifact@v4
    with:
      name: lambda-package
      path: ./lambda-package
  - name: Download Docker image info from Docker build
    uses: actions/download-artifact@v4
    with:
      name: docker-image
      path: ./docker-image
```

**Important**: When multiple dependencies exist, download artifacts from all upstream build jobs. Each build job uploads its artifacts independently, so you can download them all in the downstream deploy job.

---

## Artifact Passing Methods

**For Unified Workflow**: Artifact passing happens within the same workflow. Two methods are available:

### Method 1: Local Build Placement (PREFERRED for Lambda functions)

**For Lambda functions and similar artifacts, build directly where Terraform expects them:**

- Build artifact directly in Terraform directory during build job
- No artifact upload/download needed
- Terraform deploys source directly via `terraform apply`
- Terraform's `source_code_hash` automatically detects changes and updates Lambda function code
- **This is the PREFERRED method for Lambda functions managed by Terraform**

**Pattern**:

1. **Build Job** (upstream): Build artifact directly in Terraform directory

   ```yaml
   python-build:
     needs: [python-lint, python-security, python-test]
     steps:
       - uses: actions/checkout@v4
       - name: Build Lambda package for Terraform
         run: |
           mkdir -p ./iac/terraform
           cd src/lambda-python-{feature-name}
           zip -r ../../iac/terraform/lambda_function.zip . -x "*.git*" "*.md" "tests/*"
           cd ../..
   ```

2. **Deploy Job** (downstream): Verify artifact exists, then Terraform applies
   ```yaml
   terraform-deploy:
     needs:
       [terraform-lint, terraform-security, terraform-validate, python-build]
     steps:
       - uses: actions/checkout@v4
       - name: Verify Lambda package exists
         run: |
           if [ ! -f "./iac/terraform/lambda_function.zip" ]; then
             echo "Error: Lambda package not found"
             exit 1
           fi
       # ... Terraform init/plan/apply (Terraform deploys Lambda source automatically)
   ```

### Method 2: GitHub Actions Artifacts (ALTERNATIVE - use if local build placement not feasible)

- Use `actions/upload-artifact@v4` in build jobs
- Use `actions/download-artifact@v4` in deploy jobs
- Works within same workflow run (jobs in same workflow)
- Limited retention (default 1 day, configurable up to 90 days)
- **Use this method only if local build placement is not feasible**

**Pattern**:

1. **Build Job** (upstream): Upload artifact

   ```yaml
   python-build:
     needs: [python-lint, python-security, python-test]
     steps:
       - name: Upload Lambda package
         uses: actions/upload-artifact@v4
         with:
           name: lambda-package
           path: lambda-package.zip
   ```

2. **Deploy Job** (downstream): Download artifact
   ```yaml
   terraform-deploy:
     needs:
       [terraform-lint, terraform-security, terraform-validate, python-build]
     steps:
       - name: Download Lambda package
         uses: actions/download-artifact@v4
         with:
           name: lambda-package
           path: ./lambda-package
   ```

## Single Dependency Pattern - Infrastructure Dependency

**When Code Type A's deploy needs infrastructure created by Code Type B's deploy** (e.g., Python deploy needs Lambda function created by Terraform):

### CRITICAL: Terraform Deploys Lambda Source Directly

**IMPORTANT**: When Terraform manages Lambda functions, Terraform itself should deploy the Lambda source code. The `source_code_hash` attribute in Terraform automatically detects changes to the zip file and updates the Lambda function code when `terraform apply` runs. **This eliminates the need for separate Python deploy jobs that update Lambda function code.**

**Pattern**:

- Terraform creates Lambda function AND deploys source code
- No separate `python-deploy` job needed
- Terraform's `source_code_hash` handles code updates automatically

### When Infrastructure Dependency Still Applies

**Use this pattern only when Python deploy needs infrastructure that Terraform creates BUT Python deploy does NOT update Lambda function code** (e.g., Python deploy uses Lambda function created by Terraform for other purposes):

### Upstream Job (Code Type B - Terraform Deploy)

- Creates infrastructure resources (e.g., Lambda function, S3 bucket, etc.)
- Infrastructure must exist before downstream deploy can update/use it

### Downstream Job (Code Type A - Python Deploy)

- **CRITICAL**: Configure job dependency using `needs:` to wait for upstream **deploy job**:
  ```yaml
  python-deploy:
  needs: [python-build, terraform-deploy]
  runs-on: ubuntu-latest
  environment: production
  steps:
    - uses: actions/checkout@v4
    - name: Configure AWS credentials via OIDC
      uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
        aws-region: ${{ vars.AWS_REGION }}
    - name: Download Lambda package
      uses: actions/download-artifact@v4
      with:
        name: lambda-package
    - name: Deploy Lambda function
      run: |
        # Lambda function must exist (created by Terraform) before updating code
        aws lambda update-function-code \
          --function-name s3-lambda-trigger-hello-world \
          --zip-file fileb://lambda-package/lambda-package.zip || \
        aws lambda create-function \
          --function-name s3-lambda-trigger-hello-world \
          --runtime python3.12 \
          --role ${{ secrets.AWS_LAMBDA_ROLE_ARN }} \
          --handler lambda_handler.lambda_handler \
          --zip-file fileb://lambda-package/lambda-package.zip \
          --memory-size 128
  ```

**Key Points**:

- **For Lambda functions managed by Terraform**: Terraform deploys source code directly - no separate Python deploy job needed
- **For other infrastructure dependencies**: Infrastructure dependency means the resource must exist before deploy
- Wait for upstream deploy job, not build job
- Common pattern: Application code deploy needs infrastructure to exist first (but NOT for Lambda function code updates when Terraform manages Lambda)

### Alternative Methods (Only if needed for special cases)

### Method 2: S3/Storage (For long retention or external access)

- Upload to S3 bucket with predictable naming
- Download from S3 in deploy job
- Use when: Artifacts need longer retention OR external systems need access

### Method 3: Container Registry (For Docker images)

- Push Docker images with tags to registry (ECR, Docker Hub, etc.)
- Reference image tags in deploy jobs
- Use when: Artifact is a Docker/container image

### Method 4: Environment Variables/Job Outputs (For artifact metadata)

- Pass artifact paths/URLs via job outputs
- Use when: Only artifact location/URL needs to be passed (not the artifact itself)

---

## Single Production Workflow Considerations

- Artifact names should be simple and consistent: `lambda-package` (no environment suffix)
- Workflow trigger: `push` to `main` branch only and `workflow_dispatch` for manual execution
- Use appropriate retention for artifacts (1-7 days typically sufficient)
- All deploy jobs use `environment: production` (single production environment)
- Job dependencies (`needs:`) enforce execution order
- Artifacts are passed between jobs in the same workflow (no cross-workflow downloads needed)

---

## Best Practices

1. **Always verify artifacts exist** before using them in deployment steps
2. **Use consistent artifact naming** to avoid conflicts
3. **Handle errors gracefully** with `continue-on-error` and verification steps
4. **Document artifact paths** in workflow comments for maintainability
5. **Use S3/Storage for multiple dependencies** to avoid complexity
6. **Test artifact passing** before deployment

---

## Troubleshooting

- **Artifact not found**: Check artifact name matches exactly (case-sensitive) between upload and download
- **Download fails**: Verify artifact was uploaded in upstream build job and job dependency (`needs:`) is correct
- **Path mismatch**: Verify artifact is placed where deployment code expects it
- **Job runs before dependency**: Verify `needs:` array includes all required upstream jobs
- **Multiple dependencies**: Download all artifacts from their respective build jobs in the deploy job

See `workflow-common-issues.mdc` for more troubleshooting guidance.
