#!/usr/bin/env python
"""Replots for the monolithic lit-agree-ns scaling experiment.

Regenerates the scaling / flag-distribution figures from the raw per-pair
JSONL, using encodings chosen for the claim each panel actually supports.

Reframe relative to the original figures: the original panels report
*supported fraction*, which falls 84.9% -> 3.5%. That fraction has a growing
denominator. In absolute terms the number of literature-grounded calls a single
run produces is flat (~76 rows, 4-16 targets) from 10 targets to 893.

Note on wording: nothing in the harness limits these runs. The batch config sets
max_internal_agent_steps=None, total_token_cap=None and
runner_wall_clock_timeout=None (agent_budget_summary.json), and cumulative token
use (1.6M-5.9M) exceeds the 272k context window, so continuations/compaction are
available too. The agent is therefore not hitting a cap -- it *self-terminates*
at a roughly constant effort level (median 810 s, 33k output tokens) whether it
was handed 1 target or 893. The scaling failure is self-limiting behaviour, not
an imposed budget, plus a collapse of within-target differentiation that a
share-based panel cannot show.

Outputs (beside this script):
  fig_r1_grounding_budget.{png,svg}       headline: fixed budget + composition
  fig_r2_flag_distribution_options.{png,svg}  four encodings of the same flags
  fig_r3_within_run_structure.{png,svg}   burstiness + differentiation collapse
  fig_r4_label_stability.{png,svg}        fixed-pair exemplar, square cells
  fig_r5_resource_envelope.{png,svg}      cost / runtime, emphasis form
  fig_r6_self_termination.{png,svg}       consumption vs workload; the evidence
  fig_r7_literature_quality.{png,svg}    do grounded rows stay informative?
  fig_r8_agree_quality.{png,svg}         what thins in Agree rows, and what does not
"""

from __future__ import annotations

import collections
import importlib.util
import json
import re
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

HERE = Path(__file__).resolve().parent
ANALYSIS = HERE.parent
EXPERIMENT = ANALYSIS.parent
REPO = EXPERIMENT.parents[2]
BATCH_ID = "monolithic-rosalind-5.5-top-hits-v1"
SUMMARY_CSV = EXPERIMENT / "batches" / BATCH_ID / "scaling_summary.csv"
STYLE = REPO / "src" / "figures" / "style.mplstyle"

# Canonical flag scheme, loaded by path so the script runs from any cwd.
_SPEC = importlib.util.spec_from_file_location(
    "flag_style", REPO / "src" / "figures" / "flag_style.py"
)
flag_style = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(flag_style)
FLAG_ORDER = list(flag_style.FLAG_ORDER)
FLAG_COLORS = flag_style.flag_colors()
FLAG_LABELS = flag_style.FLAG_LABELS
normalize_flag = flag_style.normalize_flag
legend_handles = flag_style.legend_handles

SEEDS = [17, 29, 43]
SCALES = [1, 3, 10, 30, 100, 205, 500, 893]
ANCHOR_PREFIX = 10
# "Grounded" here = the agent named a literature relationship at all. Disagree
# would qualify too but never occurs in this batch (0 / 17,376 rows).
SUPPORTED_FLAGS = {"agree", "inferred", "disagree"}
# From agent_budget_summary.json. The three limit knobs are all unset
# (max_internal_agent_steps / total_token_cap / runner_wall_clock_timeout), so
# these two are the only real quantities the run could have been pressing on.
CONTEXT_WINDOW_TOKENS = 272_000
AUTO_COMPACT_TOKENS = 258_400

# ---------------------------------------------------------------- palette ----
# Flag colors come from figures/flag_style.py (the repo-wide canonical scheme);
# see that module for the measured accessibility notes. Everything below is
# chrome and *derived* analytic series -- a grounded-row count or a token count
# is not a flag, so it takes an analytic color rather than borrowing a flag hue.
COL = {
    "surface": "#fcfcfb",
    "ink": "#0b0b0b",
    "ink2": "#52514e",
    "muted": "#898781",
    "grid": "#e1e0d9",
    "axis": "#c3c2b7",
    # derived analytic series (validated: "#256abf,#e34948" --pairs all passes;
    # "#86b6ef,#256abf" --ordinal passes)
    "grounded": flag_style.DERIVED_PRIMARY,
    "derived2": flag_style.DERIVED_SECONDARY,
    "reference": "#c3c2b7",  # context series (emitted rows / assigned targets)
    "replicate": "#b9b8b1",  # individual seeds, de-emphasised
    "absent": flag_style.NEUTRAL_ABSENT,
}
GAP = dict(edgecolor=COL["surface"], linewidth=0.7)  # 2px-equivalent surface gap


def load_style() -> None:
    if STYLE.exists():
        plt.style.use(STYLE)
    mpl.rcParams.update(
        {
            "figure.facecolor": COL["surface"],
            "axes.facecolor": COL["surface"],
            "savefig.facecolor": COL["surface"],
            "axes.edgecolor": COL["axis"],
            "axes.labelcolor": COL["ink"],
            "xtick.color": COL["muted"],
            "ytick.color": COL["muted"],
            "xtick.labelcolor": COL["ink2"],
            "ytick.labelcolor": COL["ink2"],
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
        }
    )


def style_axes(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_linewidth(0.5)
    ax.tick_params(length=2.5, width=0.5)


def panel_tag(ax: plt.Axes, tag: str, title: str) -> None:
    ax.set_title(
        f"{tag}   {title}", loc="left", fontsize=7.5, fontweight="bold",
        color=COL["ink"], pad=5,
    )


SCALE_POS = {s: i for i, s in enumerate(SCALES)}


def scale_axis(ax: plt.Axes, scales: list[int] | None = None) -> None:
    """Evenly spaced categorical x-axis over the 8 discrete scale conditions.

    A log axis crowds 500 against 893 and implies a continuum the design does
    not have; these are eight chosen conditions, so they get equal spacing.
    """
    scales = scales or SCALES
    ax.set_xticks([SCALE_POS[s] for s in scales])
    ax.set_xticklabels([str(s) for s in scales])
    ax.set_xlim(SCALE_POS[scales[0]] - 0.45, SCALE_POS[scales[-1]] + 0.45)


# ------------------------------------------------------------------ data -----
def load_rows() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Per-pair rows with assignment position, plus the run-level summary."""
    summary = pd.read_csv(SUMMARY_CSV)
    orders = {}
    for seed in SEEDS:
        meta = json.loads((EXPERIMENT / f"seed-{seed:03d}" / "target_order.json").read_text())
        orders[seed] = {g: i for i, g in enumerate(meta["gene_targets"])}

    records = []
    for run in summary.itertuples(index=False):
        seed, scale = int(run.seed), int(run.scale_targets)
        path = Path(run.run_dir) / "q3_cell_type_specificity.jsonl"
        recs = [json.loads(line) for line in path.open() if line.strip()]
        if len(recs) != int(run.emitted_pair_rows):
            raise ValueError(f"row mismatch seed={seed} scale={scale}")
        for emit_i, rec in enumerate(recs):
            records.append(
                dict(
                    seed=seed,
                    scale=scale,
                    emit_i=emit_i,
                    gene_target=rec["gene_target"],
                    cell_type=rec["cell_type"],
                    # The JSONL uses title case ("No Literature"); normalize to
                    # the canonical snake keys so one scheme covers the repo.
                    flag=normalize_flag(rec["flag"]),
                    assign_pos=orders[seed].get(rec["gene_target"], np.nan),
                )
            )
    rows = pd.DataFrame(records)
    rows["supported"] = rows["flag"].isin(SUPPORTED_FLAGS)
    rows["is_anchor"] = rows["assign_pos"] < ANCHOR_PREFIX
    return rows, summary


def load_events(summary: pd.DataFrame) -> pd.DataFrame:
    """Per-run internal step counts and token usage from each run's events.jsonl.

    `item.completed` events are the agent's own internal steps (tool calls,
    shell commands, messages); `turn.completed.usage` carries the cumulative
    token accounting across all internal continuations.
    """
    out = []
    for run in summary.itertuples(index=False):
        kinds: collections.Counter = collections.Counter()
        usage: dict = {}
        steps = 0
        for line in (Path(run.run_dir) / "events.jsonl").open():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = event.get("msg", event)
            if msg.get("type") == "item.completed":
                steps += 1
                kinds[(msg.get("item") or {}).get("type", "?")] += 1
            elif msg.get("type") == "turn.completed":
                usage = msg.get("usage") or {}
        out.append(
            dict(
                seed=int(run.seed),
                scale=int(run.scale_targets),
                steps=steps,
                tool_calls=kinds.get("mcp_tool_call", 0),
                commands=kinds.get("command_execution", 0),
                messages=kinds.get("agent_message", 0),
                input_tokens=usage.get("input_tokens", 0),
                cached_input_tokens=usage.get("cached_input_tokens", 0),
                output_tokens=usage.get("output_tokens", 0),
                reasoning_tokens=usage.get("reasoning_output_tokens", 0),
            )
        )
    frame = pd.DataFrame(out)
    frame["context_windows_consumed"] = frame["input_tokens"] / CONTEXT_WINDOW_TOKENS
    return frame.sort_values(["scale", "seed"]).reset_index(drop=True)


_DE_RECITAL = re.compile(r"q=|FDR|downstream|DEG|logFC|\bn=\d")
_HEDGE = re.compile(
    r"do(es)? not resolve|not resolve|cannot|can not|does not establish|no direct|"
    r"not directly|indirect inference|rather than a decisive|do(es)? not determine|"
    r"not dispositive|remains? unresolved|no target-specific|not itself",
    re.I,
)
_POSTHOC = re.compile(
    r"predicts? the observed|consistent with the observed|explains? the observed|"
    r"matches? the observed|accounts? for the observed|predicts? this|"
    r"consistent with this",
    re.I,
)


def _downstream_count(stats: object) -> float:
    """Pull the significant-downstream-gene count out of an evidence record.

    The key name drifts at every scale -- `sig_downstream`,
    `n_downstream_fdr_lt_0_10`, `n_sig_downstream_fdr_lt_0_10`,
    `n_sig_downstream`, `n_downstream_fdr10` all appear -- which is part of why
    the strict contract validator passes only 1 of 24 runs. Match on the stable
    part of the name instead of enumerating variants.
    """
    if isinstance(stats, str):
        found = re.search(r"(\d+)\s*(?:downstream|significant|FDR)", stats)
        return float(found.group(1)) if found else np.nan
    if not isinstance(stats, dict):
        return np.nan
    for key, value in stats.items():
        if "downstream" in key.lower() and isinstance(value, (int, float)):
            return float(value)
    return np.nan


def _split_summary(text: str) -> tuple[str, str]:
    """Separate the DE recital from the literature clause of a row summary.

    Every summary recites the differential-expression result and then states the
    literature bridge. Only the second part is a literature judgement, so the
    quality measures operate on it alone.
    """
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text or "") if s.strip()]
    recital = " ".join(s for s in sentences if _DE_RECITAL.search(s))
    clause = " ".join(s for s in sentences if not _DE_RECITAL.search(s))
    return recital, clause


def load_literature_quality(summary: pd.DataFrame) -> pd.DataFrame:
    """Per-row literature content: the clause, its references and its context tags."""
    out = []
    for run in summary.itertuples(index=False):
        run_dir = Path(run.run_dir)
        refs = {
            r["ref_id"]: r
            for r in map(json.loads, (run_dir / "q3_references.jsonl").open())
        }
        evidence = {}
        for e in map(json.loads, (run_dir / "q3_evidence.jsonl").open()):
            evidence[(e["gene_target"], e["cell_type"])] = _downstream_count(
                e.get("statistics")
            )
        for rec in map(json.loads, (run_dir / "q3_cell_type_specificity.jsonl").open()):
            _, clause = _split_summary(rec.get("summary", ""))
            ref_ids = rec.get("ref_ids") or []
            context = tuple(sorted(rec.get("lit_context") or []))
            out.append(
                dict(
                    seed=int(run.seed),
                    scale=int(run.scale_targets),
                    gene_target=rec["gene_target"],
                    cell_type=rec["cell_type"],
                    flag=normalize_flag(rec["flag"]),
                    lit_clause=clause,
                    n_refs=len(ref_ids),
                    ref_key=tuple(sorted(ref_ids)),
                    n_context=len(context),
                    context=context,
                    is_review=any(
                        refs.get(i, {}).get("source_type") == "review" for i in ref_ids
                    ),
                    hedged=bool(_HEDGE.search(clause)),
                    post_hoc=bool(_POSTHOC.search(clause)),
                    run_refs=len(refs),
                    n_deg=evidence.get((rec["gene_target"], rec["cell_type"]), np.nan),
                )
            )
    frame = pd.DataFrame(out)
    frame["grounded"] = frame["flag"].isin(SUPPORTED_FLAGS)
    return frame


_NON_NEURAL = re.compile(
    r"cardiomyocyte|cardiac|heart|fibroblast|hela|hek|kidney|liver|hepat|muscle|myotube|"
    r"cancer|tumou?r|carcinoma|melanoma|leukemi|lymphoma|yeast|drosophila|zebrafish|"
    r"erythro|platelet|macrophage|osteo|chondro|adipo|pancrea|intestin|colon|lung|"
    r"skin|keratino",
    re.I,
)
_SCOPED = re.compile(
    r"not itself the basis|not the basis of the flag|remains? a parallel|uncaptured|"
    r"does not explain|not explained|broader than|was not the|is not the basis|"
    r"separate module|parallel module",
    re.I,
)


def agree_quality(summary: pd.DataFrame) -> pd.DataFrame:
    """Per-run quality of the `Agree` rows specifically.

    Separates what degrades with scale (how deep the argument is) from what does
    not (whether the citation is real and on-target). The second group is kept in
    the output on purpose: several plausible "quality collapses" are not
    supported, and the controls are what show that.
    """
    out = []
    for run in summary.itertuples(index=False):
        run_dir = Path(run.run_dir)
        refs = {
            r["ref_id"]: r
            for r in map(json.loads, (run_dir / "q3_references.jsonl").open())
        }
        evidence = {
            e["evidence_id"]: e
            for e in map(json.loads, (run_dir / "q3_evidence.jsonl").open())
        }
        rows = []
        for rec in map(json.loads, (run_dir / "q3_cell_type_specificity.jsonl").open()):
            if normalize_flag(rec["flag"]) != "agree":
                continue
            cited = [refs[i] for i in (rec.get("ref_ids") or []) if i in refs]
            blob = " ".join(
                f"{r.get('ref_slug', '')} {r.get('citation', '')} {r.get('description', '')}"
                for r in cited
            ).lower()
            genes = [
                g
                for i in (rec.get("evidence_ids") or [])
                for g in (evidence.get(i, {}).get("genes") or [])
            ]
            rows.append(
                dict(
                    n_refs=len(cited),
                    multi_ref=len(cited) >= 2,
                    review=any(r.get("source_type") == "review" for r in cited),
                    target_named=rec["gene_target"].lower() in blob,
                    all_pmid=bool(cited) and all(r.get("pmid") for r in cited),
                    non_neural=bool(_NON_NEURAL.search(blob)),
                    scoped=bool(_SCOPED.search(rec.get("summary", ""))),
                    n_evidence_genes=len(genes),
                )
            )
        if not rows:
            continue
        frame = pd.DataFrame(rows)
        out.append(
            dict(
                scale=int(run.scale_targets),
                seed=int(run.seed),
                agree_rows=len(frame),
                refs_per_row=frame["n_refs"].mean(),
                multi_ref_chain=frame["multi_ref"].mean() * 100,
                scopes_exclusions=frame["scoped"].mean() * 100,
                review_backed=frame["review"].mean() * 100,
                target_named_in_ref=frame["target_named"].mean() * 100,
                all_refs_have_pmid=frame["all_pmid"].mean() * 100,
                non_neural_source=frame["non_neural"].mean() * 100,
                evidence_genes=frame["n_evidence_genes"].mean(),
            )
        )
    return pd.DataFrame(out).sort_values(["scale", "seed"]).reset_index(drop=True)


def literature_broadcast_by_run(quality: pd.DataFrame) -> pd.DataFrame:
    """Per run: share of grounded rows whose claim is not their own.

    A grounded row is *broadcast* if its literature clause is reused verbatim for
    at least one other cell type of the same target -- i.e. the row is a copy of
    a target-level statement rather than a judgement about that cell type.
    """
    grounded = quality[quality["grounded"]]
    out = []
    for (scale, seed), sub in grounded.groupby(["scale", "seed"]):
        shared = sub.groupby(["gene_target", "lit_clause"])["cell_type"].transform(
            "nunique"
        )
        out.append(
            dict(
                scale=scale,
                seed=seed,
                frac_broadcast=float((shared > 1).mean()) * 100,
                refs_per_row=float(sub["n_refs"].mean()),
            )
        )
    return pd.DataFrame(out).sort_values(["scale", "seed"]).reset_index(drop=True)


def literature_quality_summary(quality: pd.DataFrame) -> pd.DataFrame:
    """Per-scale collapse of literature specificity onto the cell-type axis."""
    grounded = quality[quality["grounded"]]
    out = []
    for scale, sub in grounded.groupby("scale"):
        per_target = sub.groupby(["seed", "gene_target"]).agg(
            n_cell_types=("cell_type", "nunique"),
            n_clauses=("lit_clause", "nunique"),
            n_refkeys=("ref_key", "nunique"),
        )
        multi = per_target[per_target["n_cell_types"] > 1]
        per_run = sub.groupby("seed").agg(
            rows=("lit_clause", "size"), distinct=("lit_clause", "nunique")
        )
        # How wide a range of actual responses does one clause get applied to?
        spans = sub.dropna(subset=["n_deg"]).groupby(
            ["seed", "gene_target", "lit_clause"]
        ).agg(n_ct=("cell_type", "nunique"), lo=("n_deg", "min"), hi=("n_deg", "max"))
        spans = spans[spans["n_ct"] > 1]
        fold = (spans["hi"] / spans["lo"].clip(lower=1)).median() if len(spans) else np.nan
        out.append(
            dict(
                scale=scale,
                grounded_rows=len(sub),
                cell_types_per_target=multi["n_cell_types"].mean(),
                clauses_per_target=multi["n_clauses"].mean(),
                frac_one_clause=(multi["n_clauses"] == 1).mean(),
                frac_one_ref=(multi["n_refkeys"] == 1).mean(),
                distinct_clauses_per_run=per_run["distinct"].mean(),
                rows_per_clause=(per_run["rows"] / per_run["distinct"]).mean(),
                refs_per_row=sub["n_refs"].mean(),
                context_dims=sub["n_context"].mean(),
                declares_cell_type=sub["context"].apply(lambda c: "cell_type" in c).mean(),
                declares_stage=sub["context"].apply(lambda c: "stage" in c).mean(),
                review_frac=sub["is_review"].mean(),
                agree_share=(sub["flag"] == "agree").mean(),
                hedged_inferred=sub.loc[sub["flag"] == "inferred", "hedged"].mean(),
                post_hoc=sub["post_hoc"].mean(),
                median_deg_fold_per_clause=fold,
            )
        )
    return pd.DataFrame(out).sort_values("scale").reset_index(drop=True)


def run_level(rows: pd.DataFrame) -> pd.DataFrame:
    """One row per run: emitted rows, grounded rows, assigned/grounded targets."""
    out = []
    for (scale, seed), grp in rows.groupby(["scale", "seed"]):
        by_target = grp.groupby("gene_target")["supported"].any()
        out.append(
            dict(
                scale=scale,
                seed=seed,
                rows=len(grp),
                grounded=int(grp["supported"].sum()),
                **{f: int((grp["flag"] == f).sum()) for f in FLAG_ORDER},
                targets=len(by_target),
                grounded_targets=int(by_target.sum()),
            )
        )
    frame = pd.DataFrame(out)
    frame["supported_fraction"] = frame["grounded"] / frame["rows"]
    return frame.sort_values(["scale", "seed"]).reset_index(drop=True)


def anchor_differentiation(rows: pd.DataFrame) -> pd.DataFrame:
    """Within-target label differentiation on the fixed anchor-10 cohort.

    These are the *same* targets with the *same* eligible cell-type rows at
    every scale, so a change here cannot come from the target mix.
    """
    anch = rows[rows["is_anchor"]]
    per_target = anch.groupby(["scale", "seed", "gene_target"]).agg(
        n=("flag", "size"), nuniq=("flag", "nunique"), supp=("supported", "mean")
    )
    out = []
    for scale, grp in per_target.groupby("scale"):
        out.append(
            dict(
                scale=scale,
                n_targets=len(grp),
                rows=int(grp["n"].sum()),
                mean_rows_per_target=grp["n"].mean(),
                single_label=float((grp["nuniq"] == 1).mean()),
                blanket_no_lit=float(((grp["nuniq"] == 1) & (grp["supp"] == 0)).mean()),
                grounded_rows=int((grp["n"] * grp["supp"]).sum()),
            )
        )
    return pd.DataFrame(out).sort_values("scale").reset_index(drop=True)


def anchor_dissent_by_run(rows: pd.DataFrame) -> pd.DataFrame:
    """Per run: how many cell types of an anchor target get a distinguishing call.

    Counting *cell types that differ from their target's majority call* rather
    than distinct flags per target: with only three flags ever used (Disagree
    never fires) a distinct-flag count is pinned in a 1-3 band and barely moves,
    whereas this is an absolute count out of a constant ~14.1 cell types per
    anchor target, so it has real dynamic range and a concrete reading.
    """
    anchor = rows[rows["is_anchor"]]
    out = []
    for (scale, seed), sub in anchor.groupby(["scale", "seed"]):
        per_target = sub.groupby("gene_target")["flag"].agg(
            n="size", modal=lambda s: s.value_counts().iloc[0]
        )
        per_target = per_target[per_target["n"] > 1]
        if not len(per_target):
            continue
        out.append(
            dict(
                scale=scale,
                seed=seed,
                cell_types_per_target=per_target["n"].mean(),
                dissenting=(per_target["n"] - per_target["modal"]).mean(),
            )
        )
    return pd.DataFrame(out).sort_values(["scale", "seed"]).reset_index(drop=True)


def differentiation_measures(rows: pd.DataFrame) -> pd.DataFrame:
    """Candidate ways to measure within-target differentiation, side by side.

    This is the evidence for what `fig_r1c` plots. `rows_per_target` is carried
    because it is the confound: a target with more eligible cell types can
    mechanically carry more distinct flags, and the anchor prefix is only fully
    assigned from 10 targets on (at 1 and 3 targets the cohort is 3 and 9
    targets at 19.0 and 15.4 rows each, not 30 targets at 14.1). Only scales
    >= 10 are a controlled comparison.
    """
    anchor = rows[rows["is_anchor"]]
    out = []
    for scale, sub in anchor.groupby("scale"):
        per = sub.groupby(["seed", "gene_target"])["flag"].agg(
            n="size",
            n_flags="nunique",
            modal=lambda s: s.value_counts().iloc[0],
        )
        per = per[per["n"] > 1]
        if not len(per):
            continue
        shares = sub.groupby(["seed", "gene_target"])["flag"].apply(
            lambda s: s.value_counts(normalize=True).to_numpy()
        )
        # Normalised by log(3): three flags are ever used, Disagree never fires.
        entropy = shares.apply(
            lambda p: 0.0 if len(p) < 2 else float(-(p * np.log(p)).sum() / np.log(3))
        )
        dissent = per["n"] - per["modal"]
        out.append(
            dict(
                scale=scale,
                target_instances=len(per),
                rows_per_target=per["n"].mean(),
                distinct_flags=per["n_flags"].mean(),
                frac_all_one_flag=(per["n_flags"] == 1).mean(),
                entropy_norm=entropy.reindex(per.index).mean(),
                minority_pct=(dissent / per["n"]).mean() * 100,
                cell_types_called_differently=dissent.mean(),
            )
        )
    return pd.DataFrame(out).sort_values("scale").reset_index(drop=True)


def burst_stats(rows: pd.DataFrame, n_perm: int = 400, seed: int = 0) -> pd.DataFrame:
    """Contiguous grounded blocks vs a permutation null, along emission order."""
    rng = np.random.default_rng(seed)
    out = []
    for (scale, sd), grp in rows.groupby(["scale", "seed"]):
        x = grp.sort_values("emit_i")["supported"].to_numpy(dtype=int)
        if x.sum() == 0:
            continue
        blocks = int((np.diff(np.r_[0, x]) == 1).sum())
        null = np.array(
            [int((np.diff(np.r_[0, rng.permutation(x)]) == 1).sum()) for _ in range(n_perm)]
        )
        out.append(
            dict(
                scale=scale,
                seed=sd,
                grounded=int(x.sum()),
                blocks=blocks,
                null_mean=null.mean(),
                z=(blocks - null.mean()) / null.std() if null.std() else np.nan,
            )
        )
    return pd.DataFrame(out)


def label_instability(rows: pd.DataFrame) -> dict:
    """How often a fixed anchor pair changes label across scales 10..893."""
    anch = rows[rows["is_anchor"] & (rows["scale"] >= 10)]
    piv = anch.pivot_table(
        index=["seed", "gene_target", "cell_type"],
        columns="scale",
        values="flag",
        aggfunc="first",
    )
    nuniq = piv.apply(lambda r: r.dropna().nunique(), axis=1)
    return {
        "n_pairs": int(len(nuniq)),
        "changed_fraction": float((nuniq > 1).mean()),
        "distribution": nuniq.value_counts().sort_index().to_dict(),
    }


# ---------------------------------------------------------------- helpers ----
def emphasis_series(
    ax: plt.Axes,
    frame: pd.DataFrame,
    value: str,
    color: str,
    label: str,
    marker: str = "o",
) -> None:
    """Replicates as de-emphasised marks; the seed mean as the accent line.

    Seeds are replicates, not identities, so they get one recessive treatment
    instead of three categorical hues.
    """
    for seed in SEEDS:
        sub = frame[frame["seed"] == seed].sort_values("scale")
        ax.plot(
            [SCALE_POS[s] for s in sub["scale"]], sub[value], marker=marker,
            ms=2.6, lw=0, color=COL["replicate"], mec="none", zorder=2,
        )
    mean = frame.groupby("scale")[value].mean().reset_index()
    ax.plot(
        [SCALE_POS[s] for s in mean["scale"]], mean[value], marker=marker,
        ms=3.6, lw=1.4, color=color, mec=COL["surface"], mew=0.6,
        label=label, zorder=3,
    )


def save(fig: plt.Figure, stem: str) -> None:
    fig.savefig(HERE / f"{stem}.png", dpi=300, bbox_inches="tight")
    fig.savefig(HERE / f"{stem}.svg", bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {stem}.png / .svg")


# ------------------------------------------------------------------ fig r1 ---
def fig_r1(runs: pd.DataFrame, anchors: pd.DataFrame,
           dissent: pd.DataFrame) -> None:
    """Headline: grounded output is constant in absolute terms; shares hide it."""
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.55))
    ax_a, ax_b, ax_c = axes

    # -- a: absolute rows vs grounded rows (same unit -> one axis) ------------
    emphasis_series(ax_a, runs, "rows", COL["reference"], "pair rows emitted")
    emphasis_series(ax_a, runs, "grounded", COL["grounded"], "rows with literature")
    ax_a.set_yscale("log")
    scale_axis(ax_a)
    ax_a.set_ylim(8, 30000)  # headroom so the legend and note clear both series
    ax_a.set_xlabel("targets assigned to one agent")
    ax_a.set_ylabel("pair rows per run")
    style_axes(ax_a)
    ax_a.grid(axis="y", color=COL["grid"], lw=0.4, zorder=0)
    ax_a.set_axisbelow(True)
    # The ratio lives in the footnote, not the plot: the free band between the
    # two series is too narrow for a legible two-line note at any anchor.
    m = runs.groupby("scale")[["rows", "grounded"]].mean()
    ax_a.legend(
        loc="upper left", frameon=False,
        fontsize=6.2, handlelength=1.4, labelspacing=0.25, borderpad=0,
    )
    panel_tag(ax_a, "a", "Grounded output does not grow")

    # -- b: composition, 100% stacked (what the original figure showed) ------
    comp = runs.groupby("scale")[FLAG_ORDER].sum()
    frac = comp.div(comp.sum(axis=1), axis=0) * 100
    y = np.arange(len(SCALES))
    left = np.zeros(len(SCALES))
    for flag in FLAG_ORDER:
        vals = frac.loc[SCALES, flag].to_numpy()
        ax_b.barh(y, vals, left=left, height=0.68, color=FLAG_COLORS[flag],
                  **GAP, zorder=3)
        left += vals
    for i, scale in enumerate(SCALES):
        ax_b.text(
            102, y[i], f"{frac.loc[scale, 'no_literature']:.0f}%",
            ha="left", va="center", fontsize=5.8, color=COL["ink2"],
        )
    ax_b.text(
        102, -0.95, "no lit.", ha="left", va="center", fontsize=5.8,
        color=COL["muted"], style="italic",
    )
    ax_b.set_yticks(y)
    ax_b.set_yticklabels([str(s) for s in SCALES])
    ax_b.invert_yaxis()
    ax_b.set_xlim(0, 118)
    ax_b.set_xticks([0, 25, 50, 75, 100])
    ax_b.set_xlabel("share of emitted pair rows (%)")
    style_axes(ax_b)
    ax_b.spines["left"].set_visible(False)
    ax_b.spines["bottom"].set_bounds(0, 100)
    ax_b.tick_params(axis="y", length=0)
    panel_tag(ax_b, "b", "Rows shift to abstention")

    # -- c: within-target differentiation on the fixed anchor cohort ---------
    sub = dissent[dissent["scale"] >= 10]
    n_ct = sub["cell_types_per_target"].mean()
    emphasis_series(ax_c, sub, "dissenting", COL["grounded"], "seed mean")
    scale_axis(ax_c, [s for s in SCALES if s >= 10])
    ax_c.set_ylim(-0.08, 2.3)
    ax_c.set_yticks([0, 0.5, 1.0, 1.5, 2.0])
    ax_c.set_xlabel("targets assigned to one agent")
    ax_c.set_ylabel("cell types called differently")
    style_axes(ax_c)
    ax_c.grid(axis="y", color=COL["grid"], lw=0.4, zorder=0)
    ax_c.set_axisbelow(True)
    n_zero = int((sub[sub["scale"] == 893]["dissenting"] == 0).sum())
    ax_c.annotate(
        f"at 893 targets, {n_zero} of 3 runs\ngive every cell type of an\n"
        "anchor target the same call",
        xy=(0.97, 0.97), xycoords="axes fraction", fontsize=6.0,
        color=COL["ink2"], ha="right", va="top",
    )
    panel_tag(ax_c, "c", "Differentiation collapses")

    fig.suptitle(
        "A single agent stops at a fixed effort level, whatever the workload",
        x=0.005, ha="left", fontsize=9, fontweight="bold", color=COL["ink"],
    )
    handles = legend_handles(labels={"disagree": "Disagree (0 rows, any scale)"})
    fig.legend(
        handles=handles, loc="lower left", bbox_to_anchor=(0.005, 0.165),
        frameon=False, fontsize=6.2, ncol=4, handlelength=1.1,
        handleheight=0.85, columnspacing=1.4, title="panel b flags",
        title_fontproperties={"size": 6.2, "weight": "bold"},
        alignment="left",
    )
    fig.text(
        0.005, 0.01,
        f"Panel a, 10 → 893 targets: {m.loc[893, 'rows'] / m.loc[10, 'rows']:.1f}× the pair "
        f"rows, {m.loc[893, 'grounded'] / m.loc[10, 'grounded']:.2f}× the grounded rows. "
        "No step, token or wall-clock limit was configured; the agent\nself-terminates. "
        f"Panel c counts, per anchor-10 target, the cell types whose flag differs from that "
        f"target's majority flag, out of {n_ct:.1f} cell types per target -- the same 10\n"
        "targets with the same 422 eligible rows at every scale, so the fall cannot come from "
        "the target mix. A distinct-flag count is not used: only three flags ever\nfire, so it "
        "stays pinned in a 1-3 band and moves only 1.8 to 1.1. "
        "Seeds shown as light marks; line is the seed mean.",
        fontsize=5.8, color=COL["muted"], ha="left", va="bottom",
    )
    fig.tight_layout(rect=(0, 0.27, 1, 0.935), w_pad=2.4)
    save(fig, "fig_r1_grounding_budget")


# ------------------------------------------------------------------ fig r2 ---
def fig_r2(rows: pd.DataFrame, runs: pd.DataFrame) -> None:
    """Four encodings of the same flag data, with what each one buys."""
    fig = plt.figure(figsize=(7.2, 6.9))
    gs = fig.add_gridspec(
        2, 2, hspace=0.52, wspace=0.30, left=0.085, right=0.985,
        top=0.875, bottom=0.085,
    )
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 0])
    ax4 = fig.add_subplot(gs[1, 1])
    CAP_Y = -0.255  # caption band below each axes, in axes coords

    comp = runs.groupby("scale")[FLAG_ORDER].sum()

    # -- option 1: 100% stacked columns -------------------------------------
    frac = comp.div(comp.sum(axis=1), axis=0) * 100
    x = np.arange(len(SCALES))
    bottom = np.zeros(len(SCALES))
    for flag in FLAG_ORDER:
        vals = frac.loc[SCALES, flag].to_numpy()
        ax1.bar(x, vals, bottom=bottom, width=0.68, color=FLAG_COLORS[flag],
                **GAP, zorder=3)
        bottom += vals
    ax1.set_xticks(x)
    ax1.set_xticklabels([str(s) for s in SCALES])
    ax1.set_ylim(0, 100)
    ax1.set_ylabel("share of emitted rows (%)")
    ax1.set_xlabel("targets assigned to one agent")
    style_axes(ax1)
    panel_tag(ax1, "1", "Share (as published)")
    ax1.text(
        0.0, CAP_Y, "Reads the shift to abstention. Hides that the grounded\n"
        "count never grew — the denominator did.",
        transform=ax1.transAxes, fontsize=6.0, color=COL["ink2"], va="top",
    )

    # -- option 2: absolute counts, same unit, one log axis ------------------
    emphasis_series(ax2, runs, "rows", COL["reference"], "all pair rows")
    emphasis_series(ax2, runs, "grounded", COL["grounded"], "grounded rows")
    ax2.set_yscale("log")
    scale_axis(ax2)
    ax2.set_ylim(8, 12000)
    ax2.set_ylabel("pair rows per run")
    ax2.set_xlabel("targets assigned to one agent")
    style_axes(ax2)
    ax2.grid(axis="y", color=COL["grid"], lw=0.4, zorder=0)
    ax2.set_axisbelow(True)
    ax2.legend(loc="upper left", frameon=False, fontsize=6.0,
               handlelength=1.4, labelspacing=0.25, borderpad=0)
    panel_tag(ax2, "2", "Absolute count (recommended)")
    ax2.text(
        0.0, CAP_Y, "Shows the self-limiting directly: a flat grounded series\n"
        "under a rising total. Both series share one unit and one axis.",
        transform=ax2.transAxes, fontsize=6.0, color=COL["ink2"], va="top",
    )

    # -- option 3: where the grounding happens along the run ----------------
    lanes = [(scale, seed) for scale in (100, 205, 500, 893) for seed in SEEDS]
    for i, (scale, seed) in enumerate(lanes):
        grp = rows[(rows["scale"] == scale) & (rows["seed"] == seed)].sort_values("emit_i")
        n = len(grp)
        pos = grp["emit_i"].to_numpy() / n
        ax3.add_patch(
            plt.Rectangle((0, i - 0.38), 1, 0.76, facecolor=FLAG_COLORS["no_literature"],
                          edgecolor="none", zorder=2)
        )
        hits = pos[grp["supported"].to_numpy()]
        ax3.vlines(hits, i - 0.38, i + 0.38, color=COL["grounded"], lw=0.45, zorder=3)
    ax3.set_ylim(len(lanes) - 0.5, -0.5)
    ax3.set_xlim(0, 1)
    ax3.set_yticks(range(len(lanes)))
    ax3.set_yticklabels([f"{scale} · s{seed}" for scale, seed in lanes], fontsize=5.2)
    ax3.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax3.set_xticklabels(["start", "25%", "50%", "75%", "end"])
    ax3.set_xlabel("position through the emitted table")
    style_axes(ax3)
    ax3.spines["left"].set_visible(False)
    ax3.tick_params(axis="y", length=0)
    panel_tag(ax3, "3", "Position within the run")
    ax3.text(
        0.0, CAP_Y, "Grounded rows fall in a few contiguous bursts separated\n"
        "by long dead stretches — not thinly spread. Shows structure\n"
        "a per-scale summary averages away.",
        transform=ax3.transAxes, fontsize=6.0, color=COL["ink2"], va="top",
    )

    # -- option 4: one run, every row ---------------------------------------
    grp = rows[(rows["scale"] == 893) & (rows["seed"] == 29)].sort_values("emit_i")
    cmap, code, order = flag_style.flag_cmap()
    codes = grp["flag"].map(code).to_numpy(dtype=float)
    ncol = 62
    nrow = int(np.ceil(len(codes) / ncol))
    grid = np.full(nrow * ncol, np.nan)
    grid[: len(codes)] = codes
    cmap.set_bad(COL["surface"])
    ax4.imshow(
        grid.reshape(nrow, ncol), cmap=cmap, vmin=-0.5, vmax=len(order) - 0.5,
        interpolation="nearest", aspect="auto",
    )
    ax4.set_xticks([])
    ax4.set_yticks([])
    for side in ("top", "right", "left", "bottom"):
        ax4.spines[side].set_visible(False)
    n_g = int(grp["supported"].sum())
    ax4.set_xlabel(
        f"one run: 893 targets, {len(codes):,} rows, {n_g} grounded", fontsize=6.4
    )
    panel_tag(ax4, "4", "Every row of one run")
    ax4.text(
        0.0, CAP_Y, "One cell per emitted row, reading order. Makes the\n"
        "sparsity and the clumping legible at once; no axis to read,\n"
        "so it is a companion to 2, not a replacement.",
        transform=ax4.transAxes, fontsize=6.0, color=COL["ink2"], va="top",
    )

    handles = legend_handles(labels={"disagree": "Disagree (never observed)"})
    fig.legend(
        handles=handles, loc="upper left", bbox_to_anchor=(0.083, 0.945),
        frameon=False, fontsize=6.4, ncol=4, handlelength=1.1, handleheight=0.85,
        columnspacing=1.4,
    )
    fig.suptitle(
        "Four ways to show the same flag distribution",
        x=0.005, y=0.987, ha="left", fontsize=9, fontweight="bold", color=COL["ink"],
    )
    save(fig, "fig_r2_flag_distribution_options")


# ------------------------------------------------------------------ fig r3 ---
def fig_r3(rows: pd.DataFrame, bursts: pd.DataFrame, anchors: pd.DataFrame) -> None:
    """The two within-run failure modes a per-scale summary cannot show."""
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(7.2, 3.1))

    # -- a: observed contiguous blocks vs permutation null ------------------
    # Restricted to scales >= 100: below that a run has too few grounded rows
    # for the block statistic to be powered (|z| < 12 and sign-unstable).
    order = (
        bursts[bursts["scale"] >= 100]
        .sort_values(["scale", "seed"])
        .reset_index(drop=True)
    )
    y = np.arange(len(order))
    ax_a.hlines(
        y, order["blocks"], order["null_mean"], color=COL["grid"], lw=1.2, zorder=2
    )
    ax_a.plot(
        order["null_mean"], y, "o", ms=3.4, color=COL["reference"],
        mec=COL["surface"], mew=0.6, label="expected if spread at random", zorder=3,
    )
    ax_a.plot(
        order["blocks"], y, "o", ms=3.4, color=COL["grounded"],
        mec=COL["surface"], mew=0.6, label="observed contiguous bursts", zorder=4,
    )
    ax_a.set_yticks(y)
    ax_a.set_yticklabels(
        [f"{r.scale} · s{r.seed}" for r in order.itertuples()], fontsize=6.0
    )
    ax_a.invert_yaxis()
    ax_a.set_xlim(0, order["null_mean"].max() * 1.32)
    ax_a.set_xlabel("contiguous blocks of grounded rows")
    style_axes(ax_a)
    ax_a.spines["left"].set_visible(False)
    ax_a.tick_params(axis="y", length=0)
    ax_a.legend(loc="lower right", bbox_to_anchor=(1.0, -0.02), frameon=False,
                fontsize=6.0, handlelength=1.0, labelspacing=0.3, borderpad=0)
    ax_a.annotate(
        f"every run: fewer bursts than chance\n"
        f"(z = {order['z'].min():.0f} to {order['z'].max():.0f})",
        xy=(0.97, 0.20), xycoords="axes fraction", ha="right", va="bottom",
        fontsize=6.0, color=COL["ink2"],
    )
    panel_tag(ax_a, "a", "Grounding arrives in bursts")

    # -- b: grounded rows on the fixed anchor cohort ------------------------
    # Only scales >= 10 have the complete cohort (10 anchors x 3 seeds = 422
    # eligible rows); at 1 and 3 targets the prefix is not yet fully assigned.
    anch = anchors[anchors["scale"] >= 10].reset_index(drop=True)
    eligible = int(anch["rows"].iloc[0])
    assert (anch["rows"] == eligible).all(), "anchor cohort denominator drifted"
    xb = np.arange(len(anch))
    ax_b.bar(xb, anch["grounded_rows"], width=0.62, color=COL["grounded"], **GAP, zorder=3)
    ax_b.axhline(eligible, color=COL["muted"], lw=0.7, zorder=2)
    ax_b.text(
        0.02, eligible - 12, f"{eligible} eligible rows (constant at every scale)",
        transform=ax_b.get_yaxis_transform(), fontsize=6.0,
        color=COL["ink2"], va="top", ha="left",
    )
    for i, r in enumerate(anch.itertuples()):
        ax_b.text(
            i, r.grounded_rows + 9, str(r.grounded_rows), ha="center",
            fontsize=5.8, color=COL["ink2"],
        )
    ax_b.set_xticks(xb)
    ax_b.set_xticklabels([str(s) for s in anch["scale"]])
    ax_b.set_ylim(0, eligible * 1.1)
    ax_b.set_xlabel("targets assigned to one agent")
    ax_b.set_ylabel("grounded rows, anchor-10 cohort")
    style_axes(ax_b)
    ax_b.grid(axis="y", color=COL["grid"], lw=0.4, zorder=0)
    ax_b.set_axisbelow(True)
    panel_tag(ax_b, "b", "The same 10 targets lose grounding")

    fig.suptitle(
        "Within-run structure: bursty attention, and grounding withdrawn from fixed work",
        x=0.005, ha="left", fontsize=9, fontweight="bold", color=COL["ink"],
    )
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    save(fig, "fig_r3_within_run_structure")


# ------------------------------------------------------------------ fig r4 ---
def fig_r4(rows: pd.DataFrame, instability: dict) -> None:
    """Fixed-pair exemplar with equal-size cells in both panels."""
    exemplar_seed = 29
    genes = ["Srsf1", "Tnpo3"]
    sub = rows[(rows["seed"] == exemplar_seed) & (rows["gene_target"].isin(genes))]
    cmap, _code, order = flag_style.flag_cmap()
    mats, labels = {}, {}
    for gene in genes:
        g = sub[sub["gene_target"] == gene]
        piv = g.pivot_table(
            index="cell_type", columns="scale", values="flag", aggfunc="first"
        ).reindex(columns=SCALES)
        labels[gene] = list(piv.index)
        mats[gene] = piv.map(lambda v: _code.get(v, np.nan)).to_numpy(dtype=float)

    heights = [len(labels[g]) for g in genes]
    fig, axes = plt.subplots(
        2, 1, figsize=(4.6, 4.9), gridspec_kw={"height_ratios": heights, "hspace": 0.16}
    )
    for ax, gene, tag in zip(axes, genes, ["a", "b"]):
        ax.imshow(
            mats[gene], cmap=cmap, vmin=-0.5, vmax=len(order) - 0.5,
            interpolation="nearest", aspect="auto",
        )
        ax.set_xticks(range(len(SCALES)))
        ax.set_xticklabels([str(s) for s in SCALES], fontsize=6.2)
        ax.set_yticks(range(len(labels[gene])))
        ax.set_yticklabels(labels[gene], fontsize=5.4)
        ax.set_xticks(np.arange(-0.5, len(SCALES), 1), minor=True)
        ax.set_yticks(np.arange(-0.5, len(labels[gene]), 1), minor=True)
        ax.grid(which="minor", color=COL["surface"], lw=0.7, ls="-")
        ax.tick_params(which="minor", length=0)
        ax.tick_params(length=0)
        for side in ("top", "right", "left", "bottom"):
            ax.spines[side].set_visible(False)
        panel_tag(ax, tag, f"{gene} pair labels")
    axes[-1].set_xlabel("targets assigned to the same agent")

    handles = legend_handles()
    handles.append(Patch(facecolor=COL["absent"], label="target not yet assigned"))
    fig.legend(
        handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.045),
        frameon=False, fontsize=6.2, ncol=3, handlelength=1.1, handleheight=0.85,
        columnspacing=1.2,
    )
    fig.suptitle(
        "Identical comparisons receive different literature labels at different scales",
        x=0.005, ha="left", fontsize=8.5, fontweight="bold", color=COL["ink"],
    )
    fig.text(
        0.005, 0.945,
        f"Seed {exemplar_seed}. Across the fixed anchor cohort, "
        f"{instability['changed_fraction'] * 100:.0f}% of "
        f"{instability['n_pairs']} pairs change label between scales.",
        fontsize=6.4, color=COL["ink2"], ha="left", va="top",
    )
    fig.tight_layout(rect=(0, 0.01, 1, 0.925))
    save(fig, "fig_r4_label_stability")


# ------------------------------------------------------------------ fig r5 ---
def fig_r5(summary: pd.DataFrame, runs: pd.DataFrame) -> None:
    """Resource envelope: absolute effort is flat, per-pair effort collapses."""
    met = summary.copy()
    met["scale"] = met["scale_targets"].astype(int)
    met["minutes"] = met["duration_s"] / 60.0
    met = met.merge(runs[["scale", "seed", "rows", "grounded"]], on=["scale", "seed"])
    met["cost_per_grounded"] = met["cost_usd"] / met["grounded"].clip(lower=1)
    met["out_per_pair"] = met["output_tokens"] / met["rows"]

    # One measure per panel: USD, minutes and tokens-per-row are three units,
    # so they get three axes side by side rather than one shared scale.
    fig, (ax_a, ax_b, ax_c) = plt.subplots(1, 3, figsize=(7.2, 2.5))

    for ax, col, ylabel, tag, title, ylim in [
        (ax_a, "cost_usd", "estimated list cost per run (USD)", "a",
         "Cost per run barely moves", (0, 5.6)),
        (ax_b, "minutes", "agent runtime per run (min)", "b",
         "Runtime per run barely moves", (0, 23)),
    ]:
        emphasis_series(ax, met, col, COL["grounded"], "seed mean")
        scale_axis(ax)
        ax.set_ylim(*ylim)
        ax.set_xlabel("targets assigned to one agent")
        ax.set_ylabel(ylabel)
        style_axes(ax)
        ax.grid(axis="y", color=COL["grid"], lw=0.4, zorder=0)
        ax.set_axisbelow(True)
        panel_tag(ax, tag, title)

    # -- c: what a marginal pair receives ---------------------------------
    emphasis_series(ax_c, met, "out_per_pair", COL["grounded"], "seed mean")
    ax_c.set_yscale("log")
    scale_axis(ax_c)
    ax_c.set_xlabel("targets assigned to one agent")
    ax_c.set_ylabel("output tokens per pair row")
    style_axes(ax_c)
    ax_c.grid(axis="y", color=COL["grid"], lw=0.4, zorder=0)
    ax_c.set_axisbelow(True)
    m = met.groupby("scale")["out_per_pair"].mean()
    ax_c.annotate(
        f"{m.loc[1] / m.loc[893]:.0f}× less output per\ncomparison, 1 → 893 targets",
        xy=(0.97, 0.95), xycoords="axes fraction", ha="right", va="top",
        fontsize=6.2, color=COL["ink2"],
    )
    panel_tag(ax_c, "c", "Per-comparison allocation collapses")

    fig.suptitle(
        "Cost, runtime and per-comparison output allocation",
        x=0.005, ha="left", fontsize=9, fontweight="bold", color=COL["ink"],
    )
    fig.text(
        0.005, 0.012,
        "Absolute cost and runtime barely move while the table grows, so the per-comparison "
        "allocation in c contracts. See fig_r6 for why this is the agent stopping\nearly rather "
        "than a limit being reached. Seeds shown as light marks; line is the seed mean. "
        "Cost is runner-estimated list price, not verified billing.",
        fontsize=5.8, color=COL["muted"], ha="left", va="bottom",
    )
    fig.tight_layout(rect=(0, 0.075, 1, 0.93), w_pad=2.2)
    save(fig, "fig_r5_resource_envelope")


# ------------------------------------------------------------------ fig r6 ---
def fig_r6(events: pd.DataFrame, runs: pd.DataFrame, summary: pd.DataFrame) -> None:
    """The self-termination evidence, carried by the marks rather than a claim.

    a: everything indexed to the 1-target run, so workload and consumption share
       one unitless axis (the sanctioned way to compare different units).
    b: tokens against the context window, the only quantity the run could have
       been pressing on -- cumulative input sits far above it, output far below.
    c: internal steps and tool calls, neither of which has a configured limit.
    """
    met = summary.copy()
    met["scale"] = met["scale_targets"].astype(int)
    met["minutes"] = met["duration_s"] / 60.0
    ev = events.merge(met[["scale", "seed", "minutes"]], on=["scale", "seed"])
    ev = ev.merge(runs[["scale", "seed", "rows"]], on=["scale", "seed"])

    fig, (ax_a, ax_b, ax_c) = plt.subplots(1, 3, figsize=(7.2, 2.6))
    mean = ev.groupby("scale").mean(numeric_only=True)
    base = mean.loc[1]

    # -- a: indexed workload vs consumption envelope ------------------------
    dims = ["steps", "tool_calls", "output_tokens", "input_tokens", "minutes"]
    idx = pd.DataFrame({d: mean[d] / base[d] for d in dims})
    xs = [SCALE_POS[s] for s in idx.index]
    work = mean["rows"] / base["rows"]

    ax_a.axhline(1.0, color=COL["axis"], lw=0.7, zorder=2)
    ax_a.plot(
        xs, work, marker="o", ms=3.4, lw=1.6, color=COL["reference"],
        mec=COL["surface"], mew=0.6, label="work assigned", zorder=4,
    )
    ax_a.fill_between(
        xs, idx.min(axis=1), idx.max(axis=1), color=COL["derived2"],
        alpha=0.45, lw=0, zorder=3,
    )
    ax_a.plot(
        xs, idx.median(axis=1), marker="o", ms=3.4, lw=1.6, color=COL["grounded"],
        mec=COL["surface"], mew=0.6, label="what the agent did", zorder=5,
    )
    ax_a.set_yscale("log")
    scale_axis(ax_a)
    ax_a.set_ylim(0.45, 400)
    ax_a.set_yticks([0.5, 1, 2, 5, 10, 30, 100, 300])
    ax_a.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(
        lambda v, _: f"{v:g}×"))
    ax_a.yaxis.set_minor_locator(mpl.ticker.NullLocator())
    ax_a.set_xlabel("targets assigned to one agent")
    ax_a.set_ylabel("relative to the 1-target run")
    style_axes(ax_a)
    ax_a.grid(axis="y", color=COL["grid"], lw=0.4, zorder=0)
    ax_a.set_axisbelow(True)
    ax_a.annotate(
        f"{work.loc[893]:.0f}×", xy=(xs[-1], work.loc[893]), xytext=(-2, 5),
        textcoords="offset points", fontsize=6.2, color=COL["ink2"], ha="right",
    )
    ax_a.annotate(
        f"{idx.median(axis=1).loc[893]:.1f}×",
        xy=(xs[-1], idx.median(axis=1).loc[893]), xytext=(-2, -9),
        textcoords="offset points", fontsize=6.2, color=COL["grounded"], ha="right",
    )
    ax_a.legend(loc="upper left", frameon=False, fontsize=6.0,
                handlelength=1.4, labelspacing=0.25, borderpad=0)
    panel_tag(ax_a, "a", "Work rises; effort does not")

    # -- b: tokens against the context window -------------------------------
    ax_b.axhspan(
        AUTO_COMPACT_TOKENS, CONTEXT_WINDOW_TOKENS, color=COL["grid"],
        lw=0, zorder=1,
    )
    ax_b.axhline(CONTEXT_WINDOW_TOKENS, color=COL["muted"], lw=0.7, zorder=2)
    ax_b.text(
        SCALE_POS[1] - 0.3, CONTEXT_WINDOW_TOKENS * 1.25,
        f"context window {CONTEXT_WINDOW_TOKENS // 1000}k  (auto-compact at "
        f"{AUTO_COMPACT_TOKENS // 1000}k)",
        fontsize=5.6, color=COL["ink2"], va="bottom", ha="left",
    )
    emphasis_series(ax_b, ev, "input_tokens", COL["grounded"],
                    "cumulative input tokens")
    emphasis_series(ax_b, ev, "output_tokens", COL["derived2"],
                    "output tokens", marker="s")
    ax_b.set_yscale("log")
    scale_axis(ax_b)
    ax_b.set_ylim(8e3, 3e7)
    ax_b.set_xlabel("targets assigned to one agent")
    ax_b.set_ylabel("tokens per run")
    style_axes(ax_b)
    ax_b.grid(axis="y", color=COL["grid"], lw=0.4, zorder=0)
    ax_b.set_axisbelow(True)
    ax_b.legend(loc="upper left", bbox_to_anchor=(0.0, 1.02), frameon=False,
                fontsize=6.0, handlelength=1.4, labelspacing=0.25, borderpad=0)
    ax_b.annotate(
        f"input = {ev['context_windows_consumed'].min():.0f}–"
        f"{ev['context_windows_consumed'].max():.0f} full context windows",
        xy=(SCALE_POS[1] - 0.3, 6.5e5), fontsize=5.8, color=COL["ink2"],
        ha="left", va="bottom",
    )
    ax_b.annotate(
        f"output = {ev['output_tokens'].max() / CONTEXT_WINDOW_TOKENS:.2f}× "
        "one window at most",
        xy=(SCALE_POS[1] - 0.3, 1.1e4), fontsize=5.8, color=COL["ink2"],
        ha="left", va="bottom",
    )
    panel_tag(ax_b, "b", "Room was available and unused")

    # -- c: internal steps, no configured limit -----------------------------
    emphasis_series(ax_c, ev, "steps", COL["grounded"], "internal steps")
    emphasis_series(ax_c, ev, "tool_calls", COL["derived2"],
                    "of which tool calls", marker="s")
    scale_axis(ax_c)
    ax_c.set_ylim(0, 205)
    ax_c.set_yticks([0, 50, 100, 150])
    ax_c.set_xlabel("targets assigned to one agent")
    ax_c.set_ylabel("events per run")
    style_axes(ax_c)
    ax_c.spines["left"].set_bounds(0, 150)
    ax_c.grid(axis="y", color=COL["grid"], lw=0.4, zorder=0)
    ax_c.set_axisbelow(True)
    ax_c.legend(loc="upper left", frameon=False, fontsize=6.0,
                handlelength=1.4, labelspacing=0.25, borderpad=0)
    ax_c.annotate(
        "no step limit is configured;\n"
        f"{ev['steps'].min()}–{ev['steps'].max()} steps either way",
        xy=(0.98, 0.02), xycoords="axes fraction", fontsize=5.8,
        color=COL["ink2"], ha="right", va="bottom",
    )
    panel_tag(ax_c, "c", "Steps taken, at every workload")

    fig.suptitle(
        "Run consumption measured against the workload it was given",
        x=0.005, ha="left", fontsize=9, fontweight="bold", color=COL["ink"],
    )
    fig.text(
        0.005, 0.01,
        "Panel a indexes each measure to its own 1-target value so five units share one axis; "
        "the band spans internal steps, tool calls, output tokens, cumulative\ninput tokens and "
        "runtime, and its median is drawn. "
        "Seeds shown as light marks in b and c; line is the seed mean. "
        "Counts come from each run's events.jsonl\n(item.completed) and "
        "turn.completed.usage; the window and auto-compact values from agent_budget_summary.json.",
        fontsize=5.8, color=COL["muted"], ha="left", va="bottom",
    )
    fig.tight_layout(rect=(0, 0.135, 1, 0.93), w_pad=2.2)
    save(fig, "fig_r6_self_termination")


# ------------------------------------------------------------------ fig r7 ---
def fig_r7(quality: pd.DataFrame, qsum: pd.DataFrame,
           broadcast: pd.DataFrame) -> None:
    """Do the surviving grounded rows stay informative? Three measures say no.

    a: the literature judgement stops being per-cell-type and becomes one
       statement broadcast across every cell type of a target.
    b: distinct judgements per run is a small flat invariant, so grounded rows
       are restatements of a handful of target-level claims.
    c: that one claim gets applied across responses spanning orders of magnitude,
       which is what makes it non-discriminating on the endpoint's own axis.
    """
    fig, (ax_a, ax_b, ax_c) = plt.subplots(1, 3, figsize=(7.2, 2.6))
    xs = [SCALE_POS[s] for s in qsum["scale"]]

    # -- a: cell types covered vs distinct literature clauses ---------------
    ax_a.plot(
        xs, qsum["cell_types_per_target"], marker="o", ms=3.4, lw=1.6,
        color=COL["reference"], mec=COL["surface"], mew=0.6,
        label="cell types per target", zorder=3,
    )
    ax_a.plot(
        xs, qsum["clauses_per_target"], marker="o", ms=3.4, lw=1.6,
        color=COL["grounded"], mec=COL["surface"], mew=0.6,
        label="distinct literature claims", zorder=4,
    )
    ax_a.axhline(1.0, color=COL["axis"], lw=0.7, zorder=2)
    scale_axis(ax_a)
    ax_a.set_ylim(0, 18)
    ax_a.set_xlabel("targets assigned to one agent")
    ax_a.set_ylabel("per target, grounded rows")
    style_axes(ax_a)
    ax_a.grid(axis="y", color=COL["grid"], lw=0.4, zorder=0)
    ax_a.set_axisbelow(True)
    ax_a.legend(loc="upper right", frameon=False, fontsize=6.0,
                handlelength=1.4, labelspacing=0.25, borderpad=0)
    panel_tag(ax_a, "a", "One claim, broadcast")

    # -- b: distinct judgements per run vs grounded rows -------------------
    ax_b.plot(
        xs, qsum["grounded_rows"] / 3, marker="o", ms=3.4, lw=1.6,
        color=COL["reference"], mec=COL["surface"], mew=0.6,
        label="grounded rows", zorder=3,
    )
    ax_b.plot(
        xs, qsum["distinct_clauses_per_run"], marker="o", ms=3.4, lw=1.6,
        color=COL["grounded"], mec=COL["surface"], mew=0.6,
        label="distinct literature claims", zorder=4,
    )
    scale_axis(ax_b)
    ax_b.set_ylim(0, 105)
    ax_b.set_xlabel("targets assigned to one agent")
    ax_b.set_ylabel("per run")
    style_axes(ax_b)
    ax_b.grid(axis="y", color=COL["grid"], lw=0.4, zorder=0)
    ax_b.set_axisbelow(True)
    ax_b.legend(loc="upper left", frameon=False, fontsize=6.0,
                handlelength=1.4, labelspacing=0.25, borderpad=0)
    panel_tag(ax_b, "b", "A handful of judgements")

    # -- c: share of grounded rows whose claim is not their own -------------
    emphasis_series(
        ax_c, broadcast, "frac_broadcast", COL["grounded"],
        "share of grounded rows",
    )
    scale_axis(ax_c)
    ax_c.set_ylim(0, 105)
    ax_c.set_yticks([0, 25, 50, 75, 100])
    ax_c.set_xlabel("targets assigned to one agent")
    ax_c.set_ylabel("shared claim (% of rows)")
    style_axes(ax_c)
    ax_c.grid(axis="y", color=COL["grid"], lw=0.4, zorder=0)
    ax_c.set_axisbelow(True)
    panel_tag(ax_c, "c", "The row is not its own judgement")

    fig.suptitle(
        "The grounded rows that survive at scale stop being cell-type judgements",
        x=0.005, ha="left", fontsize=9, fontweight="bold", color=COL["ink"],
    )
    fig.text(
        0.005, 0.01,
        f"Grounded = Agree or Inferred; the literature claim is the row summary with the "
        f"differential-expression recital removed. At 893 targets "
        f"{qsum['frac_one_clause'].iloc[-1] * 100:.0f}% of multi-cell-type targets carry ONE\n"
        f"claim for every cell type, and a run makes only "
        f"{qsum['distinct_clauses_per_run'].iloc[-1]:.0f} distinct claims in total. "
        "Panel a counts targets spanning more than one cell type. Panel b divides pooled rows "
        "by the three seeds.\nPanel c: a row counts as shared when its claim appears "
        "verbatim for at least one other cell type of the same target. Note the wide seed "
        "spread at 1-10 targets, where a run has too few\ntargets for the share to be "
        "stable, and the 205-target dip, where one seed produced markedly more distinct "
        "claims than the other two.",
        fontsize=5.8, color=COL["muted"], ha="left", va="bottom",
    )
    fig.tight_layout(rect=(0, 0.135, 1, 0.93), w_pad=2.2)
    save(fig, "fig_r7_literature_quality")


# ------------------------------------------------------------------ fig r8 ---
def fig_r8(agree: pd.DataFrame) -> None:
    """What degrades in the `Agree` rows -- and what does not.

    The argument gets shallower (a, b). The citation does not become fake or
    off-target (c). Panel c is a negative-control panel and is here so the
    figure cannot be read as "the references go bad", which the data refutes.
    """
    fig, (ax_a, ax_b, ax_c) = plt.subplots(1, 3, figsize=(7.2, 2.6))

    # -- a: references behind each Agree row --------------------------------
    emphasis_series(ax_a, agree, "refs_per_row", COL["grounded"], "seed mean")
    scale_axis(ax_a)
    ax_a.set_ylim(0, 4.2)
    ax_a.set_xlabel("targets assigned to one agent")
    ax_a.set_ylabel("references per Agree row")
    style_axes(ax_a)
    ax_a.grid(axis="y", color=COL["grid"], lw=0.4, zorder=0)
    ax_a.set_axisbelow(True)
    panel_tag(ax_a, "a", "Backing thins")

    # -- b: is the claim a multi-step chain? --------------------------------
    emphasis_series(ax_b, agree, "multi_ref_chain", COL["grounded"],
                    "≥2 references (a chain)")
    emphasis_series(ax_b, agree, "scopes_exclusions", COL["muted"],
                    "states what it cannot explain", marker="s")
    scale_axis(ax_b)
    ax_b.set_ylim(-3, 108)
    ax_b.set_yticks([0, 25, 50, 75, 100])
    ax_b.set_xlabel("targets assigned to one agent")
    ax_b.set_ylabel("of Agree rows (%)")
    style_axes(ax_b)
    ax_b.grid(axis="y", color=COL["grid"], lw=0.4, zorder=0)
    ax_b.set_axisbelow(True)
    ax_b.legend(loc="lower left", frameon=False, fontsize=6.0,
                handlelength=1.4, labelspacing=0.25, borderpad=0)
    panel_tag(ax_b, "b", "Arguments lose their steps")

    # -- c: the negative controls ------------------------------------------
    emphasis_series(ax_c, agree, "target_named_in_ref", COL["grounded"], "seed mean")
    scale_axis(ax_c)
    ax_c.set_ylim(-3, 108)
    ax_c.set_yticks([0, 25, 50, 75, 100])
    ax_c.set_xlabel("targets assigned to one agent")
    ax_c.set_ylabel("reference is about the target (%)")
    style_axes(ax_c)
    ax_c.grid(axis="y", color=COL["grid"], lw=0.4, zorder=0)
    ax_c.set_axisbelow(True)
    nn = agree.groupby("scale")["non_neural_source"].mean()
    ax_c.annotate(
        "also unchanged with scale:\n"
        "• every reference carries a PMID\n"
        "• no reference serves >2 targets\n"
        "• evidence gene sets stay coherent\n\n"
        "and NOT a scale effect:\n"
        f"• cross-system sourcing is {nn.loc[1]:.0f}% at\n"
        f"  1 target, {nn.loc[893]:.0f}% at 893",
        xy=(0.04, 0.80), xycoords="axes fraction", fontsize=5.8,
        color=COL["ink2"], ha="left", va="top", linespacing=1.5,
    )
    panel_tag(ax_c, "c", "These do not degrade")

    fig.suptitle(
        "Agree rows keep citing real, on-target work — the argument is what thins",
        x=0.005, ha="left", fontsize=9, fontweight="bold", color=COL["ink"],
    )
    fig.text(
        0.005, 0.01,
        "Panel c plots target-specificity rather than existence, because every Agree row at "
        "every scale cites references that carry a PMID. Cross-system sourcing (citing\n"
        "fibroblast, cardiomyocyte or cancer work for P16 brain data) is common at ONE target "
        "too — the 1-target Psmb4 chain rests partly on fibroblast siRNA work — so it is "
        "standing\npractice rather than a scale effect, and is reported as a number rather "
        "than plotted as a trend. Seeds shown as light marks; line is the seed mean. "
        "Verbatim exhibits in AGREE_EXAMPLES.md.",
        fontsize=5.8, color=COL["muted"], ha="left", va="bottom",
    )
    fig.tight_layout(rect=(0, 0.135, 1, 0.93), w_pad=2.2)
    save(fig, "fig_r8_agree_quality")


def write_agree_examples(summary: pd.DataFrame) -> None:
    """Verbatim Agree exhibits: strongest at 1 target, and both ends at 893."""
    picks = [
        (1, 17, "Psmb4", "the 1-target reference case"),
        (893, 17, "Tsc2", "893 targets, still strong"),
        (893, 17, "Atp2a2", "893 targets, cross-system transfer"),
        (893, 17, "Apc", "893 targets, textbook inference on a review"),
    ]
    lines = [
        "# `Agree` rows at 1 vs 893 targets — verbatim exhibits",
        "",
        "Generated by `replot_scaling.py`. Each block is one emitted row, with the",
        "references and evidence record it points at, copied verbatim.",
        "",
        "The claim under test was that `Agree` examples are strong at 1 target and no",
        "longer retain quality at 893. What the exhibits show is narrower: the",
        "**argument structure** thins (multi-reference chains with explicit scope limits",
        "become single-reference one-step assertions), while the **citations stay real and",
        "on-target**. At 893 targets quality is also *heterogeneous* — Tsc2 below is as",
        "strong as the 1-target case; Atp2a2 and Apc are not.",
        "",
    ]
    for scale, seed, target, label in picks:
        run = summary[
            (summary["scale_targets"] == scale) & (summary["seed"] == seed)
        ]
        if not len(run):
            continue
        run_dir = Path(run.iloc[0]["run_dir"])
        refs = {
            r["ref_id"]: r
            for r in map(json.loads, (run_dir / "q3_references.jsonl").open())
        }
        evidence = {
            e["evidence_id"]: e
            for e in map(json.loads, (run_dir / "q3_evidence.jsonl").open())
        }
        rec = next(
            (
                x
                for x in map(json.loads, (run_dir / "q3_cell_type_specificity.jsonl").open())
                if normalize_flag(x["flag"]) == "agree" and x["gene_target"] == target
            ),
            None,
        )
        if rec is None:
            continue
        cited = [refs[i] for i in (rec.get("ref_ids") or []) if i in refs]
        lines += [
            f"## {target} — {label}",
            "",
            f"`n={scale}` targets, seed {seed}, cell type `{rec['cell_type']}`  ",
            f"declared context match: `{rec.get('lit_context')}`  ",
            f"references: **{len(cited)}**",
            "",
            "> " + rec.get("summary", "").replace("\n", " "),
            "",
        ]
        for r in cited:
            lines += [
                f"- **[{r.get('source_type')}] PMID {r.get('pmid')}** — "
                f"{(r.get('citation') or '').strip()}",
                f"  - *why cited:* {(r.get('description') or '').strip()}",
            ]
        for i in rec.get("evidence_ids") or []:
            e = evidence.get(i, {})
            lines += [
                "",
                f"- *evidence genes:* `{e.get('genes')}`",
            ]
        lines.append("")
    (HERE / "AGREE_EXAMPLES.md").write_text("\n".join(lines))
    print("  wrote AGREE_EXAMPLES.md")


# -------------------------------------------------------------------- main ---
def main() -> None:
    load_style()
    rows, summary = load_rows()
    runs = run_level(rows)
    events = load_events(summary)
    quality = load_literature_quality(summary)
    qsum = literature_quality_summary(quality)
    broadcast = literature_broadcast_by_run(quality)
    agree = agree_quality(summary)
    anchors = anchor_differentiation(rows)
    dissent = anchor_dissent_by_run(rows)
    diffmeas = differentiation_measures(rows)
    bursts = burst_stats(rows)
    instability = label_instability(rows)

    print("\n== key numbers ==")
    m = runs.groupby("scale")[["rows", "grounded", "grounded_targets", "supported_fraction"]].agg(
        ["mean", "min", "max"]
    )
    print(m.round(2).to_string())
    print(
        f"\ngrounded rows/run, scales 10-893: mean "
        f"{runs[runs['scale'] >= 10]['grounded'].mean():.1f}, range "
        f"{runs[runs['scale'] >= 10]['grounded'].min()}-"
        f"{runs[runs['scale'] >= 10]['grounded'].max()}"
    )
    mm = runs.groupby("scale")[["rows", "grounded"]].mean()
    print(
        f"scale 10 -> 893: rows x{mm.loc[893, 'rows'] / mm.loc[10, 'rows']:.1f}, "
        f"grounded x{mm.loc[893, 'grounded'] / mm.loc[10, 'grounded']:.2f}"
    )
    print(f"Disagree rows anywhere: {int(runs['disagree'].sum())} / {int(runs['rows'].sum())}")
    print("\n== anchor-10 cohort (fixed targets, fixed 422 eligible rows) ==")
    print(anchors.round(3).to_string(index=False))
    print("\n== differentiation measures on the anchor cohort (evidence for fig_r1c) ==")
    print(diffmeas.round(3).to_string(index=False))
    first, last = diffmeas.iloc[0], diffmeas.iloc[-1]
    ctrl = diffmeas[diffmeas["scale"] >= 10]
    c0, c1 = ctrl.iloc[0], ctrl.iloc[-1]
    for col in ["distinct_flags", "entropy_norm", "minority_pct",
                "cell_types_called_differently"]:
        print(
            f"  {col:32s} n1->n893 {first[col]:7.3f} -> {last[col]:7.3f}"
            f"   |  controlled n10->n893 {c0[col]:7.3f} -> {c1[col]:7.3f}"
        )
    print(
        "  NOTE n1/n3 are uncontrolled: 3 and 9 target-instances at "
        f"{first['rows_per_target']:.1f} rows each vs {c1['rows_per_target']:.1f} from n10 on."
    )

    print("\n== burstiness vs permutation null ==")
    print(bursts.round(1).to_string(index=False))
    print(
        f"\nfixed-pair label instability: {instability['changed_fraction'] * 100:.1f}% of "
        f"{instability['n_pairs']} pairs change label (distribution {instability['distribution']})"
    )

    print("\n== per-run consumption (no step / token / timeout limit configured) ==")
    cols = ["steps", "tool_calls", "input_tokens", "output_tokens", "reasoning_tokens"]
    print(events.groupby("scale")[cols].mean().round(0).to_string())
    print(
        f"\nsteps {events['steps'].min()}–{events['steps'].max()}, "
        f"tool calls {events['tool_calls'].min()}–{events['tool_calls'].max()}, "
        f"output tokens {events['output_tokens'].min():,}–{events['output_tokens'].max():,}"
    )
    print(
        f"cumulative input = {events['context_windows_consumed'].min():.1f}–"
        f"{events['context_windows_consumed'].max():.1f} × the {CONTEXT_WINDOW_TOKENS:,}-token "
        f"context window; output = "
        f"{events['output_tokens'].max() / CONTEXT_WINDOW_TOKENS:.2f}× one window at most"
    )

    print("\n== literature quality of the grounded (Agree/Inferred) rows ==")
    show = [
        "scale", "grounded_rows", "cell_types_per_target", "clauses_per_target",
        "frac_one_clause", "distinct_clauses_per_run", "rows_per_clause",
        "refs_per_row", "declares_cell_type", "declares_stage", "review_frac",
        "agree_share", "hedged_inferred", "median_deg_fold_per_clause",
    ]
    print(qsum[show].round(3).to_string(index=False))

    print("\n== controlled trace: one identical pair at every scale ==")
    trace = quality[
        (quality["seed"] == 17)
        & (quality["gene_target"] == "Psmb4")
        & (quality["cell_type"] == "005 L4-5 IT CTX Glut")
    ].sort_values("scale")
    for row in trace.itertuples():
        print(
            f"  n={row.scale:4d}  {FLAG_LABELS[row.flag]:14s} refs={row.n_refs} "
            f"ctx={row.n_context}  {row.lit_clause[:96]}"
        )

    print("\n== Agree-row quality: what thins vs what holds ==")
    cols = ["agree_rows", "refs_per_row", "multi_ref_chain", "scopes_exclusions",
            "review_backed", "target_named_in_ref", "all_refs_have_pmid",
            "non_neural_source", "evidence_genes"]
    print(agree.groupby("scale")[cols].mean().round(2).to_string())

    print("\n== figures ==")
    fig_r1(runs, anchors, dissent)
    fig_r2(rows, runs)
    fig_r3(rows, bursts, anchors)
    fig_r4(rows, instability)
    fig_r5(summary, runs)
    fig_r6(events, runs, summary)
    fig_r7(quality, qsum, broadcast)
    fig_r8(agree)
    write_agree_examples(summary)

    runs.to_csv(HERE / "replot_run_level.csv", index=False)
    anchors.to_csv(HERE / "replot_anchor_differentiation.csv", index=False)
    bursts.to_csv(HERE / "replot_burstiness.csv", index=False)
    diffmeas.to_csv(HERE / "replot_differentiation_measures.csv", index=False)
    events.to_csv(HERE / "replot_run_consumption.csv", index=False)
    qsum.to_csv(HERE / "replot_literature_quality.csv", index=False)
    agree.to_csv(HERE / "replot_agree_quality.csv", index=False)
    quality.drop(columns=["context", "ref_key"]).to_csv(
        HERE / "replot_literature_rows.csv", index=False
    )
    print(
        "  wrote replot_run_level.csv / replot_anchor_differentiation.csv / "
        "replot_burstiness.csv / replot_differentiation_measures.csv / "
        "replot_run_consumption.csv / "
        "replot_literature_quality.csv / replot_literature_rows.csv / "
        "replot_agree_quality.csv"
    )


if __name__ == "__main__":
    main()
