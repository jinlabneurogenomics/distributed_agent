"""Join scored relational findings to curated experimental measurements."""
import pandas as pd
from .paths import RUNS, INPUTS
from .common import write_table


def prepare():
    findings = pd.read_csv(RUNS / 'novelty/findings.csv')
    measurements = pd.read_csv(INPUTS / 'novelty/finding_measurements.csv')
    keys = ['gene', 'finding_id']
    frame = findings.merge(measurements, on=keys, validate='one_to_one')
    if len(frame) != 3397 or len(frame) != len(findings):
        raise ValueError('Expected complete measurements for 3,397 relational findings')
    if not frame.evidence.ge(0).all():
        raise ValueError('Relational scores must be nonnegative')
    write_table(frame, 'novelty/analysis_table.csv')
