# Documentation

Code in `src/` speaks for itself. Prose that explains *why* lives in `docs/`, not in the module.

## The Budget (`src/` only)

| Where | Ceiling |
|---|---|
| Module docstring | **5 lines** |
| Class / function / method docstring | **3 lines** |
| Constant | **1 comment line** |

Lines are counted on the docstring body — the **non-blank** lines between the triple quotes, so a
paragraph break costs nothing and a summary plus two lines of detail is the ceiling for a function.
A constant's comment is one *physical* line: if the sentence plus its `docs/` pointer will not fit
in 100 columns, the sentence is too long. `uv run python -m scripts.check_docs` enforces all three.

Every module, public class and public function still **has** a docstring. The budget is a ceiling on
its length, not permission to drop the summary line.

`scripts/`, `notebooks/` and `tests/` are exempt — a script's docstring doubles as its `--help`, and
a notebook is a narrative by design.

## Rules

- **No `Args:` / `Returns:` / `Raises:` sections in `src/`.** Parameters and return types are
  annotated, and exceptions carry their own context in the message (`error-handling.md`).
- **A name is cheaper than a sentence.** When a parameter needs a caveat — "summed strictly before
  `asof_date` by the caller" — rename it (`trailing_volume_before_asof`) instead of spending budget
  explaining it. Long descriptive names beat short names plus prose.
- **Overflow goes to the knowledge base**, on the page whose `code:` frontmatter claims the module.
  Point at it from the module docstring's last line: `See docs/architecture/pipeline/transforms.md.`
- **Check the page before writing anything down.** The fact is usually already there, and a third
  copy in a docstring is what this budget exists to prevent.
- **Needing more than 3 lines is a design signal.** The function is doing too much, or is named
  wrong. Restructure or rename — don't overflow.
- **No development history** in comments or docstrings. Say what the code does and why it is that
  way — never what it used to do, when it changed, or which pass replaced which. That is `git log`'s
  job.
- Use **Google-style docstrings** everywhere the budget does not apply (`scripts/`, `tests/`).

## Example

```python
"""Apply the cleaning pipeline to raw vendor records before storage.

See docs/architecture/pipeline/transforms.md.
"""


def trailing_volume_before_asof(
    volumes: Sequence[float],
    timestamps: Sequence[datetime],
    asof: datetime,
    window_days: int,
) -> float:
    """Sum of volume strictly before ``asof`` over the trailing window.

    Falls back to the full available history when fewer than ``window_days`` days of
    data precede ``asof``.
    """
```
