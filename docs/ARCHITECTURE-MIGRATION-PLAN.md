# Architecture Migration Plan

1. Freeze canonical boundaries and schemas.
2. Build Core contracts before moving implementation.
3. Add structural dependency tests.
4. Add context/provenance continuity contracts.
5. Migrate reusable evidence and research to Research-Memory in small batches.
6. Keep Genesis private and extract only required interfaces.
7. Preserve old implementations until replacement evidence exists.
8. Remove obsolete paths only after verification and rollback evidence.

Migration is incremental. No whole-repository copy is considered architectural migration.
