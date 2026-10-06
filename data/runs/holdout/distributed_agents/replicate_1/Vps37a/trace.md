# Held-out DEG-count prediction trace

## Question and endpoint

The requested endpoint is the held-out value of `n_degs` for `Vps37a` in `151 TH Prkcd Grin2c Glut` nuclei: the number of measured genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after the `Vps37a` CRISPR perturbation. `151 TH Prkcd Grin2c Glut` was treated as the exact Allen-derived thalamic glutamatergic class named in the task. I used the training CSV only for non-held-out focal-cell DEG counts and the parquet only for non-held-out differential-expression signatures; the held-out `Vps37a` signature and count are absent by construction.

The endpoint is directly measured for the training perturbations, absent for `Vps37a`, and assay/power dependent. I therefore predicted a point count by transferring from measured, mechanistically nearby perturbations, with external ESCRT biology used only to decide which training perturbations were credible analogs or counterexamples.

## Sources used

- Declared training focal count table: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared training differential-expression parquet: `training differential-expression dataset`.
- Requested-target manifest: `single-target request for Vps37a`, containing the single target `Vps37a`.
- Internal same-experiment semantic corpus: `perturbai-july-260713-sourceguard-1773-v1`, release manifest SHA256 `680014dca6436746dda9d6ca0e0873f7441527a44c0c3830d1bc7a0647e3387d`. I queried its compact Finding/report layer for `Chmp4b`, `Rab7`, `Vps35`, `Vps41`, `Vps54`, `Washc4`, `Lamp2`, and V-ATPase controls. These reports are interpretations of the same experiment, not independent replication.
- External literature retrieved through NCBI PubMed:
  - Hurley and Hanson 2010, DOI `10.1038/nrm2937`, PMID `20588296`, defining ESCRT-I/II-driven budding and ESCRT-III membrane scission in multivesicular-body biogenesis, viral budding, cytokinesis, and probably autophagy.
  - Stefani et al. 2011, DOI `10.1016/j.cub.2011.06.028`, PMID `21757351`, showing that UBAP1 with VPS37A defines an endosome-specific ESCRT-I complex required for ubiquitin-dependent MVB sorting.
  - Wunderley et al. 2013, DOI `10.1242/jcs.140673`, PMID `24284069`, showing selective assembly of UBAP1 with VPS37A rather than VPS37C and functional specialization of the UBAP1/VPS37A ESCRT-I complex.
  - Zivony-Elboum et al. 2012, DOI `10.1136/jmedgenet-2012-100742`, PMID `22717650`, linking human recessive VPS37A mutation to complex hereditary spastic paraparesis and showing reduced mobility after vps37A knockdown in zebrafish.
  - Lee et al. 2007, DOI `10.1016/j.cub.2007.07.029`, PMID `17683935`, showing that strong ESCRT-III/Snf7-2 dysfunction causes autophagosome accumulation, dendritic retraction, and neurodegeneration.

## Quantitative checks

I first summarized the training `n_degs` table to calibrate the focal endpoint. It contains 1,674 non-held-out perturbations; 469/1,674 were nonzero in `151 TH Prkcd Grin2c Glut`, the median was 0, the 75th percentile was 1, the 95th percentile was 18, and the distribution was highly right-skewed with a maximum of 2,677.

I then checked a curated endosomal/lysosomal/vesicle-trafficking analog set against the training count table. The direct mammalian ESCRT-I genes were not represented as training perturbations: `Tsg101`, `Vps28`, `Vps37b`, `Vps37c`, `Vps37d`, `Mvb12a`, `Mvb12b`, and `Ubap1` were all absent. The closest represented ESCRT component was the downstream ESCRT-III subunit `Chmp4b`, which had 0 DEGs in the focal cell group. Raw focal-cell parquet rows confirmed:

| training perturbation | focal `n_degs` at FDR < 0.05 | focal pattern evidence |
| --- | ---: | --- |
| `Chmp4b` | 0 | no gene passed FDR 0.05; the smallest adjusted p-value was `Ptar1`, FDR 0.174, log2FC -0.522, from 129 perturbed vs 23,679 control nuclei |
| `Vps35` | 17 | a small retromer signature led by `Atp2a2` down, FDR 3.15e-6; `Brsk1` up, FDR 1.18e-5; `Grin2b` down, FDR 8.61e-4; 133 perturbed nuclei |
| `Vps41` | 0 | no FDR hit; weakest top rows only reached FDR 0.204-0.487; 159 perturbed nuclei |
| `Vps54` | 31 | a restricted GARP/TGN response in 151, led by `Egr1` down, FDR 2.75e-6; `Kctd16` up, FDR 7.33e-4; `Jun` up, FDR 0.00140; 161 perturbed nuclei |
| `Vps53` | 0 | same GARP/EARP neighborhood as `Vps54`, but no focal FDR hit; minimum FDR 0.362; 147 perturbed nuclei |
| `Vps35l` | 0 | retromer-related Retriever subunit, no focal FDR hit; minimum FDR 1.0; 205 perturbed nuclei |
| `Washc4` | 0 | WASH/retromer cargo-sorting neighbor, no focal FDR hit; minimum FDR 1.0; 76 perturbed nuclei |
| `Rab7` | 501 | the broad late-endosome exception, with 151 induction of V-ATPase, lysosomal, sterol, autophagy, and stress transcripts; led by `Atp6v1b2`, FDR 1.06e-16 |
| `Atp6v0a1` | 1 | only its self transcript passed FDR 0.05; no broad lysosomal response |
| `Atp6v1a`, `Atp6v1b2`, `Atp6v1e1` | 0, 0, 0 | V-ATPase subunits with no focal FDR response |
| `Lamp2` | 0 | no focal gene passed FDR 0.05; `Lamp2` and `Ppm1g` sat just above threshold at FDR 0.0537 and 0.0545 |

The same-experiment Chmp4b report agreed with the raw calculation: `Chmp4b` had no corrected downstream hit in `151`, only one downstream hit anywhere, `Pip5k1c` down in `027 NP-CT-L6b-OB Glut`, and no recurrent ESCRT/autophagy/cargo-turnover transcriptomic module. The Rab7, Vps35, Vps54, Washc4, Lamp2, and V-ATPase reports also argued against a simple rule that every endosomal or lysosomal perturbation produces a focal thalamic stress transcriptome. `Rab7` can generate a broad lysosome/sterol/autophagy program in this exact cell group, but `Vps35`, `Vps54`, `Vps41`, `Washc4`, V-ATPase subunits, and `Lamp2` were small or flat.

## Vps37a-specific transfer

The causal chain I used was:

`Vps37a` guide delivery -> partial loss of the VPS37A-containing ESCRT-I species -> altered ubiquitin-dependent MVB cargo sorting and ESCRT-III recruitment upstream of membrane scission -> possible endosomal, receptor-cargo, autophagy, or viability effects -> survival/recovery of postmitotic thalamic neurons -> nuclear mRNA DE count.

External ESCRT literature gives `Vps37a` a real neuronal and endosomal prior. Stefani et al. showed that UBAP1, VPS37A, VPS28, and TSG101 form an endosome-specific ESCRT-I complex needed for endosomal ubiquitin homeostasis and EGFR MVB sorting. Wunderley et al. showed that UBAP1 incorporation is selective for VPS37A. Zivony-Elboum et al. linked recessive VPS37A dysfunction to complex hereditary spastic paraparesis, supporting relevance to neurons. This evidence says `Vps37a` loss is plausible, but it does not directly say that a 3-4 week, sparse, postnatal CRISPR lesion should leave a broad stable nuclear RNA footprint in recovered `151` neurons.

The cleanest within-dataset analog was `Chmp4b`, not `Rab7` or `Vps54`: `Chmp4b` is a core ESCRT-III scission subunit downstream of ESCRT-I and participates in the same MVB/autophagy membrane-remodeling machinery reviewed by Hurley and Hanson. Strong ESCRT-III disruption can damage mature neurons in other systems, as Lee et al. showed for Snf7-2, so a large `Chmp4b` transcriptional response would have been the within-dataset warning that neuronal ESCRT failure reliably converts to a focal nuclear stress state. It did not: `Chmp4b` had 0 focal DEGs, no focal gene close to FDR 0.05, and only one corrected hit outside the focal class. That is a candidate-specific counterexample for `Vps37a` because it is a direct downstream ESCRT effector and should be impaired in the same broad direction, through reduced MVB membrane scission or autophagic flux, if partial postnatal ESCRT loss produced a stable DEG-rich survivor state.

The next endolysosomal controls weakened, rather than strengthened, the case for a nonzero prediction. `Vps35` and `Vps54` prove that some cargo-sorting lesions can be seen in `151`, but their effects were small and biologically different: `Vps35` is retromer cargo recognition and `Vps54` is a GARP-specific trans-Golgi tether, so neither is an obligate ESCRT-I partner. `Vps41`, `Washc4`, `Vps53`, `Vps35l`, V-ATPase subunits, and `Lamp2` were flat or nearly flat. `Rab7` was the high-count counterexample, but its 501 genes included a late lysosome/sterol/autophagy/proteasome stress state absent from `Chmp4b`, `Vps35`, and `Vps54`; broad Rab7 biology alone is therefore too upstream and too pleiotropic to transfer as a predicted `Vps37a` count.

I therefore predict that recovered `151 TH Prkcd Grin2c Glut` nuclei after `Vps37a` perturbation will look more like the near-null ESCRT-III and buffered endosomal controls than like the broad Rab7 stress state. The chosen point prediction is 0 DEGs.

## Limits

- This is an extrapolation, because no ESCRT-I perturbation (`Tsg101`, `Vps28`, `Vps37b/c/d`, `Mvb12a/b`, or `Ubap1`) was present in the training count table.
- `Chmp4b` is downstream ESCRT-III, not the same ESCRT-I complex as VPS37A/UBAP1, and it had no measured self-transcript depletion in the same-experiment report. Per the dataset guard, that weak self-RNA effect is not proof of failed editing, but it still leaves protein-level ESCRT disruption unobserved.
- The prediction is only for a nuclear RNA FDR-count endpoint in surviving NeuN+ nuclei. ESCRT-I failure could alter receptor cargo, ubiquitinated endosomal proteins, LC3-positive structures, membrane repair, or survival without producing a stable BH-significant mRNA signature at P37-P44.
- `Vps37a` has human and zebrafish nervous-system disease evidence; those are chronic or organismal contexts and are not calibrated measurements of sparse postnatal mouse thalamic CRISPR.
