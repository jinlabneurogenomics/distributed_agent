# Reasoning trace

## Question and ambiguity resolution

The requested readout is the held-out value of `n_degs` for each target in
`220_Sp4.csv`, where `n_degs` is the number of measured genes with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in
`151 TH Prkcd Grin2c Glut` after sparse P16 AAV-CRISPR perturbation.  The
manifest contained one target:

| target_name |
|---|
| Sp4 |

I treated this as a prediction for an acute, mosaic, postnatal loss-of-function
experiment, not as a germline Sp4-null or strong shRNA knockdown phenotype.  A
zero prediction would mean no focal-cell gene crosses the supplied FDR cutoff;
a small positive prediction means the perturbation is expected to have an
assay-detectable response but only a handful of DEGs.

## Sources used

- `training_de_all_cell_groups.parquet`, filtered to
  `group_name == "151 TH Prkcd Grin2c Glut"`.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` for observed focal-cell
  DEG counts in the 1,674 non-held-out targets.
- The requested-target manifest `220_Sp4.csv`.
- Distributed Agents corpus MCP release
  `perturbai-july-260713-sourceguard-1773-v1`.  `target_context("Sp4")`
  returned no same-experiment target-centered Sp4 record in this release, so I
  used the corpus mainly to check same-assay claims for CREB, Mef2, and other
  postnatal neuronal transcription-factor comparators.
- Distributed Agents runtime profile tools:
  `profile_neighbors`, `profile_compare`, and `profile_inspect` compared
  observed expression signatures in the focal group with `logfoldchanges` as
  the signed value and `pvals_adj < 0.05` as the significance threshold.
- Public PubMed-indexed Sp4 literature:
  Ramos et al. 2007, PNAS, DOI `10.1073/pnas.0701946104`, PMID `17535924`;
  Ramos et al. 2009, Molecular and Cellular Neuroscience, DOI
  `10.1016/j.mcn.2009.06.008`, PMID `19555762`;
  Zhou et al. 2010, Human Molecular Genetics, DOI `10.1093/hmg/ddq298`,
  PMID `20634195`;
  Priya et al. 2013, BBA, DOI `10.1016/j.bbamcr.2013.07.002`,
  PMID `23871830`;
  Priya et al. 2014, BBA, DOI `10.1016/j.bbamcr.2014.02.008`,
  PMID `24576410`;
  Saia et al. 2014, Journal of Neurochemistry, DOI `10.1111/jnc.12657`,
  PMID `24475768`;
  Sun et al. 2014, Developmental Neurobiology, DOI `10.1002/dneu.22212`,
  PMID `25045015`;
  Lalonde et al. 2014, Science Signaling, DOI `10.1126/scisignal.2005242`,
  PMID `24894994`;
  Nair et al. 2015, BBA, DOI `10.1016/j.bbamcr.2015.10.005`,
  PMID `26469128`.

## Dataset computations

1. I read the focal training count CSV and counted 1,674 training perturbations.
   The distribution is very sparse: 469/1,674 perturbations are nonzero, the
   median is 0 DEGs, the 75th percentile is 1 DEG, the 90th percentile is 2
   DEGs, and only the top 5% exceed 18 DEGs.  The maximum count is 2,677
   (`Uba5`).

2. I selected biologically plausible Sp4 comparators:

   - receptor and synapse nodes downstream or adjacent to reported Sp4 biology:
     `Grin1`, `Grin2a`, `Grin2b`, `Grin2d`, `Dlg4`;
   - activity-dependent or neuronal transcription-factor anchors:
     `Creb1`, `Mef2a`, `Mef2c`, `Mef2d`, `Klf9`;
   - thalamic transcriptional controls from the same focal group:
     `Zeb1`, `Ctbp1`;
   - GC-box/zinc-finger negative controls or weak KLF controls:
     `Sp7`, `Klf1`, `Klf7`;
   - a cortical developmental TF counterexample, `Tbr1`;
   - `Nrf1`, because in vitro work links Sp4 with NRF-family control of
     glutamate-receptor and oxidative-phosphorylation promoters.

3. I used `profile_compare` over the curated set in the focal group and an
   eligible universe of all 1,674 training targets.  Each candidate had an
   available 17,259-feature profile.  Within this curated set, five anchors had
   no FDR-level features and seven had only 1 to 9 significant features.  The
   strongest mechanistic anchors did not form a shared significant module: for
   example, `Creb1`, `Mef2a`, `Mef2c`, `Klf9`, `Grin1`, and the receptor
   subunits had zero same-direction intersections among their significant
   upregulated or downregulated genes in the inspected pairs.  Whole-profile
   Pearson/cosine similarities were therefore interpreted cautiously because
   they were driven by many weak, non-significant ranks.

4. I performed a targeted parquet read for the focal rows of the curated
   anchors and recorded the actual FDR-level genes and matched nucleus counts.
   This was used to distinguish self-target-only responses from small
   downstream modules.

## Target-specific reasoning: Sp4

### Biological prior

Sp4 is a neuron-enriched specificity-protein transcription factor rather than a
generic osteogenic or erythroid Sp/KLF factor.  In developing cerebellar
granule neurons, Sp4 knockdown increases dendrite number and blocks
activity-dependent pruning (Ramos et al. 2007), and Sp4 directly represses
`Ntf3` to limit dendritic branching (Ramos et al. 2009).  Sp4 hypomorphic mice
have impaired hippocampal LTP and reduced NMDAR1 protein (Zhou et al. 2010).
Sun et al. 2014 connected Sp4 to `Fchsd1`/Nwk2 and NMDAR1 surface expression,
and Priya et al. 2013, Priya et al. 2014, and Nair et al. 2015 reported
Sp4-dependent regulation of NMDA, AMPA, and GABA receptor-subunit promoters in
neurons.  Sp4 is also post-translationally controlled by membrane
depolarization, NMDA receptor signaling, and store-operated calcium entry
(Saia et al. 2014; Lalonde et al. 2014).

That biology argues against treating held-out `Sp4` like irrelevant
non-neuronal GC-box factors, but it also does not imply a broad bulk
transcriptional collapse in this assay.  Much of the direct evidence comes from
cultured cerebellar granule neurons, promoter assays, or chronic hypomorphs,
whereas the endpoint here is basal nuclear RNA in postnatal thalamic
glutamatergic nuclei after sparse editing.

### Same-experiment analogs and counterexamples

| training perturbation | observed focal `n_degs` | expression-pattern evidence and interpretation |
|---|---:|---|
| `Grin1` | 89 | Obligatory NMDAR subunit.  In the focal parquet it was the only broad receptor anchor: `Grin1` itself was strongly down (`logFC=-1.064`, FDR `3.3e-53`) and 88 other genes passed.  This bounds Sp4 on the high side; Sp4 can influence NMDAR trafficking and receptor promoters, but Sp4 loss is upstream/modulatory and Sun et al. specifically saw surface, not total, NR1 changes after acute Sp4 depletion. |
| `Grin2a` | 1 | Self-target-only FDR signal (`Grin2a`, `logFC=-0.492`, FDR `0.002`).  Direct GluN2A subunit loss was transcriptionally sparse in these TH neurons. |
| `Grin2b` | 2 | `Grin2b` itself and `Pianp` passed FDR.  This again argues that changing an Sp4-regulated NMDA subunit need not generate a large secondary nuclear-RNA response. |
| `Grin2d` | 0 | No FDR-level genes; `Grin2d` target RNA was only weakly changed.  This is a lower-bound receptor counterexample. |
| `Dlg4` | 1 | Only `Dlg4` itself passed FDR.  A core postsynaptic-density perturbation produced almost no secondary transcriptome in this cell group. |
| `Creb1` | 10 | A small CRE-family TF response with induced `Crem` and nine additional DEGs.  Distributed Agents same-assay claims describe basal `Creb1` loss as detectable in 151 TH Prkcd Grin2c Glut but not phenocopied by proximal cAMP/PKA perturbations.  This is the closest activity-regulated TF scale for Sp4. |
| `Mef2a` | 4 | Four DEGs (`Gpr4`, `Prkcg`, `Ogt`, `Sez6`) despite MEF2 factors being canonical calcium/activity-linked neuronal TFs.  This supports a one-digit prediction. |
| `Mef2c` | 1 | Only the target transcript `Mef2c` passed.  The Distributed Agents corpus describes postnatal TF responses as factor-specific, with `Mef2c` sometimes detectable but not interchangeable with other developmental TF axes. |
| `Mef2d` | 0 | No FDR-level focal response, setting a null bound for an active neuronal TF family member. |
| `Klf9` | 19 | A neuronal zinc-finger TF with a small coherent positive response including `Wsb1`, `Rasgrp2`, `Pld3`, `Dzip1`, `Maged2`, and `Mest`.  It is not an Sp-family paralog but is a useful GC-rich DNA-binding comparator that is expressed and detectably active. |
| `Zeb1` | 15 | A private thalamic upregulated module with `Stxbp2`, `Ap1m2`, `F11r`, and others.  It shows that this focal group can expose small TF modules, but the Ctbp1/Zeb1 module is mechanistically unrelated to Sp4 and was not used as a direct phenocopy. |
| `Ctbp1` | 5 | Shared the `Stxbp2`/`F11r`/`Ap1m2` module with `Zeb1`; useful as a one-digit thalamic TF/repressor scale, not as an Sp4 pathway member. |
| `Nrf1` | 138 | External promoter studies put NRF factors near Sp4 on AMPA/NMDA and energy-metabolism genes.  In this assay, though, Distributed Agents claims indicate that the ERR/PGC/PPAR/NRF network is node-specific; `Nrf1` was an oxidative-metabolism response rather than a glutamatergic-receptor or Sp4-like signature.  I treated 138 as too high for Sp4. |
| `Sp7` | 0 | A same-family Sp transcription factor but osteoblast-lineage rather than neuronal.  It is a family-name counterexample, not a biological analog. |
| `Klf1` | 0 | Erythroid KLF factor; confirms that unrelated GC-box TFs are silent in this postnatal neuronal endpoint. |
| `Klf7` | 1 | One DEG (`Tuba1a`), consistent with weak KLF-family effects in this focal group. |
| `Tbr1` | 0 | A neuronal developmental TF that was flat in this thalamic group; useful as a reminder that TF annotation alone does not imply retained postnatal activity. |

The observed profiles did not reveal an assayed upstream node that repeatedly
shifted measured `Sp4` expression.  Across all 1,674 focal training
perturbations, `Sp4` itself was FDR-significant only under `Rab7` loss
(`logFC=-0.537`, FDR `0.043`), a broad 501-DEG vesicle/lysosome response rather
than a specific Sp4 pathway.  That removes support for predicting a broad Sp4
perturbation by borrowing from a same-signature parent.

### Zero/nonzero decision and point estimate

I predicted a nonzero response because Sp4 is a neuronal transcription factor
with direct evidence for regulating dendritic and receptor programs, whereas
the irrelevant Sp/KLF controls (`Sp7`, `Klf1`) are flat for obvious biological
reasons.  I kept the point estimate small because the closest same-assay
neuronal TF and synaptic analogs are sparse: `Mef2a` has 4 DEGs, `Mef2c` has 1,
`Mef2d` has 0, `Creb1` has 10, `Ctbp1` has 5, and most NMDAR/PSD subunit
perturbations have 0 to 2.  `Grin1`, `Klf9`, `Zeb1`, and `Nrf1` show that
larger responses are possible in this cell group, but each has a private
mechanism that would overstate an acute Sp4 loss prediction.

The resulting call for `Sp4` is therefore **4 DEGs**.

## Limits

- There is no observed Sp-family neuronal paralog in the training set:
  `Sp1`, `Sp2`, and `Sp3` were absent, and `Sp7` is a poor osteogenic
  counterexample.  This is a cross-pathway extrapolation.
- The Distributed Agents corpus had no Sp4-centered internal record, so target-specific
  Sp4 biology came from public literature rather than a same-experiment Sp4
  neighborhood.
- Cultured cerebellar granule neuron Sp4 knockdown and promoter assays need not
  match basal P16-to-P37/44 CRISPR in thalamic glutamatergic nuclei.
- Protein-level Sp4 regulation by phosphorylation and degradation can alter
  neuronal morphology without producing many nuclear RNA DEGs at the sampling
  time used here.
- Counts near zero are intrinsically fragile: with this training distribution,
  a target predicted as 4 DEGs could plausibly resolve as a self-target-only or
  10-to-20-DEG response without changing the qualitative biological
  interpretation.
