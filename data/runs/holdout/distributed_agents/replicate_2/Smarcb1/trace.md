# DEG-count prediction trace

## Question interpreted

The requested held-out perturbation list contains one mouse target, `Smarcb1`. I treated the requested endpoint as the integer number of genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon `pvals_adj < 0.05` after acute AAV-CRISPR loss of that target at P16 and harvest at P37-P44. `Smarcb1` was absent from both supplied training tables, so its own expression vector and count were not used.

The main ambiguity was how much to transfer from other BAF/mSWI-SNF subunits. The corpus and parquet show that the 151 thalamic class can detect a BAF response, but that same-family membership is not enough: `Smarcc2`, `Smarce1`, `Arid1a`, and partly `Arid2` respond, whereas `Smarca4`, `Smarca2`, `Smarcc1`, `Bicra`, `Arid1b`, and `Brwd1` are flat or nearly flat. I therefore treated each BAF-family perturbation as a calibrated analogue or boundary depending on complex role, not as equal votes.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`: exact FDR<0.05 `n_degs` for the focal cell group.
- `[local file: training_de_all_cell_groups.parquet]`: focal-cell log fold-changes, Wilcoxon scores, adjusted p-values, and matched perturbed/control nucleus counts for comparator perturbations.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`: the high-confidence claim `claim:845db620c0afdfc1b86a` summarizing a subunit-selective BAF/mSWI/SNF module in `151 TH Prkcd Grin2c Glut`, plus target contexts for `Smarcc2`, `Smarce1`, `Arid1a`, `Arid2`, `Smarcd1`, and `Smarca4`.
- PubMed literature for SWI/SNF composition and SMARCB1 mechanism:
  - Phelan et al. 1999, DOI `10.1016/s1097-2765(00)80315-9`, PMID `10078207`, reconstituted a functional human SWI/SNF core from BRG1/BRM plus INI1/SMARCB1, BAF155/SMARCC1, and BAF170/SMARCC2.
  - Alpsoy and Dykhuizen 2018, DOI `10.1074/jbc.RA117.001065`, PMID `29374058`, defined GLTSCR1/GBAF/ncBAF as a smaller SWI/SNF subcomplex lacking BAF45, BAF47/SMARCB1, and BAF57.
  - He et al. 2020, DOI `10.1126/science.aaz9761`, PMID `32001526`, showed in a nucleosome-bound human BAF cryo-EM structure that SMARCB1 contacts the nucleosome acidic patch and that ARID1A and SMARCC form the base-module scaffold.
  - Mashtalir et al. 2020, DOI `10.1016/j.cell.2020.09.051`, PMID `33053319`, resolved endogenous nucleosome-bound cBAF architecture and placed SMARCB1 at a BAF nucleosome engagement interface.
  - Radko-Juettner et al. 2024, DOI `10.1038/s41586-024-07250-1`, PMID `38538798`, found that in SMARCB1-mutant cancers, incompletely assembled SWI/SNF complexes are destabilized by DCAF5-mediated quality control.

## Dataset computations

I verified that the held-out manifest has only `Smarcb1`, then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for BAF/SWI-SNF comparators and counted rows with `pvals_adj < 0.05`. I also pivoted the same rows by measured gene to check FDR-significant overlap and sign agreement among the BAF comparators.

The training endpoint is zero-heavy: 1205 of 1674 training targets have zero DEGs in 151; only 43 have at least 100. That makes the nonzero call meaningful. Within the measured BAF family, exact FDR<0.05 counts were:

| comparator | 151 n_degs | matched perturbed nuclei | interpretation for `Smarcb1` |
| --- | ---: | ---: | --- |
| `Smarcc2` | 185 | 162 | Best direct analogue: shared BAF/PBAF core scaffold subunit with a broad same-direction module. |
| `Arid2` | 56 | 170 | PBAF-specific but partly same module; useful lower active bound. |
| `Arid1a` | 22 | 316 | cBAF selector with a compact same-direction module; lower active bound. |
| `Smarce1` | 11 | 273 | BAF57/core-associated response that strongly overlaps the Smarcc2 recurrent genes but is small. |
| `Smarcd1` | 1 | 208 | Weak boundary; only `Ankrd40` crossed FDR<0.05, though `Ptpn3` was directionally down and subthreshold at FDR<0.10. |
| `Arid1b` | 1 | 173 | Alternative ARID cBAF selector, not an `Arid1a` phenocopy. |
| `Smarca2` | 1 | 152 | ATPase paralog, likely buffered by `Smarca4`. |
| `Smarca4` | 0 | 146 | ATPase paralog and strong counterexample to treating all BAF subunits as interchangeable. |
| `Smarcc1` | 0 | 165 | SMARCC paralog counterexample; the response is biased to `Smarcc2`/BAF170 in this state. |
| `Bicra` | 0 | 229 | ncBAF-specific GLTSCR1 ortholog and not a direct SMARCB1 complex analogue. |
| `Brwd1` | 0 | 117 | BAF-associated chromatin reader, not a core loss analogue. |
| `Smarcad1` | 0 | 133 | SWI/SNF-like remodeler outside BAF/PBAF, a broad chromatin-remodeler counterexample. |

The exact expression-pattern evidence points to a real recurrent BAF module rather than one isolated training hit. At FDR<0.05, `Smarcc2` and `Smarce1` shared 9 significant genes and all 9 moved in the same direction: `Abhd12b`, `Begain`, `Lrrc7`, `Prkcd`, `Ptpn3`, `Rasa4`, `Reep2`, `Serinc2`, and `Slc25a37`. `Smarcc2` and `Arid1a` shared 13 significant genes, again all same-direction, including `Begain`, `L1cam`, `Lrrc7`, `Prkcb`, `Ptpn3`, `Ptprz1`, and `Rasa4`. `Arid2` overlapped `Smarcc2` on 9 significant genes with 7 same-direction, including strong same-direction loss of `Abhd12b`, `Prkcd`, and `Stxbp2`. Conversely, `Smarca4`, `Smarcc1`, and `Bicra` had adequate matched nuclei but no FDR<0.05 genes in the same cell class, supporting the corpus claim that this is a subunit-selective BAF/PBAF module rather than a generic chromatin-perturbation or power artifact.

The Distributed Agents corpus contributed a high-confidence synthesized same-experiment claim that `Smarcc2`, `Smarce1`, and `Arid1a` converge most clearly in this exact cell group, with partial `Arid2` and weak `Smarcd1` involvement and flat or divergent responses for `Smarca4`, `Smarca2`, `Smarcc1`, `Bicra`, `Arid1b`, and `Brwd1`. I used that claim to choose the biologically relevant measured set, then used the parquet/CSV counts above, rather than the corpus' FDR<0.10 summaries, to calibrate the endpoint requested here.

## Target-specific reasoning

### `Smarcb1`

`Smarcb1` encodes BAF47/INI1/SNF5, a non-ATPase core mSWI/SNF subunit. The structural and biochemical literature places SMARCB1 in the functional BAF core with the SMARCA ATPase and SMARCC scaffold (`Smarcc1`/`Smarcc2`) rather than in the ARID-selective periphery; the C-terminal SMARCB1 helix contacts the nucleosome acidic patch in BAF, and loss of SMARCB1 can destabilize otherwise assembled BAF/PBAF complexes. That makes `Smarcb1` closer mechanistically to the active `Smarcc2` perturbation than to the flat ATPase paralogs or to the ncBAF-specific `Bicra`.

The strongest same-assay analogue is therefore `Smarcc2`, which had 185 DEGs. `Smarce1` and `Arid1a` had smaller counts, 11 and 22, but their FDR genes were nested in the same Smarcc2 recurrent down-program on `Ptpn3`, `Begain`, `Lrrc7`, `Rasa4`, `Prkcb`, and related neuronal signaling or scaffold genes. `Arid2` had 56 DEGs and supports that a PBAF/core route is also active, though its overlap is partial and contains an extracellular/adhesion arm that is not simply the Arid1a/Smarce1 response. These observations support a nonzero call and argue against assigning `Smarcb1` to the 0-1 DEG boundary class.

I discounted several tempting but inappropriate counterexamples. `Smarca4` and `Smarca2` are mutually substitutable ATPases in many complexes and can be buffered after a single acute knockout, so their 0-1 DEG results do not predict a unique, non-ATPase core scaffold. `Smarcc1` is the paralog of active `Smarcc2`, but the training data themselves show SMARCC paralog specificity in this postnatal thalamic state. `Bicra` and `Brwd1` are even weaker boundaries: `Bicra` belongs to ncBAF/GBAF, which is compositionally distinct and lacks SMARCB1/BAF47, and `Brwd1` is a BAF-associated chromatin reader rather than an obligatory cBAF/PBAF core subunit.

For magnitude, I expect `Smarcb1` to be a strong BAF/PBAF perturbation but not necessarily larger than `Smarcc2`. The experiment is mosaic and partial, and many congenital SWI/SNF effects may be earlier than the P16-to-P37/P44 window. I therefore placed the point prediction below the 185-gene `Smarcc2` training count but above the `Arid2` 56-gene partial-PBAF response:

**Prediction: `Smarcb1 -> 140` DEGs.**

## Limits and extrapolation

The largest uncertainty is that no measured `Smarcb1`, `Pbrm1`, `Brd7`, `Actl6b`, `Dpf1`, or `Dpf3` profile is present in the supplied training data, so the inference for a unique BAF47 lesion is extrapolated from neighboring subunits. The BAF training signatures themselves are sharply subunit-selective, so complex membership alone could overpredict the effect. The public SMARCB1 evidence comes mostly from purified human complexes, tumors, or dividing cells, not sparse CRISPR editing in surviving postmitotic mouse thalamic neurons. Finally, `n_degs` is power- and assay-dependent; an unobserved low perturbed-nucleus count for held-out `Smarcb1` or especially efficient depletion of responsive cells before capture would lower the FDR<0.05 count without proving the biology absent.
