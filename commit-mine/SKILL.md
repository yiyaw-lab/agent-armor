---
description: Commit ONLY this session's work out of a shared dirty tree where parallel agent sessions have uncommitted edits in the same files. Positive hunk selection, staged-snapshot test (checkout-index + suite), and a foreign-symbol check before every commit. Use whenever git status shows modifications you didn't all make.
argument-hint: "[test command] (optional; auto-detected from the repo if omitted)"
allowed-tools: Bash, Read, Write, Edit
---

You are landing this session's changes from a working tree that peer sessions also write to. Two failure modes have actually happened and this procedure exists to prevent both: (1) `git add <file>` swept a peer's unfinished hunks into a commit; (2) a *subtractive* hunk-split (dropping only the peer hunks you knew about) swept an **unknown** peer's hunks into main without their dependencies — dangling references that no test caught, because lazy imports and daemon threads don't fire under unittest.

## Step 0 — Inventory: mine vs theirs, per file
- `git status --short` and `git log --oneline -5` (a peer may have just committed — re-derive, don't assume).
- Build YOUR edit list from what you actually did this session (files you Edited/Wrote). For each modified file, decide: **wholly mine**, **wholly theirs** (touch nothing), or **mixed**.
- For mixed files, `git diff origin/<base> -- <file>` and identify your hunks **positively** — by matching against edits you made — never by subtracting hunks you recognize as someone else's. A peer whose work you haven't seen is exactly the peer you can't subtract.

## Step 1 — Stage
- Wholly-mine files: `git add <path>` (explicit paths, never `-A`/`-a`).
- Mixed files: hand-write a minimal patch containing only your hunks (context lines + your additions; recount the `@@` headers, or split mechanically with `awk '/^@@/{h++} h!=N || /^diff|^index|^---|^\+\+\+/'`), then `git apply --cached <patch>`. The working tree (peers' edits) stays untouched.
- If the repo's default branch is checked out, branch first.

## Step 2 — Prove the STAGED SNAPSHOT stands alone
Run the bundled checker (it exports the index via `checkout-index` and tests THAT, not the working tree):
```
bash ~/claude-code-skills/commit-mine/scripts/staged_check.sh [test command]
```
- A failure here is a staging-dependency gap (you staged a consumer without its provider, or vice versa) — fix the staging, re-run.
- **Known blind spot, check by hand:** the suite can't catch references that only fire at runtime (lazy imports, daemon-thread targets, entrypoint wiring). Grep the staged additions for every symbol/module they call and confirm each is either staged or already in HEAD.

## Step 3 — Foreign-symbol check
The checker also prints all staged added lines. Scan them against your edit list: **any added symbol, import, or comment you don't recognize as yours is a peer's hunk — unstage it** (`git restore --staged <file>` and re-split). Do not rationalize an unfamiliar line as "probably fine."

## Step 4 — Commit in logical stages, then push
- One coherent commit per concern; subject + body explaining why; the repo's trailer conventions.
- Repeat Step 2 per commit when committing in stages.
- On push rejection: `git log <branch>..origin/<branch>`; if disjoint (a bot or peer pushed), `git rebase --autostash origin/<branch>` replays your commits and restores the peers' dirty tree. Never force-push a shared branch.

## Report
List per commit: hash, files, and which were hunk-split. Note anything left intentionally uncommitted (peers' work) so the user knows the tree isn't dirty by accident.
