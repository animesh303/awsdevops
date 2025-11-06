# Orchestrator Workflow Patterns

## Purpose

This document defines patterns for generating orchestrator workflows that manage the execution order of code type workflows based on dependencies. Orchestrator workflows simplify dependency management and reduce complexity when multiple code types have interdependencies.

## Overview

**Problem**: When multiple code types have dependencies (e.g., Terraform depends on Python, Kubernetes depends on Docker, etc.), managing `workflow_run` triggers and artifact passing becomes complex and error-prone.

**Solution**: Generate orchestrator workflows that:

- Trigger on branch push (develop/main)
- Invoke code type workflows in dependency order
- Wait for each workflow to complete before starting the next
- Handle artifact passing between workflows
- Simplify the dependency graph

## Architecture

### Two-Tier Workflow Structure

1. **Orchestrator Workflows** (one per environment):

   - `orchestrator-dev.yml` - Orchestrates all code type workflows for dev environment
   - `orchestrator-test.yml` - Orchestrates all code type workflows for test environment
   - `orchestrator-prd.yml` - Orchestrates all code type workflows for prod environment

2. **Code Type Workflows** (three per code type, per environment):
   - `{code-type}-dev.yml` - CI + Deploy to Dev (can be triggered independently or via orchestrator)
   - `{code-type}-test.yml` - CI + Deploy to Test (can be triggered independently or via orchestrator)
   - `{code-type}-prd.yml` - CI + Deploy to Prod (can be triggered independently or via orchestrator)

### Orchestrator Workflow Structure

Each orchestrator workflow:

- Triggers on branch push (develop for dev, main for test/prd)
- Contains jobs that invoke code type workflows in dependency order
- Uses `workflow_run` to wait for each code type workflow to complete
- Handles artifact passing between workflows
- Provides centralized error handling and reporting

## Dependency Resolution

### Topological Sort Algorithm

Orchestrator workflows use topological sort to determine execution order:

1. **Build Dependency Graph**:

   - Nodes: Code types (python, terraform, docker, kubernetes, etc.)
   - Edges: Dependencies (terraform → python means terraform depends on python)
   - Example: `{terraform: [python], kubernetes: [docker], docker: [python]}`

2. **Calculate Execution Order**:

   - Start with code types that have no dependencies (leaf nodes)
   - Process code types in order: dependencies first, dependents after
   - Example order: `[python, docker, terraform, kubernetes]`

3. **Generate Orchestrator Jobs**:
   - One job per code type in dependency order
   - Each job triggers the corresponding code type workflow
   - Each job waits for previous jobs to complete

## Orchestrator Workflow Pattern

### Dev Environment Orchestrator

```yaml
name: Orchestrator Dev

on:
  push:
    branches: [develop]

permissions:
  contents: read
  id-token: write
  actions: write # Required to trigger other workflows

jobs:
  # Job 1: Invoke first code type (no dependencies)
  invoke-python-dev:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Python Dev workflow
        uses: actions/github-script@v7
        with:
          script: |
            const response = await github.rest.actions.createWorkflowDispatch({
              owner: context.repo.owner,
              repo: context.repo.repo,
              workflow_id: 'python-dev.yml',
              ref: context.ref
            });
            console.log('Python Dev workflow triggered');

  # Job 2: Wait for Python Dev, then invoke Terraform Dev
  wait-python-invoke-terraform-dev:
    runs-on: ubuntu-latest
    needs: [invoke-python-dev]
    steps:
      - name: Wait for Python Dev workflow
        uses: lewagon/wait-on-check-action@v1.3.4
        with:
          ref: ${{ github.ref }}
          check-name: "Python Dev"
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          wait-interval: 10
          allowed-conclusions: success

      - name: Download artifacts from Python Dev
        uses: actions/download-artifact@v4
        with:
          name: lambda-package-dev
          github-token: ${{ secrets.GITHUB_TOKEN }}
          # Find the workflow run ID for Python Dev
          run-id: ${{ steps.find-run.outputs.run-id }}

      - name: Trigger Terraform Dev workflow
        uses: actions/github-script@v7
        with:
          script: |
            const response = await github.rest.actions.createWorkflowDispatch({
              owner: context.repo.owner,
              repo: context.repo.repo,
              workflow_id: 'terraform-dev.yml',
              ref: context.ref
            });
            console.log('Terraform Dev workflow triggered');
```

### Alternative: Using workflow_run Pattern

**RECOMMENDED**: Instead of manually triggering workflows, use `workflow_run` to wait for code type workflows:

```yaml
name: Orchestrator Dev

on:
  push:
    branches: [develop]

permissions:
  contents: read
  id-token: write

jobs:
  # This job waits for all code type workflows to complete
  # Code type workflows trigger independently on branch push
  orchestrate-deployment:
    runs-on: ubuntu-latest
    needs: [] # Start immediately
    steps:
      - name: Wait for Python Dev
        uses: lewagon/wait-on-check-action@v1.3.4
        with:
          ref: ${{ github.ref }}
          check-name: "Python Dev"
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          wait-interval: 10
          allowed-conclusions: success

      - name: Download Python artifacts
        uses: actions/download-artifact@v4
        with:
          name: lambda-package-dev
          github-token: ${{ secrets.GITHUB_TOKEN }}
          run-id: ${{ steps.find-python-run.outputs.run-id }}

      - name: Wait for Terraform Dev
        uses: lewagon/wait-on-check-action@v1.3.4
        with:
          ref: ${{ github.ref }}
          check-name: "Terraform Dev"
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          wait-interval: 10
          allowed-conclusions: success

      - name: Deployment Summary
        run: |
          echo "✓ All workflows completed successfully"
          echo "✓ Python Dev: Completed"
          echo "✓ Terraform Dev: Completed"
```

### Recommended Pattern: Sequential Job Invocation

**BEST PRACTICE**: Use sequential jobs that trigger workflows and wait for completion:

```yaml
name: Orchestrator Dev

on:
  push:
    branches: [develop]

permissions:
  contents: read
  id-token: write
  actions: write

jobs:
  # Step 1: Python (no dependencies)
  python-dev:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Find Python Dev workflow run
        uses: actions/github-script@v7
        id: find-run
        with:
          script: |
            // Find the most recent Python Dev workflow run for this commit
            const runs = await github.rest.actions.listWorkflowRuns({
              owner: context.repo.owner,
              repo: context.repo.repo,
              workflow_id: 'python-dev.yml',
              head_sha: context.sha,
              per_page: 1
            });

            if (runs.data.workflow_runs.length === 0) {
              // Trigger the workflow if it hasn't run yet
              await github.rest.actions.createWorkflowDispatch({
                owner: context.repo.owner,
                repo: context.repo.repo,
                workflow_id: 'python-dev.yml',
                ref: context.ref
              });
              // Wait a bit and find the run
              await new Promise(resolve => setTimeout(resolve, 5000));
              const newRuns = await github.rest.actions.listWorkflowRuns({
                owner: context.repo.owner,
                repo: context.repo.repo,
                workflow_id: 'python-dev.yml',
                head_sha: context.sha,
                per_page: 1
              });
              core.setOutput('run-id', newRuns.data.workflow_runs[0].id);
            } else {
              core.setOutput('run-id', runs.data.workflow_runs[0].id);
            }

      - name: Wait for Python Dev to complete
        uses: lewagon/wait-on-check-action@v1.3.4
        with:
          ref: ${{ github.ref }}
          check-name: "Python Dev"
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          wait-interval: 10
          allowed-conclusions: success

      - name: Download Python artifacts
        uses: actions/download-artifact@v4
        with:
          name: lambda-package-dev
          github-token: ${{ secrets.GITHUB_TOKEN }}
          run-id: ${{ steps.find-run.outputs.run-id }}

  # Step 2: Terraform (depends on Python)
  terraform-dev:
    runs-on: ubuntu-latest
    needs: [python-dev]
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Download Python artifacts from previous job
        uses: actions/download-artifact@v4
        with:
          name: lambda-package-dev
          github-token: ${{ secrets.GITHUB_TOKEN }}
          run-id: ${{ needs.python-dev.outputs.run-id }}

      - name: Place artifacts for Terraform
        run: |
          mkdir -p ./iac/terraform
          cp ./lambda-package-dev/lambda-package.zip ./iac/terraform/lambda_function.zip
          echo "✓ Lambda package placed for Terraform"

      - name: Find Terraform Dev workflow run
        uses: actions/github-script@v7
        id: find-run
        with:
          script: |
            const runs = await github.rest.actions.listWorkflowRuns({
              owner: context.repo.owner,
              repo: context.repo.repo,
              workflow_id: 'terraform-dev.yml',
              head_sha: context.sha,
              per_page: 1
            });

            if (runs.data.workflow_runs.length === 0) {
              await github.rest.actions.createWorkflowDispatch({
                owner: context.repo.owner,
                repo: context.repo.repo,
                workflow_id: 'terraform-dev.yml',
                ref: context.ref
              });
              await new Promise(resolve => setTimeout(resolve, 5000));
              const newRuns = await github.rest.actions.listWorkflowRuns({
                owner: context.repo.owner,
                repo: context.repo.repo,
                workflow_id: 'terraform-dev.yml',
                head_sha: context.sha,
                per_page: 1
              });
              core.setOutput('run-id', newRuns.data.workflow_runs[0].id);
            } else {
              core.setOutput('run-id', runs.data.workflow_runs[0].id);
            }

      - name: Wait for Terraform Dev to complete
        uses: lewagon/wait-on-check-action@v1.3.4
        with:
          ref: ${{ github.ref }}
          check-name: "Terraform Dev"
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          wait-interval: 10
          allowed-conclusions: success

  # Final: Deployment Summary
  deployment-summary:
    runs-on: ubuntu-latest
    needs: [python-dev, terraform-dev]
    if: always()
    steps:
      - name: Generate deployment summary
        run: |
          echo "## Deployment Summary" >> $GITHUB_STEP_SUMMARY
          echo "| Workflow | Status |" >> $GITHUB_STEP_SUMMARY
          echo "|----------|--------|" >> $GITHUB_STEP_SUMMARY
          echo "| Python Dev | ${{ needs.python-dev.result }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Terraform Dev | ${{ needs.terraform-dev.result }} |" >> $GITHUB_STEP_SUMMARY
```

## Code Type Workflow Modifications

### Make Code Type Workflows Orchestrator-Compatible

Code type workflows should:

1. **Support workflow_dispatch trigger** (for orchestrator invocation):

   ```yaml
   on:
     push:
       branches: [develop]
     workflow_dispatch: # Allow orchestrator to trigger
   ```

2. **Upload artifacts with consistent naming**:

   ```yaml
   - name: Upload artifacts
     uses: actions/upload-artifact@v4
     with:
       name: {code-type}-package-{environment}  # Consistent naming
       path: {artifact-path}
       retention-days: 7
   ```

3. **Set workflow outputs** (for orchestrator to track):
   ```yaml
   jobs:
     deploy-dev:
       outputs:
         artifact-name: lambda-package-dev
         artifact-path: ./lambda-package.zip
         deployment-status: ${{ job.status }}
   ```

## Dependency Graph Generation

### Algorithm for Building Execution Order

```python
def build_execution_order(dependency_map):
    """
    Build execution order from dependency map.

    Args:
        dependency_map: List of {code_type, depends_on, artifacts}
        Example: [
            {"code_type": "terraform", "depends_on": "python", "artifacts": ["lambda-package.zip"]},
            {"code_type": "kubernetes", "depends_on": "docker", "artifacts": ["docker-image"]}
        ]

    Returns:
        List of code types in execution order
    """
    # Build dependency graph
    graph = {}
    all_types = set()

    for dep in dependency_map:
        code_type = dep["code_type"]
        depends_on = dep["depends_on"]
        all_types.add(code_type)
        all_types.add(depends_on)

        if code_type not in graph:
            graph[code_type] = []
        graph[code_type].append(depends_on)

    # Add code types with no dependencies
    for code_type in all_types:
        if code_type not in graph:
            graph[code_type] = []

    # Topological sort
    in_degree = {code_type: 0 for code_type in all_types}
    for code_type, deps in graph.items():
        for dep in deps:
            in_degree[code_type] += 1

    queue = [code_type for code_type, degree in in_degree.items() if degree == 0]
    execution_order = []

    while queue:
        current = queue.pop(0)
        execution_order.append(current)

        for code_type, deps in graph.items():
            if current in deps:
                in_degree[code_type] -= 1
                if in_degree[code_type] == 0:
                    queue.append(code_type)

    return execution_order
```

## Environment-Specific Orchestrators

### Dev Environment (`orchestrator-dev.yml`)

- **Trigger**: Push to `develop` branch
- **Execution**: Invokes all code type workflows in dependency order
- **Artifact Handling**: Downloads and passes artifacts between workflows
- **Error Handling**: Stops on first failure, reports which workflow failed

### Test Environment (`orchestrator-test.yml`)

- **Trigger**: Push to `main` branch
- **Execution**: Same as dev, but for test environment
- **Artifact Handling**: Uses test-specific artifact names
- **Error Handling**: Same as dev

### Prod Environment (`orchestrator-prd.yml`)

- **Trigger**: `workflow_run` after successful `orchestrator-test.yml` completion
- **Execution**: Same pattern, but for prod environment
- **Artifact Handling**: Uses prod-specific artifact names, longer retention
- **Error Handling**: More strict - requires manual approval for retry

## Benefits of Orchestrator Pattern

1. **Simplified Dependency Management**: Dependencies are managed in one place (orchestrator)
2. **Clear Execution Order**: Topological sort ensures correct order
3. **Centralized Error Handling**: One place to handle failures and report status
4. **Reusable Code Type Workflows**: Code type workflows can still be triggered independently
5. **Easier Debugging**: Single workflow run shows entire deployment pipeline
6. **Scalability**: Easy to add new code types without modifying existing workflows

## When to Use Orchestrators

**ALWAYS Use Orchestrators**: Orchestrator workflows are generated for ALL scenarios to maintain consistency and simplify dependency management:

- Multiple code types with dependencies
- Single code type (no dependencies)
- Multiple independent code types
- Complex dependency graphs

**Benefits of Always Using Orchestrators**:

- Consistent workflow structure across all projects
- Simplified logic (no conditional generation)
- Centralized control and visibility
- Easier to add dependencies later without restructuring
- Uniform deployment pipeline regardless of complexity

## Implementation Checklist

When generating orchestrator workflows:

- [ ] Build dependency graph from Phase 1 analysis
- [ ] Calculate execution order using topological sort
- [ ] Generate orchestrator workflow for each environment (dev/test/prd)
- [ ] Modify code type workflows to support `workflow_dispatch` trigger
- [ ] Ensure consistent artifact naming across workflows
- [ ] Add artifact download/upload steps in orchestrator
- [ ] Add error handling and status reporting
- [ ] Test orchestrator with simple dependency chain first
- [ ] Document execution order in orchestrator workflow comments

## Related Documents

- `workflow-dependency-handling.md` - Detailed dependency patterns
- `phase2-generate-workflow.md` - Workflow generation steps
- `cicd-github-workflow.md` - Main workflow generation rules
