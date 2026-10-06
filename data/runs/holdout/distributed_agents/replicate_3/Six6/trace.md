# DEG-count prediction trace

## Question and endpoint

The requested held-out target list contains one perturbation:

| target_name |
|---|
| Six6 |

I interpreted the endpoint as the number of measured genes in `151 TH Prkcd Grin2c Glut` with `pvals_adj < 0.05` after a sparse AAV-PHP.eB CRISPR loss-of-function perturbation delivered at P16 and assayed at P37-44. Six6 itself was completely held out, so its DEG count and its expression signature were not used. A prediction of zero means that no individual gene is expected to pass the Benjamini-Hochberg FDR cutoff in this cell group; it does not mean that Six6 has no developmental function or that editing would fail.

## Sources used

- `training_de_all_cell_groups.parquet`: per-gene log2 fold changes, Wilcoxon scores, and adjusted p-values for all non-held-out perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed `n_degs` in the focal cell group for 1,674 non-held-out perturbations.
- `208_Six6.csv`: requested held-out manifest; this contained only `Six6`.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`: I queried `Six6`, `Six3`, `Rax`, and `Sox2` target contexts. The corpus had no Six6 target entry, but it did contain same-experiment findings for Six3, Rax, Sox2, Hesx1, Otx2, Pou1f1, Pax6, and Six5.
- Distributed Agents runtime profile tools: I compared focal-cell log-fold-change profiles for the represented Six6 analogs and counterexamples.
- PubMed literature via BioEval Literature:
  - Jean, Bernier and Gruss 1999, PMID 10473118, DOI `10.1016/S0925-4773(99)00068-4`: mouse Six6/Optx2 is a Six3-related homeobox gene expressed in the presumptive pituitary/hypothalamic axis and ventral optic stalk.
  - Li et al. 2002, PMID 12130660, DOI `10.1126/science.1073263`: Six6 acts with Dach corepressors to regulate progenitor proliferation in retina and pituitary.
  - Lopez-Rios et al. 2003, PMID 12441302, DOI `10.1242/dev.00185`: SIX6 and SIX3 interact with Groucho/TLE-family repressors.
  - VanDunk, Hunter and Gray 2011, PMID 21525287, DOI `10.1523/JNEUROSCI.5385-10.2011`: Six3 and Six6 mark the embryonic suprachiasmatic nucleus region; early Six3 deletion prevents SCN formation.
  - Clark et al. 2013, PMID 23382588, DOI `10.1177/0748730412468084`: Six6-null mice have abnormal SCN development and circadian behavior.
  - Pandolfi et al. 2019, PMID 31705443, DOI `10.1007/s12035-019-01781-9`: Vax1 and Six6 are required for SCN development and function in conditional mouse experiments.
  - Diacou et al. 2018, PMID 30485816, DOI `10.1016/j.celrep.2018.10.106`: Six3 and Six6 jointly maintain multipotent retinal progenitors and suppress Wnt/beta-catenin signaling in embryonic retina.
  - Cheng et al. 2021, PMID 35008655, DOI `10.3390/ijms23010229`: SOX2 regulates SCN neuronal differentiation, with postnatal loss of Six6 and Lhx1 expression after embryonic SCN Sox2 ablation.

## Computational checks

I first calibrated the endpoint distribution in the focal group from the training count CSV. It is extremely zero-inflated:

| quantity | value |
|---|---:|
| training perturbations | 1,674 |
| `n_degs == 0` | 1,205 |
| `n_degs > 0` | 469 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

Six6 is most plausibly compared with the Six3/Six6 Optix subfamily, with the broader retinal-determination Six/Eya/Dach/Pax axis, and with anterior neural, SCN, retinal, and pituitary transcription factors. I filtered the 7.8 GB parquet to the focal cell group and to represented analogs with PyArrow dataset predicates:

```python
flt = (
    pc.field("group_name") == "151 TH Prkcd Grin2c Glut"
) & pc.field("gene_target").isin(analogs)
```

This pulled 17,259 measured genes for each analog target, rather than loading all 616 million rows. The direct focal-cell analog counts were:

| training target | focal `n_degs` | expression-pattern evidence | interpretation for Six6 |
|---|---:|---|---|
| Six3 | 0 | No FDR genes in `151`; `min(pvals_adj) = 1.0`; 167 perturbed nuclei. | Closest represented paralog to Six6 and the strongest available test of an Optix/Six3-Six6-like transcription factor in these postnatal neurons. Its focal null argues against a broad acute Six6 program. |
| Six5 | 0 | No FDR genes; `min(pvals_adj) = 1.0`; 215 perturbed nuclei. | More distant SIX-family member. The corpus finding `Six5:F004` also found that represented SIX/retinal-determination comparators including Six3, Dach1, and Pax6 failed to phenocopy Six5. Useful as a same-family counterexample, not a direct Six6 substitute. |
| Dach1 | 0 | No FDR genes; `min(pvals_adj) = 1.0`; 173 perturbed nuclei. | Six6 can use Dach/Groucho-style corepressor logic in developmental systems, but Dach1 was inactive in this focal postnatal group. |
| Pax6 | 0 | No FDR genes; `min(pvals_adj) = 1.0`; 138 perturbed nuclei. | Eye/anterior neural developmental comparator. Six6 is not simply downstream of Pax6 in the optic primordium, so this is a boundary comparator, and its focal null supports the general absence of an eye-field response. |
| Rax | 0 | No FDR genes; `min(pvals_adj) = 0.649`; 209 perturbed nuclei. | Retinal/hypothalamic homeobox comparator. Same-experiment corpus findings `Rax:F002` and `Rax:F003` found only isolated one-gene Rax effects across the broader experiment and no retinal, pineal, or hypothalamic transcriptional program in postnatal NeuN+ brain neurons. |
| Otx2 | 0 | No FDR genes; `min(pvals_adj) = 0.885`; 162 perturbed nuclei. | Retinal, pineal, and midbrain developmental comparator. Its null and the Distributed Agents `Otx2:F005` comparison argue that Otx/retina/homeobox biology did not recover a shared postnatal neuronal module. |
| Hesx1 | 0 | No FDR genes; `min(pvals_adj) = 1.0`; 222 perturbed nuclei. | Rathke's-pouch/anterior neural comparator. The corpus finding `Hesx1:F003` explicitly tested Prop1, Lhx3, Lhx4, Otx2, Pax6, Pitx2, Pou1f1, Gli2, Pax2, Six3, Rax, and Sox2 and found the matched pituitary/forebrain module absent from the neuronal assay. |
| Pou1f1 | 0 | No FDR genes; `min(pvals_adj) = 1.0`; 208 perturbed nuclei. | Pituitary differentiation counterexample. It is downstream of a different pituitary branch and is useful mainly because the pituitary cascade around Six6 is off-lineage here. |
| Pax2 | 0 | No FDR genes; `min(pvals_adj) = 0.937`; 251 perturbed nuclei. | Optic stalk/midbrain-hindbrain developmental comparator; not a close Six6 paralog, but another sampled eye-region homeobox factor with no focal signal. |
| Sox2 | 2 | Two negative DEGs, `Tnnt1` logFC -1.01, `pvals_adj = 3e-6`, and `Stam` logFC -0.57, `pvals_adj = 0.0147`; 173 perturbed nuclei. | SOX2 is upstream of SCN differentiation and Six6/Lhx1 expression during embryonic SCN development, but its actual acute postnatal response in this focal group is only a two-gene thalamic event. Distributed Agents findings `Sox2:F001` and `Sox2:F005` also found no canonical Sox2 neural-stem or pluripotency program and no phenocopy by measured Sox-family, Notch, Pax6, or chromatin-neighbor targets. |

The relevant exact partners that would have been even closer to Six6 were not available as training perturbations: Six1, Six2, Six4, Vax1, Vax2, Lhx1, Tle1, Tle3, Eya1, Eya2, Dach2, and Six6 itself were absent from the 1,674 training count table.

I also inspected sentinel genes from the Six6/SCN literature in the focal rows for the analogs. `Vip`, `Avp`, `Nms`, and `Lhx1` were queryable but none moved at FDR 0.05 under Six3, Six5, Pax6, Rax, Otx2, Dach1, Sox2, Hesx1, Pou1f1, or Pax2. The Six6-pituitary/progenitor cell-cycle genes available in the focal table were likewise quiet: `Cdkn1b` and `Cdkn2a` had `pvals_adj = 1.0` in every one of those analog perturbations. Six6 mRNA itself was also not FDR-regulated by the represented analogs.

Finally, I ran a Distributed Agents runtime `profile_compare` over `Six3`, `Six5`, `Pax6`, `Rax`, `Otx2`, `Dach1`, `Sox2`, `Hesx1`, `Pou1f1`, and `Pax2` within `151 TH Prkcd Grin2c Glut`. Nine of the ten analogs had `response_activity_status = no_significant_features`; Sox2 had `1_to_9_significant_features`. None of the pairwise analog comparisons had an intersection of FDR-significant positive or negative genes. Some whole-vector correlations were numerically positive because the vectors contain thousands of nonsignificant genes, but their top shared features all had `pvals_adj = 1.0`; I treated those as background rather than as phenocopies.

## Six6-specific reasoning

Six6 is real developmental biology, not a throwaway target. Six6/Optx2 is a Six3-related homeobox factor expressed in embryonic retina, optic stalk, pituitary primordium, and the presumptive hypothalamic axis; it can act as a transcriptional repressor with Dach and TLE/Groucho cofactors; and it is genetically required for normal retina, pituitary, and SCN development. In the SCN specifically, germline or embryonic conditional loss produces structural and circadian phenotypes, and Six3/Six6/Vax1/Lhx1/Sox2 form a plausible anterior-hypothalamic developmental network.

The critical mismatch is timing and sampled lineage. The Perturb-seq experiment perturbs sparse, mostly postmitotic NeuN+ brain neurons at P16 and profiles them several weeks later. It does not assay embryonic progenitors, retina, pituitary, or the initial specification of the SCN. The focal class, `151 TH Prkcd Grin2c Glut`, is a thalamic glutamatergic group rather than the GABAergic SCN lineage where Six6 function is best established. The training data give several checks on that mismatch:

- The closest represented Optix-family paralog, Six3, had 0 DEGs in the focal cell group.
- The broader Six/Eya/Dach/Pax/Rax/Otx/Hesx/Pou pituitary and eye-field neighborhood was also focal-null, with only Sox2 producing two non-SCN genes.
- SCN marker/output genes (`Vip`, `Avp`, `Nms`, `Lhx1`) and Six6-related cell-cycle genes (`Cdkn1b`, `Cdkn2a`) were not redistributed by any represented analog in the focal group.
- Same-experiment Distributed Agents findings already place Six3 and Rax as sparse or null in this P16 NeuN+ assay and explicitly reject recovery of canonical Wnt/BMP/SHH/FGF, retinal, pineal, pituitary, or hypothalamic transcriptional programs.

Those points make a small nonzero Six6 effect less likely than a null. Six6 could in principle be more SCN-specific than Six3 or Dach1, but the exact SCN comparators Vax1 and Lhx1 were absent from the perturbation library, and the measured upstream Sox2 perturbation was only a two-gene thalamic response with no SCN output markers. I therefore predicted that Six6 will not put any gene below FDR 0.05 in `151 TH Prkcd Grin2c Glut`.

## Predicted count

| target_name | predicted_n_degs |
|---|---:|
| Six6 | 0 |

## Limits and extrapolation

- Six6 itself had no same-experiment corpus card and no observed expression signature, so the prediction is extrapolated from Six3/Six5/Rax/Otx2/Pax6/Dach1/Sox2/Hesx1/Pou1f1/Pax2 rather than transferred from a direct perturbation.
- Exact Six6 SCN partners and cofactors were incompletely sampled. Vax1, Lhx1, Six4, Eya genes, Tle1/Tle3, and Dach2 would have made the analog set stronger.
- The broad `151 TH Prkcd Grin2c Glut` cluster could dilute a tiny Six6-expressing subpopulation if one is present.
- The experiment is sparse CRISPR and does not measure indels or protein loss in each nucleus. A focal null does not exclude protein-level Six6 biology or an electrophysiological phenotype.
- Germline and embryonic conditional phenotypes can be much stronger than P16 perturbations in already specified neurons. This is the main reason I let the focal training nulls override the severity of Six6 developmental phenotypes.
