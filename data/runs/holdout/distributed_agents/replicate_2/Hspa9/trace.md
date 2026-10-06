# Reasoning trace

## Question interpreted

The requested endpoint is the exact focal-cell `n_degs` count that would have
been reported for each held-out CRISPR target if that target had been present in
the differential-expression parquet: the number of measured genes with
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in
`151 TH Prkcd Grin2c Glut` nuclei.

This run requests one completely held-out target:

| target | prediction |
| --- | --- |
| `Hspa9` | number of FDR<0.05 genes after acute sparse CRISPR loss in the focal thalamic glutamatergic group |

I treated the endpoint as inclusive of the perturbed target transcript itself,
because the training count table does the same: for example `Tomm40` has
`n_degs=1` in the focal class and the one significant row is `Tomm40` itself.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`: authoritative observed focal `n_degs` for all training perturbations.
- `[local file: training_de_all_cell_groups.parquet]`: focal differential-expression rows for mechanistic analogs and counterexamples.
- `[local file: 109_Hspa9.csv]`: requested target list; it contains only `Hspa9`.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`: same-experiment interpreted reports and claim graph for training perturbations. `Hspa9` itself is absent from the corpus, as expected for this held-out target.
- PubMed literature for HSPA9/mortalin biology:
  - van der Laan, Hutu and Rehling, 2010, DOI `10.1016/j.bbamcr.2010.01.013`, review of the TIM23 presequence translocase and the mtHsp70-containing PAM motor.
  - Iosefson, Sharon, Goloubinoff and Azem, 2011, DOI `10.1007/s12192-011-0285-3`, showing human mortalin/HSPA9 with Tid1 can refold mitochondrial aggregates and summarizing mortalin as both a mitochondrial import-motor component and matrix chaperone.
  - Amick et al., 2014, DOI `10.1002/pro.2466`, structural and functional context for mortalin as a mitochondrial Hsp70 involved in import, quality control and Fe-S/homeostasis pathways.
  - Ferre et al., 2021, DOI `10.1038/s41598-021-97162-1`, showing that HSPA9/mortalin down-regulation in primary neurons perturbs mitochondrial morphology and promotes axonal damage.
  - Jain, Paz and Azem, 2024, DOI `10.3390/genes15121534`, a TIM23 disease review placing mitochondrial Hsp70 and its J-domain regulators in the presequence translocase-associated motor.

## Computation over the training data

I first read the focal training-count CSV. It contains 1,674 training
perturbations; 469 are nonzero, the median is 0, the 75th percentile is 1, the
95th percentile is 18, and the maximum is 2,677. Thus counts of 0 or 1 are not
meaningless edge cases in this cell group; they cover most observed targets.

I then queried the parquet for
`group_name = '151 TH Prkcd Grin2c Glut'` and a curated set of training
perturbations in four classes:

- mitochondrial import or TIM/PAM-adjacent: `Dnajc19`, `Tomm40`, `Agk`;
- mitochondrial matrix or inner-membrane proteostasis: `Clpp`, `Clpx`,
  `Lonp1`, `Yme1l1`, `Afg3l2`;
- chaperone/proteostasis paralog or pathway counterexamples: `Hspa8`, `Hspa5`,
  `Hsp90ab1`, `Hsf1`;
- a positive mitochondrial-stress counterexample: `Opa1`.

For each, I counted rows with `pvals_adj < 0.05`, extracted the best adjusted
P value, and checked canonical mitochondrial ISR/UPR and chaperone markers
(`Atf4`, `Atf5`, `Ddit3`, `Herpud1`, `Asns`, `Chac1`, `Mthfd2`, `Mthfd1l`,
`Shmt2`, `Slc7a1`, `Slc7a5`, `Hspd1`, `Hspe1`, `Hspa9`, `Clpp`, `Lonp1`,
`Hspa5`, `Hsp90b1`, `Xbp1`). I also computed pairwise Pearson correlations of
the full focal Wilcoxon-score vectors among these nominated training targets.

Key focal counts and rows were:

| training target | focal `n_degs` | focal signature evidence |
| --- | ---: | --- |
| `Dnajc19` | 0 | all rows FDR=1.0; best marker panel rows including `Ddit3`, `Herpud1`, `Hspd1`, `Hspe1`, `Clpp`, `Lonp1`, and `Hspa9` were FDR=1.0 |
| `Tomm40` | 1 | the only FDR<0.05 row was `Tomm40` itself, logFC -0.923, FDR 5.46e-07; all downstream import/ISR/chaperone markers checked were FDR=1.0 |
| `Agk` | 0 | all focal rows FDR=1.0; a TIM22/lipid import-adjacent comparator rather than a PAM component |
| `Clpp` | 0 | best FDR 0.723; matrix Clp protease loss did not induce mitochondrial chaperone, ISR, or HSPA9-neighborhood genes |
| `Clpx` | 0 | best FDR 0.540; same ClpXP branch as `Clpp` but also silent |
| `Lonp1` | 0 | self row FDR 0.507 and all checked ISR/UPRmt genes FDR=1.0 in this focal group |
| `Yme1l1` | 0 | all rows FDR=1.0 |
| `Afg3l2` | 0 | best FDR 0.912 |
| `Hsp90ab1` | 1 | the only FDR<0.05 row was `Hsp90ab1` itself |
| `Hspa5` | 5 | a small ER-quality-control response, led by `Erc1`, `Hsp90b1`, `Nfe2l1`, `Pdia4`, `Derl3` |
| `Hspa8` | 9 | a small cytosolic Hsp70 response, led by `Dnaja1`, `Hspa4l`, `Syt4`, `Hsp90aa1` |
| `Hsf1` | 6 | repression of heat-shock targets such as `Hsph1`, `Hsp90aa1`, `Hsp90ab1`, `Ahsa2` |
| `Opa1` | 37 | induced a detectable mitochondrial ISR-like program including `Asns`, `Chac1`, `Ddit3`, `Mthfd2`, `Slc7a1`, `Slc7a5` |

The selected score-vector similarities in the focal cell group were modest even
among positive controls: `Hspa5`-`Hspa8` was the largest at r=0.279,
`Hspa5`-`Opa1` was r=0.243, `Hspa8`-`Opa1` was r=0.177, and
`Lonp1`-`Opa1` was r=0.148. Null mitochondrial genes did not form a coherent
high-correlation state; the comparison is therefore informative mainly because
the FDR-level markers that would define a broad mitochondrial stress response
were absent.

## Target-specific reasoning for `Hspa9`

### External function prior

`Hspa9` encodes mortalin/GRP75/mitochondrial Hsp70. It is mechanistically
closer to the TIM23/PAM mitochondrial import motor than to the cytosolic Hsp70
or ER BiP systems: mtHsp70 supplies the ATP-driven pulling/folding activity for
matrix import through TIM23, and it is regulated by J-domain and GrpE-like
cofactors. Mortalin also participates in matrix protein folding/disaggregation
with Tid1/DNAJ partners and in broader mitochondrial homeostasis. Neuronal
knockdown experiments outside this atlas show that lower HSPA9 can fragment
mitochondria and injure axons, so `Hspa9` is not a biologically inert target.

### Most relevant within-dataset analogs

`Dnajc19` is the closest represented PAM/J-domain neighbor. It has 0 focal DEGs,
FDR=1.0 for all checked ISR/UPRmt/chaperone markers, and the same-experiment
Distributed Agents report concludes that it was globally transcriptionally buffered:
22 recovered neuronal groups had no downstream gene at FDR<0.10. This is the
strongest direct argument that partial acute disruption of an import-motor
cofactor can fail to trigger a nuclear RNA stress program in surviving neurons.

`Tomm40`, the outer-membrane import pore, is a stringent import counterexample.
It had one focal DEG, and that DEG was the `Tomm40` self-transcript; no
downstream ATF/CHOP, mitochondrial chaperone, protease, or TOM/TIM compensation
gene passed correction. The Distributed Agents report similarly interpreted `Tomm40` as
a pan-neuronal downstream-null perturbation whose self-depletion did not become
an import-stress transcriptome.

`Agk`, `Clpp`, `Clpx`, `Lonp1`, `Yme1l1`, and `Afg3l2` bound the broader
mitochondrial-proteostasis expectation. Their focal counts were all 0, and the
ClpXP/AAA/matrix protease branch did not induce `Ddit3`, `Herpud1`, `Hspd1`,
`Hspe1`, `Clpp`, `Lonp1`, or `Hspa9` in this cell group. The Distributed Agents corpus
also records that represented mitochondrial protease perturbations are
branch-specific rather than interchangeable: `Lonp1` can make a small ISR-like
state in other cell classes, while `Clpp`, `Clpx`, `Afg3l2`, and `Yme1l1` do
not share that state broadly.

`Opa1`, `Hspa5`, `Hspa8`, and `Hsf1` are counterexamples, not direct analogs.
They show that the focal assay can detect stress transcription when it occurs:
`Opa1` induced 37 genes with `Asns`/`Ddit3`/`Chac1`/one-carbon features,
`Hspa5` induced a 5-gene ER-quality-control signature, `Hspa8` induced a
9-gene cytosolic Hsp70/co-chaperone signature, and `Hsf1` repressed 6
heat-shock targets. None is a same-complex mitochondrial Hsp70 perturbation,
so they raised the prediction above a hard zero only slightly.

### Count decision

I predict that `Hspa9` will be detectable, if at all, as a one-gene event rather
than as a broad mitochondrial ISR/UPRmt state in `151 TH Prkcd Grin2c Glut`.
The decisive within-dataset evidence is that `Dnajc19`, `Tomm40`, and the
mitochondrial protease comparators are 0 to 1 in the focal training counts and
lack the `Ddit3`/`Asns`/`Hspd1`/`Hspe1`/`Clpp`/`Lonp1` programs that full matrix
stress would have produced. I still made the prediction nonzero because HSPA9
is the central mtHsp70 rather than a distal cofactor, is abundantly expressed,
and the endpoint counts the target transcript itself; `Tomm40` demonstrates
that a core mitochondrial import gene can register exactly one significant
gene in this focal group via self-depletion while remaining downstream-flat.

Final point prediction for `Hspa9`: **1 DEG**.

## Limits and extrapolation

- No direct `Hspa9` perturbation signature or DEG count was present in the
  supplied training files or the same-experiment corpus.
- The closest biochemical partners of HSPA9, including `Timm44`, `Grpel1`,
  `Grpel2`, `Hspd1`, and `Hspe1`, were not available as focal training
  perturbations, so the comparison leans on the adjacent PAM gene `Dnajc19`,
  the import pore `Tomm40`, and matrix protease/chaperone counterexamples.
- The prediction is assay-conditioned. DNA indels, HSPA9 protein loss,
  mitochondrial import flux, axonal mitochondrial morphology, respiration, ROS,
  and edited-cell survival were not directly measured.
- Severe biallelic `Hspa9` loss could kill or deplete cells before snRNA-seq,
  leaving recovered nuclei buffered; conversely, a stronger perturbation in a
  culture or bulk tissue setting could produce much larger mitochondrial stress
  than this sparse P16-to-P37/44 neuronal readout.
- The one-gene nonzero call depends partly on whether the `Hspa9` mRNA itself
  would pass FDR in recovered nuclei. The atlas shows target-transcript drops
  are not a reliable editing proxy, so this is the weakest part of the estimate.
