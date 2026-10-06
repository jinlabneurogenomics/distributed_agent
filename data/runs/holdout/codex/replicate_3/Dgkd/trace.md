# Dgkd forecast for 151 TH Prkcd Grin2c Glut

## Target biology

The manifest target is `Dgkd` in `151 TH Prkcd Grin2c Glut`.  The biology
bundle maps this assignment to mouse Entrez 110524, current official `Dgkq`
/ DGKtheta, with `Dgkd` as the atlas target name.  DGKtheta is a DAG-to-PA
lipid kinase present at glutamatergic synapses.

The exact focal-population reach in the declared target bundle argues that the
perturbation is observable enough for a self-transcript signal: the `Dgkd`
feature is detected in 11,627 of 23,679 non-target nuclei in this class
(`49.10%`; mean raw UMI 0.752; pseudobulk 47.10 cpm).  The functional-stock
card also favors actual loss by harvest: new intact DGKtheta production should
stop after editing, full-length endogenous protein has an hours-scale cell-line
half-life, and the P16-to-P37/P44 experimental interval is 21-28 days.

I did not treat those facts as evidence for a large transcriptional response.
The direct mouse neuronal phenotype is slower activity-evoked synaptic-vesicle
endocytosis in cultured cortical/hippocampal neurons; no acute postnatal
thalamic loss experiment pins that physiology to a durable basal nuclear RNA
state.  Other DGK isoforms also remain available, and the perturbation is a
synaptic lipid-enzyme loss rather than a direct RNA-processing, chromatin, or
proteostasis lesion.

## Same-assay training scale

The declared count table for the exact focal class contains 1,674 training
targets.  It is heavily zero-inflated on the requested endpoint:

| statistic | n_degs |
| --- | ---: |
| zero-count targets | 1,205 |
| targets with exactly 1 DEG | 276 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |

The very large tail is dominated by global cellular regulators such as `Uba5`,
`Tpr`, `Sin3a`, spliceosome/RNA-binding factors, proteasome factors, and
transcriptional regulators.  DGKtheta's expected operation is much closer to
the buffered lipid-signaling and synaptic examples than to that high-tail class.

## Endpoint-matched comparators

From the declared `n_degs` table and the training Parquet restricted to
`group_name == "151 TH Prkcd Grin2c Glut"`:

| comparator | rationale | n_degs at BH p_adj < 0.05 |
| --- | --- | ---: |
| `Dgke` | only represented DGK-family perturbation in the focal-class training table | 1 |
| `Pik3r1`, `Pik3r2`, `Pik3cb` | receptor-proximal PI3K lipid-signaling nodes | 0, 0, 0 |
| `Plcb1` | DAG/IP3-producing PLC beta node upstream of PKC | 0 |
| `Prkca`, `Prkcg` | DAG/Ca-sensitive PKC relatives | 0, 1 |
| `Synj1`, `Dnm1`, `Syp`, `Dlg4` | synaptic vesicle/endocytic or synaptic scaffold genes with strong physiological expectations | 1, 1, 1, 1 |
| `Cltc`, `Stxbp1`, `Dlgap4`, `Shank3` | stronger synaptic boundary cases in this class | 3, 1, 2, 2 |

The Parquet rows show why the small counts matter.  `Dgke`'s lone significant
row in this class is `Dgke` itself (`logfoldchanges = -0.586`,
`pvals_adj = 5.97e-08`), and the same self-only pattern holds for `Synj1`,
`Dnm1`, `Syp`, `Dlg4`, `Stxbp1`, `Syn1`, and `Grin2a`.  `Plcb1` and the class
IA PI3K targets are fully zero in the focal class.  The same-experiment corpus,
which is an interpreted surface over these measurements rather than an
independent replicate, likewise annotates `Dgke` as lacking a robust downstream
steady-state neuronal transcriptional output and annotates `Dnm1`, `Synj1`,
`Syp`, `Dlg4`, and `Pik3r1` as buffered or transcriptionally flat despite known
synaptic or signaling biology.

## Point synthesis

I expect `Dgkd` loss to be realized by harvest and to be present enough in this
thalamic glutamatergic class for a target-transcript row to survive BH
correction, as in `Dgke`, `Dnm1`, `Synj1`, `Syp`, and `Dlg4`.  I do not expect a
multi-gene downstream state: the closest lipid-signaling and synaptic
comparators in the same endpoint are almost all 0-1 DEG perturbations, and the
physiological DGKtheta evidence is not tied to a broad basal snRNA-seq module in
postnatal thalamic neurons.

The resulting direct forecast is therefore a single significant gene, most
likely the perturbed transcript itself:

`predicted_n_degs = 1`
