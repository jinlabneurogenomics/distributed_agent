# DEG-count prediction trace

## Question and setup

The requested held-out perturbation set contains one target, `Zfp398`, from `270_Zfp398.csv`. I interpreted the endpoint as the exact focal-cell count:

```text
151 TH Prkcd Grin2c Glut, n_degs = number of measured genes with pvals_adj < 0.05
```

The `Zfp398` perturbation itself is absent from both `training_de_all_cell_groups.parquet` and `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, so I did not use any direct same-target signature. The exact DEG-count CSV was treated as the authoritative FDR 0.05 endpoint; the same-experiment Distributed Agents corpus was used only as a curated semantic layer over non-held-out perturbations, and I treated its FDR 0.10 summaries as pattern-level annotations rather than exact substitutes for the FDR 0.05 training endpoint.

## Sources used

* Training DEG-count CSV for the endpoint values of all assayed, non-held-out targets in `151 TH Prkcd Grin2c Glut`.
* Training DE parquet for focal-cell significant genes and matched-nucleus counts for biologically selected comparator perturbations.
* Distributed Agents same-experiment corpus release `perturbai-july-260713-sourceguard-1773-v1`, queried with `target_context`, `search_claims`, and calibration endpoints for preinterpreted non-held-out Findings.
* NCBI Gene record `272347`, queried 2026-09-23, and UniProtKB mouse `Zfp398` entries `Q8BVH0`/`Q8BV16`, queried 2026-09-23, for the mouse gene identity and predicted nuclear RNA polymerase II transcription-factor annotation.
* Literature for ZNF398/ZER6 biology:
  * Conroy et al. 2002, JBC, DOI `10.1074/jbc.M107702200`, PMID `11779858`: defined ZER6 as a KRAB/C2H2 zinc-finger transcription factor with p52 and p71 isoforms and estrogen-receptor-alpha-dependent regulation.
  * Zorzan et al. 2020, Nature Communications, DOI `10.1038/s41467-020-16205-9`, PMID `32398665`: found human ZNF398 downstream of TGF-beta in pluripotent stem cells, binding active promoters/enhancers with SMAD3 and EP300.
  * Kwag et al. 2025, BBRC, DOI `10.1016/j.bbrc.2025.151316`, PMID `39809138`: reported predominant brain expression of p52-ZER6 and repression of `MT3` by p52-ZER6 in neuronal cell-line models.
  * Zorzan et al. 2025, Nature Cell Biology, DOI `10.1038/s41556-025-01831-6`, PMID `41339717`: placed ZNF398 downstream of TGF-beta in a human epiblast model.

## Computation over the supplied dataset

I first checked the endpoint distribution in the 1,674-target training CSV. It is zero-inflated: 1,205/1,674 targets have `n_degs = 0`, the median is `0`, the 75th percentile is `1`, the 95th percentile is `18`, and only 43 targets have `n_degs >= 100`. The held-out `Zfp398` target is not in this file.

I then filtered the 616,253,184-row parquet to rows with:

```sql
group_name = '151 TH Prkcd Grin2c Glut'
AND gene_target IN (
  selected C2H2/KRAB/SCAN zinc-finger targets,
  TGF-beta/BMP receptor-SMAD targets,
  EP300/CREBBP/ESR/MT3 comparators,
  and high-DE transcription-factor counterexamples
)
AND pvals_adj < 0.05
```

This recovered the exact focal significant genes and the matched perturbed/control nucleus counts for the analogs below. I used the exact `n_degs` in the training CSV for calibration and used the parquet hits to verify whether a comparator was truly flat, singleton-only, or broad in the same focal cell group.

## Target-specific reasoning

### `Zfp398`

`Zfp398` is the mouse ortholog of human `ZNF398`/`ZER6`, a predicted nuclear RNA polymerase II transcription regulator. The public biology makes it a plausible transcriptional repressor, but not one with a known mature thalamic glutamatergic program:

* ZER6/ZNF398 has KRAB and C2H2 zinc-finger domains and p52/p71 isoforms; p52 can interact with estrogen receptor alpha in the presence of estradiol in reporter systems (Conroy et al. 2002, DOI `10.1074/jbc.M107702200`).
* In human pluripotent stem cells, ZNF398 cooperates with `SMAD3` and `EP300` to promote TGF-beta-dependent pluripotency and epithelial identity genes (Zorzan et al. 2020, DOI `10.1038/s41467-020-16205-9`; Zorzan et al. 2025, DOI `10.1038/s41556-025-01831-6`). That is a developmental epithelial/pluripotency context, not a P16-to-P37 postmitotic neuronal perturbation.
* In neuronal cell-line work, p52-ZER6 repressed `MT3`, increasing ROS after overexpression, and ERalpha reduced p52-ZER6 occupancy at the `MT3` promoter (Kwag et al. 2025, DOI `10.1016/j.bbrc.2025.151316`). This creates a weak prior for a small `Mt3` derepression phenotype after Zfp398 loss, but the study used overexpression/cell lines/AD cortex rather than acute sparse knockout of juvenile thalamic neurons.

The closest within-dataset evidence argues against a broad focal response.

**KRAB/C2H2/SCAN zinc-finger comparators.** `Zfp397`, `Zfp664`, `Zkscan1`, `Zkscan16`, and `Zfp644` were all `0` in the focal training endpoint. `Zfp612` was the only very close KRAB-associated exception but had only `1` focal DEG, `Notum` up with log2FC `1.01` at FDR `1.6e-7`, from 252 perturbed versus 23,679 control nuclei. The Distributed Agents corpus also has a moderate-confidence same-experiment Claim that represented SCAN/C2H2/KRAB-associated zinc-finger perturbations did not form an interchangeable neuronal regulon; `Zfp397`, `Zfp664`, and `Zkscan1` were explicitly all-null or nonconvergent in their matched neuronal surfaces. These are not proven Zfp398 paralogs, but they are the best assayed sequence-specific KRAB/C2H2 boundaries, and their endpoint counts put the local prior near zero.

**Other C2H2 zinc-finger transcription factors.** Some more distant zinc-finger regulators were not silent: `Zfp148` had `8` focal DEGs and `Zfp236` had `19`. Their signatures were narrow and idiosyncratic (`Zfp236` was led by `Ogt`, `Eif4a2`, and `Gdi1`; `Zfp148` by `Ypel4`, `Srrm2`, `Cacnb3`, and `Plekhj1`). These counts show that a zinc-finger perturbation can cross FDR in `151 TH Prkcd Grin2c Glut`, but they support a weak/small expectation rather than a large one.

**Large TF counterexamples.** `Zbtb7a` and `Zfp423` demonstrate that the focal cell group has ample power for transcription-factor responses when the target controls a postmitotic neuronal state. `Zbtb7a` produced `841` DEGs in the focal endpoint from 282 matched perturbed cells, dominated by `Pnma3`, `Col9a3`, `Gpc1`, `Usp11`, `Sema4a`, and lysosome/endomembrane/neuropeptide remodeling. `Zfp423` produced `150` DEGs from 160 matched perturbed cells, with a thalamic identity and receptor/adhesion signature led by downregulated `Grid2ip`, `Cd47`, `Syt13`, `Grin2c`, and `Slc12a5` and upregulated `Ntsr1`, `Kcnab3`, `Nptxr`, and `Ptprm`. These are useful positive controls, not direct predictors: the Distributed Agents corpus specifically notes that obvious `Zfp423` relatives such as `Zfp521`, `Ebf1/2/3`, BMP-SMADs, RA receptors, and `Zic` genes did not phenocopy `Zfp423`, so transferring a high count across a generic DNA-binding label would overfit.

**TGF-beta/SMAD/EP300 axis.** The stem-cell ZNF398 papers made `Smad3`, `Smad2`, `Smad4`, TGF-beta receptors, BMP/activin receptors, and `Ep300` the most mechanistic pathway comparators. In the focal count file, all of `Smad1`, `Smad3`, `Smad4`, `Smad6`, `Smad9`, `Tgfbr1`, `Tgfbr2`, `Tgfbr3`, `Acvr1`, `Acvr2a`, `Acvr2b`, `Acvrl1`, `Bmpr1a`, `Bmpr1b`, `Bmpr2`, and `Ep300` were `0`; `Smad2` had a one-gene focal signature, `Cpne7` down at log2FC `-0.41`; `Crebbp` had `8`. The Distributed Agents corpus independently summarizes represented TGF-beta/activin/BMP receptor-SMAD perturbations as flat, singleton-only, or nonconvergent in basal postnatal neuronal snRNA-seq. Thus, the external human PSC mechanism does not transfer to this assay as a broad basal thalamic module.

**`MT3`/estrogen-receptor branch.** The Kwag et al. 2025 neuronal model suggests `Mt3` as a possible p52-ZER6 target. The focal training count for `Mt3` perturbation was only `1`, and the only significant row was the direct `Mt3` transcript decrease after `Mt3` CRISPR itself; `Esr1` and `Esr2` were both `0`. In the focal parquet, `Mt3` was not FDR-significant after `Zfp397`, `Zfp612`, `Zfp664`, `Zkscan1`, `Smad2/3/4`, `Tgfbr1/2/3`, or `Ep300`. This does not rule out `Mt3` derepression after direct `Zfp398` loss, but it makes a multi-gene oxidative or estrogen-linked response unlikely.

Putting those lanes together, I predict that `Zfp398` will be buffered or context-displaced in recovered `151 TH Prkcd Grin2c Glut` nuclei. The only positive external prior points to a possible singleton `Mt3`-like event, while the measured KRAB/C2H2 and TGF-beta/SMAD/p300 comparators are overwhelmingly null at FDR 0.05. I therefore chose the zero side of the zero/nonzero decision and used `0` as the point count rather than `1`.

## Limits and uncertainty

`Zfp398` itself was completely held out, so all reasoning is extrapolation from imperfect neighbors. The represented zinc-finger genes are family comparators rather than direct `Zfp398` paralogs or known binding partners; `Trim28`/KAP1 and many KRAB proteins were not available as exact pathway controls. ZNF398 mechanisms in the literature come mostly from human PSCs, epiblast models, cancer cells, or neuronal overexpression systems, and could miss a mouse thalamic p52-ZFP398 function. The assay measures survivor-conditioned nuclear RNA 3-4 weeks after sparse CRISPR; repeat-derived KRAB outputs, transient SMAD activity, ROS, metal buffering, indel rate, and protein abundance were not directly measured. Because the focal count distribution is highly zero-inflated, the boundary between `0` and a singleton FDR hit remains the largest uncertainty for this target.
