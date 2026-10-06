# Question and endpoint

I interpreted the task as a point prediction for the held-out perturbation
`Prdm12` in `151 TH Prkcd Grin2c Glut` cells.  The predicted value is the
number of measured RNAs that would pass `pvals_adj < 0.05` after BH-corrected
Wilcoxon testing in the same Perturb-seq pipeline that produced the supplied
training data.  The target itself was completely held out, so I treated the
training DEG-count CSV and the non-held-out differential-expression parquet as
direct observations only for analog perturbations, not as measurements of the
`Prdm12` perturbation.

The requested manifest contains one target:

```tsv
target_name
Prdm12
```

# Sources

* Direct local endpoint data: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`,
  with 1,674 non-held-out perturbations and their observed focal-cell
  `n_degs`.
* Direct local DE data:
  `training_de_all_cell_groups.parquet`, queried only for non-held-out analogs
  with columns `gene_target`, `group_name`, `names`, `logfoldchanges`,
  `scores`, `pvals_adj`, `n_pert_matched`, and `n_ctrl_matched`.
* Dataset and measurement context: the run-local PerturbAI atlas portrait and
  measurement registry.  I used the parquet as same-experiment data, not as raw
  UMI counts or guide-exposure denominators.
* Same-experiment interpretation: the packaged
  `perturbai-july-260713-sourceguard-1773-v1` Findings/Evidence corpus, used
  for PRDM-family and developmental-transcription-factor summaries over the
  visible non-held-out perturbations.
* External biology: PubMed searches for PRDM12/nociceptor function.  I used
  Chen et al. 2015, DOI `10.1038/ng.3308`; Bartesaghi et al. 2019, DOI
  `10.1016/j.celrep.2019.02.098`; Desiderio et al. 2019, DOI
  `10.1016/j.celrep.2019.02.097`; Landy et al. 2021, DOI
  `10.1016/j.celrep.2021.108913`; Latragna et al. 2021, DOI
  `10.1097/j.pain.0000000000002536`; Kokotovic et al. 2021, DOI
  `10.3389/fnmol.2021.720973`; and Vermeiren et al. 2023, DOI
  `10.1016/j.isci.2023.108364`.

# Dataset calibration

The training count distribution in the focal class is sparse:

* `n = 1674` visible biological perturbations.
* Mean `n_degs = 14.05`, but median `0`.
* 1,205/1,674 perturbations had `n_degs = 0`; 469 had at least one DEG.
* 75th percentile `1`, 90th percentile `2`, 95th percentile `18`.
* The upper tail was broad and driven by core RNA-processing/proteostasis or
  chromatin perturbations such as `Uba5` with 2,677 DEGs, `Tpr` with 1,768,
  `Sin3a` with 1,433, `Rnpc3` with 868, and `Zbtb7a` with 841.

That distribution makes zero the calibrated prior for a held-out developmental
transcription factor unless the target has a close analog with a robust
postnatal neuronal signature.  I therefore queried PRDM-family genes,
nociceptor-lineage genes downstream or upstream of PRDM12, and other
developmental TFs whose decisive phenotypes occur before the P16 perturbation
window.

The raw count query over the parquet was:

```sql
SELECT gene_target, group_name,
       SUM(CASE WHEN pvals_adj < 0.05 THEN 1 ELSE 0 END) AS n_fdr05,
       SUM(CASE WHEN pvals_adj < 0.10 THEN 1 ELSE 0 END) AS n_fdr10
FROM parquet_scan('training_de_all_cell_groups.parquet')
WHERE gene_target IN (...)
GROUP BY 1, 2;
```

# Target-specific reasoning

## Prdm12

PRDM12 is a PR-domain zinc-finger transcriptional regulator with a strong,
specific requirement in embryonic somatosensory/nociceptor specification.
Human biallelic `PRDM12` mutations cause congenital insensitivity to pain, and
loss of mouse `Prdm12` compromises nociceptor lineage generation and maturation
by regulating a NEUROG1/2-TRKA/NTRK1, NEUROD1, BRN3A/POU4F1, and ISL1
developmental cascade and by repressing PHOX2A/B visceral-neuron determinants
in somatosensory ganglia (Chen et al. 2015; Bartesaghi et al. 2019; Desiderio
et al. 2019; Vermeiren et al. 2023).  Adult conditional studies in dorsal-root
ganglion nociceptors show that PRDM12 can still remodel ion-channel and
receptor expression after development, but those studies are in peripheral
nociceptors rather than thalamic glutamatergic neurons (Landy et al. 2021;
Latragna et al. 2021; Kokotovic et al. 2021).

The matching experimental chain for this dataset therefore argues against a
large signal:

* Intervention: acute, mosaic AAV-CRISPR loss after P16 rather than embryonic or
  neural-crest deletion.
* Direct molecular consequence: reduced PRDM12 function in successfully edited
  NeuN+ nuclei.
* Propagation: PRDM12's best-established cascade is in sensory ganglia and
  nascent nociceptors; the focal class is thalamic `Prkcd/Grin2c`
  glutamatergic neurons.
* Sampling: the screen excluded the olfactory bulb and hindbrain and was
  NeuN-enriched; it did not assay peripheral DRG nociceptors, spinal cord
  dorsal horn, retina, or embryonic progenitor populations.
* Endpoint: only a recovered-nucleus snRNA gene-abundance response at P37-P44
  is scored; loss of a developmental lineage would not be recapitulated as
  within-cell DE in already specified thalamic neurons.

The most useful same-screen analogs support the same conclusion.

**PRDM-family analogs.**  `Prdm10` is the only represented PRDM-family target
with a clear focal signature.  It had 52 focal FDR<0.05 genes, 51 of them
downstream rather than the `Prdm10` transcript itself.  The significant genes
were mostly a compact down-regulated neuronal module, led by `Madd`, `Cadm3`,
`Ptov1`, `Uchl1`, `Kcnt1`, `Rnasek`, `Stmn2`, `Myt1`, `Psip1`, `Shisa7`,
`Selenow`, `Fus`, `Them6`, `Hap1`, `Ackr1`, `Ttll7`, `Plxna3`, and `Celsr3`;
the same-experiment corpus summarizes this as a real but restricted posterior
neuronal response.  That is a counterexample to the idea that every
developmental PRDM is silent, but the corpus also tested obvious PRDM-family
comparators and found the `Prdm10` module did not transfer: `Prdm16` and
`Prdm5` had no downstream FDR<0.10 genes across 23 groups, and `Prdm2` had one
non-overlapping Pvalb gene across the screened brain.  At the task's stricter
focal endpoint, `Prdm2 = 0`, `Prdm5 = 0`, and `Prdm16 = 0` FDR<0.05 genes.  I
therefore did not use `Prdm10 = 52` as a positive same-family estimate for
`Prdm12`; it is a sequence- and context-specific positive outlier among the
represented PRDM perturbations.

**PRDM12/nociceptor pathway analogs.**  Visible members of the PRDM12 sensory
program were transcriptionally buffered in the focal class: `Isl1 = 0`,
`Neurod1 = 0`, `Neurod2 = 0`, `Ntrk1 = 0`, `Pou4f3 = 0`, and `Trpv1 = 0`
FDR<0.05 genes.  These are not obligate complex partners of PRDM12 in thalamic
neurons, but they are the closest represented pieces of the external
nociceptor cascade.  Their flat surfaces argue that the dataset does not
contain an active postnatal thalamic version of the peripheral nociceptor
program.

**Other developmental TF counterexamples.**  The same logic held for other
developmental factors with dramatic embryonic phenotypes.  `Ptf1a`, `Atoh1`,
`Tcf3`, `Tcf12`, `Tcf4`, `Pax6`, `Lmx1b`, `Vsx2`, `Gfi1`, `Ebf2`, `Tgfbr1`,
and `Nkx2-1` each had 0 focal FDR<0.05 genes.  The corpus reports no FDR<0.10
downstream genes for `Ptf1a` across all 23 recovered neuronal groups despite
its canonical bHLH role in embryonic inhibitory-neuron fate (Jin and Xiang
2019, PMID `30470852`).  For `Nkx2-1`, the same-experiment report specifically
checked hypothalamic markers including `Pomc`, `Isl1`, `Prdm12`, and `Tbx3` and
found them unchanged in broad hypothalamic groups.  Those observations are not
measurements of `Prdm12` loss, but they show that transcription factors whose
biology is decisive before cell specification often collapse to a zero or
one-gene mature-neuron response in this assay.

Together, the direct count analogs point to the zero class rather than to a
low-positive value.  The only positive within-family comparator, `Prdm10`, has
a local focal program that visibly separates from `Prdm2`, `Prdm5`, and
`Prdm16`; the PRDM12 external mechanism is in sensory/nociceptive neurons and
embryonic lineage choice; and the visible nociceptor/developmental neighbors
are zero in the requested thalamic class.  I therefore predict no genes will
pass BH FDR 0.05 for held-out `Prdm12`.

# Limits

This is a direct DEG-count endpoint for `Prdm12`, but the `Prdm12` perturbation
itself is absent from both supplied inputs, so the prediction is extrapolative.
The screen did not measure indel rates, PRDM12 protein, chromatin binding, DRG
nociceptors, embryonic neural crest, spinal cord, or retinal and hindbrain
contexts, any of which could show strong PRDM12 biology.  A true small effect
of one or two focal DEGs would be hard to distinguish a priori from the many
zero and one-gene developmental-TF surfaces.  Conversely, a PRDM10-like
posterior neuronal signature cannot be ruled out from PRDM-domain membership
alone, but the measured divergence of represented PRDM-family genes makes that
less likely than a null focal result.
