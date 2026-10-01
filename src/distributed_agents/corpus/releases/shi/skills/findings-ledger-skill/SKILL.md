---
name: findings-ledger-skill
description: Retrieve over the Shi narrative-findings ledger. Use to filter and read interpreted per-perturbation findings by finding type, gene, cell type, or prose, then resolve measurements, caveats, and citations for material candidates.
---

## findings-ledger-skill

Use this skill to retrieve over the dataset's own **interpreted findings** without
a graph. The ledger is the flat table of atomic findings, so anything that is a *property of a
finding* (its `finding_type`, `literature_status`, cell types, prose) or a
*count by one entity* (findings per gene / per type) is answered here directly,
by filtering columns and reading prose, with no traversal.

This is an evidence-access skill, not the reasoning agent. Its job is to get you
from candidate-scoped Findings to compact, grounded evidence. Full reports are
available for the few unresolved cases where integrated prose can change a
disposition; they are not the default ranking input.

## The ledgers (findings, reports, evidence, references)

**1. The findings ledger** (atomic unit: one finding):
`artifacts/ledgers/findings.csv` — 11,343 packaged findings. Each row includes:

| field | meaning |
|---|---|
| `doc_id` | `<gene>:<finding_id>` |
| `finding_id` | e.g. `F006` |
| `gene_target` | perturbed gene (the atomic analysis unit) |
| `summary`, `why_it_matters` | self-contained finding prose |
| `source.finding_type` | one of the 12 types below |
| `source.cell_types` | list of cell types the finding pertains to (may be empty = global/unspecified scope) |
| `source.direction`, `source.confidence` | qualitative direction; confidence label |
| `source.genes`, `source.comparators` | downstream/comparator genes (free-text symbols) |
| `source.evidence_ids`, `source.ref_ids` | keys into the full report's Evidence / References blocks |
| `source.literature_status` | extends / agrees / refines / contradicts / … |
| `source.main_caveats`, `source.source_summary`, `source.source_why_it_matters` | hedged judgment fields |

`finding_type` vocabulary (counts): `negative_result`, `cross_perturbation_contrast`,
`cell_type_selectivity`, `buffered_response`, `pathway_uncoupling`,
`therapeutic_direction_warning`, `disease_mechanism_refinement`, `convergent_module`,
`biomarker_candidate`, `homeostatic_compensation`, `other`, `literature_direction_mismatch`.

**2. The full per-perturbation reports** (richer; forensic/on-demand):
`artifacts/reports/reports.jsonl`
— 2,046 reports, keyed by `gene_target`, field `final_report`. The report prose
carries a structured appendix (Biological Findings, **Evidence JSONL with the
actual DE statistics**, **References JSONL with citations**, Literature
Comparisons, Pathways, Cell Type Specificity). This is where a weak/null finding
is explained and where grounding citations live. Open these only after compact
Finding review identifies a material conflict, uncertainty, or citation
need.

**3. The evidence & reference ledgers** (first-class artifacts, packaged in
`artifacts/ledgers/`): the report Structured Appendix, extracted into queryable tables
that share the findings' exact ID space, so a finding's `evidence_ids` / `ref_ids`
resolve directly without re-parsing report prose.
- `evidence.csv` — one row per `evidence_id` (E0xx): `evidence_slug`,
  `cell_type`, `genes`, `statistics` (the actual DE numbers), `description`.
- `references.csv` — one row per `ref_id` (R0xx): `source`, `source_type`
  (`pubmed`/`pmc`/`review`/`preprint`/`database`/…), `citation`, **`url`**,
  `description`. These are the citations the original per-perturbation analysis
  pulled — verifiable, with a URL.
- `findings.csv` — canonical packaged findings table with pipe-delimited
  `evidence_ids`/`ref_ids` per `finding_id`.
- `ledger_calibration.json` — Finding counts, crosstabs, Claim-layer semantics,
  and query assertions.
- `value_dictionary.csv` — query-facing field/value definitions and aliases.

The calibration artifacts are independently schema-validated. Do not recreate
their semantics from this skill prose. Use the bounded lookup interface:

```bash
# Field/value contract lookup.
python scripts/query_corpus.py describe literature_status
python scripts/query_corpus.py describe literature_status

# Corpus calibration summaries and exact crosstabs.
python scripts/query_corpus.py calibrate summary
python scripts/query_corpus.py calibrate claim-layer

# Canonical compact counts without raw matching rows.
python scripts/query_corpus.py count \
  --artifact findings --field literature_status --canonical contradiction

# Bounded Finding inventory with exact totals.
python scripts/query_corpus.py inventory --artifact findings --gene Psmb4 --limit 10
```

Every operation emits exact totals plus structured truncation metadata when a
row or byte ceiling is reached. Retain returned Finding IDs for a bounded
second slice instead of dumping or grepping a whole ledger.
IDs are GENE-SCOPED (E001 for one gene ≠ E001 for another).

**Citation grounding (use this, do not confabulate):** when a claim needs a
reference or its supporting DE numbers, resolve them from these ledgers rather
than recalling an identifier from memory. If you need a reference the corpus does
not carry, use the orchestrator's selected direct external skill or web
discovery before asserting a PMID/DOI, or mark it explicitly as an unverified
prior. Never emit a confabulated identifier.

## Access points (stdlib, no pixi env, run directly)

`scripts/query_findings.py` — filter/grep/count over the ledger:

```bash
# finding_type vocabulary with counts
python scripts/query_findings.py --count finding_type

# candidate-scoped warnings matching a declared semantic question
python scripts/query_findings.py --finding-type therapeutic_direction_warning \
    --grep "buffered|uncoupled|contradiction"

# findings tied to a cell type (matches cell_types field OR the prose)
python scripts/query_findings.py --cell-type "151 TH Prkcd Grin2c Glut" --limit 20

# findings for a candidate set, chosen fields (or --fields all)
python scripts/query_findings.py --gene Atp6v1e1 --gene Taf1 \
    --fields gene_target,finding_id,finding_type,source_summary,main_caveats

# how many DISTINCT targets carry a finding type (honest support, not edge count)
python scripts/query_findings.py --finding-type negative_result --count gene_target
```

`scripts/read_reports.py` — forensic full-report access for a bounded material
candidate set:

```bash
python scripts/read_reports.py Atp6v1e1 Taf1 Ndufs8 Pdhb --max-reports 4
# only sentences relevant to the unresolved question:
python scripts/read_reports.py Atp6v1e1 Taf1 Ndufs8 \
    --grep "buffered|uncoupled|contradiction" --max-reports 3
```

`scripts/resolve_evidence.py` — resolve a finding's `evidence_ids` / `ref_ids` to
the structured Evidence (DE stats/genes) and Reference (citation + source_type +
URL) rows, straight from the packaged ledgers (no report re-parsing). Use this to
ground citations in the corpus instead of recalling them:

```bash
# everything behind a gene
python scripts/resolve_evidence.py --gene Arx
# resolve exactly what a finding cites (verifiable references + the DE evidence)
python scripts/resolve_evidence.py --gene Arx --finding F002
# just references / just a specific id / machine-readable
python scripts/resolve_evidence.py --gene Arx --refs-only
python scripts/resolve_evidence.py --gene Arx --ref-id R004 --json
```

Use the scripts above instead of grepping or dumping the raw report JSONL. The
ledger is small (~18 MB), while the reports file is ~60 MB and contains
candidate-irrelevant references. Candidate-scoped access keeps evidence review
auditable and respects any active source policy. Override paths with
`--ledger-path` / `--reports-path` or `DISTRIBUTED_AGENTS_FINDINGS_LEDGER` /
`BIOKG_REPORTS_PATH`.

## Workflow: compact evidence first, reports on demand

1. **Classify the endpoint.** In-schema (a property the ledger records — a
   `finding_type`, a literature_status, a cell type) vs out-of-schema
   (depletion, survival, accessibility, abundance — *not* a field here).
2. **Respect the orchestrator's evidence role.** For an in-schema Findings task,
   filter broadly by the relevant `finding_type`(s) and/or prose. For an
   out-of-schema predicted task, do not create a second corpus-wide candidate
   pool: interpret only the quantitative starting set and additional
   Finding-related genes supplied by the orchestrator.
3. **Narrow within that scope.** Keep `buffered_response` / `negative_result` /
   `therapeutic_direction_warning` in candidate-scoped review—the signal for an
   orthogonal endpoint can hide in quiet/null findings. Do not scope
   interpretation to one cell type when a reached candidate has a relevant
   global warning.
4. **Read only the material candidates' reports** with `read_reports.py`.
   Candidate cards may use structured Findings and Evidence first; open the full
   report when integrated prose or a cited caveat can change the disposition.
5. **Return compact interpretation, not a parallel rank.** One fresh global
   reviewer compares the complete starting-plus-related candidate set using the
   quantitative evidence and these interpretations.
6. **Corroborate, don't rank-by, the numbers.** The DE parquet / FDR burden is
   corroboration of engagement, never the ranking key for an out-of-schema axis.

## Interpretation rules

- Structured Findings focus interpretation; neither row frequency nor DEG
  burden is a substitute for the requested endpoint.
- A `buffered_response` / `negative_result` / `absent` finding — or no finding in
  a queried cell type — is uncertainty or a relational pointer, never automatic
  evidence against the candidate. Open the report only if resolving that
  uncertainty can change a material disposition.
- Cite findings by `gene_target`, `finding_id`, `finding_type`, cell types,
  `evidence_ids`, `ref_ids`; cite report-derived claims by their Evidence
  statistics and References. Keep an explicit candidate ledger for ranked tasks.
