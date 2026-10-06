# Drd3 DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The requested prediction is the integer number of genes expected to pass
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after acute CRISPR-Cas9
loss of the held-out target `Drd3` in the thalamic glutamatergic cell group
`151 TH Prkcd Grin2c Glut`.

I treated the DEG count, not the fold change of the target transcript itself,
as the endpoint. A zero prediction means no measured gene, including but not
limited to the target RNA, is expected to pass FDR 0.05 in this focal group.
This is an assay- and power-dependent survivor-nucleus endpoint, not a direct
viability or editing-efficiency readout.

The held-out target list contained one target:

```tsv
target_name
Drd3
```

## Sources used

- Declared training DEG counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression Parquet:
  `training differential-expression dataset`.
- Declared held-out manifest:
  `single-target request for Drd3`.
- PerturbAI July same-experiment corpus,
  `perturbai-july-260713-sourceguard-1773-v1`, used only as packaged
  interpretation of the same experiment. The corpus had no `Drd3` Finding
  rows, as expected for this held-out perturbation.
- PubMed literature for external receptor biology:
  Sokoloff et al. 1990, Nature, DOI `10.1038/347146a0`, PMID `1975644`;
  Levesque et al. 1992, PNAS, DOI `10.1073/pnas.89.17.8155`, PMID `1518841`;
  Demotes-Mainard et al. 1996, Developmental Brain Research,
  DOI `10.1016/0165-3806(96)00041-7`, PMID `8836575`;
  Le Moine and Bloch 1996, Neuroscience,
  DOI `10.1016/0306-4522(96)00029-2`, PMID `8783237`;
  Missale et al. 1998, Physiological Reviews,
  DOI `10.1152/physrev.1998.78.1.189`, PMID `9457173`;
  Gurevich et al. 2016, Pharmacological Research,
  DOI `10.1016/j.phrs.2016.05.010`, PMID `27178731`.

## Quantitative calibration

I first checked the focal training endpoint distribution and then queried the
Parquet for receptor and second-messenger analogs in exactly
`151 TH Prkcd Grin2c Glut`.

The 1,674 non-held-out training perturbations were sparse in this cell group:
1,205 had `n_degs = 0`, the median was 0, the 90th percentile was 2, and the
mean was 14.054 because a small set of spliceosome, proteasome, ubiquitin, and
transcriptional regulators produced hundreds to thousands of DEGs. I therefore
did not assign a count from the global mean; I used target-specific dopamine
receptor and cAMP-pathway comparators.

For the focal Parquet rows I computed, per training perturbation:

- `sum(pvals_adj < 0.05)` to confirm the endpoint in the DE table;
- `min(pvals_adj)` and the smallest raw Wilcoxon p-values to inspect
  subthreshold expression-pattern evidence;
- `n_pert_matched` and `n_ctrl_matched` to catch major focal-cell power
  differences among the analogs.

The closest receptor and coupling analogs were all flat at the FDR endpoint:

| training perturbation | focal `n_degs` | focal evidence |
|---|---:|---|
| `Drd2` | 0 | D2-like Gi/o dopamine receptor. There were 213 matched perturbed nuclei and 23,679 controls; the best raw-p rows were modest, for example `Zbtb7a` logFC -0.447 and raw p 0.00046, but every adjusted p-value was 1.0. `Drd3` itself was unchanged in the `Drd2` contrast, logFC -0.059, adjusted p 1.0. |
| `Drd4` | 0 | D2-like Gi/o dopamine receptor. There were 218 matched perturbed nuclei; all adjusted p-values in the focal class were 1.0. The same-experiment corpus described `Drd4` as taxonomy-wide FDR-clean, including no cAMP, immediate-early, NMDA/AMPA, or GABA mRNA program. |
| `Drd5` | 0 | D1-like Gs/olf dopamine receptor and a receptor-family counterexample with the opposite adenylate-cyclase sign from `Drd3`. There were 228 matched perturbed nuclei; all focal adjusted p-values were 1.0. The corpus also reported no strong positive or negative `Drd5` neighbors and no dopamine/cAMP/CREB program in the represented screen. |
| `Gnao1` | 1 | Gi/o alpha subunit connected to D2-like receptor signaling. Its only focal FDR hit was `Gnao1` itself, logFC -0.591, adjusted p `9.42e-7`; downstream genes were FDR-flat. |
| `Gnal` | 0 | G alpha olf subunit for dopamine/adenylyl-cyclase signaling. It had 148 matched perturbed nuclei and no focal FDR hits. |
| `Gnas` | 0 | G alpha s subunit. It had 306 matched perturbed nuclei and no focal FDR hits. |
| `Adcy1`, `Adcy3`, `Adcy5` | 0, 0, 0 | Adenylyl cyclase genes represented in training; none produced a focal FDR hit. |
| `Pde10a`, `Pde1c`, `Pde4b`, `Pde4d` | 0, 0, 0, 0 | cAMP/cGMP phosphodiesterases. Loss should increase cyclic nucleotide signaling, the direction expected from loss of a Gi-coupled inhibitory receptor, yet all were FDR-flat in the focal group. `Pde10a` and `Pde1c` had the strongest subthreshold rows among these, with minimum adjusted p-values 0.304 and 0.180. |
| `Prkaca` | 1 | Core PKA catalytic subunit downstream of cAMP. The only focal FDR call was `Prkaca` itself, adjusted p `7.91e-22`; downstream rows were below FDR. |
| `Creb1`, `Crebbp` | 10, 8 | Nuclear CREB-axis counterexamples. These show that directly perturbing transcriptional machinery downstream of cAMP can yield a small nonzero focal signature, but they are not receptor or membrane-proximal analogs for `Drd3`. |

The same-experiment corpus summaries for `Drd2`, `Drd4`, `Drd5`, `Gnal`, and
`Gnao1` also reported absence of broad dopamine/cAMP convergence across the
atlas. I used those summaries to check that the focal nulls were not obviously
contradicted by a strong same-experiment dopamine module elsewhere. I did not
use corpus relation counts, graph topology, or comparator multiplicity as a
score.

## Biological transfer to Drd3

`Drd3` encodes dopamine receptor D3, a D2-like GPCR. D2/D3/D4 receptors couple
through G alpha i/o and inhibit adenylyl cyclase, while D1/D5 receptors couple
through G alpha s/olf and stimulate adenylyl cyclase (Missale et al. 1998;
Gurevich et al. 2016). Molecularly, the best within-dataset transfer is
therefore `Drd2` and `Drd4`, with `Gnao1`, `Gnal`, `Gnas`, `Adcy*`, `Pde*`, and
`Prkaca` testing adjacent signaling steps rather than receptor identity.

The causal chain I applied was:

`Drd3` CRISPR loss of function -> lower D3 receptor signaling in infected,
recovered nuclei -> disinhibition of Gi/o-sensitive cAMP only where D3 is
expressed and limiting -> CREB/immediate-early or other second-messenger
programs -> recovered thalamic glutamatergic nuclei sampled at P37-P44 ->
Wilcoxon FDR calls in `151 TH Prkcd Grin2c Glut`.

That chain weakens at the exposure and limiting-function steps. Drd3 receptor
binding and mRNA are best known in limbic basal forebrain and ventral striatal
compartments, especially islands of Calleja and nucleus accumbens, with lower
or more restricted expression in thalamic or other regions (Sokoloff et al.
1990; Levesque et al. 1992; Le Moine and Bloch 1996). D3 receptors are present
developmentally in anterior thalamic regions by early postnatal stages, but the
mouse distribution by and after weaning is still much more limbic than
thalamic (Demotes-Mainard et al. 1996). The focal Perturb-seq group is
thalamic glutamatergic, not ventral striatal or islands-of-Calleja neurons.

The receptor-level same-outcome prior is also weak because loss of `Drd2`,
`Drd4`, and `Drd5` produced zero focal DEGs despite similar focal perturbed-cell
recovery. If focal thalamic neurons contained a robust basal dopamine receptor
to cAMP to transcription axis, one would expect at least some of the D2-like,
Gs/olf, adenylyl cyclase, phosphodiesterase, or PKA perturbations to show
coherent FDR-level responses. They did not. The small `Creb1`/`Crebbp` counts
show that downstream nuclear perturbation can be detected, but they sit below
receptor coupling and are not enough to infer that acute, partial `Drd3` loss
will drive an FDR-significant receptor-state signature.

## Target-specific prediction

### Drd3: predicted `n_degs = 0`

I predict that `Drd3` loss will be FDR-flat in `151 TH Prkcd Grin2c Glut`.
The decisive within-dataset evidence is the receptor and membrane-proximal
calibration: `Drd2 = 0`, `Drd4 = 0`, `Drd5 = 0`, `Gnal = 0`, `Gnas = 0`,
`Gnao1` only called its own transcript, the represented adenylyl cyclases were
0, and the cAMP-increasing PDE perturbations were 0. External literature makes
`Drd2` and `Drd4` the mechanistically closest visible receptor analogs but also
places the strongest D3 biology outside this thalamic glutamatergic focal
population. I therefore do not upshift `Drd3` above the zero receptor baseline.

## Limits and uncertainty

The prediction is an extrapolation because no `Drd3` DE contrast or DEG count
is present in the supplied inputs, and the July same-experiment corpus had no
`Drd3` Finding rows to resolve. The Parquet does not contain raw counts or
baseline receptor expression, so I could not directly verify D3 receptor
abundance in the focal recovered nuclei from the declared tables. A Drd3 effect
could also be missed if it were restricted to an anatomic subset inside the
broader `151 TH Prkcd Grin2c Glut` label, if it changed electrophysiology or
synaptic signaling without a stable nuclear RNA program at 3-4 weeks, or if
the small infected population with D3 dependence was selected out before
snRNA-seq. Those are reasons for uncertainty, but they do not overcome the
zero-DEG receptor and cyclic-nucleotide training analogs in the same focal
cell group.
