# Documentation

- **Every module** has a module-level docstring explaining its purpose.
- **Every public class** has a docstring describing what it represents and when to use it.
- **Every public function** has a docstring with a one-line summary, parameter descriptions, return type, and possible exceptions.
- Use **Google-style docstrings**.

```python
def transform_records(
    records: Sequence[RawRecord],
    pipeline: list[TransformFn],
    *,
    strict: bool = True,
) -> list[CleanRecord]:
    """Apply a sequence of transformations to raw records.

    Args:
        records: Input records to transform.
        pipeline: Ordered list of transformation functions to apply.
        strict: If True, raise on first transformation error.
            If False, skip failing records and log warnings.

    Returns:
        List of successfully transformed records.

    Raises:
        DataValidationError: If strict mode is on and a record fails transformation.
        EmptyPipelineError: If pipeline contains no transformation functions.
    """
```