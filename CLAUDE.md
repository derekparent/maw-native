# CLAUDE.md — MAW Native Plugin

## What This Is

MAW Native is a Claude Code plugin for multi-agent development workflows. It coordinates agents (parallel or sequential) with git worktree isolation to autonomously improve codebases.

## Architecture

The **main Claude instance** acts as the lead orchestrator when a MAW skill or command is invoked. It spawns specialist agents as direct teammates — there is no separate "lead" subagent. This avoids nested agent spawning issues.

## Key Concepts

- **Main Claude = Lead.** The skill/command loads orchestration logic into the current session. No delegation.
- **One team at a time.** Always TeamDelete before creating a new team (CLEANUP phase).
- **Worktree isolation.** Each implementation agent gets `../maw-wt-impl-N` — never works in the main repo directly.
- **Lead decides parallel vs sequential.** Based on task analysis, the lead recommends a mode and presents it at the approval gate.
- **User approves before launch.** The lead presents its task breakdown and waits for explicit approval.
- **State persistence.** Lead writes `.maw-lead-state.json` at phase transitions for compaction survival. Includes `mode` and `current_task_index` for sequential tracking.

## Agent Roster

| Agent | Role | Model | Spawned via |
|-------|------|-------|-------------|
| _(main Claude)_ | Orchestrator — plans, delegates, integrates | Opus | skill/command invocation |
| `maw-implementer` | Autonomous coder | Opus | `Task(subagent_type: "maw-native:maw-implementer")` |
| `maw-tester` | Test writer | Sonnet | `Task(subagent_type: "maw-native:maw-tester")` |
| `maw-reviewer` | Quality gate (read-only) | Opus | `Task(subagent_type: "maw-native:maw-reviewer")` |
| `maw-fixer` | Targeted fixes | Opus | `Task(subagent_type: "maw-native:maw-fixer")` |

## Entry Points

- `/maw-native:maw-orchestration` — primary skill (recommended)
- `/maw-native:maw` — alias skill
- `/maw-native:maw <goal>` — command with argument

## For Detailed Protocol

See `skills/maw-orchestration/SKILL.md` — contains phase definitions, merge order logic, compaction survival protocol, Task spawn syntax, and cost checkpoints.

## Scripts

- `scripts/setup-worktrees.sh` — create worktrees (supports `--sparse`)
- `scripts/cleanup-worktrees.sh` — remove worktrees (idempotent)
- `scripts/maw-recover.sh` — detect orphaned worktrees after crash
- `scripts/save-lead-state.sh` — PreCompact hook (validates state file)
