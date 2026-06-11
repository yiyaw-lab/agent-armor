# claude-code-skills

Skills and slash commands from my working Claude Code setup. Shared as-is — these run my actual workflow, not a polished library, and I'm not maintaining a community around them.

I'm [yiya](https://yiya.dev) — non-traditional engineer building in public on [X @yiyadev](https://x.com/yiyadev). I work on a few projects — [Synapi](https://synapi.app) is one — but the one I'm most excited about is a company brain + a factory that builds itself. The skills in this repo are working parts of that machine.

## Skills

| Skill | What it does |
|-------|--------------|
| [archive-session](archive-session/) | Archives a Claude Code session into the project's `private/` folder: full transcript, durable findings + decisions docs, and a graded session summary — scoring both my prompting and the agent's performance. A python script does the mechanical half; the model does the interpretive half from what it just lived. |
| [grade-session](grade-session/) | The report card, standalone: two candid graded tables — your prompting and the agent's performance — plus a coach note for each side. No dependencies; prints in chat. |
| [snip](snip/) | Turns any file or snippet into a build-in-public bundle: disclosure-boundary + secrets check first, then a freeze-rendered PNG in my house style, a draft post caption, and a posted/not-posted index. |

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
