"""Lint the ``docs/`` knowledge base, and regenerate its indexes.

The knowledge base rots when nothing checks it: links go stale after a rename, a new page never
reaches an index, and a page's ``updated`` date stops meaning anything. This is the lint step that
keeps the structure in `.claude/rules/knowledge-base.md` true. Run as a module:

    uv run python -m scripts.check_docs                # check, non-zero exit on any error
    uv run python -m scripts.check_docs --write-index  # regenerate index blocks, then check

Checks:

- **frontmatter** — every page carries ``title``, ``summary`` and a naive ``updated`` date;
- **links** — every relative markdown link resolves to a file that exists;
- **code references** — every path in a page's ``code:`` list exists in the repo;
- **index coverage** — every page is listed in ``docs/README.md`` or in its folder ``README.md``;
- **docstring budget** — ``src/`` prose stays within `.claude/rules/documentation.md`: 5 lines a
  module docstring, 3 a class or function one, 1 a constant's comment. Overflow belongs on the page
  whose ``code:`` claims the module, which is what makes this a knowledge-base check;
- **orphans** — pages nothing links to (reported as a warning, never fatal);
- **staleness** — pages whose ``code:`` modules were committed after the page's ``updated`` date
  (a warning: a code change does not always invalidate the page, but it always deserves a look).

``docs/plans/`` is exempt: plans are a dated record of intent, not maintained knowledge, and they
deliberately quote the paths that were true when they were written.
"""

import argparse
import ast
import re
import subprocess
import sys
import tokenize
from collections.abc import Iterator
from datetime import date
from functools import cache
from pathlib import Path

import yaml
from loguru import logger
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from src.exceptions import DataValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
SRC_DIR = REPO_ROOT / "src"

#: The prose budget from `.claude/rules/documentation.md`, in non-blank lines of docstring body.
#: Anything longer belongs on the knowledge-base page whose ``code:`` claims the module.
MODULE_DOCSTRING_MAX_LINES = 5
DEFINITION_DOCSTRING_MAX_LINES = 3

#: Comments that carry no prose — tool pragmas and ``# --- section ---`` dividers — and so are never
#: counted against the one-line constant budget.
PRAGMA_COMMENT_RE = re.compile(r"^#\s*(?:type:|noqa|ruff:|fmt:|!|-{3,})")

EXEMPT_DIRS = frozenset({"plans"})
INDEX_START = "<!-- index:start -->"
INDEX_END = "<!-- index:end -->"

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
EXTERNAL_LINK_PREFIXES = ("http://", "https://", "mailto:", "#", "/")


class DocPageFrontmatter(BaseModel):
    """The required YAML header on every knowledge-base page.

    Pages may carry extra keys; only the fields below are enforced, because only these the
    indexes and the staleness audit depend on. ``code`` is optional — a page under ``domain/``
    or ``project/`` documents no module.
    """

    model_config = ConfigDict(frozen=True, extra="allow")

    title: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    updated: date
    code: tuple[str, ...] = ()

    @property
    def one_line_summary(self) -> str:
        """The summary collapsed to a single line, for printing in an index bullet."""
        return re.sub(r"\s+", " ", self.summary).strip()


#: Every page that parsed, keyed by absolute path — built once, shared by the checks that need it.
type FrontmatterByPage = dict[Path, DocPageFrontmatter]


def iter_pages() -> Iterator[Path]:
    """Yield every knowledge-base page, skipping the exempt directories."""
    for path in sorted(DOCS_DIR.rglob("*.md")):
        if path.relative_to(DOCS_DIR).parts[0] in EXEMPT_DIRS:
            continue
        yield path


def parse_frontmatter(path: Path) -> DocPageFrontmatter:
    """Read and validate one page's YAML header.

    Args:
        path: Absolute path to a markdown page.

    Returns:
        The validated frontmatter model.

    Raises:
        DataValidationError: If the header is missing, is not a YAML mapping, or fails validation.
    """
    match = FRONTMATTER_RE.match(path.read_text(encoding="utf-8"))
    if match is None:
        raise DataValidationError(
            f"{path.relative_to(REPO_ROOT)}: no YAML frontmatter — every page needs "
            "title/summary/updated (see .claude/rules/knowledge-base.md)"
        )
    try:
        raw = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise DataValidationError(
            f"{path.relative_to(REPO_ROOT)}: unparseable frontmatter: {exc}"
        ) from exc
    if not isinstance(raw, dict):
        raise DataValidationError(
            f"{path.relative_to(REPO_ROOT)}: frontmatter is {type(raw).__name__}, "
            "expected a mapping"
        )
    try:
        return DocPageFrontmatter.model_validate(raw)
    except ValidationError as exc:
        missing = ", ".join(str(err["loc"][0]) for err in exc.errors())
        raise DataValidationError(
            f"{path.relative_to(REPO_ROOT)}: invalid frontmatter ({missing})"
        ) from exc


def page_links(path: Path) -> list[str]:
    """Return every relative link target on a page, anchors stripped."""
    targets = []
    for _, target in LINK_RE.findall(path.read_text(encoding="utf-8")):
        if target.startswith(EXTERNAL_LINK_PREFIXES):
            continue
        body = target.split("#", 1)[0]
        if body:
            targets.append(body)
    return targets


def check_links(errors: list[str]) -> dict[Path, set[Path]]:
    """Verify every relative link resolves; return the resolved link graph for orphan detection."""
    graph: dict[Path, set[Path]] = {}
    for page in iter_pages():
        resolved_targets: set[Path] = set()
        for target in page_links(page):
            resolved = (page.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{page.relative_to(REPO_ROOT)}: broken link -> {target}")
                continue
            # a link to `storage/` reaches that folder through its README
            resolved_targets.add(resolved / "README.md" if resolved.is_dir() else resolved)
        graph[page.resolve()] = resolved_targets
    return graph


def check_index_coverage(errors: list[str]) -> None:
    """Every page must be reachable from docs/README.md or from its own folder README."""
    for page in iter_pages():
        if page.name == "README.md":
            continue
        indexes = [DOCS_DIR / "README.md", page.parent / "README.md"]
        listed = any(
            index.exists()
            and page.resolve() in {(index.parent / t).resolve() for t in page_links(index)}
            for index in indexes
        )
        if not listed:
            errors.append(
                f"{page.relative_to(REPO_ROOT)}: not listed in docs/README.md or "
                f"{page.parent.relative_to(REPO_ROOT)}/README.md — run --write-index"
            )


def check_code_references(frontmatter_by_page: FrontmatterByPage, errors: list[str]) -> None:
    """Every ``code:`` path must exist — a page pointing at a deleted module is a broken link."""
    for page, frontmatter in frontmatter_by_page.items():
        for reference in frontmatter.code:
            if not (REPO_ROOT / reference).exists():
                errors.append(f"{page.relative_to(REPO_ROOT)}: code: -> {reference} does not exist")


def check_docstring_budget(errors: list[str]) -> None:
    """Prose in ``src/`` stays within the budget: 5 lines a module, 3 a definition, 1 a constant."""
    for path in sorted(SRC_DIR.rglob("*.py")):
        source = path.read_text(encoding="utf-8")
        if not source.strip():
            continue
        relative = path.relative_to(REPO_ROOT)
        tree = ast.parse(source, filename=str(path))

        nodes: list[tuple[ast.AST, str, int]] = [
            (tree, "module docstring", MODULE_DOCSTRING_MAX_LINES)
        ]
        nodes += [
            (node, f"{node.name}: docstring", DEFINITION_DOCSTRING_MAX_LINES)
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef)
        ]
        for node, label, ceiling in nodes:
            docstring = ast.get_docstring(node, clean=False)
            if docstring is None:
                continue
            length = sum(1 for line in docstring.splitlines() if line.strip())
            if length > ceiling:
                line = getattr(node, "lineno", 1)
                errors.append(f"{relative}:{line}: {label} is {length} lines (max {ceiling})")

        # A run of full-line comments is the one-line constant budget's mechanical form; tokenize
        # rather than scan text, so a ``#`` inside a string is not mistaken for one.
        with path.open("rb") as handle:
            commented = [
                token.start[0]
                for token in tokenize.tokenize(handle.readline)
                if token.type == tokenize.COMMENT
                and token.line.lstrip().startswith("#")
                and not PRAGMA_COMMENT_RE.match(token.string)
            ]
        run_start = None
        for index, line in enumerate(commented):
            if run_start is None:
                run_start = line
            is_last = index == len(commented) - 1
            if is_last or commented[index + 1] != line + 1:
                run_length = line - run_start + 1
                if run_length > 1:
                    errors.append(
                        f"{relative}:{run_start}: comment block is {run_length} lines (max 1)",
                    )
                run_start = None


@cache
def last_commit_date(reference: str) -> date | None:
    """The date of the last commit touching a repo path, or None if git has never seen it."""
    committed = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "log", "-1", "--format=%cs", "--", reference],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    return date.fromisoformat(committed) if committed else None


def report_stale_pages(frontmatter_by_page: FrontmatterByPage) -> None:
    """Warn about pages whose ``code:`` modules moved on after the page was last updated.

    This is what makes ``updated`` a claim rather than a decoration. It is a warning and not an
    error because a commit does not always invalidate the prose — a rename or a comment leaves the
    page true. The comparison is strict, so a page edited in the same commit as the code it
    documents never trips.
    """
    for page, frontmatter in sorted(frontmatter_by_page.items()):
        dated = [
            (commit, reference)
            for reference in frontmatter.code
            if (commit := last_commit_date(reference)) is not None and commit > frontmatter.updated
        ]
        if dated:
            newest_commit, newest_reference = max(dated)
            logger.warning(
                f"stale: {page.relative_to(REPO_ROOT)} (updated {frontmatter.updated}, "
                f"{newest_reference} changed {newest_commit})"
            )


def report_orphans(graph: dict[Path, set[Path]]) -> None:
    """Warn about pages nothing links to — usually a page that never made it into an index."""
    linked = {target for targets in graph.values() for target in targets}
    entry_points = {(DOCS_DIR / "README.md").resolve(), (DOCS_DIR / "GLOSSARY.md").resolve()}
    for page in sorted(graph):
        if page not in linked and page not in entry_points:
            logger.warning(f"orphan (nothing links to it): {page.relative_to(REPO_ROOT)}")


def render_index(index_path: Path) -> str:
    """Build the bullet list of pages an index file is responsible for.

    ``docs/README.md`` indexes the top-level folders; a folder ``README.md`` indexes the pages and
    subfolders directly beneath it.
    """
    lines: list[str] = []
    for child in sorted(index_path.parent.iterdir()):
        if child.name.startswith(".") or child.name in EXEMPT_DIRS:
            continue
        if child.is_dir():
            readme = child / "README.md"
            if readme.exists():
                frontmatter = parse_frontmatter(readme)
                lines.append(
                    f"- [{frontmatter.title}]({child.name}/) — {frontmatter.one_line_summary}"
                )
            else:
                lines.append(f"- [`{child.name}/`]({child.name}/)")
        elif child.suffix == ".md" and child.name != "README.md":
            frontmatter = parse_frontmatter(child)
            lines.append(f"- [{frontmatter.title}]({child.name}) — {frontmatter.one_line_summary}")
    return "\n".join(lines)


def write_indexes() -> int:
    """Regenerate every index block between the start/end markers. Returns files changed."""
    changed = 0
    for index_path in sorted(DOCS_DIR.rglob("README.md")):
        if index_path.relative_to(DOCS_DIR).parts[0] in EXEMPT_DIRS:
            continue
        text = index_path.read_text(encoding="utf-8")
        if INDEX_START not in text or INDEX_END not in text:
            continue
        before, _, rest = text.partition(INDEX_START)
        _, _, after = rest.partition(INDEX_END)
        updated = f"{before}{INDEX_START}\n{render_index(index_path)}\n{INDEX_END}{after}"
        if updated != text:
            index_path.write_text(updated, encoding="utf-8")
            logger.info(f"rewrote index: {index_path.relative_to(REPO_ROOT)}")
            changed += 1
    return changed


def main() -> int:
    """Run the checks (optionally regenerating indexes first) and report. Returns an exit code."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "--write-index",
        action="store_true",
        help="regenerate the index blocks in docs/README.md and each folder README before checking",
    )
    args = parser.parse_args()

    if args.write_index:
        try:
            logger.info(f"regenerated {write_indexes()} index block(s)")
        except DataValidationError as exc:
            logger.error(f"cannot build an index while a page is invalid — {exc}")
            return 1

    errors: list[str] = []
    frontmatter_by_page: FrontmatterByPage = {}
    for page in iter_pages():
        try:
            frontmatter_by_page[page] = parse_frontmatter(page)
        except DataValidationError as exc:
            errors.append(str(exc))

    graph = check_links(errors)
    check_code_references(frontmatter_by_page, errors)
    check_index_coverage(errors)
    check_docstring_budget(errors)
    report_orphans(graph)
    report_stale_pages(frontmatter_by_page)

    page_count = sum(1 for _ in iter_pages())
    module_count = sum(1 for _ in SRC_DIR.rglob("*.py"))
    if errors:
        for error in errors:
            logger.error(error)
        logger.error(
            f"{len(errors)} problem(s) across {page_count} pages and {module_count} modules"
        )
        return 1

    logger.success(f"{page_count} pages and {module_count} modules OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
