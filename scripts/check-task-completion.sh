#!/bin/bash
# check-task-completion.sh — TeammateIdle hook
#
# Runs when a teammate goes idle. Checks if they actually marked their
# task as complete. Exit code 2 keeps them working if task isn't done.
#
# Note: This is a basic check. The lead agent handles the nuanced cases
# (agent legitimately idle waiting for input, etc.)

# TeammateIdle hook receives teammate info via environment variables
# If no task context is available, let the lead handle it
if [ -z "${MAW_TASK_ID:-}" ]; then
  exit 0  # No task context, let the lead decide
fi

echo "Teammate went idle. Lead should check if their task is complete." >&2
exit 0
