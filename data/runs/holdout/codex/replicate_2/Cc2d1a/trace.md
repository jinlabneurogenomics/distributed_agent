# Cc2d1a direct DEG-count forecast

## Target

`Cc2d1a` in `151 TH Prkcd Grin2c Glut`.

Endpoint: number of genes in the declared thalamic-glutamatergic training DE universe with Wilcoxon BH-adjusted `p < 0.05`.

## Evidence Used

- **Declared target biology bundle**:
  `[local file: Cc2d1a.json]`,
  SHA256 `480006823de285fb59405ad01974645f268432a9d33b83680a74a60116129efb`.
- **Exact focal-population reach** from that bundle:
  `Cc2d1a` was measured in non-target nuclei for `151 TH Prkcd Grin2c Glut`,
  with mean CP10K `0.494`, mean raw UMI `0.786`, and expression in
  `12152 / 23679` cells, i.e. `51.32%`.
- **Functional-stock adjudication** from that bundle:
  CRISPR loss is expected to stop new CC2D1A production while existing dynamic
  scaffold protein persists until turnover; adult CA1 AAV-Cre data showed
  protein loss and a neuronal phenotype by three weeks. The bundle adjudicates
  stock at P37-P44 as `likely_substantially_depleted`, with partial evidence
  completeness because no thalamic turnover or half-life is known.
- **Mechanism facts** from that bundle:
  CC2D1A is a dynamic ESCRT/endosomal scaffold/regulator that directly binds
  CHMP4B and restrains CHMP4B polymerization. Cc2d1a-only loss has postnatal
  forebrain and adult hippocampal phenotypes despite the related `Cc2d1b`
  paralog, but those phenotypes are outside the assayed thalamic population.
- **Declared `151 TH Prkcd Grin2c Glut` count table**:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  It contained 1,674 visible training perturbations; 1,205 had `n_degs = 0`,
  276 had `n_degs = 1`, and the quartiles were 0, 0, and 1
  with a 90th percentile of 2.
- **Closed profile check on the declared Parquet**:
  `workbench/cc2d1a_candidate_profile_compare.json` and
  `workbench/cc2d1a_candidate_profile_inspect.json`, computed only in
  `151 TH Prkcd Grin2c Glut`, confirmed that the close and pathway-adjacent
  training perturbations split into mostly null or tiny signatures.

## Training Counts Considered

The direct ESCRT/endosomal and signaling comparators available in the training
table were:

```tsv
target	n_degs	role_in_this_forecast
Chmp4b	0	direct ESCRT-III binding partner; closest measured proximal comparator
Notch1	0	endosomal cargo / signaling context
Notch2	0	endosomal cargo / signaling context
Notch4	0	endosomal cargo / signaling context
Nfkb1	0	signaling context
Braf	4	MAPK-signaling context
Mtor	2	mTOR-signaling context
Rptor	0	canonical mTORC1 component
Akt3	0	PI3K-Akt-mTOR upstream context
Mapk1	0	MAPK context
Mapk9	0	MAPK context
Ep300	0	transcriptional co-regulator context
Crebbp	8	transcriptional co-regulator context
Ube3a	0	neuronal disease/synaptic comparator
Vps13a	0	endolysosomal context
Vps13b	0	endolysosomal context
Vps13c	0	endolysosomal context
Vps35	17	retromer/endosomal upper-bound comparator
Vps35l	0	related retromer/Commander branch
Vps41	0	late-endosomal/HOPS context
Vps53	0	endosomal-recycling context
Vps54	31	endosomal-recycling upper-bound comparator
Rab7	501	core late-endosomal upper-bound comparator
Tsc2	86	mTORC1-activation upper-bound comparator
Snx10	0	endolysosomal context
```

The two local count sets had medians of zero:

- endolysosomal set:
  `Chmp4b`, `Vps13a`, `Vps13b`, `Vps13c`, `Vps35`, `Vps35l`,
  `Vps41`, `Vps53`, `Vps54`, `Rab7`, `Snx10` had 3/11 nonzero
  entries and median `0`;
- signaling-context set:
  `Notch1`, `Notch2`, `Notch4`, `Nfkb1`, `Braf`, `Mtor`, `Rptor`,
  `Tsc2`, `Akt3`, `Mapk1`, `Mapk9`, `Ep300`, `Crebbp`, `Ube3a`
  had 4/14 nonzero entries and median `0`.

The same-experiment corpus, used only for these visible training
perturbations, reinforces that the large `Rab7` and `Tsc2` counts are not
generic outputs of every nearby perturbation. `Rab7` anchors a strong
late-endosomal/lysosomal and sterol compensation state; `Vps35` gives a much
smaller, branch-specific thalamic retromer response; and `Mtor` shows that
canonical PI3K/Akt/mTOR members can be flat or mutually non-phenocopying in
the basal postnatal neuronal RNA endpoint.

## Forecast Reasoning

`Cc2d1a` has enough in-assay expression and enough protein-turnover support
that I would not treat it as an unreachable target. The main downward evidence
is endpoint specificity: the documented Cc2d1a phenotypes are morphology,
plasticity, and behavior in forebrain or hippocampus, while the forecasted
endpoint is a survivor-conditioned nuclear RNA response in thalamic
glutamatergic neurons 21-28 days after sparse editing.

The nearest visible perturbations argue for a tiny RNA footprint rather than
a Rab7-like stress state. The direct CHMP4B perturbation is `0` in this cell
class; Notch and NF-kB nodes are flat; Braf, Mtor, and Crebbp are only `2-8`;
and most represented VPS/endosomal perturbations are also `0`. Rab7, Vps35,
Vps54, and Tsc2 show that the assay can report endolysosomal or mTOR-linked
stress when a stronger core node is hit, but those losses are less direct
analogues for removing CC2D1A, which is a regulatory scaffold rather than the
core late-endosomal GTPase, retromer core, or TSC brake.

I therefore place Cc2d1a just above the zero-heavy local median to allow for
target reach, functional stock depletion, and a possible self or very weak
downstream call, but below the multi-gene responses of Vps35/Vps54/Tsc2/Rab7.

Point forecast: **1** DEG.
