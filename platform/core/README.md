# Core Runtime

Minimal trusted runtime boundary for state and transition operations.

The first implementation is intentionally small. It establishes the contract boundary before adding persistence, evolution plugins, or domain modules.

## Pipeline
Candidate → Test → Select → Evolve → Verify → Commit
