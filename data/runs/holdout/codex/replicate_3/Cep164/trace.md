# Cep164 `n_degs` forecast

## Target and endpoint

- Held-out target: `Cep164`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: count of measured genes in this population with BH-adjusted Wilcoxon `p < 0.05`.
- Declared direct measurements: the focal-class training count table and the held-in differential-expression Parquet. `Cep164` had zero rows in the training Parquet, so no target signature or target DEG count was used.

## Target biology

- The canonical `Cep164` biology bundle, served with `characterization_bundle(target="Cep164", view="biology")`, places CEP164 at the basal-body distal appendage where it supports membrane docking and IFT-B recruitment/stabilization.
- Exact in-assay reach was moderate rather than absent: in matched non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Cep164` was detected in 12,103 of 23,679 nuclei, or 51.11%, with pseudobulk CPM 48.53.
- The functional-stock adjudication concluded that stock in edited, expressing cells is likely substantially depleted by P37-P44, but with transfer uncertainty because the direct clock is post-ciliogenesis photoreceptor deletion and photoreceptor cilia have far higher renewal demand than ordinary thalamic primary cilia.
- The selected same-experiment corpus release contained no `Cep164` target report, Finding, or Claim, so the forecast came from same-process held-in perturbations rather than a packaged target observation.

## Training evidence

- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contains 1,674 held-in targets. Its distribution is sparse: median `n_degs` is 0; 1,205 of 1,674 targets are 0; the mean is 14.05 because of a small upper tail.
- Manually selected primary-cilium, IFT, dynein-2, BBSome, transition-zone, basal-body, and ciliary Hedgehog comparators were near-null in the focal endpoint:

  `Adcy3 0; Arl3 1; Bbs5 0; Cep120 0; Cep290 0; Dync2h1 0; Dync2i1 0; Gli2 0; Ift43 0; Ift81 0; Ift88 0; Kif3b 0; Lztfl1 0; Pkd1 0; Rpgrip1l 0; Sclt1 0; Smo 0; Ttc21b 0; Ttc8 1`.

- The closest structural cohort to `Cep164` excluded receptor/readout genes and retained `Bbs5`, `Cep120`, `Cep290`, `Dync2h1`, `Dync2i1`, `Ift43`, `Ift81`, `Ift88`, `Kif3b`, `Lztfl1`, `Rpgrip1l`, `Sclt1`, and `Ttc21b`; all 13 had exactly 0 focal-class DEGs, mean 0.
- Adding the singleton `Ttc8` to those 13 structural comparators gave 1 DEG across 14 perturbations, arithmetic mean 0.071 and log1p-mean back-transform 0.051. Thus even a slightly wider structural-ciliary pool still rounds to 0.
- Direct Parquet filtering verified a full 17,259-gene row block for each ciliary comparator above. Among the 13 zero-count structural comparators, only three rows even reached `pvals_adj < 0.25` in the focal class: `Dennd4b` after `Rpgrip1l`, `Lhfp` after `Lztfl1`, and `Ptprn` after `Bbs5`.
- Same-experiment Findings for `Cep120:F002`, `Cep290:F003`, `Dync2h1:F003`, `Ift81:F002`, `Ift88:F003`, and `Kif3b:F002` independently summarize the represented ciliary machinery perturbations as flat or singleton responders in the postnatal neuronal snRNA readout. They reinforce that the null is a pathway-class property of these assayed perturbations, not a single anomalous guide set.
- A profile comparison restricted to 19 ciliary/Hedgehog comparators in `151 TH Prkcd Grin2c Glut` found 17 with no significant features. Inspection of 50 signed-profile pairs between `Cep290`, `Ift88`, `Dync2h1`, `Kif3b`, `Bbs5` and ten peer ciliary nodes showed all Pearson/cosine similarities near zero, no shared significant positive features, and no shared significant negative features.

## Synthesis

`Cep164` is expressed in the focal nuclei and is expected to matter at the ciliary base by harvest, so I did not treat it as an unexpressed or unrealized perturbation. The endpoint, however, is a survivor-conditioned nuclear RNA DEG count, and the held-in loss-of-function perturbations that most directly disrupt cilium construction, IFT, dynein-2 transport, BBSome trafficking, transition-zone gating, and Hedgehog ciliary signaling are essentially silent in this same focal class. Because the zero-count structural comparators are both mechanistically closer to CEP164 than the strong global RNA-processing/proteostasis responders and flat down to relaxed BH thresholds, the biologically weighted forecast is the mode of that local cohort rather than the all-target mean.

Predicted `n_degs`: **0**.
