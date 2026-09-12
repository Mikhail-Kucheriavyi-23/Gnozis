# Baseline vs plasticity protocol

## Purpose

Determine whether Drosophila-inspired structural plasticity adds genuine adaptive capability to Gnozis, rather than merely adding computation.

## Controlled comparison

Use identical initial state `Ψ0=(X0,R0)`, identical perturbation sequence, identical step budget, and identical initial pulse.

- **Baseline:** no Drosophila-inspired topology plasticity.
- **Plastic:** local structural plasticity and endogenous candidate relation formation.

## Primary measurements

For each perturbation cycle `i` record:

- `V_i`: structural viability.
- `ΔR_i`: structural change (`R_i symmetric-difference R_{i-1}`).
- `A_i`: whether the system remains capable of recovery under the next perturbation.
- `C_i`: number/diversity of distinct viable organizations reached.

## Novel-damage gate

Train/expose both variants only to `D1,D2`. Then apply unseen `D3,D4` using the same protocol.

The strongest useful result is not merely `V_plastic > V_baseline` once. It is repeated superiority on unseen perturbations:

`A_plastic(novel) > A_baseline(novel)`

while the plastic system reaches structures not explicitly prescribed by the experiment.

## Interpretation

- If plasticity helps only on familiar damage, it is specialized adaptation.
- If it helps on unseen damage, it is evidence of structural generalization.
- If it preserves the ability to adapt again after adaptation, it becomes evidence for accumulated adaptive capacity.
- None of these alone proves autonomous intelligence or autopoiesis.

The Drosophila mechanism remains a research adapter until these controls produce reproducible evidence.
