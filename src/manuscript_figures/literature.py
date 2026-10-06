"""Summarize reviewed literature labels for original and shuffled findings."""
import pandas as pd
from .paths import INPUTS
from .common import write_table

ARMS = ('Unshuffled', 'Within-screen shuffled', 'Out-of-screen shuffled')
FLAGS = {'agree': 'Agree', 'disagree': 'Disagree', 'inferred': 'Inferred', 'no_literature': 'No Literature'}
SCOPES = {
    'program_response': 'Pathway or state change',
    'comparator_relationship': 'Perturbation convergence/divergence',
    'expected_program_test': 'Prior-prediction outcome',
    'cell_group_relationship': 'Cell-group-dependent response',
    'mixed': 'Other',
}


def prepare():
    findings = pd.read_csv(INPUTS / 'literature/final_classified_findings.csv')
    flags, scopes = [], []
    for layer in ('primary', 'sensitivity'):
        valid = findings['valid_for_' + layer].astype(str).str.lower().eq('true')
        for arm in ARMS:
            selected = findings[valid & findings.arm.eq(arm)]
            if selected.empty or not set(selected.flag) <= FLAGS.keys() or not set(selected.claim_scope) <= SCOPES.keys():
                raise ValueError(f'Invalid reviewed findings for {layer}, {arm}')
            for column, labels, output, key in (('flag', FLAGS, flags, 'flag'), ('claim_scope', SCOPES, scopes, 'scope')):
                counts = selected[column].value_counts()
                for value, label in labels.items():
                    count = int(counts.get(value, 0))
                    output.append(dict(analysis_layer=layer, arm=arm, **{key: value, key + '_label': label},
                                       count=count, percent=round(100 * count / len(selected), 3), n_findings=len(selected)))
    write_table(pd.DataFrame(flags), 'literature/final_overall_distribution.csv')
    write_table(pd.DataFrame(scopes), 'literature/final_finding_scope_distribution.csv')
    reviewed = pd.read_csv(INPUTS / 'literature/meaningful_primary_findings_union.csv')
    counts = reviewed.flag.value_counts()
    n = len(reviewed)
    taxonomy = [dict(flag=label, has_literature=int(flag != 'no_literature'), count=int(counts.get(label, 0)),
                     percent=round(100 * counts.get(label, 0) / n, 1), n_findings=n)
                for flag, label in FLAGS.items()]
    grounded = sum(row['count'] for row in taxonomy if row['has_literature'])
    taxonomy.append(dict(flag='Has literature (Agree+Disagree+Inferred)', has_literature=1,
                         count=grounded, percent=round(100 * grounded / n, 1), n_findings=n))
    if sum(row['count'] for row in taxonomy[:4]) != 1519:
        raise ValueError('Expected 1,519 reviewed primary findings')
    write_table(pd.DataFrame(taxonomy), 'literature/union_flag_taxonomy.csv')
