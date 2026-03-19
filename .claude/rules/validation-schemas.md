# Validation & Schemas

## Validate at Boundaries

All data entering the system — from APIs, files, databases, user input, or external services — must be validated through a schema before use.

## Schema Rules

- **Every config file, API payload, and database result** must have a corresponding schema.
- **Use `strict=True`** in Pydantic models to prevent silent type coercion.
- **Use `Field(...)` constraints** (`min_length`, `ge`, `le`, `pattern`) instead of manual validation where possible.
- **Custom validators** must be `@classmethod` and raise `ValueError` with descriptive messages.
- **PyArrow schemas live in `src/storage/schema.py`; Pydantic models live in `config/schemas.py`** — never inline in scripts or service functions.