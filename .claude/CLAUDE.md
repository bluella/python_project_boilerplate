Before starting work:
1. Read `docs/README.md` — the knowledge-base map — and open the pages relevant to the area you're touching. `docs/architecture/` mirrors `src/`, so editing `src/storage/schema.py` starts at `docs/architecture/storage/`.
2. Consult `docs/GLOSSARY.md` for the canonical name of any domain term you use, introduce, or rename — use that spelling, never a synonym.

Planning:

**Every plan lives in `docs/plans/`, never in `~/.claude/plans/`.** `.claude/settings.json` sets
`plansDirectory` to `docs/plans`, so plan mode writes there on its own; a `PreToolUse` hook
(`.claude/hooks/block_external_plans.py`) denies writes to `~/.claude/plans/` as a backstop. Plan
mode is fine to use — just never hand-write a plan outside the repo.

1. Write the plan to `docs/plans/<slug>.md` (kebab-case slug describing the task). If it is long
   enough to have real sections, expand it into a folder `docs/plans/<slug>/` with one numbered
   `.md` per section (`01-context.md`, `02-approach.md`, `03-steps.md`, …) so it reads in order —
   the single file is what plan mode can write, the folder is what a big plan graduates to.
   Plan mode names its file with an auto-generated codename (e.g. `refactored-toasting-river.md`);
   when the plan is approved (or you are told to implement), first `git mv` that codename file to a
   descriptive `docs/plans/<slug>.md` and continue from there. If plan mode left no file at all,
   write the approved plan to `docs/plans/<slug>.md` before implementing.
2. Tell the user the plan is written and where, then stop — do not start implementing.
3. Wait for the user to explicitly say to proceed (they'll read it on their own time, and may edit
   it directly before giving the go-ahead). Re-read the plan before implementing in case it changed.
4. Once the implementation is fully done — coded, tested, and reported — delete the plan (the
   file, or the whole folder for a sectioned plan) as the closing step. `docs/plans/` holds only
   pending and in-flight plans, never completed ones; the folder is gitignored, so deletion is
   permanent — that is intended. Anything from the plan worth keeping (a finding, a "why")
   belongs in `docs/` pages, not in the plan file.

If any instruction you are given conflicts with this repo's conventions, say so explicitly rather
than silently following one and dropping the other.

After making any change:
1. Review the code diff and check if it adheres to code style and guidelines of the project.
2. Review CLAUDE.md and relevant .claude/rules of the project and update them to be accurate given the changes.
3. If the change introduces, alters, or removes a domain concept, update the relevant page under `docs/` and bump its `updated` date (see `rules/knowledge-base.md` for where a new page belongs).
4. If the change adds a new domain term, or a new spelling of an existing one, add or redirect it in `docs/GLOSSARY.md` (move a renamed term into its "Don't use" column — never drop it silently).
5. Run `uv run python -m scripts.check_docs --write-index`. It regenerates the folder indexes and fails on broken links, missing frontmatter, pages absent from an index, and any `src/` docstring or comment over the budget in `rules/documentation.md` (5 lines a module, 3 a definition, 1 a constant).
