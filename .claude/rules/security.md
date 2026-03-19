# Security

- **Never log sensitive data** (tokens, passwords, PII) — even at DEBUG level.
- **Never hardcode credentials.** Use environment variables or secret managers.
- **Validate and sanitize all external input** through schemas before processing.
- **Pin all dependencies** in `pyproject.toml` with exact versions or bounded ranges.