# Prediction trace for Hnrnpa1

## Question and resolved ambiguities

The task asks for a point prediction of `n_degs` for each held-out perturbation in
the requested manifest, in the focal `151 TH Prkcd Grin2c Glut` cell group.
Here `n_degs` means the number of measured genes with Wilcoxon
Benjamini-Hochberg-adjusted `pvals_adj < 0.05` in the held-out perturbation
versus matched non-targeting controls.

The requested manifest contains one held-out target:

- `Hnrnpa1`

I treated the held-out expression profile as genuinely absent. I did not use
`Hnrnpa1` as a `gene_target`, because it is absent from both the parquet and the
151 TH training-count CSV. Rows where `names == "Hnrnpa1"` under other
perturbations were used only as downstream readouts of those other training
perturbations.

## Sources used

- Primary data:
  - `[local file: training_de_all_cell_groups.parquet]`
  - `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  - `[local file: 106_Hnrnpa1.csv]`
- Distributed Agents same-experiment semantic corpus:
  - release `perturbai-july-260713-sourceguard-1773-v1`
  - especially curated reports and claims for `Hnrnpa2b1`, `Hnrnpc`, `Hnrnpdl`, `Hnrnpu`, and `Tardbp`
- Distributed Agents run-local profile comparison:
  - a 14-node focal-cell comparison artifact over measured hnRNP/RBP/splicing targets was written to `profiles/rbp_compare.json` and inspected through `profiles/rbp_inspect.json`
- PubMed literature for external HNRNPA1 biology:
  - Kim et al. 2013, *Nature*, DOI `10.1038/nature11922`, PMID `23455423`
  - Guo et al. 2018, *Cell*, DOI `10.1016/j.cell.2018.03.002`, PMID `29677512`
  - Beijer et al. 2021, *JCI Insight*, DOI `10.1172/jci.insight.148363`, PMID `34291734`
  - An and Grabowski 2007, *PLoS Biology*, DOI `10.1371/journal.pbio.0050036`, PMID `17298175`

## Computational steps over the input tables

1. I read the held-out manifest and confirmed that it contains exactly
   `Hnrnpa1`.

2. I read the 1,674-row 151 TH training-count table and calibrated the endpoint
   scale. The focal response distribution is heavily zero-inflated: 1,205
   perturbations are zero, 363 have 1-9 DEGs, 63 have 10-99 DEGs, and 43 have
   at least 100 DEGs. The median is 0; the 90th percentile is 2; the top
   responses, such as `Uba5` at 2,677 and `Tpr` at 1,768, are extreme outliers.

3. I selected biologically relevant training perturbations from the count table:
   hnRNP-family and closely related RBPs (`Hnrnpa2b1`, `Hnrnpc`, `Hnrnpdl`,
   `Hnrnph2`, `Hnrnpu`, `Syncrip`, `Tardbp`, `Ddx3x`) plus focal
   RNA-processing and spliceosome boundaries (`Rnpc3`, `U2af2`, `Cdc40`,
   `Tnpo3`, `Prpf6`, `Thoc1`, `Snrnp70`).

4. I queried the parquet only for `group_name == "151 TH Prkcd Grin2c Glut"`
   and those candidate `gene_target` values, then counted genes with
   `pvals_adj < 0.05` and inspected the top adjusted-significant genes. The
   non-obvious operation was the row-group-filtered parquet scan:

   ```python
   filt = (pc.field("group_name") == focal) & pc.field("gene_target").isin(targets)
   table = dataset.to_table(
       columns=["names", "logfoldchanges", "scores", "pvals_adj", "gene_target"],
       filter=filt,
   )
   ```

5. I made a second targeted parquet scan for RNA-processing marker rows
   (`Hnrnpa1`, `Hnrnpa2b1`, `Rbm25`, `Hnrnpu`, `Tcerg1`, `Drosha`, `Luc7l2`,
   `Rsrp1`, `Srsf2`, `Fus`, and `Hnrnpm`) across the same perturbations. This
   was used to distinguish true Hnrnpa2b1/Hnrnpa1 compensation from generic
   spliceosome collapse.

6. I used the Distributed Agents runtime profile tools to compute a matched 151 TH
   signature comparison across the candidate RBP set. I used the activity
   counts and FDR-significant overlaps for sanity checks, but I did not treat
   whole-vector top-tail similarity as decisive because several tails were
   dominated by nonsignificant extreme log-fold changes from very lowly
   expressed genes.

## Within-dataset analogs and boundaries

### Primary analog: `Hnrnpa2b1`

`Hnrnpa2b1` is the closest represented paralog/function analog for held-out
`Hnrnpa1`. In the focal class it had:

- `n_degs = 11`
- `Rbm25` up: log2FC `0.369`, FDR `1.13e-05`
- `Hnrnpa1` up: log2FC `1.080`, FDR `2.98e-05`
- `Parp6` up: log2FC `0.529`, FDR `8.79e-05`
- `Tcerg1` up: log2FC `0.369`, FDR `0.00212`
- `Hnrnpu` down: log2FC `-0.290`, FDR `0.00212`
- `Drosha` up: log2FC `0.395`, FDR `0.0294`

The internal Hnrnpa2b1 report in the Distributed Agents corpus calls `Hnrnpa1`
up-regulation one of the main RNP-family compensation markers after Hnrnpa2b1
loss. This is strong within-dataset evidence that the A1/A2B1 branch is sensed
in 151 TH cells, but also that it remains sparse at total-gene-abundance level:
Hnrnpa2b1 produced only 11 FDR<0.05 calls in the focal class, far below the
hundreds of DEGs triggered by core spliceosome or Hnrnpu-like perturbations.

The reciprocal `Hnrnpa1` perturbation was held out, so the direction of
Hnrnpa2b1 compensation after Hnrnpa1 loss is extrapolated rather than directly
observed.

### Weak or flat hnRNP/RBP boundaries

Several represented RNA-binding proteins were much quieter than the broad
RNA-processing hits:

- `Syncrip`: `0` DEGs in 151 TH.
- `Hnrnpdl`: `1` DEG in 151 TH; only `Hnrnpu` was significant, up with
  log2FC `0.227`, FDR `0.00609`.
- `Hnrnph2`: `4` DEGs in 151 TH, led by `Rsrp1` down, FDR `3.62e-09`.
- `Ddx3x`: `8` DEGs in 151 TH.

These targets show that being an abundant neuronal RBP is not sufficient to
guarantee a broad FDR footprint in this CRISPR/snRNA-seq design. The Distributed Agents
corpus makes the same point for `Hnrnpdl` and `Syncrip`: measurable hnRNP-like
perturbations ranged from nearly flat to very broad and did not form a single
family-level phenocopy group.

### Stronger but imperfect nuclear RBP boundaries

Three nuclear RBP perturbations produced clearly nonzero but mechanistically
different signatures:

- `Hnrnpc`: `122` DEGs. It decreased `Rbm25`, `Luc7l2`, `Srsf2`, and `Rsrp1`
  in 151 TH, but `Hnrnpa1` itself was flat. The corpus report identifies
  `Hnrnpc` as spliceosome-adjacent but explicitly non-interchangeable with
  measured hnRNP-family comparators.
- `Tardbp`: `210` DEGs. Its focal signature was led by `Ppp6c`, `Gabpa`,
  `Usp15`, `Fam135a`, `Brms1l`, and `Uggt2` induction, plus `Tardbp` and
  `Fus` down-regulation. `Hnrnpa1` was not significant.
- `Hnrnpu`: `733` DEGs. It was much broader, with `Dmtf1`, `Depdc5`,
  `Slc20a1`, proteostasis/ISR-like genes, and `Hnrnpu` self-RNA up-regulation;
  `Hnrnpa1` was actually down while `Hnrnpa2b1` was up.

These are useful as positive assay controls for RBP biology but poor numerical
analogs for Hnrnpa1. Same-experiment Distributed Agents claims explicitly separate the
Hnrnpu/Hnrnpc/Tardbp states from weak or sparse hnRNP-family surfaces.

### Core spliceosome and RNA-processing upper bounds

The broad RNA-processing perturbations were far larger:

- `Rnpc3`: `868` DEGs
- `U2af2`: `828`
- `Cdc40`: `624`
- `Tnpo3`: `618`
- `Prpf6`: `454`
- `Thoc1`: `303`
- `Snrnp70`: `213`

They share some local RBP markers, such as repeated `Rsrp1` down-regulation,
but they look like spliceosome/transport stress states, not an A1/A2B1 paralog
state. For example, `U2af2` and `Rnpc3` each had hundreds of 151 TH calls and
large `Rsrp1` decreases, whereas Hnrnpa2b1 had only 11 calls and no significant
`Rsrp1` change. I therefore treated these as upper-bound counterexamples:
they prove the assay can recover RNA-processing failure in this cell type, but
they should not be averaged into the Hnrnpa1 prediction.

## External biological interpretation

HNRNPA1 and HNRNPA2B1 are close heterogeneous nuclear RNP proteins with two RNA
recognition motifs and low-complexity/prion-like C-terminal regions. Mutations
in the prion-like domains of HNRNPA2B1 and HNRNPA1 cause multisystem
proteinopathy and ALS, and disease mutations can enhance fibrillization, stress
granule recruitment, and cytoplasmic inclusion formation (Kim et al. 2013,
DOI `10.1038/nature11922`, PMID `23455423`). Later HNRNPA1 patient variants
were shown to alter fibrillization, liquid-liquid phase separation, and stress
granule dynamics in variant-specific ways (Beijer et al. 2021, DOI
`10.1172/jci.insight.148363`, PMID `34291734`).

That literature argues for a real RNP/stress-granule-sensitive gene, but it is
not a direct template for a broad loss-of-function DEG count here: this screen
made acute mosaic indels in postmitotic juvenile mouse neurons, not dominant
aggregation-prone PrLD alleles in aging motor neurons or muscle. Guo et al.
2018 showed that karyopherin-beta2/Transportin-1 can bind PY-NLS-bearing
proteins including hnRNPA1/hnRNPA2 and prevent or reverse aberrant phase
transitions (DOI `10.1016/j.cell.2018.03.002`, PMID `29677512`), again pointing
to cytoplasmic phase behavior and nuclear-import chaperoning rather than a
simple steady-state mRNA abundance collapse. In neurons, hnRNP A1 can contribute
to activity-regulated alternative splicing at UAGG motifs (An and Grabowski
2007, DOI `10.1371/journal.pbio.0050036`, PMID `17298175`), an isoform-level
process only indirectly captured by the gene-level 10x Flex Wilcoxon readout.

## Target-specific prediction

`Hnrnpa1` should be nonzero because the exact closest represented paralog,
`Hnrnpa2b1`, produced a reproducible 151 TH response and made `Hnrnpa1` one of
its top induced RNP-family transcripts. Loss of Hnrnpa1 is therefore likely to
perturb the same compact A1/A2B1/RNP compensation axis rather than being a
complete transcriptional null like `Syncrip`.

I predict it should stay close to `Hnrnpa2b1` rather than to `Hnrnpc`,
`Tardbp`, `Hnrnpu`, or the spliceosome targets. The stronger targets either
affected core spliceosome machinery or produced broad secondary ISR,
proteostasis, ER/lysosomal, or nuclear-scaffold states that were absent from
the Hnrnpa2b1 focal signature. The disease literature also mostly concerns
toxic aggregation/phase-separation alleles, so it should not inflate an acute
loss-of-function prediction into the hundreds.

Final point prediction: `12` DEGs for `Hnrnpa1`.

## Limits and extrapolation

- The main limitation is that Hnrnpa1 itself is held out, so there is no direct
  reciprocal measurement of whether Hnrnpa1 loss induces `Hnrnpa2b1`.
- `Hnrnpa2b1` is the best analog but still not an obligate complex partner; A1
  and A2B1 can bind overlapping RNA motifs and both participate in RNP granules,
  yet they are distinct proteins with different targets.
- The focal endpoint counts whole-gene abundance changes, not alternative
  splicing, intron retention, mRNA localization, translation, stress-granule
  dynamics, or hnRNPA1 protein aggregation.
- The curated same-experiment corpus has no Hnrnpa1 report because the target
  was absent from the training perturbation set. All Hnrnpa1-specific inference
  therefore comes from downstream `Hnrnpa1` rows under other perturbations and
  from external HNRNPA1/HNRNPA2B1 biology.
- The integer `12` is an assay-scale point estimate, not a claim that exactly 12
  biological pathways are affected. A count a few genes above or below
  Hnrnpa2b1 would be equally consistent with the current evidence.
