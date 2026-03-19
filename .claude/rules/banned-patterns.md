# Banned Patterns

| Pattern | Why It's Banned | Alternative |
|---|---|---|
| `import inside function` | Hidden dependencies, breaks traceability | Top-level imports |
| `sys.path.append(...)` | Fragile, non-reproducible import resolution | Proper packaging with `pyproject.toml` |
| `from x import *` | Namespace pollution, unclear dependencies | Explicit named imports |
| Raw `dict` as data model | No type safety, no validation, no docs | `dataclass` or Pydantic model |
| Bare `except:` / `except Exception:` | Silently hides bugs | Specific exception types |
| `Any` type (unqualified) | Defeats the type system | Proper types, generics, protocols |
| `print()` in library code | Unstructured, can't be filtered/routed | `loguru` |
| `os.path` | Stringly-typed, platform-inconsistent | `pathlib.Path` |
| Magic strings for categories | Typo-prone, no autocomplete, no exhaustiveness checking | `Enum` / `StrEnum` |
| Mutable default arguments | Shared state bug | `field(default_factory=...)` |
| `import pandas` | Not installed; adds unnecessary dependency | `polars` |