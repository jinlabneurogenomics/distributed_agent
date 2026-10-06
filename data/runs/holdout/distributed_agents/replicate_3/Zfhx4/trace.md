# DEG-count prediction trace

## Question and setup

I interpreted the task as a point prediction of the focal-cell endpoint

`n_degs = count(pvals_adj < 0.05)`

for each gene in `268_Zfhx4.csv`, using the non-held-out perturbations in the parquet and the focal `151 TH Prkcd Grin2c Glut` training counts. The requested manifest contained a single held-out target, `Zfhx4`.

The perturbation is acute sparse AAV CRISPR loss of function from P16 to P37-P44 in NeuN+ postmitotic brain nuclei. I therefore treated embryonic germline phenotypes, neural-progenitor cell culture phenotypes, and tumor-cell phenotypes as evidence for possible molecular partners but not as direct estimates of the postnatal thalamic DEG count.

## Sources used

- Focal training endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Full DE table: `[local file: training_de_all_cell_groups.parquet]`
- Held-out manifest: `[local file: 268_Zfhx4.csv]`
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, via `target_context`, `search_claims`, and focal profile-comparison tools.
- PubMed literature on ZFHX4 function and interacting proteins.

The Distributed Agents corpus had no direct `Zfhx4` target node, so no hidden Zfhx4 expression signature or curated Zfhx4 neighborhood was available. I used its same-experiment summaries for observed neighboring perturbations, especially `Zfhx2`, `Chd4`, and `Zfp423`.

Key external papers:

- Hemmi et al. 2006, DOI `10.1248/bpb.29.1830`: cloned human `ZFHX4`; reported the four-homeodomain/22-zinc-finger architecture, similarity to `ATBF1/ZFHX3`, adult brain expression, and induction during neuronal differentiation of P19 cells.
- Chudnovsky et al. 2014, DOI `10.1016/j.celrep.2013.12.032`: found that ZFHX4 maintains glioblastoma tumor-initiating and human neural-precursor phenotypes, physically interacts with CHD4, and overlaps CHD4-bound regulatory programs.
- Nakamura et al. 2021, DOI `10.1038/s42003-021-02793-9`: showed Zfhx4 interaction with Osterix/Sp7 and Runx2 in endochondral ossification.
- Liu et al. 2024, DOI `10.1002/dvdy.740`: found conserved mouse/zebrafish craniofacial expression and skeletal defects after Zfhx4 loss.
- Perez Baca et al. 2025, DOI `10.1016/j.ajhg.2025.04.008`: defined human ZFHX4 loss-of-function as a neurodevelopmental disorder, reported increased expression during human brain development/neuronal differentiation, and found promoter binding near embryonic, neuronal, and axonal-development genes.

## Computational checks over the DE table

I first read the requested manifest and training count CSV to identify which candidate analogs were actually measured as training perturbations in the focal cell group. The closest measured ZFHX-family gene was `Zfhx2`; `Zfhx3` was absent.

For biologically nominated targets, I then read only focal rows from the 616M-row parquet using PyArrow filters equivalent to:

```python
pd.read_parquet(
    de_parquet,
    filters=[
        ("group_name", "==", "151 TH Prkcd Grin2c Glut"),
        ("gene_target", "in", candidate_targets),
    ],
)
```

I counted `pvals_adj < 0.05` rows per target and inspected the leading significant genes. I also ran a focal `profile_compare` over 16 candidates using `logfoldchanges` as the signed profile value and `pvals_adj < 0.05` as the significance threshold; that supplied FDR-overlap evidence between the observed analogs.

## Same-experiment analogs and counterexamples

### ZFHX-family paralog

`Zfhx2` was the only represented `Zfhx` perturbation. It had `0` DEGs in `151 TH Prkcd Grin2c Glut`. The Distributed Agents corpus summarized its central-brain surface as essentially flat: one weak `Nt5c3` up-regulation at FDR 0.10 in `009 L2-3 IT PIR AON ENT Glut`, no broad Zfhx2 regulon, no meaningful score-neighbor module, and no compensatory `Zfhx3`/`Zfhx4` mRNA rebound. This is not a perfect phenocopy because ZFHX2 is better tied to peripheral DRG nociceptor biology than ZFHX4, but it shows that an acute ZFHX-family TF perturbation is not automatically visible in sampled postnatal central neurons.

### CHD4 / NuRD-adjacent branch

The strongest literature link to a measured focal response is ZFHX4-CHD4: Chudnovsky et al. reported physical and genomic cooperation between ZFHX4 and CHD4 in glioblastoma tumor-initiating cells and neural precursors.

In the focal training data, `Chd4` itself had `100` DEGs, led by `Begain` up, `Cpne7` down, `Pygm` up, `Bcan` up, `Cacng7` up, `Cyp46a1` down, `Abhd12b` up, and `Msra` up. Distributed Agents described this as a selective 151-thalamic CHD4 response with channel/calcium, adhesion/extracellular-matrix, and metabolic/redox branches.

I did not transfer the full `Chd4` breadth to `Zfhx4`, because all of the same-experiment boundaries point to target-selective NuRD behavior:

- `Mbd2`: `0` focal DEGs.
- `Gatad2b`: `1` focal DEG, its own transcript.
- `Casz1`: `0` focal DEGs, despite developmental/tumor NuRD recruitment evidence.
- `Phf6`: `0` focal DEGs.
- `Zmynd8`: `74` focal DEGs, but a different thalamic chromatin response led by `Ptgds`, `Msra`, `Lhcgr`, `Capn3`, and `Abhd12b`, not a general NuRD phenocopy.

The Distributed Agents `Chd4` claims explicitly state that represented NuRD/MBD-adjacent perturbations do not collapse into a single neuronal mRNA loss signature, that `Gatad2b` and `Mbd2` did not phenocopy the `Chd4` thalamic program, and that even represented chromatin repressors produced target-selective, non-interchangeable surfaces. The focal profile comparison matched that statement: the flat MBD/NuRD candidates shared no FDR-significant 151 features with `Chd4`, whereas only known CHD4-associated responders such as `Adnp` and `Zmym2` had small same-direction intersections.

### Other neural zinc-finger / developmental-TF controls

`Zfp423` was a useful counterexample rather than a direct analog. It is a neural developmental zinc-finger cofactor with a large focal response (`150` DEGs; `Grid2ip` and `Cd47` down, `Ntsr1`, `Kcnab3`, and `Nptxr` up), but Distributed Agents found that its obvious relatives did not phenocopy it. The close paralog `Zfp521` had `0` focal DEGs; its EBF, BMP-SMAD, RA-receptor, ZIC, and `Chd4` comparators were absent, sparse, or weakly overlapping (`Ebf1`, `Ebf2`, `Ebf3`, `Atoh1`, `Smad1`, `Smad3`, `Smad4`, `Smad9`, `Rarb`, `Rarg`, `Zic2`, `Zic3`, `Zic4` were all `0`; `Smad2` had `1`; `Zic1` had `2`). This argued against using broad "large zinc-finger developmental regulator" behavior as a generic nonzero rule for `Zfhx4`.

The focal endpoint was also near zero for many postnatal developmental TFs and craniofacial or lineage regulators: `Runx2` `0` and `Sp7/Osterix` `0` despite the published Zfhx4 interaction in bone; `Foxp2` `0`, `Tbr1` `0`, `Pax6` `0`, `Satb2` `0`, `Sox4` `0`, `Sox11` `0`, and `Sox2` only `2`. These are not mechanistic matches to `Zfhx4`, but they calibrate the assay: a gene can be an important developmental TF and still yield no FDR-scale acute RNA response in this postmitotic thalamic population.

## Zfhx4 prediction

External biology says that `Zfhx4` is a transcription factor relevant to neuronal differentiation and neurodevelopment, but the direct evidence is mostly from neural progenitors, developing craniofacial/endochondral tissue, zebrafish/mouse embryogenesis, or glioma stem-like cells. The strongest possible focal analog, `Chd4`, is active, yet same-experiment NuRD partners and CHD4-adjacent developmental cofactors are mostly flat or non-phenocopying. The closest family member in the observed screen, `Zfhx2`, is `0` in the focal group and lacks a central-brain regulon. I therefore predict that partial acute `Zfhx4` loss in P16-edited `151 TH Prkcd Grin2c Glut` neurons will fall below the FDR 0.05 threshold, with no measured DEGs.

Prediction: `Zfhx4 -> 0`.

## Limits

`Zfhx4` itself was completely held out, `Zfhx3` was not a training perturbation, and the Distributed Agents corpus had no `Zfhx4` node, so the estimate extrapolates from an imperfect set of neighbors. `Chd4` is a core remodeler with functions beyond ZFHX4, while `Zfhx2` has DRG/nociceptor biology that is not ZFHX4 biology. A small `Zfhx4`-specific postmitotic regulon, if present, could land just above FDR even though the analogs suggest buffering; the prediction should be read as a zero/nonzero call for this particular assay and power regime, not as a claim that ZFHX4 is biologically unimportant in brain development.
