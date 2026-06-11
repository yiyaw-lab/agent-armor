---
description: Grade the session that's ending — two candid report cards (the user's prompting, the agent's performance) plus a coach note for each side. Prints in chat; optionally saves to a file.
argument-hint: "[output-path] (optional; prints to chat by default)"
allowed-tools: Read, Write
---

You are grading the session that is ending, from what you lived — do NOT re-read the transcript.

## The grades
Two tables. Each row: Dimension | Grade (A–F, +/− allowed) | Notes (one candid sentence, specific to THIS session).

**User Communication**
- Prompt Clarity — could you act on first read, or did you have to guess?
- Context Provided — did they give what you needed, or did you have to dig?
- Specificity of Intent — did asks state the goal, or just an artifact?
- Feedback Quality — when correcting you, did they say what was wrong and why?

**Agent Performance** (grading yourself — be harder here than on the user)
- Output Quality — correct, complete, idiomatic?
- Alignment to Intent — built what was meant, not just what was said?
- Depth — surfaced non-obvious considerations, or stayed shallow?
- Efficiency — wasted turns, redundant work, questions you could have answered yourself?
- Avoided Mistakes — count them honestly, including ones the user never noticed.

## The notes
- **Coach Note (for user)** — 2–3 sentences: the single highest-leverage change to how they prompt and steer, grounded in a real moment from this session.
- **Agent Note** — what you'd do differently next session; name your own errors plainly.

## Rules
- Grade candidly. A report card of straight A's is a failed grading.
- Evidence over vibes: every grade must be justifiable by a specific moment from the session.
- If `$ARGUMENTS` gives a path, also save the full report there; otherwise just print it.
