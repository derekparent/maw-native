#!/bin/bash
# maw-recover.sh — Detect orphaned MAW worktrees and report their state
#
# Usage: ./maw-recover.sh [repo-root]
# Scans for ../maw-wt-* directories and reports branch state for each.

set -uo pipefail

REPO_ROOT="${1:-$(git rev-parse --show-toplevel 2>/dev/null || echo ".")}"
PARENT="$(dirname "$REPO_ROOT")"
FOUND=0

echo "Scanning for MAW worktrees..."

for wt in "$PARENT"/maw-wt-*; do
  [ -d "$wt" ] || continue
  FOUND=$((FOUND + 1))

  BRANCH=$(git -C "$wt" branch --show-current 2>/dev/null || echo "detached")
  STATUS=$(git -C "$wt" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  COMMITS=$(git -C "$wt" log main..HEAD --oneline 2>/dev/null | wc -l | tr -d ' ')

  echo "  $wt"
  echo "    Branch:      $BRANCH"
  echo "    Uncommitted:  $STATUS files"
  echo "    Commits ahead: $COMMITS"

  if [ "$STATUS" -gt 0 ]; then
    echo "    ⚠ Has uncommitted changes"
  fi
  if [ "$COMMITS" -gt 0 ]; then
    echo "    ✓ Has committed work"
  fi
  echo ""
done

if [ $FOUND -eq 0 ]; then
  echo "No MAW worktrees found."
else
  echo "Found $FOUND worktree(s)."
  echo ""
  echo "Recovery options:"
  echo "  - To continue: start a new MAW session, lead can merge completed branches"
  echo "  - To clean up: ./scripts/cleanup-worktrees.sh"
fi

# Check for stale state file
STATE_FILE="$REPO_ROOT/.maw-lead-state.json"
if [ -f "$STATE_FILE" ]; then
  echo ""
  echo "Found state file: $STATE_FILE"
  echo "  Last modified: $(stat -f '%Sm' "$STATE_FILE" 2>/dev/null || stat -c '%y' "$STATE_FILE" 2>/dev/null)"
  echo "  Size: $(wc -c < "$STATE_FILE" | tr -d ' ') bytes"
  echo "  Lead can re-read this to restore orchestration context."
fi

exit 0
