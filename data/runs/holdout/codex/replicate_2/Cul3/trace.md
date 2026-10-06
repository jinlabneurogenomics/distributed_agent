# Cul3 DEG-count forecast

## Endpoint and target

- Target: `Cul3`, the one row in the declared holdout manifest.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counting measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`.
- Measurement context: P16 mouse neuronal CRISPR/Cas9 loss of function, harvested at P37-P44 from survivor-conditioned nuclei.
- Declared exact target reach: the in-assay non-target thalamic population measured `Cul3` in 21,435 of 23,679 nuclei, 90.5% of cells, with mean raw UMI 2.97 and mean log1p CP10K 0.953. This supports transcript availability in the focal class, but I did not use target self-knockdown as an editing or response-strength proxy.

## Biology used for the forecast

The prediction-safe biology bundle says CUL3 is the cullin scaffold of BTB-CUL3-RBX1 ubiquitin ligases, so a disruptive edit should stop new intact CUL3 production across many adaptor-specific ligase complexes. That makes `Cul3` more consequential than a single redundant adaptor. The same bundle also adjudicates functional stock at the 21-28 day endpoint as only `partially_depleted_or_leading_edge`: pre-edit CUL3 protein and preassembled complexes are not directly inactivated by the edit, there is no absolute neuronal turnover measurement at the P16-to-P37/P44 interval, and the closest postnatal neural deletion data come from forebrain excitatory neurons at adult endpoints rather than juvenile thalamus. The net prior is therefore a real but muted postnatal effect.

## Training measurements

The declared 151-class training count table contains 1,674 non-held-out perturbations. It is extremely sparse:

- 1,205/1,674 have `n_degs = 0`;
- the median is 0 and the 75th percentile is 1;
- 366 have 1-10 DEGs;
- 45 have 11-50 DEGs;
- 58 have more than 50 DEGs;
- the mean is 14.1 and is dominated by rare outliers up to 2,677.

The highest ubiquitin/proteostasis comparators in `151 TH Prkcd Grin2c Glut` are not generic E3-ligase analogs. `Uba5` had 2,677 DEGs and `Ufc1` had 572 DEGs in the same class; their same-experiment Finding summaries identify them as a UFMylation E1/E2 pair with organelle and proteostasis stress. `Psmb4` had 742 DEGs and `Psmc1` had 430; the same-experiment summaries identify those signatures as direct 20S/19S proteasome bounce-back plus integrated-stress, heat-shock, autophagy/lysosome, and apoptotic-state programs. The 151 profile comparison confirmed the two direct proteasome hits and the two UFMylation hits were internally coherent but did not define a single transferable UPS scale: among `Uba5`, `Ufc1`, `Psmb4`, `Psmc1`, `Usp48`, `Ube3a`, and `Klhl7`, the strongest positive significant overlap was the pathway-specific `Uba5`-`Ufc1` pair, while null genes still showed high whole-profile cosine because they had no significant feature set to overlap.

Lower-burden E3 and UPS pathway members are more informative for `Cul3` than the core proteasome/UFMylation extremes:

- `Usp48`: 10 DEGs in 151, and the corpus describes a compact noncanonical thalamic module rather than canonical UPR, ISR, autophagy, p53, Hh, or NF-kB output.
- `Marchf6`: 14 DEGs in 151, with a compact sterol/SREBP2 module.
- `Mib1`: 27 DEGs in 151, with a sterol module uncoupled from canonical Notch.
- `Huwe1`: 158 DEGs in 151, but its Finding summaries explicitly state that the Huwe1 response was not a generic HECT/E3-ligase phenotype and did not recover proteasome bounce-back or UPR/ISR programs.
- `Vcp`: 2 DEGs at the requested FDR threshold; its same-experiment summary calls acute `Vcp` loss sparse and pathway-uncoupled despite obvious proteostasis biology.
- `Sqstm1`, `Uchl1`, `Fbxw7`, `Fbxo11`, and `Hectd4`: 1 DEG each in 151.
- `Ube3a`, `Herc1`, `Herc2`, `Hecw2`, `Rnf216`, `Rnf220`, `Nfe2l1`, `Nfe2l2`, and `Atf6`: 0 DEGs in 151.

The represented BTB/Kelch/adaptor-like neighbors were mostly quiet as well: `Klhl7`, `Klhl20`, `Kctd16`, `Kctd8`, `Kbtbd7`, and `Btbd9` were all zero in 151; `Kctd1` had 2; `Gigyf2` had 17. `Zbtb7a` was a large 841-DEG outlier but is a transcription-factor perturbation with a broad response, not a cullin-scaffold control.

## Synthesis

I did not average all UPS genes, because the largest responses come from direct proteasome or UFMylation disruption and same-experiment Findings specifically separate those programs from basal E3, adaptor, NRF2, VCP, autophagy, and UPR perturbations. I also did not put all weight on the mostly null adaptor genes, because `Cul3` is the shared CUL3-RBX1 scaffold, is detected in nearly every focal thalamic non-target nucleus, and should affect many BTB-adaptor complexes once new synthesis stops.

The best scale is a compact 151-specific response like `Usp48`, `Marchf6`, `Mib1`, and `Gigyf2`, discounted below `Mib1` because CUL3 functional stock is likely only partially depleted by harvest. I therefore forecast a low double-digit count and use **12** as the point estimate.
