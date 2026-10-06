# Srgap3 DEG-count prediction

## Question and resolved ambiguities

The requested held-out target list is:

```text
Srgap3
```

I interpreted the task as a point prediction for `n_degs`, the number of measured transcripts with
`pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` differential-expression table after an
acute P16 AAV-CRISPR loss-of-function perturbation. The target itself is counted if the perturbed
gene's own RNA passes FDR 0.05; it is not excluded as a QC feature. The focal cell label is the
thalamic glutamatergic `151` class, not a tyrosine-hydroxylase class.

`Srgap3` was absent from both supplied training files, so no held-out `Srgap3` DEG count or
signature was used. The decision is an extrapolation from represented pathway neighbors plus
external SRGAP3 biology.

## Sources used

- Supplied focal endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Supplied DE Parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested held-out manifest:
  `[local file: 221_Srgap3.csv]`
- Distributed Agents selected same-experiment corpus release:
  `perturbai-july-260713-sourceguard-1773-v1`
- Distributed Agents runtime pairwise profile tools over the provided Parquet, used only on non-held-out
  observed profiles.
- PubMed literature on SRGAP3/WRP and the WAVE/Rac actin pathway.
- Reactome pathway entries cited inside the same-experiment corpus for
  RAC1:GTP/WAVE regulatory complex and RAC1/CDC42/PAK1 signaling.

## Dataset calculations

I loaded the focal training-count CSV and summarized the empirical count distribution in the
cell group to calibrate sparsity:

- 1,674 training perturbations were present.
- 1,205/1,674 had `n_degs = 0`.
- The median was 0, the 75th percentile was 1, the 95th percentile was 18, and the maximum was
  2,677.

I then filtered the Parquet to the focal cell group and a hand-curated Rho/Rac/WAVE/cytoskeletal
cohort:

```python
pd.read_parquet(
    de_parquet,
    columns=["names", "gene_target", "logfoldchanges", "pvals_adj",
             "group_name", "n_pert_matched", "n_ctrl_matched"],
    filters=[
        ("group_name", "==", "151 TH Prkcd Grin2c Glut"),
        ("gene_target", "in", analog_targets),
    ],
)
```

For each analog I checked the exact FDR-significant genes, the top subthreshold genes, and matched
perturbed/control nucleus counts. I also computed symmetric pairwise logFC-profile comparisons
among 18 represented relatives using the Distributed Agents runtime in the exact focal context. That
profile comparison showed that the inspected Rho/Rac/WAVE pairs shared no FDR-supported focal
features; the apparent whole-profile correlations were correlations between nearly flat vectors
with no shared significant downstream program.

As a guard for the target-self ambiguity, I counted self-target rows in the focal Parquet:
1,642 training targets had `names == gene_target` rows in this cell group, and 319/1,642
(19.4%) had their own transcript significant at FDR 0.05. This makes an isolated `Srgap3`
self hit possible but not the default.

## Target-specific evidence

### Srgap3

`Srgap3`, also called `WRP`/`MEGAP`, encodes a Slit-Robo Rho GTPase-activating protein with an
inverse F-BAR domain, a RhoGAP domain, and an SH3 domain. The protein is a local neuronal
cytoskeletal regulator rather than a nuclear transcription factor: WRP/SRGAP3 binds WAVE-1,
anchors a Rac-to-WAVE/Arp2/3 actin-remodeling complex, and contributes to dendritic spine
initiation and synaptic plasticity. Soderling et al. 2007 showed that a WAVE-1/WRP complex
regulates spine density, synaptic plasticity, and memory (J Neurosci,
doi:10.1523/JNEUROSCI.3209-06.2006). Carlson et al. 2011 showed that the WRP IF-BAR domain
facilitates spine initiation and that WRP loss impairs learning and memory
(J Neurosci, doi:10.1523/JNEUROSCI.4433-10.2011). Chen et al. 2011 found that srGAP3 binds
activated Rac1 and regulates Neuro2A neuronal differentiation in a Rac1-dependent way
(Cell Mol Neurobiol, doi:10.1007/s10571-011-9664-7). Ma et al. 2013 supported functional
interplay among srGAP1-3 and placed srGAP3 in Slit-Robo-dependent neurite biology
(PLoS One, doi:10.1371/journal.pone.0057865). Waltereit et al. 2012 reported that germline
`Srgap3` knockout mice have increased basal RAC1 activity, altered spines/white matter, and
behavioral phenotypes (FASEB J, doi:10.1096/fj.11-202317). Bacon et al. 2012 reviewed SRGAP3
as a Rac-inhibitory actin regulator linked to spine development and intellectual disability
(Mech Dev, doi:10.1016/j.mod.2012.10.005).

The closest mechanistic training perturbations available in the focal endpoint were all tiny:

| training target | focal `n_degs` | expression-pattern evidence and relevance |
| --- | ---: | --- |
| `Arhgap32` | 0 | A neuronal Rac/Rap GAP and the closest represented GAP-style counterexample. In `151 TH Prkcd Grin2c Glut`, 180 perturbed nuclei versus 23,679 controls produced no FDR 0.05 genes; even `Arhgap32` itself was only logFC -0.333, FDR 0.607. The same-experiment corpus summarized it as a negative result with no meaningful unbiased Arhgap32 convergence or opposition. |
| `Arhgap18` | 0 | Rho-family GAP included in the corpus' Cdc42/Rac comparator set. It had 201 perturbed focal nuclei and no focal FDR 0.05 genes. |
| `Rac1` | 0 | Direct substrate-side analog. Although SRGAP3 inhibits Rac1 and Rac1 feeds WAVE/PAK actin effectors, focal `Rac1` loss had 193 perturbed nuclei and zero FDR 0.05 genes. The corpus found the whole postnatal Rac1 surface transcriptionally buffered, with only a single Ranbp1 event outside this focal cell group and no meaningful genome-wide signature neighbor. Reactome curates RAC1:GTP binding to WAVE regulatory complex through CYFIP1/CYFIP2, and the same-experiment Rac1 finding explicitly compared `Cdc42`, `Pak1`, `Pak2`, `Pak3`, `Limk1`, `Tiam1`, `Kalrn`, `Cyfip1`, `Cyfip2`, `Arhgap18`, `Arhgap32`, `Fyn`, `Sos1`, and `Dock3`, which did not reproduce the Rac1 event. |
| `Cdc42` | 1 | Parallel Rho-family GTPase. Its only focal DEG was `Cdc42` itself, logFC -0.593, FDR 8.6e-5, in 122 perturbed nuclei; there were no downstream focal genes. Distributed Agents `Cdc42:F003` reported that represented Rho/Rac/Cdc42 relatives, including `Rac1`, `Pak1-3`, `Limk1`, `Cfl2`, `Cyfip1/2`, `Tiam1`, `Kalrn`, `Dock3`, `Fgd4`, `Arhgap18`, `Arhgap32`, and `Arhgef9`, were flat or single-gene responders and did not form a shared module. |
| `Pak1` | 1 | RAC1/CDC42 effector-side analog. The focal FDR hit was only `Pak1` itself, logFC -0.599, FDR 5.0e-8, with no downstream transcript. The same-experiment corpus reported that `Pak1` was essentially uncoupled from represented Rac/Cdc42/LIMK and MEK/MAPK nodes. |
| `Pak2` | 0 | Group-I PAK paralog; 163 focal perturbed nuclei, no FDR 0.05 genes. The corpus found no FDR 0.10 downstream transcriptome in any recovered neuronal cell group. |
| `Pak3` | 0 | Neuronal group-I PAK paralog; 188 focal perturbed nuclei, no FDR 0.05 genes. Its corpus-supported singleton response was outside this cell group. |
| `Limk1` / `Cfl2` | 0 / 0 | Downstream actin-turnover nodes in the RAC/CDC42-to-PAK cascade; both were focal zeros. |
| `Cyfip1` | 0 | WAVE-regulatory-complex component that links RAC1 signaling to actin remodeling and FMRP-associated translation. It had 192 focal perturbed nuclei, `Cyfip1` logFC -0.082/FDR 1, and no focal FDR 0.05 genes. The same-experiment corpus classified it as transcriptionally buffered in all measured neuronal groups. |
| `Cyfip2` | 1 | WRC paralog. Its only focal DEG was `Cyfip2` itself, logFC -0.489, FDR 4.39e-11, in 218 perturbed nuclei; the same-experiment corpus found no downstream FDR 0.10 genes across measured groups. |
| `Tiam1`, `Kalrn`, `Dock3`, `Fgd4`, `Fyn`, `Sos1` | 0 each | Represented GEF/upstream signaling comparators from the Rac/Cdc42 corpus findings; all were focal zeros. |
| `Fmr1`, `Fxr1`, `Gphn` | 0 each | Less direct synaptic/cytoskeletal counterexamples. `Fmr1`/`Fxr1` probe the CYFIP translation side of WRC biology, and `Gphn` probes collybistin/`Arhgef9` inhibitory postsynaptic scaffolding. None produced a focal FDR 0.05 gene. |

The informative pattern is therefore not one matching strong profile but a repeated absence of
detectable downstream transcriptional breadth for the represented local actin regulators. The
only nonzero focal counts in the direct cohort were isolated self-transcript hits in `Cdc42`,
`Pak1`, `Arhgef9`, and `Cyfip2`; they are evidence that a target transcript can contribute a
single DEG, but they are not evidence for a broader SRGAP3-like nuclear program.

## Prediction

I predict `Srgap3` will have **0** DEGs in `151 TH Prkcd Grin2c Glut`.

The within-dataset evidence drove the zero/nonzero decision. `Srgap3` is expected to perturb
Rac/WAVE actin dynamics locally at developing synapses and neurites; in this P16-to-P37/44 sparse
postmitotic CRISPR design, the assayed Rho-family GAP/GEF/GTPase/PAK/WRC/CYFIP relatives were
almost all zero-count or self-only in the same focal population. External biology argues that
`Srgap3` is important for spine morphogenesis and neurodevelopment, but it does not make it more
similar to the broad training responders in this cell group, which were dominated by splicing,
proteostasis, transcriptional, and signaling perturbations that drove many FDR-supported RNA
changes.

I chose `0` rather than `1` for a target-self-only call because the most analogous represented
GAPs, `Arhgap32` and `Arhgap18`, lacked focal self hits, and the WRC-side `Cyfip1` was also a
complete focal zero despite direct relevance to SRGAP3/WRP signaling. The global 19.4% self-hit
rate in the focal group leaves uncertainty, but it is below the majority pattern, and `Srgap3`
has no held-out evidence suggesting its nuclear RNA should be one of the high-confidence
self-depleted transcripts.

## Limits

This prediction is extrapolative. The training table lacked `Srgap1` and `Srgap2`, so I could not
calibrate against the closest paralogs. The assay measures recovered postmitotic neuronal nuclei
3-4 weeks after mosaic AAV-CRISPR editing, not embryonic germline loss, spine morphology, axon
guidance, electrophysiology, or RAC1-GTP. A true SRGAP3 morphologic phenotype could be
transcriptionally silent in snRNA-seq, and a significant `Srgap3` self-transcript reduction alone
would change the observed count from 0 to 1 even without any downstream response. Finally, the
same-experiment corpus had no direct `Srgap3` report, so SRGAP3-specific reasoning came from
PubMed literature rather than a curated in-corpus target entry.
