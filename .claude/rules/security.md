# Security

- **Never log sensitive data** (tokens, passwords, PII) — even at DEBUG level.
- **Never hardcode credentials.** Use environment variables or secret managers.
- **Validate and sanitize all external input** through schemas before processing.
- **Pin all dependencies** in `pyproject.toml` with exact versions or bounded ranges.
- **Use `exclude-newer` in uv** to defend against supply chain attacks. Set `exclude-newer` under `[tool.uv]` in `pyproject.toml` to a date at least 7 days in the past. This prevents installing packages published less than 7 days ago, giving the community time to detect compromised releases. Update the date periodically (e.g., weekly). Example:
  ```toml
  [tool.uv]
  exclude-newer = "2026-04-02T00:00:00Z"
  ```