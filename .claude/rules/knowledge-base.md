# Knowledge Base

`docs/` is a living knowledge base of domain-specific ideas, decisions, and mental models that are
not obvious from the code alone. One markdown file per concept, cross-linked, with a map at
`docs/README.md` and generated per-folder indexes.

## When to Read

- **Before starting any feature or fix**, read `docs/README.md` and open the pages relevant to the
  area you're working in. This prevents re-learning what a previous session already figured out.
- `docs/architecture/` mirrors the `src/` package names, so the page you want is usually one
  directory lookup away from the file you're editing.

## When to Create or Update

- **After implementing a feature** that introduces a new domain idea (a data source quirk, a
  pricing model, a business rule, a resolution policy), create a page if one doesn't exist.
- **After changing code** that materially affects an existing page (e.g. switching from one
  algorithm to another), update the page and bump its `updated` date.
- **After discovering a non-obvious "why"** — why a threshold is 0.5, why a record maps to a
  specific category, why fees are quadratic — capture it on the relevant page.
- **Do not create pages for trivial or self-evident things.** If the code speaks for itself, a page
  adds noise. Reserve pages for knowledge that crosses multiple files or that a new session would
  have to re-derive from scratch.

## Where a New Page Goes

Evaluate top to bottom; first match wins. Folders are created on first use.

| Question | Folder |
|---|---|
| Would this still be true if we deleted the repo? | `docs/domain/` |
| Is it a fact about a vendor's API, limits, or cost? | `docs/data/vendors/` |
| Does it describe a stored table's keys/columns/semantics? | `docs/data/tables/` |
| Does it explain why a module in `src/` works the way it does? | `docs/architecture/<src module>/` |
| Is it a dated one-off measurement or analysis? | `docs/experiments/` |
| Is it the project spec, tooling choice, or roadmap? | `docs/project/` |

`docs/plans/` is exempt from every rule here — a plan is a working statement of intent for work
in flight, not maintained knowledge, and it deliberately quotes the paths that are true when it
is written. A plan is deleted once its implementation is fully done (see CLAUDE.md, Planning);
the folder holds only pending and in-flight plans.

## Page Format

Frontmatter is required. `title`, `summary` and `updated` are enforced; extra keys are allowed.
`updated` is the date the page was last **verified against the code**, not merely the date it was
last edited — re-dating a page you reread and found still true is correct and expected.

```markdown
---
title: Vendor Candles (candles_1h / candles_1m)
summary: >
  One standalone sentence — this is what the generated indexes print, so it must read as a
  list item without the title for context.
updated: 2026-08-31
code: [src/vendors/example.py, scripts/ingest_candles.py]   # optional
related: [../vendors/example_vendor_limits.md]              # optional
---

# Concept Title

One-paragraph summary of what this is and why it matters.

## How It Works

Technical detail — formulas, decision logic, data flow. Keep it concise.
Reference source files where the implementation lives.

## Why It's This Way

Design decisions, constraints, trade-offs. The "why" that isn't in the code.

## Related Concepts

- [Other Concept](other_concept.md)
```

## Rules

- **One concept per file.** Name files in `lower_snake_case.md`.
- **Keep files short** — aim for under 80 lines. If a page needs more, split it.
- **Cross-link related concepts** with relative markdown links (`../` across folders). The linter
  verifies every one, so a rename that breaks a link fails loudly.
- **Every folder has a `README.md`** with a one-line intro and a generated index block between
  `<!-- index:start -->` and `<!-- index:end -->`. Prose outside the markers survives regeneration.
- **Don't duplicate code.** Reference file paths and function names; don't paste implementations.
- **Don't duplicate other pages.** If two pages explain the same mechanism, one links to the other.
- **Date non-obvious facts** that may go stale (e.g. "As of April 2026, the upstream API caps
  responses at 1000 records per page").
- **Never edit `docs/project/` unless the user explicitly asks.** The spec and the roadmap are the
  user's own statements of intent, not compiled knowledge. Read them freely; propose changes in
  your reply and let the user make them.
- **No development narrative.** A page describes how things work now and why — never how they used
  to work, what a later session changed, or in which order. Keep the rationale, drop the chronology;
  history lives in `git log`. Two exemptions, and no others: `docs/experiments/` is a dated record
  by design, and `docs/plans/` holds only in-flight plans (deleted on completion).

  A **dated fact** is not narrative and stays: a measurement with its provenance ("measured
  2026-08-11 over 2016-2023 hourly, the charge is 17,529"), a property of the stored data ("every
  pre-2020 snapshot is daily-only"). What goes is the account of a *change* — "until 2026-08-11 the
  fee was flat", "(since 2026-07-29)", "this page used to say". When a change left an artifact a
  reader may still hold — a cache, a published number — state the artifact's property, not the
  change: "a cache built without the parity sort holds one arbitrary draw", never "caches written
  before 2026-08-06 hold one arbitrary draw".
- **Run the linter** after any docs change:

  ```bash
  uv run python -m scripts.check_docs --write-index
  ```

  It regenerates the indexes, then fails on missing/invalid frontmatter, broken relative links,
  a `code:` path that does not exist, and pages absent from an index. Orphan and stale pages are
  reported as warnings.

## Provenance & Decay

A compiled knowledge base rots when it drifts away from the code it describes. One frontmatter key
makes that drift checkable.

- **`code:` — required on every `architecture/` and `data/` page.** List the modules the page
  explains (`code: [src/analytics/example.py, src/analytics/other.py]`; use a YAML block list if
  the flow form passes 100 characters). Pages under `domain/`, `project/` and `experiments/`
  describe things that are true without this repo — they carry no `code:`.
- **A staleness warning is a prompt to reread, not a prompt to re-date.** When the linter reports
  `stale: <page> (updated X, <module> changed Y)`, open the page against the current code. Fix what
  actually drifted, *then* set `updated`. Bulk-bumping dates to silence the warnings converts the
  audit into decoration. A sweep commit that only rewrites docstring paths will trip it — that is
  the cost of a per-file check, and one honest re-verification pass clears it.
