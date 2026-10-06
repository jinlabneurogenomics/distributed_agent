# Prediction trace

## Question and resolved ambiguities

The requested endpoint is `n_degs` for each held-out perturbation in the single focal cell group `151 TH Prkcd Grin2c Glut`: the number of measured genes with `pvals_adj < 0.05` after Wilcoxon testing against the matched non-targeting controls. The manifest for this run contains exactly one held-out target, `Tbck`, and `Tbck` is absent from both supplied training files, so I treated every `Tbck` value as truly unobserved.

I interpreted the Allen-style cell label literally as a thalamic `Prkcd`/`Grin2c` glutamatergic class. The output count is a response-breadth point prediction for a sparse postnatal AAV-CRISPR perturbation, not an estimate of editing rate, target depletion, lethality, or biochemical mTOR/Rab activity.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`, for exact FDR 0.05 DEG counts in the focal class for 1,674 non-held-out training perturbations.
- `[local file: training_de_all_cell_groups.parquet]`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` for pathway-candidate expression signatures, FDR calls, signs, overlaps, and matched nucleus counts.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`, for same-experiment curated Findings and Claims around `Tsc2`, `Mtor`, `Depdc5`, `Rab7`, and `Vps54`. The corpus had no direct held-out `Tbck` Finding, which I treated as no packaged internal interpretation rather than as a biological null.
- Distributed Agents runtime `profile_compare` on the selected mTOR/endolysosomal comparator set, as a run-local check of focal-cell activity classes.
- External PubMed-indexed literature on TBCK: Liu, Yan, and Zhou 2013, PLoS ONE, DOI `10.1371/journal.pone.0071349`; Bhoj et al. 2016, AJHG, DOI `10.1016/j.ajhg.2016.03.016`; Chong et al. 2016, AJHG, DOI `10.1016/j.ajhg.2016.01.016`; Beck-Wodl et al. 2018, Acta Neuropathologica Communications, DOI `10.1186/s40478-018-0646-6`; Moreira et al. 2022, Frontiers in Cellular Neuroscience, DOI `10.3389/fncel.2021.803302`; Chen et al. 2026, Autophagy, DOI `10.1080/15548627.2026.2642337`.

## Computational calibration

The focal training endpoint is sparse and heavy-tailed. Among the 1,674 training targets, 1,205 had `n_degs == 0`, the median was 0, the 75th percentile was 1, the 95th percentile was 18, and only 43 targets had at least 100 DEGs. This makes zero the default for an uninformative target and makes hundreds of DEGs exceptional.

I then filtered the parquet to the focal class and to mechanistically relevant mTOR, autophagy, lysosomal, Rab and vesicle-trafficking targets. The non-obvious operation was just a row-group-pruned Arrow scan:

```python
expr = (
    (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & ds.field("gene_target").isin(candidate_targets)
)
table = dataset.to_table(
    columns=["names", "scores", "logfoldchanges", "pvals_adj", "gene_target"],
    filter=expr,
)
```

Relevant focal-class endpoint counts at FDR 0.05 were:

| training perturbation | `n_degs` | relevance to `Tbck` |
| --- | ---: | --- |
| `Rab7` | 501 | late-endosome/lysosome positive control; Distributed Agents reports a sterol, lysosomal, V-ATPase and stress program in this same thalamic class |
| `Tsc2` | 86 | loss of an mTORC1 brake; induces sterol/lysosomal genes and overlaps `Rab7`, but tests mTORC1 activation rather than TBCK's RAB5-GAP loss |
| `Vps54` | 31 | vesicle-trafficking disease gene with a 151-restricted neuronal downshift, useful as a mid-sized trafficking-stress comparator |
| `Vps35` | 17 | retromer/endosome-to-Golgi trafficking comparator with a modest 151 signal |
| `Depdc5` | 13 | GATOR1/mTORC1 derepression comparator; same-direction sterol overlap with `Tsc2` and part of `Rab7` |
| `Mtor` | 2 | mTOR kinase loss itself; weak and anti-correlated with the TSC/GATOR derepression axis |
| `Rb1cc1` | 4 | autophagy-initiation component; weak ER-stress-like signature rather than broad lysosome failure |
| `Atp6v0a1`, `Ctsb`, `Sqstm1` | 1 each | mostly self-transcript or extremely narrow lysosome/autophagy controls |
| `Rptor`, `Becn1`, `Atg5`, `Atg16l1`, `Lamp2`, `Vps53`, `Vps41`, `Pik3cb`, `Pik3r1`, `Pik3r2`, `Akt3`, `Strada`, `Rab18`, `Rab27a`, `Rab3gap1`, `Rab3gap2`, `Tbc1d23`, `Tbc1d24`, `Tbc1d32` | 0 | important counterexamples: single perturbation of many nominally related pathway or family members was FDR-flat in the focal readout |

Focal-cell FDR overlaps supported using `Rab7`, `Tsc2`, and `Depdc5` as real positive anchors but not as interchangeable replicas. `Tsc2` and `Depdc5` shared 8 FDR genes, all in the same direction (`Ldlr`, `Msmo1`, `Pik3r1`, `Pik3r3`, `Rnpc3`, `Snhg11`, `Tubb3`, `Amy1`). `Rab7` and `Tsc2` shared 38 FDR genes, 36 in the same direction, including lysosome/sterol-response genes such as `Atp6v0b`, `Cyp51`, `Dpp7`, `Grn`, `Lamp2`, `Ldlr`, `Msmo1`, `Rragd`, and `Scpep1`. `Rab7` and `Depdc5` shared 5 FDR genes, all same-direction (`Hmgcs1`, `Insig1`, `Ldlr`, `Msmo1`, `Snhg11`). In contrast, `Tsc2` and `Mtor` had no shared focal FDR gene and their full signed-score correlation was negative.

These measurements matched the Distributed Agents corpus interpretation: represented PI3K/Akt and positive mTORC1-associated perturbations were often buffered or mutually non-phenocopying, while selected negative regulators and `Rab7` exposed sterol/endolysosomal outputs. The corpus also emphasized that `Rab7` is a large late-endosomal stress outlier: related lysosome, V-ATPase, HOPS, retromer and autophagy perturbations were usually flat or only partial in this assay.

## Target-specific reasoning

### `Tbck`

TBCK is not just a generic TBC-domain gene. Human biallelic loss causes a severe neurodevelopmental and neurodegenerative syndrome with hypotonia, seizures, brain atrophy or white-matter abnormalities, and loss of TBCK protein; fibroblasts from affected people can show reduced S6 phosphorylation, tying the disease gene to mTOR signaling (Bhoj et al. 2016, DOI `10.1016/j.ajhg.2016.03.016`; Chong et al. 2016, DOI `10.1016/j.ajhg.2016.01.016`). TBCK depletion also changed cell size and mTOR-complex component expression in cultured cells (Liu et al. 2013, DOI `10.1371/journal.pone.0071349`), and patient-derived neural progenitor work reported secretory-pathway, autophagosome-biogenesis, cell-cycle and migration defects while cautioning that reduced mTOR may be secondary to trafficking dysfunction (Moreira et al. 2022, DOI `10.3389/fncel.2021.803302`). The endolysosomal link is supported by TBCK deficiency with neuronal lipofuscin/lysosomal storage pathology (Beck-Wodl et al. 2018, DOI `10.1186/s40478-018-0646-6`) and, most directly, by the 2026 RAB5-GAP model in which a TBCK-PPP1R21-FERRY3 complex restrains RAB5; TBCK deficiency hyperactivates RAB5, enlarges early endosomes, blocks early-to-late endosome transition, perturbs PIK3C3/VPS34, and secondarily collapses autophagic flux (Chen et al. 2026, DOI `10.1080/15548627.2026.2642337`).

That biology argues for a nonzero thalamic neuronal response: TBCK sits at a basal membrane-traffic checkpoint, not only at a ligand-gated receptor branch, and loss has direct neuronal disease relevance. The strongest positive in-dataset analog is therefore `Rab7` rather than `Mtor`: `Rab7` loss gave 501 DEGs and induced the exact kind of lysosomal, V-ATPase, sterol and proteostasis-compensation genes that an endosomal-to-lysosomal trafficking block could trigger. `Tsc2` and `Depdc5` are weaker positive anchors for the mTOR/sterol branch, with 86 and 13 DEGs respectively, because TBCK perturbation has been connected to mTORC1 but the literature does not place TBCK as a simple TSC2- or GATOR1-like repressor. `Vps35` and `Vps54`, with 17 and 31 DEGs, show that other vesicle-trafficking disease genes can be visible in this exact class without reproducing the full `Rab7` lysosomal-stress state.

The counterevidence pushes the count down sharply. Older TBCK papers often reported reduced, not derepressed, mTOR signaling, whereas the two mTORC1-derepression perturbations in this training set (`Tsc2` and `Depdc5`) induce a same-direction sterol program. If TBCK loss primarily reduces mTORC1 output, the within-dataset match is closer to `Mtor` loss with only 2 DEGs, not to `Tsc2`. In the more recent RAB5 model, the best same-stage perturbations were missing: `Rab5a`, `Rab5b`, `Rab5c`, `PIK3C3`, `PIK3R4`, `PPP1R21`, and `C12orf4/FERRY3` are not training endpoints. The represented near-neighbors that do exist are sobering: `Appl1`, an effector for the Rab5-positive early-endosomal APPL compartment, is curated in the Distributed Agents corpus as FDR-flat despite available `Rab7`, `Tsc2` and `Mtor` comparators; `Ankfy1`, a Rab5 effector, is also flat while `Rab7`, `Tsc2`, `Vps35`, `Wdfy3` and `Vps54` respond; `Atg5`, `Becn1`, `Atg16l1`, `Lamp2`, `Vps53` and V-ATPase subunits were all zero or nearly zero in the focal class. Finally, the other represented TBC-family and RabGAP genes (`Tbc1d23`, `Tbc1d24`, `Tbc1d32`, `Rab3gap1`, `Rab3gap2`) had 0 DEGs and are not valid positive analogs because they regulate different trafficking routes.

I therefore predicted a weak but nonzero response. The point estimate, 4 DEGs, deliberately sits in the training distribution's "weak" class: larger than the flat same-family and core-autophagy controls, comparable to the weak `Mtor`/`Rb1cc1` edge, but below `Depdc5` and far below `Tsc2`, `Vps54` or `Rab7`.

## Limits

This is extrapolation from pathway-adjacent perturbations. The most direct TBCK complex partners and the RAB5 paralogs were absent from the training perturbation universe, so no same-complex or same-Rab-GTPase comparator could be observed. Published TBCK models come from fibroblasts, cultured cell lines, neural progenitors, postmortem tissue, or whole-body disease models rather than sparse P16-to-P37/44 CRISPR in recovered postmitotic thalamic nuclei. The mTOR direction is especially uncertain: TBCK loss has been linked to reduced mTOR readouts in older work, but the cleanest positive mTOR-axis signatures in this dataset are loss of negative regulators that increase an SREBP/sterol arm. A stronger hidden `Tbck` response resembling `Rab7` is plausible if early RAB5 hyperactivation is enough to create secondary lysosomal stress in these neurons; a strict zero is plausible if acute partial TBCK loss is buffered at the nuclear-RNA level, as many other endolysosomal and autophagy genes are.
