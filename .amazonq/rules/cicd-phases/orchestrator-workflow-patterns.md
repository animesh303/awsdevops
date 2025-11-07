# Orchestrator Workflow Patterns

## Purpose

This document defines patterns for generating orchestrator workflows that manage the execution order of code type workflows based on dependencies. Orchestrator workflows simplify dependency management and reduce complexity when multiple code types have interdependencies.

## Overview

**Problem**: When multiple code types have dependencies (e.g., Terraform depends on Python, Kubernetes depends on Docker, etc.), managing execution order and dependencies becomes complex and error-prone.

**Solution**: Generate orchestrator workflows that:

- Trigger on branch push (develop/main)
- Invoke code type workflows in dependency order using reusable workflow syntax
- Each workflow automatically waits for the previous one to complete
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
- Uses reusable workflows with direct `uses` syntax to chain workflows sequentially
- Each step automatically waits for the previous workflow to complete
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

3. **Generate Orchestrator Steps**:
   - One step per code type in dependency order
   - Each step uses `uses: ./.github/workflows/{code-type}-{env}.yml`
   - Steps execute sequentially, automatically waiting for previous steps

## Orchestrator Workflow Pattern

Use reusable workflows with direct `uses` syntax for clean, simple chaining:

```yaml
name: Orchestrator Dev

on:
  push:
    branches: [develop]
  workflow_dispatch:

permissions:
  contents: read
  id-token: write

jobs:
  orchestrate:
    runs-on: ubuntu-latest
    steps:
      - name: Run Python Dev Workflow
        uses: ./.github/workflows/python-dev.yml

      - name: Run Terraform Dev Workflow
        uses: ./.github/workflows/terraform-dev.yml

      - name: Run Kubernetes Dev Workflow
        uses: ./.github/workflows/kubernetes-dev.yml
```

**Note**: This pattern requires code type workflows to be defined as reusable workflows with `workflow_call` trigger:

```yaml
# python-dev.yml
name: Python Dev

on:
  workflow_call: # Required for reusable workflows
  push:
    branches: [develop]

jobs:
  deploy-dev:
    runs-on: ubuntu-latest
    steps:
      # ... workflow steps
```

**Benefits**:

- Simplest syntax - no complex scripting needed
- Automatic dependency chaining (each step waits for previous)
- Clean, readable workflow structure
- Native GitHub Actions feature
- No need for workflow_dispatch or complex artifact handling

## Code Type Workflow Modifications

### Make Code Type Workflows Orchestrator-Compatible

Code type workflows should:

1. **Support workflow_call trigger** (required for reusable workflows):

   ```yaml
   on:
     workflow_call: # Required for reusable workflows
     push:
       branches: [develop]
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
- **Execution**: Invokes all code type workflows in dependency order using `uses` syntax
- **Error Handling**: Stops on first failure, reports which workflow failed

### Test Environment (`orchestrator-test.yml`)

- **Trigger**: Push to `main` branch
- **Execution**: Same as dev, but for test environment
- **Error Handling**: Same as dev

### Prod Environment (`orchestrator-prd.yml`)

- **Trigger**: `workflow_run` after successful `orchestrator-test.yml` completion
- **Execution**: Same pattern, but for prod environment
- **Error Handling**: More strict - requires manual approval for retry

## Benefits of Orchestrator Pattern

1. **Simplified Dependency Management**: Dependencies are managed in one place (orchestrator)
2. **Clear Execution Order**: Topological sort ensures correct order
3. **Simple Syntax**: Using reusable workflows (`uses: ./.github/workflows/wf.yml`) provides the cleanest, most readable workflow structure
4. **Centralized Error Handling**: One place to handle failures and report status
5. **Reusable Code Type Workflows**: Code type workflows can still be triggered independently
6. **Easier Debugging**: Single workflow run shows entire deployment pipeline
7. **Scalability**: Easy to add new code types without modifying existing workflows

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
- [ ] Use reusable workflow pattern (`uses: ./.github/workflows/{code-type}-{env}.yml`)
- [ ] Modify code type workflows to support `workflow_call` trigger
- [ ] Ensure consistent artifact naming across workflows
- [ ] Add error handling and status reporting
- [ ] Test orchestrator with simple dependency chain first
- [ ] Document execution order in orchestrator workflow comments

## Related Documents

- `workflow-dependency-handling.md` - Detailed dependency patterns
- `phase2-generate-workflow.md` - Workflow generation steps
- `cicd-github-workflow.md` - Main workflow generation rules
