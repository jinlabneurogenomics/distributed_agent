"""Extract the complete set of DE rows needed for the manuscript biology panels."""
import argparse
from pathlib import Path
import pyarrow.dataset as ds
import pyarrow.parquet as pq
from .paths import INPUTS

TARGETS = (
    'Psmb4', 'Pomp', 'Hspa5', 'Hspa8', 'Hspa9', 'Lonp1', 'Opa1', 'Dnm1l',
    'Smarcb1', 'Smarcc2', 'Arid2', 'Arid1a', 'Grin2a', 'Grin2b', 'Tsc1',
    'Tsc2', 'Rab7', 'Wdr26',
)
COLUMNS = (
    'names', 'gene_target', 'group_name', 'logfoldchanges', 'pvals', 'pvals_adj',
    'scores', 'n_pert_matched', 'n_ctrl_matched',
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='Full Wilcoxon DE Parquet file')
    args = parser.parse_args()
    table = ds.dataset(args.source, format='parquet').to_table(
        columns=list(COLUMNS), filter=ds.field('gene_target').isin(TARGETS), use_threads=False,
    )
    if set(table.column('gene_target').to_pylist()) != set(TARGETS):
        raise ValueError('The source does not contain all 18 figure targets')
    destination = INPUTS / 'biology/differential_expression.parquet'
    destination.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, destination, compression='zstd')
    print(f'Wrote {table.num_rows:,} rows to {destination}')


if __name__ == '__main__':
    main()
