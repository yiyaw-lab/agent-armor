#!/usr/bin/env bash
# Prove the staged snapshot stands alone: export the index with checkout-index,
# run the test suite inside the export, then print every staged added line for
# the foreign-symbol review. Tests the INDEX, never the working tree.
#
# Usage: staged_check.sh [test command...]
#   No args: auto-detects (tests/ + Python -> PYTHONPATH=src unittest discover;
#   package.json with a test script -> npm test).
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

if ! git diff --cached --quiet; then :; else
  echo "staged_check: nothing staged" >&2; exit 2
fi

snap="$(mktemp -d /tmp/stagecheck.XXXXXX)"
trap 'rm -rf "$snap"' EXIT
git checkout-index --prefix="$snap/" -a

if [ "$#" -gt 0 ]; then
  test_cmd=("$@")
elif [ -d "$snap/tests" ] && ls "$snap"/src/*.py >/dev/null 2>&1; then
  test_cmd=(env PYTHONPATH=src python3 -m unittest discover -s tests)
elif [ -f "$snap/package.json" ] && grep -q '"test"' "$snap/package.json"; then
  test_cmd=(npm test --silent)
else
  echo "staged_check: no test command given and none auto-detected" >&2
  test_cmd=()
fi

status=0
if [ "${#test_cmd[@]}" -gt 0 ]; then
  echo "== staged-snapshot test: ${test_cmd[*]} (in $snap)"
  (cd "$snap" && "${test_cmd[@]}") || status=$?
  if [ "$status" -ne 0 ]; then
    echo "== FAILED: the staged snapshot does not stand alone (staging-dependency gap?)" >&2
  else
    echo "== staged snapshot: tests pass standalone"
  fi
fi

echo
echo "== staged ADDED lines (foreign-symbol review: every line must be YOURS)"
git diff --cached | grep '^+' | grep -v '^+++' | sed 's/^+//' | head -200

echo
echo "== reminder: suite can't catch lazy imports / daemon-thread targets —"
echo "==           grep staged additions for symbols they call; each must be staged or in HEAD"
exit "$status"
