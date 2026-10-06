"""Build notebook inputs and supplementary workbooks from saved experiments."""
import argparse
import json
from pathlib import Path
import shutil
import pandas as pd
from .paths import INPUTS, TABLES
from . import biology, depletion, holdout, scaling


def publish_curated():
    """Expose fixed measurements and reviewed annotations alongside computed tables."""
    for name in json.loads((INPUTS / 'curated_tables.json').read_text()):
        source, destination = INPUTS / name, TABLES / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix in ('.csv', '.tsv'):
            frame = pd.read_csv(source, sep='\t' if source.suffix == '.tsv' else ',')
            if frame.columns.duplicated().any() or frame.empty:
                raise ValueError(f'Invalid curated input: {name}')
        shutil.copyfile(source, destination)


def supplementary_tables():
    """Write one workbook per analysis from the same tables consumed by notebooks."""
    for directory in sorted(TABLES.iterdir()):
        if not directory.is_dir():
            continue
        paths = sorted(p for p in directory.iterdir() if p.suffix in ('.csv', '.tsv'))
        if not paths:
            continue
        with pd.ExcelWriter(TABLES / f'{directory.name}.xlsx', engine='openpyxl') as writer:
            sheets = []
            for index, path in enumerate(paths, 1):
                sheet = f'{index:02d}_{path.stem}'[:31]
                frame = pd.read_csv(path, sep='\t' if path.suffix == '.tsv' else ',')
                frame.to_excel(writer, sheet_name=sheet, index=False)
                sheets.append({'sheet': sheet, 'table': path.name, 'rows': len(frame)})
            pd.DataFrame(sheets).to_excel(writer, sheet_name='Contents', index=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tables-only', action='store_true', help='Skip Excel workbook generation')
    args = parser.parse_args()
    TABLES.mkdir(parents=True, exist_ok=True)
    publish_curated()
    from . import literature, novelty, survey
    for module in (biology, scaling, holdout, depletion, literature, novelty, survey):
        print(f'Preparing {module.__name__.rsplit(".", 1)[-1]}...', flush=True)
        module.prepare()
    if not args.tables_only:
        supplementary_tables()
    print(f'Prepared manuscript tables in {TABLES}')


if __name__ == '__main__':
    main()
