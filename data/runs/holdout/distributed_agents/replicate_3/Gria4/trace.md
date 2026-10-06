# DEG count prediction trace

## Question and ambiguity resolution

The task is to predict, for each gene in
`098_Gria4.csv`, the held-out value of `n_degs`: the number of measured genes
with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after CRISPR loss
of that gene in `151 TH Prkcd Grin2c Glut` nuclei.

There is one requested held-out target: `Gria4`.

I treated `n_degs` exactly as in the supplied focal-cell training count table:
the perturbed target's own transcript is included if it passes FDR, and zero
means that no measured transcript, including the target transcript, reaches
FDR 0.05. The target was not present as a perturbation in the training parquet,
so there was no direct same-experiment `Gria4` DE signature to inspect.

## Sources used

- Training endpoint CSV:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Training differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested-target manifest:
  `[local file: 098_Gria4.csv]`
- Same-experiment semantic layer: Distributed Agents corpus MCP,
  release `perturbai-july-260713-sourceguard-1773-v1`
- Same-experiment profile tooling: Distributed Agents runtime `profile_compare` over the
  focal-cell parquet profiles
- External literature from NCBI PubMed:
  - Paz et al. 2011, `Nature Neuroscience`, DOI `10.1038/nn.2896`,
    PMID `21857658`
  - Barad et al. 2012, `Neuroscience`, DOI
    `10.1016/j.neuroscience.2012.05.011`, PMID `22609941`
  - Nicoll, Tomita and Bredt 2006, `Science`, DOI
    `10.1126/science.1123339`, PMID `16513974`
  - Schwenk et al. 2009, `Science`, DOI `10.1126/science.1167852`,
    PMID `19265014`
  - Diaz 2010, `European Journal of Neuroscience`, DOI
    `10.1111/j.1460-9568.2010.07357.x`, PMID `20946114`

## Computation over the supplied training data

The training count table has 1,674 focal-cell perturbations; 1,205 of them
have `n_degs = 0`, 363 have 1-9 DEGs, 63 have 10-99, and 43 have 100 or more.
Thus a zero prediction is common but not automatic; strong focal-cell
responders such as `Grin1` and `Atp1a3` are present when this cell class mounts
a detectable response.

To inspect receptor and postsynaptic analogs directly in the parquet, I used
the parquet row-group statistics for `group_name` and read only row groups
whose min/max bracketed `151 TH Prkcd Grin2c Glut`. I then filtered the rows to
the AMPAR, kainate, NMDAR and scaffold candidates below and counted
`pvals_adj < 0.05` for each target. This reproduced the scalar CSV values.

| training perturbation | focal `n_degs` | focal-cell expression evidence |
| --- | ---: | --- |
| `Gria1` | 0 | no FDR<0.05 transcript; its own transcript had `pvals_adj = 1`; `Gria4` as a measured transcript also had `pvals_adj = 1` |
| `Gria2` | 0 | no FDR<0.05 transcript; its own transcript had `pvals_adj = 1`; no `Gria4` change |
| `Gria3` | 0 | no FDR<0.05 transcript; self log2FC -0.414 but `pvals_adj = 0.9707`; no `Gria4` change |
| `Cacng2` | 0 | no FDR<0.05 transcript; AMPAR/TARP measured rows, including `Gria4`, were all FDR=1 |
| `Cacng3` | 0 | no FDR<0.05 transcript |
| `Dlg4` | 1 | only the target transcript, `Dlg4`, passed FDR; no downstream AMPAR response |
| `Grik1` | 0 | no FDR<0.05 transcript |
| `Grik3` | 0 | no FDR<0.05 transcript |
| `Grik4` | 0 | no FDR<0.05 transcript |
| `Grik5` | 1 | only the target transcript, `Grik5`, passed FDR |
| `Grin1` | 89 | broad response: 40 upregulated and 49 downregulated FDR genes |
| `Grin2a` | 1 | only the target transcript, `Grin2a`, passed FDR |
| `Grin2b` | 2 | `Grin2b` and `Pianp` passed FDR |
| `Grin2d` | 0 | no FDR<0.05 transcript |
| `Grin3a` | 0 | no FDR<0.05 transcript |
| `Shank2` | 0 | no FDR<0.05 transcript |
| `Shank3` | 2 | a small two-gene call, `Shank3` and `Uba5`, not an AMPAR subunit program |

The matched perturbed-nucleus counts for the three closest paralogs were 174
for `Gria1`, 157 for `Gria2`, and 132 for `Gria3`; `Cacng2` and `Cacng3` had
143 and 149. These are in the same range as other weak-but-detectable targets,
so the all-zero AMPAR-core result in `151` is not explained by a single gross
low-power outlier.

The Distributed Agents runtime profile comparison over the same `151` rows gave the
same activity classes: `Gria1`, `Gria2`, `Gria3`, and `Cacng2` each had zero
significant features, while `Grin1` had 89. Pairwise focal-cell comparisons
between each AMPAR paralog and the receptor/scaffold peers had zero shared
significant features. I therefore did not use continuous whole-profile
correlations among these near-null signatures as quantitative weights, because
their top features were nonsignificant.

## Target-specific reasoning for `Gria4`

`Gria4` encodes the GluA4 AMPA-receptor pore-forming subunit. The closest
training perturbations are the represented AMPAR-core genes `Gria1`, `Gria2`,
and `Gria3`; all three are direct paralogs, all encode GluA subunits of the
same receptor family, and all had `n_degs = 0` in `151 TH Prkcd Grin2c Glut`.
This is the decisive within-dataset evidence. In the same focal cell class,
acute loss of a GluA1, GluA2, or GluA3 subunit did not produce even a one-gene
FDR<0.05 response.

The Distributed Agents corpus independently summarized the broader same-experiment AMPAR
neighborhood. `Gria1:F003`, `Gria2:F004`, and `Gria3:F003` all contrasted the
AMPAR subunits with auxiliary/scaffold genes and concluded that represented
AMPAR-core and AMPAR-trafficking perturbations were buffered or near-null in
basal juvenile neuronal snRNA-seq. The high-confidence corpus claim
`claim:a9367c3aeaad95bfae9c` made the same point at the module level:
represented AMPAR-core, TARP, and postsynaptic-scaffold losses did not form a
shared AMPAR-loss nuclear RNA program.

The best AMPAR-complex comparators outside the pore-forming paralogs also
support the zero call. `Cacng2` and `Cacng3`, transmembrane AMPAR regulatory
proteins, were both zero in the focal group. `Dlg4`, a PSD-95 scaffold for
AMPAR/NMDAR postsynaptic organization, had one significant row, but it was its
own target transcript. `Shank2` was zero and `Shank3` had only two genes. The
external literature agrees that TARPs, cornichons, and related accessory
proteins regulate AMPAR trafficking and gating rather than necessarily driving
basal transcription: Nicoll et al. 2006 and Diaz 2010 reviewed TARP control of
AMPAR trafficking/channel properties, and Schwenk et al. 2009 identified CNIH2
and CNIH3 as native AMPAR auxiliary subunits that regulate AMPAR surface
expression and gating.

`Grin1` is the important counterexample rather than the template. It encodes
the obligatory NMDA-receptor subunit and had 89 focal DEGs, including a mixed
synaptic, ion-channel, growth/plasticity and stress-linked response. The
corpus `Gria1:F004`, `Gria2:F003`, and `Gria3:F003` findings use NMDAR
subunits to show that ionotropic glutamate receptors are not invisible to this
assay, but they also show that AMPAR loss does not phenocopy the NMDAR
calcium-to-nucleus response. Other NMDAR members were weak or absent in this
focal group (`Grin2a` 1, `Grin2b` 2, `Grin2d` 0, `Grin3a` 0), reinforcing that
same receptor family membership alone is insufficient.

External biology prevents treating `Gria4` as a meaningless orphan: GluA4 is
prominent in thalamic AMPAR physiology, and germline `Gria4` deficiency alters
corticothalamic transmission and absence-epilepsy circuitry in mouse
thalamus (Paz et al. 2011; Barad et al. 2012). That makes `Gria4` a plausible
electrophysiological perturbation. However, those data are in germline
thalamocortical/reticular-circuit settings, not sparse P16 CRISPR in recovered
postmitotic thalamic glutamatergic nuclei. The same-experiment AMPAR evidence
therefore has the stronger calibration for this FDR-count endpoint.

## Final decision

I predict `Gria4` will be nonresponsive at FDR 0.05 in `151 TH Prkcd Grin2c
Glut`: `predicted_n_degs = 0`.

The prediction is driven primarily by the supplied training data and the
Distributed Agents same-experiment corpus over `Gria1`, `Gria2`, `Gria3`, `Cacng2`,
`Cacng3`, and `Dlg4`. External AMPAR literature was used to verify that these
are mechanistically appropriate comparators and to bound the extrapolation from
receptor physiology to a nuclear RNA count.

## Limits

`Gria4` itself was held out, so there is no direct perturbation signature,
self-transcript FDR value, matched nucleus count, or corpus report for it. The
prediction assumes GluA4 loss behaves like the represented GluA1-GluA3 losses
in this specific basal snRNA-seq endpoint. That is biologically plausible but
imperfect: GluA4 expression is thalamus-enriched, its germline knockout has
thalamocortical circuit consequences, and a strong reduction of the `Gria4`
transcript itself could in principle yield a one-gene focal count. The
training data nevertheless show that focal-cell AMPAR-core and AMPAR-trafficking
perturbations usually land at exactly zero, whereas broad nonzero receptor
responses in this class are NMDAR-specific or unrelated stress/trafficking
states.
