# Ψ Mathematical Corpus v1

Status: experimental research specification. This document deliberately separates definitions, candidate derivations, and open bridges. It is not a claim that every downstream physical result has been proven.

## 1. Fundamental substrate

Define the relational state

\[
\Psi=(X,R),
\]

where `X` is the system state and `R` is the set/structure of relations.

Local neighborhood:

\[
\mathcal N(x)=\{y\mid R(x,y)\neq0\}.
\]

Endogenous local evolution may be represented abstractly as

\[
E(x)=F(x,\mathcal N(x)).
\]

For a global state:

\[
X_{t+1}\in E(X_t,R_t),
\qquad
R_{t+1}=F(X_t,R_t).
\]

The external correction operator is not fundamental: if validation/selection can be incorporated into the endogenous loop, the process closes on itself.

## 2. Extended state and memory

If two instantaneous states can be identical while their futures differ because of prior history, then `X` alone is not dynamically closed. Introduce

\[
Y=(X,\rho),
\]

with memory as a derived historical trace rather than an independent primitive:

\[
\rho_t=\mathcal H(X_0,\ldots,X_t).
\]

The desired memory is minimal: retain only information required to predict/close future dynamics.

## 3. Internal model

Seek an internal representation

\[
\varphi:Y\rightarrow Z
\]

and an induced model dynamics `G`/`F` such that

\[
\varphi(E(Y))\approx F(\varphi(Y)).
\]

The representation should preserve dynamically relevant relations while minimizing representational complexity.

## 4. Alternative trajectories

Given current state and constraints, construct a set of admissible continuations

\[
\mathcal T(Y)=\{\tau_1,\ldots,\tau_k\}.
\]

Each trajectory is tested against constraints and observations. A generic selection functional is

\[
Q(\tau)=-\epsilon(\tau)-\lambda C(\tau)+\mu P(\tau),
\]

where `epsilon` is error/constraint violation, `C` complexity, and `P` predictive/explanatory value.

Selection:

\[
\tau^*=\arg\max_{\tau\in\mathcal T}Q(\tau).
\]

## 5. Recursive evolution

The general recursive loop is

\[
Y_n\rightarrow Generate\rightarrow Test\rightarrow Select\rightarrow Y_{n+1}.
\]

The stronger meta-level loop permits the evolution operator itself to change:

\[
(Y_n,E_n)\rightarrow(Y_{n+1},E_{n+1}).
\]

Candidate operators:

\[
\mathcal E_n=\{E_n^{(1)},\ldots,E_n^{(k)}\}.
\]

Evaluate with

\[
J(E)=L(E)+\lambda C(E),
\]

and select

\[
E_{n+1}=\arg\min_{E'\in\mathcal E_n}J(E').
\]

A self-modification is accepted only if improvement reproduces on a held-out test set:

\[
L_{train}(E_{n+1})<L_{train}(E_n)
\]

and

\[
L_{holdout}(E_{n+1})\le L_{holdout}(E_n)+\delta.
\]

## 6. Minimality principle

Complexity should not be increased unless it produces measurable explanatory/predictive gain. A generic objective is

\[
J(M)=L(M)+\lambda C(M).
\]

Thus derived variables/operators should be retained only when removing them increases irreducible error or destroys a required structural property.

## 7. Quantum-structure research branch

The prior research explored whether a relational substrate can recover quantum mathematical structure. The following are research targets, not all established consequences of `Psi`.

### 7.1 Hilbert/Born branch

A candidate route considered was

\[
\text{Hilbert structure}\rightarrow\text{Gleason-type constraints}\rightarrow\rho\rightarrow P(a)=|\langle a|\psi\rangle|^2.
\]

The bridge

\[
\Psi\rightarrow\mathcal H
\]

must be proved rather than assumed.

### 7.2 Positivity branch

A candidate algebraic chain was

\[
V(a^*a)\ge0
\Rightarrow K\ge0
\Rightarrow H
\Rightarrow P=|c|^2,
\]

again marked as a proof obligation unless all intermediate assumptions are explicitly established.

### 7.3 Bell/CHSH branch

For local classical hidden-variable models the CHSH bound is

\[
|S|\le2.
\]

No-signalling alone permits stronger correlations, so no-signalling is not by itself sufficient to derive ordinary quantum correlations.

Further candidate constraints studied include composition, local tomography, interference, and continuous symmetries. These should be tested as independent axioms/constraints, not silently promoted to consequences of the substrate.

## 8. Operational time branch

A recursive state sequence may be represented as

\[
\Omega_{n+1}=\mathcal F(\Omega_n),
\]

with operational time defined through ordered state transitions rather than assumed as an external primitive. The physical interpretation remains a research question.

## 9. Test protocol for Ψ-Core

The kernel receives this corpus as hypotheses/constraints and must distinguish:

1. definitions;
2. directly derivable consequences;
3. empirical/model tests;
4. conjectures;
5. unresolved mathematical bridges.

It must not reward itself for reproducing a target formula. A stronger result is an independently rediscovered structure or a counterexample showing that an assumed step is unnecessary/invalid.

Primary experiment:

\[
M_0=D_\Psi
\rightarrow Generate
\rightarrow Test
\rightarrow Select
\rightarrow M_1
\rightarrow\cdots
\]

Measure at every generation:

\[
(\epsilon,C,\text{coverage},\text{contradictions},\text{novelty}).
\]

The principal self-optimization criterion is improvement in explanatory/predictive performance without uncontrolled complexity growth.

## 10. Non-negotiable scientific safeguards

- Never label a hypothesis a theorem.
- Preserve counterexamples and failed candidates.
- Keep training and holdout tests separate.
- Do not modify the evaluator merely to improve a score.
- Prefer a smaller equivalent model over an expanded model.
- Record every accepted/rejected self-modification.
- Preserve the original v33 baseline for comparison.
