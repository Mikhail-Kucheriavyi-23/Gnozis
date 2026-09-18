# AI_CONTEXT.md — Gnozis Strategic Mathematical Context
## 2026-09-18 consolidation

This file records the strategic and mathematical conclusions established during the current analytical phase. It is not a claim that every statement below is proven. Distinguish: definition, candidate derivation, implementation fact, empirical result, and hypothesis.

## 1. Strategic foundation

Gnozis is not to be designed by accumulating software modules and then fitting mathematics afterward. The direction is reversed:

Natural mathematical structure
-> laws/constraints
-> computable representation
-> architecture
-> implementation
-> verification
-> empirical experiments.

The target is a natural and efficient mathematical architecture, not a maximally complex architecture.

A useful engineering criterion is:

Minimum primitives -> maximum derived structure.

Do not add a primitive entity if it can be derived from lower-level structure.

The real-world model is treated as recursively structured; this is a design/philosophical premise to be mathematically investigated, not a license to assert unproven physical claims.

Panpsychist/philosophical ideas may guide the research direction, but Core must distinguish philosophical interpretation from mathematical proof and empirical verification.

## 2. Core candidate ontology

Primary candidate:

Psi = (X, R)

X = elements/structures.
R = relations between elements.

For finite representations, R may be represented by one or more relation matrices, but the matrix representation is an implementation of the relational structure, not necessarily the fundamental ontology.

Candidate general relation form:

R subset of X x X x K

where K can encode relation type.

An element x in X may itself have recursive structure of the same mathematical class. Therefore Agent, World, Memory, Knowledge, etc. should not automatically be fundamental classes.

## 3. State and immutability

State must remain the single source of truth for Psi.

Do not introduce a second hidden state model.

Psi_t = (X_t, R_t).

Transitions must produce a new state; old states must remain deeply immutable. Frozen dataclasses alone are insufficient if nested mutable objects remain reachable.

R must be a first-class evolving component. The model must permit:
- X' = X with R' != R
- X' != X with R' = R
- X' != X and R' != R
- R' = empty when permitted.

## 4. Laws and admissibility

Do not put every law into Psi by default.

Candidate separation:

Psi = structure
L = admissibility/laws
T_L = transition dynamics compatible with L.

Basic admissible future set:

A_L(Psi) = { Psi' | L(Psi, Psi') = 1 }

Core transition is therefore not necessarily a single deterministic F(Psi). The state may have multiple admissible futures:

Psi_{t+1} in A_L(Psi_t).

Selection must never create an inadmissible state.

Selection and value are not fundamental until shown necessary.

## 5. Invariants

Separate:
- invariant properties;
- variable properties;
- derived quantities.

Do not make everything invariant, because that would prevent evolution.

Candidate preservation condition:

I(Psi_{t+1}) = I(Psi_t)

for invariants that truly define organizational identity.

Safety, logical validity, identity, etc. are candidates for constraints/invariants rather than scalar scores.

## 6. Evolution and recursion

Ordinary evolution:

(Psi_t, L_t) -> (Psi_{t+1}, L_t)

Meta-evolution/self-evolution:

(Psi_t, L_t) -> (Psi_{t+1}, L_{t+1})

The second is the meaningful higher-order self-evolution problem: changing the state and/or the space of possible transformations.

Proof-preserving evolution candidate:

L_t |- Valid(L_{t+1})
and
L_t |- Invariant(Psi_{t+1})

A new law must not simply be accepted because an AI proposed it.

Software self-modification and mathematical evolution are separate layers:
mathematical evolution -> validated law/behavior -> software implementation -> verification.

## 7. Recursion and scale

Potential recursive structure:

x in X may itself be a structure (X_x, R_x).

Relations can exist:
- between elements;
- between substructures;
- potentially between relations or higher-order structures.

Do not introduce separate Agent/World classes unless analysis shows they are irreducible.

Candidate derived agent:

A subset A of X that is relatively internally organized, causally bounded, dynamically persistent, and interacts with the surrounding structure through a boundary of relations.

Candidate world:

W = (X_W, R_W), i.e. a structure of the same mathematical family.

World A and World B should be different instances/constraints/observation contexts, not separate hard-coded engines.

## 8. Observation, information, memory, knowledge

Observation:

O: Psi -> Y

An observation y restricts possible states:

Omega_y = {Psi in Omega | O(Psi) = y}

Candidate information interpretation:

Information = reduction/restriction of the space of possible states.

Observation can therefore restrict admissible futures:

A_y(Psi) subseteq A(Psi).

Memory is not merely a database. Candidate operational definition:

Memory exists when past information has a persistent causal effect on future dynamics.

A testable condition is that, holding other relevant conditions fixed, future behavior differs depending on whether prior information was retained.

Knowledge is stronger than memory: candidate definition is information incorporated into generative constraints/admissibility.

Do not collapse raw observation, memory, and knowledge into one object.

## 9. Different realities / World A and World B

Different observations need not imply different underlying structures.

O_A(Psi) may differ from O_B(Psi).

Thus different realities can be modeled as different observation/constraint contexts over a common mathematical core.

When two sources produce constraints C_A and C_B:
- compatible case: A(C_A) intersection A(C_B) is nonempty;
- incompatible case: the intersection may be empty.

Do not force an artificial compromise when constraints are incompatible. Incompatibility itself is information.

This is a key mathematical route for collective integration of different realities.

## 10. Tension and creativity

Candidate structural tension:

tau = a measure of incompatibility/difference between constraints, structures, or admissible spaces.

Do NOT assume that the universal objective is tau -> 0.

Persistent or increased tension may create a richer structure.

Important candidate distinction:

Ordinary optimization:
choose x inside an existing admissible space A_t.

Higher-order creativity:
transform the structure so that A_t itself changes.

Candidate formulation:

Creativity = structural transformation of the solution/admissible space, not merely better selection inside a fixed space.

A genuinely new solution may be a state that was unavailable under A_t but becomes admissible under A_{t+1}.

This is a candidate hypothesis to test, not yet a theorem.

## 11. Agents, multi-agent behavior, trust

Agenthood should preferably emerge as a structural property of a substructure, rather than be hard-coded as a primitive.

Multi-agent behavior can then arise from multiple persistent substructures A_i within a common relational system.

Trust should preferably be derived from historical evidence/consistency relations rather than made a primitive scalar.

Candidate:
Trust(a,b) = f(consistency, evidence, history, context)

The exact form must be derived/tested later.

Gnozis interacting with users and Gnozis creating capabilities for user copies should use the same underlying relational/agent model rather than separate special-purpose ontologies.

## 12. Time and causality

Avoid requiring a global clock in Core.

The index t can be an ordering of transformations rather than an externally imposed universal clock.

Candidate causal structure:
Psi_a precedes Psi_b when a is a dependency/causal prerequisite for b.

A partial order may be more fundamental than global time for distributed/multi-agent evolution.

## 13. Candidate variational direction

Do not yet declare a final formula.

Candidate classes to compare:
A. relational dynamics: Psi_{t+1} = F(Psi_t)
B. matrix dynamics: M_{t+1} = Phi(M_t)
C. operator dynamics: Psi_{t+1} = T_Psi(Psi_t)
D. variational dynamics: delta S = 0
E. constrained variational dynamics: delta S = 0 with C_i = 0
F. recursive relational dynamics involving R, transformations of R, and higher-order relations.

Potential unified transition:

Psi_{t+1} in Ext_{Psi' in A_L(Psi_t)} E(Psi_t, Psi')

Use Ext deliberately rather than prematurely assuming min/max.

A functional E must not simply be invented as a fitness score. The research goal is to determine whether E can be derived from structure, information, invariants, or constraints.

Potentially important alternative:
minimum sufficient structural change subject to required constraints.

But this remains a candidate, not a final law.

## 14. Optimality criterion for the mathematical model

Do not define optimality as mathematical complexity or number of features.

Candidate model selection criterion:

M* = argmin_M Complexity(M)

subject to M satisfying the required structural properties.

A useful informal compression criterion:

K(M) = Complexity(M) - DerivedCapability(M)

Seek a low-K model while preserving required properties.

The desired result is not a magical single equation chosen by taste. It is a minimal mathematical principle from which the necessary equations and architecture can be derived.

## 15. 14 current requirements for candidate models

A candidate fundamental model should be tested for:
1. structurality
2. relationality
3. X-change
4. R-change
5. recursion
6. admissibility/constraints
7. invariants
8. branching
9. emergence
10. self-maintenance
11. observability
12. mathematical verifiability
13. compositionality
14. recursive/self-similar or scale behavior

A candidate that satisfies only some of these is not automatically the final model.

## 16. Current core hypothesis

The strongest current candidate minimal chain is:

Psi = (X,R)
-> observation O
-> information as restriction of possibilities
-> constraints/admissibility A_L(Psi)
-> tension from incompatibility
-> structural transformation
-> new Psi
while preserving required invariants.

Meta-evolution adds:
L_t -> L_{t+1}, subject to proof-preserving validation.

This is a research scaffold, not a final theorem.

## 17. What must NOT happen

Do not:
- add AI models into mathematical Core;
- turn every concept into a class;
- introduce a global selector as an oracle;
- assume fitness is fundamental;
- assume minimizing tension is universally correct;
- confuse empirical behavior with mathematical proof;
- claim the model proves a physical/panpsychist worldview;
- use World A/B as hard-coded special engines;
- allow self-modification to bypass validation;
- treat a database as proof of memory;
- treat an LLM's generated output as proof of mathematical validity.

## 18. Immediate research program while repository access is constrained

Before implementation, derive and compare:
1. information from distinguishability/restriction of possibility;
2. memory as persistent causal influence;
3. knowledge as incorporation into generative constraints;
4. tension as incompatibility of constraints/admissible spaces;
5. creativity as transformation of the admissible space;
6. agenthood as a persistent relational substructure;
7. worldhood as a structure/context of the same family;
8. trust as a derived evidence relation;
9. causality as dependency/partial order;
10. autopoiesis as preservation of organization under structural change;
11. meta-evolution as proof-preserving transformation of laws;
12. a candidate variational/structural principle unifying selection, stability and evolution.

For every result mark it as:
DEFINITION / DERIVATION / THEOREM-CANDIDATE / IMPLEMENTATION REQUIREMENT / EMPIRICAL TEST / OPEN QUESTION.

## 19. Strategic principle

Gnozis should aim to reproduce the organization of natural mathematical systems rather than imitate their surface complexity.

The central engineering question is:
What is the smallest lawful recursive structure from which the observed higher-level capabilities can naturally emerge?

Do not optimize the architecture before answering this question.
