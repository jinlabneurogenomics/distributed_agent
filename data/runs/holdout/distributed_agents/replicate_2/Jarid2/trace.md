# Jarid2 DEG-count prediction

## Question and resolved ambiguities

The task asks for a point prediction of the number of measured genes that would pass
Benjamini-Hochberg FDR 0.05 after acute mosaic `Jarid2` CRISPR loss of function in
`151 TH Prkcd Grin2c Glut` neurons. The requested manifest
`115_Jarid2.csv` contains a single held-out target, `Jarid2`, and `Jarid2` is absent
from both supplied training inputs.

I treated `n_degs` as the same assay-specific endpoint as the training CSV: a focal
cell-group count of rows in the differential-expression parquet with
`pvals_adj < 0.05`. I did not use target-transcript knockdown as an editing-efficiency
filter, because in this experiment weak target RNA loss can coexist with functional
indel formation.

## Sources

- Input differential-expression table:
  `[local file: training_de_all_cell_groups.parquet]`
- Input training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Requested-target manifest:
  `[local file: 115_Jarid2.csv]`
- Run-local PerturbAI atlas context and scalar calibration in
  `codex_runtime/pipeline/`.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`.
- PubMed-indexed primary literature and reviews for JARID2/PRC2 biology.

## Dataset computations

I first summarized the 1,674 training perturbations in the focal class. The response
is heavily zero-inflated: 1,205/1,674 targets have `0` DEGs; 363 have 1-9; 63 have
10-99; and only 43 have at least 100.

I then checked whether exact PRC2/JARID2 comparators were present in the focal
training table. `Eed`, `Ezh1`, `Ezh2`, `Suz12`, `Aebp2`, `Mtf2`, `Phf1`, `Phf19`,
`Rbbp4`, and `Rbbp7` were all absent, so there is no direct same-complex count to
transfer.

Because the closest complex members were unavailable, I assembled a chromatin
control set from PRC2-adjacent H3K27/H3K36/H3K4 regulators, repressive chromatin
factors, and active BAF/NuRD perturbations described in the same-experiment corpus.
I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and these
20 targets, recomputed `pvals_adj < 0.05` counts, and compared their focal
log-fold-change profiles with the run-local `profile_compare` and `profile_cohort`
tools using the full observed expression vectors and top-200 signed tails.

Observed focal counts for the most relevant analogs and counterexamples were:

| group | training target | focal n_degs | focal DE pattern used for calibration |
| --- | --- | ---: | --- |
| Polycomb-linked / H3K27-adjacent | `Yy1` | 720 | Strong posterior chromatin/transcriptional response; corpus notes mixed Polycomb/chromatin rewiring with `Pcgf2` down and `Ring1` up, so it shows Polycomb-linked genes can be detected but is much broader than a PRC2.2 cofactor. |
| H3K27 antagonist | `Kdm6b` | 0 | Same focal cells stayed flat after loss of an H3K27 demethylase. This is an important zero counterexample, although losing the eraser is not the same as losing the PRC2 recruiter. |
| H3K36 / PRC2-antagonist axis | `Nsd1` | 23; `Ash1l` 1; `Kmt2c` 0 | Nearby chromatin-mark regulators ranged from sparse to null; the corpus specifically reports that H3K36/PRC2-axis relatives are not interchangeable in this postmitotic assay. |
| H3K4 / bivalent-chromatin axis | `Setd1a` | 368 | Strong but mostly down-regulated mitochondrial, GPI-anchor, cilia, and organelle-maintenance state; useful as a positive chromatin detectability control, not a PRC2 phenocopy. |
| H3K4 / MLL axis | `Kmt2a` | 24; `Kdm5c` 18; `Kdm5b` 0 | Sparse, target-specific responses on a bivalent-mark-adjacent axis. `Kmt2a` down-regulated neuronal identity/connectivity genes, whereas `Kdm5b` was fully FDR-flat. |
| H3K9 repression | `Setdb1` | 22 | Weak-medium repressive-chromatin signal marked by `Tasor`, `Atf7ip`, and protocadherin changes; a count-scale analog for chromatin silencing, not a mechanistic PRC2 substitute. |
| NuRD | `Chd4` | 100 | Detectable but target-specific mixed thalamic signature; the corpus reports that NuRD/MBD-adjacent perturbations do not collapse into one generic repressive-chromatin signature. |
| BAF / mSWI-SNF | `Smarcc2` | 185; `Arid1a` 22; `Smarce1` 11; `Smarca4` 0; `Smarcc1` 0 | The same focal class reports a BAF module, but even same-family subunits range from 0 to 185 DEGs. This brackets the uncertainty for chromatin cofactors. |
| REST/DNMT repression | `Rest` | 0; `Dnmt3a` 0 | Additional methylation/repressor counterexamples in the exact same focal class. |

The exact profile comparison also argued against pooling all chromatin counts.
Across the 20-node cohort there were 190 pairwise comparisons. Positive
top-tail overlap was weak, with a mean overlap coefficient of 0.069, while
significant-gene overlap among active pairs was usually small and often
opposite in sign. The curated Distributed Agents corpus made the same point from
precomputed same-experiment findings: represented BAF, NuRD, H3K4, H3K36,
H3K27-antagonist, DNA-methylation, and repressive-chromatin perturbations were
detectable in this screen but target-selective.

## Jarid2-specific biological reasoning

`Jarid2` encodes a catalytically inactive JmjC/ARID protein and regulatory subunit
of Polycomb repressive complex 2. In embryonic stem cells, JARID2 colocalizes with
EZH2/SUZ12, promotes PRC2 recruitment at developmental targets, and tunes H3K27
methylation and Polycomb occupancy rather than acting as a histone demethylase
itself (Peng et al. 2009, DOI 10.1016/j.cell.2009.12.002, PMID 20064375; Shen et
al. 2009, DOI 10.1016/j.cell.2009.12.003, PMID 20064376; Pasini et al. 2010, DOI
10.1038/nature08788, PMID 20075857; Li et al. 2010, DOI 10.1101/gad.1886410,
PMID 20123894). Landeira et al. showed that Jarid2-deficient ES cells have impaired
neural and mesodermal differentiation with altered PRC1/PRC2 and paused Pol II
recruitment at bivalent developmental genes (2010, DOI 10.1038/ncb2065, PMID
20473294).

Those data make `Jarid2` a real chromatin-regulatory target rather than a random
zero-class gene. They do not, however, imply a large acute signature in P16-P37
postmitotic neurons. The strongest JARID2 evidence is in embryonic pluripotent or
progenitor transitions, where PRC2 must establish new repression. Petracovici and
Bonasio found that during ESC-to-neural-progenitor differentiation, PRC2.2/JARID2
and PRC2.1/MTF2 control distinct Polycomb target sets, with JARID2 most important
for newly repressed genes rather than all pre-existing H3K27me3 domains (2021,
DOI 10.1016/j.molcel.2021.03.038, PMID 33887196). In nondividing neurons, many
H3K27me3 domains should already be established and need not dilute through S phase
over this 3-4 week assay.

There is still some postmitotic precedent for JARID2/PRC2 having a neuronal RNA
maintenance role: Yen et al. found that Dlk1-Dio3 lncRNAs, including `Meg3`, help
the `Ezh2`-`Jarid2` interaction preserve postmitotic motor-neuron fate and Hox
patterning through H3K27me3 (2018, DOI 10.7554/eLife.38080, PMID 30311912). Human
genetics also supports dosage sensitivity: Verberne et al. established JARID2
haploinsufficiency as a neurodevelopmental syndrome (2020, DOI
10.1038/s41436-020-00992-z, PMID 33077894). These are reasons not to set the
focal count to zero, but neither source specifically tests acute incomplete
`Jarid2` loss in juvenile thalamic glutamatergic neurons.

## Final target prediction

For `Jarid2`, the closest available counts point below the 10-30 DEG band seen for
`Setdb1`, `Kmt2a`, `Nsd1`, `Arid1a`, and `Kdm5c`: the most direct H3K27-axis
counterexample, `Kdm6b`, was 0; the H3K36/PRC2-antagonist comparators were 0-23;
and `Dnmt3a`, `Rest`, `Smarca4`, and `Smarcc1` show that several nuclear regulators
can be completely silent despite adequate matched-cell counts. I therefore predict
a weak but nonzero response, comparable to the low end of chromatin/NDD weak
responders such as `Smarce1`, `Setd5`, `Crebbp`, `Phf21a`, `Brd1`, and `Ehmt1`,
rather than a medium BAF/NuRD/SETD1A-scale footprint.

Predicted `Jarid2` `n_degs`: **6**.

## Limits

- The decisive limitation is missing exact PRC2 coverage: `Eed`, `Ezh2`, `Suz12`,
  `Aebp2`, `Mtf2`, `Phf1`, `Phf19`, `Rbbp4`, and `Rbbp7` were not in the focal
  training table, and `Jarid2` itself had no same-experiment Distributed Agents report.
- PRC2 accessory loss is not directionally equivalent to H3K27 demethylase,
  H3K36-writer, H3K4-writer, SETDB1, BAF, NuRD, DNMT3A, or REST loss. I used those
  perturbations to bracket count scale and assay detectability, not as biochemical
  phenocopies.
- Most external JARID2 data are from ESCs, progenitors, differentiating systems,
  or human developmental genetics. The requested experiment perturbs sparse,
  already postmitotic juvenile mouse neurons and reads out survivor-conditioned
  nuclear RNA, so the prediction is an extrapolation from developmental Polycomb
  biology into a maintenance setting.
- The integer 6 should be read as a point estimate for a noisy FDR threshold, not
  as a claim that exactly six direct JARID2 target genes are regulated.
