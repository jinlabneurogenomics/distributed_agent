#!/usr/bin/env python3
"""Build deterministic mixed, rank-stratified packets for cluster-description review."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def make_packets(clusters: list[dict], packet_count: int) -> list[dict]:
    """Give every reviewer one cluster per rank stratum while balancing findings."""
    if packet_count < 1:
        raise ValueError("packet_count must be positive")
    packets = [
        {
            "packet_id": f"CR{i + 1:02d}",
            "cluster_ids": [],
            "prose_paths": [],
            "finding_count": 0,
        }
        for i in range(packet_count)
    ]
    for start in range(0, len(clusters), packet_count):
        stratum = clusters[start : start + packet_count]
        available = list(packets)
        # Within each consecutive rank stratum, place the largest units first
        # into the currently lightest packets. This preserves rank coverage and
        # avoids one reader receiving all of the large communities.
        for cluster in sorted(
            stratum,
            key=lambda item: (-int(item.get("n") or 0), str(item["cluster_id"])),
        ):
            packet = min(
                available,
                key=lambda item: (
                    item["finding_count"],
                    len(item["cluster_ids"]),
                    item["packet_id"],
                ),
            )
            packet["cluster_ids"].append(cluster["cluster_id"])
            packet["prose_paths"].append(cluster["prose_index"])
            packet["finding_count"] += int(cluster.get("n") or 0)
            available.remove(packet)
    return packets


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clusters-in", required=True)
    parser.add_argument("--packets", required=True, type=int)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    clusters_path = Path(args.clusters_in).resolve()
    clusters = json.loads(clusters_path.read_text())
    if not isinstance(clusters, list):
        raise SystemExit("clusters input must be a JSON list")
    packets = make_packets(clusters, args.packets)
    payload = {
        "method": "rank-stratified balanced cluster-description packets",
        "clusters_path": str(clusters_path),
        "input_cluster_count": len(clusters),
        "input_finding_count": sum(int(cluster.get("n") or 0) for cluster in clusters),
        "packet_count": len(packets),
        "packets": packets,
    }
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n")
    temporary.replace(output)
    print(
        f"packed {payload['input_cluster_count']} clusters / "
        f"{payload['input_finding_count']} findings into {len(packets)} review packets; "
        f"packet findings={[packet['finding_count'] for packet in packets]}"
    )


if __name__ == "__main__":
    main()
