# MAW Orchestration Protocol

This document contains the detailed workflow rules for the MAW lead agent. It supplements the lead's system prompt with operational procedures that are too detailed to embed directly.

## Phase Transition Rules

### Valid Transitions
```
SETUP   → REVIEW    (always)
REVIEW  → LAUNCH    (after user approves task breakdown)
LAUNCH  → INTEGRATE (when all tasks complete or critical mass reached)
INTEGRATE → DECIDE  (after all merges complete and tests pass)
DECIDE  → LEARN     (always, regardless of decision)
LEARN   → CLEANUP   (always)
CLEANUP → REVIEW    (if iterating)
CLEANUP → [done]    (if deploying or user stops)
```

### Phase Entry Conditions
- **REVIEW**: Must have completed codebase analysis (standalone) or received maw_review output (hybrid).
- **LAUNCH**: User must explicitly approve the task breakdown. Never auto-launch.
- **INTEGRATE**: At least one task must be marked complete. Can proceed with partial completion if user approves.
- **DECIDE**: All merges must be attempted. Test suite must have been run.
- **CLEANUP**: Must run before any new iteration. One team at a time.

## Task Decomposition Heuristics

When analyzing a codebase in standalone mode, look for these categories:

### Bug Detection
- Division by zero, off-by-one errors
- Unhandled None/null checks
- Missing error handling (bare try/except, empty catch blocks)
- Resource leaks (unclosed files, connections)

### Test Gaps
- Files in `src/` with no corresponding `test_` file
- Functions with complexity >5 but no tests
- Missing edge case tests (empty input, boundary values, error paths)

### Code Quality
- Functions >50 lines (decomposition candidates)
- Duplicated code blocks (DRY violations)
- Missing type hints in typed projects
- Inconsistent naming conventions
- TODO/FIXME/HACK comments

### Security
- Hardcoded credentials or secrets
- Missing input validation on user-facing endpoints
- SQL string concatenation (injection risk)
- Unescaped output (XSS risk)

### Task Sizing
- Each task should be completable by one agent in 10-30 turns
- If a task touches >5 files, consider splitting it
- If a task has ambiguous acceptance criteria, clarify before creating it
- Maximum 5 tasks per wave (more causes coordination overhead to outweigh parallelism benefit)

## Merge Order Logic

Always merge in this order to minimize conflicts:

1. **Documentation** — README, docstrings, comments (no code conflicts possible)
2. **Test infrastructure** — conftest.py, fixtures, test utilities (sets up for later merges)
3. **Tests** — test files (may depend on test infra)
4. **Backend/core** — business logic, models, services
5. **Frontend/UI** — templates, views, API endpoints (most likely to conflict with backend)

### Conflict Resolution
- If a merge has conflicts, attempt auto-resolution first:
  ```bash
  git merge agent/branch-name --no-edit
  ```
- If conflicts remain, examine them:
  ```bash
  git diff --name-only --diff-filter=U  # list conflicted files
  ```
- For simple conflicts (both agents added to the same file): resolve by keeping both additions.
- For complex conflicts: notify the user with the conflict details and both sides' intent.

## Check-in Contract

### Agents SHOULD message the lead when:
- Task is complete (mandatory — include evidence)
- Hit a blocker they can't resolve (with `[BLOCKER]` prefix)
- Discover something that affects another task's scope
- Need a design decision not covered in the task description

### Agents SHOULD NOT message the lead when:
- Making progress (no "50% done" updates)
- Making minor implementation choices
- Fixing their own test failures (first attempt)
- Refactoring within their scope

### Lead checks on agents when:
- No message received for >5 minutes during active work
- `TaskList` shows a task stuck in `in_progress` for too long
- Another task is blocked waiting on the silent agent

## Risk Tiering

### Tier 1 — Agent Autonomous (no check-in needed)
- Implementation patterns and code structure
- Variable/function naming
- Refactoring within assigned scope
- Test structure and assertion choices
- Error message wording
- Import ordering, formatting

### Tier 2 — Check with Lead
- Adding a new dependency to the project
- Changing a shared interface (affects other agents' work)
- Modifying files outside the assigned scope
- Creating a new module/package
- Changing database schema

### Tier 3 — Check with User (lead escalates)
- Security/authentication/authorization decisions
- Breaking changes to public APIs
- Architectural pattern choices (when multiple valid options exist)
- Continuing past cost checkpoints
- Deploying or pushing to remote

## Compaction Survival Protocol

Context compaction WILL happen during long workflows. Prepare for it:

### Proactive State Maintenance
Every ~10 turns (or after significant events like task completion), write `.maw-lead-state.json`:

```json
{
  "phase": "LAUNCH",
  "team_name": "maw-quality-wave",
  "target_repo": "/path/to/repo",
  "agents": [
    {
      "name": "impl-1",
      "type": "maw-implementer",
      "worktree": "../maw-wt-agent-1",
      "branch": "agent/1-testing",
      "task_id": "1",
      "status": "working"
    }
  ],
  "merge_order": ["agent/1-testing", "agent/2-errors"],
  "decisions": [
    "Using middleware pattern for auth",
    "Skipped task 4 per user request"
  ],
  "blockers_resolved": [
    "Agent 2 asked about auth pattern → told to use middleware"
  ],
  "turn_count": 35,
  "updated_at": "2026-02-08T15:30:00Z"
}
```

### Post-Compaction Recovery
After compaction, your context will be compressed. Immediately:
1. Read `.maw-lead-state.json` to recover your orchestration state.
2. Call `TaskList` to get current task status (this survives compaction natively).
3. Cross-reference the two: state file has decisions and merge order, TaskList has current agent progress.
4. Resume orchestrating from where you left off.

### What Survives Compaction
- **TaskList**: Always available (managed by Claude Code, not your context)
- **State file**: On disk, read it back
- **Worktrees**: On disk, still there
- **Agent memory**: Persistent, survives everything

### What Does NOT Survive Compaction
- Your mental model of the workflow
- Conversation history with agents
- Decisions you made but didn't write down
- Why you chose a particular merge order

This is why you write state proactively — everything important must be in the file.

## Cost Checkpoint Protocol

Track turn count as a proxy for token spend:

| Checkpoint | Action |
|-----------|--------|
| 50 total turns | Notify user: "Checkpoint: ~50 turns. N/M tasks done. Continue?" |
| 75 turns | Notify + assess: is remaining work worth the cost? |
| Every 25 after | Repeat notification |

Notifications go through two channels:
1. `SendMessage` or `AskUserQuestion` (in the terminal)
2. macOS notification via Bash: `osascript -e 'display notification "..." with title "MAW"'`

If the user says "stop" or "pause", proceed to CLEANUP immediately.

## CLAUDE.md Generation

If the target repo has no CLAUDE.md, generate a minimal one:

```markdown
# CLAUDE.md

## Project Overview
[1-2 sentences based on README or file structure]

## Tech Stack
[Detected languages, frameworks, test runners]

## Build & Test
[Detected commands: pytest, npm test, etc.]

## Key Directories
[src/, tests/, etc.]
```

This helps all agents understand the project context. Don't over-engineer it — just capture the basics.
