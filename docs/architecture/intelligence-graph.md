# Intelligence Graph

X5 adds a graph abstraction for relationships among accounts, events, signals, evidence, capabilities and opportunities.

## Design

The first implementation is relationally compatible and dependency-free. It does not introduce Neo4j or another graph database prematurely.

Every edge requires evidence and both endpoints must already exist. Historical graph facts are treated as append-only domain evidence; mutation and persistence semantics remain owned by tads_db.

## Provenance

Edges such as SUPPORTED_BY, DERIVED_FROM and CONTRADICTS preserve the relationship between derived intelligence and its supporting evidence. This matches the general provenance principle that relationships among entities, activities and derivations are needed to assess trust. See W3C PROV-DM.

## Promotion rule

A dedicated graph database may be evaluated only after measured query latency, traversal depth, storage volume or operational isolation requirements demonstrate that PostgreSQL is insufficient.
