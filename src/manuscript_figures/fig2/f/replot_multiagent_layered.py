#!/usr/bin/env python
"""Panel B with a layered multi arm: reviewed atlas first, 260713 fills the gaps.

Panel a uses the June 2,046-report corpus for the per-target arm's final
reference-entry counts. Panels b and c retain the reviewed-atlas / 260713 flag
layering described below; panel a is independent of those flag sources.

The two earlier variants trade coverage against flag provenance:

* `replot_multiagent.py` uses the 260801 union primary atlas. Flags are
  citation-reviewed (stage-2, full reference ledgers) but it claims only 1,249 of
  the 2,324 shared pairs (53.7%) and 373 of 893 targets, because a primary atlas is
  a conservative distillation.
* `replot_multiagent_260713.py` uses every finding in the 260713 production corpus.
  Coverage is 2,230 pairs (96.0%) but the flags are each finding's own
  `lit_direction`, never citation-reviewed.

This variant takes the best available provenance per pair: **the reviewed atlas
wherever it placed a call, the 260713 corpus only where it did not.** Precedence is
by pair, not by finding -- a pair the atlas covers is never touched by 260713, so
no pair mixes the two vocabularies.

Result: 2,236 / 2,324 pairs (96.2%) and 893 / 893 targets, 858 of them with at
least one grounded call. 55.9% of covered pairs carry reviewed flags, 44.1% carry
self-reported ones; panel c reports that split per rung so the mix is never
implicit. 88 pairs are covered by neither corpus.

Why the layering is visible in the numbers. The fill is not a neutral extension:
the reviewed layer runs 32.6% Agree / 4.0% Disagree, the fill layer 9.2% Agree /
23.0% Disagree. Same underlying findings generation, but stage-2 review demotes
most self-reported disagreements, so the fill is far more contradictory-looking.
Combined lands between at 22.3% / 12.4%. Grounded share is nearly identical across
the two layers (72.7% vs 74.1%), so the fill costs nothing on grounding -- it only
shifts *which* grounded flag a pair carries.

Everything else matches `replot_multiagent.py`: same shared pair grid, same
per-seed matching at every rung, same fractional aggregation (one pair = one unit,
split across the flags placed on it), same CVD flag colors. `FLAG_ALIGNMENT` is
switched off, so the reviewed atlas is read exactly as graded -- see `layered()`.

Outputs (beside this script):
  fig_b_single_vs_multi_layered.{png,svg}
  replot_single_vs_multi_layered.csv
"""

from __future__ import annotations

import importlib.util
import json
import re
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
new = _load("replot_multiagent_260713")
rs = mam.rs

SCALES, SEEDS = mam.SCALES, mam.SEEDS
COL, GAP = mam.COL, mam.GAP
FLAG_ORDER, FLAG_COLORS = mam.FLAG_ORDER, mam.FLAG_COLORS
SUPPORTED = mam.SUPPORTED
ARM_COLOR, ARM_SHORT = mam.ARM_COLOR, mam.ARM_SHORT
POS = [rs.SCALE_POS[s] for s in SCALES]

SINGLE_REFS: dict[tuple[int, int], int] = {}
REPORT_REFS: dict[str, int] = {}
JUNE_REPORTS = (
    mam.REPO
    / "data"
    / "perturb_sciacc_findings_report_rosalind_full_j768_target_final_outputs.jsonl"
)
EXPECTED_JUNE_REPORTS = 2046
EXPECTED_JUNE_REFERENCE_ENTRIES = 16_555


# ------------------------------------------------------------------ data -----
def layered(universe) -> tuple[dict, dict]:
    """Reviewed atlas placements, plus 260713 placements only where it is silent.

    `FLAG_ALIGNMENT` is switched off for the reviewed layer. It exists in
    replot_multiagent.py to reconcile one Srsf1 label between the union's review
    and the single agent's grading, which was load-bearing there because Srsf1's
    23-cell claim decided the low rungs. Here the reviewed atlas is read exactly as
    graded: the point of this figure is provenance, so patching a reviewed flag
    with the other arm's reading would defeat it.
    """
    saved = dict(mam.FLAG_ALIGNMENT)
    mam.FLAG_ALIGNMENT.clear()
    try:
        reviewed = mam.multi_placements(universe)
    finally:
        mam.FLAG_ALIGNMENT.update(saved)
    production, _ = new.production_placements(universe)
    fill = {pair: flags for pair, flags in production.items() if pair not in reviewed}
    combined = {**reviewed, **fill}
    source = {**{p: "reviewed" for p in reviewed}, **{p: "fill" for p in fill}}
    return combined, source


def single_reference_counts() -> dict[tuple[int, int], int]:
    """References the single agent collected per run, from its own q3_references.jsonl."""
    summary = pd.read_csv(rs.SUMMARY_CSV)
    out = {}
    for run in summary.itertuples(index=False):
        path = _run_dir(run.run_dir) / "q3_references.jsonl"
        out[(int(run.seed), int(run.scale_targets))] = sum(
            1 for line in path.open() if line.strip()
        )
    return out


def _run_dir(recorded: str) -> Path:
    """Resolve pre-move debug paths onto the current manuscript directory."""
    path = Path(recorded)
    if path.is_dir():
        return path
    try:
        results_index = path.parts.index("results")
    except ValueError as exc:
        raise FileNotFoundError(f"Cannot relocate recorded run directory: {path}") from exc
    relocated = rs.EXPERIMENT.joinpath(*path.parts[results_index:])
    if not relocated.is_dir():
        raise FileNotFoundError(
            f"Neither recorded nor relocated run directory exists: {path}, {relocated}"
        )
    return relocated


def single_rows() -> pd.DataFrame:
    """Per-pair calls from all 24 single-agent runs, after path relocation."""
    summary = pd.read_csv(rs.SUMMARY_CSV)
    records = []
    for run in summary.itertuples(index=False):
        path = _run_dir(run.run_dir) / "q3_cell_type_specificity.jsonl"
        rows = [json.loads(line) for line in path.open() if line.strip()]
        if len(rows) != int(run.emitted_pair_rows):
            raise ValueError(
                f"row mismatch seed={run.seed} scale={run.scale_targets}"
            )
        for row in rows:
            records.append(
                {
                    "seed": int(run.seed),
                    "scale": int(run.scale_targets),
                    "gene_target": row["gene_target"],
                    "cell_type": row["cell_type"],
                    "flag": mam.normalize_flag(row["flag"]),
                }
            )
    return pd.DataFrame(records)


def _strict_jsonl_section(report: str, header: str) -> list[dict]:
    """Parse one explicitly headed and fenced JSONL appendix.

    Requiring both the Markdown heading and its JSONL fence avoids the permissive
    substring parser previously used here, which could absorb JSON rows from an
    adjacent appendix when a report mentioned ``References JSONL`` in prose.
    """
    lines = report.splitlines()
    heading = next(
        (
            index
            for index, line in enumerate(lines)
            if re.match(
                rf"^#{{1,6}}\s+{re.escape(header)}\s*$",
                line.strip(),
                re.IGNORECASE,
            )
        ),
        None,
    )
    if heading is None:
        return []
    fence = next(
        (
            index
            for index in range(heading + 1, len(lines))
            if lines[index].strip().lower() == "```jsonl"
        ),
        None,
    )
    if fence is None:
        return []

    rows: list[dict] = []
    for line in lines[fence + 1 :]:
        stripped = line.strip()
        if stripped == "```":
            break
        if not stripped:
            continue
        try:
            row = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            rows.append(row)
    return rows


def report_reference_counts() -> dict[str, int]:
    """Final reference entries in each June report, counted per target."""
    out = {}
    with JUNE_REPORTS.open() as handle:
        for line in handle:
            row = json.loads(line)
            out[row["gene_target"]] = len(
                _strict_jsonl_section(row["final_report"], "References JSONL")
            )
    if len(out) != EXPECTED_JUNE_REPORTS:
        raise RuntimeError(
            f"Expected {EXPECTED_JUNE_REPORTS:,} June reports, found {len(out):,}"
        )
    total = sum(out.values())
    if total != EXPECTED_JUNE_REFERENCE_ENTRIES:
        raise RuntimeError(
            "June reference-entry total drifted: "
            f"expected {EXPECTED_JUNE_REFERENCE_ENTRIES:,}, found {total:,}"
        )
    return out


def ladder(rows, placements, source, universe, orders) -> pd.DataFrame:
    out = []
    for seed in SEEDS:
        for scale in SCALES:
            assigned = set(orders[seed][:scale])
            workload = sum(len(universe.get(t, ())) for t in assigned)
            single = rows[(rows["seed"] == seed) & (rows["scale"] == scale)]
            multi = [(p, f) for p, f in placements.items() if p[0] in assigned]
            arms = {
                "single": ([[f] for f in single["flag"]], 0),
                "multi": ([f for _, f in multi],
                          sum(1 for p, _ in multi if source[p] == "reviewed")),
            }
            for arm, (pairs, reviewed) in arms.items():
                w = mam.flag_weights(pairs)
                out.append(dict(
                    arm=arm, seed=seed, scale=scale, workload_pairs=workload,
                    calls=len(pairs), reviewed_pairs=reviewed,
                    references=(
                        SINGLE_REFS[(seed, scale)] if arm == "single"
                        else sum(REPORT_REFS.get(t, 0) for t in orders[seed][:scale])
                    ),
                    grounded=sum(w[f] for f in SUPPORTED), **w,
                ))
    frame = pd.DataFrame(out)
    frame["grounded_share"] = frame["grounded"] / frame["calls"].where(frame["calls"] > 0)
    return frame.sort_values(["arm", "scale", "seed"]).reset_index(drop=True)


# ----------------------------------------------------------------- figure -----
def stacked_with_provenance(ax, frame: pd.DataFrame) -> pd.DataFrame:
    """Panel c: flag composition plus the reviewed/self-reported split per rung."""
    sub = frame[frame["arm"] == "multi"]
    comp = sub.groupby("scale")[list(FLAG_ORDER)].sum()
    frac = comp.div(comp.sum(axis=1), axis=0) * 100
    reviewed = 100 * sub.groupby("scale")["reviewed_pairs"].sum() / sub.groupby("scale")["calls"].sum()
    y = np.arange(len(SCALES))
    left = np.zeros(len(SCALES))
    for flag in FLAG_ORDER:
        vals = frac.loc[SCALES, flag].to_numpy()
        ax.barh(y, vals, left=left, height=0.68, color=FLAG_COLORS[flag], **GAP, zorder=3)
        left += vals
    for i, scale in enumerate(SCALES):
        ax.text(103, y[i], f"{frac.loc[scale, 'no_literature']:.0f}%", ha="left",
                va="center", fontsize=5.8, color=COL["ink2"])
        ax.text(127, y[i], f"{reviewed.loc[scale]:.0f}%", ha="left", va="center",
                fontsize=5.8, color=ARM_COLOR["multi"])
    ax.text(103, -0.95, "no lit.", ha="left", va="center", fontsize=5.8,
            color=COL["muted"], style="italic")
    ax.text(127, -0.95, "reviewed", ha="left", va="center", fontsize=5.8,
            color=ARM_COLOR["multi"], style="italic")
    ax.set_yticks(y)
    ax.set_yticklabels([str(s) for s in SCALES])
    ax.invert_yaxis()
    ax.set_xlim(0, 152)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel("share of that arm's calls (%)")
    rs.style_axes(ax)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_bounds(0, 100)
    ax.tick_params(axis="y", length=0)
    rs.panel_tag(ax, "c", "one agent per target")
    return frac


def figure(frame: pd.DataFrame, layers: dict[str, dict]) -> None:
    fig, (ax_a, ax_b, ax_c) = plt.subplots(
        1, 3, figsize=(7.4, 3.55), gridspec_kw={"width_ratios": [1, 1, 1.14]}
    )

    # Final reference entries in reports. This is the one panel that does not
    # depend on any flag, aggregation or provenance decision -- it counts the
    # reference ledgers the two architectures produced for the same targets.
    for arm in ("single", "multi"):
        rs.emphasis_series(ax_a, frame[frame["arm"] == arm], "references",
                           ARM_COLOR[arm], ARM_SHORT[arm])
    rs.scale_axis(ax_a)
    end = frame[frame["scale"] == 893].groupby("arm")["references"].mean()
    ax_a.set_ylim(0, end["multi"] * 1.12)
    ax_a.set_xlabel("targets assigned to one agent")
    ax_a.set_ylabel("final reference entries in reports")
    rs.style_axes(ax_a)
    ax_a.grid(axis="y", color=COL["grid"], lw=0.4, zorder=0)
    ax_a.set_axisbelow(True)
    ax_a.legend(loc="upper left", frameon=False, fontsize=6.0, handlelength=1.4,
                labelspacing=0.25, borderpad=0)
    # The single agent's line is indistinguishable from the axis at this scale,
    # which is the finding, so it gets a direct label rather than a legend lookup.
    lo = frame[(frame["arm"] == "single")].groupby("scale")["references"].mean()
    ax_a.annotate(
        f"{lo.loc[1]:.0f} refs at 1 target,\n{lo.loc[893]:.0f} at 893",
        xy=(rs.SCALE_POS[893], lo.loc[893]), xytext=(rs.SCALE_POS[30], end["multi"] * 0.17),
        fontsize=5.9, color=ARM_COLOR["single"], ha="center", va="bottom",
        arrowprops=dict(arrowstyle="->", lw=0.5, color=ARM_COLOR["single"],
                        shrinkA=1, shrinkB=2),
    )
    x = rs.SCALE_POS[893] + 0.26
    ax_a.annotate("", xy=(x, lo.loc[893]), xytext=(x, end["multi"]),
                  arrowprops=dict(arrowstyle="<->", lw=0.6, color=COL["ink2"],
                                  shrinkA=0.5, shrinkB=0.5))
    ax_a.text(x - 0.16, end["multi"] * 0.55, f"{end['multi'] / end['single']:.0f}×",
              fontsize=6.4, fontweight="bold", color=COL["ink"], ha="right", va="center")
    rs.panel_tag(ax_a, "a", "References in final reports")

    frac_single = mam.stacked_flags(ax_b, frame, "single", "b")
    frac_multi = stacked_with_provenance(ax_c, frame)

    fig.suptitle(
        "Reviewed flags where they exist, production flags where they do not",
        x=0.005, ha="left", fontsize=9, fontweight="bold", color=COL["ink"],
    )
    fig.legend(
        handles=rs.legend_handles(cvd_safe=True), loc="lower left",
        bbox_to_anchor=(0.005, 0.315), frameon=False, fontsize=6.2, ncol=4,
        handlelength=1.1, handleheight=0.85, columnspacing=1.4, title="panel b, c flags",
        title_fontproperties={"size": 6.2, "weight": "bold"}, alignment="left",
    )
    mean = frame.groupby(["arm", "scale"])[["grounded", "calls", "workload_pairs"]].mean()
    share = frame.groupby(["arm", "scale"])["grounded_share"].mean() * 100
    a, b = layers["reviewed"], layers["fill"]
    refs = frame.groupby(["arm", "scale"])["references"].mean()
    fig.text(
        0.005, 0.01,
        f"Panel a counts each arm's own final reference ledger — the single agent's q3_references.jsonl per "
        f"run and the June per-target arm's References JSONL per report. It is the one panel that\ndepends "
        f"on no flag, "
        f"aggregation or provenance choice. The single agent collects {refs[('single', 1)]:.0f} references "
        f"on 1 target and {refs[('single', 893)]:.0f} on 893 — a flat "
        f"{frame[frame['arm'] == 'single']['references'].min():.0f}–"
        f"{frame[frame['arm'] == 'single']['references'].max():.0f} across all 24 runs, so it does a\nfixed "
        f"amount of final-reference output whatever the workload; the per-target arm reaches "
        f"{refs[('multi', 893)]:,.0f}, about {refs[('multi', 893)] / 893:.1f} per target.\n\n"
        "Panels b and c: the per-target arm takes the best provenance available per pair — the 260801 union "
        "primary atlas wherever it placed a call (citation-reviewed, stage-2\nwith full reference ledgers), "
        "the 260713 production corpus's own `lit_direction` only where the atlas is silent. Precedence is "
        "by pair, so no pair blends the two\nvocabularies. That reaches "
        f"{mean.loc[('multi', 893), 'calls']:,.0f} of {mean.loc[('single', 893), 'workload_pairs']:,.0f} "
        f"pairs ({100 * mean.loc[('multi', 893), 'calls'] / mean.loc[('single', 893), 'workload_pairs']:.1f}%) "
        f"and all 893 targets, against {len(a):,} pairs (53.7%) and 373 targets for the atlas alone. "
        f"At 893: {mean.loc[('multi', 893), 'grounded']:,.0f} grounded pair calls vs "
        f"{mean.loc[('single', 893), 'grounded']:.0f},\n"
        f"grounded share {share[('multi', 893)]:.0f}% vs {share[('single', 893)]:.0f}%. The 'reviewed' "
        "column in c is the share of that rung's pairs carrying reviewed flags. The fill is not neutral: "
        "the reviewed layer\nruns 32.6% Agree / 4.0% Disagree and the fill layer 9.2% / 23.0%, because "
        "stage-2 review demotes most self-reported disagreements — so combined Disagree "
        f"({frac_multi.loc[893, 'disagree']:.0f}%)\nsits between the two. Grounded share barely differs "
        "between layers (72.7% vs 74.1%), so the fill changes which grounded flag a pair carries, not "
        "whether it is grounded. 88\npairs are covered by neither corpus. Fractional aggregation; seeds "
        "as light marks.",
        fontsize=5.8, color=COL["muted"], ha="left", va="bottom",
    )
    fig.tight_layout(rect=(0, 0.41, 1, 0.95), w_pad=2.3)
    rs.save(fig, "fig_b_single_vs_multi_layered")


# -------------------------------------------------------------------- main ---
def main() -> None:
    rs.load_style()
    universe = mam.pair_universe()
    orders = mam.target_orders()
    combined, source = layered(universe)
    global SINGLE_REFS, REPORT_REFS
    SINGLE_REFS = single_reference_counts()
    REPORT_REFS = report_reference_counts()
    frame = ladder(single_rows(), combined, source, universe, orders)

    grid = sum(len(universe[t]) for t in orders[SEEDS[0]])
    layers = {
        "reviewed": {p: f for p, f in combined.items() if source[p] == "reviewed"},
        "fill": {p: f for p, f in combined.items() if source[p] == "fill"},
    }
    for name, pl in (("reviewed layer", layers["reviewed"]), ("260713 fill", layers["fill"]),
                     ("combined", combined)):
        w = mam.flag_weights(list(pl.values()))
        tot = sum(w.values())
        print(f"{name:16s} pairs={len(pl):5d} ({100 * len(pl) / grid:5.1f}%) "
              f"grounded={100 * sum(w[f] for f in SUPPORTED) / tot:5.1f}%  "
              + "  ".join(f"{f[:5]}={100 * w[f] / tot:4.1f}%" for f in FLAG_ORDER))
    print(f"uncovered by both: {grid - len(combined)} pairs")
    print(frame.pivot_table(index="scale", columns="arm",
                            values=["calls", "grounded", "grounded_share"]).round(3).to_string())
    figure(frame, layers)
    frame.to_csv(HERE / "replot_single_vs_multi_layered.csv", index=False)
    print("  wrote replot_single_vs_multi_layered.csv")


if __name__ == "__main__":
    main()
