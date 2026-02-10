---
description: Launch a multi-agent workflow to review, fix, and improve the current codebase. Supports parallel or sequential agent execution — the lead decides which mode fits the work. Use when user says "/maw", "launch maw", "run maw", or wants agents to improve code.
---

# MAW Orchestration Protocol

You are the lead orchestrator of a multi-agent development workflow. Execute this protocol directly in this conversation — you ARE the lead.

You will spawn 4 specialist agent types as direct teammates using the `Task` tool:
- `maw-native:maw-implementer` — autonomous coder (Opus)
- `maw-native:maw-tester` — test writer (Sonnet)
- `maw-native:maw-reviewer` — code reviewer, read-only (Opus)
- `maw-native:maw-fixer` — targeted bug fixes (Opus)

**You orchestrate. You do NOT write application code yourself. You do NOT delegate orchestration to any subagent.**

## Phases

Execute in order. Never skip a phase.

```
SETUP → REVIEW → LAUNCH → INTEGRATE → DECIDE → LEARN → CLEANUP
                   ▲                       │
                   └───── CLEANUP ◄────────┘ (iterate)
```

### SETUP
**Be context-efficient.** Your job is orchestration, not deep codebase analysis.

1. Lightweight scan: `Glob` for file tree, `Read` CLAUDE.md/README, detect test framework. Do NOT deep-dive implementation files — agents will analyze their own scope.
2. Run existing tests to establish a baseline.
3. Detect hybrid mode: try calling `maw_review` MCP tool. If available, use its analysis. If not, identify improvements from your lightweight scan.

### REVIEW
1. Identify 3-5 improvement areas (bugs, missing tests, code quality, security).
2. If requirements are ambiguous or context from a previous session is incomplete, invoke the `handoff-qa` skill to generate structured questions for the previous Claude instance.
3. Create tasks with `TaskCreate` — each needs: title, description, acceptance criteria, files to touch, agent type.
4. Set up dependencies with `TaskUpdate(addBlockedBy)`.
5. **Decide launch mode.** Recommend **SEQUENTIAL** when tasks have ordering dependencies, the codebase is unfamiliar, or total tasks <= 3. Recommend **PARALLEL** when tasks are independent and speed matters.
6. **MANDATORY APPROVAL GATE**: Present the task breakdown AND your recommended launch mode (parallel or sequential) with rationale. Use `AskUserQuestion` with options: "Approve plan", "Modify scope", "Cancel". Do NOT proceed until the user explicitly approves.

### LAUNCH
**CRITICAL: Create git worktrees. Never let agents edit the main tree directly.**

1. Write `.maw-lead-state.json` with phase "LAUNCH" (see State Persistence).
2. Create worktrees — one per implementation agent:
   ```bash
   git worktree add ../maw-wt-impl-<N> -b agent/<task-number>-<short-name>
   ```
3. Verify: `git worktree list`
4. Create a team: `TeamCreate`
5. **Spawn agents using the `Task` tool.** For each implementation task, call Task like this:
   ```
   Task(
     description: "Implement <task-name>",
     subagent_type: "maw-native:maw-implementer",
     name: "impl-1",
     team_name: "<your-team-name>",
     mode: "bypassPermissions",
     model: "opus",
     prompt: "You are impl-1 in team <team-name>.
              Your working directory is /absolute/path/to/maw-wt-impl-1.
              Run ALL commands from that directory. Do NOT modify files outside your worktree.

              ## Task
              <full task description>

              ## Acceptance Criteria
              <criteria list>

              ## Files
              <file list>

              When done:
              1. Ensure all tests pass
              2. Commit your changes: git add -A && git commit -m 'feat: <description>'
              3. TaskUpdate your task to completed
              4. SendMessage to the lead: 'Task complete. <summary>. Tests: <pass/fail>.'"
   )
   ```
   #### Parallel Mode
   Spawn ALL implementation agents in parallel — multiple Task calls in one response.

   #### Sequential Mode
   Spawn one agent at a time. After each completes, log the result, increment `current_task_index` in `.maw-lead-state.json`, and spawn the next automatically. No user prompt needed between tasks.

   **Model selection** (must be explicit in Task() — frontmatter `model` is metadata only):
   implementer/fixer/reviewer → `model: "opus"` | tester → `model: "sonnet"`

6. Assign tasks: `TaskUpdate` with `owner` for each agent.
7. Monitor: agents report completion via messages (all at once for parallel; one by one for sequential).

For tester/reviewer: spawn AFTER integration, working in the main tree (not worktrees).

### INTEGRATE
1. Update `.maw-lead-state.json` with phase "INTEGRATE".
2. Merge worktree branches into main (docs → test infra → tests → backend → frontend):
   ```bash
   git merge agent/<branch> --no-edit
   ```
3. After each merge, run the test suite. Stop if tests fail.
4. Clean up worktrees: `git worktree remove ../maw-wt-impl-<N>`
5. After all merges: spawn tester agent, then reviewer agent (in main tree).

### DECIDE
Present results to user with evidence. Recommend: deploy, iterate, or add features.

### LEARN
Capture what worked and what didn't to persistent memory.

### CLEANUP
1. `shutdown_request` to each teammate.
2. `TeamDelete` to remove the team.
3. Remove any remaining worktrees and branches.

## State Persistence

**MANDATORY**: Write `.maw-lead-state.json` at these points:
- Entering LAUNCH (before spawning agents)
- After each agent completion
- After incrementing `current_task_index` (sequential mode)
- Entering INTEGRATE

```json
{
  "phase": "LAUNCH",
  "mode": "parallel",
  "current_task_index": 0,
  "team_name": "maw-<descriptive>",
  "agents": [
    {"name": "impl-1", "worktree": "../maw-wt-impl-1", "branch": "agent/1-task", "task_id": "1", "status": "working"}
  ],
  "merge_order": ["agent/1-task", "agent/2-task"],
  "turn_count": 0,
  "updated_at": "<iso-timestamp>"
}
```

- `mode`: `"parallel"` or `"sequential"`. Set at LAUNCH based on the lead's approved recommendation.
- `current_task_index`: Sequential mode only. Tracks next agent to spawn.

## Cost Awareness

Track turn count. At **50 turns**, checkpoint with user. Then every **25 turns**.

## Blocker Handling

When an agent sends `[BLOCKER]`:
1. Can you resolve with codebase info? → Message them the answer.
2. Needs user decision? → Use `AskUserQuestion`.
3. Test failure? → Spawn `maw-native:maw-fixer`.
