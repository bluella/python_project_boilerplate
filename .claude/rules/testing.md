# Testing

## Structure

- One test file per module: `tests/unit/test_<module>.py`.
- Use `conftest.py` for shared fixtures — not test base classes.
- Mark slow or integration tests: `@pytest.mark.integration`.

## Test Data

- **Use factories or fixtures**, not raw dicts.
- **Use `dataclass` / Pydantic model instances** as test inputs — never raw dicts that bypass validation.

## Coverage & Quality

- Strive for good coverage on new code.
- Every public function should have at least one test.
- Schema and validation logic should be thoroughly tested.