#!/usr/bin/env python
"""Panel B with the multi arm read from the full 260713 production corpus.

`replot_multiagent.py` scores the per-target arm from the 260801 union's primary
atlas: 1,519 findings, citation-reviewed flags, but only 1,249 of the 2,324 shared
pairs (53.7%) and 373 of the 893 targets (41.8%), because a primary atlas is a
conservative distillation. This variant instead reads every finding in
`PerturbAI_findings_260713_rosalind_j768_reports_2045.jsonl` -- the 2,045
per-target production agents themselves, 10,232 findings -- and takes each
finding's own `lit_direction`.

What that buys.

1. Coverage: 2,230 / 2,324 pairs (96.0%) and 892 / 893 targets (99.9%), against
   the single agent's 100% by contract. The two arms are now matched on coverage,
   so panels b and c compare composition over nearly the same denominator instead
   of 54% vs 100%. The non-anchor remainder does this work: the 1,071 promoted
   anchors alone reach 298 targets, the rest reach 888.
2. Symmetry: both arms are now self-graded under comparable contracts.
   `lit_direction` is a controlled four-value field that normalizes onto the
   canonical axis with no loss (`ambiguous` is the pre-rename `inferred`, see
   flag_style._ALIASES): 3,781 / 2,460 / 2,172 / 1,698 with only 121 missing
   across 10,232 findings. These findings also carry `lit_context` with the same
   five-value mismatch vocabulary the single agent's q3 contract uses. The union's
   flags, by contrast, come from a dedicated stage-2 citation review that the
   single agent never got -- strictly stronger, and asymmetric.
3. No cross-arm alignment needed. `FLAG_ALIGNMENT` in replot_multiagent.py patches
   a labelling inconsistency between the union's review and the single agent's
   grading of Srsf1. Here the multi arm's flags come from the same generation the
   single agent is compared against, so that patch is dropped, not carried.

What it costs, stated plainly: these flags are NOT citation-reviewed. Self-reported
`disagree` runs 17.8% of pair mass here against 6.6% in the union's reviewed atlas,
so the union's stage-2 pass demoted roughly two thirds of self-reported
disagreements. This figure therefore reports what the production system asserted,
not what survives citation review. The union version is the right figure for the
latter question; the two answer different things and are worth keeping as a pair.

Everything else matches `replot_multiagent.py`: same shared pair grid (target x
cell-type with >=1 downstream DEG at FDR<0.1, reproducing the single agent's
`expected_pairs` for all 24 runs), same per-seed matching at every rung, same
fractional aggregation (one pair = one unit, split across the flags placed on it),
same CVD flag colors.

Outputs (beside this script):
  fig_b_single_vs_multi_260713.{png,svg}
  replot_single_vs_multi_260713.csv
"""

from __future__ import annotations

import importlib.util
import json
from collections import defaultdict
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mam = _load("replot_multiagent")
rs = mam.rs

SCALES = mam.SCALES
SEEDS = mam.SEEDS
COL = mam.COL
GAP = mam.GAP
FLAG_ORDER = mam.FLAG_ORDER
FLAG_COLORS = mam.FLAG_COLORS
SUPPORTED = mam.SUPPORTED
ARM_COLOR = mam.ARM_COLOR
ARMS = mam.ARMS
ARM_SHORT = mam.ARM_SHORT
normalize_flag = mam.normalize_flag

REPORTS = mam.REPO / "data" / "PerturbAI_findings_260713_rosalind_j768_reports_2045.jsonl"
POS = [rs.SCALE_POS[s] for s in SCALES]


# ------------------------------------------------------------------ data -----
def jsonl_section(report: str, header: str) -> list[dict]:
    """The fenced JSONL block under `header`, same convention run_union.py uses."""
    start = report.find(header)
    if start < 0:
        return []
    out: list[dict] = []
    for line in report[start:].splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        elif out and line.startswith("#"):
            break
    return out


def production_placements(universe: dict[str, set[str]]) -> tuple[dict, dict[str, int]]:
    """Every 260713 finding's `lit_direction`, placed on the shared pair grid."""
    per_pair: dict[tuple[str, str], list[str]] = defaultdict(list)
    stats = {"findings": 0, "no_flag": 0, "placed": 0}
    with REPORTS.open() as handle:
        for line in handle:
            row = json.loads(line)
            target = row["gene_target"]
            for finding in jsonl_section(row["report"], "Biological Findings JSONL"):
                stats["findings"] += 1
                direction = finding.get("lit_direction")
                if not isinstance(direction, str):
                    stats["no_flag"] += 1
                    continue
                flag = normalize_flag(direction)
                hit = False
                for cell in finding.get("cell_types") or []:
                    if cell in universe.get(target, ()):
                        per_pair[(target, cell)].append(flag)
                        hit = True
                stats["placed"] += hit
    return dict(per_pair), stats


def ladder(rows, placements, universe, orders) -> pd.DataFrame:
    out = []
    for seed in SEEDS:
        for scale in SCALES:
            assigned = set(orders[seed][:scale])
            workload = sum(len(universe.get(t, ())) for t in assigned)
            single = rows[(rows["seed"] == seed) & (rows["scale"] == scale)]
            arms = {
                "single": [[f] for f in single["flag"]],
                "multi": [f for (t, _), f in placements.items() if t in assigned],
            }
            for arm, pairs in arms.items():
                w = mam.flag_weights(pairs)
                out.append(dict(
                    arm=arm, seed=seed, scale=scale, workload_pairs=workload,
                    calls=len(pairs), grounded=sum(w[f] for f in SUPPORTED), **w,
                ))
    frame = pd.DataFrame(out)
    frame["grounded_share"] = frame["grounded"] / frame["calls"].where(frame["calls"] > 0)
    return frame.sort_values(["arm", "scale", "seed"]).reset_index(drop=True)


# ----------------------------------------------------------------- figure -----
def figure(frame: pd.DataFrame, stats: dict[str, int]) -> None:
    fig, (ax_a, ax_b, ax_c) = plt.subplots(1, 3, figsize=(7.2, 3.15))

    # -- a: grounded pair calls, linear so the gap reads as a size -----------
    ref = frame[frame["arm"] == "single"]
    rs.emphasis_series(ax_a, ref, "workload_pairs", COL["reference"], "pairs in the workload")
    # With 96% coverage the multi arm's claimed pairs nearly overlay the workload;
    # showing it makes the coverage match visible instead of a footnote claim.
    claimed = frame[frame["arm"] == "multi"].groupby("scale")["calls"].mean()
    ax_a.plot(POS, claimed.loc[SCALES], color=ARM_COLOR["multi"], lw=0.9,
              ls=(0, (2.6, 1.5)), zorder=3, label="claimed, one agent/target")
    for arm in ("single", "multi"):
        rs.emphasis_series(ax_a, frame[frame["arm"] == arm], "grounded",
                           ARM_COLOR[arm], f"grounded, {ARM_SHORT[arm]}")
    rs.scale_axis(ax_a)
    ax_a.set_ylim(0, 2500)
    ax_a.set_yticks([0, 500, 1000, 1500, 2000, 2500])
    ax_a.set_xlabel("targets assigned to one agent")
    ax_a.set_ylabel("pair calls")
    rs.style_axes(ax_a)
    ax_a.grid(axis="y", color=COL["grid"], lw=0.4, zorder=0)
    ax_a.set_axisbelow(True)
    ax_a.legend(loc="upper left", frameon=False, fontsize=5.8, handlelength=1.4,
                labelspacing=0.25, borderpad=0)
    end = frame[frame["scale"] == 893].groupby("arm")["grounded"].mean()
    x = rs.SCALE_POS[893] + 0.26
    ax_a.annotate("", xy=(x, end["single"]), xytext=(x, end["multi"]),
                  arrowprops=dict(arrowstyle="<->", lw=0.6, color=COL["ink2"],
                                  shrinkA=0.5, shrinkB=0.5))
    ax_a.text(x - 0.16, (end["single"] + end["multi"]) / 2,
              f"{end['multi'] / end['single']:.0f}×", fontsize=6.4, fontweight="bold",
              color=COL["ink"], ha="right", va="center")
    rs.panel_tag(ax_a, "a", "Grounded pair calls")

    frac = {}
    for arm, ax, tag in (("single", ax_b, "b"), ("multi", ax_c, "c")):
        frac[arm] = mam.stacked_flags(ax, frame, arm, tag)

    fig.suptitle(
        "Matched on coverage: both arms call ~all of the same pairs",
        x=0.005, ha="left", fontsize=9, fontweight="bold", color=COL["ink"],
    )
    fig.legend(
        handles=rs.legend_handles(cvd_safe=True), loc="lower left",
        bbox_to_anchor=(0.005, 0.215), frameon=False, fontsize=6.2, ncol=4,
        handlelength=1.1, handleheight=0.85, columnspacing=1.4, title="panel b, c flags",
        title_fontproperties={"size": 6.2, "weight": "bold"}, alignment="left",
    )
    mean = frame.groupby(["arm", "scale"])[["grounded", "calls", "workload_pairs"]].mean()
    share = frame.groupby(["arm", "scale"])["grounded_share"].mean() * 100
    fig.text(
        0.005, 0.01,
        "The per-target arm is every finding in the 260713 production corpus (2,045 per-target agents, "
        f"{stats['findings']:,} findings on all targets), flagged by each finding's own\n`lit_direction` "
        "— a controlled field that maps onto this axis without loss. It claims "
        f"{mean.loc[('multi', 893), 'calls']:,.0f} of {mean.loc[('single', 893), 'workload_pairs']:,.0f} "
        f"pairs ({100 * mean.loc[('multi', 893), 'calls'] / mean.loc[('single', 893), 'workload_pairs']:.0f}%) "
        "against the single agent's 100% by contract, so b and c\nnow compare composition over nearly the "
        f"same denominator. At 893: {mean.loc[('multi', 893), 'grounded']:,.0f} grounded pair calls vs "
        f"{mean.loc[('single', 893), 'grounded']:.0f}, and the grounded share of each arm's own calls is "
        f"{share[('multi', 893)]:.0f}% vs {share[('single', 893)]:.0f}%.\nBoth arms are self-graded here, "
        "which the union-atlas version is not: its flags come from a stage-2 citation review the single "
        "agent never got. The cost is that these flags are\nunreviewed — self-reported Disagree is "
        f"{frac['multi'].loc[893, 'disagree']:.0f}% of per-target pair mass against 6.6% in the reviewed "
        "atlas, so review demotes roughly two thirds of them. Fractional aggregation, seeds as light "
        "marks.",
        fontsize=5.8, color=COL["muted"], ha="left", va="bottom",
    )
    fig.tight_layout(rect=(0, 0.31, 1, 0.945), w_pad=2.4)
    rs.save(fig, "fig_b_single_vs_multi_260713")


# -------------------------------------------------------------------- main ---
def main() -> None:
    rs.load_style()
    universe = mam.pair_universe()
    orders = mam.target_orders()
    placements, stats = production_placements(universe)
    frame = ladder(mam.single_rows(), placements, universe, orders)

    grid = sum(len(universe[t]) for t in orders[SEEDS[0]])
    print(f"260713: {stats['findings']:,} findings, {stats['no_flag']:,} without lit_direction")
    print(f"placed on the shared grid: {len(placements):,}/{grid:,} pairs "
          f"({100 * len(placements) / grid:.1f}%)")
    print(frame.pivot_table(index="scale", columns="arm",
                            values=["calls", "grounded", "grounded_share"]).round(3).to_string())
    figure(frame, stats)
    frame.to_csv(HERE / "replot_single_vs_multi_260713.csv", index=False)
    print("  wrote replot_single_vs_multi_260713.csv")


if __name__ == "__main__":
    main()
