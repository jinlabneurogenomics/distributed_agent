# Timp2 DEG-count prediction

## Question and inputs

I interpreted the task as a scalar prediction for the held-out `Timp2`
perturbation in `151 TH Prkcd Grin2c Glut`, the thalamic glutamatergic focal
class. The endpoint is the number of measured genes with `pvals_adj < 0.05` in
the held-out Timp2-versus-control Wilcoxon comparison. The requested target was
completely absent from both the supplied per-gene differential-expression
Parquet and the supplied focal-cell training DEG-count CSV, so no row from a
Timp2 perturbation itself entered the calculation.

The run-local target manifest
`single-target request for Timp2`
contains a single requested held-out target:

```tsv
target_name
Timp2
```

## Sources used

- Declared focal training-count CSV:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared all-cell-group differential-expression Parquet:
  `training differential-expression dataset`.
- Run metadata: `task.md`, `codex_runtime/pipeline/dataset_context.md`,
  `codex_runtime/pipeline/task_bindings.json`,
  `codex_runtime/pipeline/coverage.json`, and
  `codex_runtime/pipeline/capabilities.json`.
- Internal same-experiment semantic corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, queried through the July release
  Findings ledger and BioKG graph. These records are interpretations of the
  same Perturb-seq experiment, so I used them to find and interpret visible
  analogs, not as independent replication.
- External literature:
  - Gomez et al., 1997, PubMed 9352216: TIMP1--TIMP4 are tissue inhibitors of
    metalloproteinases that regulate ECM deposition/degradation, with TIMP1 and
    TIMP2 inhibiting known MMP activities.
  - Nagase, 1998, doi:10.1038/cr.1998.18, PubMed 9791731, and Bernardo &
    Fridman, 2003, doi:10.1042/BJ20030557, PubMed 12755684: TIMP2 participates
    in the MT1-MMP/pro-MMP2 cell-surface activation system and also constrains
    extracellular MMP2 activity.
  - Jaworski et al., 2005, doi:10.1016/j.brainres.2005.05.057, PubMed
    15979591: germline Timp2-null mice have altered prepulse inhibition and
    fear-potentiated startle, supporting a brain ECM/synaptic-plasticity
    phenotype for TIMP2 loss.
  - Ferreira et al., 2023, doi:10.1038/s41380-023-02296-5, PubMed 37914840:
    neuronal TIMP2 regulates hippocampal ECM complexity, adult neurogenesis,
    dendritic spine turnover, and hippocampus-dependent memory.

## Quantitative checks

I first summarized the focal training counts because the endpoint is an
assay- and cell-class-specific count, not a generic biological essentiality
score. The focal training set has 1,674 perturbations:

- 1,205/1,674 are zero-DEG calls.
- 469/1,674 have any DEG.
- The median and 75th percentile are 0 and 1 DEG; the 95th percentile is
  18 DEGs, and the largest focal response is 2,677 DEGs for `Uba5`.
- 276/1,674 have exactly one DEG.

I then scanned the Parquet only for `151 TH Prkcd Grin2c Glut` rows matching
the plausible within-dataset analogs around TIMP/MMP/ADAM/ECM biology. The
closest visible family member was `Timp3`; `Timp1`, `Timp2`, `Timp4`, and
MMP-family genes were not present as training perturbation targets in the focal
training-count CSV. The visible candidate set gave the following focal
`n_degs` values:

| training perturbation | focal `n_degs` | relevance to Timp2 |
| --- | ---: | --- |
| `Timp3` | 1 | TIMP-family ECM metalloprotease inhibitor; closest visible biochemical analog |
| `Adam10` | 0 | TIMP/ADAM/MMP neighborhood, APP/Notch/shed substrate axis; useful counterexample |
| `Adam22` | 1 | ADAM-family neuronal membrane protein, but its one call was self-only |
| `Adamts17` | 0 | metalloprotease-family ECM neighbor; no focal response |
| `App` | 1 | ADAM10 substrate and neuronal membrane/secretory counterexample; one self-only call |
| `Itgb1` | 0 | ECM/adhesion integrin counterexample |
| `Itga2`, `Itga2b`, `Itga4`, `Itga6`, `Itga7`, `Itga8`, `Itga9`, `Itgb2` | 0 | represented ECM-adhesion counterexamples |

For the strongest TIMP analog, `Timp3`, the focal Parquet row showed that the
only FDR<0.05 call in this cell class was the target transcript itself:

| measured gene | perturbation | log2 fold change | adjusted p-value |
| --- | --- | ---: | ---: |
| `Timp3` | `Timp3` | -0.841638 | 1.45e-6 |

The next-ranked `Timp3` focal rows all had `pvals_adj = 1.0`, including
`Clmn`, `Lsm14b`, `L3mbtl3`, `Hmgn3`, `Ptpa`, `Dhx57`, and `Psme4`. The
metalloprotease/ECM genes checked inside the same `Timp3` focal signature were
also flat after correction: `Timp2` log2FC +0.240, adjusted p=1; `Adam10`
+0.092, adjusted p=1; `Adam17` -0.221, adjusted p=1; `Mmp14` -1.595 with a
near-zero Wilcoxon score and adjusted p=1; `Mmp15` -0.069, adjusted p=1;
`Mmp16` +0.068, adjusted p=1; and `App` +0.027, adjusted p=1.

The visible ADAM/APP neighbors supported the same low-count scale rather than
a broader pathway effect. `Adam10` had 0 focal DEGs with only 69 matched
perturbed nuclei; its best raw rows had `pvals_adj = 1.0`. `App` had 1 focal
DEG, its own transcript (`App`, log2FC -1.420, adjusted p=8.4e-58).
`Adam22` likewise had one self-transcript call (`Adam22`, log2FC -0.550,
adjusted p=1.1e-9). Represented integrin ECM-adhesion targets were all null.

As a calibration check on the self-only interpretation, all 1,674 training
targets had a focal self-transcript row and 319/1,674 were significant for
their own transcript. Among the 276 one-DEG training perturbations, 237 had the
self transcript significant. Thus a prediction of 1 for a weakly downstream
TIMP-family perturbation is a common, concrete mode of the focal endpoint: it
means one detectable self-target RNA change and no additional BH-significant
downstream program.

The internal July corpus agreed with this numeric reading. Its `Timp3` report
records that `Timp3` was broadly buffered in neurons and had no downstream
FDR<0.10 program in 22 of 23 measured cell groups; it specifically called out
the `151 TH Prkcd Grin2c Glut` `Timp3` result as a thalamic self-drop without
a downstream nuclear RNA program. The same report also noted that represented
ADAM10/APP, VEGFR, TNF-receptor, and Notch targets did not phenocopy the one
CTX-CGE `Timp3`/`Syp` hit or reveal a hidden canonical TIMP3 pathway program.
The `Adam10` report independently found no broad postmitotic neuronal RNA
biomarker for the ADAM10/APP/Notch/synaptic-adhesion axis. I queried the
same-experiment graph for visible Findings that report `Timp2`; none were
present, so there was no direct held-out-gene analog in the corpus to override
the numeric TIMP3/ADAM/ECM calibration.

## Target-specific call

### Timp2 -> predicted `n_degs = 1`

TIMP2 is a secreted TIMP-family inhibitor/adapter in MMP signaling, especially
the MT1-MMP/MMP2 axis, and neuronal TIMP2 has reported roles in hippocampal
ECM remodeling and plasticity in mouse models. That external evidence supports
Timp2 as a real neuronal ECM regulator, not as an inert or unexpressed gene.
However, the requested endpoint is acute sparse CRISPR loss in recovered
postmitotic NeuN+ nuclei from a thalamic class, three to four weeks after AAV
delivery. That design is poorly aligned to secreted, extracellular, potentially
non-cell-autonomous protease phenotypes that may require hippocampal circuitry,
adult neurogenesis, dense tissue perturbation, injury, or glial/vascular
responses.

The closest visible perturbation, `Timp3`, therefore carries the most weight:
it had exactly one DEG in the focal thalamic class, and that one DEG was its
own transcript. `Timp3` did not move `Timp2`, ADAM-family transcripts,
MMP-family transcripts, or `App` at FDR<0.05 in this cell group. `Adam10`
itself was a complete focal null, and other represented ECM/adhesion or
metalloprotease neighbors were also null or self-only. Those within-dataset
counterexamples make a multi-gene TIMP2-triggered ECM/APP/Notch/MMP response
unlikely in this particular assay.

I still predicted a nonzero value rather than zero because `Timp2` is a
measured, dynamic transcript in the focal Parquet: it was FDR-significantly
altered by several strong visible perturbations (`Sin3a`, `Uba5`, `Gfpt1`,
`Zbtb7a`, and `Rora`). In the focal training data, self-transcript-only calls
are frequent among exactly-one-DEG perturbations, and `Timp3`, `App`, and
`Adam22` show that such isolated self hits occur in secretory/membrane
neighbors without a broader downstream state. The final point estimate is
therefore `1`: a predicted `Timp2` self-transcript call with no additional
FDR<0.05 downstream genes.

## Limits and uncertainty

This is an extrapolation from one visible TIMP family member plus pathway
counterexamples; `Timp2` itself, `Timp1`, `Timp4`, `Mmp2`, `Mmp14`, `Adam17`,
and the ADAMTS proteases most biochemically linked to TIMPs were not all
available as focal training perturbations. The Parquet does not provide raw
UMI-level baseline expression, protein abundance, MMP2 activity, or secreted
ECM proteolysis, so I could not directly test whether TIMP2 protein was
depleted in the focal thalamic neurons. Literature on TIMP2 establishes brain
and ECM function but mostly in germline, conditional, hippocampal, or
non-snRNA endpoints, which are informative priors rather than measurements of
this sparse postnatal Perturb-seq endpoint. The prediction is consequently
high confidence for a very small count and low confidence for the exact
integer distinction between 0 and 1.
