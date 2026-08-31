# Model Delegation (Fable orchestrates, Sonnet executes)

The interactive session runs on Fable (or Opus), acting as **orchestrator, analyst, and author
only**. Mechanical, token-heavy work is delegated to **Sonnet subagents** (Agent tool,
`model: sonnet`, `subagent_type: general-purpose`; use the `Explore` agent for read-only codebase
sweeps). This is a hard rule, not a preference — its purpose is token economy: Sonnet handles
well-specified concrete tasks excellently, so specify them well and hand them off.

## Always delegate to Sonnet subagents (never do inline)

- **Web research**: WebSearch/WebFetch — vendor API docs, library docs, reference hunting.
- **Script and pipeline runs**: ingestion scripts, long analysis runs, `scripts/` entry points, and
  any run whose value is the output/log, not the act of running it.
- **Log and output reading**: digging through long run logs, tracebacks, or verbose tool output to
  extract the relevant lines.
- **Bulk data exploration**: database coverage checks, row counts, sanity queries over stored
  tables when the answer is a handful of numbers.
- **Broad codebase searches**: fan-out greps across many files or naming conventions where only
  the conclusion matters (prefer the `Explore` agent here).

## Never delegate (Fable keeps)

- Writing and editing code in `src/`, `scripts/`, and `tests/` — authorship stays with the
  orchestrator.
- Analysis and study design, parameter choices, interpretation of results, and every
  thesis-level conclusion.
- Writing `docs/` pages, plans, and anything else user-facing.
- Review of what subagents did: a subagent that mutates state (DB writes, file generation) must
  report back what changed — old vs. new values, row counts, file paths; the orchestrator reviews
  that report before treating the step as done.

## Subagent prompt requirements

- Name exact paths, symbols, tables, and the expected return format; state that the
  final message is the raw data deliverable, not a human-facing summary.
- Restate the project constraints the task touches (`uv run` for execution, polars-not-pandas,
  naive-UTC datetimes) — don't assume the subagent infers them.
- Fan out independent gathering tasks as parallel subagents in one message.
- Quick inline runs are still fine when iterating tightly on code you just edited (e.g. one
  focused pytest invocation whose output you need to act on immediately); delegate as soon as the
  run is long, output-heavy, or standalone.
