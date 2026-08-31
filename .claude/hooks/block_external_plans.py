#!/usr/bin/env python3
"""PreToolUse guard: keep plan files inside the repo.

`.claude/settings.json` sets `plansDirectory` to `docs/plans`, which is what normally routes
plan-mode output into the repo. This hook is the backstop for sessions that started before that
setting was read: it denies Write/Edit anywhere under `~/.claude/plans/` and says where to write
instead. Stdlib only and system `python3` — hooks run outside the project venv.
"""

import json
import sys
from pathlib import Path

DENY_REASON = (
    "Project convention (.claude/CLAUDE.md): plans live in docs/plans/ inside the repo, never in "
    "~/.claude/plans/. Write the plan to docs/plans/<slug>.md, or docs/plans/<slug>/0N-section.md "
    "if it is long enough to split into sections."
)


def main() -> None:
    """Emit a PreToolUse deny decision when the target path is under ~/.claude/plans/."""
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return

    file_path = payload.get("tool_input", {}).get("file_path")
    if not file_path:
        return

    plans_dir = Path.home() / ".claude" / "plans"
    if plans_dir in Path(file_path).parents:
        json.dump(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": DENY_REASON,
                },
            },
            sys.stdout,
        )


if __name__ == "__main__":
    main()
