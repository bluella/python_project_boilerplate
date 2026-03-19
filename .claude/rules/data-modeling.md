# Data Modeling

## Use Dataclasses or Pydantic Models for Everything

**Every data structure must be a typed dataclass or Pydantic model.** Raw dicts and tuples are not acceptable as data containers that cross function or module boundaries.

```python
# GOOD — structured, typed, self-documenting
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Status(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    ARCHIVED = "archived"


@dataclass(frozen=True)
class UserRecord:
    user_id: str
    email: str
    status: Status
    created_at: datetime
    tags: tuple[str, ...] = field(default_factory=tuple)
```

```python
# BAD — untyped, no schema, no documentation
user = {"user_id": "abc", "email": "x@y.com", "status": "active"}
```

## Dataclass Rules

- **Use `frozen=True`** unless mutation is explicitly required and documented.
- **Use `__post_init__`** for derived fields or validation, not for side effects.
- **Use `field(default_factory=...)`** for mutable defaults — never use mutable default arguments.
- **Prefer `tuple` over `list`** for immutable collections in frozen dataclasses.
- **Use `slots=True`** (Python 3.10+) for performance-critical models.
- **Use `kw_only=True`** (Python 3.10+) for dataclasses with more than 3 fields to prevent positional argument mistakes.

```python
@dataclass(frozen=True, slots=True, kw_only=True)
class PipelineConfig:
    source: str
    destination: str
    batch_size: int = 1000
    retry_limit: int = 3
    timeout_seconds: float = 30.0
```