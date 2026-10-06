# Tsc1 DEG-count prediction

## Question and resolved ambiguities

The held-out manifest for this run contains one requested perturbation, `Tsc1`. I interpreted the task as: predict the number of measured genes in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons that would have `pvals_adj < 0.05` after acute sparse AAV-CRISPR loss of `Tsc1`, using only non-held-out perturbations for calibration. The held-out `Tsc1` signature itself was absent from both supplied inputs, so I did not treat the manifest as evidence for its observed count.

I kept the readout narrow: `n_degs` is the number of single-gene Wilcoxon DE calls in recovered nuclei at BH FDR 0.05. It is a response-breadth endpoint, not a phospho-S6, cell-size, viability, or editing-efficiency measurement. I also treated `151 TH Prkcd Grin2c Glut` as the Allen thalamic glutamatergic class label, not as tyrosine hydroxylase expression.

## Sources used

- Input count table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input DE table: `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest: `[local file: 250_Tsc1.csv]`.
- Distributed Agents same-experiment corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`. This was used for curated claims/findings over the same Perturb-seq experiment. It is a semantic layer over the same experiment rather than external replication.
- Distributed Agents run-local observed-profile tool `profile_neighbors`, used on the supplied parquet to compare focal-cell Wilcoxon score vectors.
- External literature:
  - Huang and Manning 2008, DOI `10.1042/BJ20080281`, reviewed TSC1/TSC2 as a Rheb GAP complex and a negative regulator of mTORC1.
  - Dibble et al. 2012, DOI `10.1016/j.molcel.2012.06.009`, identified TBC1D7 as a stable third TSC-complex subunit and showed the TSC1-TSC2-TBC1D7 complex has Rheb-GAP activity.
  - Menon et al. 2014, DOI `10.1016/j.cell.2013.11.049`, showed that growth-factor signaling activates mTORC1 by spatially dissociating the TSC complex from lysosomal Rheb.
  - Dibble and Cantley 2015, DOI `10.1016/j.tcb.2015.06.002`, summarized the PI3K-AKT-TSC-Rheb branch and its integration with Rag/amino-acid signals at lysosomal mTORC1.
  - Shen et al. 2018, DOI `10.1038/nature26158`, defined the DEPDC5/NPRL2/NPRL3 GATOR1 complex as a RagA GAP upstream of amino-acid-dependent mTORC1 signaling.
  - Karalis et al. 2022, DOI `10.1038/s41467-022-31961-6`, showed that reducing Raptor, the mTORC1 subunit, rescues multiple neuronal phenotypes in mouse models of TSC.

## Computational calibration

The focal count table has 1,674 non-held-out biological targets. It is extremely zero-inflated: 1,205 targets have 0 DEGs; the median is 0; the 75th percentile is 1; the 95th percentile is 18; 63 targets fall in the 10-89 medium band and 43 have at least 100 DEGs. `Tsc2` has 86 DEGs in the focal cell group and ranks 45th of 1,674, so the observed loss of the TSC brake sits near the upper edge of the medium class.

I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and inspected pathway and expression-neighbor comparators. The key exact focal counts were:

| training target | focal `n_degs` | role in the Tsc1 prediction |
| --- | ---: | --- |
| `Tsc2` | 86 | direct TSC-complex analog; best mechanistic calibration |
| `Depdc5` | 13 | mTORC1 activator through GATOR1/Rag amino-acid branch; attenuated but partially overlapping sterol/endolysosomal state |
| `Mtor` | 2 | core kinase loss, opposite pathway direction from TSC loss and nearly flat |
| `Rptor` | 0 | mTORC1 scaffold loss, also opposite direction from TSC loss and flat |
| `Igf1r`, `Insr`, `Irs1`, `Pik3r1` | 0 each | receptor-proximal PI3K inputs are buffered at this basal nuclear-RNA endpoint |
| `Rab7` | 501 | strong endolysosomal/sterol downstream-state neighbor, not a same-pathway target |
| `Psmc1`, `Psmb4` | 430, 742 | proteostasis-stress neighbors of `Tsc2`, useful as downstream stress comparators |
| `Dctn1`, `Mib1`, `Marchf6`, `Selenoi`, `Srebf2`, `Htt` | 75, 27, 14, 5, 7, 3 | recurrent sterol or cholesterol-homeostasis comparators with node-specific magnitudes |
| `Fam120a`, `Pkd1` | 0 each | same-corpus counterexamples: linked to mTORC1/SREBP biology but no focal broad output |

For the DE-signature comparison I used Wilcoxon `scores` as signed profiles, kept positive and negative top-200 tails, and evaluated same-direction tail overlap and whole-profile Pearson/cosine. The focal `Tsc2` signature itself contained 58 up and 28 down FDR 0.05 genes. Its strongest FDR genes in this group included up-regulated sterol or growth-control genes such as `Cyp51`, `Pik3r3`, `Ldlr`, `Msmo1`, `Ddit4`, `Rragd`, and `Pik3r1`, plus down-regulated genes such as `Nrbp2`, `Amy1`, `Snhg11`, and `Rnpc3`.

The most informative pairwise observations were:

- `Tsc2` vs. `Depdc5`: cosine `0.290`; 39/200 positive-tail and 39/200 negative-tail features overlapped. At FDR 0.05, `Depdc5` had only 13 DEGs but shared 8 with `Tsc2` in the same direction: the up genes `Pik3r3`, `Tubb3`, `Pik3r1`, `Ldlr`, `Msmo1`, and the down genes `Amy1`, `Snhg11`, `Rnpc3`. This supports the same sterol/metabolic direction but shows that the amino-acid/Rag branch was much weaker than direct TSC loss.
- `Tsc2` vs. `Rab7`: cosine `0.304`; 46/200 positive-tail and 40/200 negative-tail overlaps; 25 of the 58 positive `Tsc2` DEGs were also positive `Rab7` DEGs. `Rab7` is a data-driven endolysosomal/cholesterol-state comparator rather than a TSC-complex proxy, and its 501-DEG footprint argues that the shared sterol/lysosome module can ride on very broad trafficking stress.
- `Tsc2` vs. `Mtor` and `Rptor`: `Mtor` had cosine `-0.204` with no shared significant genes; `Rptor` had cosine `-0.093` and no shared significant genes. These are useful counterexamples because losing a positive core mTORC1 component is not the same perturbation sign as removing the TSC brake.
- `Srebf2` had only 7 DEGs and reversed sterol genes (`Dhcr24`, `Insig1`, `Hmgcs1`, `Msmo1`, `Cyp51`, `Sqle`) relative to `Tsc2`/`Depdc5`, bounding the TSC response to a broader mTORC1-associated state with a sterol branch rather than to SREBF2 targets alone.

The Distributed Agents corpus agreed with this decomposition. Its `Tsc2` findings describe a caudal neuronal mTORC1/SREBP/lysosomal program, induction of sterol and lysosomal genes, and homeostatic induction of `Ddit4`, `Rragd`, `Pik3r1`, `Pik3r3`, and related regulators. Corpus claims also specifically warn that represented basal PI3K/AKT/mTOR relatives are often flat or mutually non-phenocopying in postnatal neurons, and that `Mtor`/`Rptor`/receptor-proximal nodes do not form a generic reciprocal PI3K-mTOR RNA state. A focal corpus claim linked `Rab7` and `Depdc5` through a sterol/endolysosomal state in `151 TH Prkcd Grin2c Glut`.

## Target-specific reasoning for Tsc1

`Tsc1` encodes hamartin, the obligate partner of TSC2/tuberin in the TSC complex. The biochemical prior is therefore unusually strong: unlike `Depdc5` or PI3K receptors, `Tsc1` and `Tsc2` act in the same Rheb-GAP complex that restrains mTORC1. The TSC1-TSC2-TBC1D7 complex is the direct Rheb inhibitor upstream of mTORC1, and disrupting either TSC1 or TSC2 should release Rheb and increase mTORC1 output. Neuronal TSC phenotypes in mouse models are mTORC1/Raptor-sensitive, so a postmitotic neuronal Tsc1 loss-of-function perturbation is expected to be biologically active rather than a generic buffered receptor-input case.

Within this dataset, the direct observed analog is `Tsc2`, not `Mtor`, `Rptor`, or the receptor-proximal PI3K genes. `Tsc2` produced 86 DEGs in the focal cell group, while `Mtor` produced 2, `Rptor` 0, `Igf1r` 0, `Insr` 0, `Irs1` 0, and `Pik3r1` 0. I therefore called a nonzero response for `Tsc1`; the zero call would require assuming that CRISPR disruption of the TSC1 half of the same complex is silent while TSC2 loss is one of the strongest focal responses in the training table.

I did not simply copy the full 86-count `Tsc2` endpoint. The `Tsc2` signature has downstream overlap with stress and trafficking perturbations (`Rab7`, `Psmc1`, `Psmb4`) that can inflate or reshape RNA breadth beyond pure mTORC1 activation. Conversely, `Depdc5` proves that a mechanistically real mTORC1-activating lesion can be much smaller in this focal endpoint, and several sterol comparators show only 3-27 DEGs. `Tsc1` is much closer to `Tsc2` than to those branches, but acute sparse guide performance, survivor sampling, and unequal dependence on the TSC1 scaffold versus the TSC2 GAP domain could easily move its observed FDR count tens of genes away from `Tsc2`.

I therefore predicted an upper-medium count, slightly below the direct `Tsc2` analog and well above the attenuated `Depdc5` branch:

| held-out target | prediction | rationale |
| --- | ---: | --- |
| `Tsc1` | 78 | Same TSC/Rheb/mTORC1 brake as `Tsc2`; expected strong nonzero sterol/lysosomal/homeostatic response in `151 TH Prkcd Grin2c Glut`, calibrated downward from `Tsc2`'s 86 to allow imperfect CRISPR effectiveness and a not-quite-identical TSC1/TSC2 perturbation |

## Limits

The prediction is a single point for a noisy endpoint. I do not know the recovered `Tsc1` guide-positive nucleus count, actual indel rate, or gRNA quality in the held-out experiment, and any of those could shift the BH FDR count sharply around a threshold. No same-experiment `Tbc1d7`, `Rheb`, `Nprl2`, or `Nprl3` focal perturbation was available to bridge `Tsc2` to other exact Rheb/Rag regulators. The external mouse Tsc1/Tsc2 literature mostly uses germline, conditional, or stronger cell-type-specific deletions and often measures phospho-protein, morphology, seizures, or survival rather than acute sparse postnatal snRNA-seq, so I used it only to choose the correct mechanistic analogs. Finally, the Distributed Agents corpus is valuable for interpreting the same experiment but is not an independent validation dataset.
