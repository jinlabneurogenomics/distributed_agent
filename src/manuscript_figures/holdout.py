"""Parse saved holdout predictions and compute replicate performance."""
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from .paths import RUNS, INPUTS
from .common import prediction_rows, write_table


def prepare():
    records = []
    for source in ("distributed_agents", "codex"):
        for run in sorted((RUNS / "holdout" / source).glob("replicate_*/*/answer.txt")):
            replicate = int(run.parents[1].name.split("_")[-1])
            public_method = "codex" if source == "codex" else "distributed"
            parsed = prediction_rows(run.read_text())
            if len(parsed) != 1 or parsed[0]["target_name"].lower() != run.parent.name.lower():
                raise ValueError(f"Answer target does not match run: {run}")
            records.append(dict(method=public_method, replicate=replicate, **parsed[0]))
    predictions = pd.DataFrame(records)
    truth = pd.read_csv(INPUTS / "holdout/measurements.csv")[["target_name", "actual_n_degs"]]
    if len(predictions) != 1632 or predictions.duplicated(["method", "replicate", "target_name"]).any():
        raise ValueError("Expected six unique sets of 272 target predictions")
    predictions = predictions.merge(truth, on="target_name", validate="many_to_one")
    if len(predictions) != 1632:
        raise ValueError("Predictions and truth do not have identical target sets")
    predictions["signed_log1p_error"] = np.log1p(predictions.predicted_n_degs) - np.log1p(predictions.actual_n_degs)
    predictions["absolute_log1p_error"] = predictions.signed_log1p_error.abs()
    metrics = []
    for (method, replicate), group in predictions.groupby(["method", "replicate"]):
        if len(group) != 272:
            raise ValueError("Incomplete replicate")
        metrics.append(dict(method=method, replicate=replicate, targets=len(group),
                            spearman=spearmanr(group.actual_n_degs, group.predicted_n_degs).statistic,
                            mse_log1p=float((group.signed_log1p_error ** 2).mean()),
                            mean_absolute_log1p_error=float(group.absolute_log1p_error.mean())))
    write_table(predictions.sort_values(["method", "replicate", "target_name"]), "holdout/replicate_predictions.csv")
    write_table(pd.DataFrame(metrics), "holdout/replicate_metrics.csv")
    distributed = predictions.loc[predictions.method.eq("distributed")].pivot(
        index="target_name", columns="replicate", values="predicted_n_degs"
    ).rename(columns={1: "original_distributed_agents", 2: "toolbox_rep_1", 3: "toolbox_rep_2"}).rename_axis(columns=None)
    merged = distributed.reset_index().merge(truth, on="target_name", validate="one_to_one")
    merged["actual_effect"] = np.where(merged.actual_n_degs.gt(0), "Actual > 0 DEGs", "Actual = 0 DEGs")
    write_table(merged, "holdout/distributed_agents_3x_merged.tsv")
    prepare_figure_comparison()


def prepare_figure_comparison():
    """Retain the manuscript's original comparison cohort when adding replicates."""
    observations = pd.read_csv(INPUTS / 'holdout/measurements.csv')
    saved = pd.read_csv(RUNS / 'holdout/figure_comparison/predictions.csv')
    frame = observations.merge(saved, on='target_name', validate='one_to_one')
    if len(frame) != 272:
        raise ValueError('Expected 272 targets in the published comparison')
    frame['actual_effect'] = frame.actual_n_degs.gt(0)
    for method in ('codex', 'distributed_agents'):
        count = frame[method + '_predicted_n_degs']
        signed = np.log1p(count) - np.log1p(frame.actual_n_degs)
        frame[method + '_predicted_effect'] = count.gt(0)
        frame[method + '_log1p_squared_error'] = signed ** 2
        frame[method + '_effect_correct'] = count.gt(0).eq(frame.actual_effect)
        frame[method + '_absolute_log1p_error'] = signed.abs()
        frame[method + '_signed_log1p_error'] = signed
        frame[method + '_exact_count'] = count.eq(frame.actual_n_degs)
    difference = frame.codex_absolute_log1p_error - frame.distributed_agents_absolute_log1p_error
    frame['closer_log1p_count'] = np.select([difference > 1e-12, difference < -1e-12], ['distributed_agents', 'codex'], default='tie')
    write_table(frame, 'holdout/task1_per_target.csv')
