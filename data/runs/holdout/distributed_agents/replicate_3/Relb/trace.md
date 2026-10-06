# Relb prediction trace

## Question and target

I treated the requested readout as a point prediction for the number of genes with `pvals_adj < 0.05` after each held-out CRISPR loss-of-function perturbation in `151 TH Prkcd Grin2c Glut` neurons. `n_degs = 0` means no measured transcript is expected to pass the Wilcoxon Benjamini-Hochberg cutoff in this cell group.

The run manifest `[local file: 197_Relb.csv]` contained one held-out target:

```text
Relb
```

I resolved the main ambiguity by predicting the FDR-thresholded DEG count in this exact focal cell group, not pan-neuronal activity, effect size, or Relb target-RNA depletion. The held-out gene was absent from both the DE parquet and the focal-cell count CSV, so every numerical comparison below uses non-held-out perturbations.

## Sources used

- `training_de_all_cell_groups.parquet`: per-gene differential-expression statistics. I filtered it to `group_name == "151 TH Prkcd Grin2c Glut"` and to mechanistic NF-kappaB/TNFR/TLR comparators.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed focal-cell `n_degs` for training perturbations.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`: I queried `target_context`, `candidate_set_topology`, and related-target views. The corpus had no `Relb` entry, but it did contain same-experiment annotations for represented NF-kappaB/TNFR comparators.
- Distributed Agents runtime profile comparison: I compared focal-cell log-fold-change vectors for `Rel`, `Nfkb1`, `Chuk`, `Traf3`, `Tnfrsf1a`, `Tnfrsf11a`, and `Cd40`.
- NCBI PubMed literature searches for external biology. Mechanistic facts used here are supported by Sun 2012, DOI `10.1111/j.1600-065X.2011.01088.x`, PMID `22435551`; Fusco et al. 2016, DOI `10.1126/scisignal.aad9413`, PMID `27678221`; Engelmann et al. 2020, DOI `10.1002/dvdy.170`, PMID `32145043`; and Le Voyer et al. 2024, DOI `10.1073/pnas.2321794121`, PMID `39231201`.

## Computation over the supplied DE tables

I first verified that `Relb` is not in the focal training-count table and then checked the count-table values for represented NF-kappaB/TNFR/TLR genes. For expression-pattern evidence, I filtered the Arrow parquet rather than reading all 616,253,184 rows:

```python
filt = (
    ds.field("group_name") == "151 TH Prkcd Grin2c_Glut".replace("_", " ")
) & ds.field("gene_target").isin(selected_targets)
```

The actual selected set was:

```text
Rel, Nfkb1, Chuk, Traf3, Map3k7, Cd40,
Tnfrsf1a, Tnfrsf11a, Tnfrsf13c,
Tlr2, Tlr3, Tlr4, Tlr5, Tlr7, Tlr8
```

For each selected perturbation, I recomputed the number of focal-cell rows with `pvals_adj < 0.05` from the parquet and cross-checked it against the training-count CSV. Every selected comparator had 17,259 measured genes in this cell type and `n_sig = 0`, matching the count CSV:

| training target | pathway role relative to RelB | perturbed nuclei | minimum focal FDR | focal `n_degs` |
|---|---|---:|---:|---:|
| `Rel` | Rel-family NF-kappaB transcription factor | 205 | 0.140 | 0 |
| `Nfkb1` | p105/p50 NF-kappaB subunit | 181 | 1.000 | 0 |
| `Chuk` | IKKalpha, central noncanonical p100-processing kinase | 156 | 0.727 | 0 |
| `Traf3` | TNFR adaptor and noncanonical NF-kappaB brake | 211 | 1.000 | 0 |
| `Map3k7` | TAK1, canonical TNFR/TLR-to-IKK/JNK/p38 kinase | 160 | 1.000 | 0 |
| `Cd40` | TNFRSF receptor that can activate NIK/NFKB2/RelB | 226 | 1.000 | 0 |
| `Tnfrsf1a` | TNFR1, canonical TNF-to-NF-kappaB receptor | 173 | 1.000 | 0 |
| `Tnfrsf11a` | RANK, noncanonical NF-kappaB-capable TNFRSF receptor | 159 | 1.000 | 0 |
| `Tnfrsf13c` | BAFFR, noncanonical NF-kappaB-capable TNFRSF receptor | 219 | 0.816 | 0 |
| `Tlr2` | innate receptor upstream of NF-kappaB | 167 | 1.000 | 0 |
| `Tlr3` | innate receptor upstream of NF-kappaB/IRF signaling | 132 | 1.000 | 0 |
| `Tlr4` | innate receptor upstream of NF-kappaB/IRF signaling | 113 | 1.000 | 0 |
| `Tlr5` | innate receptor upstream of NF-kappaB | 130 | 1.000 | 0 |
| `Tlr7` | innate receptor upstream of NF-kappaB/IRF signaling | 89 | 1.000 | 0 |
| `Tlr8` | innate receptor upstream of NF-kappaB/IRF signaling | 89 | 1.000 | 0 |

I then used `profile_compare` on the focal log-fold-change vectors for the most direct represented comparators: `Rel`, `Nfkb1`, `Chuk`, `Traf3`, `Tnfrsf1a`, `Tnfrsf11a`, and `Cd40`. This confirmed that each had `response_activity_status = no_significant_features`. Pairwise whole-profile correlations were descriptive, not strong evidence for a specific shared program, because no node had significant coordinates. Still, the absence of any FDR-significant features across the seven profiles ruled out the possibility that the count table had hidden an obvious RelB-like focal response in these immediate relatives.

The Distributed Agents corpus gave the same interpretation for the represented pathway:

- `Rel:F001` reported no robust downstream transcriptional response for acute `Rel` loss in any of the 23 measured neuronal groups.
- `Nfkb1:F002` reported that represented canonical NF-kappaB/TNF/TLR comparators phenocopied the flat `Nfkb1` state.
- `Chuk:F003` reported that `Nfkb1`, `Rel`, `Traf3`, and `Tnfrsf1a` were likewise null on the `Chuk`-matched neuronal surface.
- `Traf3:F004` reported that measured TNFR/TLR/NF-kappaB relatives did not phenocopy a positive `Traf3` program; `Cd40`, `Chuk`, `Map3k7`, `Nfkb1`, `Rel`, `Tlr2`, `Tlr4`, and `Tnfrsf1a` each had zero downstream FDR < 0.10 genes in their matched neuronal surfaces.
- Corpus claim `claim:778b2c45f226febe4372` summarized the same-experiment pattern as transcriptional silence of the represented CD40/TNFR/TLR/IL-1 to TAK1/IKK/NF-kappaB/JNK/p38 module in unchallenged postnatal NeuN-positive neurons.

## Target-specific reasoning

### Relb

RelB is the transactivation subunit most closely associated with the noncanonical NF-kappaB pathway. In stimulated immune and stromal cells, TNFR-superfamily receptors stabilize NIK, Chuk/IKKalpha phosphorylates NFKB2 p100, p100 is processed to p52, and p52:RelB enters the nucleus to regulate target genes; p100 can also sequester RelB in inactive complexes. That pathway architecture is reviewed by Sun 2012 and experimentally dissected in the RelB/p100/NIK/IKKalpha complex by Fusco et al. 2016. Human RELB loss-of-function disrupts alternative NF-kappaB outputs in immune cells, while preserving canonical TNF/IL-1beta responses in fibroblasts, supporting RELB as a noncanonical rather than pan-canonical NF-kappaB node (Le Voyer et al. 2024).

The most relevant training perturbation was `Chuk` because IKKalpha is the kinase directly upstream of p100 processing in noncanonical NF-kappaB. It had `n_degs = 0` in `151 TH Prkcd Grin2c Glut`; 17,259 genes were tested and the smallest adjusted p-value was 0.727. The corpus also reports Chuk as a broad basal-neuron null and specifically notes that canonical NF-kappaB feedback/inflammatory/survival transcripts were absent from the `Chuk` surface. If RelB/p52 signaling were tonically active in these thalamic glutamatergic neurons, partial loss of this direct upstream kinase would be an expected place to see at least a weak shared signature.

The second tier was the nuclear Rel-family comparison. `Rel` is not RelB, but it is the closest assayed Rel-family transactivating NF-kappaB subunit; it had `n_degs = 0` in the focal group, with only one row even reaching `pvals_adj = 0.140`. `Nfkb1`, encoding p50/p105, also had `n_degs = 0`. Corpus `Rel:F002` and `Nfkb1:F002` explicitly compared `Rel`, `Nfkb1`, `Chuk`, and `Traf3` and interpreted their shared behavior as absence of a basal NF-kappaB module rather than a missed single gene effect.

The receptor/adaptor side gave no counterexample. `Traf3`, which controls basal NIK turnover in noncanonical NF-kappaB, had `n_degs = 0`; `Cd40`, `Tnfrsf11a/RANK`, and `Tnfrsf13c/BAFFR`, all TNFR-family receptors capable of engaging noncanonical NF-kappaB in appropriate immune or stromal contexts, also had `n_degs = 0`. Canonical inflammatory inputs were similarly flat: `Tnfrsf1a`, `Map3k7`, and TLRs `Tlr2`, `Tlr3`, `Tlr4`, `Tlr5`, `Tlr7`, and `Tlr8` all had zero focal-cell DEGs. This is important because RelB expression has been detected in mouse brain domains by Engelmann et al. 2020, so the prediction is not that Relb is never neuronal; it is that the unstimulated, sparse, postnatal NeuN-positive CRISPR endpoint lacks a tonic RelB-dependent transcriptional program large enough to cross the Wilcoxon FDR threshold.

I therefore predicted no significant focal-cell response:

```text
Relb: predicted_n_degs = 0
```

This call is driven mainly by same-experiment evidence from the flat `Chuk`, `Rel`, `Nfkb1`, `Traf3`, `Cd40`, TNFR, and TLR perturbations. External biology was used to justify why those flat perturbations are appropriate analogs: they lie immediately upstream, downstream, or parallel to RelB in the NF-kappaB network.

## Limits

`Relb` itself, `Nfkb2`, `Rela`, `Ikbkb`, `Ikbkg`, `Map3k14/NIK`, `Traf2`, `Traf6`, and `Birc2/Birc3` were missing as perturbation targets, so no training signature directly removes the p52:RelB dimer or the full NIK destruction complex. The CRISPR experiment also assayed basal nuclei 3 to 4 weeks after P16 AAV delivery, without CD40L, BAFF, RANKL, LTbetaR, TNF, IL-1, TLR ligand, injury, or seizure-like stimulation. RelB biology is often ligand-gated or strongest in thymic, stromal, B-cell, dendritic, microglial, and epithelial systems; many of those lineages were absent from the NeuN-enriched data. Finally, `n_degs` is thresholded and power-dependent: the zero prediction means I do not expect any transcript to clear FDR 0.05 in this cell group, not that RelB protein is irrelevant in every neuronal setting.
