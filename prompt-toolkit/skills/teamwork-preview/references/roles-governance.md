# Roles & Governance in Autonomous Agent Teams

Effective multi-agent execution relies on strict role boundaries, formal handoffs, and isolated workspaces.

---

## 1. Role Specifications

### Sentinel (Project Orchestrator & Anchor)
- **Role**: Coordinates the entire project lifecycle, manages the global DAG, communicates with the human developer, and resolves cross-agent deadlocks.
- **Authority**:
  - Only agent permitted to communicate directly with the user for high-level milestone sign-offs.
  - Controls worktree allocation and task dispatching.

### Specialist Workers (Domain Implementers)
- **Role**: Execute targeted coding or research tasks defined by the Sentinel.
- **Constraints**:
  - Operate inside an assigned Git worktree or directory scope.
  - Communicate outward only through structured deliverables (diffs, reports, PR descriptions).
  - Do NOT modify shared configuration files without Sentinel approval.

### Critic / Quality Gate Agents
- **Role**: Provide peer review on proposed changes before submission to the Auditor.
- **Focus**:
  - Code conventions, idiomatic style, type safety, documentation integrity, and potential performance regressions.

### Success Auditor (Independent Verification Authority)
- **Role**: Serves as an uncompromised verification gate for milestone sign-offs.
- **Core Principles**:
  1. **Strict Impartiality**: Never writes code for the reviewed milestone.
  2. **Empirical Validation**: Relies exclusively on executable tests, linters, and verification commands.
  3. **Zero-Assumption**: Re-runs all test suites from a clean checkout rather than trusting previous test logs.

---

## 2. Workspace Isolation with Git Worktrees

To prevent multiple autonomous agents from clobbering each other's work or encountering file-lock issues, use Git worktrees:

```bash
# Create an isolated workspace for Specialist A
git worktree add ../worktrees/specialist-backend -b feature/backend-migration

# Create an isolated workspace for Specialist B
git worktree add ../worktrees/specialist-frontend -b feature/frontend-migration
```

When work is complete and reviewed, merge branches cleanly into the integration branch:
```bash
git checkout main
git merge --no-ff feature/backend-migration
git worktree remove ../worktrees/specialist-backend
```

---

## 3. Communication Protocol

Agents communicate via structured markdown artifacts:
- **Task Dispatch**: Sent by Sentinel specifying Target Files, Objective, Invariants, and Acceptance Criteria.
- **Workstream Delivery**: Sent by Specialist containing Summary of Changes, Test Results, and Known Caveats.
- **Audit Sign-off**: Published by Success Auditor stating status (`APPROVED` / `CHANGES_REQUESTED`), test output summary, and verification checksum.
