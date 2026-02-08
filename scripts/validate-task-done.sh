#!/bin/bash
# validate-task-done.sh — TaskCompleted hook
#
# Runs when a task is marked complete. Validates basic completion criteria.
# Exit code 2 blocks the completion if validation fails.

# Check if we're in a worktree with uncommitted changes
WORKTREE_PATH="${MAW_WORKTREE:-}"
if [ -n "$WORKTREE_PATH" ] && [ -d "$WORKTREE_PATH" ]; then
  UNCOMMITTED=$(git -C "$WORKTREE_PATH" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  if [ "$UNCOMMITTED" -gt 0 ]; then
    echo "WARNING: $UNCOMMITTED uncommitted files in $WORKTREE_PATH" >&2
    echo "Agent should commit all changes before marking task complete." >&2
    # Don't block — agent may have intentionally left some files
  fi
fi

echo "Task completion validated." >&2
exit 0
