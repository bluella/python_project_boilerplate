# Domain Concepts

The `.claude/concepts/` directory is a living knowledge base of domain-specific ideas, decisions,
and mental models that are not obvious from the code alone. One markdown file per concept,
cross-linked, optionally organized into topic subdirectories, with a flat index at
`concepts/INDEX.md`.

## When to Read Concepts

- **Before starting any feature or fix**, read `concepts/INDEX.md` and open any concept files
  relevant to the area you're working in. This prevents re-learning what a previous session
  already figured out.

## When to Create or Update Concepts

- **After implementing a feature** that introduces a new domain idea (a data source quirk, a
  pricing model, a business rule, a resolution policy), create a concept file if one doesn't
  exist.
- **After changing code** that materially affects an existing concept (e.g., switching from one
  algorithm to another), update the concept file to match.
- **After discovering a non-obvious "why"** — why a threshold is 0.5, why a record maps to a
  specific category, why fees are quadratic — capture it in the relevant concept file.
- **Do not create concept files for trivial or self-evident things.** If the code speaks for
  itself, a concept file adds noise. Reserve concepts for knowledge that crosses multiple files
  or that a new session would have to re-derive from scratch.

## Concept File Format

```markdown
# Concept Title

One-paragraph summary of what this concept is and why it matters.

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
- **Group related concepts** in topic subdirectories (e.g., `data/`, `pipeline/`, `domain/`)
  once you have more than a few files. Keep the structure flat until categories are obvious.
- **Keep files short** — aim for under 80 lines. If a concept needs more, split it.
- **Cross-link related concepts** with relative markdown links (use `../` for cross-directory).
- **Update `INDEX.md`** whenever you add, rename, or remove a concept file. One line per entry.
- **Don't duplicate code.** Reference file paths and function names; don't paste implementations.
- **Date non-obvious facts** that may go stale (e.g., "As of April 2026, the upstream API caps
  responses at 1000 records per page").
