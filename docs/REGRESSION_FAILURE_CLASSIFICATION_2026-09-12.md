# Regression Failure Classification — 2026-09-12

## Evidence

The full `test.yml` workflow executed on the reconciled Core and reported 45 failed, 114 passed, 1 xfailed. This is a real test failure, not a CI/`tee` masking issue.

## Cluster A — obsolete State attribute API

Some tests still access `state.x` / `state.relations`, while the canonical State implementation exposes the data through `state.values` and the explicit `to_psi()` / `from_psi()` boundary. The current State implementation contains only `values` plus the adapters. These failures are test-fixture/API migration work, not evidence that the new canonical State implementation itself is broken.

## Cluster B — non-Ψ / incomplete State fixtures

Several older tests create score-only States and then exercise paths that now require the fundamental Ψ fields `x` and `relations`. `State.to_psi()` intentionally rejects a State missing either field. Such tests must either remain explicitly generic/legacy tests or be migrated to a valid Ψ State fixture.

## Cluster C — genuine semantic candidates

Failures involving hidden closure dependence, Markov sufficiency, invalid-candidate handling, empty valid sets, selector sensitivity, and state-space/hashability require separate semantic review. They must not be dismissed as fixture migration merely because other failures are obsolete API usage.

## Cluster D — intentionally red-team behavior

Generic `State -> State` callables cannot automatically guarantee that evolution is a function only of `(X,R)`. A callable can close over hidden external state. Therefore a failing adversarial test may be demonstrating the limitation of the legacy compatibility boundary rather than a defect in the canonical `PsiTransition` path.

## Immediate decision

Do not repair the 45 failures one-by-one blindly. First migrate/classify the obsolete State API fixtures, then re-run the full suite. The remaining failures after migration become the genuine semantic defect set.

## Architectural implication

Canonical Ψ evidence must use `PsiTransition` or explicitly prove delegation to the same Ψ semantics. Generic `State -> State` behavior is compatibility evidence only.

## Next gate

1. Migrate Cluster A/B tests without weakening canonical contracts.
2. Re-run full pytest CI.
3. Review remaining failures as semantic candidates.
4. Run adversarial regression against the reconciled canonical path.
5. Decide whether the legacy compatibility path can be removed.
