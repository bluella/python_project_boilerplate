# Type Annotations

## Hard Rules

- **All public functions and methods must have complete type annotations** — parameters and return types.
- **Use modern syntax** (`list[str]` not `List[str]`, `str | None` not `Optional[str]`).
- **Never use `Any`** unless interfacing with genuinely untyped third-party code, and document why.
- **Name an alias** for complex types used more than once — with the `type` keyword, not
  `TypeAlias`, which `ruff` rejects under UP040.
- **Use `Protocol`** for structural subtyping instead of ABCs where appropriate.

```python
from collections.abc import Callable, Iterator

type JsonDict = dict[str, JsonValue]
type JsonValue = str | int | float | bool | None | list[JsonValue] | JsonDict
type TransformFn = Callable[[pl.DataFrame], pl.DataFrame]
```

## Generics

Use generics for reusable containers and utilities:

```python
from typing import Generic, TypeVar
from dataclasses import dataclass

T = TypeVar("T")

@dataclass(frozen=True)
class Result(Generic[T]):
    value: T | None
    error: str | None = None

    @property
    def is_ok(self) -> bool:
        return self.error is None
```