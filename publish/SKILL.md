---
description: The closed-loop publisher — turn durable work from a Claude Code session into quality content on the yiya.dev site, PR-gated (nothing auto-ships). Takes a harvested artifact (a finding, a decision, a build-log ship, a graded report card, a scored prediction), runs a disclosure+secrets scan, then a four-part quality gate (Reusable · Non-trivial · Specific · Verified), renders it as the matching yiya.dev content entry against the REAL src/content schemas, and opens a PR to yiyaw-lab/yiyadev (which syncs from GitHub via Lovable/Cloudflare and deploys on merge). A human reviews the PR + preview and merges. Never auto-merges. The public-publishing sibling of the harvest→milk flywheel — it fills the site's guides / notes / code / track-record from real work, so public credibility compounds. Modes: <artifact|path> | sweep | draft.
argument-hint: "<artifact|path> | sweep | draft <artifact|path>  (default: treat the argument as one artifact to publish)"
allowed-tools: Bash, Read, Write, Edit, Grep
---

The law this skill runs on: **the thesis applied to publishing — receipts ship, claims don't, and the human plus the preview are the verification step.** harvest reaps a session into a private archive; the gold inside it dies private unless something carries the *publicly-valuable, verifiable* part to the site. publish is that carrier. It is PR-gated by design: it renders a valid content entry and opens a pull request, and the merge — gated by a human reading the diff and a Cloudflare/Lovable preview building it — is the proof that the entry is real, on-voice, and discloses nothing it shouldn't. Generating the entry is free; the gate is the product.

It is the public-facing sibling of the flywheel: `harvest` extracts durable artifacts into `private/`, `milk` deposits more mid-session, and **publish** sweeps the newest of those and promotes the few that clear the bar onto yiya.dev. It NEVER invents — it only ever publishes a real, dated, verifiable thing that already happened.

## The non-negotiables (every mode obeys these — they are the skill)

- **Disclosure boundary + secrets scan run FIRST, before anything else.** Never publish private strategy, internal IDs, credentials, unshipped plans, taxonomy, or anything the project marks private. Honor the repo's disclosure conventions (`seas` build_log entries are tagged PUBLIC-SAFE for exactly this; `yiyadev/docs/BRAND-BRAIN.md` §5 sets the voice guardrails). **Receipts, not strategy.** If an artifact can't be published without crossing the boundary, redact to the receipt or REJECT it — never soften-and-ship.
- **The four-part gate.** An artifact is publishable only if it is **Reusable** (useful to a frontier builder beyond this one session), **Non-trivial** (the site genuinely lacked it / it isn't obvious), **Specific** (a concrete pattern, number, or dated outcome — not "be better"), and **Verified** (traceable to a real, dated event: a shipped commit, a passing test count, a scored prediction). Reject anything that misses one, *with the reason named*.
- **Voice: claim-free, receipts-over-adjectives, editorial.** Match the site's register (BRAND-BRAIN §5: austere, editorial, no hype, no vanity metrics; the spine line is *"Verification is the product — for code, and for the humans using it."*). The receipts are the live CI / tests / release tags / scored rows — not the adjectives in the copy. No markdown hype, no em-dash-stuffing beyond the house style, no "I used X."
- **PR-gated: open a PR, NEVER merge.** The human + the preview build are the verification step (this is the thesis applied to the act of publishing). No `--auto`, no merge, no direct push to `main`.
- **Track-record rows are sacred: only real, dated, SCORED outcomes.** Never fabricate a row to fill the page. An ungraded prediction is not a track-record row — it waits until reality scores it.

## Schema-awareness (CRITICAL — render against the REAL shapes, or the build fails)

The target repo is `yiyaw-lab/yiyadev` (a Vite + TanStack-Router site; content lives as typed arrays in `src/content/*.ts`, built with `npm run build`, deployed by Lovable/Cloudflare on merge to `main`). **Clone/refresh it and read the exact current shapes before rendering — do not trust this list to be current; the schemas evolve.**

```sh
test -d /tmp/yiyadev || gh repo clone yiyaw-lab/yiyadev /tmp/yiyadev
git -C /tmp/yiyadev pull --ff-only 2>/dev/null
```

The artifact-type → content-file map, with each REAL target schema (verbatim from `src/content/`, 2026-06-22):

- **A hard-won lesson / reusable pattern → a GUIDE** in `src/content/guides.ts`. Editorial prose, claim-free. Schema:
  ```ts
  export type Guide = { title: string; body: string[]; /* paragraphs */ };
  ```
  Render 2–4 tight paragraphs in the voice of the existing guides ("Make your agent prove its work, not describe it.", "Agent spend is rent."). The title is a flat imperative sentence.

- **A shipped, public, tested repo/tool → a CODE repo or a TOOL** in `src/content/code.ts` (the tested code under the systems) or `src/content/tools.ts` (small free builder tools). PUBLIC REPOS ONLY. The receipts live in the `tags` and `href` (live CI/tests/releases), not the note. Schemas:
  ```ts
  export type CodeRepo = { title: string; note: string; href: string; tags: string[]; };
  export type Tool     = { name: string; note: string; get: string; href: string; tags: string[]; };
  ```
  Tags carry verifiable receipts only — `"594 tests"`, `"v0.3.0"`, `"Python"` — never adjectives. A test count or version must be real and current.

- **A scored prediction / a dated SHIP/KILL outcome / a graded bet → a TRACK-RECORD row.** This is the differentiator (BRAND-BRAIN §6: *"here's what I predicted, here's how it graded"* — the verification thesis applied to the author). **As of 2026-06-22 the track-record page is NOT YET BUILT — there is no `src/content/track-record.ts`.** So `/publish` does ONE of two things, and says which:
  1. if `src/content/track-record.ts` exists now (re-check on every run), render a row against its real schema and its integrity rules;
  2. if it does NOT, scaffold the file against the documented spec in `docs/BRAND-BRAIN.md` §6 and propose it in the PR, clearly flagged as introducing the schema (the human decides whether to land the new surface). The proposed shape, matching the existing `src/content/*.ts` typed-array convention and the §6 spec (predicted → scored, dated, calibration-legible):
     ```ts
     export type TrackRecordRow = {
       date: string;        // ISO YYYY-MM-DD the prediction was MADE
       claim: string;       // the falsifiable prediction, as stated then
       verdict: "hit" | "miss" | "partial";
       scoredOn: string;    // ISO date reality scored it
       evidence: string;    // the receipt: a commit, a metric, a link
       source?: string;     // e.g. "SEAS prediction grader", "Rehearse SHIP call"
     };
     export const trackRecord: TrackRecordRow[] = [ /* only real, dated, SCORED rows */ ];
     ```
     INTEGRITY RULE (carry it into the file's header comment): every row is a real prediction made on `date` and scored on `scoredOn` by an outcome you can point to. No retroactive rows, no un-scored rows, no rounding a miss into a partial. The page is worthless the first time it lies.

- **An essay / a durable written note → a NOTE (writing entry)** in `src/content/writing.ts`. Notes/writing on this site ARE the `Essay` array (rendered at `/writing` and `/process/notes`); there is no separate notes store. Schema:
  ```ts
  export type Essay = { title: string; dek: string; category: WritingCategory; date: string; readTime: string; href: string; };
  ```
  `category` MUST be one of the existing `WritingCategory` union members (read the file — e.g. "Founder Notes", "AI & Human Potential"). `date` matches the existing format (`"2026.06"`). `href` is `"#"` only if the piece isn't hosted yet; prefer the real Substack/essay URL.

**Validation = add the entry and build.** The proof that an entry matches the schema is that the typed array still compiles and the site builds:
```sh
cd /tmp/yiyadev && npm ci --silent 2>/dev/null || npm install --silent; npm run build
```
A green build is the receipt that the render is valid. If it fails, the entry is malformed — fix it before opening the PR, never open a red PR.

## /publish &lt;artifact|path&gt;  (default)
Publish ONE artifact end to end.

1. **Resolve the artifact.** `$ARGUMENTS` may be a path to a harvested file (`private/findings/Finding_NNN_*.md`, `private/decisions/Decision_NNN_*.md`, a `private/session_summaries/*-summary.md`, a `private/build_log.md` ship entry), a scored prediction from the prediction store, or a described item. Read it fully (it's about to be published — full read, not a skim).
2. **Disclosure + secrets scan (FIRST, blocking).** Run the project's public-disclosure-boundary check and a secrets scan over the exact text you'd publish. Strip/redact internal IDs, credentials, private strategy/taxonomy, unshipped plans. If what remains isn't a clean receipt, REJECT and say why. (Reuse `/snip`/`/harvest`'s safety gate — same boundary.)
3. **Four-part gate.** Score the artifact on Reusable · Non-trivial · Specific · Verified. If any fails, REJECT with the specific reason; do not "fix" a weak artifact into a strong-sounding one.
4. **Classify → pick the content file + schema.** Map the artifact to guide / code / tool / track-record / note using the map above. Refresh the clone and READ the real current schema from `src/content/<file>.ts` (never render from memory).
5. **Render the entry in-voice.** Produce the typed object matching the schema exactly, in the site's editorial register. Receipts in tags/evidence; claims nowhere. For a track-record row, confirm the outcome is dated + scored, or stop.
6. **Insert + build (the validation).** On a fresh branch `publish/<slug>` in the clone, add the entry to the array (append; match the file's existing formatting and trailing-comma style). Run `npm run build`. Green = valid. Red = fix the entry, re-build; never proceed on a red build.
7. **Open the PR — never merge.** Commit the single content-file change, push the branch, and `gh pr create` against `yiyaw-lab/yiyadev` main. PR body: the entry rendered, the artifact it came from (dated, with its receipt), how the gate scored, and "preview + human review before merge — do not auto-merge." Stop. Report the PR URL and that merge is the human's call.

## /publish sweep
Scan the newest harvest output and PROPOSE the publishable items — don't publish silently.

1. Find the project's `private/` archive (the one this session worked on, or the path given). Read the NEWEST `session_summaries/*-summary.md`, the recent `findings/Finding_*.md`, and the latest `build_log.md` session entry. (Delegate the reading to a subagent so only the candidate list — not the full files — enters main context.)
2. For each candidate, run the disclosure+secrets scan and the four-part gate (steps 2–3 above). Drop anything that fails, with the reason.
3. Classify each survivor to its content file and draft the rendered entry (don't write yet).
4. Present the shortlist: per item — the source artifact (dated + receipt), the target content file + schema, the rendered entry, and the gate verdict. The bar is the same as harvest's gold: *"a frontier builder would find this worth the site."* One excellent entry beats three filler ones.
5. The user picks which to publish; for each chosen, run the default mode's steps 4–7 (insert → build → PR). Never open PRs for un-chosen items.

## /publish draft &lt;artifact|path&gt;
Render the entry but do NOT open a PR — show it and stop. Run steps 1–5 of the default mode (resolve → scan → gate → classify → render), print the exact typed object that would be inserted and the file it targets, and optionally do the local insert + `npm run build` to prove it compiles — but commit nothing, push nothing, open no PR. Use this to eyeball voice/shape before committing to a pull request.

## Rules
- **Nothing auto-ships.** Every mode ends at a PR (or, for `draft`, at a printed entry). No merge, no push to `main`, no `gh pr merge`. The human + the Cloudflare/Lovable preview are the verification step — that is the entire point.
- **Receipts, not strategy.** The disclosure boundary is non-negotiable and runs first. When in doubt, publish less. A leaked internal detail is unrecoverable once the PR is public.
- **Schema-true or it doesn't ship.** Always read the live `src/content/*.ts` schema and prove the entry with a green `npm run build`. A red build never becomes a PR.
- **Track-record honesty.** Only real, dated, SCORED rows. An un-scored prediction waits. Never fabricate, never round a miss up. If the track-record schema doesn't exist yet, scaffold-and-flag it in the PR; don't smuggle a new surface in silently.
- **In-voice or rejected.** Claim-free, editorial, receipts-over-adjectives, matching the existing entries in the target file. If you can't write it in the house voice without a claim, the artifact isn't ready.
- **Honest empty result.** If a sweep finds nothing that clears both the disclosure boundary and the four-part gate, say so and open no PR. A manufactured entry is worse than none — it spends the one credibility a real-receipts site has.
- **One artifact, one entry, one PR.** Keep PRs small and per-entry so the human can review and the preview can isolate. Don't batch unrelated entries into one PR.
