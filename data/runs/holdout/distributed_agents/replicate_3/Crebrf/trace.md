# Prediction trace

## Question and resolved ambiguities

The requested output is a point prediction for `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` nuclei after each requested CRISPR loss-of-function perturbation. The requested manifest contains one held-out target:

- `Crebrf`

The endpoint counts all measured genes that cross FDR 0.05 in the focal cell group. It does not exclude the perturbed target's own transcript, so I treated a self-only hit in the training data as one counted DEG when using analog counts. I did not use target-transcript downregulation as an editing-efficiency score because the dataset documentation states that measured self-RNA change is poorly correlated with the functional and downstream response.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`: exact focal-cell `n_degs` values for the 1,674 non-held-out training perturbations.
- `[local file: training_de_all_cell_groups.parquet]`: focal-cell signed log2 fold changes and adjusted p-values for analog perturbations.
- Distributed Agents same-experiment semantic corpus, release `perturbai-july-260713-sourceguard-1773-v1`: curated same-screen findings and claims for `Creb1`, `Atf6`, `Hspa5`, `Manf`, `Sec63`, and neighboring ER-stress perturbations.
- Distributed Agents runtime profile comparison over the focal-cell parquet rows: a direct comparison of the selected CREB/UPR analog signatures in `151 TH Prkcd Grin2c Glut`.
- PubMed literature retrieved through NCBI E-utilities:
  - DenBoer et al. 2005, DOI `10.1016/j.bbrc.2005.03.141`, PMID `15845366`: Luman/CREB3 can bind the unfolded-protein response element and induce `Edem`, but it is not activated by tunicamycin or thapsigargin in the same way as ATF6.
  - Liang et al. 2006, DOI `10.1128/MCB.01046-06`, PMID `16940180`: CREB3/Luman directly regulates the ERAD gene `Herpud1` through an ER-stress response element and contributes to `Herpud1` induction under ER stress.
  - Asada et al. 2011, DOI `10.1093/jb/mvr041`, PMID `21454302`: ATF6-like ER-resident bZIP factors, including CREB3/Luman, have specialized stimuli and tissue distributions rather than interchangeable UPR roles.
  - Xue et al. 2016, DOI `10.3892/ijo.2016.3576`, PMID `27278737`: CREBRF can act upstream of CREB3/ATG5-dependent autophagy in hypoxic glioblastoma cells.
  - Oh-Hashi et al. 2021, DOI `10.1007/s11033-021-06543-2`, PMID `34275032`: mouse CREBRF is an unstable proteasome substrate and can potentiate a CREB3 reporter in Neuro2a cells without simply phenocopying canonical ER stress.
  - Frahm et al. 2020, DOI `10.1210/endocr/bqaa163`, PMID `32901804`: germline `Crebrf` loss alters anxiety-like behavior and circulating glucocorticoids in adult mice, supporting organism-level neuroendocrine biology but in a chronic global setting.
  - Minster et al. 2016, DOI `10.1038/ng.3620`, PMID `27455349`: the human CREBRF p.Arg457Gln variant is associated with Samoan BMI and altered energy use/fat storage in an adipocyte model; I treated this as tissue- and variant-specific context, not as a direct neuronal loss-of-function analog.

## Computational evidence

I first read the manifest and confirmed that it contains only `Crebrf`; `Crebrf` is absent from the training count CSV, as required. The focal training distribution is strongly zero-inflated:

- 1,205 of 1,674 training targets have `n_degs = 0`.
- 363 have 1-9 DEGs.
- 63 have 10-99 DEGs.
- 43 have at least 100 DEGs.

I then pulled the exact focal counts for represented perturbations related to CREB3/CREB signaling or ER-stress transcription:

| perturbation class | training target | `n_degs` in 151 |
| --- | ---: | ---: |
| CREB/PKA/KAT3 nuclear arm | `Ep300` | 0 |
| CREB/PKA/KAT3 nuclear arm | `Prkaca` | 1 |
| CREB/PKA/KAT3 nuclear arm | `Crebbp` | 8 |
| CREB/PKA/KAT3 nuclear arm | `Creb1` | 10 |
| canonical ATF6/UPR or ERAD regulators | `Atf6` | 0 |
| canonical ATF6/UPR or ERAD regulators | `Edem3` | 0 |
| ER-associated genes that did not give a broad HSPA5-like response | `Fgf12` | 0 |
| ER-associated genes that did not give a broad HSPA5-like response | `Lman2l` | 0 |
| ER-associated genes that did not give a broad HSPA5-like response | `Mttp` | 0 |
| ER-associated genes that did not give a broad HSPA5-like response | `Suco` | 0 |
| ERAD or BAP31 branch controls | `Amfr` | 1 |
| ERAD or BAP31 branch controls | `Bcap31` | 1 |
| ER stress / chaperone positives | `Manf` | 3 |
| ER stress / chaperone positives | `Hspa5` | 5 |
| ER stress / translocation positives | `Sec63` | 11 |
| strong ER-load counterexamples | `Dhdds` | 116 |
| strong ER-load counterexamples | `Atp2a2` | 187 |
| strong ER-load counterexamples | `Gfpt1` | 311 |

For the small analog signatures I also queried the parquet directly for focal rows with `pvals_adj < 0.05`:

- `Atf6`, `Edem3`, `Fgf12`, `Lman2l`, `Mttp`, `Suco`, `Sil1`, `Nfe2l1`, `Nfe2l2`, and `Ep300`: no FDR 0.05 genes.
- `Amfr` and `Bcap31`: one self-transcript hit each and no detectable downstream module.
- `Prkaca`: one self-transcript hit and no downstream CREB program.
- `Manf`: `Hspa5` and `Pdia6` up, with `Manf` itself down.
- `Hspa5`: `Hsp90b1`, `Nfe2l1`, `Pdia4`, and `Derl3` up, with `Erc1` down.
- `Sec63`: a stronger ER-client program including `Hspa5`, `Canx`, `Hyou1`, and `Chac1` up, plus neuronal/surface features such as `Nlgn2` and `Syne1` down.
- `Creb1`: `Crem` up and a small mixed set including `Tmem181a`, `Txndc12`, `Chkb`, `Nceh1`, `Ppox`, `Rnf139`, and `Sez6l2` down.
- `Crebbp`: an 8-gene focal response that did not share the `Creb1`/`Crem` or ER-chaperone pattern.

Finally, I ran a focal-cell Distributed Agents `profile_compare` on 20 selected CREB/UPR analogs. In that selected cohort, 10/20 targets had no significant focal feature, 8/20 had 1-9 significant features, and only `Creb1` and `Sec63` entered the 10-49 band. The profile inspection recovered `Atf6` as a no-significant-feature node, `Hspa5` as a 5-feature node, `Manf` as a 3-feature node, `Sec63` as an 11-feature node, and `Creb1` as a 10-feature node, matching the count CSV.

## Target-specific reasoning

### `Crebrf`

`Crebrf` encodes CREB3 regulatory factor, a protein linked most directly to the Luman/CREB3 bZIP transcription-factor branch. CREB3/Luman has biochemical connections to ERAD genes such as `Herpud1` and to UPRE/ERSE-driven transcription, but the literature describes it as an ATF6-like, specialized ER-resident bZIP rather than the core ATF6 or IRE1/PERK apparatus. Mouse CREBRF overexpression in Neuro2a cells potentiated CREB3 reporter output and endogenous CREBRF was low and proteasome-sensitive, pointing to a regulatory role with weak basal abundance rather than to loss of a constitutive ER chaperone.

The within-dataset tests place that kind of regulator on the quiet side. `Atf6`, the canonical and much stronger ATF6 branch perturbation, had `n_degs = 0` in the exact endpoint and the Distributed Agents corpus reports it as a broad basal null across recovered neuronal groups. Other represented ERAD or ER-associated perturbations that could have exposed generic ER-stress sensitivity, including `Edem3`, `Lman2l`, `Mttp`, `Suco`, and `Fgf12`, were also zero in the focal count file. `Amfr` and `Bcap31` were one-hit, self-only cases. This argues that acute basal loss of a regulatory ER-stress branch usually fails to make a durable 151 TH Prkcd Grin2c Glut RNA program.

The positive ER comparators are useful counterexamples rather than direct analogs. `Hspa5`, `Manf`, and `Sec63` have 5, 3, and 11 focal DEGs, respectively, and their parquet rows show actual ER client-handling markers: `Hspa5`, `Hsp90b1`, `Pdia4`, `Pdia6`, `Derl3`, `Canx`, `Hyou1`, and `Chac1`. Stronger 151 responses from `Gfpt1`, `Dhdds`, and `Atp2a2` perturb N-glycan precursor supply, dolichol supply, or ER calcium loading and therefore impose ER client load directly; they are not good quantitative matches for a CREB3 modulator. CREBRF loss might change CREB3 or autophagy under hypoxia or secretory stress, but there is no evidence that it should mimic BiP/MANF/SEC63 depletion in unstimulated juvenile thalamic neurons.

The CREB/cAMP side is also weak. `Creb1` itself gave only 10 focal DEGs and was centered on `Crem` induction plus a small mixed down-regulated module. More upstream cAMP and coactivator components were smaller or flat: `Prkaca` had only its own transcript as a hit, `Ep300` was zero, and `Crebbp` had 8 genes without the `Creb1` `Crem` pattern. Because CREBRF does not encode the nuclear CREB1 factor and its known CREB3/Luman relationship is ER-associated, I used these as an upper bound for a generic CRE-family nuclear effect, not as evidence for a `Creb1`-sized signature.

CREBRF also has external organism-level associations that I down-weighted for this endpoint. Adult global `Crebrf` knockout mice show altered corticosterone and anxiety-like behavior, and the human p.Arg457Gln missense allele affects BMI and adipocyte energy storage. Those are chronic endocrine/adipose or whole-organism phenotypes; the training table shows `Nr3c1`, `Ncoa1`, `Ncoa3`, `Lepr`, and `Agrp` as zero in the focal 151 group, so they do not justify a broad thalamic single-nucleus transcriptome response after sparse P16 neuronal editing.

Taken together, the focal training data say that direct ER load can produce 100s of DEGs, weak ER-chaperone perturbations produce a few to 11, but basal loss of ER/UPR regulators is usually zero. CREBRF is closer to the latter group than to `Sec63`/`Gfpt1`/`Atp2a2`. I therefore predict no FDR 0.05 genes for `Crebrf`.

Prediction: `Crebrf = 0`.

## Limits of the prediction

- `Crebrf` itself is held out, so there is no direct same-experiment signature, DEG count, or self-transcript measurement for the target.
- The closest biochemical target, `Creb3`/Luman, was not present as a training perturbation. I had to triangulate from `Atf6`, ER-client perturbations, and the separate `Creb1` nuclear CRE-family node.
- Several CREBRF papers use transformed glioblastoma, reproductive, adipocyte, or overexpression systems. Those differ substantially from acute mosaic CRISPR in recovered postmitotic neurons.
- The focal endpoint includes self-transcript hits. I predicted zero rather than adding a default self-hit because target-RNA loss is unreliable in this assay and the CREBRF literature suggests low endogenous neuronal-model expression, but a self-only call is still the main way the prediction could be off by one.
- Absence of a durable mRNA response at P37-P44 would not exclude transient ER-stress signaling, protein-level CREB3/autophagy changes, endocrine phenotypes, or effects in hypothalamic, glial, retinal, adipose, or reproductive cell types that are not represented by this readout.
