# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The requested held-out perturbation file contains one target, `Tbck`. I interpreted the requested scalar as the count of measured genes in `151 TH Prkcd Grin2c Glut` with `pvals_adj < 0.05` after acute AAV CRISPR loss of function, i.e. the same `n_degs` endpoint reported for held-in training genes in `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`. `Tbck` is absent from both the focal-cell training-count CSV and the training DE parquet, so its count has to be transferred from held-in perturbations and from TBCK biology rather than read directly.

Two interpretation choices matter.

- I treated the focal cell label literally as a thalamic glutamatergic class. `TH` is not tyrosine hydroxylase in this taxonomy.
- I did not use measured self-knockdown as an editing-efficiency filter. The assay is sparse mosaic CRISPR and the supplied task notes that self-RNA change is not a calibrated measure of functional knockout.

## Sources

- Supplied `training_de_all_cell_groups.parquet`: per-gene log2 fold changes and Wilcoxon adjusted p values for held-in perturbations.
- Supplied `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: exact focal-cell DEG counts for 1,674 held-in targets.
- Supplied `233_Tbck.csv`: the ordered held-out target list.
- Distributed Agents same-experiment semantic corpus, release `perturbai-july-260713-sourceguard-1773-v1`. It had no direct packaged `Tbck` claim, but it had relevant claims for `Rab7`, `Tsc2`, `Depdc5`, and `Vps35`: Rab7 late-endosomal/lysosomal compensation; Tsc2 mTORC1/SREBP/lysosome-like sterol response; Rab7/Depdc5 sterol-endolysosomal convergence; and Vps35-retromer pathway specificity.
- PubMed-indexed literature:
  - Liu, Yan & Zhou 2013, PLoS One, DOI 10.1371/journal.pone.0071349: TBCK depletion perturbs cell growth and mTOR-complex expression/signaling.
  - Chong et al. 2016, Am J Hum Genet, DOI 10.1016/j.ajhg.2016.01.016, and Bhoj et al. 2016, Am J Hum Genet, DOI 10.1016/j.ajhg.2016.03.016: biallelic TBCK inactivation causes severe infantile encephalopathy and connects TBCK to Rab-GAP and mTOR biology.
  - Ortiz-Gonzalez et al. 2018, Ann Neurol, DOI 10.1002/ana.25130, and Tintos-Hernandez et al. 2021, Brain Communications, DOI 10.1093/braincomms/fcab215: TBCK patient cells show autophagic/lysosomal abnormalities and impaired lysosomal proteolysis/mitophagy.
  - Moreira et al. 2022, Front Cell Neurosci, DOI 10.3389/fncel.2021.803302: TBCK loss in patient iPSC-derived neural progenitors alters ER-to-Golgi vesicle transport and autophagosome biogenesis.
  - Chen et al. 2026, Autophagy, DOI 10.1080/15548627.2026.2642337: TBCK with PPP1R21 and FERRY3/C12orf4 acts as a RAB5 GAP brake required for endolysosomal homeostasis; TBCK deficiency hyperactivates RAB5, blocks early-to-late endosome transition, alters PIK3C3/VPS34 signaling, and secondarily collapses autophagic flux.
  - Bar-Peled et al. 2013, Science, DOI 10.1126/science.1232044: GATOR1, including DEPDC5, is a GAP for RagA/B upstream of lysosomal mTORC1.
  - Wolfson et al. 2017, Nature, DOI 10.1038/nature21423: KICSTOR recruits GATOR1 to lysosomes for nutrient regulation of mTORC1.
  - Inoki et al. 2003, Genes Dev, DOI 10.1101/gad.1110003: TSC2 is a Rheb GAP upstream of mTOR signaling.
  - Kuchitsu & Fukuda 2018, Cells, DOI 10.3390/cells7110215, and Modica & Lefrancois 2018, Small GTPases, DOI 10.1080/21541248.2017.1387686: Rab7/Rab7a controls late-endosome/lysosome traffic and multiple steps of autophagy.
  - Chandra, Kendall & Jackson 2020, Biochem Soc Trans, DOI 10.1042/BST20200552: the VPS26/VPS35/VPS29 retromer sorts endosomal cargo and is important in neurons.

## Dataset computations

The focal-cell count table is highly zero-inflated: among 1,674 training targets, 1,205 had 0 DEGs, 363 had 1-9, 63 had 10-89, and 43 had at least 100. The mean was 14.1 but the median and 75th percentile were 0 and 1, so the global table alone would strongly favor zero unless a target has a pathway-supported reason to be visible.

I intersected held-in targets with TBCK-relevant early/late endosomal, Rab, lysosomal, autophagy, PI3K-AKT-mTOR, GATOR/TSC, VPS, and TBC-domain genes. The closest represented genes and focal-cell counts were:

| training perturbation | n_degs | role relative to Tbck |
| --- | ---: | --- |
| `Rab7` | 501 | late-endosomal/lysosomal hub; downstream-neighbor stress upper bound, not a direct scale donor |
| `Tsc2` | 86 | mTOR/SREBP sterol and lysosome-like response via Rheb; broad positive mTOR comparator |
| `Vps54` | 31 | GARP/endosomal trafficking response, but Jun/Egr1 state rather than TBCK-like autophagy/sterol |
| `Vps35` | 17 | retromer endosomal trafficking; modest thalamic response with some overlap with Rab7 |
| `Depdc5` | 13 | GATOR1 negative regulator of amino-acid mTORC1; modest sterol/endolysosomal state |
| `Tbcd` | 12 | tubulin-folding gene, symbolically similar but not TBCK biology; low relevance |
| `Rb1cc1` | 4 | autophagy-initiation scaffold boundary |
| `Mtor` | 2 | catalytic mTOR loss was almost buffered |
| `Ctsb`, `Ppt1` | 1 each | lysosomal enzyme boundaries |
| `Rptor`, `Becn1`, `Atg5`, `Atg16l1`, `Lamp2`, `Vps41`, `Tbc1d23`, `Tbc1d24`, `Tbc1d32`, `Rab3gap1`, `Rab3gap2`, `Rab18`, `Rab27a`, `Vps13a`, `Vps13b`, `Vps13c`, `Vps35l`, `Vps53`, `Akt3`, `Pik3cb`, `Pik3r1`, `Pik3r2`, `Ulk4` | 0 each | same broad pathway or vesicle controls that were transcriptionally silent in this assay |

I then ran a symmetric Distributed Agents observed-profile comparison over those 33 candidates in `151 TH Prkcd Grin2c Glut`, using `gene_target` as the node, `names` as the feature, `logfoldchanges` as the signed profile value, and `pvals_adj < 0.05` as the significant-feature threshold. Of the 33, only 10 had any significant features and only `Rab7` and `Tsc2` had >=50. Whole-profile Pearson/cosine values were all moderately positive because the full rank vector contains many weak genes; I therefore used exact FDR overlaps as the discriminating evidence.

The most relevant FDR overlaps were:

- `Rab7` with `Tsc2`: 38 shared significant genes, including sterol/lysosome genes `Ldlr`, `Scpep1`, `Ptgds`, `Dusp1`, `Rragd`, `Msmo1`, `Optn`, `Neu1`, `Dpp7`, `Lamp2`, `Cyp51`, and `Hmgcr`; profile Pearson 0.671, 25 shared up-regulated and 11 shared down-regulated FDR genes.
- `Tsc2` with `Depdc5`: 8 shared significant genes, including `Ldlr`, `Msmo1`, `Pik3r1`, `Pik3r3`, and `Tubb3`; profile Pearson 0.688, with no significant direction conflicts.
- `Rab7` with `Vps35`: 9 shared significant genes, including `Atp2a2`, `Ccdc136`, `Grin2b`, `Kcnc2`, and `Ptgds`; the overlap was real but small, consistent with the Distributed Agents claim that retromer/HOPS/V-ATPase genes did not recreate the broad Rab7 FDR program.
- `Rab7` with `Depdc5`: 5 shared significant genes, `Hmgcs1`, `Insig1`, `Ldlr`, `Msmo1`, and `Snhg11`, on the same sterol-growth axis.
- `Vps35` with `Depdc5`: 0 shared FDR genes, so endosomal and mTOR-sterol branches were not fully collapsed.
- `Mtor` had only two focal-cell DEGs (`Rims3`, `Tmed8`) and no FDR overlap with the positive branches; `Rptor` had zero, which argues that acute partial loss of the mTOR catalytic/core complex is buffered.

For exact rows, I queried only the focal cell and the relevant `gene_target` values from the parquet with a `pvals_adj < 0.05` filter. This was used to list genes shared across the positive branches rather than to fit a numerical model.

## Target-specific reasoning

### `Tbck`

TBCK is biologically close enough to endosomal and lysosomal stress to predict a nonzero response. Human and patient-cell studies connect TBCK loss to neurodevelopmental encephalopathy, abnormal autophagy/lysosomal function, and vesicle trafficking; newer work places TBCK in a PPP1R21-FERRY3/C12orf4 complex that acts as a RAB5 GAP and prevents sustained RAB5/PIK3C3 activity and early-endosome enlargement. This makes the held-out perturbation mechanistically closer to the observed endolysosomal/mTOR-sterol branch than to the global zero mode of the training table.

The response should nevertheless be far below `Rab7`'s 501 DEGs. `Rab7` is a late-endosome hub whose held-in signature included broad V-ATPase, lysosomal, sterol, ISR/UPR, proteasome, and synaptic down-shift arms. The same-experiment corpus explicitly notes that HOPS/retromer/WASH/V-ATPase/lysosomal comparators mostly failed to phenocopy `Rab7` at FDR scale, and the local counts agree: `Vps35` had 17 DEGs, `Vps41` 0, `Becn1` 0, `Lamp2` 0, and `Atg5` 0. TBCK loss is early-endosomal/RAB5-sided and should not be assumed to trigger the full late-lysosomal `Rab7` stress state in recovered postnatal nuclei.

The best positive scale anchors are therefore `Depdc5` at 13 and `Vps35` at 17. `Depdc5` contributes a lysosomal nutrient-signaling/mTORC1 branch whose sterol genes overlap `Rab7`; `Vps35` contributes an endosomal recycling branch with a small Rab7-like component. `Tsc2` at 86 is retained as an upper comparator because it produced a stronger mTORC1/SREBP/lysosomal program and overlapped `Rab7` on 38 focal-cell FDR genes, but TSC2 loss is mTORC1-hyperactivating via Rheb whereas TBCK loss has mixed, context-dependent reports and is now best viewed as a RAB5 endosomal defect. `Mtor` at 2 and `Rptor` at 0 keep the estimate from rising solely on pathway membership.

Balancing those observations, I predict a low but nonzero response, just above the `Depdc5`/`Vps35` branch and well below `Tsc2`: 18 DEGs.

## Limits

- No TBCK expression signature was available in the supplied input, and the Distributed Agents same-experiment corpus had no direct `Tbck` claim; the prediction is a pathway extrapolation.
- The most direct TBCK complex partners, `Ppp1r21` and `C12orf4`/FERRY3, as well as `Rab5` genes and many HOPS/Ragulator/GATOR genes, were not represented as focal-cell training donors. The analogs are adjacent processes, not same-complex controls.
- External TBCK evidence comes mostly from germline biallelic human disease, patient fibroblasts/iPSC-derived progenitors or neurons, and cultured cells. The assay here is acute, mosaic, partially penetrant CRISPR in postnatal mouse neurons, so slow lysosomal storage and developmental migration phenotypes may be muted.
- The `n_degs` endpoint is sensitive to recovered-cell counts and Wilcoxon power. The close donors had only 121-215 matched perturbed nuclei in this cell group, and small changes near the FDR threshold could move a 10-20 DEG prediction appreciably.
- Endolysosomal biology in this screen is not monotone: direct autophagy or lysosomal genes were often null while `Rab7` was very broad. The integer 18 reflects the subset of TBCK biology expected to become a nuclear RNA response in this focal cell, not a claim that TBCK biology is intrinsically weak.
