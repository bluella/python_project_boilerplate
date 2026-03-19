# Git Workflow

## Branch Naming

```
feature/short-description
fix/issue-number-short-description
refactor/what-changed
docs/what-documented
```

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(models): add UserRecord dataclass with validation
fix(loader): handle empty CSV files without crashing
refactor(pipeline): replace raw dicts with typed TransformStep
test(validators): add edge-case tests for email validation
```

## Pull Request Checklist

Before submitting a PR, ensure:

- All new data structures use dataclasses or Pydantic models (no raw dicts crossing boundaries)
- All imports are at the top of the file
- No `sys.path` manipulation anywhere
- No wildcard imports
- All public functions have complete type annotations
- All external data has a corresponding validation schema
- Custom exceptions used instead of bare `ValueError` / `Exception`
- New code has tests with adequate coverage
- `ruff check` passes with zero errors
- `ruff format --check` passes
- No `# type: ignore` without an accompanying comment explaining why