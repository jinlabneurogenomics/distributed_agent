# Reasoning trace

## Question and resolved ambiguities

The requested held-out target manifest contained one perturbation:

```text
Prokr2
```

I interpreted the task as a point prediction of the number of genes that would pass Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after acute AAV-CRISPR loss of `Prokr2` in the focal `151 TH Prkcd Grin2c Glut` neuronal group. I used the requested endpoint literally: the prediction is the assay-specific count of significant measured genes in this one cell group, not a prediction of organismal phenotype severity, circuit physiology, or the number of all biologically perturbed genes.

I also treated `Prokr2` as fully held out: no `Prokr2` perturbation signature or focal `Prokr2` DEG count was used, and the available within-dataset evidence comes only from non-held-out targets.

## Sources

- `training_de_all_cell_groups.parquet`: per-gene signed differential-expression statistics for non-held-out perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed `n_degs` for 1,674 non-held-out perturbations in the focal cell group.
- `187_Prokr2.csv`: requested target manifest.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`. There was no `Prokr2`-scoped finding, but retrieved claims about neuromodulatory GPCR, Gq/PLC/Ca2+, and circadian perturbations in the same screen were used as same-experiment summaries.
- Local Distributed Agents gene-annotation tables from the gene-annotation skill:
  - `gene_relationships.parquet`, including STRING physical-interaction edges from STRING v12.0.
  - `gene_membership.parquet`, including GO, Reactome, MSigDB/WikiPathways, and functional-class memberships.
- Public literature:
  - Cheng et al., 2002, Nature, DOI `10.1038/417405a`, PMID `12024206`.
  - Prosser et al., 2007, PNAS, DOI `10.1073/pnas.0606884104`, PMID `17202262`.
  - Abreu et al., 2008, J. Clin. Endocrinol. Metab., DOI `10.1210/jc.2008-0958`, PMID `18682503`.
  - Sarfati et al., 2010, Frontiers of Hormone Research, DOI `10.1159/000312698`, PMID `20389090`.
  - Morris et al., 2021, EMBO J., DOI `10.15252/embj.2021108614`, PMID `34487375`.

## Computations over the supplied data

I first read the requested-target CSV and confirmed that the only requested target was `Prokr2`.

I used the focal training count table to calibrate response breadth. In `151 TH Prkcd Grin2c Glut`, the training endpoint is highly zero-heavy:

- 1,674 training perturbations total.
- 1,205/1,674 had `n_degs = 0`.
- Median `n_degs = 0`; 75th percentile `= 1`; 90th percentile `= 2`; 95th percentile `= 18`.
- The extreme broad responses were rare outliers such as `Uba5 = 2677`, `Tpr = 1768`, `Sin3a = 1433`, `Rnpc3 = 868`, and `Zbtb7a = 841`, none of which is mechanistically close to `Prokr2`.

I then selected focal-cell training perturbations that test three mechanistic possibilities:

1. peptide and neuromodulatory GPCR receptor losses;
2. G protein, PLC, Ca2+, MAPK, and CREB-adjacent downstream losses;
3. circadian and ROR/REV-ERB perturbations, because public `Prok2`/`Prokr2` biology is strongest in the SCN clock-output system.

The all-cell DE parquet was profiled only under `group_name == "151 TH Prkcd Grin2c Glut"`. I compared the signed `logfoldchanges` vectors for a 28-node declared cohort:

```text
Kiss1r, Tacr3, Npy1r, Npy2r, Npy5r, Cckar, Cckbr,
Chrm2, Chrm3, Grm5, Htr2c, Plcb1, Gnao1, Cnr1, Sstr5,
Bmal1, Nr1d1, Clock, Cry1, Cry2, Nr1d2, Rora, Rorb, Rorc,
Creb1, Ppp3ca, Ppp3r1, Map2k1
```

The same-focal-cell profile comparison showed:

- 15 of 28 candidate analogs had no FDR-significant features.
- 9 of 28 had only 1-9 significant features.
- 1 of 28 had 10-49 significant features.
- 3 of 28, `Rora`, `Nr1d1`, and `Bmal1`, had at least 50 features.
- Across all 378 candidate pairs, the median significant-program overlap coefficient was `0` in both the positive and negative directions.

This made broad pathway pooling inappropriate: even within a hand-picked `Prokr2`-relevant panel, receptor and second-messenger genes did not form a shared FDR-supported transcriptional module.

## Prokr2-specific analogs and counterexamples

The exact same-ligand analogs were not represented. The local annotation layer placed `Prokr2` in a very small prokineticin module:

- `Prok1` -- `Prokr2`, STRING v12.0 physical interaction, confidence `0.916`.
- `Prok2` -- `Prokr2`, STRING v12.0 physical interaction, confidence `0.982`.
- `Prok1` -- `Prokr1` and `Prok2` -- `Prokr1` were also present.

`Prok1`, `Prok2`, and `Prokr1` were not in the focal training-count table, so they could not provide direct endpoint calibration.

The nearest receptor and Gq/PLC examples instead argued for zero:

| training perturbation | focal `n_degs` | relevance to `Prokr2` | interpretation |
|---|---:|---|---|
| `Kiss1r` | 0 | peptide Class A GPCR; hypogonadotropic-hypogonadism/GnRH-axis comparator | No durable basal thalamic nuclear-RNA response. |
| `Tacr3` | 0 | tachykinin peptide GPCR, another HPG/KNDy/GnRH-axis receptor | No effect in the focal endpoint. |
| `Npy1r`, `Npy2r`, `Npy5r` | 0, 0, 0 | peptide GPCRs | All zero, arguing against a generic peptide-receptor effect. |
| `Cckar`, `Cckbr` | 0, 0 | peptide GPCRs | Both zero. |
| `Chrm3`, `Grm5`, `Htr2c` | 0, 0, 0 | represented Gq/PLC-linked neuromodulatory receptors | No focal DEGs despite canonical receptor signaling proximity to PROKR2. |
| `Plcb1` | 0 | immediate Gq effector for phosphoinositide/calcium signaling | Direct loss of a proximal effector was also zero. |
| `Chrm2`, `Sstr5` | 0, 0 | Gi/o-coupled receptor counterexamples | Other neuromodulatory receptor losses were also flat. |
| `Gnao1`, `Cnr1` | 1, 1 | Gi/o/cannabinoid signaling | Singleton-only activity, not a broad module. |

The Distributed Agents corpus independently summarized the same pattern for this assay. A moderate-confidence claim over `Chrm2`, `Chrm3`, `Grm5`, `Htr2c`, `Kiss1r`, and `Plcb1` states that represented neuromodulatory GPCR receptors and proximal second-messenger effectors generally fail to produce a shared basal neuronal nuclear-transcriptome module. Related same-experiment claims reported flat or nonconvergent outputs for HPG/KNDy/GnRH-axis targets, mGluR/PLC/IP3/Ca2+ pathway nodes, Gi/o effectors, and cAMP/PKA/CREB-adjacent GPCR pathway genes. This evidence is directly from the supplied perturbation universe and is the main driver of the predicted zero.

Circadian comparators were a biologically important counterweight, because `Prok2` is an SCN clock-output neuropeptide. The focal training set showed that `151 TH Prkcd Grin2c Glut` can detect some circadian/ROR perturbations:

| training perturbation | focal `n_degs` | relation to `Prokr2` |
|---|---:|---|
| `Bmal1` | 103 | core positive-limb clock transcription factor. |
| `Nr1d1` | 116 | REV-ERB clock repressor; shared a detectable thalamic state with `Bmal1`. |
| `Rora` | 278 | ROR-family nuclear receptor with a selective thalamic signature. |
| `Clock` | 3 | core positive-limb clock factor but only a sparse focal response. |
| `Cry1`, `Cry2`, `Nr1d2` | 1, 3, 1 | clock-loop genes with narrow responses. |
| `Rorb`, `Rorc` | 0, 0 | ROR-family counterexamples. |

The `Bmal1`-`Nr1d1` pair shared 35 positive and 4 negative significant genes in the 28-node profile cohort, whereas `Bmal1`-`Rora` shared only 3 negative significant genes and had 16 significant direction conflicts, and `Nr1d1`-`Rora` shared only 2 significant genes with 14 direction conflicts. The same-experiment corpus also stated that represented circadian, ROR, and REV-ERB pathway perturbations are not interchangeable in this acute postnatal neuronal loss-of-function surface.

I therefore used the circadian positives as evidence that the focal cell group is capable of reporting stable clock transcription-factor perturbations, but not as evidence that every clock-associated output receptor will have the same endpoint. `Prokr2` is a membrane receptor for the SCN output peptide rather than a core CLOCK/BMAL1/REV-ERB transcriptional node.

## External biological rationale

`Prokr2` encodes prokineticin receptor 2, a GPCR for PROK2/BV8-family ligands. The strongest mouse brain phenotypes reported for this axis are not simple broad postmitotic neuronal RNA effects:

- Cheng et al. identified `Prok2` as a rhythmic SCN output molecule and showed that exogenous PK2 suppresses nocturnal locomotor activity; receptor expression is part of the SCN output architecture rather than a core clock transcriptional factor.
- Prosser et al. found that `Prokr2` null mice have disrupted circadian coordination of locomotor activity and thermoregulation but retain a competent SCN cellular oscillator in organotypic slices, consistent with an output/circuit role.
- Morris et al. showed by SCN single-cell analysis and genetics that `Prok2`-`Prokr2` signaling shapes network-level SCN period and rhythmicity.
- `PROK2` and `PROKR2` loss-of-function mutations cause Kallmann syndrome and hypogonadotropic hypogonadism through developmental olfactory-bulb/GnRH-neuron biology, as summarized and extended by Abreu et al. and Sarfati et al.

Those functions are real, but they do not map tightly onto the experimental endpoint here: the assay perturbs postmitotic juvenile neurons after AAV delivery at P16, reads out unstimulated nuclear RNA 3-4 weeks later, excludes the olfactory bulb and hindbrain, and asks about one thalamic glutamatergic cell group. Developmental GnRH/olfactory-bulb phenotypes and SCN circuit timing are therefore more likely to be missed or to appear outside this focal group than to cause dozens of FDR-supported genes in `151 TH Prkcd Grin2c Glut`.

## Prediction

I predict:

```text
Prokr2 -> 0 DEGs
```

The zero/nonzero call is driven mainly by within-dataset evidence: the best available acute neuronal peptide-GPCR and Gq/PLC receptor analogs were flat in the focal group, the closest training G-protein/PLC examples were zero or singleton-only, and same-experiment Distributed Agents claims report repeated failure of these basal receptor perturbations to collapse into a shared nuclear-RNA module. External knowledge raises `Prokr2` as biologically important but points to developmental, circuit-output, and SCN-specific phenotypes rather than to a broad thalamic postmitotic transcriptional response.

## Limits

- No direct `Prokr2`, `Prokr1`, `Prok1`, or `Prok2` training perturbation was available, so the comparison necessarily extrapolates from other peptide GPCRs and downstream signaling genes.
- Class A peptide GPCRs are imperfect analogs: ligand availability, receptor localization, basal tone, and coupling can be cell-type-specific.
- The all-feature profile similarities of sparse GPCR perturbations can be inflated by shared unexpressed or floor-effect genes, so I relied on FDR-supported counts and significant-program overlap rather than whole-vector cosine alone.
- Public `Prokr2` studies often use germline knockouts, congenital human genetics, SCN-specific preparations, or circuit/behavioral endpoints. Those are informative about mechanism but do not directly estimate the acute partial AAV-CRISPR snRNA-seq endpoint.
- A true `Prokr2` effect in a rare `Prokr2`-expressing subset of the thalamic group, on protein localization, or after ligand/circadian stimulation could be invisible to this pooled basal single-endpoint differential-expression test.
