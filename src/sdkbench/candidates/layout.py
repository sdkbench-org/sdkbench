"""Common, timed final-layout restoration for separately registered controls."""

from collections import deque
from typing import Any

from ..p0.models import require


def restoration_swaps(
    layout: list[int], edges: list[list[int]]
) -> list[tuple[int, int]]:
    """Route tokens home on a deterministic spanning tree, fixing leaves in order.

    This bounded control is not an optimal token-swapping or SDK routing claim.
    ``layout[logical]`` is its current physical position.
    """
    n = len(layout)
    require(
        n > 0
        and all(type(q) is int for q in layout)
        and sorted(layout) == list(range(n)),
        "Invalid restoration permutation",
    )
    adjacency: list[set[int]] = [set() for _ in range(n)]
    for edge in edges:
        require(
            len(edge) == 2
            and all(type(q) is int and 0 <= q < n for q in edge)
            and edge[0] != edge[1],
            "Invalid restoration edge",
        )
        a, b = edge
        adjacency[a].add(b)
        adjacency[b].add(a)
    tree: list[set[int]] = [set() for _ in range(n)]
    seen = {0}
    queue = deque([0])
    while queue:
        a = queue.popleft()
        for b in sorted(adjacency[a] - seen):
            seen.add(b)
            tree[a].add(b)
            tree[b].add(a)
            queue.append(b)
    require(len(seen) == n, "Restoration requires a connected target")
    positions = list(layout)
    tokens = [0] * n
    for logical, physical in enumerate(layout):
        tokens[physical] = logical
    active = set(range(n))
    swaps: list[tuple[int, int]] = []
    while len(active) > 1:
        leaf = min(q for q in active if len(tree[q]) == 1)
        start = positions[leaf]
        parents = {start: start}
        queue = deque([start])
        while leaf not in parents:
            a = queue.popleft()
            for b in sorted(tree[a]):
                if b not in parents:
                    parents[b] = a
                    queue.append(b)
        path = [leaf]
        while path[-1] != start:
            path.append(parents[path[-1]])
        path.reverse()
        for a, b in zip(path, path[1:]):
            left, right = tokens[a], tokens[b]
            tokens[a], tokens[b] = right, left
            positions[left], positions[right] = b, a
            swaps.append((a, b))
        neighbor = next(iter(tree[leaf]))
        tree[neighbor].remove(leaf)
        tree[leaf].clear()
        active.remove(leaf)
    require(
        positions == list(range(n)), "Restoration did not return every logical wire"
    )
    return swaps


def restore_payload(payload: dict[str, Any], edges: list[list[int]]) -> dict[str, int]:
    """Append exact H/CZ SWAPs; expose their separate cost without optimizing it."""
    swaps = restoration_swaps(payload["final_layout"], edges)
    for a, b in swaps:
        for control, target in ((a, b), (b, a), (a, b)):
            payload["operations"].extend(
                [
                    {"name": "h", "qubits": [target]},
                    {"name": "cz", "qubits": [control, target]},
                    {"name": "h", "qubits": [target]},
                ]
            )
    payload["final_layout"] = list(range(len(payload["final_layout"])))
    return {
        "restoration_swaps": len(swaps),
        "restoration_cz_count": 3 * len(swaps),
        "restoration_operations": 9 * len(swaps),
    }
