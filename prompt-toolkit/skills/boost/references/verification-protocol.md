# Zero-Trust Verification & Adversarial Falsification Protocol

In the Boost skill, code is never presumed correct based on completion or model confidence alone. All proposed solutions must endure a strict, multi-stage verification pipeline.

---

## 1. The 4 Verification Gates

Every candidate solution must successfully pass four successive gates before it can be marked as resolved:

```text
Gate 1: Baseline Reproduction
   └── The failure MUST fail deterministically before any fix is introduced.

Gate 2: Solution Pass
   └── The fix MUST turn the failing reproduction test green (0 errors, exit 0).

Gate 3: Full Regression Suite
   └── The existing workspace test suite MUST pass with zero regressions.

Gate 4: Adversarial Falsification
   └── The fix MUST survive active attempts to break it with edge cases and stress scenarios.
```

---

## 2. Adversarial Falsification Techniques

When testing a patch, formulate adversarial tests specifically targeting common AI implementation pitfalls:

### A. Boundary & Degenerate Cases
- Empty collections, null/undefined inputs, zero/negative values, single-element collections.
- Extremely large payloads or high-cardinality collections (OOM / memory spike checks).

### B. Concurrency & Race Conditions
- Run the reproduction script concurrently with 10–50 parallel threads or asynchronous tasks.
- Randomize interleaving or introduce simulated I/O latency (e.g., mock network delays) to verify thread-safety and lock mechanisms.

### C. State Leaks & Idempotence
- Invoke the patched function/service multiple times sequentially on the same state.
- Verify that cleanup hooks, socket closures, and database transaction rollbacks execute reliably under unexpected exceptions.

---

## 3. Backtracking State Machine

If any gate fails:
1. **Do not patch the patch**: Avoid writing layers of patches on top of an unverified hypothesis.
2. **Revert the workspace**: Undo the edits made by `DeepCoder` to restore the clean baseline state.
3. **Invalidate the hypothesis**: Mark the tested hypothesis as `REJECTED` in the Hypothesis Tree, noting the failure log.
4. **Advance to next hypothesis**: Select the next ranked hypothesis from the tree or formulate an alternative approach based on new evidence.
