# Testing

## Structure

- Tests mirror the source tree: one file per module at `tests/unit/<package>/test_<module>.py`, so
  `src/storage/schema.py` is tested by `tests/unit/storage/test_schema.py`. Tests covering
  `scripts/` live under `tests/unit/scripts/`.
- Every test folder is a package — a new one needs an empty `__init__.py`. That is what makes test
  modules import under their full dotted path, so two folders may hold the same file name.
- Use `conftest.py` for shared fixtures — not test base classes. The shared one lives at
  `tests/unit/conftest.py` and applies to every folder below it.
- Mark slow or integration tests: `@pytest.mark.integration`.

## Test Data

- **Use factories or fixtures**, not raw dicts.
- **Use `dataclass` / Pydantic model instances** as test inputs — never raw dicts that bypass validation.

## Coverage & Quality

- Strive for good coverage on new code.
- Every public function should have at least one test.
- Schema and validation logic should be thoroughly tested.