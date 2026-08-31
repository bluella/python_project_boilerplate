---
title: Knowledge Base
summary: >
  The map of everything this project knows: domain truth, data and vendor facts, code
  architecture, dated experiment results, and the project spec.
updated: 2026-08-31
---

# Knowledge Base

Everything this project knows that is not obvious from the code alone. **Read this page first**,
then open the folders relevant to what you are touching.

For the canonical spelling of any domain term, see [GLOSSARY.md](GLOSSARY.md) — use that spelling,
never a synonym, and add or redirect a term there whenever you introduce or rename one.

## How this is organized

Pages are filed by **what kind of truth they hold**, so that a task maps to a folder. Evaluate top
to bottom; first match wins. Folders are created on first use.

| If the page… | It lives in |
|---|---|
| would still be true if we deleted the repo | `domain/` |
| is a fact about a vendor's API, limits, or cost | `data/vendors/` |
| describes a stored table's keys, columns, or semantics | `data/tables/` |
| explains why a module in `src/` works the way it does | `architecture/<src module>/` |
| is a dated one-off measurement or analysis | `experiments/` |
| is the project spec, tooling choice, or roadmap | `project/` |

`architecture/` mirrors the `src/` package names, so editing `src/storage/schema.py` points at
`architecture/storage/`. Every folder has a `README.md` listing its pages; those lists are
generated from page frontmatter by `uv run python -m scripts.check_docs --write-index`, which also
fails on broken links, missing frontmatter, and pages absent from an index.

## Sections

<!-- index:start -->
- [Glossary](GLOSSARY.md) — The canonical spelling for every domain term in this project.
- [Module Flow Chart](module_flow_chart.md) — How the modules fit together — placeholder, to be filled in as the project takes shape.
<!-- index:end -->

`plans/` holds per-task implementation plans and is exempt from the conventions above — a plan is a
dated record of intent, not maintained knowledge.

`project/` holds the spec and the roadmap — statements of intent rather than compiled knowledge.
Agents read it and propose changes in conversation; they do not edit it unless asked.

## Conventions

- **One concept per file**, `lower_snake_case.md`, under 80 lines. If it needs more, split it.
- **Frontmatter is required**: `title`, `summary` (one standalone sentence — it is what the indexes
  print), `updated` (`YYYY-MM-DD`, naive UTC — the date the page was last *verified against the
  code*, not merely edited). `related` is optional.
- **`code:` lists the modules a page explains** and is expected on every `architecture/` and
  `data/` page. The linter fails if a listed path does not exist, and warns when one was committed
  after the page's `updated` date — that warning is the prompt to reread the page, then either fix
  it or re-date it.
- **Cross-link liberally** with relative markdown links; the linter verifies every one.
- **Date non-obvious facts that may go stale** (e.g. "As of April 2026, the upstream API caps
  responses at 1000 records per page").
- **Don't duplicate code** — reference file paths and function names instead.

Full rules: [`.claude/rules/knowledge-base.md`](../.claude/rules/knowledge-base.md).
