# Reasoning trace

## Question and endpoint alignment

The requested output is a point prediction of `n_degs` for each held-out target in `151 TH Prkcd Grin2c Glut` cells. `n_degs` is the number of measured genes whose Wilcoxon Benjamini-Hochberg adjusted p-value is below 0.05 in the focal cell group. The requested-target manifest contains one perturbation, `Lmx1a`, and that perturbation is absent from both the supplied focal training-count table and the differential-expression Parquet.

I treated the focal training count CSV as the direct source for observed `n_degs` among visible perturbations and the Parquet as the direct source for expression-pattern evidence among visible perturbations. The held-out `Lmx1a` endpoint itself is absent by design, so the prediction is an extrapolation from visible perturbations plus external mechanism.

## Sources used

- Declared training DEG counts: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression Parquet: `training differential-expression dataset`.
- Run-local target manifest: `single-target request for Lmx1a`.
- PerturbAI July same-experiment semantic corpus, queried with `corpus.direct_evidence`, release `perturbai-july-260713-sourceguard-1773-v1`. This is packaged interpretation of the same Perturb-seq experiment, not independent replication.
- PubMed-indexed external literature for Lmx1a/Lmx1b/Foxa/Otx2/Pitx3 dopaminergic and roof-plate biology:
  - Failli, Bachy, and Retaux 2002, `Mechanisms of Development`, DOI `10.1016/s0925-4773(02)00254-x`, PMID `12351192`.
  - Chung et al. 2009, `Cell Stem Cell`, DOI `10.1016/j.stem.2009.09.015`, PMID `19951692`.
  - Nakatani et al. 2009, `Developmental Biology`, DOI `10.1016/j.ydbio.2009.12.017`, PMID `20035737`.
  - Lin et al. 2009, `Developmental Biology`, DOI `10.1016/j.ydbio.2009.07.006`, PMID `19607821`.

## Computation over the declared dataset

I first read the requested-target CSV and verified that it contains only `Lmx1a`. I then read the focal training-count CSV to calibrate the `n_degs` scale:

- 1,674 visible perturbations had focal `n_degs`.
- 1,205 of 1,674 were zero.
- The median was 0, the 75th percentile was 1, the 90th percentile was 2, and the 95th percentile was 18.

I queried the Parquet only for declared rows needed for analog inspection. For every visible developmental or dopamine-lineage perturbation listed below, I filtered to

`group_name == "151 TH Prkcd Grin2c Glut" and gene_target in {visible analogs}`

and counted rows with `pvals_adj < 0.05`, recording the smallest adjusted p-value and the matched perturbed/control nucleus counts. This checks that a zero training count corresponded to a globally flat focal signature rather than to a count-table join issue. I also repeated the count across all assayed cell groups for the closest Lmx1/Foxa/Otx2/Pitx3/En/Msx/Dcc/Isl/Phox2a analog set.

## Lmx1a-specific reasoning

### Mechanistic expectation

`Lmx1a` encodes a LIM-homeobox transcription factor with strong developmental roles in dorsal midline/roof plate and cortical hem patterning and in mesencephalic dopaminergic differentiation. Failli et al. described embryonic nervous-system-restricted `Lmx1a` expression in the roof plate, cortical hem, developing cerebellum, otic vesicle, and notochord. Chung et al. identified a Wnt1-Lmx1a autoregulatory loop that regulates Otx2, Nurr1/Nr4a2, and Pitx3 during midbrain dopaminergic differentiation and noted overlapping Lmx1a/Lmx1b function. Nakatani et al. showed that Lmx1a/Lmx1b cooperate with Foxa2 to specify mesencephalic dopamine identity in floor-plate progenitors. Lin et al. placed Foxa1/Foxa2 upstream of, and cooperative with, Lmx1a/Lmx1b in mesodiencephalic dopaminergic development.

The Perturb-seq experiment, however, perturbed postmitotic postnatal neurons at P16 and harvested recovered nuclei at P37-P44. `151 TH Prkcd Grin2c Glut` is a thalamic glutamatergic class, not a ventral-midbrain dopaminergic progenitor, not a roof-plate progenitor, and not a cortical-hem developmental population. Thus the main external prior is that acute partial `Lmx1a` loss in these recovered thalamic neurons should often be transcriptionally silent unless `Lmx1a` has an adult, cell-autonomous maintenance role in this exact class.

### Within-dataset analogs and counterexamples

The visible training perturbations most directly tied to the Lmx1a program were flat in the focal group:

| training target | focal `n_degs` | best focal FDR | matched perturbed nuclei | why compared |
|---|---:|---:|---:|---|
| `Lmx1b` | 0 | 1.000 | 271 | closest paralog and overlapping partner of Lmx1a in mesencephalic dopamine development |
| `Foxa2` | 0 | 1.000 | 213 | upstream/cooperating floor-plate and dopamine-specification factor |
| `Otx2` | 0 | 0.885 | 162 | upstream developmental factor in the Lmx1a/Wnt/Otx2 dopamine module |
| `Pitx3` | 0 | 0.751 | 184 | downstream dopamine-neuron differentiation and maintenance factor |
| `En1` | 0 | 1.000 | 242 | midbrain dopamine developmental/maintenance comparator |
| `En2` | 0 | 1.000 | 257 | paralogous Engrailed dopamine-development comparator |
| `Msx2` | 0 | 1.000 | 254 | marker/regulator around ventral mesencephalic progenitor programs |
| `Pbx1` | 0 | 1.000 | 200 | dopamine-lineage transcriptional cofactor comparator |
| `Ebf3` | 0 | 0.755 | 167 | adult dopamine-associated developmental marker from the same broader program |
| `Ret` | 0 | 0.607 | 240 | dopamine-neuron trophic/support marker, less direct than Lmx1b/Foxa2 |
| `Gfra1` | 0 | 1.000 | 190 | RET/GDNF pathway cofactor, a support-pathway counterexample |
| `Snca` | 0 | 1.000 | 187 | dopamine-neuron disease-associated counterexample rather than a transcription-factor analog |

Across all 23 assayed neuronal classes, the close visible set `Lmx1b`, `Foxa2`, `Otx2`, `Pitx3`, `En1`, `En2`, `Lhx3`, `Lhx4`, `Isl1`, `Dcc`, and `Phox2a` had zero FDR-significant genes; `Msx2` had only one DEG, and it was in `308 CB GABA`, not in the focal thalamic class. The July same-experiment corpus reported the same qualitative result for visible anchors: the Lmx1b report found that neither data-driven nearest signatures nor represented midbrain-dopamine network perturbations converged with Lmx1b; Foxa2's canonical dopamine branch was untested or off-lineage and measured nearby groups were flat; and Otx2 did not show the expected Otx2/Pitx3/Lmx1b dopamine or Otx2-Crx pineal programs. Those summaries agree with the direct Parquet counts and did not provide an Lmx1a-like positive state among the visible analogs.

I treated `Ctnnb1` as the main positive counterexample. Its focal count is high, 383 DEGs with a minimum FDR of `3.55e-25`, and Wnt/beta-catenin is upstream of Lmx1a in embryonic midbrain models. I did not transfer that high count to `Lmx1a`: beta-catenin has broad cadherin, Wnt-transcription, and adult neuronal functions that are not specific to the postmitotic Lmx1a dopamine/roof-plate program. The immediate, Lmx1-family and Foxa/Otx/Pitx visible comparators are the appropriate same-experiment analogs for an acute `Lmx1a` loss-of-function prediction, and they were silent.

### Zero/nonzero and count decision

The intervention is expected to reduce Lmx1a function only in sparse edited P16 neurons. In this thalamic glutamatergic class, there is no direct held-out signature and no raw baseline-expression input, but the visible members of the same embryonic dopaminergic patterning circuit and the closest paralog had no focal FDR-significant response despite adequate recovered-cell counts. The most plausible causal chain is therefore:

`Lmx1a CRISPR` -> little relevant direct molecular perturbation in mature 151 thalamic glutamatergic nuclei -> no coherent propagated Lmx1a/Foxa/Pitx/Engrailed program -> no broad survivor-state differential-expression signature at FDR 0.05.

I therefore predicted `0` DEGs for `Lmx1a`.

## Limits and uncertainty

This is a true extrapolation because the held-out `Lmx1a` perturbation and its expression signature are absent from the supplied inputs. The Parquet gives differential-expression statistics but not raw baseline expression, guide-level editing, pre-assay cell loss, or the guide-exposure denominator. The `Lmx1b`, `Foxa2`, `Otx2`, `Pitx3`, and `En1/En2` analogs strongly support silence of the canonical midbrain developmental module in this acute postnatal assay, but they are not `Lmx1a` itself. A very small Lmx1a effect in a rare 151 substate, or an adult Lmx1a role outside the canonical developmental literature, could be missed. The point prediction is thus a low-count prediction, rounded to the assay's most likely observed count, not a claim that Lmx1a is biologically irrelevant.
