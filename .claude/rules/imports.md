# Imports

## Hard Rules

1. **All imports must be at the top of the file.** No imports inside functions, methods, or conditional blocks.

    **The only exception** is for optional dependencies with graceful degradation:
    ```python
    try:
        import orjson as json
    except ImportError:
        import json  # type: ignore[no-redef]
    ```

2. **Never use `sys.path.append()` or `sys.path.insert()`.** Fix your packaging instead — use `pyproject.toml` and `pip install -e .`.

3. **Never use wildcard imports** (`from module import *`). Import explicitly.

4. **Never use relative imports beyond one level.** `from .models import X` is fine; `from ...core.utils import Y` is not.

## Import Ordering

Imports must be sorted by `ruff` (isort rules) in three groups separated by blank lines:

```python
# 1. Standard library
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path

# 2. Third-party
import polars as pl
import pyarrow as pa
from loguru import logger
from pydantic import BaseModel, Field

# 3. Local/project
from config.settings import TRADES_DIR
from src.storage.schema import TRADES_SCHEMA
```