#!/bin/bash
# setup-worktrees.sh — Create git worktrees for MAW agents
#
# Usage: ./setup-worktrees.sh [--sparse] branch1 branch2 ...
# Each branch gets a worktree at ../maw-wt-<N>
#
# Options:
#   --sparse  Use sparse checkout (for large repos >1GB)

set -euo pipefail

SPARSE=false
BRANCHES=()

for arg in "$@"; do
  case "$arg" in
    --sparse) SPARSE=true ;;
    *) BRANCHES+=("$arg") ;;
  esac
done

if [ ${#BRANCHES[@]} -eq 0 ]; then
  echo "Usage: $0 [--sparse] branch1 branch2 ..." >&2
  echo "Example: $0 agent/1-testing agent/2-errors agent/3-types" >&2
  exit 1
fi

REPO_ROOT=$(git rev-parse --show-toplevel)
echo "Creating ${#BRANCHES[@]} worktrees from: $REPO_ROOT"

for i in "${!BRANCHES[@]}"; do
  N=$((i + 1))
  BRANCH="${BRANCHES[$i]}"
  WT_PATH="$REPO_ROOT/../maw-wt-agent-$N"

  if [ -d "$WT_PATH" ]; then
    echo "  Worktree $WT_PATH already exists, skipping"
    continue
  fi

  if $SPARSE; then
    echo "  Creating sparse worktree: $WT_PATH → $BRANCH"
    git worktree add --no-checkout "$WT_PATH" -b "$BRANCH" 2>/dev/null || \
      git worktree add --no-checkout "$WT_PATH" "$BRANCH"
    # Caller should set sparse-checkout paths per agent needs
  else
    echo "  Creating worktree: $WT_PATH → $BRANCH"
    git worktree add "$WT_PATH" -b "$BRANCH" 2>/dev/null || \
      git worktree add "$WT_PATH" "$BRANCH"
  fi
done

echo "Done. Worktrees:"
git worktree list
