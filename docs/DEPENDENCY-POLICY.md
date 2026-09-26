# Dependency Policy

## Allowed

Genesis -> Core contracts
Product -> Core contracts
Product -> Genesis interfaces
Research/Knowledge -> explicit evidence/context interfaces
External adapters -> public interfaces

## Forbidden

Core -> Genesis
Core -> Research-Memory
Core -> LLM/API/connector
Core -> Product/Commercial/UI
External repository -> direct Core database mutation
Research/Knowledge -> implicit authority

## Enforcement

The policy must be represented by structural tests and reviewed whenever a new package or connector is introduced.
