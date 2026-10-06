# DEG-count prediction trace

## Question and interpretation

The requested manifest contains one held-out perturbation, `Clcn5`. I interpreted the requested endpoint as:

- focal cell group: `151 TH Prkcd Grin2c Glut`
- endpoint: the number of measured genes with `pvals_adj < 0.05` in the supplied Wilcoxon differential-expression table
- perturbation labels: acute P16 AAV-CRISPR loss-of-function targets, not germline knockouts or pharmacologic inhibition
- prediction target: the held-out `Clcn5` endpoint only; its DE rows and scalar count are absent from both training files

Zero therefore means that no measured gene, including the perturbed transcript itself, is predicted to pass BH FDR 0.05 in this focal group.

## Sources used

I used four same-experiment data sources:

1. `[local file: 041_Clcn5.csv]`
   - read the requested target list and confirmed it contains exactly `Clcn5`
2. `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
   - read all 1,674 non-held-out scalar DEG counts in the focal cell group
3. `[local file: training_de_all_cell_groups.parquet]`
   - filtered the DE table to `151 TH Prkcd Grin2c Glut` and chloride/endolysosomal comparator perturbations
4. Distributed Agents same-experiment semantic corpus
   - release `perturbai-july-260713-sourceguard-1773-v1`
   - queried `Clcn3`, `Clcn4`, `Ocrl`, `Rab7`, and endolysosomal claims for preinterpreted same-screen findings

I also used Distributed Agents runtime profile tools over the held-in DE parquet:

- `profile_compare` / `profile_inspect` compared log2-fold-change vectors in `151 TH Prkcd Grin2c Glut` among selected ClC, V-ATPase, phosphoinositide, and endolysosomal comparators.
- The comparison used measured gene as the feature, `gene_target` as the profiled entity, `logfoldchanges` as the signed value, and `pvals_adj < 0.05` to annotate significant features.
- It also searched the 1,674 training perturbations as the eligible universe for nearest whole-profile and top-tail neighbors of the ClC comparators.

External biological priors came from PubMed-indexed literature:

- Jentsch 2006, Journal of Physiology, DOI `10.1113/jphysiol.2006.124719`, PMID `17110406`: ClC-3 through ClC-7 are vesicular ClC transporters in the endosomal-lysosomal pathway and ClC-4/ClC-5 behave as electrogenic Cl-/H+ exchangers.
- Stauber, Weinert, and Jentsch 2012, Comprehensive Physiology, DOI `10.1002/cphy.c110038`, PMID `23723021`: review of mammalian ClC channel/transporter localization and the distinct disease biology of endosomal/lysosomal ClC-3, ClC-4, ClC-5, ClC-6, and ClC-7/Ostm1.
- Picollo, Malvezzi, and Accardi 2010, Journal of General Physiology, DOI `10.1085/jgp.201010428`, PMID `20513761`: CLC-5 is an endosomal H+/Cl- exchanger whose loss of function causes Dent disease.
- Novarino, Weinert, Rickheit, and Jentsch 2010, Science, DOI `10.1126/science.1188070`, PMID `20430975`: ClC-5-mediated Cl-/H+ exchange, not just chloride conductance, is crucial for renal proximal-tubule endocytosis.
- Devuyst and Luciani 2015, Journal of Physiology, DOI `10.1113/JP270087`, PMID `25820368`: ClC-5 loss is primarily a proximal-tubule endocytic/lysosomal trafficking disorder in Dent disease.
- Weinert et al. 2020, EMBO Journal, DOI `10.15252/embj.2019103358`, PMID `32118314`: ClC-3 and ClC-4 have closer neuronal endosomal roles; ClC-4 can compensate and stabilize ClC-3-containing endosomal exchangers in mouse brain.

## Dataset calibration

The scalar training endpoint is highly sparse:

- 1,674 training perturbations
- median `n_degs`: 0
- mean `n_degs`: 14.05
- 1,205 / 1,674 perturbations have 0 DEGs
- 469 / 1,674 have any nonzero FDR 0.05 hit
- only 3 training perturbations exceed 1,000 DEGs in this cell group

For the biologically relevant held-in comparators, I filtered the parquet to the focal cell group and counted rows with `pvals_adj < 0.05`. I did this rather than using signature frequency or a family name alone, because the question is a count endpoint in this exact Wilcoxon table.

The relevant focal counts were:

| comparator | rationale | focal `n_degs` |
| --- | --- | ---: |
| `Clcn3` | endosomal ClC exchanger, closest represented ClC-5 family analog with strong neuronal mouse biology | 0 |
| `Clcn4` | endosomal ClC exchanger and ClC-3 partner | 1 |
| `Ocrl` | Lowe/Dent-adjacent phosphoinositide endocytic gene | 0 |
| `Inpp5k` | phosphoinositide/endocytic pathway neighbor used in the corpus as an `Ocrl` contrast | 0 |
| `Synj1` | synaptic/endocytic phosphoinositide phosphatase | 1 |
| `Dnm1` | presynaptic endocytosis comparator | 1 |
| `Appl1` | endosomal scaffold in the OCRL comparator neighborhood | 0 |
| `Atp6ap2` | V-ATPase accessory / vesicle-acidification comparator | 2 |
| `Atp6v0a1` | V-ATPase V0 subunit | 1 |
| `Atp6v1a` | V-ATPase V1 subunit | 0 |
| `Atp6v1b2` | V-ATPase V1 subunit | 0 |
| `Atp6v1e1` | V-ATPase V1 subunit | 0 |
| `Lamp2` | lysosomal membrane comparator | 0 |
| `Ctsb` | lysosomal cathepsin; singleton was self-target | 1 |
| `Vps41` | HOPS / Rab7 late-endolysosomal comparator | 0 |
| `Vps35` | retromer comparator | 17 |
| `Vps54` | GARP trafficking comparator | 31 |
| `Rab7` | positive control for a detectable late-endosomal/lysosomal stress state | 501 |

Among same-family and near-pathway analogs, the nonzero calls were mostly self or almost-self depletion:

- `Clcn4`: the only focal hit was `Clcn4` itself, log2FC -0.802, adjusted p `6.72e-11`
- `Atp6v0a1`: the only hit was `Atp6v0a1`, log2FC -0.640
- `Atp6ap2`: the two hits were `Atp6ap2` itself and `Atp6v0a1`
- `Ctsb`, `Dnm1`, `Gdi1`, and `Synj1`: each had only self-target transcript depletion

That makes `Clcn4` more informative as a "no downstream program" comparator than as a nonzero multi-gene phenotype.

## Signature comparisons

I compared full focal log2FC vectors and top 200 positive/negative tails among `Clcn3`, `Clcn4`, `Ocrl`, `Inpp5k`, `Atp6ap2`, `Atp6v0a1`, `Rab7`, `Vps35`, `Vps54`, `Lamp2`, `Ctsb`, and `Snx10`.

Key observations:

- `Clcn3` and `Clcn4` were both at the assay floor:
  - `Clcn3`: 0 significant features
  - `Clcn4`: 1 significant feature, all negative, the self transcript
- `Ocrl` and `Inpp5k` were also fully FDR-flat in the focal group.
- The V-ATPase comparators did not form a broad acidification signature:
  - `Atp6v0a1`: 1 DEG
  - `Atp6ap2`: 2 DEGs
- The ClC signatures were not near the `Rab7` large response among the selected comparators:
  - `Clcn3` ranked `Rab7` last by whole-profile Pearson/cosine in the selected endolysosomal cohort.
  - `Clcn4` also ranked `Rab7` last by whole-profile Pearson among the selected endolysosomal cohort.
  - `Clcn3` and `Clcn4` had no shared FDR-significant downstream genes with `Rab7`.
- Across all 1,674 training perturbations, the top tail-overlap neighbors of `Clcn3` and `Clcn4` were mostly unrelated and weak:
  - `Clcn3` positive-tail top-200 neighbors included `Nr1h5`, `Figla`, `Atxn1`, `Dag1`, `L1cam`, with overlap fractions only 0.125-0.135.
  - `Clcn4` positive-tail top-200 neighbors included `Unc5d`, `Gpr45`, `Trpa1`, `Pcdh19`, `Atad1`, with overlap fractions only 0.130-0.150.
  - the nearest whole-profile neighbors for `Clcn3` and `Clcn4` were not an endolysosomal module.

The same-experiment Distributed Agents corpus agreed with this reading:

- `Clcn3:F001-F005` summarize that `Clcn3` was transcriptionally buffered across recovered neuronal groups and did not activate lysosomal-autophagy, ISR/UPR, or synaptic-marker RNA programs.
- `Clcn4:F001-F006` summarize a near-null acute `Clcn4` loss-of-function surface and failure of `Clcn3`/V-ATPase relatives to form a `Clcn4`-like transcriptomic module.
- Corpus claim `claim:2aa16e813622a843c706` states that shared endomembrane-acidification annotation was insufficient to produce a conserved neuronal snRNA-seq module among represented NHE, CLC, and V-ATPase relatives.
- `Ocrl:F004` explicitly used `Clcn3`, `Clcn4`, `Inpp5k`, `Synj1`, `Appl1`, and `Dnm1` as measured endocytic/phosphoinositide relatives and found a shared flat downstream surface.
- `Rab7:F002/F003` and claim `claim:726468d7afc216bc3be2` supply the key positive control: this assay can detect a late-endosomal/lysosomal and sterol compensation state after `Rab7` perturbation, but `Ocrl`, `Abca7`, and `Gdi1` do not generically activate it.

## Target-specific reasoning

### `Clcn5`

`Clcn5` encodes ClC-5, a vesicular Cl-/H+ exchanger best known for renal proximal-tubule receptor-mediated endocytosis and Dent disease. It is mechanistically in the same broad endosomal ClC transporter family as `Clcn3` and `Clcn4`, but the external literature puts the strongest ClC-5 phenotype in kidney epithelium rather than postmitotic thalamic neurons. In contrast, `Clcn3` and `Clcn4` have more direct neuronal endosomal biology and ClC-3/ClC-4 interaction/compensation in mouse brain.

The best same-family training perturbations are therefore `Clcn3` and `Clcn4`, not `Rab7`:

- `Clcn3` had 0 DEGs in `151 TH Prkcd Grin2c Glut`.
- `Clcn4` had exactly 1 DEG, `Clcn4` itself, so its downstream count was effectively zero.
- In the Distributed Agents corpus, both are interpreted as FDR-flat acute postmitotic neuronal perturbations, despite known disease or neurodegeneration biology in other settings.

I used several counterexamples to keep this from becoming an automatic "all endosomal genes are zero" rule:

- `Rab7` had 501 focal DEGs, with V-ATPase, lysosomal, and sterol transcripts such as `Atp6v1b2`, `Dpp7`, `Lamp2`, `Mcoln1`, `Insig1`, `Msmo1`, and `Fdft1` induced.
- `Vps35` and `Vps54` were nonzero at 17 and 31 DEGs.
- The corpus reports `Rab7` as a real late-endosomal/lysosomal compensation state in the same screen.

Those positives show that the focal cell group and snRNA readout are not globally blind to vesicle/lysosome stress. However, they do not point to a large `Clcn5` effect because the single endosomal ClC exchanger perturbations, the V-ATPase acidification comparators, and the Dent/Lowe-adjacent `Ocrl`/`Inpp5k` phosphoinositide branch are all flat or singleton-sized. This is exactly the neighborhood in which ClC-5 sits biochemically.

The predicted count is therefore the floor, `0`: an acute sparse `Clcn5` knockout is less likely than `Clcn3` or `Clcn4` to produce a broad thalamic neuronal nuclear-RNA program, and even a self-transcript hit is not expected strongly enough to call one DEG.

## Limits and extrapolation

- `Clcn5` was held out completely, so there is no measured `Clcn5` focal signature or self-target row to inspect.
- The closest represented paralogs are `Clcn3` and `Clcn4`; ClC-5 itself has distinct renal epithelial specialization, and more distant ClCs such as `Clcn6`/`Clcn7` were not in the focal training count table.
- A zero DEG prediction is not a prediction of no ion-transport, endosomal pH, protein-trafficking, electrophysiologic, or viability consequence. The endpoint only counts BH-significant nuclear RNA changes in recovered NeuN+ nuclei at one postnatal time point.
- Mosaic P16 CRISPR loss may miss embryonic, homozygous, or allele-specific dominant ClC disease mechanisms, and the average transcript knockdown per guide is modest.
- The positive `Rab7` counterexample is a late-endosomal/lysosomal blockade, not a same-complex comparator for ClC-5. I used it only to bound assay sensitivity for lysosomal compensation, not to scale the ClC-5 count.
- The prediction is mainly within-dataset evidence from `Clcn3`, `Clcn4`, `Ocrl`, `Inpp5k`, V-ATPase comparators, and `Rab7`; external biology only tilts the same-family evidence further toward the floor because ClC-5 is kidney/Dent-centered relative to the represented neuronal ClC-3/ClC-4 pair.
