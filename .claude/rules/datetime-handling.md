# Datetime Handling

## UTC+0, Timezone-Unaware Everywhere

**All datetimes in the codebase must be UTC+0 and timezone-unaware (naive).**

This applies to all layers: dataclasses, Pydantic models, Polars/Arrow columns, function parameters, constants, and return types.

### Rules

- **Never attach timezone info** to datetime objects in application code. Use `datetime(2024, 1, 1)`, not `datetime(2024, 1, 1, tzinfo=timezone.utc)`.
- **Convert at the boundary.** When downloading or querying data from any external source (APIs, databases, files), the very first cleanup/preparation step must:
  1. Convert all datetimes to UTC+0.
  2. Strip the timezone info to produce naive datetimes.
- **Polars columns** should use `Datetime("us")` (no timezone), not `Datetime("us", "UTC")`. Cast during initial data loading if the source provides tz-aware timestamps.
- **No `timezone`-related imports** should appear outside of boundary/ingestion code.

### Example — Ingestion Boundary

```python
# At the data ingestion boundary: convert to UTC and strip tz
def clean_timestamps(df: pl.DataFrame) -> pl.DataFrame:
    """Convert tz-aware datetime columns to naive UTC datetimes."""
    return df.with_columns(
        pl.col("created_at").dt.convert_time_zone("UTC").dt.replace_time_zone(None),
    )
```

### Example — Application Code

```python
# GOOD — naive UTC datetime
start = datetime(2024, 1, 1)

# BAD — tz-aware datetime in application code
start = datetime(2024, 1, 1, tzinfo=timezone.utc)
```
