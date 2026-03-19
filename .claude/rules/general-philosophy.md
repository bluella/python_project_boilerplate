# General Philosophy

- **Explicit is better than implicit.** Prefer clear, typed, validated data structures over raw dicts, tuples, or untyped containers.
- **Fail fast, fail loudly.** Validate inputs at boundaries; never silently swallow errors.
- **Immutability by default.** Use `frozen=True` dataclasses and avoid mutation where possible.
- **No magic.** Code should be understandable without tracing dynamic imports, monkey-patching, or runtime path manipulation.
- **Readability — code should speak for itself.** Prefer long, descriptive variable and function names over short names with explanatory comments. If a name needs a comment to clarify its purpose, rename it instead. 