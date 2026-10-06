# Rab28 direct n_degs forecast

## Endpoint

- Target: `Rab28`.
- Population: `151 TH Prkcd Grin2c Glut`.
- Quantity predicted: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- I treated the training count CSV and training DE Parquet as the same Perturb-seq experiment, not as independent replication, and used the held-out `Rab28` biology bundle only as a target prior. I did not use a `Rab28` DE signature or `Rab28` count outcome.

## Biology that set the upward prior

Source: `biology_bundles/Rab28.json`, sha256 `c3ff69c95aae39634e9dab3754cc9eca9f251774c760a4d700192ffcd6347371`, served by `characterization_bundle(target="Rab28", view="biology")`.

- The exact focal-population expression reach is real: in matched non-target `151 TH Prkcd Grin2c Glut` nuclei, `Rab28` was detected in 20,462 / 23,679 cells, or 86.414%, with mean raw UMI 2.309, mean log1p(CP10K) 0.806, and pseudobulk CPM 144.698. This says the transcript is available in the assayed thalamic population; it does not measure editing efficiency.
- The functional-stock adjudication concluded that a P16 disruptive edit likely substantially depleted operative Rab28 by P37-P44, because Rab28 is a dynamic prenylated trafficking GTPase rather than a permanent installed state and the nearest mature-neuronal proteome proxy has a 5.4-day median half-life.
- The biological phenotype prior is positive but distant: germline Rab28 loss has a reproducible postnatal mouse retinal-neural phenotype involving cone outer-segment disc shedding and retinal degeneration, and orthologous RAB-28 participates in ciliary intraflagellar transport. The same bundle left adult thalamic Rab28 demand unresolved and noted that the retinal and nematode ciliary evidence does not demonstrate a comparable operation in thalamic neurons.

## Training evidence that set the scale

Source count table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.

- The focal-class training distribution has 1,674 targets; 1,205 are exactly zero. Its median is 0, the 75th percentile is 1, the 90th percentile is 2, and the high arithmetic mean of 14.05 is driven by a small heavy tail.
- I used ciliary and IFT perturbations represented in the count table as the closest endpoint-scale analogues to Rab28's biology. Their `151 TH Prkcd Grin2c Glut` counts were almost all null: `Bbs5=0`, `Cep290=0`, `Dync2h1=0`, `Dync2i1=0`, `Ift43=0`, `Ift81=0`, `Ift88=0`, `Kif3b=0`, `Ttc21b=0`, and `Ttc8=1`, for 9 / 10 zeros and a mean of 0.1.
- A small-GTPase/neuron-traffic check pointed the same way for the nearer non-lysosomal genes: `Arl2bp=0`, `Rab18=0`, `Rab27a=0`, `Rab3gap1=0`, and `Rab3gap2=0`, with `Arl3=1`. I did not transfer the large `Rab7=501` count, because the same-experiment corpus places Rab7 in a broad late-endosomal/lysosomal, catabolic-stress state rather than the specialized Rab28 ciliary/photoreceptor axis.

Selected exact Parquet slice: `[local file: training_de_all_cell_groups.parquet]`, restricted to the selected training genes in `151 TH Prkcd Grin2c Glut`.

- Each selected comparator had 17,259 focal-class measured-gene rows. The ciliary/IFT genes above had no significant focal-class genes except `Ttc8`, which had one significant feature, and the non-lysosomal small-GTPase genes were also zero or one.
- The packaged same-experiment corpus has the same qualitative boundary: `Ift88:F003` states that represented cilium-related perturbations converged mainly by being transcriptionally buffered rather than by inducing a shared IFT-B knockout transcriptome; `Bbs5:F003` states that BBSome/ciliary relatives did not phenocopy Bbs5 and mostly produced isolated one-gene effects; `Arl3:F003` states that represented ciliopathy comparators did not phenocopy Arl3 in the postnatal neuronal snRNA readout.

## Forecast

The target is expressed and the edited stock should be at least partly depleted, so a response is biologically possible. The endpoint-scale comparators most tied to the Rab28 prior, however, show that ciliary genes were generally buffered in this exact postnatal neuronal readout, including in this high-yield thalamic glutamatergic class. I therefore kept the forecast at the ciliary-comparator mode rather than pulling it toward the heavy-tailed genome-wide mean.

Predicted `n_degs`: **0**.
