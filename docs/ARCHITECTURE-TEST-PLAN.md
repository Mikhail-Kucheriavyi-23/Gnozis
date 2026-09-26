# Architecture Test Plan

The first automated gate checks that the trusted Core does not acquire direct dependencies on Genesis, Research-Memory, external AI/connectors, or product/commercial surfaces.

This is an initial lexical guard only. It must later be replaced or supplemented by an AST import graph and runtime boundary tests.

The gate also verifies that the canonical Core contract documents exist. Missing contracts are an architecture failure, not a documentation warning.
