# Question and resolved ambiguities

The held-out manifest contains one requested perturbation, `Grik2`. I need to predict the number of measured genes with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` nuclei after acute postnatal mosaic CRISPR loss of that target.

I treated `n_degs` exactly as the focal training count file defines it: every measured transcript in the per-gene DE table is eligible, including the perturbed gene's own RNA if it passes FDR. Thus a prediction of `1` for this target would most plausibly mean "only the `Grik2` self transcript is significant"; it would not imply a broad downstream kainate-receptor program.

# Sources used

- `[local file: 099_Grik2.csv]`: requested target list. It contained only `Grik2`.
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`: focal-cell training endpoint for 1,674 observed targets.
- `[local file: training_de_all_cell_groups.parquet]`: focal-cell signed Wilcoxon scores, log2 fold changes, adjusted p-values, and matched perturbed/control nucleus counts for mechanistic analogs.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`: same-experiment interpreted findings and claims for the assayed kainate receptor targets.
- Distributed Agents runtime profile tools: signed-score comparisons within `151 TH Prkcd Grin2c Glut`.
- External PubMed literature on kainate receptor biology and GluK2/GluK5/NETO complexes:
  - Pinheiro and Mulle 2006, DOI `10.1007/s00441-006-0265-6`, PMID `16847640`.
  - Fisher and Mott 2013, DOI `10.1113/jphysiol.2013.256776`, PMID `23798491`.
  - Wyeth et al. 2014, DOI `10.1523/JNEUROSCI.3098-13.2014`, PMID `24403160`.
  - Sheng, Shi and Nicoll 2017, DOI `10.1073/pnas.1619253114`, PMID `28100490`.
  - Li et al. 2019, DOI `10.1074/jbc.RA119.008631`, PMID `31628192`.
  - Khanra et al. 2021, DOI `10.7554/eLife.66097`, PMID `33724189`.
  - Nair et al. 2021, DOI `10.1016/j.neuropharm.2021.108540`, PMID `33794245`.

# Same-experiment computations

I first summarized the 1,674 focal training counts to calibrate the endpoint. The distribution is sharply zero-inflated: 1,205/1,674 observed perturbations have no focal DEGs, the median is 0, the 75th percentile is 1, and only 59 targets have at least 50 DEGs.

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for assayed ionotropic-glutamate and postsynaptic comparators. This retrieved 17,259 measured transcripts per perturbation. Observed focal counts at FDR 0.05 were:

| training target | focal `n_degs` | comment |
| --- | ---: | --- |
| `Grik1` | 0 | assayed pore-forming kainate subunit |
| `Grik3` | 0 | assayed pore-forming kainate subunit |
| `Grik4` | 0 | high-affinity kainate subunit |
| `Grik5` | 1 | high-affinity kainate subunit; the one hit was self-depletion |
| `Gria1` | 0 | AMPA counterexample |
| `Gria2` | 0 | AMPA counterexample |
| `Gria3` | 0 | AMPA counterexample |
| `Grid1` | 1 | one self-depletion hit |
| `Grid2` | 0 | delta receptor counterexample |
| `Grin1` | 89 | clear NMDA-receptor downstream response |
| `Grin2a` | 1 | self-depletion only in this cell group |
| `Grin2b` | 2 | self plus one additional hit |
| `Grin2d` | 0 | NMDA-family but no focal hit |
| `Grin3a` | 0 | NMDA-family but no focal hit |
| `Dlg4` | 1 | PSD95 self-depletion only |
| `Shank2` | 0 | postsynaptic scaffold |
| `Cacng2` | 0 | AMPAR auxiliary subunit |

The exact focal self rows for the measured kainate genes were:

| training target | self score | self log2FC | self FDR |
| --- | ---: | ---: | ---: |
| `Grik1` | -3.417 | -0.507 | 1.000 |
| `Grik3` | -1.003 | -0.173 | 1.000 |
| `Grik4` | -0.182 | -0.073 | 1.000 |
| `Grik5` | -5.564 | -0.508 | 4.54e-4 |

So the only focal FDR hit among `Grik1/3/4/5` was the `Grik5` transcript itself. `Grik5` had no off-target downstream DEGs, and the other represented kainate targets did not even have a self row survive the 17,259-gene BH correction.

To check subthreshold expression-pattern evidence, I compared signed Wilcoxon `scores` for `Grik1`, `Grik3`, `Grik4`, and `Grik5` against the focal ionotropic/PSD panel and against the whole eligible set of 1,674 training targets. I used:

```python
context = {"group_name": "151 TH Prkcd Grin2c Glut"}
value_column = "scores"
significance_column = "pvals_adj"
significance_threshold = 0.05
top_k_features = 500
```

The profile activity table again showed 0 significant features for `Grik1`, `Grik3`, and `Grik4`, and 1 negative significant feature for `Grik5`. Pairwise correlations from each kainate anchor to AMPAR, NMDA, GRID, `Dlg4`, and `Shank2` comparators were near zero: among the 40 requested kainate-vs-panel pairs, the largest cosine was only 0.0856 for `Grik1` vs `Grin1`; most absolute cosines were below 0.04. Whole-eligible nearest neighbors were also weak and biologically scattered, with the top whole-profile Pearson values of only 0.077 for `Grik1`, 0.095 for `Grik3`, 0.104 for `Grik4`, and 0.109 for `Grik5`. Top-500 signed-tail overlaps were similarly small, with leading same-tail overlap fractions around 0.09 to 0.12 rather than a coherent module.

The Distributed Agents corpus independently summarizes the represented kainate subunits in the same direction. Its high-confidence claim `claim:2eb3c1f67e285c7f7a99` states that `Grik1`, `Grik3`, `Grik4`, and `Grik5` "do not form a shared basal neuronal transcriptomic response module" in this postnatal mosaic screen. The supporting `Grik5:F002`, `Grik4:F002`, `Grik3:F003`, and `Grik1:F003` findings explicitly note that `Grik2` and `Neto1/2` were not assayed, but that the assayed kainate relatives were flat, near-zero, or idiosyncratic rather than convergent. `Grik5:F003` further contrasts flat `Grik5` with detectable `Grin1` activity/synaptic RNA output in this same 151 thalamic cell group, which matches the direct focal counts above.

# Target-specific prediction: `Grik2`

`Grik2` encodes GluK2, one of the low-affinity pore-forming kainate receptor subunits. Kainate receptors are ligand-gated ionotropic glutamate receptors with prominent pre- and postsynaptic roles in neurotransmitter release, excitability, and plasticity rather than a direct transcription-factor-like role (Pinheiro and Mulle 2006; Nair et al. 2021). GluK2 can form homomeric channels and can co-assemble with high-affinity GluK5 in heteromeric receptors; GluK4/5 need a low-affinity GluK1/2/3 partner for functional channels, and GluK2/GluK5 receptors assemble with two copies of each subunit (Fisher and Mott 2013; Khanra et al. 2021). Neto1 and Neto2 auxiliary proteins regulate KAR trafficking, synaptic localization, and gating, including for GluK2-containing receptors (Wyeth et al. 2014; Sheng et al. 2017; Li et al. 2019).

Those mechanisms make the observed `Grik1`, `Grik3`, `Grik4`, and especially `Grik5` perturbations the closest same-assay analogs. They also argue against borrowing the broad `Grin1` count: NMDA receptor loss changes calcium-dependent activity and stress/plasticity transcripts in this thalamic group, whereas the represented kainate receptors behaved as synaptic physiology genes with little or no basal nuclear RNA response. AMPA receptors and postsynaptic scaffolds were also flat or self-only in the focal group.

The one reason to consider a nonzero point was the possibility that `Grik2` itself, like `Grik5`, would pass as an on-target depleted transcript. I did not assign that hit because focal self-detection was inconsistent across nearby receptors: `Grik1` had essentially the same self log2FC as `Grik5` but FDR 1.0 with fewer perturbed nuclei, while `Grik3` and `Grik4` had no meaningful self depletion. A held-out `Grik2` guide set could therefore land on either side of the self-row threshold, and there is no same-experiment evidence for an additional downstream `Grik2` signature to pull the prediction above zero.

I therefore predict no focal genes, including the `Grik2` transcript, will clear FDR 0.05.

# Limits

This is an extrapolation because `Grik2` itself, `Neto1`, and `Neto2` were not observed as perturbation targets. GluK2 is not a perfect substitute for GluK1, GluK3, GluK4, or GluK5: it has its own expression pattern, can traffic efficiently without Neto proteins in some contexts, and occupies the pore-forming position in GluK2/GluK5 heteromers. The CRISPR screen also measured somatic nuclear RNA after 3 to 4 weeks, not KAR currents, surface trafficking, synapse localization, or behavior. A flat `n_degs` prediction should therefore be read only as a prediction about the FDR 0.05 snRNA-seq endpoint in `151 TH Prkcd Grin2c Glut`, not as a prediction that GluK2 biology is inert.
