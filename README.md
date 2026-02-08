# MAW Native — Multi-Agent Workflow for Claude Code

Orchestrate parallel Claude Code agents with autonomous execution, git worktree isolation, and human-in-the-loop review.

## What It Does

MAW Native coordinates a team of specialized AI agents to improve your codebase in parallel:

1. **Lead** analyzes your codebase and creates a task breakdown
2. You review and approve the plan
3. Lead spawns agents — each working in its own git worktree (no conflicts)
4. Agents implement, test, review, and fix autonomously
5. Lead merges everything back, runs tests, reports results
6. You decide: deploy, iterate, or add more

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

Then tell Claude what to do:

```
> Review this codebase for code quality issues and fix them
> Launch agents to fix the security issues in src/auth/
> Review and improve test coverage for this project
```

### What Happens

1. **SETUP** — Lead checks for CLAUDE.md, detects review mode (standalone vs hybrid)
2. **REVIEW** — Lead analyzes codebase, creates 3-5 tasks, presents to you for approval
3. **LAUNCH** — After you approve: worktrees created, team spawned, tasks assigned
4. **INTEGRATE** — Agents work autonomously → lead merges branches → runs tests
5. **DECIDE** — Lead recommends: deploy, iterate, or add features
6. **LEARN** — Captures learnings to persistent memory

### Sequential Mode

For bandwidth-constrained environments or cost savings:

```
> Review this codebase and work through improvements one at a time
```

### Focused Mode

Target specific areas:

```
> Launch agents to fix the security issues in src/auth/
```

## Agents

| Agent | Role | Model |
|-------|------|-------|
| `maw-lead` | Orchestrator — plans, delegates, integrates | Opus |
| `maw-implementer` | Autonomous coder — implements tasks | Sonnet |
| `maw-tester` | Test writer — validates implementations | Sonnet |
| `maw-reviewer` | Quality gate — reviews code, approves/rejects | Sonnet |
| `maw-fixer` | Bug fixer — handles reviewer change requests | Sonnet |

## Git Worktree Isolation

Each agent works in its own git worktree — a full working copy with its own branch. This means:

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
# Lead reads the recovery output and picks up where it left off
```

## Hybrid Mode

If [maw-mcp](https://github.com/derekparent/maw-mcp) is configured as an MCP server, the lead uses its `maw_review` tool for richer codebase analysis. Otherwise, the lead runs its own analysis (standalone mode). No configuration needed — auto-detected.

## Project Structure

```
maw-native/
├── .claude-plugin/plugin.json    # Plugin manifest
├── agents/                       # 5 agent definitions
├── skills/maw-orchestration/     # Workflow protocol
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
