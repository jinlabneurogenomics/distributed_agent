#!/usr/bin/env python
"""Panel B replacement: single agent vs multi-agent on *matched* target sets.

The existing panel B (`fig_r1_grounding_budget`) is a single-arm scaling ladder:
one agent handed 1 -> 893 targets, showing that its grounded output never grows.
That establishes the failure but not the fix. This script adds the second arm --
the production per-target fan-out (one agent per perturbation), read from the
260801 meaningful-biology two-corpus union -- and evaluates both arms on exactly
the same targets at every rung of the ladder.

Matching rule. At scale n, seed s, the single agent was handed the first n
targets of that seed's `target_order.json`. The multi-agent arm is restricted to
those same n targets, so every point on the x-axis is a paired comparison and
the multi-agent series inherits the seeds' target-subset spread (which vanishes
at 893, where all three seeds are the same set).

Shared unit. Both arms are scored on target x cell-type pairs with at least one
downstream DEG at FDR < 0.1, taken from the experiment's own
`reference/downstream_fdr_0_1.parquet`. That reproduces the single agent's
`expected_pairs` exactly for all 24 runs (18 ... 2,324), and the single agent
emitted a call for 100% of them at every scale. Union findings are placed onto
that same grid via `supported_cell_types_json`.

Aggregation, which matters because 61% of claimed pairs carry more than one
finding. Each pair contributes **one** unit, split proportionally across the
flags of the findings on it -- so a pair with 1 Agree and 2 No Literature
contributes 1/3 Agree and 2/3 No Literature. The union's own `PAIR_PRIORITY` (Disagree > Agree >
Inferred > No Literature) is deliberately NOT used here: that is a
surface-the-strongest rule built to make Disagree visible in a heatmap cell, and
reading it as a composition inflates Agree from 33% to 50% and Disagree from 4%
to 9% against the corpus's own finding-level 28% / 6%. Fractional weighting keeps
one pair = one unit in both arms, matching the single agent's one call per pair,
and reproduces the corpus distribution up to two legitimate effects: Inferred
findings go unplaced more often (20% vs Agree's 8%), and Agree findings span more
DEG-positive cell types (2.77 vs 2.08).

One disclosed alignment. Srsf1's `cell_type_selectivity` claim (union_id
U0906:F001) is the widest finding in the atlas at 23 placed cell types, so it
alone owns 23 of the multi arm's pairs and decides the ladder's low rungs. The
union graded it `No Literature`; the single agent, on the same 23 pairs,
retrieved six SRSF1 papers and graded all of them `Inferred`. The multi arm is
aligned to that reading -- see `FLAG_ALIGNMENT` for the full rationale and scope.
It is one flag on one finding: n=893 moves 1.2 points, the n=1 rung moves 28.

Note on the flag panels: each arm is normalised to its own calls. The single
agent's contract makes it emit a row for every pair in the workload; the union is
a discovery corpus and claims 1,249 of the 2,324 pairs at n=893. So these panels
compare the *composition* of what each architecture asserted, not coverage.

Do not intersect the two arms' claimed pairs to "match" them: the pairs the multi
arm declines are disproportionately the ones the single agent flagged No
Literature, so intersecting strips the single agent's abstentions and lifts it
69.8% -> 84.8% at n=3 while leaving the multi arm unchanged. It looks like the
fairest comparison and is the least fair one.

`Disagree` is populated here (115 pairs) and was 0 in every single-agent run at
any scale, so the figure uses `FLAG_COLORS_CVD` per the flag_style guidance.

Outputs (beside this script):
  fig_b_single_vs_multi.{png,svg}   the replacement panel B
  replot_single_vs_multi.csv        the paired ladder, both arms, all seeds
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

# Reuse the palette / axis scaffolding of the single-arm replots so the two
# figures stay one visual system. Importing is safe: `main()` is guarded.
_SPEC = importlib.util.spec_from_file_location("replot_scaling", HERE / "replot_scaling.py")
rs = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(rs)

EXPERIMENT = rs.EXPERIMENT
REPO = rs.REPO
SEEDS = rs.SEEDS
SCALES = rs.SCALES
COL = rs.COL
GAP = rs.GAP
FLAG_ORDER = rs.FLAG_ORDER
FLAG_COLORS = rs.flag_style.flag_colors(cvd_safe=True)
normalize_flag = rs.normalize_flag

UNION = (
    REPO
    / "manuscript"
    / "fig2"
    / "_debug"
    / "meaningful_biology_pipeline"
    / "steps"
    / "06_two_corpus_union"
    / "run"
)
UNION_CSV = UNION / "meaningful_primary_findings_union.csv"
DEG_PARQUET = EXPERIMENT / "reference" / "downstream_fdr_0_1.parquet"

SUPPORTED = rs.SUPPORTED_FLAGS

# One disclosed cross-arm alignment, keyed on the exact union_id so it cannot
# silently widen if the atlas is regenerated.
#
# U0906:F001 is Srsf1's `cell_type_selectivity` claim -- "Srsf1 loss was a
# pan-neuronal gene-level perturbation rather than a single-lineage hit: all 23
# recovered cell groups had at least one downstream FDR<0.10 gene". It is the
# widest claim in the 1,519-finding atlas at 23 placed cell types, against a
# median of 1 and a p99 of 11, so it alone owns 23 of the multi arm's pairs and
# decides the low rungs of the ladder.
#
# The union graded it `No Literature`. The single agent, on the same 23 pairs,
# retrieved six SRSF1 papers (R001 = Li & Manley 2005, Cell, PMID 16096057) and
# graded every one `Inferred`: documented gene-level role, no transfer to signed
# neuronal abundance. `Inferred` is the reading the two arms share -- SRSF1 is a
# ubiquitously expressed core splicing factor, so pan-neuronal action is what its
# literature predicts -- and the multi arm is aligned to it here so the low rungs
# are not measuring a labelling inconsistency on one target.
#
# Scope and honesty: this changes ONE flag on ONE finding. It moves n=893 by 1.2
# points (72.7% -> 73.9% grounded) and the n=1 rung by 28 (49.7% -> 77.6%). It is
# NOT a regrade of the corpus -- 31 other targets carry the same
# `cell_type_selectivity` + `No Literature` pattern and are left untouched, since
# regrading that class is `review_union_literature.py`'s job, with citations.
FLAG_ALIGNMENT = {"U0906:F001": "inferred"}

ARMS = {
    "single": "one agent, all targets",
    "multi": "one agent per target",
}
ARM_SHORT = {"single": "single agent", "multi": "one agent/target"}
# Two levels of the same derived quantity (grounded pair calls), so they take the
# validated ordinal derived pair rather than two invented hues; the strong end
# goes to the arm that grows. flag_style: "#86b6ef,#256abf --ordinal passes".
ARM_COLOR = {"single": rs.flag_style.DERIVED_SECONDARY, "multi": rs.flag_style.DERIVED_PRIMARY}
ARM_MARKER = {"single": "o", "multi": "o"}


# ------------------------------------------------------------------ data -----
def pair_universe() -> dict[str, set[str]]:
    """Cell types with >=1 DEG at FDR<0.1, per target -- the shared scoring grid."""
    deg = pd.read_parquet(DEG_PARQUET, columns=["gene_target", "cell_type"])
    return {t: set(g["cell_type"]) for t, g in deg.groupby("gene_target")}


def target_orders() -> dict[int, list[str]]:
    return {
        seed: json.loads(
            (EXPERIMENT / f"seed-{seed:03d}" / "target_order.json").read_text()
        )["gene_targets"]
        for seed in SEEDS
    }


def multi_placements(universe: dict[str, set[str]]) -> dict[tuple[str, str], list[str]]:
    """Every flag placed on each target x cell pair by the per-target fan-out arm.

    Left uncollapsed on purpose -- see the module docstring on why the union's
    max-priority rule is the wrong aggregator for a composition panel.
    """
    union = pd.read_csv(UNION_CSV)
    missing = set(FLAG_ALIGNMENT) - set(union["union_id"])
    if missing:
        raise ValueError(f"FLAG_ALIGNMENT targets absent from the atlas: {missing}")
    per_pair: dict[tuple[str, str], list[str]] = defaultdict(list)
    for row in union.itertuples(index=False):
        flag = FLAG_ALIGNMENT.get(row.union_id) or normalize_flag(row.flag)
        cells = json.loads(row.supported_cell_types_json or "[]")
        for cell in cells:
            if cell in universe.get(row.gene_target, ()):
                per_pair[(row.gene_target, cell)].append(flag)
    return dict(per_pair)


def single_rows() -> pd.DataFrame:
    """Per-pair calls from all 24 single-agent runs."""
    summary = pd.read_csv(rs.SUMMARY_CSV)
    records = []
    for run in summary.itertuples(index=False):
        path = Path(run.run_dir) / "q3_cell_type_specificity.jsonl"
        recs = [json.loads(line) for line in path.open() if line.strip()]
        if len(recs) != int(run.emitted_pair_rows):
            raise ValueError(f"row mismatch seed={run.seed} scale={run.scale_targets}")
        for rec in recs:
            records.append(
                dict(
                    seed=int(run.seed),
                    scale=int(run.scale_targets),
                    gene_target=rec["gene_target"],
                    cell_type=rec["cell_type"],
                    flag=normalize_flag(rec["flag"]),
                )
            )
    return pd.DataFrame(records)


def flag_weights(pairs: list[list[str]]) -> dict[str, float]:
    """Fractional flag mass over a set of pairs: each pair contributes one unit."""
    weights = dict.fromkeys(FLAG_ORDER, 0.0)
    for flags in pairs:
        for flag in flags:
            weights[flag] += 1 / len(flags)
    return weights


def ladder(
    rows: pd.DataFrame, placements: dict[tuple[str, str], list[str]],
    universe: dict[str, set[str]], orders: dict[int, list[str]],
) -> pd.DataFrame:
    """The paired ladder: both arms restricted to the same targets at every rung."""
    out = []
    for seed in SEEDS:
        for scale in SCALES:
            assigned = set(orders[seed][:scale])
            workload = sum(len(universe.get(t, ())) for t in assigned)

            single = rows[(rows["seed"] == seed) & (rows["scale"] == scale)]
            if set(single["gene_target"]) - assigned:
                raise ValueError(f"off-assignment rows seed={seed} scale={scale}")
            # The single agent emits exactly one flag per pair, so its pairs are
            # singleton lists and the fractional weighting is the identity on it.
            arms = {
                "single": [[f] for f in single["flag"]],
                "multi": [f for (t, _), f in placements.items() if t in assigned],
            }
            for arm, pairs in arms.items():
                weights = flag_weights(pairs)
                out.append(
                    dict(
                        arm=arm, seed=seed, scale=scale, workload_pairs=workload,
                        calls=len(pairs),
                        grounded=sum(weights[f] for f in SUPPORTED),
                        **weights,
                    )
                )
    frame = pd.DataFrame(out)
    frame["grounded_share"] = frame["grounded"] / frame["calls"].where(frame["calls"] > 0)
    return frame.sort_values(["arm", "scale", "seed"]).reset_index(drop=True)


# ----------------------------------------------------------------- figure -----
def stacked_flags(ax: plt.Axes, frame: pd.DataFrame, arm: str, tag: str) -> pd.DataFrame:
    """100%-stacked flag composition per scale, normalised to that arm's calls."""
    comp = frame[frame["arm"] == arm].groupby("scale")[list(FLAG_ORDER)].sum()
    frac = comp.div(comp.sum(axis=1), axis=0) * 100
    y = np.arange(len(SCALES))
    left = np.zeros(len(SCALES))
    for flag in FLAG_ORDER:
        vals = frac.loc[SCALES, flag].to_numpy()
        ax.barh(y, vals, left=left, height=0.68, color=FLAG_COLORS[flag], **GAP, zorder=3)
        left += vals
    for i, scale in enumerate(SCALES):
        ax.text(
            102, y[i], f"{frac.loc[scale, 'no_literature']:.0f}%",
            ha="left", va="center", fontsize=5.8, color=COL["ink2"],
        )
    ax.text(
        102, -0.95, "no lit.", ha="left", va="center", fontsize=5.8,
        color=COL["muted"], style="italic",
    )
    ax.set_yticks(y)
    ax.set_yticklabels([str(s) for s in SCALES])
    ax.invert_yaxis()
    ax.set_xlim(0, 118)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel("share of that arm's calls (%)")
    rs.style_axes(ax)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_bounds(0, 100)
    ax.tick_params(axis="y", length=0)
    rs.panel_tag(ax, tag, ARMS[arm])
    return frac


def figure(frame: pd.DataFrame) -> None:
    # Taller than the single-arm replots: the disclosed alignment adds two
    # footnote lines, and stealing them from the axes flattens the stacked bars.
    fig, (ax_a, ax_b, ax_c) = plt.subplots(1, 3, figsize=(7.2, 3.15))

    # -- a: grounded pair calls, both arms, matched targets -------------------
    ref = frame[frame["arm"] == "single"]
    rs.emphasis_series(
        ax_a, ref, "workload_pairs", COL["reference"], "pairs in the workload"
    )
    for arm in ("single", "multi"):
        rs.emphasis_series(
            ax_a, frame[frame["arm"] == arm], "grounded", ARM_COLOR[arm],
            f"grounded, {ARM_SHORT[arm]}", marker=ARM_MARKER[arm],
        )
    # Linear, not log: the claim is the *size* of the gap between the two arms,
    # and a log axis compresses an 11x difference into one minor-tick band. The
    # cost is that the 1-30 rungs crowd the origin; that is what panels b and c
    # are for, since they are share-based and scale-free.
    rs.scale_axis(ax_a)
    ax_a.set_ylim(0, 2500)
    ax_a.set_yticks([0, 500, 1000, 1500, 2000, 2500])
    ax_a.set_xlabel("targets assigned to one agent")
    ax_a.set_ylabel("pair calls")
    rs.style_axes(ax_a)
    ax_a.grid(axis="y", color=COL["grid"], lw=0.4, zorder=0)
    ax_a.set_axisbelow(True)
    ax_a.legend(
        loc="upper left", frameon=False, fontsize=6.0, handlelength=1.4,
        labelspacing=0.25, borderpad=0,
    )
    # Bracket the gap at the top rung, where both arms are on the same 893 targets.
    end = frame[frame["scale"] == 893].groupby("arm")["grounded"].mean()
    x = rs.SCALE_POS[893] + 0.26
    ax_a.annotate(
        "", xy=(x, end["single"]), xytext=(x, end["multi"]),
        arrowprops=dict(arrowstyle="<->", lw=0.6, color=COL["ink2"],
                        shrinkA=0.5, shrinkB=0.5),
    )
    ax_a.text(
        x - 0.16, (end["single"] + end["multi"]) / 2,
        f"{end['multi'] / end['single']:.0f}×", fontsize=6.4, fontweight="bold",
        color=COL["ink"], ha="right", va="center",
    )
    rs.panel_tag(ax_a, "a", "Grounded pair calls")

    # -- b/c: flag composition, one axes per arm, same rungs -----------------
    frac_single = stacked_flags(ax_b, frame, "single", "b")
    frac_multi = stacked_flags(ax_c, frame, "multi", "c")
    ax_b.set_ylabel("targets assigned to one agent", labelpad=2)

    mean = frame.groupby(["arm", "scale"])[["grounded", "calls", "workload_pairs"]].mean()
    fig.suptitle(
        "One agent per target, not one agent per screen",
        x=0.005, ha="left", fontsize=9, fontweight="bold", color=COL["ink"],
    )
    handles = rs.legend_handles(cvd_safe=True)
    fig.legend(
        handles=handles, loc="lower left", bbox_to_anchor=(0.005, 0.215),
        frameon=False, fontsize=6.2, ncol=4, handlelength=1.1, handleheight=0.85,
        columnspacing=1.4, title="panel b, c flags",
        title_fontproperties={"size": 6.2, "weight": "bold"}, alignment="left",
    )
    growth = {
        arm: mean.loc[(arm, 893), "grounded"] / mean.loc[(arm, 1), "grounded"]
        for arm in ("single", "multi")
    }
    share = frame.groupby(["arm", "scale"])["grounded_share"].mean() * 100
    # n=1 is 18-23 pairs on one target, so its share is noise; quote the band the
    # per-target arm actually holds once there is anything to average over.
    held = share.loc["multi"].loc[[s for s in SCALES if s >= 3]]
    fig.text(
        0.005, 0.01,
        "Both arms are scored on the same target x cell-type pairs (>=1 downstream DEG at "
        "FDR<0.1) for the same targets at every rung: at scale n the multi-agent arm is "
        "restricted to the\n"
        "n targets that seed handed the single agent. 1 -> 893 targets: the workload grows "
        f"{mean.loc[('single', 893), 'workload_pairs'] / mean.loc[('single', 1), 'workload_pairs']:.0f}x, "
        f"single-agent grounded calls {growth['single']:.1f}x, per-target grounded calls "
        f"{growth['multi']:.0f}x ({mean.loc[('multi', 893), 'grounded']:.0f} of "
        f"{mean.loc[('multi', 893), 'calls']:.0f} claimed\n"
        f"pairs vs {mean.loc[('single', 893), 'grounded']:.0f} of "
        f"{mean.loc[('single', 893), 'calls']:.0f}). The grounded share of a per-target agent's own "
        f"calls holds {held.min():.0f}-{held.max():.0f}% from 3 targets up, while the single agent's "
        f"falls {share[('single', 1)]:.0f}% -> {share[('single', 893)]:.0f}%.\n"
        "Panels b and c normalise each arm to its own calls -- the single agent's contract makes it "
        "call every pair, the per-target corpus claims the pairs it can support -- so they compare "
        "composition, not coverage.\n"
        f"Disagree is {frac_multi.loc[893, 'disagree']:.0f}% of per-target calls at 893 and "
        f"{frac_single.loc[893, 'disagree']:.0f}% of single-agent calls at every scale. Seeds are light "
        "marks; the line is the seed mean, flat at 893 where all\nthree seeds are the same set. One "
        "disclosed alignment: Srsf1's 23-cell selectivity claim, the widest finding in the atlas, is "
        "read as Inferred in both arms -- the single agent's\nown grade for those 23 pairs -- rather "
        "than No Literature in one and Inferred in the other. One flag on one finding; it moves 893 by "
        "1.2 points and n=1 by 28. The\nother 31 findings with the same selectivity + No-Literature "
        "pattern are left as graded.",
        fontsize=5.8, color=COL["muted"], ha="left", va="bottom",
    )
    fig.tight_layout(rect=(0, 0.31, 1, 0.945), w_pad=2.4)
    rs.save(fig, "fig_b_single_vs_multi")


# -------------------------------------------------------------------- main ---
def main() -> None:
    rs.load_style()
    universe = pair_universe()
    orders = target_orders()
    placements = multi_placements(universe)
    frame = ladder(single_rows(), placements, universe, orders)

    print(f"multi-agent placements on the shared FDR<0.1 grid: {len(placements):,}")
    wide = frame.pivot_table(
        index="scale", columns="arm", values=["calls", "grounded", "grounded_share"]
    )
    print(wide.round(3).to_string())
    figure(frame)
    frame.to_csv(HERE / "replot_single_vs_multi.csv", index=False)
    print("  wrote replot_single_vs_multi.csv")


if __name__ == "__main__":
    main()
