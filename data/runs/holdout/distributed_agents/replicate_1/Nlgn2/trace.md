# Predicting held-out DEG count for Nlgn2

## Question and endpoint

The requested endpoint is the number of rows with `pvals_adj < 0.05` in the hidden
`Nlgn2` perturbation contrast in `151 TH Prkcd Grin2c Glut` cells. The row for the
perturbed gene itself is included if it is measured and significant. I therefore
treated `n_degs = 1` as meaning "possibly self-transcript only", not as evidence
for a downstream transcriptional program.

`Nlgn2` was held out from both supplied inputs, so the hidden readout was absent.
The differential-expression parquet and the training count CSV are direct
measurements for non-held-out perturbations in the same experiment and same focal
cell type. The selected July same-experiment corpus is a packaged interpretation
of that experiment, used only to inspect visible training analogs. I used PubMed
literature as external prior knowledge for NL2, neuroligins, neurexins, gephyrin,
and collybistin.

The count distribution in the focal training CSV was highly zero-inflated:
`1205 / 1674` training perturbations had 0 DEGs and `1546 / 1674` had at most 5
DEGs. The median was 0, the 75th percentile was 1, and the few large responders
were transcriptional or RNA-processing genes such as `Uba5`, `Tpr`, `Sin3a`, and
`Rnpc3`, not synaptic adhesion factors.

## Dataset computations

I read `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
for the focal-class training counts and queried
`training differential-expression dataset`
with DuckDB, restricted to:

```sql
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (<biologically related visible perturbations>)
```

For each visible analog I counted `pvals_adj < 0.05`, checked the matched
perturbed and control nuclei, and inspected the highest absolute Wilcoxon-score
rows to see whether the count represented self-knockdown or downstream genes.
For the closest visible perturbations, the focal signatures were:

| training perturbation | matched perturbed nuclei | observed `n_degs` at FDR 0.05 | expression-pattern evidence in `151 TH Prkcd Grin2c Glut` | relevance to `Nlgn2` |
|---|---:|---:|---|---|
| `Nlgn3` | 177 | 1 | The only significant row was `Nlgn3` itself, logFC -0.896, FDR 4.79e-11; the next rows, `Slc25a14` and `Aak1`, had FDR 1.0. | Best visible neuroligin-family perturbation. Nlgn3 is not NL2-specific, but it is a postsynaptic neurexin ligand and a direct test that an acute neuroligin loss can be self-only in this assay. |
| `Nrxn1` | 253 | 1 | The only significant row was `Nrxn1` itself, logFC -0.518, FDR 2.67e-23; `Cacna1g` and `Bcar1` had FDR 1.0. | Neurexins are presynaptic NL2 binding partners. Loss of one neurexin does not reproduce postsynaptic NL2 loss because of isoform/splice redundancy, but it tests the same adhesion axis. |
| `Nrxn2` | 281 | 0 | Best absolute-score row was `Azin2`, FDR 0.165; `Nrxn2` itself was nonsignificant, logFC -0.129, FDR 1.0. | Same broad neurexin ligand family; a counterexample to a required neurexin/neuroligin nuclear RNA state. |
| `Nrxn3` | 175 | 0 | Best absolute-score row was `Vps4a`, FDR 0.091; no row passed 0.05. | Same broad neurexin ligand family; another flat same-axis comparator. |
| `Gphn` | 205 | 0 | `Gphn` itself was not significant, logFC -0.296, FDR 1.0; the best rows `Tk2`, `Atp11a`, and `Chd4` all had FDR 1.0. | Gephyrin is an inhibitory postsynaptic scaffold downstream of NL2/collybistin. If NL2 loss drove a broad GABA-receptor clustering stress transcriptome, Gphn would be an expected analog; it was flat in this focal class. |
| `Arhgef9` | 131 | 1 | The only significant row was `Arhgef9` itself, logFC -0.571, FDR 3.70e-08; `Ralgps1` and `Sirt3` were nonsignificant. | ARHGEF9/collybistin is activated by NL2 and helps tether gephyrin. Its self-only focal result argues that disrupting this postsynaptic scaffold axis is mainly silent to nuclear RNA here. |
| `Gabra1` | 128 | 1 | The only significant row was `Gabra1` itself, logFC -1.134, FDR 4.26e-18. | GABA(A) receptor alpha subunit; tests direct perturbation of inhibitory receptor components. |
| `Gabrb2` | 140 | 4 | `Gabrb2` self was significant, and `Nr4a1`, `Vgf`, and `Nalf1` were downstream FDR hits. | Counterexample showing that this focal class could emit a small activity-linked response to an inhibitory receptor lesion, but even this direct receptor perturbation produced only four DEGs. |
| `Gabrg2` | 166 | 1 | The only significant row was `Gabrg2` itself, logFC -1.046, FDR 4.66e-24. | Another inhibitory receptor subunit; self-only in the focal class. |
| `Dlg4` | 273 | 1 | The only significant row was `Dlg4` itself, logFC -0.444, FDR 1.15e-08. | Excitatory postsynaptic scaffold and NLGN-associated counterexample; visible synaptic scaffolds were not broad responders. |
| `Fyn` | 173 | 0 | `Fyn` itself was the strongest row but did not pass FDR 0.05. | Synaptic kinase comparator; no evidence for a broad shared state. |
| `Shank3` | 280 | 2 | `Shank3` and `Uba5` passed FDR 0.05. | ASD/synaptic scaffold comparator with only a two-gene signature. |
| `Slc6a1` | 220 | 0 | Best rows were all nonsignificant at adjusted FDR 1.0. | GABA transporter comparator; flat in this focal class. |

Two other checks mattered for the final integer. First, `Nlgn2` is a measured
gene in this focal dataset: it appeared in all 1,674 visible focal perturbations,
and seven broad or RNA-processing perturbations changed it at FDR 0.05
(`Zbtb7a`, `Sin3a`, `Rnpc3`, `Tardbp`, `Sec63`, `Prpf6`, `Smarcc2`). It is
therefore plausible that the hidden `Nlgn2` contrast has a testable self row.
Second, the rows for `Nlgn2`, `Nlgn3`, `Nrxn1`, `Nrxn2`, `Gphn`, `Arhgef9`,
`Gabra1`, `Gabrb2`, and `Gabrg2` did not form a recurring cross-regulatory
module across the inhibitory-synapse analog perturbations: in the focal
cross-table, nearly all off-target rows had `pvals_adj = 1.0`.

## Same-experiment corpus evidence

I inspected the July 260713 same-experiment corpus for the visible analogs
`Nlgn3`, `Gphn`, and `Arhgef9`. These reports summarize the same Perturb-seq
experiment, not an independent replicate.

* `Nlgn3` was classified as a pan-surface downstream transcriptomic null:
  across 22 recovered neuronal cell groups it had zero downstream genes even at
  FDR 0.10, including groups with significant `Nlgn3` self-transcript depletion.
  The report also noted that obvious measured neurexin and synaptic scaffold
  neighbors, including `Nrxn1`, `Nrxn2`, `Nrxn3`, `Dlg4`, `Shank2`, `Shank3`,
  `Dag1`, `Lrrtm1`, and `Cntnap2`, had near-zero similarity to `Nlgn3` and only
  0 to 2 downstream FDR 0.10 genes each.
* `Arhgef9` was also self-only or flat in all recovered groups. In the focal
  class it had zero downstream genes at FDR 0.10 despite a significant
  `Arhgef9` self-transcript drop.
* `Gphn` had no downstream genes in `151 TH Prkcd Grin2c Glut`; the only robust
  Gphn response in the atlas was a singleton `Cbarp` up-regulation in a cortical
  glutamatergic class, not a GABA/glycine-receptor or neuroligin module.

These corpus summaries supported the raw focal-class count table: the canonical
NL2-gephyrin-collybistin inhibitory-postsynapse axis was visible in the training
set but nearly silent as a nuclear RNA phenotype.

## External biological rationale

NL2/NLGN2 is a synapse-local cell-adhesion protein. It binds presynaptic
neurexins and is selectively associated with inhibitory GABAergic synapses, in
contrast to NLGN1 and the less synapse-type-restricted NLGN3. Mouse studies show
that loss or interference of NL2 changes inhibitory synaptic function and
behavioral/circuit readouts rather than acting as a transcription factor or a
protein-homeostasis gene:

* Chubykin et al. 2007, Neuron, DOI `10.1016/j.neuron.2007.05.029`, PMID
  `17582332`: NL1 and NL2 validate different synapse classes; NL2 loss
  selectively decreased inhibitory synaptic responses.
* Blundell et al. 2008, Genes Brain and Behavior, DOI
  `10.1111/j.1601-183X.2008.00455.x`, PMID `19016888`: NL2-deficient mice had
  decreased inhibitory synaptic function and anxiety-like behavior.
* Poulopoulos et al. 2009, Neuron, DOI `10.1016/j.neuron.2009.08.023`, PMID
  `19755106`: NL2 binds gephyrin and activates collybistin to assemble
  inhibitory postsynaptic specializations; Nlgn2 deletion perturbed GABAergic
  and glycinergic synaptic transmission.
* Chanda et al. 2017, Journal of Neuroscience, DOI
  `10.1523/JNEUROSCI.0125-17.2017`, PMID `28607166`: conditional deletion of
  major neuroligin isoforms in mouse neurons produced isoform-specific synaptic
  functional defects with only small changes in synapse number.
* Ali, Marth, and Krueger-Burg 2020, Science Signaling, DOI
  `10.1126/scisignal.abd8379`, PMID `33443230`: a focused review summarizes
  NL2 as a central organizer of inhibitory synapses through neurexin,
  gephyrin/collybistin, GABA(A)-receptor, and MDGA-related mechanisms.

Those papers make `Gphn`, `Arhgef9`, GABA(A)-receptor subunits, and neurexins
biologically relevant analogs. Their direction is "same postsynaptic limiting
function" for gephyrin/collybistin and partly same trans-synaptic adhesion
axis for neurexins, but the endpoint is nuclear DEG count after sparse acute
postnatal CRISPR. In that causal chain, the intervention should first perturb
local inhibitory postsynaptic assembly or receptor localization; only if that
synaptic defect propagates into activity-dependent cell-body RNA would it create
many FDR-level DEGs. The training analogs show that this propagation step was
weak or absent for the relevant synaptic genes.

## Target-specific prediction

`Nlgn2`: I predict one DEG.

The zero/nonzero decision is close. Most of the biologically appropriate
training analogs had zero downstream DE in the focal class: `Gphn`, `Nrxn2`,
`Nrxn3`, `Fyn`, and `Slc6a1` had zero total DEGs, while `Nlgn3`, `Nrxn1`,
`Arhgef9`, `Gabra1`, `Gabrg2`, and `Dlg4` had one self-only DEG each. `Gabrb2`
is the main counterexample, with a four-gene focal response that included a few
activity-regulated downstream genes, but direct receptor-subunit loss is closer
to changing inhibitory current than NL2 loss is to causing a large nuclear RNA
state.

The external prior says NL2 loss should impair inhibitory synaptic organization,
not that it should activate stress, ISR, UPR, proteasome, RNA-splicing, or
translation programs like the high-count training perturbations. The same
experiment directly shows that the NL3/neurexin/gephyrin/collybistin/GABA(A)
neighborhood is FDR-level flat or self-only under the same P16 AAV CRISPR,
P37-P44 NeuN+ snRNA-seq design. I therefore did not use the high-count global
tail of the training distribution to inflate `Nlgn2`.

I chose 1 rather than 0 because `Nlgn2` is represented among the measured genes
in the focal parquet, and the closest visible self-detectable synaptic
perturbations often score exactly one DEG through the perturbed transcript
itself. The held-out `Nlgn2` self row could fail, as `Nrxn2`, `Nrxn3`, and `Gphn`
did, but a self-only one-gene call is the best point estimate.

## Limits

The prediction is extrapolative because no `Nlgn2` perturbation, no `Nlgn1`
perturbation, no `Nlgn4` perturbation, no DNA indel fraction, no NL2 protein
staining, no gephyrin or GABA(A)-receptor puncta imaging, and no
electrophysiology were available. The focal endpoint is also power-dependent:
an FDR count of 0 or 1 could hide small coherent shifts below the Wilcoxon/BH
threshold, and a severe presynaptic or postsynaptic phenotype could be invisible
if it affected local synaptic function without a sampled survivor-state nuclear
RNA response. Finally, the neuroligin literature is rich in germline, adult
conditional, hippocampal, cortical, amygdala, and slice physiology models;
those mechanisms constrain the direction of expected synaptic effects but are
not direct measurements of acute mosaic `Nlgn2` loss in juvenile thalamic
glutamatergic nuclei.
