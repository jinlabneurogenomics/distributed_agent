# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The held-out manifest `[local file: 070_Epha6.csv]` contains one requested target:

| target_name |
|---|
| Epha6 |

I interpreted `predicted_n_degs` as the integer number of measured genes in the held-out `Epha6` perturbation with `pvals_adj < 0.05` in the focal `151 TH Prkcd Grin2c Glut` thalamic glutamatergic class. I did not exclude the target transcript itself, because the supplied training endpoint counts all measured genes passing FDR.

The prediction is therefore a point prediction for the assay-specific breadth of the acute, sparse, P16-to-P37/44 CRISPR loss-of-function response, not a prediction of EphA6 developmental importance, editing efficiency, spine morphology, electrophysiology, or cell survival.

## Sources used

- Raw same-experiment endpoint table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Raw same-experiment DE table: `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents same-experiment semantic corpus, release `perturbai-july-260713-sourceguard-1773-v1`. `Epha6` itself was absent from the frozen corpus, but represented Eph receptors and their pathway comparators had curated findings and claims.
- A Distributed Agents runtime `profile_neighbors` calculation over the focal-cell signed Wilcoxon `scores`, comparing the represented Eph receptors against all 1,674 eligible training targets in the focal group.
- PubMed-indexed Eph/ephrin and EphA6 literature:
  - Kullander and Klein 2002, DOI `10.1038/nrm856`, PMID `12094214`: Eph/ephrin mechanisms and neural functions.
  - Pasquale 2005, DOI `10.1038/nrm1662`, PMID `15928710`: membrane-tethered ephrin ligands, contact-dependent bidirectional Eph signaling, axon guidance, adhesion, and migration.
  - Lisabeth, Falivelli, and Pasquale 2013, DOI `10.1101/cshperspect.a009159`, PMID `24003208`: Eph receptors as contact-dependent, bidirectional RTKs with kinase-dependent and kinase-independent outputs.
  - Fu et al. 2006, DOI `10.1038/nn1811`, PMID `17143272`: EphA4 uses Cdk5/ephexin1/RhoA signaling to drive dendritic-spine retraction.
  - Mendes, Henkemeyer, and Liebl 2006, DOI `10.1523/JNEUROSCI.3162-05.2006`, PMID `16421308`: multiple EphB/A4 receptors and B-class ephrins regulate mouse forebrain callosal axon guidance, with stronger phenotypes in double knockouts.
  - Das et al. 2016, DOI `10.1186/s13578-016-0115-5`, PMID `27489614`: EphA5 and EphA6 deletion alters neuronal and dendritic-spine morphology.

## Dataset computations

I first read the requested-target manifest and the focal training-count CSV. The focal training endpoint has 1,674 targets; 469 have at least one FDR<0.05 DEG, the median is 0, and the maximum is 2,677. Thus a prediction of zero is common in this assay, while large DEG burdens occur only for a small subset of perturbations.

I then extracted the focal-cell DE rows for every represented Eph receptor in the training set:

```sql
SELECT gene_target, names, logfoldchanges, pvals_adj, scores,
       n_pert_matched, n_ctrl_matched
FROM parquet_scan('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN
      ('Epha10','Epha2','Epha3','Epha4','Epha5','Ephb1','Ephb2','Ephb4');
```

This returned 17,259 measured genes for each represented Eph perturbation in the focal cell group. The raw FDR<0.05 counts exactly matched the training-count CSV:

| analog | focal `n_degs` | focal evidence |
|---|---:|---|
| `Epha5` | 0 | Closest biologically nominated A-class comparator to `Epha6`; no focal row below FDR 0.05; self row `Epha5` log2FC -0.149, adjusted p=1.0. |
| `Epha4` | 1 | A-class Eph receptor with strong neuronal actin/spine literature; the one focal DEG was the self-transcript, `Epha4` log2FC -1.027, adjusted p=7.88e-32. |
| `Epha2` | 0 | A-class Eph receptor; focal self row log2FC +0.842, adjusted p=1.0, and no downstream focal DEG. |
| `Epha3` | 0 | A-class Eph receptor; focal self row log2FC -0.005, adjusted p=1.0, and no downstream focal DEG. |
| `Epha10` | 0 | A-class Eph receptor; weakest non-self focal rows had adjusted p=0.603 and no focal DEG. |
| `Ephb1` | 0 | EphB receptor in the broader Eph/ephrin signaling family; no focal DEG. |
| `Ephb2` | 0 | EphB/NMDAR/spine receptor; minimum focal adjusted p was 0.589 and no focal DEG. |
| `Ephb4` | 0 | EphB receptor; no focal DEG. |

The obvious intracellular pathway comparators also sat at the floor in the focal endpoint: `Adam10`, `Chn1`, `Fyn`, `Kalrn`, `Mapk1`, `Mapk9`, `Pik3cb`, `Pik3r1`, `Pik3r2`, `Psen1`, `Ptpn11`, `Rac1`, `Rasa2`, and `Sos1` all had 0 focal DEGs; `Cdc42` and `Pak1` had one each; `Pak2` and `Pak3` had 0. These are not receptor paralogs, but they are useful counterexamples because Eph signaling commonly feeds Src-family, Rho/Rac/Cdc42, MAPK, PI3K, and cytoskeletal branches.

The focal signed-score neighbor calculation gave the same interpretation. For the closest receptor comparator, `Epha5`, the strongest whole-profile Pearson neighbor anywhere in the 1,674-target focal universe was only `r=0.064`; its strongest cosine neighbor was `0.064`. For the other Eph anchors, top whole-profile Pearson values were all below `0.094`. None of the Eph receptors had a compelling significant-gene overlap program in `151 TH Prkcd Grin2c Glut`: seven had zero significant focal features and `Epha4` had only its self-transcript. These correlations are too close to the null surface to justify importing a large hidden expression module into `Epha6`.

As a small target-transcript sanity check, measured `Epha6` itself was present in the focal DE matrix for all 1,674 training perturbations, and only two perturbations made it significant secondarily: `Uba5` and `Smarcc2`. Those were broad, non-Eph transcriptional states rather than Eph-family analogs.

## Same-experiment corpus evidence

The selected Distributed Agents same-experiment corpus had no `Epha6` target record, so it could not directly state the held-out result. It did contain structured findings for the available Eph-family receptors:

- High-confidence claim `claim:2d52a03dd54eace8a29f`: "Single represented Eph receptor perturbations in postnatal neurons do not produce a common Eph-family nuclear transcriptomic program, instead showing flat or receptor-specific sparse effects." This claim is built from `Epha10`, `Epha2`, `Epha3`, `Epha4`, `Epha5`, `Ephb1`, and `Ephb2`.
- `Epha5:F003` reported that the represented Eph-family comparators did not converge with `Epha5`: `Epha2`, `Epha3`, `Ephb2`, and `Ephb4` were fully flat across the matched surface, while `Epha10`, `Epha4`, and `Ephb1` each produced one unrelated off-cell or off-gene hit. The finding explicitly noted that `Epha6` and ephrin-A ligands were absent, which makes transfer to `Epha6` an extrapolation.
- `Ephb2:F003` reported "convergent flatness" for single Eph-family receptor perturbations, with a transcriptionally flat `Ephb2` surface and flat or singleton-only `Ephb1`, `Ephb4`, `Epha4`, and `Epha5` comparators.
- `Epha4:F004` reported that represented Eph receptors and Rho/PAK actin nodes did not phenocopy `Epha4`; the same corpus evidence showed `Rac1`, `Cdc42`, `Pak1`, `Pak2`, and `Pak3` were flat or singleton-only rather than a recurrent Eph/Rho/PAK RNA branch.

This same-experiment semantic layer was used as a guard against choosing analogs by family name alone: the represented family members are indeed the right mechanistic neighborhood, but the corpus shows that in this perturbation map they did not make a shared nuclear expression signature.

## Target-specific reasoning: `Epha6`

`Epha6` encodes an A-class Eph receptor tyrosine kinase. The strongest biological link among represented training perturbations is `Epha5`, because Das et al. directly analyzed EphA5 and EphA6 loss and found effects on neuronal and dendritic-spine morphology. `Epha5` had 0 focal DEGs in the training endpoint, and the same-experiment corpus found only a single robust `Epha5` downstream hit outside the focal thalamic class. That makes `Epha5` a direct argument that EphA-family neuronal morphology can be real while remaining almost invisible in this P16 acute snRNA-seq endpoint.

`Epha4` is a useful A-class counterexample because the focal assay clearly could see Epha receptor self-transcript depletion: `Epha4` itself was the single significant `Epha4` focal row, with log2FC -1.027 and adjusted p=7.88e-32. It did not show a downstream thalamic program. Thus an `Epha6` count of 1 would be plausible if only the `Epha6` self-transcript fell, but the family prior favors 0: only 1 of 8 represented Eph receptors had a focal self hit, and `Epha5`, the most relevant `Epha6` comparator, did not.

`Epha2`, `Epha3`, and `Epha10` bound the rest of the A-class family. Their focal counts were all zero, and the corpus found no meaningful convergence between these receptors and `Epha5`/`Epha4`. `Ephb1`, `Ephb2`, and `Ephb4` are less direct paralogs but they sample the same contact-dependent Eph/ephrin logic and adjacent dendritic-spine signaling. They were also zero in the focal endpoint. The pathway-side comparators, including `Fyn`, `Ptpn11`, PI3K/MAPK genes, Rho/Rac/Cdc42/PAK nodes, `Chn1`, `Rasa2`, `Kalrn`, and `Sos1`, were likewise zero or singleton-only, so a generic "Eph receptor perturbs cytoskeletal signaling" argument did not translate into dozens of focal DEGs in this experiment.

The external biology strengthens the zero decision rather than reversing it. Eph/ephrin receptors are membrane contact sensors with bidirectional and often local cytoskeletal outputs, not canonical nuclear transcriptional regulators (Kullander and Klein 2002; Pasquale 2005; Lisabeth et al. 2013). EphA4 can drive spine retraction through Cdk5, ephexin1, and RhoA without requiring a broad transcriptional cascade (Fu et al. 2006), and developing callosal axons use multiple Eph receptors/ephrins with evidence for compensation in double knockouts (Mendes et al. 2006). EphA6 itself can affect neuronal and spine morphology with EphA5 (Das et al. 2016), but those morphology phenotypes are compatible with a flat P37/44 nuclear RNA endpoint after a single acute mosaic knockout.

Prediction: `Epha6` is most likely a focal transcriptional null, so I predict `0` DEGs rather than a one-gene self-transcript hit.

## Limits and weak points

- `Epha6` was held out from both the raw DEG endpoint and the Distributed Agents same-experiment corpus, so the prediction is an extrapolation from `Epha5`/`Epha4`/other Eph receptors rather than a measured `Epha6` signature.
- No ephrin ligands and no `Ephb3`, `Ephb6`, `Cdk5`, `Ngef`/ephexin, `Nck1`, or `Nck2` perturbations were available as direct comparator targets, limiting coverage of the pathway.
- The decisive endpoint is single-nucleus RNA in recovered nuclei. It can miss altered receptor phosphorylation, growth cones, dendritic spine morphology, axon wiring, NMDAR localization, and electrophysiology.
- The broad `151 TH Prkcd Grin2c Glut` label may dilute a small thalamic subclass where EphA6 is highly expressed.
- Self-transcript visibility is unpredictable in this CRISPR screen. `Epha4` had a strong focal self hit while `Epha5` and the other represented Eph receptors did not; an `Epha6` self-only hit is the main way this zero prediction could be off by one.
