---
description: Audit a local HTML page's layout and rendering the trustworthy way — measured facts (overflow, element widths) via an instrumented iframe harness, then screenshots via modern headless Chrome with animations neutralized. Use before diagnosing any visual bug, and instead of eyeballing legacy-headless screenshots.
argument-hint: "<path-to-html> [widths, default 390,768,1440]"
allowed-tools: Bash, Read, Write
---

You are auditing a local HTML page. The core rule: **measurements are facts; screenshots are testimony.** Legacy headless Chrome ignores `--window-size`, viewport-relative units (svh/vh) balloon in tall capture windows, and IntersectionObserver reveals race the shutter — screenshots alone produce false bugs and hide real ones. Facts first, pictures second, and never diagnose from a screenshot a measurement contradicts.

## Step 1 — Measure (facts)
Run the bundled harness against the page at each target width (default `390,768,1440`; honor `$ARGUMENTS`):
```
python3 ~/claude-code-skills/page-audit/scripts/measure_page.py <page.html> --widths 390,768,1440
```
It loads the page in fixed-width iframes, waits for layout, and reports per width: `scrollWidth` vs viewport (horizontal overflow = bug), and every element whose bounding rect exceeds the viewport (tag.class, right edge, width). It finds Chrome automatically (`CHROME_BIN` overrides). If the harness errors, fix the invocation — do not fall back to eyeballing.

## Step 2 — Render (pictures, done right)
Only after the measurements, capture visuals with **modern** headless and animations neutralized:
```
"$CHROME" --headless=new --disable-gpu --force-device-scale-factor=1 \
  --force-prefers-reduced-motion --hide-scrollbars \
  --window-size=1440,900 --screenshot=/tmp/audit-desktop.png "file://<abs-path>"
```
Repeat at 390x844 for mobile. For below-the-fold content prefer one tall capture (e.g. 1440x4500) and **remember**: any `svh/vh`-sized section stretches with the capture window — that's an artifact, not a bug. `--force-prefers-reduced-motion` makes pages with reveal animations show everything instantly (if the page handles reduced motion; if sections are still blank, that's a finding about the page's reduced-motion path, not proof of broken layout). Anchor fragments (`page.html#section`) do not reliably scroll in headless — don't use them as evidence of anything.

## Step 3 — Read the screenshots with the Read tool and report
- Lead with the measured verdict (overflow or clean, per width), then visual observations.
- Flag every discrepancy between what a screenshot *suggests* and what the harness *measured* — the measurement wins; say so explicitly.
- If the user reported a visual bug the audit can't reproduce, say "not reproduced under measurement" rather than inventing a cause.

## Known artifact catalogue (check before claiming a bug)
| Symptom in screenshot | Likely artifact |
|---|---|
| Text clipped at right edge, but scrollWidth == viewport | Legacy headless ignored --window-size |
| Giant empty void above/below a hero | svh/vh section scaled to a tall capture window |
| Sections blank/black mid-page | Reveal transitions raced the shutter (use --force-prefers-reduced-motion) |
| Anchor screenshot shows the top of the page | Headless didn't scroll to the fragment |
