# Held-out DEG-count prediction for `151 TH Prkcd Grin2c Glut`

Correction: the focal group in the task is `151 TH Prkcd Grin2c Glut`, a thalamic glutamatergic neuronal group; `TH` was treated as the atlas thalamus abbreviation, not as the `Th` tyrosine-hydroxylase gene. The requested manifest contained exactly one held-out target, `Six1`. I therefore predicted the number of genes that would have `pvals_adj < 0.05` for a P16-to-P37/P44 sparse AAV-CRISPR loss-of-function perturbation of `Six1` in this one focal cell group. I used a point integer for the FDR-0.05 DEG count and did not use either the held-out target itself, any held-out signature, or target-transcript knockdown as a proxy for editing strength.

## Sources used

- Differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Focal-cell training endpoint table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested-target manifest: `[local file: 207_Six1.csv]`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, queried through `target_context` and `search_claims` for `Six3`, `Six5`, and `Dach1`. There was no `Six1` node in this corpus because `Six1` was held out for this run.
- Distributed Agents runtime focal-profile comparison over selected candidate analogs, written to `six1_candidate_profile_compare.json` and inspected through `six1_candidate_profile_inspect.json`.
- External literature retrieved with NCBI PubMed E-utilities.

## Dataset calculations

I first loaded the requested-target CSV and verified that it contains only `Six1`. I then used the focal training CSV to calibrate counts in `151 TH Prkcd Grin2c Glut`. The endpoint is sparse: among 1,674 training perturbations, 1,205 have `n_degs = 0`, the median is `0`, the 75th percentile is `1`, and the mean is pulled upward by a small number of large responses.

For mechanistic analogs I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and to the represented SIX/retinal-determination/TGF-neighborhood targets:

`Six3`, `Six5`, `Dach1`, `Pax6`, `Ski`, `Smad1`, `Smad2`, `Smad3`, `Smad4`, `Smad6`, `Smad9`, `Tgfbr1`, `Tgfbr2`, `Tgfbr3`, `Tgif1`, `Crebbp`, and `Ep300`.

For each perturbation I counted rows with `pvals_adj < 0.05` and inspected the smallest adjusted p-values. The direct focal counts were:

| training perturbation | focal `n_degs` | focal nuclei vs control | reason used |
| --- | ---: | ---: | --- |
| `Six3` | 0 | 167 vs 23,679 | represented SIX-family homeobox factor; eye/anterior-neural comparator |
| `Six5` | 0 | 215 vs 23,679 | represented SIX-family factor, coexpressed with `Six1`/`Six4` in several developmental settings |
| `Dach1` | 0 | 173 vs 23,679 | core PAX-SIX-EYA-DACH / retinal-determination network member |
| `Pax6` | 0 | 138 vs 23,679 | eye-field/Pax-Six-Eya-Dach developmental comparator |
| `Ep300` | 0 | 155 vs 23,679 | broad transcriptional coactivator and RDGN-adjacent counterexample in the corpus |
| `Crebbp` | 8 | 61 vs 23,679 | paralogous p300/CBP coactivator, positive but small focal counterexample |
| `Ski` | 2 | 335 vs 23,679 | TGF/SMAD pathway regulator compared to `Dach1` in the corpus |
| `Smad2` | 1 | 136 vs 23,679 | TGF/SMAD pathway comparator |
| `Smad1`, `Smad3`, `Smad4`, `Smad6`, `Smad9` | 0 | 123-283 vs 23,679 | BMP/TGF SMAD comparators |
| `Tgfbr1`, `Tgfbr2`, `Tgfbr3`, `Tgif1` | 0 | 180, 298, 164, 217 vs 23,679 | TGF receptor/TGIF comparators |

The most direct analogs, `Six3`, `Six5`, `Dach1`, and `Pax6`, had no focal genes even nominally close to the FDR boundary: every row for these four targets in `151 TH Prkcd Grin2c Glut` had `pvals_adj = 1.0`. In the full training table outside the focal cell group, `Six5` was null in all 23 measured neuronal groups, `Pax6` was null in all 22 groups in which it was tested, `Six3` had a single off-focal FDR<0.05 gene in `007 L2-3 IT CTX Glut`, and `Dach1` had a single off-focal FDR<0.05 gene in `017 CA3 CA2-FC DG Glut`.

I then used the Distributed Agents runtime `profile_compare` operation on the same focal log-fold-change vectors for the 14-gene candidate set above. This was meant as a sanity check on the expression signatures, not as a way to manufacture signal from sub-threshold rows. The four most relevant profiles, `Six3`, `Six5`, `Dach1`, and `Pax6`, each had 17,259 measured features and zero significant positive or negative features. The exact FDR-significant intersections with the sparse `Ski`, `Smad2`, and `Crebbp` signatures were also all zero. Whole-vector Pearson/cosine values among null profiles were moderate because weak non-significant log-fold changes share background structure, so I treated the FDR-level absence of a focal signature as the salient evidence for this endpoint.

## Distributed Agents same-experiment corpus evidence

- `Six5`: the curated corpus reports a high-confidence negative result: `Six5` loss produced a pan-neuronal transcriptional null, with zero downstream genes at FDR<0.10 in every one of 23 measured mouse-brain neuronal groups. The same report also found no hidden Six5 module by cross-perturbation search; the strongest positive Wilcoxon-score neighbor had only `r = 0.0349`, the strongest anti-neighbor had `r = -0.0314`, and several extrema were safe-target controls or nearly flat biological perturbations. This is the best same-family negative analog for `Six1`.
- `Six3`: the curated corpus reports only one FDR-supported `Six3` phenotype, `Slc6a6` up in `007 L2-3 IT CTX Glut` from 72 perturbed nuclei, and separately reports that P16 `Six3` perturbation did not move canonical Wnt/BMP/SHH/FGF sentinels or anterior forebrain/eye transcription factors in any measured neuronal group. This supports the interpretation that a SIX factor can be strongly developmental yet transcriptionally buffered after acute postnatal neuronal editing.
- `Dach1`: the corpus reports only a one-gene `Ppdpf` response in `017 CA3 CA2-FC DG Glut`; global Dach1 similarity was near zero, and the curated RDGN/TGF/SMAD comparison found that `Six3`, `Six5`, `Ski`, `Smad1/2/3/4/6/9`, `Tgfbr1/2/3`, `Tgif1`, `Crebbp`, and `Ep300` did not phenocopy a shared Dach1 state in P16 neurons. This argues against a recurrent postmitotic RDGN module in the observed brain neurons.

## External biological rationale

`Six1` encodes a SIX homeobox transcription factor. The family is ancient and its members act with EYA and DACH proteins in the conserved Pax-Six-Eya-Dach / retinal-determination network; SIX proteins use a SIX domain and SIX-type homeodomain for DNA binding and EYA interaction (Kawakami et al., 2000, DOI `10.1002/1521-1878(200007)22:7<616::AID-BIES4>3.0.CO;2-R`; Christensen et al., 2008, DOI `10.1016/S0065-230X(08)00405-3`). In mouse, germline `Six1` loss disrupts embryonic patterning of inner ear, nose, thymus, kidney, skeletal muscle, and sensory ganglia rather than pointing to a mature thalamic-neuron maintenance function: Ozaki et al. showed that Six1-deficient embryos have severe inner-ear patterning defects together with nose, thymus, kidney, and skeletal-muscle abnormalities (2003, DOI `10.1242/dev.00943`); Zou et al. placed `Six1` and `Eya1` in embryonic thymus/parathyroid pouch patterning (2006, DOI `10.1016/j.ydbio.2005.12.015`); and Konishi et al. showed that `Six1` and `Six4` support early trigeminal sensory-neuron survival (2006, DOI `10.1016/j.brainres.2006.07.103`). `Six1` and `Six4` are also redundant in mouse embryonic myogenesis and gonadogenesis, including Pax3/Mrf control and male sex determination through Fog2/Zfpm2 and Nr5a1/Sf1 pathways (Grifone et al., 2005, DOI `10.1242/dev.01773`; Fujimoto et al., 2013, DOI `10.1016/j.devcel.2013.06.018`).

That prior makes `Six1` a developmental fate and organogenesis factor, but it does not nominate a strong reason for a surviving juvenile thalamic glutamatergic nucleus to launch a broad 10x nuclear RNA response when the perturbation is sparse and begins at P16. The closest represented same-experiment perturbations already stress-tested that idea: `Six3`, `Six5`, `Dach1`, and `Pax6` were all exactly zero in the focal endpoint, and the broader SMAD/TGF/RDGN neighborhood was zero or one-gene with only `Crebbp` and `Ski` as small positive exceptions.

## Target-specific prediction

### `Six1`: predicted `0`

The zero/nonzero decision is driven mainly by within-dataset evidence. The two represented SIX-family perturbations do not produce a focal FDR<0.05 signature: `Six3` has `0` DEGs and `Six5` has `0` DEGs in `151 TH Prkcd Grin2c Glut`. `Six5` is especially useful as a boundary case because the Distributed Agents corpus calls it a pan-neuronal null across all measured groups at FDR<0.10, while `Six3` only has one off-focal cortical `Slc6a6` DEG. The core RDGN comparator `Dach1` and the eye-field/PSEDN comparator `Pax6` are also focal zeros, with `pvals_adj = 1.0` for every measured gene in the focal class. SMAD/TGF comparisons were included because the curated corpus explicitly used them to test for RDGN-adjacent convergence around `Dach1`; they likewise do not reveal a broad thalamic module.

External biology mostly supports the same direction rather than setting the count itself. The best-characterized `Six1` phenotypes are embryonic placodal/sensory, kidney, thymus/parathyroid, gonadal, and muscle programs with `Six4` and EYA cofactors. Those systems are not present, or are long past their sensitive developmental window, in NeuN-enriched thalamic glutamatergic nuclei edited after P16. Because `Six1` itself and its closest same-subfamily partner `Six4` were held out or absent as training perturbations, a one- or two-gene idiosyncratic response remains possible by analogy to `Six3` and `Dach1`; however, there was no focal-cell expression-pattern evidence arguing for a nonzero count. I therefore rounded the expected focal response down to zero DEGs.

## Limits and extrapolation

This is still an extrapolation from related factors, not a direct `Six1` measurement: `Six1` was deliberately absent as a perturbation in both the parquet and the training count CSV. `Six3` and `Six5` are imperfect paralogs; `Six3` belongs to a different SIX subclass, and `Six4`, the closest represented functional partner for `Six1` in several embryonic settings, was not a training perturbation. EYA genes were not available as perturbation targets either. The public literature comes largely from germline embryonic mutants, organ explants, and non-neuronal developmental systems, whereas the assay here is acute, mosaic, postnatal, and survivor-conditioned. A rare focal `Six1`-specific maintenance function in thalamic neurons would be missed by the analog set. The prediction should therefore be read as a calibrated expectation that no gene will cross BH FDR 0.05, not as evidence that `Six1` is biologically unimportant.
