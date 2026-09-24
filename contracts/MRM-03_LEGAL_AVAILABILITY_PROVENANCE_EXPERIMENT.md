# MRM-03 — Legal-Availability Provenance Experiment

**Date:** 2026-09-24
**Status:** ACTIVE — research / no legal-rights claim
**Depends on:** MRM-01, MRM-02
**Purpose:** determine the maximum legally and technically usable scope for provenance experiments without treating a hash as proof of ownership, consent, authorship, valuation, or legal entitlement.

## 1. Core rule

A cryptographic commitment proves that a particular representation existed or was committed at a particular point in an integrity chain. It does not by itself establish copyright ownership, inventorship, contractual entitlement, identity, consent, valuation, or legal enforceability.

## 2. Evidence classes

Separate:
- repository commits and immutable release artifacts;
- authored design decisions and questions;
- AI-assisted outputs;
- third-party contributions;
- licenses and contractual permissions;
- personal data;
- public-source material;
- verification results.

Each class must carry its own provenance and permission status.

## 3. Privacy boundary

Do not place raw personal data, credentials, private API keys, sensitive documents, or unnecessary identifying information into the public hash archive.

Where personal data is involved, prefer data minimisation, purpose limitation, pseudonymisation and encryption. The Serbian personal-data framework and GDPR principles must be treated as applicable constraints where their territorial/material scope is met.

## 4. Legal-status labels

Every provenance record must distinguish:
- FACT — directly evidenced;
- ATTRIBUTED — claim attributed to a source/person;
- LICENSED — permission/license evidenced;
- CONSENTED — consent evidenced where legally relevant;
- UNVERIFIED — evidence incomplete;
- THEORETICAL — proposed only;
- LEGAL_REVIEW_REQUIRED — legal effect cannot safely be inferred.

## 5. Contribution model

Prototype:

ContributionRecord =
(ActorRef, Role, ArtifactRef, ParentRefs, Timestamp,
EvidenceRefs, PermissionStatus, Hash, VerificationStatus)

The record must not assign monetary value automatically.

## 6. AI contribution boundary

AI-generated or AI-assisted material must be recorded as process provenance, not automatically as human authorship or ownership. Human contributions, source materials, licenses and contractual terms remain separate evidence dimensions.

## 7. Maximum lawful experiment set

Test, where permissions and applicable law allow:
1. hashing historical repository states;
2. hashing design decisions and contract records;
3. linking commits to documented decisions;
4. recording independent audit attestations;
5. recording contribution lineage;
6. creating signed release manifests;
7. testing redacted/pseudonymised provenance;
8. testing selective disclosure;
9. testing partner-submitted machine-readable contribution records;
10. testing cross-repository lineage without copying protected source material.

Do not test by collecting third-party private data, bypassing access controls, scraping restricted systems, or claiming rights that have not been granted.

## 8. Data-subject / owner controls

For future personal-data workflows, design for:
- access;
- rectification;
- restriction/objection where applicable;
- deletion/erasure where legally applicable;
- portability where applicable;
- consent withdrawal where consent is the legal basis.

A hash or immutable audit event must not be treated as a reason to retain personal data indefinitely. Store the minimum necessary evidence and separate immutable integrity references from mutable personal-data stores.

## 9. Legal experiment outputs

Produce:
A. Provenance schema;
B. legal-status taxonomy;
C. privacy/data-flow map;
D. license/permission matrix;
E. contribution evidence graph;
F. redaction/selective-disclosure prototype;
G. unresolved legal questions requiring qualified counsel.

## 10. Acceptance

The experiment is successful only if the system can demonstrate provenance and integrity while clearly refusing to infer unsupported legal rights.

No commercial valuation, ownership allocation, royalty allocation, or legal authorship claim is activated by this contract.

## 11. Next gate

After the experiment, optimize the contract system around the smallest provenance object that survives technical, privacy and legal scrutiny. Any production legal terms require jurisdiction-specific professional review.
