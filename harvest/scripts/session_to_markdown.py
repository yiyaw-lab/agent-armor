#!/usr/bin/env python3
"""Mechanical half of the session-archive routine: convert a Claude Code JSONL
transcript to clean markdown, and report the next session number for a project.

Cross-project. The interpretive half (metadata block, findings, decisions, graded
summary) is done by the model via the /archive-session command.

Usage:
  session_to_markdown.py --project-root /path/to/project [--jsonl PATH] [--title TXT]

Behavior:
  - If --jsonl is omitted, picks the most recently modified *.jsonl under
    ~/.claude/projects/ (the active session is the newest while it's being written).
  - Parses user/assistant messages; skips tool_result blocks and system noise;
    summarizes tool_use as *[ToolName: detail]*.
  - Computes next session NN from <project-root>/private/session_summaries/.
  - Writes the transcript body to <project-root>/private/transcript/<topic-slug
    placeholder> and prints a JSON report the model uses to finish the archive.
"""
from __future__ import annotations
import argparse, glob, json, os, re, sys
from pathlib import Path

PROJECTS = Path.home() / ".claude/projects"


def newest_jsonl() -> Path | None:
    cands = glob.glob(str(PROJECTS / "**" / "*.jsonl"), recursive=True)
    if not cands:
        return None
    return Path(max(cands, key=os.path.getmtime))


def block_text(content) -> str:
    if isinstance(content, str):
        return content
    parts = []
    for b in content:
        if not isinstance(b, dict):
            continue
        t = b.get("type")
        if t == "text":
            parts.append(b.get("text", ""))
        elif t == "tool_use":
            name = b.get("name", "tool")
            inp = b.get("input", {}) or {}
            detail = (inp.get("description") or inp.get("command") or inp.get("file_path")
                      or inp.get("prompt") or inp.get("skill") or inp.get("pattern") or "")
            detail = re.sub(r"\s+", " ", str(detail))[:100]
            parts.append(f"*[{name}: {detail}]*")
        # tool_result and thinking intentionally skipped
    return "\n".join(p for p in parts if p.strip())


def is_noise(text: str) -> bool:
    if not text.strip():
        return True
    s = text.lstrip()
    return (s.startswith("Base directory for this skill")
            or s.startswith("<system-reminder>")
            or s.startswith("Caveat: The messages below")
            or s.startswith("# Building LLM-Powered"))


def parse(jsonl: Path, title: str) -> tuple[str, int]:
    out = [f"# {title}\n"] if title else []
    n = 0
    with open(jsonl) as f:
        for line in f:
            try:
                d = json.loads(line)
            except Exception:
                continue
            if d.get("type") not in ("user", "assistant"):
                continue
            msg = d.get("message", {}) or {}
            role = msg.get("role")
            content = msg.get("content", "")
            if role == "user" and isinstance(content, list) and content and all(
                isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
                continue
            txt = block_text(content).strip()
            if is_noise(txt):
                continue
            if len(txt) > 6000:
                txt = txt[:3000] + f"\n\n*[... {len(txt) - 3000} chars elided ...]*"
            out.append(f"\n## {'User' if role == 'user' else 'Claude'}\n\n{txt}\n")
            n += 1
    return "\n".join(out), n


def next_num(folder: Path, pattern: str) -> int:
    """Highest NNN/NN in folder matching pattern's first capture group, + 1."""
    hi = 0
    if folder.is_dir():
        for p in folder.iterdir():
            m = re.search(pattern, p.name)
            if m:
                hi = max(hi, int(m.group(1)))
    return hi + 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", required=True)
    ap.add_argument("--jsonl", default=None)
    ap.add_argument("--title", default="")
    ap.add_argument("--topic-slug", default="session", help="kebab-case topic for the filename")
    ap.add_argument("--date", required=True, help="YYYY-MM-DD (model passes today's date)")
    args = ap.parse_args()

    root = Path(args.project_root).expanduser()
    proj = root.name
    jsonl = Path(args.jsonl) if args.jsonl else newest_jsonl()
    if not jsonl or not jsonl.exists():
        print(json.dumps({"error": "no jsonl found"})); sys.exit(1)

    priv = root / "private"
    nn = next_num(priv / "session_summaries", r"session-0*(\d+)-summary")
    nn_str = f"{nn:02d}"
    title = args.title or f"{proj.title()} Session {nn_str}"
    body, n_msgs = parse(jsonl, title)

    tdir = priv / "transcript"; tdir.mkdir(parents=True, exist_ok=True)
    tpath = tdir / f"{proj}-session-{nn_str}-{args.topic_slug}-{args.date}.md"
    tpath.write_text(body)

    report = {
        "project": proj,
        "project_root": str(root),
        "session_number": nn_str,
        "jsonl_used": str(jsonl),
        "jsonl_mtime": __import__("datetime").datetime.fromtimestamp(
            os.path.getmtime(jsonl)).isoformat(timespec="seconds"),
        "messages": n_msgs,
        "transcript_path": str(tpath),
        "transcript_kb": tpath.stat().st_size // 1024,
        "next_finding": next_num(priv / "findings", r"Finding_0*(\d+)_"),
        "next_decision": next_num(priv / "decisions", r"Decision_0*(\d+)_"),
        "summary_path": str(priv / "session_summaries" / f"{proj}-session-{nn_str}-summary.md"),
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
