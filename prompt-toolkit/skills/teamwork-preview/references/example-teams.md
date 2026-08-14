# Example Team Sheets

These are illustrative. Always adapt roles, ownership, and success criteria to the actual task. Prefer the smallest team that still provides parallelism + independent verification.

## 1. Full-Stack Web Application

**Goal:** Build a production-ready multi-user collaborative whiteboard with real-time sync, auth, and basic widgets.

| Role | Specialty | Owns | Inputs | Outputs | Success Criteria |
|------|-----------|------|--------|---------|------------------|
| Coordinator | Orchestration | Overall plan, integration, final synthesis | User goal + Team Sheet | TEAM_PLAN.md, final walkthrough | All streams integrated, user can demo |
| Frontend Builder | React / UI / real-time client | Client app, components, WebSocket client | Design notes, API contract | Working UI + client tests | UI matches requirements, real-time updates visible |
| Backend Builder | API / DB / real-time server | Server, auth, persistence, WebSocket | Data model, security needs | API + server tests | Auth works, data persists, concurrent edits safe |
| QA Verifier | Testing + edge cases | Test suite, security review | All code | Test report + bug list | Critical paths covered, no obvious security holes |
| Critic | Adversarial review | Cross-cutting quality | All artifacts | Critique notes | Finds at least the top risks before final delivery |

**Parallel tracks:** Frontend + Backend can start after API contract is agreed. Verifier and Critic run after first integration.

## 2. Systems / Low-Level Component

**Goal:** Implement a minimal but correct userspace scheduler + basic memory allocator (educational OS component).

| Role | Specialty | Owns | Inputs | Outputs | Success Criteria |
|------|-----------|------|--------|---------|------------------|
| Coordinator | Architecture + integration | Plan, interfaces, final report | Spec | TEAM_PLAN.md + design notes | Interfaces stable, components link |
| Explorer | Research + prior art | Literature, existing designs | Problem statement | Research summary + recommended approach | Justifies design choices with references |
| Scheduler Worker | Scheduling algorithms | Scheduler core + tests | Interface contract | Code + unit tests | Correct under concurrent load tests |
| Allocator Worker | Memory management | Allocator + tests | Interface contract | Code + unit tests | No leaks in stress tests, correct alignment |
| Auditor | Static analysis + consistency | Cross-checks, anti-cheat | All code | Audit report | No hidden state, no undefined behavior |

## 3. Research + Implementation Pipeline

**Goal:** Investigate a new technique, implement a prototype, and rigorously evaluate it.

| Role | Specialty | Owns | Inputs | Outputs | Success Criteria |
|------|-----------|------|--------|---------|------------------|
| Coordinator | Synthesis | Overall narrative + final paper-like report | All outputs | Final report | Coherent story, claims backed by evidence |
| Researcher | Literature + design | Survey, hypotheses, experiment design | Goal | Research notes + experiment plan | Covers key prior work, clear metrics |
| Implementer | Prototype code | Code + basic tests | Experiment plan | Working prototype | Reproducible results on sample data |
| Evaluator | Metrics + analysis | Evaluation scripts, statistical checks | Prototype + data | Evaluation report | Claims are quantified, limitations stated |
| Critic | Adversarial | Challenge of assumptions and results | All artifacts | Critique | Forces honesty about weaknesses |

## 4. Data Pipeline / ETL + Analysis

**Goal:** Ingest messy multi-source data, clean it, build reliable features, and produce analysis + dashboard.

| Role | Specialty | Owns | Inputs | Outputs | Success Criteria |
|------|-----------|------|--------|---------|------------------|
| Coordinator | End-to-end flow | Pipeline design + final delivery | Goal | TEAM_PLAN.md + architecture | Data flows end-to-end without manual fixes |
| Ingest Worker | Sources + schema | Raw ingestion + validation | Source docs | Clean raw tables + schema | Handles missing/corrupt records gracefully |
| Feature Worker | Transformation | Feature engineering + tests | Clean tables | Feature store + docs | Features are deterministic and documented |
| Analyst | Insights + viz | Analysis + dashboard | Features | Insights report + dashboard | Actionable findings with confidence notes |
| Verifier | Data quality | Tests, drift checks, lineage | Full pipeline | Quality report | No silent data loss, lineage is clear |

Use these as starting templates. Always re-evaluate after the first verification cycle and shrink or expand the team if needed.
