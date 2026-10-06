# Cacng8 DEG-count prediction trace

## Question and resolved scope

The held-out manifest for this run contains one target:

| target_name |
| --- |
| Cacng8 |

I interpreted the requested endpoint as the exact `151 TH Prkcd Grin2c Glut`
endpoint used in the training-count CSV: for a target perturbation, predict the
number of measured genes with `pvals_adj < 0.05` in the focal cell group. I
therefore ignored DE rows from other cell groups except as same-experiment
corpus context, and I used the training-count CSV, not a recomputation at a
different FDR threshold, to calibrate point counts. `Cacng8` is absent from both
the training-count file and from the parquet `gene_target` column, so there is
no direct held-out signature available.

## Sources used

- Primary data:
  `[local file: training_de_all_cell_groups.parquet]`.
  I filtered it to `group_name == "151 TH Prkcd Grin2c Glut"`, yielding
  28,891,566 focal rows over 1,674 training targets.
- Endpoint calibration:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested-target manifest:
  `[local file: 027_Cacng8.csv]`.
- Distributed Agents same-experiment corpus MCP,
  release `perturbai-july-260713-sourceguard-1773-v1`, for precomputed
  findings and claims about related training perturbations. No `Cacng8`
  context was present in that corpus; `Cacng2`, `Cacng3`, `Gria1`, `Gria2`,
  and `Gria3` were represented.
- Distributed Agents runtime `profile_neighbors`, which I used to compare the focal
  Wilcoxon-score profiles of `Cacng2`, `Cacng3`, `Gria1`, `Gria2`, `Gria3`,
  and `Dlg4` against the 1,674 eligible focal training targets. The resulting
  neighbor artifact is in `outputs/ampar_tarp_profile_neighbors.json`.
- NCBI PubMed E-utilities literature searches for Cacng8/TARP/AMPAR biology.
  The main external mechanistic anchors were Tomita et al. 2003
  (PMID 12771129, DOI `10.1083/jcb.200212116`), Yamazaki et al. 2004
  (PMID 15567474, DOI `10.1016/j.neures.2004.10.002`), Rouach et al. 2005
  (PMID 16222232, DOI `10.1038/nn1551`), Inamura et al. 2006
  (PMID 16516319, DOI `10.1016/j.neures.2006.01.004`), Cho et al. 2007
  (PMID 17880893, DOI `10.1016/j.neuron.2007.08.024`), Milstein and Nicoll
  2009 (PMID 19549880, DOI `10.1073/pnas.0905570106`), and Kato et al. 2010
  (PMID 20219255, DOI `10.1016/j.tins.2010.02.004`).

## Computations over the training data

I first checked the focal training-count distribution. Most perturbations in
this group are null: the median count is 0, the 75th percentile is 1, the 90th
percentile is 2, and the mean is inflated to 14.1 by a small tail of broad
responses such as `Uba5` at 2,677 DEGs. In this response endpoint, choosing
between 0 and 1 is therefore biologically meaningful and should be driven by
close comparators, not by the global mean.

I then pulled out AMPAR, TARP, glutamate-receptor, PSD, and CaMKII candidates
from the training counts. The focal endpoint for the closest assayed genes was:

| perturbation | role | focal `n_degs` |
| --- | --- | ---: |
| `Cacng2` | TARP gamma-2, stargazin; closest represented Cacng/TARP analog | 0 |
| `Cacng3` | TARP gamma-3 / Cacng paralog | 0 |
| `Gria1` | AMPAR pore subunit GluA1 | 0 |
| `Gria2` | AMPAR pore subunit GluA2 | 0 |
| `Gria3` | AMPAR pore subunit GluA3 | 0 |
| `Dlg4` | PSD-95 scaffold that binds TARPs through PDZ interactions | 1 |
| `Camk2a` | activity/plasticity effector downstream of glutamatergic synapses | 0 |
| `Camk2b` | CaMKII paralog; one self-transcript hit | 1 |
| `Grid1`, `Grid2` | ionotropic glutamate receptor delta subunits | 1, 0 |
| `Grik1`, `Grik3`, `Grik4`, `Grik5` | kainate receptor subunits | 0, 0, 0, 1 |
| `Grin1`, `Grin2a`, `Grin2b`, `Grin2d`, `Grin3a` | NMDAR subunits; counterexamples for receptor perturbations that can be visible | 89, 1, 2, 0, 0 |

The Cacng/AMPAR analogs were flat at the expression-pattern level, not merely
below a count threshold:

- `Cacng2`: 143 perturbed nuclei, 23,679 controls, 0 FDR<0.05 genes. The top
  focal adjusted p-values were all 1.0.
- `Cacng3`: 149 perturbed nuclei, 23,679 controls, 0 FDR<0.05 genes. The top
  focal adjusted p-values were all 1.0.
- `Gria1`: 174 perturbed nuclei, 23,679 controls, 0 FDR<0.05 genes. One gene
  had `pvals_adj = 0.2457`; the rest of the top ranks were 1.0.
- `Gria2`: 157 perturbed nuclei, 23,679 controls, 0 FDR<0.05 genes. The top
  focal adjusted p-values were all 1.0.
- `Gria3`: 132 perturbed nuclei, 23,679 controls, 0 FDR<0.05 genes. Its own
  transcript was the strongest focal row but only had `pvals_adj = 0.9707`.
- `Dlg4`: 273 perturbed nuclei, 23,679 controls, 1 FDR<0.05 gene, `Dlg4`
  itself; the next rows were not significant.

To test whether AMPAR perturbations induced a hidden compensatory receptor or
activity cassette, I queried the focal parquet for marker transcripts including
`Cacng2`, `Cacng3`, `Cacng4`, `Cacng5`, `Cacng7`, `Cacng8`, `Gria1`-`Gria4`,
`Cnih2`, `Cnih3`, `Shisa6`, `Shisa7`, `Shisa9`, `Dlg4`, `Bdnf`, `Arc`, `Fos`,
`Egr1`, and `Npas4`. For `Cacng2`, `Cacng3`, `Gria1`, and `Gria2`, every one of
these marker rows had `pvals_adj = 1.0`; for `Gria3`, the marker minimum was
its own row at `pvals_adj = 0.9707`; for `Dlg4`, the only significant marker was
the edited `Dlg4` transcript. `Cacng8` as a downstream transcript was present
but nonsignificant in the measured AMPAR/TARP perturbations, for example
`pvals_adj = 1.0` after both `Cacng2` and `Cacng3` perturbation.

Finally, I ran `profile_neighbors` on the signed Wilcoxon-score profiles of
`Cacng2`, `Cacng3`, `Gria1`, `Gria2`, `Gria3`, and `Dlg4` in the focal group.
All six anchors had either zero significant features or a single self feature,
and their best all-gene correlations against the eligible focal universe were
very small:

| anchor | FDR<0.05 features in runtime profile | strongest focal whole-profile Pearson neighbors |
| --- | ---: | --- |
| `Cacng2` | 0 | `Il1rapl1` 0.0607, `Tek` 0.0528, `Gria2` 0.0471 |
| `Cacng3` | 0 | `Pak3` 0.0685, `Nop56` 0.0671, `Uba5` 0.0622 |
| `Gria1` | 0 | `Ufc1` 0.0581, `Prpf6` 0.0553, `Psmb4` 0.0553 |
| `Gria2` | 0 | `Esrra` 0.0768, `Scn1a` 0.0682, `Plcb1` 0.0659 |
| `Gria3` | 0 | `Tecr` 0.0725, `Tmem63c` 0.0698, `Polr3b` 0.0660 |
| `Dlg4` | 1 | `Rack1` 0.0748, `Pknox2` 0.0739, `Nrp2` 0.0709 |

Those are noise-scale associations, so I did not import any unrelated
data-driven neighbor as a positive Cacng8 analog.

## Same-experiment corpus evidence

The Distributed Agents corpus did not have `Cacng8` as a target, matching its held-out
status. It did have a high-confidence claim,
`claim:a9367c3aeaad95bfae9c`, that "represented AMPAR-core and
AMPAR-trafficking/scaffold perturbations are transcriptionally buffered in basal
juvenile neurons rather than forming an interchangeable AMPAR-loss nuclear RNA
program." The contributing findings were the ones needed here:

- `Cacng2:F004`: `Cacng2` was shared-flat or nearly flat with `Cacng3`,
  `Dlg4`, `Gria1`, `Gria2`, and `Gria3`; the finding explicitly cautioned that
  `Cacng4/5/7/8`, `Cnih2/3`, and `Gria4` were not direct training targets.
- `Cacng3:F001` and `Cacng3:F003`: `Cacng3` was pan-null in recovered neuronal
  groups and had no robust whole-genome neighbor; obvious receptor-trafficking
  comparators, including `Cacng2` and `Dlg4`, were also flat.
- `Gria1:F003`, `Gria2:F004`, and `Gria3:F003`: represented AMPAR pore
  subunits did not converge on a larger AMPAR-loss RNA program, whereas
  NMDAR-subunit perturbations were detectable elsewhere in the same dataset.

I also audited the induced corpus topology over `Cacng2`, `Cacng3`, `Dlg4`,
`Gria1`, `Gria2`, and `Gria3`. All 15 possible pairs were connected by explicit
finding references and the AMPAR-core/TARP subset was tied by the shared
buffering claim. I used this as support that the focal null observations were a
coherent same-experiment neighborhood, not as a numeric weight.

## Biological rationale for Cacng8

`Cacng8` encodes TARP gamma-8, a classical transmembrane AMPA-receptor
regulatory protein. Tomita et al. 2003 defined gamma-2/stargazin, gamma-3,
gamma-4, and gamma-8 as TARPs that interact with AMPARs and promote mature
surface AMPAR expression. Yamazaki et al. 2004 showed that gamma-2, gamma-3,
gamma-4, and gamma-8 can enhance AMPAR current responses in expression systems.
Rouach et al. 2005 showed that gamma-8 controls hippocampal AMPAR number,
extrasynaptic surface expression, and long-term potentiation; Cho et al. 2007,
Milstein and Nicoll 2009, and Kato et al. 2010 further established that TARP
isoforms sculpt AMPAR trafficking, gating, and pharmacology. Inamura et al.
2006 showed that gamma-8 and stargazin have distinct membrane localization and
regulation, so `Cacng8` is not identical to `Cacng2`, but it remains in the same
postsynaptic AMPAR auxiliary-subunit mechanism.

That biology makes `Cacng2` and `Cacng3` the closest measured training analogs
for the held-out target, followed by `Gria1`-`Gria3` and `Dlg4`. All of those
were zero or self-only in `151 TH Prkcd Grin2c Glut`, and none induced Cacng8,
other TARP paralogs, AMPAR subunits, or activity-regulated genes such as `Arc`,
`Fos`, `Egr1`, `Npas4`, or `Bdnf` at FDR<0.05. Because direct AMPAR pore
subunit perturbations were also flat, I treated loss of TARP gamma-8 as likely
to perturb receptor trafficking/localization or synaptic currents without
creating a steady-state nuclear RNA state that passes this Wilcoxon/BH
threshold.

The useful counterexamples point in the same direction. `Grin1` had 89 focal
DEGs and `Cacna1g` had 12, showing that this thalamic group can produce a
multi-gene response to a membrane excitability target. However, the responses
were NMDAR- or T-type calcium-channel specific and did not extend to the
represented AMPAR/TARP/CaV auxiliary neighborhood. I therefore predicted the
strict zero endpoint rather than a small count of 1 to 2.

Predicted count:

| held-out target | predicted `n_degs` | zero/nonzero rationale |
| --- | ---: | --- |
| `Cacng8` | 0 | Closest within-dataset analogs `Cacng2`, `Cacng3`, `Gria1`, `Gria2`, and `Gria3` all had 0 focal DEGs, `Dlg4` had only a self hit, AMPAR/TARP feedback markers were not significant, and external TARP biology places Cacng8 in this same synaptic trafficking module rather than in the NMDAR/Cacna1g modules that produced broader nuclear responses. |

## Limits and weak points

- The decisive evidence is by analogy: `Cacng8` itself was held out, and the
  training universe did not include `Cacng4`, `Cacng5`, `Cacng7`, `Cnih2`,
  `Cnih3`, `Shisa6`, `Shisa7`, `Shisa9`, `Grip1`, or `Grip2` perturbations.
- Gamma-8 has isoform-specific domains and is not simply redundant with
  stargazin/gamma-2; a Cacng8-specific protein or electrophysiology phenotype
  could exist while the nuclear RNA endpoint remains zero.
- The strongest external Cacng8 literature is hippocampal and cortical, whereas
  the prediction is for `151 TH Prkcd Grin2c Glut`; I used it to identify the
  pathway and nearest paralogs, not to import hippocampal KO DEG counts.
- Sparse P16 AAV CRISPR with average target-RNA down-regulation of about 18% is
  not a germline or complete knockout model, and no DNA indel, AMPAR surface
  abundance, miniature EPSC, or protein abundance measurements are present in
  the input parquet.
- A zero prediction means that I expect no measured gene to pass
  Benjamini-Hochberg FDR 0.05 in this assay. It does not imply that TARP
  gamma-8 is biologically unimportant, successfully edited in every nucleus, or
  electrophysiologically inert.
