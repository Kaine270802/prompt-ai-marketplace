# Hypothesis Tree Template

Use this document to track investigation hypotheses, evidence, and verification statuses during a `/boost` session.

---

## Problem Definition
- **Symptom**: [Brief description of the observed defect or challenge]
- **Expected Invariant**: [What condition must always hold true]
- **Reproduction Command**: `[e.g. pytest tests/test_concurrency.py -k test_deadlock]`

---

## Hypothesis Matrix

| ID | Hypothesis | Proposed Mechanism | Status | Evidence / Verification Notes |
| :--- | :--- | :--- | :--- | :--- |
| **H1** | [Hypothesis 1 description] | [Why this could cause the bug] | `UNTESTED` / `VERIFIED` / `REJECTED` | [Test results, callstack traces] |
| **H2** | [Hypothesis 2 description] | [Alternative root cause] | `UNTESTED` / `VERIFIED` / `REJECTED` | [Test results, callstack traces] |
| **H3** | [Hypothesis 3 description] | [Edge case / environment anomaly] | `UNTESTED` / `VERIFIED` / `REJECTED` | [Test results, callstack traces] |

---

## Gate Checklist for Active Hypothesis: [e.g. H1]

- [ ] **Gate 1: Reproduction Test Created & Verified Failing**
  - Test file: `[path/to/test]`
  - Exit code / Error message: `[error details]`
- [ ] **Gate 2: Patch Applied & Reproduction Test Passing**
  - Patch files: `[files modified]`
  - Result: `PASSED`
- [ ] **Gate 3: Full Regression Suite Clean**
  - Command: `[suite command]`
  - Result: `0 failures, 0 errors`
- [ ] **Gate 4: Adversarial Falsification Completed**
  - Edge cases tested: `[list cases tested]`
  - Result: `ROBUST`

---

## Final Resolution Summary
- **Validated Root Cause**: [Summary of confirmed root cause]
- **Solution Implemented**: [Summary of patch]
- **Regression Guard**: [Automated test retained to prevent future recurrence]
