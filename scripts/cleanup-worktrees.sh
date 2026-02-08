#!/bin/bash
# cleanup-worktrees.sh — Remove all MAW worktrees (idempotent)
#
# Usage: ./cleanup-worktrees.sh [repo-root]
# Removes all ../maw-wt-* worktrees. Safe to run multiple times.

set -uo pipefail

REPO_ROOT="${1:-$(git rev-parse --show-toplevel 2>/dev/null || echo ".")}"
PARENT="$(dirname "$REPO_ROOT")"
FOUND=0
REMOVED=0

for wt in "$PARENT"/maw-wt-*; do
  [ -d "$wt" ] || continue
  FOUND=$((FOUND + 1))

  echo "  Removing worktree: $wt"
  git -C "$REPO_ROOT" worktree remove "$wt" --force 2>/dev/null && \
    REMOVED=$((REMOVED + 1)) || \
    echo "  Warning: could not remove $wt (may need manual cleanup)"
done

# Prune stale worktree references
git -C "$REPO_ROOT" worktree prune 2>/dev/null || true

if [ $FOUND -eq 0 ]; then
  echo "No MAW worktrees found. Nothing to clean up."
else
  echo "Removed $REMOVED/$FOUND worktrees."
fi

exit 0
