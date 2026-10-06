"""Aggregate single-agent classifications and measured effort at each workload."""
from collections import Counter, defaultdict
import json
import re
import pandas as pd
from .paths import RUNS, INPUTS
from .common import read_jsonl, write_table
from .flag_style import normalize_flag


def appendix(report, title, strict=False):
    if strict:
        lines = report.splitlines()
        heading = next((i for i, line in enumerate(lines)
                        if re.match(r'^#{1,6}\s+' + re.escape(title) + r'\s*$', line.strip(), re.I)), None)
        fence = next((i for i in range(heading + 1, len(lines))
                      if lines[i].strip().lower() == '```jsonl'), None) if heading is not None else None
        rows = []
        if fence is not None:
            for line in lines[fence + 1:]:
                if line.strip() == '```':
                    break
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(row, dict):
                    rows.append(row)
        return rows
    start = report.find(title)
    rows = []
    if start < 0:
        return rows
    for line in report[start:].splitlines():
        line = line.strip()
        if line.startswith('{'):
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        elif rows and line.startswith('#'):
            break
    return rows


def distributed_comparison(paths):
    deg = pd.read_parquet(INPUTS / 'scaling/downstream_fdr_0_1.parquet', columns=['gene_target', 'cell_type'])
    universe = {t: set(g.cell_type) for t, g in deg.groupby('gene_target')}
    reviewed, production = defaultdict(list), defaultdict(list)
    for row in pd.read_csv(INPUTS / 'literature/meaningful_primary_findings_union.csv').itertuples(index=False):
        for cell in json.loads(row.supported_cell_types_json or '[]'):
            if cell in universe.get(row.gene_target, ()):
                reviewed[(row.gene_target, cell)].append(normalize_flag(row.flag))
    for report in read_jsonl(RUNS / 'reports/july/reports.jsonl'):
        target = report['gene_target']
        for finding in appendix(report['report'], 'Biological Findings JSONL'):
            if not isinstance(finding.get('lit_direction'), str):
                continue
            for cell in finding.get('cell_types') or []:
                if cell in universe.get(target, ()):
                    production[(target, cell)].append(normalize_flag(finding['lit_direction']))
    placements = {**reviewed, **{k: v for k, v in production.items() if k not in reviewed}}
    references = {r['gene_target']: len(appendix(r['report'], 'References JSONL', strict=True))
                  for r in read_jsonl(RUNS / 'reports/june/reports.jsonl')}
    if len(references) != 2046 or sum(references.values()) != 16555:
        raise ValueError('June report/reference coverage differs from the experiment')
    records = []
    for run in paths:
        seed, scale = int(run.parent.name[5:]), int(run.name[1:])
        targets = json.loads((run / 'targets.json').read_text())['gene_targets']
        assigned = set(targets)
        pairs = [(pair, flags) for pair, flags in placements.items() if pair[0] in assigned]
        weights = dict.fromkeys(('agree', 'disagree', 'inferred', 'no_literature'), 0.0)
        for pair, flags in pairs:
            for flag in flags:
                weights[flag] += 1 / len(flags)
        grounded = sum(weights[f] for f in ('agree', 'disagree', 'inferred'))
        records.append(dict(arm='multi', seed=seed, scale=scale,
                            workload_pairs=sum(len(universe.get(t, ())) for t in assigned),
                            calls=len(pairs), reviewed_pairs=sum(pair in reviewed for pair, flags in pairs),
                            references=sum(references.get(t, 0) for t in targets), grounded=grounded,
                            **weights, grounded_share=grounded / len(pairs)))
    return pd.DataFrame(records)


def prepare():
    summaries, consumption, classifications = [], [], []
    paths = sorted((RUNS / "scaling").glob("seed-*/n*"))
    if len(paths) != 24:
        raise ValueError(f"Expected 24 workload runs; found {len(paths)}")
    for run in paths:
        seed, scale = int(run.parent.name[5:]), int(run.name[1:])
        targets = json.loads((run / "targets.json").read_text())["gene_targets"]
        rows = read_jsonl(run / "q3_cell_type_specificity.jsonl")
        references = read_jsonl(run / "q3_references.jsonl")
        pairs = {(r["gene_target"], r["cell_type"]) for r in rows}
        if len(targets) != scale or len(rows) != len(pairs) or {r["gene_target"] for r in rows} != set(targets):
            raise ValueError(f"Unexpected target or pair coverage in {run.name}")
        flags = Counter(r["flag"].lower().replace(" ", "_") for r in rows)
        summary = dict(arm="single", seed=seed, scale=scale, workload_pairs=len(rows),
                       calls=len(rows), reviewed_pairs=0, references=len(references))
        summary.update({f: flags[f] for f in ("agree", "disagree", "inferred", "no_literature")})
        summary["grounded"] = summary["agree"] + summary["disagree"] + summary["inferred"]
        summary["grounded_share"] = summary["grounded"] / summary["calls"]
        summaries.append(summary)
        classifications.extend(dict(seed=seed, scale=scale, **r) for r in rows)
        kinds, usage = Counter(), {}
        for event in read_jsonl(run / "events.jsonl"):
            if event["type"] == "item.completed":
                kinds[event["item"]["type"]] += 1
            elif event["type"] == "turn.completed":
                usage = event["usage"]
        item = dict(seed=seed, scale=scale, steps=sum(kinds.values()),
                    tool_calls=kinds["mcp_tool_call"], commands=kinds["command_execution"], messages=kinds["agent_message"])
        item.update({k: usage.get(k, 0) for k in ("input_tokens", "cached_input_tokens", "output_tokens")})
        item["reasoning_tokens"] = usage.get("reasoning_output_tokens", 0)
        item["context_windows_consumed"] = item["input_tokens"] / 272000
        consumption.append(item)
    distributed = distributed_comparison(paths)
    comparison = pd.concat([distributed, pd.DataFrame(summaries)], ignore_index=True)
    comparison = comparison.sort_values(["arm", "scale", "seed"]).reset_index(drop=True)
    write_table(comparison, "scaling/replot_single_vs_multi_layered.csv")
    write_table(pd.DataFrame(consumption).sort_values(["scale", "seed"]), "scaling/replot_run_consumption.csv")
    flat = pd.DataFrame(classifications)
    for column in ("lit_context", "ref_ids", "evidence_ids"):
        flat[column] = flat[column].map(json.dumps)
    write_table(flat, "scaling/single_agent_classifications.csv")
