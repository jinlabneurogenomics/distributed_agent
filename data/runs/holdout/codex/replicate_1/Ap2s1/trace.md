# Ap2s1 n_degs forecast for 151 TH Prkcd Grin2c Glut

## Declared target

- Target: `Ap2s1`
- Endpoint: `n_degs`, the count of measured genes with Wilcoxon BH-adjusted `p < 0.05` in `151 TH Prkcd Grin2c Glut`
- The Ap2s1 perturbation contrast and its endpoint value were absent from the declared count table and DE Parquet used here.

## Evidence used

### Biology-only Ap2s1 bundle

The canonical target bundle identified AP2S1 as the sole sigma subunit of the heterotetrameric AP-2 adaptor complex, used in clathrin-dependent cargo selection and synaptic-vesicle membrane recycling. The stock adjudication favored a real perturbation by harvest: AP-2 is a dynamic, repeatedly recruited complex; P16 editing should stop new AP2S1 supply; the P37-P44 readout is 21-28 days later; and a same-complex Ap2m1 neural loss model altered mature neurons within days. This was still only partial evidence because the days-scale postmitotic timing evidence came from Ap2m1 rather than Ap2s1, and no Ap2s1 protein-depletion time course in postmitotic thalamic neurons was available.

The exact focal expression reach argues that Ap2s1 was available to the assay, but not massively or uniformly so: in the `151 TH Prkcd Grin2c Glut` non-target population, Ap2s1 was detected in 13,203 of 23,679 nuclei, 55.76%, with mean 0.908 raw UMI and pseudobulk 56.9 CPM.

### Same-experiment corpus context

The selected corpus had no Ap2s1 target report, Claim, or explicit reference record, so it supplied no hidden Ap2s1 measurement.

Clathrin and AP-adaptor Claims were the most relevant packaged interpretation:

- `claim:6a51d47ce98166a0f24f` concluded that represented AP-adaptor perturbations and Prepl are not transcriptionally equivalent to bulk clathrin-coated-vesicle failure in juvenile CNS neurons.
- `claim:97fd9a4f6d91daf7bdbb` concluded that responses to represented AP-adaptor perturbations are target-specific rather than a generic AP-family or clathrin-adjacent vesicle-trafficking signature.
- `claim:491c5c6eb002662cbefd` separated broad/core Cltc activity from flat or sparse adaptor-tier, APP-linked, Dnm1, Synj1, Bin1-like, and presynaptic/endocytic neighbors.
- `claim:f48dd8852b94eb3b98e0` documented that acute sparse perturbation of Dnm1 and Synj1 can leave neuronal nuclear downstream programs undetectably flat by FDR-based snRNA-seq, despite their strong vesicle-endocytosis biology.

These are same-experiment interpretations, not independent replication, but they identify which measured training perturbations are the closest AP-2-adjacent comparators and which high-count endolysosomal genes should be treated as more distal.

### Declared focal count table and Parquet

The 1,674-target focal training table was strongly zero-heavy:

- 1,205 / 1,674 targets had `n_degs = 0`.
- 1,481 / 1,674 had `n_degs <= 1`.
- 1,527 / 1,674 had `n_degs <= 3`.
- Only 43 / 1,674 had `n_degs >= 100`.

The closest represented AP/adaptor and synaptic-endocytosis genes were all zero or singletons in the requested cell class:

| comparator | focal `n_degs` | Parquet interpretation |
|---|---:|---|
| `Ap1b1` | 1 | self transcript only |
| `Ap1s2` | 0 | no FDR<0.05 gene |
| `Ap3b1` | 0 | no FDR<0.05 gene |
| `Ap4s1` | 0 | no FDR<0.05 gene |
| `Cltc` | 3 | three downstream genes, no focal self hit |
| `Dnm1` | 1 | self transcript only |
| `Synj1` | 1 | self transcript only |
| `Bin1` | 1 | self transcript only |
| `Cd2ap` | 0 | no FDR<0.05 gene |
| `Sh3kbp1` | 0 | no FDR<0.05 gene |
| `Prepl` | 1 | self transcript only |

More distal endolysosomal / retrograde-trafficking perturbations could be transcriptionally visible in this class, but I did not use them as equal-scale analogs for AP-2 plasma-membrane adaptor loss: `Vps35` had 17 genes, `Vps54` had 31, and `Rab7` had 501.

## Synthesis

The forecast has two competing bearings. Upward, AP2S1 is an obligate AP-2 component, is expressed in the focal thalamic glutamatergic class, has no annotated AP-2 sigma substitute, and likely loses functional stock before harvest. Downward, the assay measures survivor-conditioned nuclear RNA rather than endocytosis physiology, direct same-AP-2 training donors were absent, and the best available focal training perturbations from AP adaptors, dynamin, synaptojanin, and endocytic scaffolds were concentrated at 0-1 significant genes. Even `Cltc`, the visible core-coat exception in the corpus, gave only 3 BH<0.05 genes in the requested 151 class.

The AP2S1-specific biology keeps me above a pure zero call, but the quantitative scale of the focal AP/clathrin-neighbor rows supports a self-or-singleton-sized footprint rather than a Rab7/Vps35-like endolysosomal stress state. I therefore predict:

`predicted_n_degs = 1`
