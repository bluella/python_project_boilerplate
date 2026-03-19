# Type Annotations

## Hard Rules

- **All public functions and methods must have complete type annotations** — parameters and return types.
- **Use modern syntax** (`list[str]` not `List[str]`, `str | None` not `Optional[str]`).
- **Never use `Any`** unless interfacing with genuinely untyped third-party code, and document why.
- **Use `TypeAlias`** for complex types used more than once.
- **Use `Protocol`** for structural subtyping instead of ABCs where appropriate.

```python
from typing import TypeAlias
from collections.abc import Callable, Iterator

JsonDict: TypeAlias = dict[str, "JsonValue"]
JsonValue: TypeAlias = str | int | float | bool | None | list["JsonValue"] | JsonDict
TransformFn: TypeAlias = Callable[[pd.DataFrame], pd.DataFrame]
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