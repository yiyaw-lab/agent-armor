#!/usr/bin/env python3
"""Measure a local HTML page's layout facts via an instrumented iframe harness.

For each requested width, loads the page in a fixed-width iframe (so media
queries apply per width), waits for layout + late reveals, then reports the
document scrollWidth and every element whose bounding rect exceeds the
viewport. Output is JSON on stdout. Stdlib only; needs a Chrome/Chromium binary.

Usage:
  python3 measure_page.py path/to/page.html --widths 390,768,1440
  CHROME_BIN=/path/to/chrome python3 measure_page.py page.html
"""

import argparse
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

CHROME_CANDIDATES = [
    os.environ.get("CHROME_BIN", ""),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
]

WRAPPER = """<!doctype html><html><body>
<iframe id="f" src="{page_url}" style="width:{width}px;height:900px;border:0"></iframe>
<pre id="out"></pre>
<script>
document.getElementById('f').onload = function() {{
  setTimeout(function() {{
    var d = document.getElementById('f').contentDocument;
    var vw = {width};
    var bad = Array.prototype.slice.call(d.querySelectorAll('*'))
      .map(function(e) {{
        var r = e.getBoundingClientRect();
        var cls = (e.className && typeof e.className === 'string')
          ? '.' + e.className.trim().split(/\\s+/)[0] : '';
        return {{ n: e.tagName + cls, right: Math.round(r.right),
                 w: Math.round(r.width) }};
      }})
      .filter(function(x) {{ return x.right > vw + 2; }})
      .slice(0, 20);
    document.getElementById('out').textContent = JSON.stringify({{
      width: vw,
      scrollWidth: d.documentElement.scrollWidth,
      overflow: d.documentElement.scrollWidth > vw,
      offenders: bad
    }});
  }}, 1800);
}};
</script></body></html>"""


def find_chrome():
    for c in CHROME_CANDIDATES:
        if c and pathlib.Path(c).exists():
            return c
    sys.exit("error: no Chrome/Chromium found; set CHROME_BIN")


def measure(chrome, page_url, width):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(WRAPPER.format(page_url=page_url, width=width))
        wrapper = f.name
    try:
        out = subprocess.run(
            [chrome, "--headless", "--disable-gpu",
             "--allow-file-access-from-files", "--virtual-time-budget=5000",
             "--dump-dom", f"file://{wrapper}"],
            capture_output=True, text=True, timeout=60).stdout
    finally:
        os.unlink(wrapper)
    m = re.search(r'<pre id="out">(.*?)</pre>', out, re.DOTALL)
    if not m or not m.group(1).strip():
        return {"width": width, "error": "harness produced no measurement "
                "(page JS error, or virtual time too short)"}
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return {"width": width, "error": "unparseable harness output",
                "raw": m.group(1)[:300]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("--widths", default="390,768,1440")
    args = ap.parse_args()
    page = pathlib.Path(args.page).resolve()
    if not page.exists():
        sys.exit(f"error: {page} not found")
    chrome = find_chrome()
    widths = [int(w) for w in args.widths.split(",") if w.strip()]
    report = {"page": str(page),
              "results": [measure(chrome, page.as_uri(), w) for w in widths]}
    report["verdict"] = ("OVERFLOW at " + ", ".join(
        str(r["width"]) for r in report["results"] if r.get("overflow"))
        if any(r.get("overflow") for r in report["results"]) else "clean")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
