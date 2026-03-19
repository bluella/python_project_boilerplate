# Code Style & Formatting

## Tooling

| Tool | Purpose | Config |
|---|---|---|
| `ruff` | Linting + formatting (replaces black, flake8, isort) | `pyproject.toml` |
| `pytest` | Testing | `pyproject.toml` |

All PRs must pass `ruff check` and `ruff format --check` with zero errors.

## Style Rules

- **Maximum line length: 100 characters.**
- **Use trailing commas** in multi-line structures for cleaner diffs.
- **Use f-strings** for string formatting, never `%` or `.format()`.
- **Use `pathlib.Path`**, never `os.path` for filesystem operations.
- **Use `loguru`**, never `print()`, for any output in library/service code.
- **Constants are `UPPER_SNAKE_CASE`** and defined in `constants.py`.
- **Private functions/methods are prefixed with `_`.**
- **No single-letter variable names** except `i`, `j`, `k` in tight loops, or well-known conventions like `df` for DataFrames.

## Naming Conventions

| Entity | Convention | Example |
|---|---|---|
| Module | `snake_case` | `data_loader.py` |
| Class | `PascalCase` | `UserRecord` |
| Function/Method | `snake_case` | `load_records()` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_BATCH_SIZE` |
| Type alias | `PascalCase` | `JsonDict` |
| Enum member | `UPPER_SNAKE_CASE` | `Status.ACTIVE` |