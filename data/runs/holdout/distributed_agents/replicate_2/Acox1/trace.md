# DEG-count prediction trace

## Question and resolved ambiguities

The requested endpoint is the number of measured genes with
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in
`151 TH Prkcd Grin2c Glut` nuclei after each held-out CRISPR perturbation.
The run manifest contained one held-out target:

| target | requested prediction |
|---|---:|
| Acox1 | `n_degs` in `151 TH Prkcd Grin2c Glut` |

I treated the target as acute, sparse, postnatal neuronal CRISPR loss of
function in the PerturbAI whole-brain atlas, not as a germline Acox1-null,
retinal, liver, glial, siRNA, or drug experiment.  The endpoint includes the
perturbed transcript if it passes FDR, so a count of 1 in the training data can
be either a self-transcript effect or one downstream gene.  Target-RNA
knockdown was used only to identify those self-only singleton cases, not as a
proxy for editing efficiency.

## Sources

Internal, experiment-matched sources:

- `training_de_all_cell_groups.parquet`, the authoritative per-gene DE table.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, the focal class
  `n_degs` table for the 1,674 non-held-out perturbations.
- `002_Acox1.csv`, the held-out manifest.
- The Distributed Agents same-experiment semantic corpus
  `perturbai-july-260713-sourceguard-1773-v1`.
- Distributed Agents run-local profile tools over the focal Parquet slice.

External mechanism sources:

- Fournier et al. 1994, J. Clin. Invest., DOI `10.1172/JCI117365`: cloned
  human peroxisomal acyl-CoA oxidase and identified ACOX1 deletion as the
  cause of pseudoneonatal adrenoleukodystrophy.
- Ferdinandusse et al. 2007, Human Mutation, DOI `10.1002/humu.20535`:
  clinical, biochemical, and mutational spectrum of peroxisomal acyl-CoA
  oxidase deficiency; very-long-chain fatty acid accumulation is its hallmark.
- Violante et al. 2018, FASEB J., DOI `10.1096/fj.201801498R`: ABCD3 and
  HSD17B4 are required for a peroxisomal medium/long-chain fatty-acid oxidation
  route when mitochondrial beta-oxidation is limited.
- Ranea-Robles et al. 2021, Cell. Mol. Life Sci., DOI
  `10.1007/s00018-021-03869-9`: ABCD3 and ACOX1 are essential for
  dicarboxylic-acid beta-oxidation in the peroxisome, with overlapping
  contributions from EHHADH/HSD17B4 and ACAA1/SCPx.
- Rao and Reddy 2001, Semin. Liver Dis., DOI `10.1055/s-2001-12928`, and
  He et al. 2020, Mol. Cell, DOI `10.1016/j.molcel.2020.05.007`: Acox1 loss
  can strongly perturb hepatic peroxisomal beta-oxidation, PPARA signaling, and
  autophagy/lipid homeostasis in metabolically matched tissues.
- Tahri-Joutey et al. 2021, Int. J. Mol. Sci., DOI `10.3390/ijms22168969`:
  review of PPARA/RXRA control of hepatic peroxisomal fatty-acid
  beta-oxidation genes.

## Computations over the training data

I first read the held-out manifest and the focal count table.  The count table
contains 1,674 training targets; 1,205 have `n_degs = 0`, 363 have 1-9 DEGs,
63 have 10-99 DEGs, and 43 have at least 100.  Thus the prior in this focal
class is heavily weighted toward no detected response.

For the mechanistic comparisons I scanned the Parquet with
`group_name == "151 TH Prkcd Grin2c Glut"` and direct `gene_target` filters.
For each comparator I counted rows with `pvals_adj < 0.05`, inspected the
significant genes, and checked the target's own transcript when it was present.
The focal control count for these rows was 23,679 matched control nuclei; the
selected perturbations had 105-315 matched perturbed nuclei, so they were in
the same sparse but usable scale as the held-out endpoint.

I also ran a Distributed Agents profile comparison for observed focal log-fold-change
vectors from these training perturbations:

`Hsd17b4, Abcd3, Pex1, Pex14, Acbd5, Agps, Ppara, Ppard, Pparg, Ppargc1a,
Rxra, Rxrb, Rxrg, Aco2, Acsl4, Cpt1c, Etfa`

The 14-profile subset available in the runtime comparison had 11 profiles with
zero FDR-significant focal genes and 3 profiles in the 1-to-9 bin.  In direct
Parquet inspection, those three one-DEG profiles were self-only for `Pex14`,
`Acsl4`, and `Cpt1c`; `Agps` had one non-self focal DEG, `Dhcr24`.

## Acox1-specific reasoning

### Mechanistic neighborhood considered

`Acox1` encodes peroxisomal acyl-CoA oxidase 1, the oxidase initiating
straight-chain very-long-chain fatty-acyl-CoA and dicarboxylic-acid
beta-oxidation.  `Acox2`/`Acox3`, the closest oxidase relatives, were not
present as focal training perturbations.  The best in-dataset comparators were
therefore peroxisomal substrate transport, downstream beta-oxidation, import,
ether-lipid synthesis, and PPAR/RXR regulators:

| training perturbation | focal `n_degs` | expression-pattern evidence in `151 TH Prkcd Grin2c Glut` | relevance to Acox1 |
|---|---:|---|---|
| `Hsd17b4` | 0 | no FDR<0.05 genes; self row `padj = 1` | D-bifunctional protein downstream of acyl-CoA oxidase in peroxisomal beta-oxidation |
| `Abcd3` | 0 | no FDR<0.05 genes; self row `padj = 1` | peroxisomal ABC transporter feeding fatty-acyl substrates into the organelle |
| `Acbd5` | 0 | no FDR<0.05 genes; self row `padj = 1` | peroxisome-ER tether and VLCFA-CoA handling protein; same lipid/organelle compartment |
| `Pex1` | 0 | no FDR<0.05 genes; self row `padj = 1` | peroxisome biogenesis/import AAA ATPase; stronger organelle-level loss than one oxidase |
| `Pex14` | 1 | only `Pex14` itself passed FDR (`logFC = -0.907`, `padj = 3.7e-7`) | peroxisomal matrix-protein import docking factor |
| `Agps` | 1 | one non-self focal DEG, `Dhcr24` (`logFC = 0.66`, `padj = 0.0019`) | ether-lipid branch of peroxisome metabolism; less direct than beta-oxidation |
| `Ppara` | 0 | no FDR<0.05 genes; minimum adjusted p-value was 1 | nuclear receptor often regulating hepatic peroxisomal FAO |
| `Ppard` | 0 | no FDR<0.05 genes; minimum adjusted p-value was 1 | related fatty-acid-responsive nuclear receptor |
| `Pparg` | 0 | no FDR<0.05 genes | PPAR paralog and corpus-nominated boundary |
| `Ppargc1a` | 0 | no FDR<0.05 genes; minimum adjusted p-value was 0.189 | coactivator linked to peroxisome/mitochondrial oxidative programs |
| `Rxra`, `Rxrb`, `Rxrg` | 0, 0, 0 | no FDR<0.05 genes | RXR heterodimer partners for PPARs |
| `Acsl4`, `Cpt1c`, `Etfa` | 1, 1, 0 | `Acsl4` and `Cpt1c` were self-only singleton profiles; `Etfa` had no FDR<0.05 genes | fatty-acid activation, neuronal carnitine acyltransferase, and mitochondrial electron-transfer comparator set |
| `Aco2` | 0 | no FDR<0.05 genes | not a peroxisomal paralog; useful only as a distant aconitase-name counterexample |

The Distributed Agents corpus for the same experiment independently reported that
`Hsd17b4`, `Abcd3`, `Pex1`, `Acbd5`, and `Ppara` were pan-neuronal or
near-pan-neuronal transcriptional nulls, and that `Pex14` had no downstream
FDR<0.10 transcript in any of 23 measured neuronal groups.  I used corpus
Finding IDs `Hsd17b4:F001-F004`, `Abcd3:F001-F004`, `Pex1:F001-F004`,
`Acbd5:F001-F004`, `Ppara:F001-F006`, and `Pex14:F001-F005` as the
same-experiment semantic layer over the Parquet.

I also expanded the same-experiment outbound graph from `Hsd17b4`, `Abcd3`,
`Pex1`, and `Ppara`.  The recurrent returned candidates and dispositions were:

| candidate | focal count | disposition | reason |
|---|---:|---|---|
| `Pex14` | 1 | keep | explicit import comparator for the peroxisome nulls; focal singleton was self only |
| `Acbd5` | 0 | keep | peroxisomal VLCFA-handling comparator; null in the focal count table |
| `Agps` | 1 | keep | peroxisomal ether-lipid comparator; only a one-gene sterol response at FDR<0.05 |
| `Ppargc1a` | 0 | keep | PPAR coactivator boundary for lipid oxidative transcription |
| `Ppard` | 0 | keep | PPAR-family boundary for fatty-acid signaling |
| `Pparg` | 0 | keep | more distant PPAR-family boundary; quiet and not positively weighted |

### Zero/nonzero decision

The closest biochemical nodes to ACOX1 in the training set were `Hsd17b4` and
`Abcd3`, because they participate in the same peroxisomal beta-oxidation
system rather than merely sharing a lipid-metabolism label.  Both had
`n_degs = 0` in the focal cell group.  The broader peroxisome-import genes were
also flat: `Pex1 = 0`, `Acbd5 = 0`, and `Pex14 = 1` only because the `Pex14`
transcript itself was significantly depleted.  PPARA/PPARGC1A/RXR
transcriptional regulators that could have conveyed lipid-feedback gene
induction were all `0`.

Those data argue that acute perturbation of a peroxisomal fatty-acid oxidation
node is normally buffered or invisible in recovered `151 TH Prkcd Grin2c Glut`
nuclei.  Complete ACOX1 deficiency is biologically consequential in germline
human disease and in liver-specific mouse models, but those settings involve
developmental exposure, whole tissues with strong peroxisomal lipid flux, and
metabolic stress.  They are imperfect for a 3-4 week mosaic knockout in
postmitotic thalamic neurons with glia largely absent from the readout.

The self-transcript calibration also favored zero rather than a singleton.  A
few training nulls became `n_degs = 1` because their own RNA passed FDR
(`Pex14`, `Acsl4`, `Cpt1c`), but equally close peroxisomal genes with detected
self down-shifts did not pass (`Hsd17b4`, `Abcd3`, `Pex1`, `Acbd5`).  Across
all 1,674 focal signatures, measured `Acox1` itself was rarely significant as
a feature: it passed FDR only once, under `Rab7`, and otherwise behaved like a
modest, weakly varying transcript rather than a consistently high-power
marker.  I therefore predicted no measured gene, including `Acox1` itself,
will cross `pvals_adj < 0.05`.

### Prediction

`Acox1 -> 0` DEGs.

## Limits of the reasoning

- There is no observed `Acox1` perturbation profile in the training Parquet;
  the prediction is a transfer from mechanistic neighbors.
- `Hsd17b4`, `Abcd3`, `Pex1`, `Pex14`, `Acbd5`, and `Agps` are close but not
  identical.  ACOX1 performs the first oxidative step and can have
  substrate/ROS/acetyl-CoA effects that a transporter or import-factor
  perturbation may not reproduce.
- The focal Parquet gives DE statistics, not raw expression or editing
  genotypes, so the probability of an `Acox1` self-transcript hit can only be
  inferred indirectly from other self hits and from `Acox1` as a measured
  feature under non-Acox1 perturbations.
- Literature on ACOX1 disease, retinal phenotypes, and hepatic PPARA feedback
  shows that ACOX1 can matter, but most of it is systemic, developmental,
  hepatic, retinal, or glial and should not be copied quantitatively into this
  postnatal NeuN-positive thalamic CRISPR readout.
- A true small response of one or a few genes is the hardest case to predict:
  the difference between 0 and 1 can be a single self-transcript or a single
  pathway gene crossing the BH threshold.
