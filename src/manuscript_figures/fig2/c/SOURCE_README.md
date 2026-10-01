# Updated Figure 2C: sources accessed versus sources cited

This directory recreates the selected cost × wall-clock design from
`../fig_panelC.svg` with the full June run and the source-access audit.

The updated panel replaces the old 300-trace proxy (web-search queries versus
references retained) with directly audited source use across all 2,046 June
reports:

| quantity | total | mean/report | median/report | counting unit |
|---|---:|---:|---:|---|
| sources accessed | 39,185 | 19.15 | 18 | distinct report–source pair |
| sources cited | 16,445 | 8.04 | 8 | distinct report–source pair |
| final citation entries | 16,555 | 8.09 | 8 | raw report reference entry |

The top densities compare distinct sources cited and accessed within each
report. Both density markers show means (8.04 cited and 19.15 accessed),
matching the values used in the workload calculation. The headline uses 16,555
because this is the final citation-entry total
reported in `data/summary_statistics.csv`; the 110-entry difference from 16,445
comes from duplicate/canonically equivalent references within reports. A source
used by two reports counts once in each report, matching the per-report unit of
analysis.

The analyst scenarios use the means of the distinct per-report counts: 8.04
cited sources or 19.15 accessed sources, at the existing heuristic of 15 minutes
per perturbation plus 10 minutes per source read and $25/hour. The agent runtime
and cost assumptions are unchanged from the original panel: median 31.6 minutes
over 24 single-target runs and an estimated $2.3439 per target.

## Reproduce

From the repository root:

```bash
python manuscript/fig2/c/updated/prepare_source_access_data.py
pixi run python manuscript/fig2/c/updated/plot_panelC.py
```

The first command verifies and aggregates the canonical June source-access
ledger into `source_access_per_report.csv` and copies its audit summary. The
second writes:

- `fig_panelC.svg` — editable-text vector deliverable;
- `fig_panelC.png` — 400 dpi raster deliverable;
- `fig_panelC_sources.{svg,png}` — square standalone source-distribution panel;
- `fig_panelC_cost_time.{svg,png}` — wide standalone cost-by-time panel using
  the original crop's 974 × 534 dimensions;
- `fig_panelC_analysis.json` — exact plotted inputs and derived estimates.

The standalone source panel uses the same per-report distributions as the top
band of `fig_panelC`, rotated onto a vertical count axis so the labels and corpus
totals remain legible when the panel is placed as a square. Its totals use the
audit's comparable unit: distinct report–source pairs, counted separately when
the same source appears in different reports.

The standalone cost-by-time panel follows the supplied simplified layout. Its
log cost axis ends at $240k and uses a final $200k tick because the largest
plotted estimate is $176.1k; the legacy $300k tick and $1.1m upper bound would
compress the meaningful interval between $100k and that estimate.

The prepared CSV and JSON inputs are retained here so the figure does not
depend on the large trace-level ledger at render time.

## Manuscript-ready methods text

Runtime, token use, and literature retrieval were extracted from system logs.
Per-target runtime was measured in a separate benchmark of 24 completed
single-target invocations of the production report task (mean, 32.8 min;
median, 31.6 min; interquartile range, 24.7–36.8 min). The approximately
32-min runtime shown in the panel is the median per-target runtime and is an
idealized lower bound that assumes all 2,046 independent tasks execute in
parallel; it is neither a measured duration of the June production batch nor
the sum of agent compute time. The June production logs did not retain
per-report end-to-end timing, but did record 9.17 billion cumulative input
tokens (including repeated conversation history), 183.85 million input tokens
after repeated history was removed, and 74.34 million sampled output tokens.

Retrieved sources included article or metadata records from PubMed, PubMed
Central, DOI-linked publisher and preprint pages, and literature APIs such as
bioRxiv, Crossref, OpenAlex, and Semantic Scholar; structured responses from
biological resources including Open Targets, ChEMBL/EMBL-EBI, STRING, UniProt,
Reactome, the Human Protein Atlas, ClinicalTrials.gov, Ensembl, gnomAD, RCSB
PDB, BindingDB, MGI, and NCBI Gene; and other successfully opened webpages or
direct HTTP responses. A source was counted as accessed only when a successful
open or response returned source content or metadata in a model-visible tool
result and therefore entered the agent's context window. Search-result cards,
failed or blocked calls, local parquet output, and downloaded files whose
contents were not subsequently printed into a model-visible result were
excluded. Literature records were canonicalized across PMID, PMCID, and DOI,
and repeated access to the same canonical source within one report was counted
once. A citation was counted when a parseable reference entry with a non-empty
HTTP URL appeared in the final structured report. The same source accessed or
cited by different perturbation-scoped agents was counted once for each report
because the agents ran independently and did not share context. Across 2,046
reports, this procedure identified 39,185 distinct report–source accesses
(mean, 19.15 per report; median, 18), 16,445 distinct report–source citations
(mean, 8.04; median, 8), and 16,555 raw final reference entries. The difference
between the latter two totals reflects duplicate or canonically equivalent
references within reports. Retrieval and citation counts were extracted from
the execution logs and final structured reports, respectively.

The source-access audit retains 1,117 unresolved accessed report–source pairs
in the primary total. Because exported browser results sometimes omitted the
opened URL, cursor lineage, page identifiers, and titles were used to
deduplicate those pages within reports; this limitation should remain stated
where the access total is reported.
