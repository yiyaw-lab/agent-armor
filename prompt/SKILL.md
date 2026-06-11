---
description: Personal prompt library + prompt compiler. Save frequently used prompts as parameterized templates, invoke them by name, or refine a draft prompt into a more effective, token-lean version — informed by TASTE.md so the refined prompt asks for what the user will actually accept, not just what they typed. Modes: <name> | save | list | refine.
argument-hint: "<name> [args] | save [name] [text] | list | refine <draft, or 'last'>"
---

The library lives in `~/.claude/prompts/`, one file per prompt: frontmatter (`name`, `when` — one line on when to reach for it) + body = the template, with `{placeholders}` for the parts that vary.

## /prompt <name> [args]
Read `~/.claude/prompts/<name>.md`, fill `{placeholders}` from args and session context, then EXECUTE the template as if the user had typed it in full. Infer missing placeholders from context; ask only if genuinely ambiguous. (This is the token saver: the user types 3 words, the agent runs the 80-word version that actually works.)

## /prompt save [name] [text]
- Source: the given text, or the user's most recent substantive prompt this session.
- Distill to a reusable template: replace session-specific details with `{placeholders}`; KEEP the phrasing that made it effective (constraints, the bar, the verification ask).
- Write the file, report: name, when-to-use, and an invocation example.

## /prompt list
Table: `name | when to use | example invocation`. If the library is empty, say so and point at save/refine.

## /prompt refine <draft | "last">
Compile the prompt for effect-per-token. Diagnose, then rebuild:
1. **Goal, not artifact.** State the outcome wanted, not just the deliverable. (The user's revealed pattern: the real bar arrives as round-2 corrections — front-load it instead.)
2. **Acceptance criteria from TASTE.md.** Read `~/.claude/TASTE.md` ACTIVE rules and bake the relevant ones into the prompt explicitly — e.g. modern design idiom, verified-not-claimed side effects, system-level scope, loose ends closed. This is the difference between what the user types and what they'll accept.
3. **Cut filler.** Pleasantries, hedges, context the agent already has, double-asks.
4. **Structure.** Constraints and output format as terse bullets; one primary ask per prompt.
- Output: **BEFORE** (word count) → **AFTER** (word count), then a 2–3 bullet "what changed and why."
- Rule: the refined prompt must not be longer than the original unless missing acceptance criteria justify the growth — effectiveness first, tokens second. Never pad.
- End by offering `/prompt save <suggested-name>` if the shape looks reusable.

## Rules
- Templates are the user's voice, not corporate prompt-speak — terse, direct, no "please act as."
- Never execute a `refine` result without the user sending it; refine produces text, not action.
- The library is local. Publishing it is a disclosure decision (prompts can leak project strategy).
