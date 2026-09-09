# Teamwork Blueprints & Execution Patterns

The Teamwork skill dynamically adapts its team composition and execution graph based on proven architectural blueprints.

---

## 1. Distributed Coding Blueprint

- **Ideal For**: Large-scale refactoring, repository migrations, full-stack microservice builds, multi-module feature implementation.
- **Topology**: Parallel workers converging on integration milestones.
- **Team Composition**:
  - `Sentinel` (Orchestrator & Project Lead)
  - `Domain Specialist A` (e.g. Backend API / Data Layer)
  - `Domain Specialist B` (e.g. Frontend UI / Client State)
  - `Integration Critic` (Diff review, contract verification)
  - `Success Auditor` (End-to-end integration testing and milestone sign-off)
- **Workflow**:
  1. Sentinel establishes shared API schema and interface contracts.
  2. Specialists fork worktrees and implement modules concurrently.
  3. Integration Critic verifies contract compatibility.
  4. Success Auditor runs integration tests against the merged candidate.

---

## 2. Iterative Coding Blueprint

- **Ideal For**: Core algorithmic pipelines, compiler passes, tight feedback loops where downstream work depends on upstream correctness.
- **Topology**: Sequential, test-driven iteration loop with rapid feedback.
- **Team Composition**:
  - `Sentinel` (Orchestrator)
  - `Lead Implementer` (Core logic and algorithmic author)
  - `Test & Benchmark Specialist` (Test suite generation, performance benchmarks)
  - `Success Auditor` (Correctness verification)
- **Workflow**:
  1. Test Specialist defines failing tests and performance budgets.
  2. Implementer writes targeted solution.
  3. Continuous evaluation until all tests and benchmarks pass.
  4. Auditor verifies edge conditions before committing milestone.

---

## 3. Long Proof / Deep Research Blueprint

- **Ideal For**: Architectural design proposals, performance profiling & capacity planning, library evaluations, root-cause investigations across distributed systems.
- **Topology**: Divergent exploration followed by tree-based synthesis.
- **Team Composition**:
  - `Lead Researcher / Sentinel`
  - `Explorer Agents (x2 or x3)`: Investigate divergent technical strategies in parallel.
  - `Adversarial Falsifiers`: Actively attempt to disprove or identify fatal flaws in candidate strategies.
  - `Tree Synthesis Engine`: Aggregates surviving findings into a unified technical blueprint or recommendation report.
- **Workflow**:
  1. Scoping the problem space and research hypotheses.
  2. Parallel exploration across independent workspaces.
  3. Adversarial critique and stress testing of proposed designs.
  4. Final synthesis into an actionable technical report.
