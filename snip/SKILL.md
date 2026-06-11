---
description: Save a code/md snippet as a build-in-public bundle — source + freeze PNG + draft post caption — under ~/build-in-public/snippets/, with a disclosure-boundary and secrets check first.
argument-hint: "<file>[:<start>-<end>] [slug] — or just describe the snippet from this session"
allowed-tools: Bash, Read, Write, Edit
---

You are saving a snippet for one of the user's build-in-public X posts.

## Step 1 — Resolve the snippet
- If `$ARGUMENTS` gives a file path (optionally `:<start>-<end>` line range), read exactly that.
- If it describes something from this session ("the freeze command", "that skill file"), extract it from context.
- Pick a kebab-case slug (≤4 words) from `$ARGUMENTS` or the content.

## Step 2 — Safety gate (do this BEFORE writing anything)
- Check the snippet against the project's **public-disclosure-boundary** memory. If the snippet leaks private material, STOP and tell the user what specifically crosses the line.
- Scan for secrets: API keys (`sk-ant`, `sk-`, `AKIA`), tokens, `.env` contents, absolute paths revealing private project structure, emails. Redact with `<REDACTED>` and note it, or stop if redaction would gut the snippet.

## Step 3 — Write the bundle
Create `~/build-in-public/snippets/<YYYY-MM-DD>_<slug>/` (date from your context) containing:
- `snippet.<ext>` — the exact source, original extension.
- `snippet.png` — freeze render. Wrap prose first; use the house style:
  ```
  fold -s -w 80 snippet.<ext> | freeze --config full \
    --theme catppuccin-mocha --language <lang> -o snippet.png
  ```
  If the snippet is >30 lines, ALSO render a `hero.png` of the most interesting ~20 lines and say which lines you chose.
- `post.md` — a draft X post: hook line, 2–4 short lines of substance (what it does + the one non-obvious detail), no hashtag spam. Note the char count and whether it needs Premium long-post. End with a `Status: draft` line.

## Step 4 — Index + open
- Append to `~/build-in-public/snippets/INDEX.md` (create with a `# Snippets` header if missing):
  `- [ ] <YYYY-MM-DD> <slug> — <one-line what it is> (<source file>)`
  (The checkbox tracks posted/not-posted; never check it yourself.)
- `open` the PNG so the user can review, and print the bundle path + draft post.

Keep the caption in the user's voice: builder-casual, concrete numbers and filenames over adjectives, no emoji walls.
