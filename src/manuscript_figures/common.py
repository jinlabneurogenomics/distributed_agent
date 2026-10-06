"""Shared readers and table writers for manuscript analyses."""
import json
import re
from pathlib import Path
import pandas as pd
from .paths import TABLES


def read_jsonl(path):
    with Path(path).open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_table(frame, relative):
    path = TABLES / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".parquet":
        frame.to_parquet(path, index=False)
    else:
        frame.to_csv(path, sep="\t" if path.suffix == ".tsv" else ",", index=False)
    return path


def prediction_rows(text):
    """Read the task's TSV answer, allowing its optional Markdown code fence."""
    blocks = re.findall(r"```(?:tsv)?\s*\n(.*?)```", text, re.S)
    for block in blocks or [text]:
        lines = block.strip().splitlines()
        for start, line in enumerate(lines):
            columns = [x.strip() for x in line.split("\t")]
            if "target_name" not in columns or "predicted_n_degs" not in columns:
                continue
            rows = []
            for line in lines[start + 1:]:
                cells = line.strip().split("\t")
                if len(cells) != len(columns):
                    continue
                row = dict(zip(columns, cells))
                try:
                    value = float(row["predicted_n_degs"])
                except ValueError:
                    continue
                if value < 0 or not value.is_integer():
                    raise ValueError("Predicted DEG counts must be nonnegative integers")
                rows.append({"target_name": row["target_name"], "predicted_n_degs": int(value)})
            if rows:
                return rows
    raise ValueError("No target_name/predicted_n_degs TSV answer found")
