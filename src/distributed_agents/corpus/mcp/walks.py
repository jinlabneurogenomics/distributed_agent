"""Dependency-free graph-walk primitives for bounded corpus discovery."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Collection, Mapping, Sequence


@dataclass(frozen=True)
class RandomWalkResult:
    """Converged multi-source random walk with exact seed decomposition."""

    nodes: tuple[str, ...]
    scores: tuple[float, ...]
    seed_components: tuple[tuple[float, ...], ...]
    in_degrees: tuple[int, ...]
    out_degrees: tuple[int, ...]
    iterations: int
    l1_residual: float
    max_seed_l1_residual: float
    probability_mass: float
    directed_edge_count: int


def random_walk_with_restart(
    adjacency: Mapping[str, Collection[str]],
    seeds: Sequence[str],
    *,
    restart_probability: float = 0.15,
    tolerance: float = 1e-10,
    max_iterations: int = 200,
) -> RandomWalkResult:
    """Run an equal-personalization RWR over a directed binary graph.

    Dangling mass is redistributed to the same global personalization vector.
    The per-seed component matrix uses that fixed transition operator, so its
    rows sum to the reported stationary scores up to floating-point error.
    """

    if not 0.0 < restart_probability < 1.0:
        raise ValueError("restart_probability must be between 0 and 1")
    if tolerance <= 0.0:
        raise ValueError("tolerance must be positive")
    if max_iterations < 1:
        raise ValueError("max_iterations must be positive")

    seed_tuple = tuple(seeds)
    if not seed_tuple or len(set(seed_tuple)) != len(seed_tuple):
        raise ValueError("seeds must contain distinct graph nodes")

    node_set = set(adjacency)
    node_set.update(seed_tuple)
    for neighbors in adjacency.values():
        node_set.update(neighbors)
    nodes = tuple(sorted(node_set))
    node_index = {node: offset for offset, node in enumerate(nodes)}

    targets_by_source: list[tuple[int, ...]] = []
    in_degrees = [0] * len(nodes)
    for node in nodes:
        targets = tuple(
            sorted(
                {
                    node_index[target]
                    for target in adjacency.get(node, ())
                    if target != node
                }
            )
        )
        targets_by_source.append(targets)
        for target in targets:
            in_degrees[target] += 1

    seed_count = len(seed_tuple)
    restart_share = 1.0 / seed_count
    restart_components = [
        [0.0 for _ in range(seed_count)] for _ in range(len(nodes))
    ]
    seed_indices = []
    for column, seed in enumerate(seed_tuple):
        seed_index = node_index[seed]
        seed_indices.append(seed_index)
        restart_components[seed_index][column] = restart_share

    components = [row.copy() for row in restart_components]
    damping = 1.0 - restart_probability
    residual = float("inf")
    max_seed_residual = float("inf")
    for iteration in range(1, max_iterations + 1):
        next_components = [
            [restart_probability * value for value in row]
            for row in restart_components
        ]
        dangling_mass = [0.0] * seed_count
        for source, targets in enumerate(targets_by_source):
            source_components = components[source]
            if not targets:
                for column, value in enumerate(source_components):
                    dangling_mass[column] += value
                continue
            edge_scale = damping / len(targets)
            contribution = [value * edge_scale for value in source_components]
            for target in targets:
                target_components = next_components[target]
                for column, value in enumerate(contribution):
                    target_components[column] += value

        dangling_scale = damping / seed_count
        for seed_index in seed_indices:
            target_components = next_components[seed_index]
            for column, value in enumerate(dangling_mass):
                target_components[column] += value * dangling_scale

        residual = 0.0
        seed_residuals = [0.0] * seed_count
        for next_row, current_row in zip(next_components, components):
            differences = [
                next_value - current_value
                for next_value, current_value in zip(next_row, current_row)
            ]
            residual += abs(sum(differences))
            for column, difference in enumerate(differences):
                seed_residuals[column] += abs(difference)
        max_seed_residual = max(seed_residuals)
        components = next_components
        if residual < tolerance and max_seed_residual < tolerance:
            break
    else:
        raise RuntimeError(
            "random walk failed to converge after "
            f"{max_iterations} iterations; residual={residual}; "
            f"maximum_source_residual={max_seed_residual}"
        )

    scores = tuple(sum(row) for row in components)
    return RandomWalkResult(
        nodes=nodes,
        scores=scores,
        seed_components=tuple(tuple(row) for row in components),
        in_degrees=tuple(in_degrees),
        out_degrees=tuple(len(targets) for targets in targets_by_source),
        iterations=iteration,
        l1_residual=residual,
        max_seed_l1_residual=max_seed_residual,
        probability_mass=sum(scores),
        directed_edge_count=sum(len(targets) for targets in targets_by_source),
    )
