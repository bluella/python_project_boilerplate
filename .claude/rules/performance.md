# Performance

- **Profile before optimizing.** Don't guess; use `cProfile`, `line_profiler`, or `py-spy`.
- **Use generators and iterators** for large datasets — don't materialize everything into memory.
- **Use `__slots__`** on dataclasses that will have millions of instances.
- **Batch I/O operations** — never make one database/API call per record.
- **Use appropriate data structures** — `set` for membership checks, `dict` for lookups, `deque` for queues.