# Prediction trace

## Question and resolved ambiguities

The held-out perturbation in this run is `Caly`. I interpreted the task as a
point prediction of the `151 TH Prkcd Grin2c Glut` endpoint: the number of
measured genes whose Wilcoxon test in the Perturb-seq differential-expression
table would have `pvals_adj < 0.05` if the `Caly` perturbation had not been
held out. A prediction of `0` means no measured transcript is expected to pass
the adjusted-p cutoff in this cell group.

I used the readout as an assay-specific count, not as a generic measure of gene
importance. The supplied experiment uses sparse postnatal AAV-CRISPR in neurons
and has an average target mRNA decrease of only about 18 percent per guide, so
phenotypes from germline or high-efficiency knockouts are useful for mechanism
but not as a direct scale for `n_degs`.

## Sources

Primary same-experiment data:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for observed focal-cell DEG counts of the 1,674 non-held-out perturbations.
- `[local file: training_de_all_cell_groups.parquet]`
  for per-gene log2 fold changes and adjusted p-values used to compare focal
  signatures of mechanistic analogs.
- `[local file: 028_Caly.csv]`
  for the requested target list.

Local analysis/corpus sources:

- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
  `target_context(Caly)` returned no target-scoped claims, findings, or
  explicit references, so the corpus did not provide a Caly-specific comparator.
- Distributed Agents runtime profile tools. I extracted 34 mechanistically nominated
  focal-cell profiles and compared them with Pearson, cosine, and signed
  top-feature overlap using the measured `logfoldchanges` vectors.
- A wider runtime scan compared anchors `Cltc`, `Dnm1`, `Ap3b1`, `Adcy5`, and
  `Gria1` against all 1,674 eligible focal-cell training profiles. This was a
  guard against missing an unexpected same-experiment neighbor.

External biological sources:

- Xiao et al. 2006, PMID 16595675, DOI `10.1074/jbc.M600265200`: calcyon binds
  clathrin light chain, stimulates clathrin assembly, and calcyon-null cortical
  neurons have reduced transferrin uptake.
- Davidson et al. 2009, PMID 19120439, DOI
  `10.1111/j.1460-9568.2008.06563.x`: Caly deletion impairs activity-dependent
  AMPA receptor internalization and hippocampal LTD.
- Muthusamy et al. 2012, PMID 22650988, DOI
  `10.1111/j.1471-4159.2012.07814.x`: calcyon interacts with AP-3 medium
  subunits and regulates AP-3 cargo targeting in mouse brain.
- Ha et al. 2012, PMID 22843680, DOI `10.1074/jbc.M112.370601`: calcyon forms
  a PSD-95-dependent complex with dopamine D1 receptor and can regulate D1
  receptor internalization.
- Zelenin et al. 2002, PMID 11920718, DOI `10.1002/cne.10198`: calcyon is
  brain-enriched and expressed in regions overlapping D1/D5 dopamine receptor
  expression.

## Computational checks over the supplied data

The manifest contained exactly one target, `Caly`, and `Caly` was absent from
the training DEG-count CSV as expected.

The focal training count distribution was very sparse:

- 1,674 training perturbations.
- 1,205 had `n_degs = 0`.
- 276 had `n_degs = 1`.
- 31 had `n_degs = 2`.
- 1,527, or 91.2 percent, had `n_degs <= 3`.
- Median = 0, 75th percentile = 1, mean = 14.1, maximum = 2,677.

I used PyArrow row-group filtering to extract `151 TH Prkcd Grin2c Glut`
profiles for 34 hand-nominated Caly comparators from the parquet:

```python
expr = (
    pc.field("group_name") == "151 TH Prkcd Grin2c Glut"
) & pc.field("gene_target").isin(available_comparator_genes)
```

Each extracted perturbation had 17,259 measured gene rows. I then verified that
the number of rows with `pvals_adj < 0.05` exactly reproduced the training
`n_degs` values for those genes. A runtime `profile_compare` over these 34
profiles used the full log2-fold-change vectors plus signed top tails of 200
genes and 1/2/5 percent of features. The result had no missing profiles and
reported 21 of 34 candidate profiles with no significant focal features, 10
with 1 to 9, 2 with 10 to 49, and only `Grin1` with at least 50.

The all-training eligible-neighbor scan used all 1,674 training targets. Its
nearest neighbors of `Cltc`, `Dnm1`, `Ap3b1`, `Adcy5`, and `Gria1` were mostly
heterogeneous low-count genes rather than a hidden high-response Caly module.
For example, the whole-profile nearest neighbors to `Cltc` were `Atp6v1b2`,
`Unc13b`, `Atp6v1e1`, `Timmdc1`, and `Hspa5` with counts 0, 0, 0, 0, and 5;
nearest whole-profile neighbors to `Ap3b1` were `Ndufs4`, `Slit2`, `Pcsk2`,
`Ryr2`, and `Dyrk1a` with counts 0, 0, 1, 0, and 0. I therefore treated that
wide scan as reassurance that the endocytosis anchors sit in the no/low-response
bulk of the assay, not as evidence for a broader nonzero prediction.

## Target-specific reasoning

### Caly

`Caly` encodes calcyon, a brain-enriched single-pass vesicular protein. The
best direct molecular evidence links it to clathrin/AP trafficking and synaptic
receptor internalization: Xiao et al. found a clathrin-light-chain interaction
and defective transferrin uptake in calcyon-null neocortical neurons; Davidson
et al. found impaired AMPAR internalization and LTD; Muthusamy et al. found
binding to AP-3 medium subunits and altered AP-3 cargo localization; Ha et al.
placed calcyon in a PSD-95/D1 receptor trafficking complex.

I therefore calibrated against three nearby training groups.

Direct clathrin and vesicle-recycling analogs were nearly silent:

| perturbation | focal `n_degs` | why it is relevant |
| --- | ---: | --- |
| `Cltc` | 3 | Core clathrin heavy chain, upstream of the clathrin coats that calcyon stimulates |
| `Dnm1` | 1 | Neuronal dynamin for vesicle scission in clathrin-mediated endocytosis |
| `Synj1` | 1 | Synaptic vesicle uncoating/recycling factor |
| `Ap3b1` | 0 | AP-3 beta subunit in the adaptor complex whose mu subunits bind calcyon |
| `Reps1` | 0 | Endocytic adaptor candidate and low-response counterexample |
| `Ap1b1` | 1 | AP-1 adaptor subunit, a broader clathrin trafficking control |
| `Ap1s2` | 0 | AP-1 sigma subunit, another broader trafficking control |

Their significant genes were not a shared program. `Cltc` had only three
significant genes, all down (`Gabra4`, `Rbms1`, `Ero1b`); `Dnm1` and `Synj1`
each only passed on the perturbed transcript itself; `Ap3b1` and `Reps1` passed
on nothing. Runtime pair inspection found modest same-direction similarity among
the top log-fold-change tails, for example `Cltc` versus `Synj1` Pearson 0.660
and cosine 0.742, and `Synj1` versus `Ap3b1` Pearson 0.708 and cosine 0.773,
but zero shared significant genes in those pairs. This supports a very small
same-experiment signature for this branch of biology.

The receptor-signaling analogs were even quieter:

| perturbation | focal `n_degs` | why it is relevant |
| --- | ---: | --- |
| `Drd5` | 0 | D1-like receptor family member overlapping with calcyon expression |
| `Drd2` | 0 | dopamine receptor / GPCR trafficking counterexample |
| `Drd4` | 0 | dopamine receptor / GPCR trafficking counterexample |
| `Gnal` | 0 | G alpha olf, stimulatory GPCR signaling to adenylyl cyclase |
| `Gnas` | 0 | G alpha s, stimulatory GPCR signaling |
| `Adcy1` | 0 | neuronal adenylyl cyclase |
| `Adcy3` | 0 | adenylyl cyclase |
| `Adcy5` | 0 | dopamine-linked striatal adenylyl cyclase |
| `Pde10a`, `Pde1c`, `Pde4b`, `Pde4d` | 0 each | cAMP phosphodiesterases |
| `Prkaca`, `Prkar1a`, `Gnao1` | 1 each | downstream PKA/G-protein controls |

These are not direct biochemical copies of `Caly`, but they are good
counterexamples to an argument that Caly should be broad solely through D1/D5
or cAMP coupling. The D1-family and cAMP nodes had no significant genes in the
focal cell type despite high whole-vector correlations typical of the assay's
low-amplitude profiles.

AMPA/NMDA postsynaptic comparators also point low:

| perturbation | focal `n_degs` | why it is relevant |
| --- | ---: | --- |
| `Dlg4` | 1 | PSD-95 scaffold used by calcyon to form the D1 receptor complex in Ha et al. |
| `Gria1`, `Gria2`, `Gria3` | 0 each | AMPAR subunits affected downstream in Caly-null hippocampal LTD |
| `Grin2a` | 1 | NMDA receptor subunit comparator |
| `Grin2b` | 2 | NMDA receptor subunit comparator |
| `Camk2a` | 0 | CaMKII signaling downstream of calcium/glutamate signaling |
| `Camk2b` | 1 | CaMKII signaling control |
| `Camk2g` | 0 | CaMKII signaling control |

The exception was `Grin1` with 89 DEGs, including a strong loss of `Grin1`
itself and many secondary synaptic/immediate-response changes. I treated `Grin1`
as a boundary rather than an analog: it removes an obligate NMDA receptor pore
subunit in Grin2c-positive glutamatergic cells, which is much closer to direct
receptor loss than to partial loss of a calcyon accessory trafficking protein.

`Vps35` and `Vps54` were the only trafficking-adjacent candidates above the
single-digit range, at 17 and 31 DEGs. They are useful upper-bound
counterexamples because retromer/GARP loss affects endolysosomal sorting more
globally than calcyon's specialized clathrin/AP3 role. Their nonzero responses
also had broader stress/synaptic genes such as `Atp2a2`, `Jun`, and `Egr1`
rather than a clathrin/Caly-specific set. `Vps35` and `Vps54` shared only one
negative significant gene with each other in the inspected profile table and
shared none of their significant genes with `Cltc`, `Dnm1`, `Synj1`, or
`Ap3b1`.

### Decision

The direct within-dataset evidence dominates the final scale. The perturbations
closest to Caly in clathrin/AP trafficking had observed counts of 0, 1, 1, and
3; the dopamine/cAMP and AMPAR/Dlg4 comparators were 0 to 1 except for direct
NMDA receptor loss; and the all-training profile scan did not reveal a coherent
high-count analog. External biology shows Caly can matter for synaptic receptor
traffic, but mostly as an accessory endocytic factor, so in an acute sparse
CRISPR snRNA-seq assay I expect its transcriptional response to fall below the
BH 0.05 detection threshold.

Predicted `n_degs` for `Caly`: **0**.

## Limits

The evidence for `Caly` is extrapolative because the Distributed Agents corpus had no
Caly-specific local findings and the gene itself was absent from the training
DE table by construction. Several of the clearest Caly papers use germline
mouse nulls, cultured neurons, hippocampal CA1, or overexpression systems rather
than sparse P16-to-P37/P44 AAV-CRISPR in `151 TH Prkcd Grin2c Glut` cells.
The runtime profile similarities among low-count perturbations are dominated by
subthreshold log-fold changes, so I used them only to rule out a strong shared
program. Finally, a true count of 1 to 3 would also be biologically consistent
with the direct `Cltc`/`Dnm1`/`Synj1` analogs; the exact zero/nonzero boundary is
therefore the main uncertainty, and I placed `Caly` just below it.
