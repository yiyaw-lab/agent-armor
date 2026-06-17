---
description: Harvest the session that's ending — milk every durable asset (transcript + findings + decisions + a candid graded report card + build-log + memory) so the next run starts richer. Renamed from /archive-session; folds in /grade-session's grade.
argument-hint: "[project-name-or-path] (optional; defaults to the project this session worked on)"
allowed-tools: Bash, Read, Write, Edit
---

You are HARVESTING the session that is ending: extract every durable asset so nothing valuable is lost and the next run starts richer (don't just store it — milk it). Follow the **session-archive-conventions** memory (folder taxonomy, file naming, metadata-block format) exactly. The mechanical half is a script; you do the interpretive half from what you already lived this session — you should NOT need to re-read the whole transcript.

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
- **Concurrent-run guard:** if another session is archiving in parallel, you can collide on session/finding/decision numbers (and the non-slug `-summary.md` name can clobber). If you see a peer's just-created session-N files, do NOT ping-pong-renumber: adopt the peer's declared numbering once, take a clearly-separate block (yours = the next free session number + a finding/decision block above theirs), verify no duplicate numbers, and stop. (See memory: parallel-agent-sessions.)

## Step 4 — Interpretive write-up (match the format of the LATEST existing files in each folder)
- **Transcript metadata** (high-signal only): prepend the convention's metadata block (`# Metadata` … Project / Artifact Type / Date / Author: Yiya + Claude Code / Status / Outcome / Key Insight / Decisions / Open Questions / Historical Importance / Related Artifacts) above the `# <title>` line, via Edit on `transcript_path`.
- **Findings** (high-signal only): for each distinct durable learning, write `findings/Finding_<NNN>_PascalCaseTitle.md` starting at `next_finding`. Use the existing findings' structure (`## What Was Learned` / `## Evidence` / `## Implications`). Be specific — real numbers, real file names.
- **Decisions** (high-signal only): for each architectural choice/pivot/commitment, write `decisions/Decision_<NNN>_PascalCaseTitle.md` starting at `next_decision` (`## What Changed` / `## Why` / `## Tradeoffs Accepted`).
- **Session summary** (always): write `summary_path`. Open with the `# Session Evaluation` block from Step 5 (the two graded tables + Coach/Agent notes); then `---`; then `# <Project> Session <NN> Summary` with Date, Session (transcript filename), `## What Happened` (bullets, linking Finding_/Decision_ ids), `## Key Output`.

## Step 5 — Grade candidly (the /grade-session half) — write it into the summary AND print it in chat
Grade from what you lived (do NOT re-read the transcript). Two tables; each row: Dimension | Grade (A–F, +/− allowed) | one candid sentence specific to THIS session.
- **User Communication** — Prompt Clarity (could you act on first read, or guess?) · Context Provided (gave what you needed, or you had to dig?) · Specificity of Intent (stated the goal, or just an artifact?) · Feedback Quality (when correcting you, said what was wrong AND why?).
- **Agent Performance** (be harder on yourself than on the user) — Output Quality (correct/complete/idiomatic?) · Alignment to Intent (built what was MEANT, not just said?) · Depth (surfaced non-obvious considerations, or shallow?) · Efficiency (wasted turns, redundant work, questions you could've answered yourself?) · Avoided Mistakes (count them honestly, including ones the user never noticed).
- **Coach Note (for user)** — 2–3 sentences: the single highest-leverage change to how they prompt and steer, grounded in a real moment from this session.
- **Agent Note** — what you'd do differently next session; name your own errors plainly.
Rules: grade candidly — a report card of straight A's is a failed grading; every grade must be justifiable by a specific moment. This block goes into the summary file (Step 4) AND is **printed in chat** at the end so the user sees the grade without opening the file.

## Step 6 — Build log (always)
- Append a session entry to `<ROOT>/private/build_log.md` (create with `# <Project> — Build Log` + `---` if missing). Match the established entry format: `## <YYYY-MM-DD> — Session <NN>: <Topic>` · bold **Duration / Stack / Spend** lines (only what you actually know — never invent numbers) · `### Built` (concrete artifacts) · `### Key decisions` · `### Lessons` (hard-won only).
- Register: PUBLIC-SAFE. This file is the source the public build-log page is distilled from — apply the project's disclosure-boundary memory while writing, not later (claims stated, private methodology omitted).

## Step 7 — Publish the gold (auto build-in-public asset)
The internal archive captures value; this step EXTRACTS the publicly-valuable part. From everything harvested, pick the strongest 1–3 items that (a) are genuinely useful to frontier builders and (b) build the user's credibility/competence — a counterintuitive stat, a hard-won lesson, or a clean reusable pattern. For each, produce ONE share-ready asset:
- **Gold is a STAT or INSIGHT** (a number that lands, a surprising finding) → make a **/card** (follow the /card skill exactly: ≤45 words, number-as-hero, the modern house aesthetic, render at 2x, and LOOK at the PNG before finishing).
- **Gold is CODE** (a clean, novel, reusable pattern) → make a **/snip** (follow the /snip skill exactly: exact source + freeze PNG, with the disclosure-boundary + secrets safety gate run FIRST; render a hero.png too if >30 lines).
Bundle each under `~/build-in-public/snippets/<YYYY-MM-DD>_<slug>/` with a draft `post.md` (`Status: draft`), append its `- [ ]` line to `~/build-in-public/snippets/INDEX.md`, and `open` the render.
- **Bar:** "a frontier builder would repost this." Don't pad — one excellent asset beats three mediocre ones. ONE idea per card/snip.
- **SAFETY (mandatory, before writing):** run the project's public-disclosure-boundary check + a secrets scan. Never publish private strategy/taxonomy/credentials; redact (`<REDACTED>`) or skip if it would cross the line. Nothing auto-posts — these are drafts for the user to publish.

## Step 8 — Index, memory, report
- If `private/README.md` has a Sessions list, add this session's line. If no README exists and the project wants one, create a brief index.
- Update any relevant memory files so the next session loads the FINAL state, not retracted intermediate claims — and bank at least one concrete self-lesson from this session (the reflection ritual) so the same mistake never recurs.
- Print a concise report of every file created/updated (paths), the session number, the graded report card from Step 5, AND the build-in-public asset(s) from Step 7.

Keep each artifact tight and high-signal — these are durable records, not a dump.
