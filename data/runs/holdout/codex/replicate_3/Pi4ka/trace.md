# Pi4ka DEG-count forecast

Target: `Pi4ka` in `151 TH Prkcd Grin2c Glut`.

Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the declared training-style count table.

Evidence used:

- Prediction-safe Pi4ka biology bundle, schema `expected-transcript-impact-agent-bundle-v1`, checksum `39c4e78139cdc7cb210164887458d0eb437cf9b39a9f3992448dd72b018c2bef`.
- Declared count table `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Declared Parquet `[local file: training_de_all_cell_groups.parquet]`, filtered only to training perturbations.
- Runtime profile comparison `profile_compare_pi_pathway.json` over visible phosphoinositide-pathway perturbations in `151 TH Prkcd Grin2c Glut`.

The bundle exposes no target outcome or labeled neighbor outcomes. It shows that Pi4ka is broadly present in the focal non-target thalamic nuclei: 22,732 of 23,679 cells express it, 96.0%, with mean raw UMI 4.61 and mean cp10k 2.86. The functional-stock card also argues that a successful P16 edit should substantially deplete the PI4KA/plasma-membrane PI4P functional pool by the P37-P44 harvest, because new PI4KA supply stops, adult induced loss can lower PI4KA protein over days in permissive tissues, and the PI4P product itself turns over within minutes once catalytic supply is gone. Those are upward bearings against a strict failed-target/null-expression call.

The same bundle also keeps the expected response bounded. Pi4ka is a plasma-membrane phosphatidylinositol 4-kinase, not a transcription factor, chromatin regulator, spliceosome component, ribosome/proteasome component, or other module that commonly drives the far right tail of the thalamic DEG-count distribution. The closest neural causal evidence is postnatal mouse Schwann cells rather than central thalamic neurons, adult systemic timing does not transfer directly to this population, selected lipid pools can be buffered, and survivor conditioning is unknown.

The declared training count table is very sparse for this exact endpoint:

```text
training perturbations: 1674
n_degs = 0: 1205
n_degs = 1: 276
positive n_degs: 469
median: 0
75th percentile: 1
90th percentile: 2
95th percentile: 18
```

I treated the nearest measured lipid-signaling perturbations as local scale references, not as labeled outcomes for Pi4ka. In `151 TH Prkcd Grin2c Glut` their counts were:

```text
Dgke    1
Inpp5k  0
Ocrl    0
Pi4kb   1
Pik3cb  0
Pik3r1  0
Pik3r2  0
Plcb1   0
Pld3    1
Synj1   1
```

The profile comparison of these ten visible training perturbations in the same thalamic class had six nodes with no significant feature and four nodes in the `1_to_9_significant_features` bin; the explicit count-table values show that the latter four were all singletons. Scanning the same genes across all other assayed classes found only singleton significant-feature calls for `Dgke`, `Pld3`, `Synj1`, and `Pi4kb`, supporting the view that this pathway neighborhood is generally transcriptionally quiet rather than only quiet in the focal class.

Synthesis: broad Pi4ka expression and likely functional depletion make an all-zero forecast too low. The relevant same-endpoint training biology is nevertheless almost entirely at 0-1 DEGs, and the global table places one DEG at the 75th percentile. I therefore forecast a singleton significant measured gene.

Predicted `n_degs`: 1
