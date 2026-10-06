# Prediction trace

## Question and conventions

The held-out target for this run is `Timp2`. I interpreted `n_degs` as the count of all measured genes in `151 TH Prkcd Grin2c Glut` with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05`, including the targeted transcript itself if that RNA passed the threshold. This convention is visible in the focal training data: `Timp3`, `Adam22`, and `Sema5a` each have `n_degs = 1`, and in each case the one counted DEG is the perturbed gene itself.

The prediction is therefore about a calibrated screen endpoint, not about whether TIMP2 is biologically important in other systems. I downweighted germline, chronic conditional, aging, injury, tumor, and vascular observations relative to the acute, sparse P16 AAV CRISPR neuronal assay.

## Sources used

- Training DEG counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training DE signatures: `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest: `[local file: 239_Timp2.csv]`.
- Distributed Agents same-experiment corpus release `perturbai-july-260713-sourceguard-1773-v1`.
- NCBI PubMed through the BioEval literature tools.

## Computations over the supplied data

1. Read the manifest and confirmed that it contains only `Timp2`.
2. Read the focal count CSV and used its empirical scale. The `151 TH Prkcd Grin2c Glut` training endpoint is highly sparse: among 1,674 non-held-out targets, the median `n_degs` is 0, the 75th percentile is 1, the 90th percentile is 2, and only the extreme tail reaches hundreds or thousands of DEGs.
3. Queried focal training counts for gene families and pathway neighbors that could be informative for a TIMP2 perturbation:
   - The only TIMP-family training target was `Timp3`, with `n_degs = 1`.
   - No `Mmp`, `Mmp2`, `Mmp9`, `Mmp14`, `Adam17`, `Timp1`, or `Timp4` perturbation was present in the training count table.
   - Related extracellular or protease-control targets were mostly null in the focal group: `Adam10 = 0`, `Adamts17 = 0`, `Fbn1 = 0`, `Efemp1 = 0`, `Itgb1 = 0`, all represented integrin alphas/beta-2 that I checked were 0, `Col2a1 = 0`, `Col11a1 = 0`, `Tgfbr1 = 0`, `Tgfbr2 = 0`, `Tgfbr3 = 0`, `Notch1 = 0`, `Notch2 = 0`, `Notch4 = 0`, `Kdr = 0`, `Igf1r = 0`, `Pik3cb = 0`, `Pik3r1 = 0`, `Pik3r2 = 0`, `Akt3 = 0`, `Lrp1 = 0`, `Serpini1 = 0`, and the GAG/heparan sulfate targets `Ext1`, `Ext2`, `Gpc6`, `Hs6st2`, `Xylt1`, `B3gat3`, and `Glce` were also 0.
4. Scanned the focal parquet row groups for the relevant comparator perturbations and counted `pvals_adj < 0.05`.
   - `Timp3`: the sole focal DEG was `Timp3` itself, with `logfoldchanges = -0.841638`, `pvals_adj = 1.45e-6`, `n_pert_matched = 223`, `n_ctrl_matched = 23679`; the next ranked genes all had adjusted p value 1.0.
   - `Adam10`: 0 DEGs; its best nominal focal rows were small and all `q = 1.0`.
   - `Adamts17`: 0 DEGs; best row was `Spata2l`, `q = 0.274`, followed by `q = 1.0`.
   - `Itgb1`, `Tgfbr1`, and `Tgfbr2`: 0 DEGs with no near-threshold focal rows.
   - Self-only controls included `Adam22`, with only `Adam22` significant, `logFC = -0.550`, `q = 1.07e-9`, and `Sema5a`, with only `Sema5a` significant, `logFC = -0.915`, `q = 3.94e-9`.
5. Scanned all target-equals-feature rows in the focal parquet. Of 1,642 training targets whose own transcripts were measured in this cell group, 319 had a significant self row; 237 of those were one-DEG perturbations. This confirmed that a target-transcript-only call is a common endpoint state in this assay.
6. Queried the Distributed Agents corpus.
   - `Timp2` itself was absent: no same-experiment claims, findings, or explicit references were available for the held-out target.
   - `Timp3` had a curated buffered-response finding: across the 23 measured neuronal groups, the only non-self row reaching FDR < 0.10 was `Syp` in `046 CTX-CGE GABA`, while `151 TH Prkcd Grin2c Glut` had a significant `Timp3` self-drop and no downstream FDR < 0.10 genes.
   - `Timp3` pathway-uncoupling findings noted that represented ADAM10/APP, VEGFR/Kdr, TNFR, and Notch perturbations did not phenocopy TIMP3.
   - `Adamts17` and `Efemp1` corpus entries independently showed that other matrix or extracellular protease-control programs were flat or near-null in this postmitotic neuronal RNA readout, despite plausible matrix biology outside this assay.

## Biological calibration for Timp2

TIMP2 is a secreted tissue inhibitor of metalloproteinases. It directly inhibits MMPs and has a distinctive role in recruiting pro-MMP2 to MT1-MMP/MMP14 at the cell surface for activation of MMP2; that TIMP2-MMP14-proMMP2 trimolecular mechanism is described by Nagase 1998, DOI 10.1038/cr.1998.18, PMID 9791731, and mapped in TIMP2 sequence mutants by Worley et al. 2003, DOI 10.1042/BJ20021573, PMID 12630911. Mouse brain work supports neuronal TIMP2 expression: Blavier and DeClerck 1997 reported adult mouse brain and neuronal-tissue expression of Timp2, DOI 10.1091/mbc.8.8.1513, PMID 9285822, and Pagenstecher et al. 1998 found high TIMP-2 expression predominantly in neurons in normal mouse CNS, PMID 9502415. More recent hippocampal studies showed that TIMP2 can influence plasticity and extracellular matrix organization: Castellano et al. 2017 implicated TIMP2 in hippocampal LTP and memory, DOI 10.1038/nature22067, PMID 28424512, and Ferreira et al. 2023 found that neuronal TIMP2 deletion alters hippocampal ECM, adult neurogenesis, spine turnover, and memory, DOI 10.1038/s41380-023-02296-5, PMID 37914840.

Those external facts make `Timp2` a real neuronal ECM regulator, but they do not by themselves imply a broad snRNA-seq response here. TIMP2 is secreted, its canonical metalloprotease effects are extracellular and often protein/activity-level, and the screen perturbed a sparse mosaic of postmitotic neurons while leaving neighboring edited and unedited neurons, choroid plexus, endothelial cells, glia, and serum-derived protein pools able to buffer secreted TIMP2. The Distributed Agents `Timp3` finding is the closest within-dataset warning: even an ECM-bound TIMP with broad MMP/ADAM/ADAMTS inhibitory activity produced no downstream focal program when its own thalamic RNA dropped significantly.

The most relevant focal analogs are therefore:

- `Timp3`: `n_degs = 1`; family member and extracellular metalloprotease inhibitor. Its focal count was only a self-hit, so I used it as the main positive analog for "TIMP transcript can be detected after guides, but downstream neuronal RNA can be absent."
- `Adam10`: `n_degs = 0`; an ADAM metalloprotease connected to TIMP3 biology and Notch/APP shedding, but flat in the focal group and curated by Distributed Agents as not phenocopying `Timp3`.
- `Adamts17` and `Fbn1`: both `n_degs = 0`; matrix protease/microfibril axis counterexamples showing that ECM remodeling biology did not transfer to a TGF-beta/BMP-SMAD neuronal transcriptomic module.
- `Itgb1` and the represented integrin alpha perturbations: all `n_degs = 0`; counterexamples for a broad cell-ECM adhesion response.
- `Tgfbr1`, `Tgfbr2`, `Tgfbr3`, `Notch1`, `Notch2`, `Notch4`, `Kdr`, `Igf1r`, `Pik3cb`, `Pik3r1`, `Pik3r2`, and `Akt3`: all `n_degs = 0`; counterexamples for common downstream receptor or survival cascades that could have amplified extracellular protease imbalance into nuclear RNA changes.
- `Adam22` and `Sema5a`: both `n_degs = 1` and both self-only; these are not mechanistic TIMP2 analogs, but they calibrate the assay behavior of surface/secreted/adhesion genes whose own RNA is knocked down without an observed downstream program.

## Target-specific decision

I predict `Timp2` will be nonzero but only barely nonzero: `predicted_n_degs = 1`.

The `1` is driven by within-dataset evidence that singleton, self-only calls are common in this exact focal group, by the directly analogous `Timp3` self-only result, and by external evidence that `Timp2` is neuronally expressed so its own focal transcript was likely quantifiable. I do not predict additional downstream DEGs because every close same-experiment comparator that could represent neuronal ECM, metalloprotease, integrin, Notch, TGF-beta, PI3K/AKT, or growth-factor amplification was silent or self-only, and the exact MMP2/MMP14 branch was not represented among training perturbations.

## Limits and extrapolation

This is still an extrapolation. The key missing within-dataset perturbations are `Mmp2`, `Mmp14`, `Mmp9`, `Mmp3`, `Adam17`, `Timp1`, and `Timp4`, so the actual TIMP2-MMP14-MMP2 biochemical axis was bounded only indirectly. I also could not observe the held-out `Timp2` guide count, editing rate, or self `logFC`; a small guide pool or weak transcript destabilization would collapse this prediction from one DEG to zero. Conversely, chronic hippocampal TIMP2 phenotypes show that TIMP2 can affect ECM and plasticity, so a small number of additional downstream genes is biologically possible. I treated those chronic structural phenotypes as poor evidence for a broad acute thalamic snRNA-seq response because this experiment is sparse, juvenile, postmitotic, NeuN-enriched, and measures nuclear RNA rather than extracellular protein abundance, MMP activity, or synaptic matrix ultrastructure.
