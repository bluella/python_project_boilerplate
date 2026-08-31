# Communication

## Always Answer in English

**Reply and reason in English no matter what language the user writes in.** The user frequently
dictates in Russian because it is faster to speak — that is an input convenience, not a request to
switch the answer's language.

- **Never mirror the user's language.** A Russian prompt gets an English answer. No preamble asking
  which language to use, no apology for not matching, no bilingual duplication.
- **Reason in English too** — visible thinking, plans, and scratch notes, not just the final reply.
- **Everything written to disk is English**: code, comments, docstrings, `docs/` pages, plans under
  `docs/plans/`, and commit messages.
- **Don't translate domain terms.** Resolve a Russian paraphrase back to the canonical spelling in
  `docs/GLOSSARY.md` — never invent a new synonym for a term the glossary already names.

**The one exception** is text the user explicitly asks to be produced in another language (a
translation, a Russian-language message they intend to send). Then the requested language applies
to that deliverable only; the surrounding explanation stays English.

## Why

The vocabulary of this project is English-native — tool names, column names, and every entry in
`docs/GLOSSARY.md` — and round-tripping it through Russian invents near-miss synonyms that the
glossary exists to prevent. English answers also paste straight into code, commits, and docs
without a translation pass.
