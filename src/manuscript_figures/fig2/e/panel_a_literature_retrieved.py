#!/usr/bin/env python
"""Panel a of the layered single-vs-multi figure, as a standalone square panel.

Same content as the first panel of `replot_multiagent_layered.py`: how many final
reference entries each architecture's own ledger contains, per rung. The
per-target arm is counted from the June 2,046-report corpus; the single-agent arm
is counted from each scaling run's `q3_references.jsonl`.
Two things change for the standalone form (`figure-conventions` skill, rules 1-2).

* **Square.** The joint figure gives panel a a wide-ish slot because it shares a
  row with two horizontal bar panels. Alone it has no such constraint, so it goes
  to a 1:1 plotting box — a square panel tiles into a plate without spending the
  plate's width on one series.
* **Axes shifted a little off the data.** In the joint figure the single-agent
  series (3-19 references) lies on the x-spine at a scale that tops out near
  7,600, so the finding "the single agent has a flat, tiny final-reference
  output" is rendered as an absence of ink. Here the limits are pushed just off the
  marks on both axes so that series floats clear of the spine and reads as a
  measurement. The spines are left unbounded, so the frame stays a connected L.

The chrome is the plain house style (`src/figures/style.mplstyle`): white ground,
neutral gray spines and grid. `replot_scaling.load_style()` is deliberately not
used here — it repaints the figure, axes and save surfaces in the warm off-white
(`COL["surface"]`, #fcfcfb) that the replot deck uses, which is not what a panel
destined for the manuscript plate should carry.

Reads `replot_single_vs_multi_layered.csv`, written by the joint script, rather
than recomputing the ladder: the extraction is then provably the same numbers as
the figure it came from.

Outputs (beside this script):
  fig_b_single_vs_multi_layered__a.{png,svg}          3.0 in, all eight rungs labelled
  fig_b_single_vs_multi_layered__a_compact.{png,svg}  2.0 in, thinned ticks
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
CSV = HERE / "replot_single_vs_multi_layered.csv"
STEM = "fig_b_single_vs_multi_layered__a"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


rs = _load("replot_scaling", HERE / "replot_scaling.py")
kit = _load("panel_kit", REPO / "src" / "figures" / "panel_kit.py")

# `emphasis_series` draws marker edges and bar gaps in COL["surface"], i.e. it
# assumes the ground it is drawn on. On the plain house style that ground is
# white, so point it there rather than at the replot deck's off-white.
rs.COL["surface"] = "white"
COL = rs.COL
ARM_COLOR = {"single": rs.flag_style.DERIVED_SECONDARY, "multi": rs.flag_style.DERIVED_PRIMARY}
ARM_SHORT = {"single": "single agent", "multi": "one agent/target"}
# The two arms are the only recurring concepts in this panel; declared so `audit`
# can check they do not collide with each other or with a reserved flag color.
CONCEPTS = {ARM_SHORT[arm]: ARM_COLOR[arm] for arm in ARM_COLOR}

# Clearance as a fraction of the drawn range. Only enough to lift the single
# agent's 3-19 references clear of the bottom spine by more than their own marker
# radius, so the flat line reads as a measurement rather than as the axis.
FLOOR_PAD = 0.05
SIDE_PAD = 0.015  # rung-1 and rung-893 marks off the left spine and the panel edge
YTICKS = [0, 2000, 4000, 6000, 8000]


def panel(ax: plt.Axes, frame: pd.DataFrame) -> None:
    for arm in ("single", "multi"):
        rs.emphasis_series(ax, frame[frame["arm"] == arm], "references",
                           ARM_COLOR[arm], ARM_SHORT[arm])

    end = frame[frame["scale"] == 893].groupby("arm")["references"].mean()
    rs.scale_axis(ax)
    ax.set_ylim(0, end["multi"] * 1.12)
    ax.set_yticks(YTICKS)
    ax.set_xlabel("targets assigned to one agent")
    ax.set_ylabel("final reference entries in reports")

    rs.style_axes(ax)
    kit.breathe(ax, "y", "low", FLOOR_PAD)
    kit.breathe(ax, "x", "both", SIDE_PAD)
    ax.grid(axis="y", zorder=0)  # grid.* from style.mplstyle
    ax.set_axisbelow(True)
    kit.square(ax)
    top = ax.get_ylim()[1]

    ax.legend(loc="upper left", frameon=False, fontsize=6.0, handlelength=1.4,
              labelspacing=0.25, borderpad=0)

    # The single agent's line is flat and near zero, which is the finding, so it
    # gets a direct label rather than a legend lookup.
    lo = frame[frame["arm"] == "single"].groupby("scale")["references"].mean()
    ax.annotate(
        f"{lo.loc[1]:.0f} refs at 1 target,\n{lo.loc[893]:.0f} at 893",
        xy=(rs.SCALE_POS[893], lo.loc[893]),
        xytext=(rs.SCALE_POS[30], top * 0.28),
        fontsize=5.9, color=ARM_COLOR["single"], ha="center", va="bottom",
        arrowprops=dict(arrowstyle="->", lw=0.5, color=ARM_COLOR["single"],
                        shrinkA=1, shrinkB=2),
    )
    x = rs.SCALE_POS[893] + 0.26
    ax.annotate("", xy=(x, lo.loc[893]), xytext=(x, end["multi"]),
                annotation_clip=False,
                arrowprops=dict(arrowstyle="<->", lw=0.6, color=COL["ink2"],
                                shrinkA=0.5, shrinkB=0.5))
    ax.text(x - 0.16, end["multi"] * 0.55, f"{end['multi'] / end['single']:.0f}×",
            fontsize=6.4, fontweight="bold", color=COL["ink"], ha="right", va="center")
    rs.panel_tag(ax, "a", "References in final reports")


def compact_panel(ax: plt.Axes, frame: pd.DataFrame) -> None:
    """The same panel at plate scale: half the size, type at full style size.

    A two-series monotone comparison does not need a 3-inch square. Shrinking the
    box while leaving the type at the style sheet's 7 pt inverts the ratio — the
    labels get larger relative to the panel, which is what makes a small panel
    readable rather than just small.

    Three compressions, all of the *chrome*, none of the data:

    * **Rung labels thinned to 1 / 10 / 100 / 893.** The x-axis is categorical —
      eight chosen conditions at equal spacing (`rs.scale_axis`) — so a tick may
      be dropped without moving anything. Each remaining tick still sits on its
      own rung; the spacing between labels is not proportional and is not read
      that way, the same as in the full panel.
    * **Three y ticks** at 0 / 4,000 / 8,000. The reader needs the order of
      magnitude, not the value at every rung.
    * **The two callouts merged into one.** The endpoint ratio is the message, so
      it is the annotation that survives, placed in the gap it measures. The single
      agent's absolute counts ride under its own line instead of on a leader.
    """
    for arm in ("single", "multi"):
        rs.emphasis_series(ax, frame[frame["arm"] == arm], "references",
                           ARM_COLOR[arm], ARM_SHORT[arm])

    end = frame[frame["scale"] == 893].groupby("arm")["references"].mean()
    lo = frame[frame["arm"] == "single"].groupby("scale")["references"].mean()

    rs.scale_axis(ax, [1, 10, 100, 893])
    ax.set_ylim(0, end["multi"] * 1.12)
    # Thousands on the tick, not on the label: "8,000" spends a quarter of a
    # 1.4-inch plotting box on chrome. The unit moves into the axis title, which
    # is rotated and costs the same width whatever it says.
    ax.set_yticks([0, 4000, 8000])
    ax.set_yticklabels(["0", "4", "8"])
    ax.set_xlabel("targets per agent")
    ax.set_ylabel("references (×1,000)")

    rs.style_axes(ax)
    kit.breathe(ax, "y", "low", FLOOR_PAD)
    kit.breathe(ax, "x", "both", SIDE_PAD)
    ax.grid(axis="y", zorder=0)
    ax.set_axisbelow(True)
    kit.square(ax)

    ax.legend(loc="upper left", frameon=False, handlelength=1.2,
              labelspacing=0.2, borderpad=0, borderaxespad=0.2)
    # Both callouts go in the two pockets the curves leave: the flat stretch at
    # the left, and the wedge under the rise at the right. Placed by rung rather
    # than by fraction, so they track the data if the ladder ever changes.
    ax.text(rs.SCALE_POS[1] + 0.55, end["multi"] * 0.10,
            f"{lo.loc[1]:.0f}→{lo.loc[893]:.0f} refs", ha="left", va="bottom",
            fontsize=6.5, color=ARM_COLOR["single"])
    ax.text(rs.SCALE_POS[893] + 0.3, end["multi"] * 0.12,
            f"{end['multi'] / end['single']:.0f}×", ha="right", va="center",
            fontsize=9, fontweight="bold", color=COL["ink"])
    rs.panel_tag(ax, "a", "Final report references")


def main() -> None:
    kit.house_style()
    frame = pd.read_csv(CSV)
    fig, ax = plt.subplots(figsize=(3.0, 3.0))
    panel(ax, frame)
    kit.audit(fig, concepts=CONCEPTS)
    fig.tight_layout()

    fig_c, ax_c = plt.subplots(figsize=(2.0, 2.0))
    compact_panel(ax_c, frame)
    kit.audit(fig_c, concepts=CONCEPTS)
    fig_c.tight_layout()

    refs = frame.groupby(["arm", "scale"])["references"].mean()
    single = frame[frame["arm"] == "single"]["references"]
    print(f"single: {refs[('single', 1)]:.0f} refs at 1 target, "
          f"{refs[('single', 893)]:.0f} at 893 "
          f"(flat {single.min():.0f}-{single.max():.0f} across {len(single)} runs)")
    print(f"multi : {refs[('multi', 893)]:,.0f} at 893 "
          f"({refs[('multi', 893)] / 893:.1f} per target, "
          f"{refs[('multi', 893)] / refs[('single', 893)]:.0f}x)")
    for path in kit.save(fig, HERE / STEM) + kit.save(fig_c, HERE / f"{STEM}_compact"):
        print(f"  wrote {path.name}")


if __name__ == "__main__":
    main()
