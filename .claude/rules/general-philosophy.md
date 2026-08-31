# General Philosophy

- **Explicit is better than implicit.** Prefer clear, typed, validated data structures over raw dicts, tuples, or untyped containers.
- **Fail fast, fail loudly.** Validate inputs at boundaries; never silently swallow errors.
- **Immutability by default.** Use `frozen=True` dataclasses and avoid mutation where possible.
- **No magic.** Code should be understandable without tracing dynamic imports, monkey-patching, or runtime path manipulation.
- **Single responsibility.** Every module, class, and function should do one thing. If a description needs "and," split it.
- **Locality over fragmentation.** A private helper with exactly one caller is usually a comment in disguise — inline it. Extract only when logic is genuinely shared (2+ callers) or isolates a separate concern (an I/O boundary, a separately testable pure core). One longer function that reads top-to-bottom beats a scatter of `_pieces` the reader must jump around to reassemble. "Single responsibility" bounds what a function is *about*, not how many lines it may have.
- **Readability — code should speak for itself.** Prefer long, descriptive variable and function names over short names with explanatory comments. If a name needs a comment to clarify its purpose, rename it instead.
