---
name: teamwork-preview
description: "Orchestrates a dynamic team of specialized subagents (coordinator + domain specialists + independent verifier/critic) to plan, implement, and quality-check complex tasks in parallel, modeled after Google Antigravity /teamwork-preview. MANUAL-ONLY: use only when the user explicitly invokes /teamwork-preview, /prompt-toolkit:teamwork-preview, or $teamwork-preview, or asks to use the prompt-toolkit teamwork-preview skill."
disable-model-invocation: true
---

# Teamwork Preview

Act as a Coordinator / Hiring Manager that designs and runs specialized Agent Teams
for complex work. Inspired by Google Antigravity Agent Teams (`/teamwork-preview`).

This plugin skill is the Team Sheet workflow below. It does not replace or impersonate
Antigravity's native `/teamwork-preview` command. If that native controller already
owns the session, reuse it and apply this workflow as the team's operating plan;
never start a second team.

Read [`references/example-teams.md`](references/example-teams.md) before designing
roles. Adapt those sheets; do not copy them blindly.

## When to Use

Activate only when:
- Task has clear parallelizable workstreams or multiple domains of expertise
- Single-agent context would bloat or quality would suffer without independent verification
- User explicitly asks for teamwork, agent teams, multi-agent, or /teamwork-preview style process

If the task is simple, say so and handle it normally. Never force a team on trivial work.

## Core Workflow

### 1. Assess & Decompose
- Restate the high-level goal in one sentence.
- Break into independent or loosely-coupled workstreams.
- Identify required expertise, dependencies, risks, and success criteria.
- Decide the minimal sufficient team size (prefer 3–6 specialists total).

### 2. Design the Team Sheet (Artifact)
Produce a clean Markdown Team Sheet containing:

**Goal summary**

**Roles table** (use this exact structure):

| Role | Specialty | Owns | Inputs | Outputs | Success Criteria |
|------|-----------|------|--------|---------|------------------|
| ...  | ...       | ...  | ...    | ...     | ...              |

Typical roles (choose and adapt dynamically):
- Coordinator / Orchestrator (you) — owns overall plan, handoffs, final synthesis
- Researcher / Explorer — unknowns, APIs, docs, prior art
- Domain Builders / Workers (1–4 parallel) — specialized by component (frontend, backend, infra, data, systems, etc.)
- Verifier / QA — tests, edge cases, correctness
- Critic / Auditor — adversarial review, anti-patterns, security, style, "did we actually solve it?"

Also include:
- Handoff protocol (shared artifact locations, e.g. `TEAM_STATE.md`, role-specific output files)
- Milestone sequence and which tracks can run in parallel
- Explicit token / cost warning for large teams

Save the Team Sheet persistently as `TEAM_PLAN.md` (or equivalent) for continuity across context resets.

### 3. Present for Approval (Mandatory Gate)
Show the full Team Sheet + high-level milestones clearly.
Ask: "Approve this team plan? Reply yes / approve / go, or give modifications."
Do **not** proceed until the user gives explicit approval. Iterate the plan if they request changes.

### 4. Launch & Coordinate
On approval:
- Prefer native dynamic subagents / parallel agents if the host platform supports them (Cursor Task, Copilot agent mode, Antigravity, etc.). Use asynchronous task management when available so the Coordinator can continue while builders work.
- Otherwise simulate with sequential focused sessions: each "subagent" receives only its role prompt + relevant artifacts; write outputs to shared files; never let the main context accumulate everything.
- Give every specialist a self-contained role brief: goal, Owns, Inputs, Outputs, Success Criteria, and the shared artifact paths from the Team Sheet. Do not assume a child can see this conversation.
- Enforce single responsibility. Re-dispatch or respawn on blockers.
- Keep progress visible via shared markdown artifacts.
- If a long-running role approaches context limits, summarize state and self-succeed into a fresh instance of the same role.

### 5. Verification Loop (Non-negotiable)
- Independent Verifier must run before final delivery.
- Critic / Auditor challenges assumptions and looks for cheating, hardcoding, incomplete coverage, or false claims of success.
- Only synthesize the final result after clean verification.

### 6. Synthesize & Hand Over
- Coordinator merges verified outputs.
- Deliver: final artifacts, short walkthrough of what each role contributed, remaining risks / TODOs, and how to iterate.
- Always respond to the user in the same language they used.

## Best Practices

- Minimal sufficient team — more agents ≠ better.
- Never pollute main context; offload aggressively to subagents or files.
- Prefer verification and adversarial review over optimism.
- Log key decisions and rationale in shared state.
- Warn the user early about high token usage on large or deeply parallel teams.

## Anti-patterns to Avoid

- Letting one agent do everything under different names
- Skipping the approval gate or the independent verification step
- Overlapping ownership that creates merge conflicts
- Hardcoding, mocking, or claiming success without evidence
- Creating teams for tasks that a single focused agent can handle cleanly

## Example Role Sets

See `references/example-teams.md` for concrete Team Sheet examples (full-stack web app, systems component, research + code, data pipeline).

When in doubt, start smaller, get approval, and expand only if verification fails.
