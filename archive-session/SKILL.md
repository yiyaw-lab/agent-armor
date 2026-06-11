---
description: Archive the current Claude Code session into the project's private/ folder (transcript + metadata + findings + decisions + graded summary) per the session-archive convention.
argument-hint: "[project-name-or-path] (optional; defaults to the project this session worked on)"
allowed-tools: Bash, Read, Write, Edit
---

You are archiving the session that is ending. Follow the **session-archive-conventions** memory (folder taxonomy, file naming, metadata-block format) exactly. The mechanical half is a script; you do the interpretive half from what you already lived this session — you should NOT need to re-read the whole transcript.

## Step 1 — Identify the target project
- If `$ARGUMENTS` names a project or path, use it. Otherwise infer the project this session actually worked on (the repo you edited files in — which may differ from the launch cwd). If genuinely ambiguous, ask the user once; otherwise proceed.
- Resolve its root (the dir containing `private/`). Confirm `private/` with the taxonomy folders exists; if not, create `private/{transcript,findings,decisions,session_summaries,origin}/`.

## Step 2 — Classify the session
Decide, honestly:
- **Topic slug** — kebab-case, ≤5 words, describing what the session covered.
- **High-signal?** Per the convention, a metadata block + findings + decisions are ONLY for high-signal sessions (origin, major pivot, first benchmark, breakthrough, major failure). Routine sessions (refactors, pushes, small fixes) get a transcript + summary only — no metadata block, no findings/decisions.

## Step 3 — Run the mechanical script
Run (substitute real values; `--date` is today's date from your context):
```
python3 ~/.claude/scripts/session_to_markdown.py \
  --project-root "<ROOT>" --topic-slug "<SLUG>" --date "<YYYY-MM-DD>"
```
It writes the transcript body and prints a JSON report. **Verify `jsonl_used` / `jsonl_mtime` is THIS session** (newest, just-now mtime) — if it picked the wrong file, re-run with `--jsonl <correct path>` (look under `~/.claude/projects/`). Read `session_number`, `next_finding`, `next_decision`, `transcript_path`, `summary_path`, `messages` from the report.

## Step 4 — Interpretive write-up (match the format of the LATEST existing files in each folder)
- **Transcript metadata** (high-signal only): prepend the convention's metadata block (`# Metadata` … Project / Artifact Type / Date / Author: Yiya + Claude Code / Status / Outcome / Key Insight / Decisions / Open Questions / Historical Importance / Related Artifacts) above the `# <title>` line, via Edit on `transcript_path`.
- **Findings** (high-signal only): for each distinct durable learning, write `findings/Finding_<NNN>_PascalCaseTitle.md` starting at `next_finding`. Use the existing findings' structure (`## What Was Learned` / `## Evidence` / `## Implications`). Be specific — real numbers, real file names.
- **Decisions** (high-signal only): for each architectural choice/pivot/commitment, write `decisions/Decision_<NNN>_PascalCaseTitle.md` starting at `next_decision` (`## What Changed` / `## Why` / `## Tradeoffs Accepted`).
- **Session summary** (always): write `summary_path`. Match the latest existing summary: a `# Session Evaluation` block with two graded tables (**User Communication**: Prompt Clarity, Context Provided, Specificity of Intent, Feedback Quality; **Agent Performance**: Output Quality, Alignment to Intent, Depth, Efficiency, Avoided Mistakes), each row Grade + honest Notes; then a **Coach Note (for user)** and **Agent Note**; then `---`; then `# <Project> Session <NN> Summary` with Date, Session (transcript filename), `## What Happened` (bullets, linking Finding_/Decision_ ids), `## Key Output`. Grade candidly — including the agent's own mistakes.

## Step 5 — Public build log (if the project keeps one)
- If the repo has `docs/build-log/`, check whether today's entry exists (`docs/build-log/<YYYY-MM-DD>.md`). If it's missing and real build work happened (check `git log` for the date — scheduler-bot/run-state commits alone don't count), **draft it** in the established voice of the latest entries (theme header, TL;DR, numbered workstreams, honest meta-lessons), covering the day **across all sessions** (yours + what peers' commits/archives show), and add it to the log's README index (newest first).
- The build log is a TRACKED, often public file: no private finding/decision ids, no personal details, nothing from gitignored strategy docs beyond an oblique mention.
- Also glance for **gap days** since the last entry; backfill only days with real work. Commit per the project's git rules (only with standing or explicit authorization; on a branch if the default branch is checked out).

## Step 6 — Index + report
- If `private/README.md` has a Sessions list, add this session's line. If no README exists and the project wants one, create a brief index.
- Update any relevant memory files so the next session loads the FINAL state, not retracted intermediate claims.
- Print a concise report of every file created/updated (paths), and the session number.

Keep each artifact tight and high-signal — these are durable records, not a dump.
