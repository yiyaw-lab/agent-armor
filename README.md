# claude-code-skills

Working skills from my Claude Code setup. Every one of them runs my actual day: they have shipped real branches, caught real bugs, and billed real tokens. A skill lands in this repo only after it has survived contact with my own work.

I'm [yiya](https://yiya.dev), a non-traditional engineer building in public on [X @yiyadev](https://x.com/yiyadev). I work on a few projects ([Synapi](https://synapi.app) is one), but the machine I care most about is a company brain plus a factory that builds itself. These skills are its working parts, and the build log for all of them is on X.

The common thread: **agents are cheap, verification is the product.** Most of these skills exist to make an agent prove its work instead of describe it. Pinned done-checks with negative controls. Fresh-context reviewers told to refute, not approve. Measured token economics instead of vibes. Staged-snapshot tests instead of "looks right." The first overnight run of `/nightshift` shipped 6 of 6 tasks at $11.52 per shipped task, and the one defect of the night was caught by exactly this discipline: an agent gamed its own done-check and the adversarial reviewer refused it.

## Skills

| Skill | What it does |
|-------|--------------|
| [nightshift](nightshift/) | The night shift. Call it at bedtime: it builds its own worklist across your active repos (stalled pursuits, breaks, code debt, research questions), executes under an absolute safety contract (branches only, nothing irreversible, nothing outward-facing), double-verifies every task with a pinned binary done-check plus a fresh-context reviewer told to refute it, and leaves a 2-minute morning brief with measured dollars-per-shipped-task economics. |
| [until](until/) | Goal-pursuit engine: pin a verifiable objective, then attempt, verify, adjust until it is done. Negative-control checks so a passing test means something, a hypothesis ledger that forbids re-testing refuted ideas, git checkpoints, and a forced escalation ladder ending in fresh-context subagents. Survives session death via a state file. |
| [commit-mine](commit-mine/) | Commit only this session's work out of a dirty tree that parallel agent sessions are also editing. Positive hunk selection (you can't subtract a peer you haven't seen), a staged-snapshot test that runs the suite against the index rather than the working tree, and a foreign-symbol check before every commit. Ships the checker script. |
| [page-audit](page-audit/) | Audit a local HTML page the trustworthy way: measurements are facts, screenshots are testimony. An instrumented iframe harness reports overflow and element widths per viewport before any screenshot is taken, then modern headless Chrome captures with animations neutralized. Includes a catalogue of headless-rendering artifacts that look like bugs and aren't. |
| [harvest](harvest/) | Milk an ending session for everything durable, so the next run starts richer: full transcript, durable findings/decisions docs, a candid graded report card (both your prompting and the agent's), a build-log entry, and banked memory lessons — then it auto-stages a build-in-public `/card` or `/snip` from the session's most shareable, frontier-builder-relevant gold (disclosure-gated). A python script does the mechanical half; the model does the interpretive half from what it just lived. (Renamed from `archive-session`; folds in `grade-session`.) |
| [grade-session](grade-session/) | The report card, standalone: two candid graded tables (your prompting, the agent's performance) plus a coach note for each side. Straight A's count as failed grading. No dependencies; prints in chat. (Also folded into `/harvest`'s close-out.) |
| [prompt](prompt/) | Prompt library plus compiler: save frequent prompts as parameterized templates, invoke them by name (type 3 words, run the 80-word version), or refine a draft for effect per token by front-loading your acceptance criteria so the bar doesn't arrive as round-2 corrections. Ships with starter templates. |
| [snip](snip/) | Turns any file or snippet into a build-in-public bundle: disclosure-boundary and secrets check first, then a freeze-rendered PNG in my house style, a draft post caption, and a posted/not-posted index. |
| [card](card/) | Stages one insight as a designed, share-ready PNG in a modern product aesthetic (gradient accents, glassy pills, ambient glow), rendered from HTML/CSS via headless Chrome. `/snip` shows source; `/card` stages an idea. |

## Start here

If you take one skill, take `until`: it changes what "done" means for everything else you run. If you take two, add `nightshift`, which runs its tasks as until-style pursuits while you sleep. If your problem is agents stepping on each other in one repo, `commit-mine` is the painkiller.

## Install

Each skill folder has a `SKILL.md` and sometimes a `scripts/` directory.

```sh
# the skill (as a slash command)
cp harvest/SKILL.md ~/.claude/commands/harvest.md

# its script, if it has one
mkdir -p ~/.claude/scripts
cp harvest/scripts/session_to_markdown.py ~/.claude/scripts/
```

Some skills reference my personal conventions: a `private/` folder taxonomy, memory files, a TASTE.md rubric. Those references are the load-bearing part. Swap in your own conventions and the skills get sharper, not weaker; a verification loop tuned to nobody verifies nothing.

These are shared as working parts, not a maintained library. Issues and PRs are welcome, and the contract is honest: this repo updates when my own workflow does.
