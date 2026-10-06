# Hspa9 DEG-count prediction

## Question and endpoint

I interpreted the task as a truth-blind point prediction for the held-out
`Hspa9` perturbation in the focal `151 TH Prkcd Grin2c Glut` neuronal group.
The endpoint is the integer count of measured genes, including the target
transcript if it passes the same test, with BH-adjusted Wilcoxon `pvals_adj <
0.05` in perturbed versus matched control nuclei. The `Hspa9` perturbation is
absent from both supplied inputs, so its exact focal DEG count and expression
signature are not directly observed.

The focal endpoint is directly observed only for the 1,674 non-held-out
training targets in
`../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
The raw Parquet at
`training differential-expression dataset`
is the direct source for the corresponding expression patterns, with one
measured gene by cell type by perturbation row. The July PerturbAI corpus
release `perturbai-july-260713-sourceguard-1773-v1` was used only as the
same-experiment report layer over those Parquet measurements, not as
independent replication. External biology was checked in PubMed.

## Computational calibration

The requested-target file contained exactly one held-out target:

```text
Hspa9
```

I verified that the focal training file has 1,674 unique targets. Its response
breadth is highly sparse in `151 TH Prkcd Grin2c Glut`: 1,205 of 1,674 training
targets have `n_degs = 0`; only 469 have any FDR 0.05 hit; the median is 0, the
90th percentile is 2, the 95th percentile is 18, and the maximum is 2,677
(`Uba5`). Thus a held-out perturbation needs target-specific evidence to be
moved away from zero.

I ran the declared `dataset.perturbseq_features summarize` operation on the
full Parquet. It summarized all 616,253,184 declared rows and wrote
`evidence/features.parquet`, confirming cached target-level FDR-burden and
log-fold-change features for all 1,674 training perturbations. The nested
rank-calibration subcommand was attempted but correctly refused this run because
`task_bindings.json` contains no ranked or partially ranked supervised gene set.
For this count-prediction task, I therefore used the cached feature table as a
sanity check on all-cell DEG burden and joined the small focal training-count
CSV directly for the focal endpoint.

To inspect expression-pattern evidence without reconstructing a new Parquet
aggregate, I filtered the declared DE Parquet to the focal cell group, a small
set of mechanistic comparators, and `pvals_adj < 0.1`. The relevant training
counts and focal patterns were:

| training perturbation | focal `n_degs` | expression-pattern evidence in `151 TH Prkcd Grin2c Glut` |
| --- | ---: | --- |
| `Dnajc19` | 0 | no focal genes at FDR 0.10; in the same-experiment corpus, no downstream FDR 0.10 response in any recovered neuronal group |
| `Nfs1` | 0 | no focal genes at FDR 0.10; corpus reports no transcriptome-wide downstream DE in any of 23 recovered neuronal groups |
| `Lonp1` | 0 | no focal genes at FDR 0.10, although the all-cell feature summary had a few FDR 0.05 hits outside the focal class |
| `Clpx`, `Afg3l2`, `Yme1l1`, `Clpp` | 0 | no focal FDR 0.05 response; corpus reports these mitochondrial protease relatives do not phenocopy `Lonp1` or `Opa1` |
| `Tomm40` | 1 | exactly one focal FDR 0.05 hit, `Tomm40` itself, with logFC -0.923 and `pvals_adj = 5.46e-7`; no focal downstream gene reached FDR 0.10 |
| `Isca2` | 1 | exactly one focal FDR 0.05 hit, `Isca2` itself, with logFC -0.700 and `pvals_adj = 0.0273` |
| `Hspa5` | 5 | a small ER-stress response: `Erc1` down plus `Hsp90b1`, `Nfe2l1`, `Pdia4`, and `Derl3` up at FDR 0.05; additional ERAD/UPR genes just missed FDR 0.05 |
| `Hspa8` | 9 | a small cytosolic chaperone/heat-shock signature with `Dnaja1`, `Hspa4l`, `Syt4`, `Hsp90aa1`, and `Cct6a` up and several neuronal genes down |
| `Slc25a46` | 1 | one focal self-transcript hit only, despite SLC25A46 being an OPA1/MFN-associated mitochondrial-dynamics disease gene |
| `Opa1` | 37 | a clear positive mitochondrial-stress counterexample: `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Mthfd2`, `Slc7a5`, aminoacyl-tRNA synthetases, and `mt-Co2` shifted in the expected ATF4/ISR-like pattern |

## Target-specific Hspa9 rationale

`Hspa9` encodes mtHsp70/mortalin/GRP75, the central mitochondrial Hsp70
chaperone. It powers or assists TIM23/PAM matrix import and folding of
nuclear-encoded mitochondrial proteins, works with J-domain and GrpE-like
co-chaperones, and has additional roles at mitochondria-ER contact sites
(Havalova et al. 2021, DOI: 10.3390/ijms22158077; Szabadkai et al. 2006,
PMID: 17178908, DOI: 10.1083/jcb.200608073). Mortalin can also participate in
iron-sulfur biogenesis, as it interacts with frataxin and the NFS1/ISCU complex
in mammalian cells (Shan et al. 2007, PMID: 17331979, DOI:
10.1093/hmg/ddm038). Neuronal mortalin knockdown can fragment mitochondria and
damage axons in primary neurons (Ferre et al. 2021, PMID: 34489498, DOI:
10.1038/s41598-021-97162-1). Those priors make a true Hspa9 loss-of-function a
plausible same-direction cause of import stress, mitochondrial folding stress,
calcium-transfer defects, and ultimately ATF4/ISR-like transcription.

The same-experiment causal chain in this screen is:

`AAV CRISPR editing of Hspa9 -> partial mtHsp70 functional depletion -> impaired
TIM23/PAM import, matrix folding, Fe-S handling, and mitochondria-ER coupling ->
mitochondrial proteostasis or calcium stress -> survival through the 3-4 week
postnatal window -> snRNA-seq of recovered 151 TH Prkcd Grin2c Glut nuclei ->
Wilcoxon FDR DEG count`.

The key question is where that chain is likely to break before the FDR endpoint.
The direct molecular consequence of Hspa9 should be stronger and broader than
`Dnajc19`, because DNAJC19 is a specialized inner-membrane J protein whereas
mtHsp70 is the core ATPase. However, several more proximal training tests show
that mitochondrial import and Fe-S disruption were largely invisible in this
assay. `Dnajc19`, the closest represented PAM/import-motor perturbation, had 0
focal DEGs and no downstream FDR 0.10 response in any recovered neuronal group.
`Tomm40`, the outer-membrane import pore upstream of mtHsp70, had only its own
transcript significant in 151 and no downstream import-failure, ATF4,
proteasome, TOM-subunit, or mitochondrial chaperone/protease compensation
program in the corpus report. `Nfs1` and `Isca2`, which bracket the Fe-S axis
that Hspa9 can influence, were null or self-only in the focal group. Those are
not same-complex evidence for Hspa9, but they are strong endpoint evidence that
partial acute CRISPR of core mitochondrial maintenance genes often fails to
propagate to a broad survivor-nucleus RNA signature here.

`Opa1` is the major counterexample. It proves that the 151-cell Wilcoxon surface
can detect a mitochondrial stress state, especially `Asns`, `Ddit3`, `Chac1`,
aminoacyl-tRNA synthetases, amino-acid transport, and one-carbon genes. That
does not make `Opa1` a quantitative phenocopy of Hspa9, because OPA1 loss
directly changes inner-membrane fusion and cristae structure; the July reports
show that represented OPA1-processing or mitochondrial-dynamics relatives
(`Yme1l1`, `Afg3l2`, `Mff`, `Clpp`, `Slc25a46`) did not phenocopy it.
Franchino et al. 2024 (PMID: 37804316, DOI: 10.1093/brain/awad340) also places
the OMA1-DELE1-HRI ISR downstream of AFG3L2/OPA1-linked mitochondrial
proteotoxicity, which is a different proximal lesion from partial mtHsp70
depletion.

The chaperone comparators set the expected nonzero scale if Hspa9 does become
visible. `Hspa5` produced only 5 FDR 0.05 genes in the focal group and `Hspa8`
produced 9, despite BiP and cytosolic Hsc70 being central proteostasis genes.
Hspa9 is mitochondrial rather than ER or cytosolic, but these training entries
argue that perturbing a broadly required chaperone does not by itself imply a
large 151-cell DEG count after sparse P16 CRISPR.

I therefore predict a near-null but not impossible response: most downstream
stress genes should stay below FDR 0.05 in recovered 151 nuclei, with at most a
self-transcript or one stress marker crossing. I used a one-gene point
prediction, closer to `Tomm40`/`Isca2` than to `Opa1`, `Hspa5`, or `Hspa8`.

## Limits

`Hspa9` has no direct training signature, and the closest same-complex TIM23/PAM
partners such as `Timm44`, mammalian `Pam16`, `Grpel1`, and `Grpel2` were not
present as focal training perturbations. The `Dnajc19` and `Tomm40` comparisons
therefore test adjacent import machinery rather than the obligate mtHsp70
ATPase itself. A larger biallelic or protein-level Hspa9 loss might trigger
cell death or an ISR before sampling, and this survivor-conditioned snRNA-seq
endpoint would not count depleted edited neurons. Finally, DEG burden is
assay- and power-dependent: the prediction is for this exact FDR 0.05 Wilcoxon
count in `151 TH Prkcd Grin2c Glut`, not a prediction of mitochondrial
importance or neuronal viability.
