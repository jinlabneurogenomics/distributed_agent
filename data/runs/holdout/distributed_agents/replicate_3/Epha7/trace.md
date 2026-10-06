# Epha7 DEG-count prediction

## Question interpreted

The requested held-out perturbation for this run is `Epha7`.  I predicted its `n_degs` in the focal `151 TH Prkcd Grin2c Glut` cells: the integer number of measured genes that would pass Benjamini-Hochberg FDR 0.05 after acute AAV-PHP.eB CRISPR perturbation of `Epha7`, scored by Wilcoxon tests against matched non-targeting/safe-targeting nuclei.

I treated the perturbed target transcript itself as eligible to count.  This matters because several receptor/guidance perturbations in the training table have exactly one FDR gene in this focal class, and direct parquet inspection showed that in `Epha4`, `Plxna2`, `Robo1`, `Sema5a`, and `Unc5c` the lone significant row is the knocked-down transcript itself rather than a downstream state.

## Sources used

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, giving the focal-cell observed counts for 1,674 non-held-out targets.
- `training_de_all_cell_groups.parquet`, queried for `151 TH Prkcd Grin2c Glut` and for Eph/ephrin and axon-guidance comparator perturbations.
- Distributed Agents corpus MCP release `perturbai-july-260713-sourceguard-1773-v1`.  The corpus had no `Epha7` record, but it had same-experiment claims and findings for represented Eph receptors (`Epha2`, `Epha3`, `Epha4`, `Epha5`, `Epha10`, `Ephb1`, `Ephb2`, `Ephb4`) and guidance receptors.
- Distributed Agents runtime profile comparison over focal-cell `logfoldchanges`, with `pvals_adj < 0.05` used only to mark significant features.
- PubMed literature on Eph/ephrin signaling and Epha7: Huot 2004, DOI `10.1016/j.pnpbp.2004.05.025`, PMID 15363605; Egea and Klein 2007, DOI `10.1016/j.tcb.2007.03.004`, PMID 17420126; Torii and Levitt 2005, DOI `10.1016/j.neuron.2005.09.021`, PMID 16301174; Lehigh et al. 2013, DOI `10.1016/j.gep.2013.08.002`, PMID 24036135; Son et al. 2015, DOI `10.1002/cne.23933`, PMID 26587807; Depaepe et al. 2005, DOI `10.1038/nature03651`, PMID 15902206; Leonard et al. 2020, DOI `10.1371/journal.pone.0231561`, PMID 33275600.

## Computation over the supplied data

The focal training endpoint was highly zero-inflated: 1,205 of 1,674 targets were zero, 276 were exactly one, the median was 0, the 75th percentile was 1, and the 95th percentile was 18.  Thus a structural/cell-surface developmental gene needed target-specific evidence before assigning anything beyond the 0-1 band.

I selected mechanistic comparators from three groups:

- direct Eph receptor relatives represented in training: `Epha10`, `Epha2`, `Epha3`, `Epha4`, `Epha5`, `Ephb1`, `Ephb2`, `Ephb4`
- other extracellular guidance receptors or ligands active in local actin-remodeling/wiring pathways: `Plxna1`, `Plxna2`, `Plxna4`, `Plxnd1`, `Nrp1`, `Nrp2`, `Sema4d`, `Sema5a`, `Sema6a`, `Dcc`, `Dscam`, `Robo1`, `Robo2`, `Robo4`, `Slit2`, `Unc5c`, `Unc5d`
- intracellular or sheddase nodes that the Distributed Agents corpus and Eph biology nominate downstream or adjacent to Eph signaling: `Adam10`, `Fyn`, `Ptpn11`, `Rac1`, `Cdc42`, `Pak1`, `Pak2`, `Pak3`, `Rho`, `Sos1`, `Mapk1`, `Mapk9`, `Pik3cb`, `Pik3r1`, `Pik3r2`, `Rasa2`, `Chn1`

For each candidate, I filtered the parquet to the focal group, counted rows with `pvals_adj < 0.05`, and identified the minimum-FDR gene:

```sql
SELECT
  gene_target,
  SUM(pvals_adj < 0.05) AS n_sig,
  MIN(pvals_adj) AS min_padj,
  arg_min(names, pvals_adj) AS min_padj_gene,
  arg_min(logfoldchanges, pvals_adj) AS min_padj_lfc
FROM read_parquet('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

The focal direct Eph counts were:

| target | focal `n_degs` | strongest FDR row in the parquet |
| --- | ---: | --- |
| `Epha10` | 0 | min q = 0.603; `Epha10` self q = 1.0 |
| `Epha2` | 0 | min q = 1.0 |
| `Epha3` | 0 | min q = 1.0 |
| `Epha4` | 1 | only hit is `Epha4`, logFC -1.027, q = 7.88e-32 |
| `Epha5` | 0 | min q = 1.0 |
| `Ephb1` | 0 | min q = 1.0 |
| `Ephb2` | 0 | min q = 0.589; `Ephb2` self q = 1.0 |
| `Ephb4` | 0 | min q = 1.0 |

The broader guidance set was similarly quiet: `Nrp1`, `Nrp2`, `Plxna1`, `Plxna4`, `Plxnd1`, `Sema4d`, `Sema6a`, `Dcc`, `Dscam`, `Robo2`, `Robo4`, `Slit2`, and `Unc5d` had 0 DEGs in the focal class.  `Plxna2`, `Robo1`, `Sema5a`, and `Unc5c` had 1 each, and in all four cases the single significant gene was the perturbed target itself (`Plxna2` q = 0.024, `Robo1` q = 2.72e-6, `Sema5a` q = 3.94e-9, `Unc5c` q = 2.04e-4).  Proximal Eph/Rho/MAPK/PI3K comparators were also 0-1 in this cell group: `Adam10`, `Fyn`, `Ptpn11`, `Rac1`, `Pak2`, `Pak3`, `Rho`, `Sos1`, `Mapk1`, `Mapk9`, `Pik3cb`, `Pik3r1`, `Pik3r2`, `Rasa2`, and `Chn1` were 0, while `Cdc42` and `Pak1` were 1.

I also ran a Distributed Agents runtime `profile_compare` on the 12 direct Eph / closest receptor-guidance targets with complete focal `logfoldchanges`.  Seven had no FDR-significant feature and five had only 1.  No pair shared a significant positive or negative feature.  Within the subthreshold vectors, EphA receptors were close to one another inside the selected near-flat cohort, for example `Epha2`-`Epha4` Pearson 0.684 and cosine 0.739, `Epha2`-`Epha5` Pearson 0.680 and cosine 0.739, but those similarities mostly describe a shared low-amplitude/null surface rather than a recurring multi-gene module.

## Same-experiment corpus evidence

The Distributed Agents corpus had no `Epha7` target context, so the final transfer did not use a prewritten `Epha7` finding.  It did contain two high-value negative controls:

- For Eph receptors, claim `claim:2d52a03dd54eace8a29f` states that represented `Epha10`, `Epha2`, `Epha3`, `Epha4`, `Epha5`, `Ephb1`, and `Ephb2` perturbations "do not produce a common Eph-family nuclear transcriptomic program, instead showing flat or receptor-specific sparse effects."  The contributing `Epha4:F004` finding explicitly contrasted `Epha4` with `Epha2`, `Epha3`, `Epha5`, `Epha10`, `Ephb1`, `Ephb2`, `Ephb4`, `Rac1`, `Cdc42`, and `Pak1`-`Pak3`.
- For semaphorin/plexin and Slit/Robo guidance comparators, the corpus made the same point: semaphorin-plexin-neuropilin perturbations did not form an interchangeable acute neuronal mRNA module, and represented axon-guidance ligand/receptor perturbations spanning netrin/DCC/UNC5/DSCAM and Slit/Robo did not form a convergent soma transcriptomic module.

Those corpus findings were used as calibration evidence that family membership and pathway adjacency are not enough to inflate `Epha7` above the self-hit range in this assay.

## Target-specific biological reasoning

`Epha7` encodes an EphA receptor tyrosine kinase in the membrane-tethered ephrin/Eph cell-contact signaling system.  Eph/ephrin complexes signal bidirectionally and often control axon attraction/repulsion, adhesion or de-adhesion, and Rho-family cytoskeletal remodeling rather than directly acting as nuclear transcription factors (Egea and Klein 2007; Huot 2004, DOI `10.1016/j.pnpbp.2004.05.025`).  That mechanism is a good match to the observed dataset behavior: perturbing single Eph, plexin, neuropilin, Robo, DCC, or UNC5 receptors in P16 postmitotic neurons usually left the soma transcriptome flat.

Among the represented training perturbations, `Epha4` is the best focal-cell analog for `Epha7`: both are EphA receptors used in developing forebrain/thalamic wiring, both bind ephrin-A ligands, and developmental thalamus contains EphA4/EphA7-positive domains (Lehigh et al. 2013).  `Epha4` was not a broad responder in `151 TH Prkcd Grin2c Glut`; it produced exactly one DEG, the `Epha4` transcript itself.  `Epha2`, `Epha3`, `Epha5`, and `Epha10` are same-subfamily counterexamples showing that many EphA perturbations are fully zero in the same focal cells.  `Plxna2`, `Robo1`, `Sema5a`, and `Unc5c` are useful positive calibration cases because they show that this assay can count a single on-target depletion for cell-surface wiring genes while still finding no downstream genes.

External Epha7 biology pointed away from a large postnatal RNA response.  EphA7 can control forebrain progenitor apoptosis and cortical size during embryogenesis (Depaepe et al. 2005), corticothalamic axon topography (Torii and Levitt 2005), thalamic nuclear parcellation (Lehigh et al. 2013), and cortical dendrite/spine development through full-length and truncated isoforms (Leonard et al. 2020).  Son et al. 2015 further showed that EphA4 and EphA7 are not interchangeable in the developing corticothalamic system.  These are real neuronal functions, but they are dominated by embryonic/early-postnatal wiring, ligand geography, receptor clustering, and local cytoskeletal signaling.  They do not imply dozens of soma DE genes three to four weeks after sparse P16 loss in a juvenile thalamic glutamatergic nucleus.

My nonzero-vs-zero decision is therefore:

- within-dataset evidence strongly predicts no secondary Eph/ephrin transcriptional program;
- same-experiment `Epha4`, `Sema5a`, `Robo1`, `Plxna2`, and `Unc5c` show that focal counts of 1 often represent only the perturbed transcript;
- Epha7 has documented thalamic expression/function during the period that builds corticothalamic and thalamic nuclei, making an `Epha7` self-transcript hit plausible in this thalamic class even if downstream effects are buffered.

The point prediction is consequently `1`: one expected FDR gene, most likely `Epha7` itself, and zero additional downstream genes.

## Limits and extrapolation

The biggest uncertainty is Epha7 expression and guide performance in the exact `151 TH Prkcd Grin2c Glut` nuclei at P37-P44; the held-out design withholds the direct self-logFC, and developmental thalamic expression need not persist uniformly into this juvenile/adult window.  A true zero would be unsurprising if the targeted nuclei expressed too little `Epha7`, if the chosen guides did not destabilize the transcript enough, or if this Allen cell group did not coincide with the EphA7-positive thalamic domains described anatomically.

The EphA, semaphorin, plexin, netrin, and Robo comparators are mechanistically appropriate for axon-guidance and local actin signaling, but none is a perfect paralogous substitute for `Epha7`; the literature explicitly shows EphA4/EphA7 specificity in corticothalamic development.  The Distributed Agents runtime similarities among near-zero signatures are also weak positive calibration, not evidence for a true shared subthreshold program.  Finally, the assay measured single-nucleus RNA in sparse, postmitotic, P16-perturbed brain neurons; it would miss many core EphA7 phenotypes, including axon targeting, thalamic parcellation, dendritic morphology, receptor phosphorylation, and cell-contact-dependent ephrin signaling.
