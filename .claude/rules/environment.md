# Environment & Tooling

## Package Management

- **Use `uv`** for all package management — never `pip` directly.
- **Virtual environment**: `.venv` in the project root.
- Install commands: `uv sync`, `uv add <package>`, `uv run <command>`.
- To run scripts: `uv run python script.py`.

## Visualization

- **Use `plotly`** for all charts and visualizations — never `matplotlib`.
- Use `plotly.graph_objects` for fine-grained control, `plotly.express` for quick exploration.
- Plotly works well in both Jupyter notebooks and `.py` notebooks with `#%%` syntax.

## Core Dependencies

```
pyarrow, duckdb, polars, httpx, huggingface-hub,
pydantic, pydantic-settings, python-dotenv, tqdm, loguru,
websockets, plotly
```

## Dev Dependencies

```
pytest, jupyter, ipykernel, ruff
```

No Airflow/Spark/Docker/Postgres — kept simple for research.

## Environment Variables

- **Store secrets and configuration in `.env`** at the project root.
- **Use `python-dotenv`** to load environment variables. Call `load_dotenv()` once at application entry points (e.g., `config/settings.py`), not scattered across modules.
- **Never commit `.env` to version control.** Ensure `.env` is in `.gitignore`.
- **Provide a `.env.example`** with placeholder values for required variables so new contributors know what to set.

```python
# config/settings.py
from dotenv import load_dotenv

load_dotenv()  # loads .env from project root
```

## DataFrame Library

- **Use `polars`** for all DataFrame operations — never `pandas`.
- Pandas is not installed and should not be added as a dependency.
- If a third-party library returns a pandas DataFrame, convert it to Polars immediately at the boundary (e.g., `pl.from_pandas(df)`).
- Only use pandas as a last resort when a required operation has no Polars equivalent, and document why.
