# DEG-count prediction trace

## Question and resolved ambiguities

The held-out perturbation manifest for this run contains one requested target,
`Pgk1`, and the requested endpoint is:

```text
number of measured genes with pvals_adj < 0.05 in 151 TH Prkcd Grin2c Glut
```

I treated `151 TH Prkcd Grin2c Glut` as the exact Allen-derived thalamic
glutamatergic neuronal class from the supplied PerturbAI whole-brain atlas
context; `TH` is the thalamic anatomical tag, not tyrosine hydroxylase. The
prediction is for the held-out acute P16 AAV-PHP.eB CRISPR-Cas9 loss-of-function
perturbation in recovered NeuN+ nuclei, not for germline or conditional Pgk1
loss, pharmacologic PGK1 inhibition or activation, red blood cells, glia, or a
flux assay.

I counted any gene whose adjusted Wilcoxon p-value was below `0.05`, including
the perturbed gene itself when it was a measured feature. That matches the
training CSV endpoint: for example, in the focal class `Hk1`, `Gpi1`, `Pfkm`,
and `Tpi1` each have `n_degs = 1`, and the single significant row is the
corresponding target transcript.

## Sources used

- Raw training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Raw differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Run manifest:
  `[local file: 176_Pgk1.csv]`.
- Run-local dataset portrait:
  `codex_runtime/pipeline/dataset_context.md`, perturbai-atlas-v5.
- Distributed Agents same-experiment semantic corpus,
  `perturbai-july-260713-sourceguard-1773-v1`; `Pgk1` itself had no Finding or
  Claim in this release, but represented glycolysis genes did.
- Distributed Agents profile runtime artifacts produced in this run:
  `pgk1_energy_profile_compare.json`, `pgk1_energy_profile_inspect.json`, and
  `pgk1_glycolysis_all_neighbors.json`.
- External literature:
  - Chiarelli et al. 2012, PLoS One, DOI `10.1371/journal.pone.0032065`,
    PMID `22348148`.
  - Fermo et al. 2012, Molecular Genetics and Metabolism, DOI
    `10.1016/j.ymgme.2012.05.015`, PMID `22705348`.
  - Gutierrez et al. 2022, Pediatric Hematology and Oncology, DOI
    `10.1080/08880018.2022.2072987`, PMID `35608390`.
  - Herrero-Mendez et al. 2009, Nature Cell Biology, DOI `10.1038/ncb1881`,
    PMID `19448625`.
  - Cai et al. 2019, Journal of Clinical Investigation, DOI
    `10.1172/JCI129987`, PMID `31524631`.

## Computational work over the supplied data

1. Loaded the requested-target CSV and confirmed it contains exactly one target:
   `Pgk1`.
2. Loaded the focal-class training counts and summarized the calibration
   distribution. The endpoint is very sparse: 1,205/1,674 training perturbations
   have zero DEGs, the median is 0, the 75th percentile is 1, and only 43
   perturbations have at least 100 DEGs.
3. Filtered the parquet with:

   ```python
   (group_name == "151 TH Prkcd Grin2c Glut") &
   gene_target.isin(selected_energy_genes)
   ```

   and counted rows with `pvals_adj < 0.05` for glycolysis, TCA, pyruvate
   dehydrogenase, and respiratory-chain targets represented in the training
   set.
4. Queried the same selected genes across all neuronal classes to test whether
   the weak focal behavior of the central-glycolysis genes was a local accident.
5. Used the Distributed Agents runtime `profile_compare` and `profile_inspect` tools to
   compute signed full-vector profile similarities among represented glycolysis
   and energy-metabolism perturbations in the focal class. The comparison used
   `gene_target` as the entity column, `names` as the measured-feature column,
   `logfoldchanges` as the signed value, and `pvals_adj < 0.05` as the
   significance definition.
6. Used `profile_neighbors` to compare `Eno1`, `Gpi1`, `Hk1`, `Pfkm`, and
   `Tpi1` against all 1,674 eligible training perturbations. That all-training
   scan retained a 310-target neighbor union from the five anchors, with no
   small recurrent high-DEG module centered on glycolysis.

The focal training counts for the biologically nearest represented enzymes were:

| training perturbation | focal `n_degs` | focal FDR<0.05 rows |
| --- | ---: | --- |
| `Eno1` | 0 | none; minimum adjusted p-value was 1.0 |
| `Gpi1` | 1 | only `Gpi1`, logFC -0.673, FDR 2.14e-7 |
| `Hk1` | 1 | only `Hk1`, logFC -0.768, FDR 9.86e-5 |
| `Pfkm` | 1 | only `Pfkm`, logFC -0.857, FDR 6.42e-14 |
| `Tpi1` | 1 | only `Tpi1`, logFC -1.010, FDR 6.23e-12 |
| `Pdha1` | 1 | only `Pdha1`, logFC -1.039, FDR 1.31e-6 |
| `Mdh2` | 1 | only `Mdh2`, logFC -0.840, FDR 7.37e-5 |
| `Sdha` | 1 | only `Sdha`, logFC -0.781, FDR 2.11e-12 |
| `Ndufs2` | 1 | only `Ndufs2`, logFC -0.728, FDR 8.26e-12 |
| `Uqcrc2` | 1 | only `Uqcrc2`, logFC -0.576, FDR 3.00e-3 |
| `Uqcrb` | 0 | none |
| `Uqcrfs1` | 0 | none |
| `Uqcrh` | 0 | none |
| `Uqcrq` | 1 | only `Gpr180`, logFC -0.466, FDR 0.0429 |
| `Aco2` | 0 | none |
| `Mdh1` | 29 | `Mdh1` self plus 28 additional genes |

The cross-class count reinforced that this was not just a `151`-specific null:
`Eno1` and `Uqcrh` had zero DEGs in every measured class; `Hk1`, `Aco2`,
`Uqcrb`, and `Uqcrq` had only one significant gene over all classes; `Pfkm`
had six total significant genes; and `Tpi1` had twelve. `Mdh1` was the main
metabolic counterexample, with a focal 29-DEG signature, but its cytosolic
malate/aspartate role is not the same as Pgk1's ATP-generating lower-glycolysis
reaction.

## Target-specific reasoning

### `Pgk1`

`Pgk1` encodes the ubiquitous X-linked phosphoglycerate kinase isoform that
catalyzes the reversible transfer from 1,3-bisphosphoglycerate to ADP, yielding
3-phosphoglycerate and ATP. Human PGK1 deficiency causes combinations of
hemolytic anemia, CNS dysfunction, and myopathy, and biochemical work on disease
variants shows that pathogenicity can come from large losses of catalytic
efficiency and/or thermal stability rather than from a mild uniform expression
decrement alone (Chiarelli et al. 2012, DOI `10.1371/journal.pone.0032065`;
Gutierrez et al. 2022, DOI `10.1080/08880018.2022.2072987`). PGK1 is the
non-testis isoform whereas PGK2 is testis-specific (Fermo et al. 2012, DOI
`10.1016/j.ymgme.2012.05.015`), so there is no obvious neuronal PGK2 paralog
whose training response could be transferred directly. PGK1 activity can matter
in neuronal stress models: terazosin activation of PGK1 raised ATP and was
protective in Parkinson's disease models (Cai et al. 2019, DOI
`10.1172/JCI129987`).

Those external facts argue that Pgk1 is a real bioenergetic node, but the
same-experiment analogs argue that this perturbation class usually remains
transcriptionally buffered. In the focal `151 TH Prkcd Grin2c Glut` class, four
nearby measured central-glycolysis perturbations, `Gpi1`, `Hk1`, `Pfkm`, and
`Tpi1`, each produced exactly one DEG, and in each case that DEG was only the
target transcript. `Eno1` produced zero DEGs, with no gene even below adjusted
`p < 0.2`. Adjacent pyruvate and mitochondrial energy targets were likewise
weak: `Pdha1`, `Mdh2`, `Sdha`, `Ndufs2`, and `Uqcrc2` were self-only; `Aco2`,
`Uqcrb`, `Uqcrfs1`, and `Uqcrh` were zero.

The Distributed Agents corpus, although lacking `Pgk1` itself, summarized the represented
glycolysis surface in the same direction. `Eno1:F001` reported no corrected
single-nucleus transcriptional response in any of the 23 recovered neuronal
groups. `Gpi1:F001` called the full Gpi1 response almost origin-centered with
only two downstream genes across 22 measured groups, and `Gpi1:E006` noted that
`Hk1`, `Pfkm`, `Tpi1`, and `Eno1` were also buffered. `Hk1:F001` found zero
downstream FDR<0.10 genes in every measured cell group. `Pfkm:F002` recorded
that represented glycolysis comparators were almost flat and that `Hk1`,
`Gpi1`, `Tpi1`, `Eno1`, and `Slc2a1` correlated only very weakly with `Pfkm`.
The released Claim `claim:455b18eeb9fd489426f1` condensed this to "Single
perturbations of represented central glycolysis genes are transcriptionally
buffered in postmitotic neurons."

The profile-comparison artifact agreed with the threshold counts. The five
focal glycolysis nodes had full 17,259-feature vectors available; `Eno1` had no
significant features, while `Gpi1`, `Hk1`, `Pfkm`, and `Tpi1` each had exactly
one negative significant feature. Their strongest apparent profile correlations
mostly arose from shared weak negative tails rather than from shared significant
DEGs: there were no positive significant intersections and no negative
significant intersections among the glycolysis pairs because each one-gene hit
was a different self transcript. This makes a medium or strong Pgk1 prediction
hard to justify.

The zero/nonzero decision is therefore close. I set `Pgk1` to a weak nonzero
count because Pgk1 is less redundant in neurons than `Eno1`, is directly
responsible for the first ATP-producing reaction of lower glycolysis, and the
most relevant self-measured glycolysis genes in the focal class were not
entirely null: they typically yielded one FDR-significant self row. I did not
raise the count above one because the same assay did not detect hypoxia,
glycolytic-compensation, UPR/ISR, or broad oxidative-phosphorylation programs
after nearby central-glycolysis perturbations, and neurons are known to keep
basal glycolysis constrained by APC/C-Cdh1-mediated degradation of Pfkfb3
(Herrero-Mendez et al. 2009, DOI `10.1038/ncb1881`).

Prediction: `Pgk1 -> 1` DEG.

## Limits

- `Pgk1` was completely held out, and the Distributed Agents same-experiment corpus had
  no target-specific `Pgk1` report. The prediction extrapolates from other
  glycolytic enzymes rather than from a direct Pgk1 profile.
- No neuronal `Pgk2` comparator was present; `Pgk2` is testis-specific, so a
  same-step paralog would have been a poor postmitotic-brain analog even if it
  had been assayed.
- The represented analogs flank, but do not duplicate, Pgk1's reaction. `Gpi1`,
  `Pfkm`, `Tpi1`, and `Eno1` are central-glycolysis steps; `Hk1` is the entry
  kinase; `Pdha1`, `Aco2`, `Mdh1/Mdh2`, and the respiratory-chain genes are
  broader energy-metabolism counterexamples.
- The single-DEG focal analogs were mostly self-transcript calls. Since
  self-target logFC is not a calibrated editing-efficiency measure in this
  dataset, those calls support a very small observed RNA response but do not
  prove stronger functional knockout for those guides.
- Human PGK1 disease and pharmacologic PGK1 activation demonstrate biological
  importance under severe or challenged settings, but the assay here samples
  sparse, recovered postnatal neuronal nuclei under basal conditions. A severe
  full knockout could select cells out of the recovered pool without leaving a
  broad survivor-state RNA signature.
- DEG count is discrete and heavily thresholded. The distinction between zero
  and one DEG depends on whether `Pgk1` itself is a measured, sufficiently
  depleted transcript in this class, so the point estimate should be read as a
  weak response centered at the endpoint's detection limit rather than as
  evidence for a multicellular stress state.
