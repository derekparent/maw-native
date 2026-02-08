# CLAUDE.md — MAW Native Plugin

## What This Is

MAW Native is a Claude Code plugin for multi-agent development workflows. It coordinates parallel agents with git worktree isolation to autonomously improve codebases.

## Key Concepts

- **Lead orchestrates, doesn't implement.** The maw-lead agent plans, delegates, monitors, and integrates. It never writes application code.
- **One team at a time.** Always TeamDelete before creating a new team (CLEANUP phase).
- **Worktree isolation.** Each agent gets `../maw-wt-agent-N` — never works in the main repo directory.
- **User approves before launch.** The lead presents its task breakdown and waits for explicit approval.

## Agent Roster

- `maw-lead` (Opus) — orchestrator
- `maw-implementer` (Sonnet) — autonomous coder
- `maw-tester` (Sonnet) — test writer
- `maw-reviewer` (Sonnet, read-only) — quality gate
- `maw-fixer` (Sonnet) — targeted fixes

## For Detailed Protocol

See `skills/maw-orchestration/SKILL.md` — contains phase definitions, merge order logic, compaction survival protocol, and task decomposition heuristics.

## Scripts

- `scripts/setup-worktrees.sh` — create worktrees (supports `--sparse`)
- `scripts/cleanup-worktrees.sh` — remove worktrees (idempotent)
- `scripts/maw-recover.sh` — detect orphaned worktrees after crash
- `scripts/save-lead-state.sh` — PreCompact hook (validates state file, never writes it)
