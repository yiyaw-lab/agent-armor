# claude-code-skills

Skills and slash commands from my working Claude Code setup. Shared as-is — these run my actual workflow, not a polished library, and I'm not maintaining a community around them.

I'm [yiya](https://yiya.dev) — non-traditional engineer building Synapi, where I benchmark how AI teams should allocate work. I build in public on [X @yiyadev](https://x.com/yiyadev).

## Skills

| Skill | What it does |
|-------|--------------|
| [archive-session](archive-session/) | Archives a Claude Code session into the project's `private/` folder: full transcript, durable findings + decisions docs, and a graded session summary — scoring both my prompting and the agent's performance. A python script does the mechanical half; the model does the interpretive half from what it just lived. |

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
