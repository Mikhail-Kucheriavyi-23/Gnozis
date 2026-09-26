# Persistence Contract v1

Persistence stores authoritative state and required integrity/provenance records.

Persistence is distinct from retrieval, consumption, and influence.

Recovery must fail closed when integrity or provenance checks cannot establish a valid authoritative state.

## Required properties
- authoritative state is versioned;
- integrity is checked before trusted recovery;
- provenance is retained with material state changes;
- conflicting authoritative records fail closed;
- persistence does not grant access by itself.
