# DEG-count prediction trace

## Question and resolved ambiguities

The requested held-out target list contains one mouse perturbation, `Twist1`. I interpreted the endpoint as the exact focal-cell metric from the prompt: the number of measured genes with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after acute AAV CRISPR loss of function in `151 TH Prkcd Grin2c Glut` neurons. The prediction is therefore a point prediction for this Perturb-seq assay and this one thalamic glutamatergic cell group, not an estimate of developmental importance, craniofacial phenotype strength, or target RNA knockdown.

`Twist1` was absent from both supplied training inputs. I therefore used the `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table as the endpoint calibration set, used the parquet-derived Distributed Agents profile tools for expression-pattern checks in the same focal group, used the Distributed Agents same-experiment corpus to audit known same-dataset contrasts, and used PubMed literature for the biology of TWIST1 dimers and lineages.

## Sources used

- Differential-expression endpoint calibration: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested held-out manifest: `[local file: 255_Twist1.csv]`.
- Differential-expression signatures: `[local file: training_de_all_cell_groups.parquet]`, queried through `distributed_agents_runtime.profile_neighbors` and `distributed_agents_runtime.profile_compare` with `group_name = "151 TH Prkcd Grin2c Glut"`, `gene_target` as the entity, `names` as the measured gene, `logfoldchanges` as the signed value, and `pvals_adj < 0.05` as the significance annotation.
- Same-experiment semantic layer: `mcp__distributed_agents_corpus`, release `perturbai-july-260713-sourceguard-1773-v1`, especially `target_context` for `Twist1`, `Twist2`, `Tcf3`, `Tcf4`, `Tcf12`, and `Zeb1`.
- External literature from PubMed:
  - Fan et al. 2020, DOI `10.1128/MCB.00663-19`, PMID `32179550`: TWIST1 forms homodimers and heterodimers with the E-proteins TCF3, TCF4, and TCF12, with dimer-specific effects on neural-crest and mesodermal differentiation.
  - Connerney et al. 2006, DOI `10.1002/dvdy.20717`, PMID `16502419`, and Connerney et al. 2008, DOI `10.1016/j.ydbio.2008.03.037`, PMID `18471809`: Twist1 dimer partner balance regulates cranial suture patterning, FGF responsiveness, and craniosynostosis in mouse.
  - Fan et al. 2021, DOI `10.7554/eLife.62873`, PMID `33554859`: TWIST1 works with chromatin regulators to control cranial neural-crest differentiation.
  - Soldatov et al. 2019, DOI `10.1126/science.aas9536`, PMID `31171666`: cranial neural crest gains ectomesenchymal potential through a Twist1-associated program.
  - Han et al. 2021, DOI `10.7554/eLife.62387`, PMID `33482080`: Runx2 and Twist1 interact in cranial neural-crest-derived soft-palate mesenchyme.
  - Huang et al. 2014, DOI `10.1371/journal.pone.0099331`, PMID `24971743`: Twist1 and Twist2 are homologous bHLH factors with overlapping developmental expression and cooperative skeletal effects.

## Computational calibration

I first read the focal training count CSV and the held-out manifest. The manifest had exactly one row, `Twist1`, and it had no overlap with the 1,674 training targets, as expected.

The focal endpoint is very sparse in training:

- `n = 1674` non-held-out perturbations.
- `1205 / 1674` have `n_degs = 0`.
- Median = `0`, 75th percentile = `1`, 90th percentile = `2`, 95th percentile = `18`, maximum = `2677`.

I then looked up candidate biological analogs in the training endpoint:

| training perturbation | focal `n_degs` | rationale |
| --- | ---: | --- |
| `Twist2` | 0 | closest represented Twist-family paralog |
| `Tcf3` | 0 | class-I E-protein, predominant TWIST1 dimer partner |
| `Tcf4` | 0 | class-I E-protein, TWIST1 dimer partner |
| `Tcf12` | 0 | class-I E-protein, TWIST1 dimer partner and craniosynostosis gene |
| `Runx2` | 0 | cranial neural-crest and osteogenic pathway counterparty to Twist1 |
| `Snai2` | 0 | EMT / neural-crest regulator, useful as an EMT-family counterexample |
| `Sox9` | 0 | neural-crest / chondrogenic regulator |
| `Neurod1`, `Neurod2`, `Atoh1`, `Myod1` | 0 each | represented bHLH comparators |
| `Zeb1` | 15 | EMT-adjacent transcriptional repressor that produced a small thalamic response but in a different ZEB/CtBP module |

For the same nominated cohort, I ran a focal-cell profile comparison over all measured genes in the DE parquet. The profile activity table reported zero significant features for `Twist2`, `Tcf3`, `Tcf4`, `Tcf12`, `Runx2`, `Snai2`, `Sox9`, `Neurod1`, and `Neurod2`; `Zeb1` was the only nominated EMT-adjacent/bHLH-neighborhood counterexample with a positive focal count, at 15 significant features. The leading log-fold-change features in the zero-count anchors were not FDR-significant, so their large raw log-fold changes did not provide a hidden low-amplitude coherent pattern that would override the endpoint count.

## Target-specific reasoning

### `Twist1`

`Twist1` itself has no same-experiment finding, claim, or explicit comparator reference in the selected Distributed Agents corpus, so I did not have direct held-out expression evidence to transfer. I treated the absence of a corpus node as missing annotation, not as a negative result.

The strongest in-dataset analog is `Twist2`, which had `n_degs = 0` in `151 TH Prkcd Grin2c Glut`. The same-experiment Distributed Agents corpus also records `Twist2:F001` as a high-confidence pan-neuronal negative result in the P16-to-P37/44 NeuN-positive assay: `Twist2` produced no robust downstream single-nucleus RNA response in any of the 23 measured neuronal groups. That is directly relevant because Huang et al. 2014 showed that Twist1 and Twist2 are highly homologous bHLH transcription factors with overlapping developmental expression and cooperative roles in bone formation. `Twist2` is not a perfect substitute for `Twist1`, but it is the represented perturbation closest to the held-out target.

The next mechanistic analogs are the E-proteins `Tcf3`, `Tcf4`, and `Tcf12`, because TWIST1 works as a bHLH dimer and Fan et al. 2020 identified TWIST1 homodimers and TWIST1 heterodimers with TCF3, TCF4, and TCF12 as predominant dimer combinations in cranial mesenchyme. All three E-protein perturbations had `n_degs = 0` in the focal cell group. The same-experiment corpus found the same qualitative behavior more broadly: `Tcf3` had no FDR-supported response in any measured NeuN-positive group; `Tcf12` was a pan-neuronal transcriptional null; and `Tcf4`, while not globally null, had only a narrow Pvalb `Oprd1`/`Tmem44` response that `Tcf3` and `Tcf12` did not phenocopy. Thus the relevant class-I E-protein neighborhood does not predict a thalamic `151` response.

I also considered developmental partners and counterexamples. `Runx2` had `n_degs = 0` in the focal group, and the corpus reports that canonical osteoblast and cranial-neural-crest effector panels were absent after `Runx2` perturbation in sampled neurons. This is a useful negative analog because Han et al. 2021 placed Runx2 and Twist1 in a cranial neural-crest soft-palate program, but that program lives in craniofacial mesenchyme rather than NeuN-positive brain nuclei. `Snai2`, `Sox9`, `Atoh1`, `Neurod1`, `Neurod2`, and `Myod1` were also focal-cell nulls, further arguing that the represented developmental bHLH or neural-crest transcription factors are usually quiescent in this postnatal neuronal screen.

`Zeb1` was the only local counterexample I found among EMT-adjacent factors: it had `n_degs = 15` in the focal group. I did not transfer that count to `Twist1`. The Distributed Agents corpus describes the `Zeb1` response as a small, all-up epithelial junction / polarity / vesicle-trafficking cassette shared partly with `Ctbp1`; it explicitly found that `Zeb2`, TGF-beta receptors, SMADs, `Snai2`, `Twist2`, `Tcf3`, `Tcf4`, and `Tcf12` failed to recover the `Stxbp2`-`Ap1m2`-`F11r`-`Patj` module. Mechanistically, ZEB/CtBP derepression is separable from TWIST1 E-protein dimer biology, so `Zeb1` supports the assay's ability to see a modest thalamic EMT-adjacent signal without making `Twist1` likely to have the same signal.

External biology points in the same direction. `Twist1` is a major regulator of embryonic neural crest, cranial mesenchyme, and cranial sutures: Connerney et al. 2006 and 2008 showed that Twist1 dimer partner balance controls cranial suture patterning; Fan et al. 2021 showed that a TWIST1/chromatin-regulator module controls neural-crest differentiation; and Soldatov et al. 2019 linked cranial neural-crest ectomesenchymal fate acquisition to activation of a Twist1-associated program. Those mechanisms are plausible in embryonic neural crest and mesenchymal progenitors, but the assay here edited sparse postmitotic juvenile NeuN-positive nuclei and excluded or under-sampled cranial mesenchyme, meninges, glia, vasculature, and the olfactory bulb/hindbrain. I therefore expect little or no cell-autonomous thalamic glutamatergic RNA effect from `Twist1` loss.

Prediction: `0` DEGs for `Twist1`.

## Limits and extrapolation

The prediction is extrapolative because `Twist1` itself was held out and the Distributed Agents corpus did not contain a direct `Twist1` node. The focal data provide excellent negative analogs for `Twist2` and the E-proteins, but they do not prove that `Twist1` is unexpressed or inactive in every `151 TH Prkcd Grin2c Glut` nucleus. `Tcf4` also shows that one E-protein can have a narrow postnatal neuronal role outside the focal cell group, so bHLH family membership alone is insufficient. Conversely, the `Zeb1` positive response shows that some EMT-adjacent repressors can produce small thalamic signatures, but the same-experiment evidence argues that this ZEB/CtBP module is not shared by the Twist/E-protein perturbations. Given the endpoint's zero inflation and the direct `Twist2`/`Tcf3`/`Tcf4`/`Tcf12` focal nulls, assigning a nonzero value to `Twist1` would require a target-specific neuronal-maintenance mechanism that I did not find.
