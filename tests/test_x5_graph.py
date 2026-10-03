import pytest

from tads_graph import EdgeType, GraphEdge, GraphNode, GraphNodeType, IntelligenceGraph


def node(node_id: str, kind: GraphNodeType) -> GraphNode:
    return GraphNode(node_id, kind)


def edge(edge_id: str, source: str, target: str) -> GraphEdge:
    return GraphEdge(edge_id, EdgeType.SUPPORTED_BY, source, target, ("ev-1",))


def test_graph_requires_existing_evidence_backed_endpoints() -> None:
    graph = IntelligenceGraph()
    graph.add_node(node("signal-1", GraphNodeType.SIGNAL))
    graph.add_node(node("evidence-1", GraphNodeType.EVIDENCE))
    graph.add_edge(edge("edge-1", "signal-1", "evidence-1"))
    assert graph.outgoing("signal-1") == (edge("edge-1", "signal-1", "evidence-1"),)


def test_graph_rejects_unknown_endpoint() -> None:
    graph = IntelligenceGraph()
    graph.add_node(node("signal-1", GraphNodeType.SIGNAL))
    with pytest.raises(ValueError, match="endpoints"):
        graph.add_edge(edge("edge-1", "signal-1", "missing"))


def test_graph_rejects_duplicate_nodes_and_edges() -> None:
    graph = IntelligenceGraph()
    graph.add_node(node("signal-1", GraphNodeType.SIGNAL))
    with pytest.raises(ValueError, match="already exists"):
        graph.add_node(node("signal-1", GraphNodeType.SIGNAL))
    graph.add_node(node("evidence-1", GraphNodeType.EVIDENCE))
    graph.add_edge(edge("edge-1", "signal-1", "evidence-1"))
    with pytest.raises(ValueError, match="already exists"):
        graph.add_edge(edge("edge-1", "signal-1", "evidence-1"))


def test_graph_edges_require_evidence_and_no_self_reference() -> None:
    graph = IntelligenceGraph()
    graph.add_node(node("signal-1", GraphNodeType.SIGNAL))
    with pytest.raises(ValueError, match="self-reference"):
        graph.add_edge(
            GraphEdge(
                "edge-1",
                EdgeType.INDICATES,
                "signal-1",
                "signal-1",
                ("ev-1",),
            )
        )
    with pytest.raises(ValueError, match="evidence"):
        GraphEdge("edge-2", EdgeType.INDICATES, "signal-1", "other", ()).validate()
