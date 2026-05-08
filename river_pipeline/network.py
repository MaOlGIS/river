"""Pure Python network metrics pro directed river segments."""

from __future__ import annotations

import collections
from dataclasses import dataclass
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class NetworkStats:
    segment_count: int
    node_count: int
    headwater_count: int
    component_count: int
    cycle_detected: bool
    cycle_node_count: int
    cycle_segment_count: int
    max_distance: float


def _as_node(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _components(nodes: set[str], adjacency: Mapping[str, set[str]]) -> list[set[str]]:
    remaining = set(nodes)
    components: list[set[str]] = []
    while remaining:
        start = next(iter(remaining))
        stack = [start]
        component: set[str] = set()
        remaining.remove(start)
        while stack:
            node = stack.pop()
            component.add(node)
            for neighbor in adjacency.get(node, set()):
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    stack.append(neighbor)
        components.append(component)
    return components


def compute_source_distances(
    records: Iterable[Mapping[str, Any]],
    start_field: str,
    end_field: str,
    length_field: str,
    id_field: str = "id",
) -> tuple[dict[Any, float | None], dict[Any, float | None], NetworkStats]:
    """Spočítá nejdelší acyclic source-distance values pro river segments.

    Vrací tři hodnoty:
    - distance ke downstream/end node každého segmentu
    - distance k upstream/start node každého segmentu
    - network QA statistics

    Segments, které jsou součástí directed cycles, dostanou hodnotu ``None``,
    protože longest path není pro positive-length cyclic graphs jednoznačně
    definovaná.
    """

    edges: list[tuple[Any, str, str, float]] = []
    nodes: set[str] = set()
    out_edges: collections.defaultdict[str, list[int]] = collections.defaultdict(list)
    in_edges: collections.defaultdict[str, list[int]] = collections.defaultdict(list)
    undirected: collections.defaultdict[str, set[str]] = collections.defaultdict(set)

    for pos, record in enumerate(records):
        start = _as_node(record.get(start_field))
        end = _as_node(record.get(end_field))
        if start is None or end is None:
            continue
        try:
            length = float(record.get(length_field) or 0.0)
        except (TypeError, ValueError):
            length = 0.0
        record_id = record.get(id_field, pos)
        idx = len(edges)
        edges.append((record_id, start, end, max(length, 0.0)))
        nodes.update((start, end))
        out_edges[start].append(idx)
        in_edges[end].append(idx)
        undirected[start].add(end)
        undirected[end].add(start)

    indegree = {node: len(in_edges.get(node, [])) for node in nodes}
    queue = collections.deque([node for node in nodes if indegree.get(node, 0) == 0])
    node_distance = {node: 0.0 for node in queue}

    while queue:
        start = queue.popleft()
        base_distance = node_distance.get(start, 0.0)
        for edge_idx in out_edges.get(start, []):
            _, _, end, length = edges[edge_idx]
            candidate = base_distance + length
            if candidate > node_distance.get(end, float("-inf")):
                node_distance[end] = candidate
            indegree[end] -= 1
            if indegree[end] == 0:
                queue.append(end)

    cycle_nodes = {node for node in nodes if indegree.get(node, 0) > 0}
    cycle_edge_ids = {
        record_id
        for record_id, start, end, _ in edges
        if start in cycle_nodes or end in cycle_nodes
    }

    downstream_by_id: dict[Any, float | None] = {}
    upstream_by_id: dict[Any, float | None] = {}
    for record_id, start, end, _ in edges:
        if record_id in cycle_edge_ids:
            downstream_by_id[record_id] = None
            upstream_by_id[record_id] = None
            continue
        downstream_by_id[record_id] = node_distance.get(end, 0.0)
        upstream_by_id[record_id] = node_distance.get(start, 0.0)

    stats = NetworkStats(
        segment_count=len(edges),
        node_count=len(nodes),
        headwater_count=sum(
            1
            for node in nodes
            if len(in_edges.get(node, [])) == 0 and len(out_edges.get(node, [])) > 0
        ),
        component_count=len(_components(nodes, undirected)) if nodes else 0,
        cycle_detected=bool(cycle_nodes),
        cycle_node_count=len(cycle_nodes),
        cycle_segment_count=len(cycle_edge_ids),
        max_distance=max((value or 0.0 for value in downstream_by_id.values()), default=0.0),
    )
    return downstream_by_id, upstream_by_id, stats
