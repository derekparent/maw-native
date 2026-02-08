#!/bin/bash
# save-lead-state.sh — PreCompact hook
#
# Validates that .maw-lead-state.json exists and is recent.
# The lead agent proactively maintains this file every ~10 turns.
# This hook does NOT write or overwrite the file — it only validates.

STATE_FILE=".maw-lead-state.json"

if [ ! -f "$STATE_FILE" ]; then
  echo "WARNING: .maw-lead-state.json not found. Lead should create it before compaction." >&2
  echo "After compaction, use TaskList to reconstruct workflow state." >&2
  exit 0  # Don't block compaction
fi

# Check if state file is stale (>30 min old)
if [ "$(uname)" = "Darwin" ]; then
  AGE=$(( $(date +%s) - $(stat -f %m "$STATE_FILE") ))
else
  AGE=$(( $(date +%s) - $(stat -c %Y "$STATE_FILE") ))
fi

if [ "$AGE" -gt 1800 ]; then
  echo "WARNING: State file is $(( AGE / 60 ))min old. May be stale." >&2
fi

echo "State file exists ($(wc -c < "$STATE_FILE" | tr -d ' ') bytes, ${AGE}s old). Compaction safe." >&2
exit 0
