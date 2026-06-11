# claude-code-skills

Skills and slash commands from my working Claude Code setup. Shared as-is — these run my actual workflow, not a polished library, and I'm not maintaining a community around them.

I'm [yiya](https://yiya.dev) — non-traditional engineer building in public on [X @yiyadev](https://x.com/yiyadev). I work on a few projects — [Synapi](https://synapi.app) is one — but the one I'm most excited about is a company brain + a factory that builds itself. The skills in this repo are working parts of that machine.

## Skills

| Skill | What it does |
|-------|--------------|
| [archive-session](archive-session/) | Archives a Claude Code session into the project's `private/` folder: full transcript, durable findings + decisions docs, and a graded session summary — scoring both my prompting and the agent's performance. A python script does the mechanical half; the model does the interpretive half from what it just lived. |
| [grade-session](grade-session/) | The report card, standalone: two candid graded tables — your prompting and the agent's performance — plus a coach note for each side. No dependencies; prints in chat. |
| [snip](snip/) | Turns any file or snippet into a build-in-public bundle: disclosure-boundary + secrets check first, then a freeze-rendered PNG in my house style, a draft post caption, and a posted/not-posted index. |
| [until](until/) | Goal-pursuit engine: pin a verifiable objective, then attempt → verify → adjust until it's done. Negative-control checks, a hypothesis ledger that forbids re-testing refuted ideas, git checkpoints, and a forced escalation ladder ending in fresh-context subagents. Survives session death via a state file. |
| [nightshift](nightshift/) | The night shift — call it at bedtime. Builds its own worklist across your active repos (stalled pursuits, breaks, code debt, research questions), executes under an absolute safety contract (branches only, nothing irreversible, nothing outward-facing), double-verifies every task — pinned binary done-check plus a fresh-context reviewer told to refute it — and leaves a 2-minute morning brief with measured $-per-shipped-task economics. |
| [card](card/) | Stages one insight as a designed, share-ready PNG — modern product aesthetic (gradient accents, glassy pills, ambient glow), rendered from HTML/CSS via headless Chrome. /snip shows source; /card stages an idea. |
| [prompt](prompt/) | Prompt library + compiler: save frequent prompts as parameterized templates, invoke them by name (type 3 words, run the 80-word version), or refine a draft for effect-per-token — front-loading your acceptance criteria so the bar doesn't arrive as round-2 corrections. Ships with starter templates. |

## Install

Each skill folder has a `SKILL.md` and sometimes a `scripts/` directory.

```sh
# the skill (as a slash command)
cp archive-session/SKILL.md ~/.claude/commands/archive-session.md

# its script
mkdir -p ~/.claude/scripts
cp archive-session/scripts/session_to_markdown.py ~/.claude/scripts/
```

Skills may reference my personal conventions (folder taxonomies, memory files). Adapt the prompts to your own setup — that's the point.
