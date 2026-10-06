# Mc3r held-out DEG-count prediction

## Question interpreted

The requested readout is the integer number of genes with `pvals_adj < 0.05` in the held-out `Mc3r` CRISPR perturbation, computed in `151 TH Prkcd Grin2c Glut` nuclei.  `Mc3r` was absent as a `gene_target` in the parquet and absent from `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, so I treated it as a pure transfer problem rather than trying to recover a hidden row.

I interpreted `n_degs` literally as all measured genes passing the BH-adjusted Wilcoxon threshold in the focal cell group; this can include the perturbed transcript itself when target-RNA loss is significant, as it does for `Atrn` in this focal group.

## Sources used

- Input count endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input DE parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest: `[local file: 134_Mc3r.csv]`; it contains a single row, `Mc3r`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`.
  - Direct `Mc3r` context was absent, as expected for this held-out gene.
  - The relevant melanocortin claim was `claim:a37db0dd68ddbbfdd6ab`: the represented melanocortin-system perturbations `Agrp`, `Atrn`, `Mc1r`, and `Mc2r` gave no evidence for a basal neuronal melanocortin transcriptional module, while central `Mc3r`, `Mc4r`, `Pomc`, `Asip`, `Mrap`, and `Mrap2` were not themselves present as perturbation targets.
  - Target-level cards used as same-experiment context included `Agrp:F003/F004`, `Mc1r:F004/F005`, `Mc2r:F003`, and `Atrn:F004/F005`.
- External biology from PubMed:
  - Butler et al. 2000, `Endocrinology`, DOI `10.1210/endo.141.9.7791`, PMID `10965927`: `Mc3r`-null mice have increased adipose mass and altered substrate partitioning rather than the severe hyperphagia/linear-growth syndrome of `Mc4r`.
  - Ellacott and Cone 2004, `Recent Progress in Hormone Research`, DOI `10.1210/rp.59.1.395`, PMID `14749511`, and Biebermann et al. 2012, `Handbook of Experimental Pharmacology`, DOI `10.1007/978-3-642-24716-3_3`, PMID `22249810`: POMC-derived melanocortins and AgRP regulate MC3R/MC4R signaling in the central leptin-melanocortin feeding pathway.
  - Renquist et al. 2012, `PNAS`, DOI `10.1073/pnas.1201994109`, PMID `22573815`: MC3R is required for normal fasting responses and metabolic communication of nutritional state.
  - Gui et al. 2023, `Cell Reports`, DOI `10.1016/j.celrep.2023.113188`, PMID `37792535`: MC3R in AgRP neurons is needed for normal AgRP-neuron activation by fasting, cold, and ghrelin.
  - Dahir et al. 2024, `Journal of Clinical Investigation`, DOI `10.1172/JCI178250`, PMID `39007271`: MC3R regulates AgRP-terminal GABA release and suppresses anorectic circuits; `Mc3r` deletion or pharmacologic inhibition sensitizes mice to GLP1, PYY, CCK, and leptin anorectic stimuli.
  - Possa-Paranhos et al. 2024, `Journal of Physiology`, DOI `10.1113/JP286699`, PMID `39718394`: adult medial-hypothalamic MC3R signaling contributes to energy rheostasis, with dorsal medial hypothalamic MC3R neurons affecting locomotion and energy expenditure.

## Computational checks over the supplied data

I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and counted `pvals_adj < 0.05` per `gene_target`.  The focal slice contained 28,891,566 rows, 1,674 non-held-out targets, and 17,259 measured genes.  The recomputed counts matched the training CSV exactly.

The focal endpoint is zero-heavy: 469/1,674 targets have any DEG at all, the median count is 0, the 75th percentile is 1, and the 90th percentile is 2.  I did not use that bulk prior by itself for `Mc3r`; it only calibrates how easily a GPCR can sit at zero in this assay.

The mechanistically useful focal counts were:

| training target | focal `n_degs` | relevant interpretation |
| --- | ---: | --- |
| `Agrp` | 0 | endogenous MC3R/MC4R antagonist and inverse agonist in the central melanocortin pathway; 261 matched perturbed nuclei in the focal group and no BH-significant genes |
| `Mc1r` | 0 | melanocortin GPCR paralog; 257 matched nuclei and no focal genes passing FDR |
| `Mc2r` | 0 | melanocortin GPCR paralog; 160 matched nuclei and no focal genes passing FDR |
| `Atrn` | 1 | melanocortin/Agouti-related accessory biology; the one focal DEG was `Atrn` itself, so this was not a propagated melanocortin module |
| `Htr2c` | 0 | appetite GPCR acting in POMC/melanocortin physiology but flat here |
| `Lepr` | 0 | upstream adipostatic receptor feeding into POMC/AgRP circuits but flat here |
| `Insr` | 0 | insulin energy-balance receptor, flat here |
| `Ghsr` | 0 | ghrelin receptor, flat here |
| `Npy1r`, `Npy2r`, `Npy5r`, `Mchr1`, `Glp1r`, `Gipr` | 0 each | represented neuropeptide/metabolic GPCR comparators, all flat in the focal endpoint |
| `Adcy1`, `Adcy3`, `Adcy5`, `Gnas`, `Ptpn11`, `Ptpn1`, `Stat3`, `Stat5b` | 0 each | represented proximal cAMP or leptin/JAK-STAT nodes that did not create a broad focal response |

For the closest melanocortin rows, the adjusted-p surface was not hovering just below threshold: in `151 TH Prkcd Grin2c Glut`, the minimum adjusted p-value was 1.0 for `Agrp`, `Mc1r`, and `Mc2r`; for `Atrn`, only the self-transcript crossed FDR, with the next best row at adjusted `p = 0.457`.

## Target-specific reasoning

### `Mc3r`

The direct biology says `Mc3r` is a real central melanocortin receptor, not a random orphan GPCR.  It is activated by POMC-derived melanocortins and antagonized by AgRP, regulates hypothalamic energy-balance circuits, and mouse loss-of-function alters adiposity, fasting responses, AgRP-neuron activation, and sensitivity to anorectic stimuli.  The newer circuit work localizes much of this biology to AgRP terminals/AgRP somata and medial-hypothalamic neurons, with outputs in GABA release, Fos after stimulation, feeding, locomotion, and energy expenditure.

Those functions are a poor match to the measured endpoint for this run.  The focal cell group is a coarse thalamic glutamatergic group, the perturbation is sparse postnatal AAV CRISPR at P16 with a P37-P44 basal snRNA-seq readout, and the assay does not apply fasting, ghrelin, leptin, GLP1, PYY, CCK, or melanocortin agonist/antagonist challenges.  A stable bulk-like nuclear RNA aftermath in `151 TH Prkcd Grin2c Glut` would therefore have to be a fairly indirect consequence of losing a receptor whose strongest public phenotypes are in rare hypothalamic physiological states.

Within the training data, the best available melanocortin comparisons all supported a zero call:

- `Agrp`, the endogenous melanocortin antagonist/inverse agonist, had `n_degs = 0` in the focal group.
- `Mc1r` and `Mc2r`, the melanocortin receptor paralogs that were assayed, each had `n_degs = 0`.
- `Atrn` had only one focal DEG, the perturbed `Atrn` transcript itself, and the Distributed Agents corpus specifically judged its screen not to expose a melanocortin/AgRP transcriptional module.
- `Htr2c`, `Lepr`, `Insr`, `Ghsr`, `Glp1r`, `Gipr`, `Npy1r`, `Npy2r`, `Npy5r`, and `Mchr1` were all focal-zero despite occupying nearby energy-balance and neuropeptide-GPCR biology.
- Proximal cAMP and leptin/JAK-STAT components were also absent or extremely sparse, so there was no evidence that cAMP-coupled or adipostatic receptors regularly propagated to this cell group's 3-4-week basal nuclear transcriptome.

The only plausible counterargument for a nonzero call is target-self RNA loss: a low-expression receptor can have no downstream program but still score as a single DEG if editing destabilizes its own transcript.  I discounted that here.  `Mc3r` was a measured transcript in the focal parquet, but it never crossed FDR in any non-held-out focal signature; the more direct `Agrp`, `Mc1r`, `Htr2c`, `Lepr`, and related receptor rows also lacked focal self or pathway events.  MC3R's essential outputs are more likely membrane/cAMP/synaptic effects in rare medial-hypothalamic cells than a large, persistent transcript-degradation signal in this thalamic group.

I therefore predicted no FDR-significant genes for held-out `Mc3r`.

## Limits

The strongest exact comparators, `Mc4r`, `Pomc`, `Mrap2`, and `Mrap`, were held out or absent as perturbation targets, so `Mc3r` is inferred from less central melanocortin paralogs and from pathway-adjacent appetite receptors rather than from its closest receptor pair.  The Distributed Agents same-experiment corpus has no direct `Mc3r` finding.  The public `Mc3r` studies largely use germline or conditional Cre deletion, adult hypothalamic viral deletion, pharmacology, or challenged animals, whereas this experiment used sparse juvenile postmitotic CRISPR and basal snRNA-seq.  Finally, a one-gene target-self hit is intrinsically hard to rule out for any held-out locus without the actual gRNA-level target-RNA measurements, so the zero-vs-one distinction is the main residual uncertainty.
