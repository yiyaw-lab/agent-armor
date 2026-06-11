---
name: ship
when: Work is done and verified — replaces "commit and push" / "push and merge"
---
Ship the current work: commit with a clean message, push, and {merge_or_pr: merge directly | open a PR}. Then VERIFY the remote actually matches local (don't claim from exit codes) and report: SHAs, branch state, and anything that didn't make it into the commit.
