# MAW Native — Multi-Agent Workflow for Claude Code

Orchestrate parallel Claude Code agents with autonomous execution, git worktree isolation, and human-in-the-loop review.

## What It Does

MAW Native coordinates a team of specialized AI agents to improve your codebase in parallel:

1. **You** invoke the MAW skill — Claude becomes the lead orchestrator
2. Lead analyzes your codebase and creates a task breakdown
3. You review and approve the plan
4. Lead spawns agents — each working in its own git worktree (no conflicts)
5. Agents implement, test, review, and fix autonomously
6. Lead merges everything back, runs tests, reports results
7. You decide: deploy, iterate, or add more

## Prerequisites

- **Claude Code** v2.1.33 or later
- **Agent teams** enabled:
  ```json
  // ~/.claude/settings.json
  {
    "env": {
      "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
    }
  }
  ```
- **Git** (for worktree support)

## Installation

Clone the plugin:

```bash
git clone git@github.com:derekparent/maw-native.git ~/.claude/plugins/maw-native
```

Or symlink from your projects directory:

```bash
ln -s /path/to/maw-native ~/.claude/plugins/maw-native
```

## Usage

### Full Autonomous Mode (recommended)

```bash
claude --dangerously-skip-permissions --teammate-mode tmux
```

Then invoke the skill:

```
> /maw-native:maw-orchestration
> run maw on this codebase
```

Or with a specific goal:

```
> /maw-native:maw review and fix security issues in src/auth/
```

### What Happens

1. **SETUP** — Lead reads codebase, runs baseline tests
2. **REVIEW** — Lead analyzes and creates 3-5 tasks, presents to you for approval
3. **LAUNCH** — After approval: worktrees created, agents spawned in parallel
4. **INTEGRATE** — Lead merges branches sequentially, runs tests after each
5. **DECIDE** — Lead recommends: deploy, iterate, or add features
6. **LEARN** — Captures learnings to persistent memory
7. **CLEANUP** — Team shutdown, worktree removal

## Architecture

The main Claude instance acts as the lead orchestrator — no separate "lead" subagent. This avoids nested agent spawning limitations. The skill/command loads the orchestration protocol directly into the current session.

## Agents

| Agent | Role | Model |
|-------|------|-------|
| _(main Claude)_ | Orchestrator — plans, delegates, integrates | Opus |
| `maw-implementer` | Autonomous coder — implements tasks | Opus |
| `maw-tester` | Test writer — validates implementations | Opus |
| `maw-reviewer` | Quality gate — reviews code, approves/rejects | Opus |
| `maw-fixer` | Bug fixer — handles reviewer change requests | Opus |

## Git Worktree Isolation

Each implementation agent works in its own git worktree — a full working copy with its own branch:

- Agents can edit the same file in parallel without conflicts
- Tests run independently per worktree
- Lead merges sequentially into main after all work completes
- Clean rollback: just delete the worktree

## Recovery

If a session crashes (laptop sleep, tmux disconnect):

```bash
# Worktrees persist on disk. Check their state:
./scripts/maw-recover.sh

# Start a new Claude Code session and say:
> recover
# Lead reads .maw-lead-state.json and picks up where it left off
```

## Hybrid Mode

If [maw-mcp](https://github.com/derekparent/maw-mcp) is configured as an MCP server, the lead uses its `maw_review` tool for richer codebase analysis. Otherwise, standalone analysis. Auto-detected.

## Project Structure

```
maw-native/
├── .claude-plugin/plugin.json    # Plugin manifest
├── agents/                       # 4 specialist agent definitions
│   ├── maw-implementer.md
│   ├── maw-tester.md
│   ├── maw-reviewer.md
│   └── maw-fixer.md
├── skills/maw-orchestration/     # Primary orchestration protocol
├── skills/maw/                   # Alias skill
├── commands/maw.md               # Command with argument support
├── hooks/hooks.json              # PreCompact state persistence
├── scripts/                      # Worktree management, recovery
├── examples/test-fixture/        # Test project with intentional bugs
├── CLAUDE.md                     # Plugin-level instructions
└── README.md
```

## Cost Awareness

The lead tracks approximate turn count and checkpoints with you:
- At ~50 total turns: "Checkpoint: ~50 turns. N/M tasks done. Continue?"
- Then every ~25 turns

You can always say "stop" or "pause" to end early.
