---
description: Turn credits that would EXPIRE UNUSED at a reset into useful, banked work — the burn-it-forward sibling of /relay. When a session/credit window is about to reset with budget left over, fan out the maximum USEFUL, disk-banked, credit-intensive work as background jobs that survive the boundary, then checkpoint what's running and how to aggregate it after. Honest by construction — never fakes a credit meter, fires only on a real reset signal, launches real artifacts not make-work. Modes: bank (default) | <task-to-front-load> | aggregate.
argument-hint: "[bank (default) | <task-to-front-load> | aggregate]"
---

You are in full-throttle mode. A credit / session window is about to reset with budget LEFT OVER, and unused credit evaporates. Your job is to convert that soon-to-expire budget into the maximum amount of USEFUL, durably-banked work — real results and artifacts, never make-work — launched as background jobs that survive the reset, with a checkpoint so nothing is orphaned on the other side.

full-throttle is the burn-it-forward sibling of /relay. **/relay makes the boundary a clean SEAM** (checkpoint the unfinished work, pause, resume single-flight). **full-throttle SPENDS the credits that would otherwise vanish AT the boundary.** At a real reset you often want both: full-throttle to bank useful compute now, /relay to carry the unfinished checklist across.

## The honest constraint — read first
You CANNOT read the credit / rate-limit meter from inside a session (same hard truth as /relay). So full-throttle NEVER fakes one and NEVER self-triggers. It fires ONLY on a real signal:
- the user says a reset is imminent, gives a "% left" / a timer, or says "use up the credits";
- or a hard limit error is genuinely near (the actual error, not a guess).
No real signal → do not burn. Idle credit is not an emergency, and unprompted fan-out is exactly how a runaway happens.

## What consumes what (the mechanic that makes this work)
Two separate budgets that behave differently at a reset — exploit both:
- **SESSION credits** (the Claude Code subscription / main-loop budget) are consumed by **Workflows and Agents**. To burn session credits, fan out a Workflow with many agents. These run IN-SESSION, so they DIE at the reset — but their per-agent file writes survive on disk (partial-but-banked).
- **Raw-API scripts** (pay-per-token provider keys — Anthropic / OpenAI / xAI) consume a SEPARATE budget and run as **detached OS processes that SURVIVE the reset** and keep computing across it. Use them for work that must COMPLETE across the boundary, for scarce/limited models, and for cross-provider fan-out.

So: **Workflows burn session credits NOW (accept interruption, bank partial); raw-API background scripts bank compute that outlives the reset.** Usually launch some of each.

## Discipline (this IS the skill — break these and you get waste or a runaway)
1. **USEFUL, not make-work.** Every job must produce a real, bankable artifact — a queued experiment, a dataset, a review, drafted content, a backlog item. If you can't name the artifact and who consumes it, don't launch it. Prefer work already scoped or registered (the next experiments, the /nightshift-style backlog, a preprint's open predictions).
2. **Bank to disk incrementally.** Every job writes as it goes (append per-row jsonl; agents `Write` files), so an interrupted job still leaves partial results. Never hold results only in a process that dies at the reset.
3. **Checkpoint for continuity — a STATE file.** Before you stop, write a durable note (e.g. `*_STATE.md`) listing EVERY launched job (task id + output path) and the post-reset plan to aggregate / score each. Banked compute is worthless if the next session can't find and use it. This is full-throttle's version of the /relay brief; pair them.
4. **Don't self-throttle to death.** Concurrent heavy same-provider jobs can trip the account throughput throttle and fail ALL of them. Cap concurrent heavy Anthropic jobs at ~2; spread load across providers; keep each job's internal concurrency modest.
5. **Scarce models get a dedicated, gentle job.** Some models (e.g. Fable) are reachable only via raw API (not Workflow agents), need STREAMING (long extended-thinking non-streamed requests time out), and a MODEST n (low usage limit). Run them isolated so their limit doesn't starve the rest, and don't be surprised by a floor result.
6. **Match the tool to the boundary.** Work that must FINISH across the reset → raw-API detached background. Goal is to spend SESSION credits that would evaporate → Workflows (bank partial). When unsure, launch some of each.
7. **Verify the launch, then stop.** Confirm each job is actually producing rows/files (not silently dead or throttled) before relying on it; then STOP launching. Do not keep firing past the window or without a signal.

## Modes
- **`/full-throttle`** (bare = bank) — survey what is genuinely useful and already queued, launch the maximum useful set of background jobs (Workflows to burn session credits + raw-API scripts to bank durable compute), write the STATE checkpoint, report every job and the aggregation plan, then stop.
- **`/full-throttle <task>`** — front-load a specific named task or experiment to the largest useful scale before the reset.
- **`/full-throttle aggregate`** — post-reset: read the STATE checkpoint, aggregate / score every banked output, and report the results. This is where the burned credits actually pay off — a burn without an aggregate is wasted.

## Where it sits
/relay carries the unfinished WORK across a boundary; /nightshift and /vacation run unattended for a night or days; /until pursues one goal to done. **full-throttle owns the LEFTOVER CREDIT at a boundary** — it turns a reset that would waste budget into one that deposits useful, banked results. Honest by construction: real signal only, real artifacts only, everything on disk, nothing orphaned.
