# Trace

## Question and resolved ambiguities

I predicted the held-out `n_degs` for `Clcn5` in `151 TH Prkcd Grin2c Glut` neurons. The endpoint is the count of measured genes with Wilcoxon Benjamini-Hochberg adjusted `pvals_adj < 0.05` in the held-out `Clcn5` perturbation. The perturbation itself was absent from both the training DEG-count table and the differential-expression Parquet, so the prediction has to transfer from non-held-out perturbations.

I treated `151 TH Prkcd Grin2c Glut` as the exact Allen-atlas thalamic glutamatergic class named in the task. I did not use the unranked one-row request file order as quantitative supervision; it only determined the output row order. Because this is a scalar count prediction rather than a ranked candidate task, I used direct queries against the declared Parquet and did not invoke the ranked-feature workbench, predictive graph review, or ordering validation capabilities.

## Sources used

- Declared training endpoint: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression table: `training differential-expression dataset`.
- Requested-target manifest: `single-target request for Clcn5`.
- Run-local dataset portrait and coverage summaries in `codex_runtime/pipeline`.
- Internal same-experiment corpus: PerturbAI July 260713 sourceguard 1773 v1 reports, especially the packaged `Clcn3`, `Clcn4`, and `Rab7` reports.
- External literature from PubMed for CLC exchanger biology and disease models:
  - Accardi and Miller 2004, *Nature*, DOI: 10.1038/nature02314, PMID: 14985752.
  - Scheel et al. 2005, *Nature*, DOI: 10.1038/nature03860, PMID: 16034422.
  - Piwon et al. 2000, *Nature*, DOI: 10.1038/35042597, PMID: 11099045.
  - Stobrawa et al. 2001, *Neuron*, DOI: 10.1016/s0896-6273(01)00189-1, PMID: 11182090.
  - Gunther et al. 2002, *Pflugers Archiv*, DOI: 10.1007/s00424-002-0950-6, PMID: 12548389.
  - Guzman et al. 2017, *Journal of Biological Chemistry*, DOI: 10.1074/jbc.M117.801951, PMID: 28972156.
  - Jentsch and Pusch 2018, *Physiological Reviews*, DOI: 10.1152/physrev.00047.2017, PMID: 29845874.
  - Weinert et al. 2020, *EMBO Journal*, DOI: 10.15252/embj.2019103358, PMID: 32118314.

## Computation over the training data

I first summarized the focal-cell training-count distribution to calibrate scale. It is highly zero-inflated: among 1,674 non-held-out training perturbations the median was 0 DEGs, the 75th percentile was 1 DEG, 1,205 perturbations were zero, the 95th percentile was 18, and only a few perturbations were hundreds to thousands of DEGs.

I then queried the focal class for assayed chloride/endolysosomal comparators:

| training target | focal `n_degs` at FDR 0.05 | focal perturbed nuclei | closest focal row |
|---|---:|---:|---|
| `Clcn3` | 0 | 91 | best adjusted P = 0.619 for the `Clcn3` self row |
| `Clcn4` | 1 | 169 | adjusted P = 6.72e-11 for the `Clcn4` self row |
| `Atp6v0a1` | 1 | 197 | adjusted P = 4.52e-12 for the `Atp6v0a1` self row |
| `Atp6v1a` | 0 | 76 | minimum adjusted P = 0.855 |
| `Atp6v1b2` | 0 | 32 | minimum adjusted P = 1.000 |
| `Atp6v1e1` | 0 | 52 | minimum adjusted P = 1.000 |
| `Lamp2` | 0 | 203 | minimum adjusted P = 0.0537 |
| `Vps41` | 0 | 159 | minimum adjusted P = 0.204 |
| `Washc4` | 0 | 76 | minimum adjusted P = 1.000 |
| `Rab7` | 501 | 215 | minimum adjusted P = 1.06e-16 |
| `Vps35` | 17 | 133 | minimum adjusted P = 3.15e-6 |
| `Atp6ap2` | 2 | 116 | minimum adjusted P = 1.90e-28 |
| `Cltc` | 3 | 32 | minimum adjusted P = 0.0424 |

The `Clcn4` and `Atp6v0a1` singleton counts are on-target transcript calls, not a broad downstream state. In the Parquet, `Clcn4` had only its own transcript significant in `151 TH Prkcd Grin2c Glut`; the next-best rows had adjusted P = 1.0. `Clcn3` had no significant row at all in the focal class. Across the full atlas, the internal corpus also called `Clcn3` a pan-neuronal FDR-null surface and `Clcn4` a pan-measured weak/null perturbation with no downstream gene at FDR < 0.10.

I used `Rab7` and `Vps35` as counterexamples rather than direct analogs. They show that the assay can see a late-endosome/lysosome/sterol or stress response in this focal class when the perturbation is strong enough; `Rab7` caused 501 DEGs at FDR 0.05 in the exact training endpoint. However, broad late-endosomal trafficking blockade is not the same intervention as loss of one endosomal ClC exchanger, and the much more direct `Clcn3` and `Clcn4` perturbations did not phenocopy `Rab7`.

## Target-specific reasoning

### Clcn5

`Clcn5` encodes ClC-5, one of the mammalian intracellular CLC transporters. Work on bacterial ClC and endosomal mammalian ClC-4/ClC-5 established that this branch behaves as coupled chloride/proton exchange rather than as a simple passive chloride channel (Accardi and Miller 2004; Scheel et al. 2005). ClC-5 is best characterized in renal proximal-tubule apical endosomes: `Clcn5` knockout mice have impaired receptor-mediated and fluid-phase endocytosis and model Dent disease (Piwon et al. 2000; Gunther et al. 2002). Jentsch and Pusch 2018 place ClC-5 in the intracellular ClC-3 to ClC-7 exchanger group that shapes vesicular ion composition, endocytosis, and lysosomal function.

The most biologically relevant in-dataset analogs are `Clcn3` and `Clcn4`, not `Rab7`. `Clcn3` is a neuronal vesicular/endosomal ClC whose constitutive disruption causes postnatal hippocampal and retinal neurodegeneration in mice (Stobrawa et al. 2001). `Clcn4` is another endosomal ClC; ClC-3 promotes ClC-4 endosomal sorting through preferential ClC-3/ClC-4 association (Guzman et al. 2017), and ClC-4 can compensate for exchange-uncoupled ClC-3 in vivo (Weinert et al. 2020). Those are stronger mechanistic neighbors for a single-gene `Clcn5` loss-of-function perturbation than generic lysosomal genes because they share transporter family, vesicular ion-homeostasis biology, and partial redundancy among endosomal CLCs.

The focal training counts for those analogs were at the assay floor: `Clcn3` caused 0 DEGs and `Clcn4` caused 1 DEG. The expression-pattern evidence also argued against a hidden ClC-family transcriptional module: the focal `Clcn3` signature had no FDR-significant genes, while the one focal `Clcn4` FDR hit was the `Clcn4` self transcript, with all next-best rows at adjusted P = 1.0. The internal same-experiment reports generalized that observation across neuronal classes: `Clcn3` had no downstream FDR < 0.10 effects across 19 measured groups, and `Clcn4` had no downstream FDR < 0.10 effects across 22 measured groups even though its own RNA was significantly reduced in the focal thalamic class.

I therefore predict that `Clcn5` will be nonzero only if its own RNA or a single secondary endosomal marker crosses FDR. Its renal endocytic role creates a prior that the protein is real biology, but the focal assay perturbs postmitotic thalamic glutamatergic neurons rather than proximal tubule, and the closer neuronal CLC homologs are buffered in this acute mosaic P16-to-P37/44 nuclear-RNA readout. V-ATPase subunits were also zero or singleton in the same focal endpoint (`Atp6v1a`, `Atp6v1b2`, and `Atp6v1e1` at 0; `Atp6v0a1` at 1 self-dominated DEG), so a narrow exchanger/vesicle-acidification lesion has not usually produced a detectable downstream state here.

`Rab7` is the main counterexample. The same focal class can mount a large lysosomal/autophagy/sterol/proteostasis response when a late-endosome master regulator is perturbed: `Rab7` had 501 FDR 0.05 DEGs. I did not transfer that count to `Clcn5` because Rab7 loss blocks a broad trafficking hub, while `Clcn5` is a single CLC exchanger and the direct CLC homologs did not trigger the Rab7-like program. Likewise, `Vps35` had a smaller 17-DEG focal response, but retromer cargo sorting is upstream of many membranes and is mechanistically less specific than `Clcn3`/`Clcn4`.

My point estimate is 0 DEGs. It is essentially a floor call: the likely outcome is no FDR-significant row, with 1 also plausible if a self-transcript or isolated vesicle gene crosses the threshold. I chose 0 rather than 1 because the closest assayed paralogs average only 0.5 DEGs and because the one `Clcn4` count was not a downstream transcriptional effect.

## Limits

This is an extrapolation from homologs and endosomal pathway perturbations, not a direct `Clcn5` measurement. DNA indels, protein loss, endosomal pH, endocytosis, lysosomal chloride, and cell survival were not measured in the held-out target. The PerturbAI corpus reports are the interpreted layer of the same experiment as the Parquet, so they helped select and interpret analogs but do not constitute independent replication. Finally, the result is specific to sparse AAV-PHP.eB CRISPR in P16 postmitotic NeuN-positive mouse neurons assayed by snRNA-seq 3-4 weeks later; it does not test germline `Clcn5` loss, kidney proximal tubule, retina/olfactory tissues, or combined `Clcn3`/`Clcn4`/`Clcn5` perturbations.
