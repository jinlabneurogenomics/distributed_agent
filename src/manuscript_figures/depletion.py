"""Reconstruct depletion recall curves from saved ranked answers."""
import io
import re
import numpy as np
import pandas as pd
from .paths import INPUTS, RUNS
from .common import write_table


def ranked_answer(path):
    text = path.read_text()
    blocks = re.findall(r'```tsv\s*\n(.*?)```', text, re.S | re.I)
    if len(blocks) != 1:
        raise ValueError(f'Expected one TSV answer in {path}')
    frame = pd.read_csv(io.StringIO(blocks[0]), sep='\t').sort_values('rank')
    if frame['rank'].tolist() != list(range(1, len(frame) + 1)) or frame.gene_target.duplicated().any():
        raise ValueError(f'Invalid ranking in {path}')
    return frame.gene_target.tolist()


def prepare():
    truth = pd.read_csv(INPUTS / 'depletion/top150_depletion_151_TH_Prkcd_Grin2c_Glut_predicted_group.csv').sort_values('depletion_rank').head(100)
    visible = set(truth.loc[truth.depletion_rank.mod(2).eq(1), 'gene_target'])
    heldout = set(truth.loc[truth.depletion_rank.mod(2).eq(0), 'gene_target'])
    if len(visible) != 50 or len(heldout) != 50 or visible & heldout:
        raise ValueError('Expected disjoint 50-target visible and held-out sets')
    records, all_records = [], []
    for method, label in [('distributed_agents', 'Distributed Agents'), ('codex', 'Codex'), ('biomni', 'BioMNI')]:
        curves = []
        for rep in range(1, 4):
            ranking = ranked_answer(RUNS / f'depletion/{method}/replicate_{rep}/answer.txt')
            if len(ranking) != 50 or set(ranking) & visible:
                raise ValueError(f'{label} replicate {rep} violates the 50 non-seed target contract')
            curve = [len(set(ranking[:k]) & heldout) / 50 for k in range(5, 51, 5)]
            curves.append(curve)
            all_records.extend(dict(cohort=label, series='individual', replicate=rep, cutoff_k=k, recall=value)
                               for k, value in zip(range(5, 51, 5), curve))
        all_records.extend(dict(cohort=label, series='median', replicate='', cutoff_k=k, recall=value)
                           for k, value in zip(range(5, 51, 5), np.median(curves, axis=0)))
    records.extend(row for row in all_records if row['cohort'] != 'BioMNI')
    for label, name, rank in [('DepMap', 'depmap_top100_annotated.csv', 'depmap_rank'), ('Top DEG', 'complete_starting_deg_ranking.tsv', 'starting_rank')]:
        frame = pd.read_csv(INPUTS / 'depletion' / name, sep='\t' if name.endswith('.tsv') else ',').sort_values(rank)
        ranking = [g for g in frame.gene_target if g not in visible][:50]
        if len(ranking) != 50 or len(set(ranking)) != 50:
            raise ValueError('Baseline ranking must contain 50 distinct non-seed targets')
        rows = [dict(cohort=label, series='baseline', replicate='', cutoff_k=k,
                     recall=len(set(ranking[:k]) & heldout) / 50) for k in range(5, 51, 5)]
        records.extend(rows)
        all_records.extend(rows)
    write_table(pd.DataFrame(records), 'depletion/depletion-best-vs-codex-heldout-recall.tsv')
    write_table(pd.DataFrame(all_records), 'depletion/all_method_recall.csv')
