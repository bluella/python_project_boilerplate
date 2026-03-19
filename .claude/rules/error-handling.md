# Error Handling

## Custom Exception Hierarchy

Define project-specific exceptions. Never raise bare `Exception` or `ValueError` for domain errors.

```python
class ProjectError(Exception):
    """Base exception for all project errors."""

class DataValidationError(ProjectError):
    """Raised when input data fails validation."""

class SchemaEvolutionError(ProjectError):
    """Raised when a schema change is incompatible."""

class SourceConnectionError(ProjectError):
    """Raised when a data source is unreachable."""
```

## Rules

- **Never use bare `except:`** or `except Exception:` without re-raising or logging.
- **Never silently swallow exceptions.** At minimum, log the error.
- **Use specific exception types** in except clauses.
- **Always include context** in error messages (what failed, what was expected, what was received).