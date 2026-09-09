# Success Auditor Checklist & Sign-off Report

> **Project Name**: [Project Name]  
> **Milestone ID**: [e.g. Milestone 2 - Backend Migration]  
> **Auditor ID**: [Success Auditor Agent]  
> **Date**: [Timestamp]  

---

## 1. Impartiality Certification
- [x] The evaluating agent did NOT write or modify application code for this milestone.
- [x] Evaluation executed from a clean branch checkout / pristine working directory.

---

## 2. Technical Quality Gates

| Gate Item | Command Executed | Expected Outcome | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Compilation / Build** | `npm run build` | Exit Code 0 | Exit Code 0 | `PASS` / `FAIL` |
| **Unit Test Suite** | `npm test` | 100% Passing | All passed | `PASS` / `FAIL` |
| **Integration Suite** | `pytest tests/e2e` | 0 Failures | 0 Failures | `PASS` / `FAIL` |
| **Type Check** | `tsc --noEmit` | 0 Errors | 0 Errors | `PASS` / `FAIL` |
| **Static Linting** | `eslint .` | 0 Errors | 0 Errors | `PASS` / `FAIL` |

---

## 3. Invariant & Regression Verification
- **Functional Requirements Check**:
  - [ ] Did the delivered code fulfill all explicit acceptance criteria for this milestone?
  - [ ] Are existing features and adjacent modules unaffected?
- **Code Quality Check**:
  - [ ] No hardcoded secrets, temporary debug logs, or commented-out code blocks left behind.
  - [ ] Error handling covers edge cases and network timeouts.

---

## 4. Auditor Recommendation
- **Verdict**: `APPROVED` / `CHANGES_REQUESTED`
- **Actionable Feedback (if rejected)**:
  - [List specific line numbers, failing tests, or architectural discrepancies]
- **Auditor Signature**: `[Signed by Success Auditor]`
