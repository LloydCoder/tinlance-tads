"""PostgreSQL-compatible graph abstraction without a graph database dependency."""

from dataclasses import dataclass
from enum import StrEnum


class GraphNodeType(StrEnum):
    ORGANIZATION = "organization"
    ACCOUNT = "account"
    EVENT = "event"
    SIGNAL = "signal"
    EVIDENCE = "evidence"
    CAPABILITY = "capability"
    OPPORTUNITY = "opportunity"


class EdgeType(StrEnum):
    SUPPORTED_BY = "supported_by"
    DERIVED_FROM = "derived_from"
    OCCURRED_AT = "occurred_at"
    CORRELATED_WITH = "correlated_with"
    CONTRADICTS = "contradicts"
    INDICATES = "indicates"
    REQUIRES = "requires"


@dataclass(frozen=True, slots=True)
class GraphNode:
    node_id: str
    node_type: GraphNodeType

    def validate(self) -> None:
        if not self.node_id:
            raise ValueError("graph node id is required")


@dataclass(frozen=True, slots=True)
class GraphEdge:
    edge_id: str
    edge_type: EdgeType
    source_id: str
    target_id: str
    evidence_ids: tuple[str, ...]

    def validate(self) -> None:
        if not self.edge_id or not self.source_id or not self.target_id:
            raise ValueError("graph edge identifiers are required")
        if self.source_id == self.target_id:
            raise ValueError("graph edges cannot self-reference")
        if not self.evidence_ids:
            raise ValueError("graph edges require evidence")


class IntelligenceGraph:
    """Deterministic graph abstraction backed by in-memory indexes for now."""

    def __init__(self) -> None:
        self._nodes: dict[str, GraphNode] = {}
        self._edges: dict[str, GraphEdge] = {}

    def add_node(self, node: GraphNode) -> None:
        node.validate()
        if node.node_id in self._nodes:
            raise ValueError(f"graph node already exists: {node.node_id}")
        self._nodes[node.node_id] = node

    def add_edge(self, edge: GraphEdge) -> None:
        edge.validate()
        if edge.edge_id in self._edges:
            raise ValueError(f"graph edge already exists: {edge.edge_id}")
        if edge.source_id not in self._nodes or edge.target_id not in self._nodes:
            raise ValueError("graph edge endpoints must already exist")
        self._edges[edge.edge_id] = edge

    def node(self, node_id: str) -> GraphNode:
        return self._nodes[node_id]

    def outgoing(self, node_id: str) -> tuple[GraphEdge, ...]:
        return tuple(edge for edge in self._edges.values() if edge.source_id == node_id)

    def incoming(self, node_id: str) -> tuple[GraphEdge, ...]:
        return tuple(edge for edge in self._edges.values() if edge.target_id == node_id)

    def nodes(self) -> tuple[GraphNode, ...]:
        return tuple(self._nodes.values())

    def edges(self) -> tuple[GraphEdge, ...]:
        return tuple(self._edges.values())
