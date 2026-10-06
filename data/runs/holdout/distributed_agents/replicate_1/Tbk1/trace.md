# DEG-count prediction trace

## Question and endpoint

The requested endpoint is the number of genes called differentially expressed at BH-adjusted Wilcoxon `pvals_adj < 0.05` after acute CRISPR loss of the held-out perturbation in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons.

There is one requested held-out target:

| target_name | predicted_n_degs |
|---|---:|
| Tbk1 | 0 |

I treated `n_degs` as an assay-specific breadth count in recovered nuclei, not as a direct readout of viability, editing efficiency, or biological importance. `Tbk1` is absent from the focal-cell training count table by construction, so the prediction has to transfer from non-held-out perturbations and from TBK1 biology.

## Sources used

- Declared endpoint CSV: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE Parquet: `training_de_all_cell_groups.parquet`; queried only for the focal cell group and a bounded set of TBK1-relevant training perturbations.
- Requested-target CSV: `b0236.csv`, containing only `Tbk1`.
- Run-local dataset portrait, task bindings, measurement registry, coverage, and capability manifest.
- Internal same-experiment corpus: `perturbai-july-260713-sourceguard-1773-v1`; I checked the selected BioKG graph and Findings ledger for `Tbk1` and for compact entries around the candidate analogs. The corpus had no `Tbk1` Findings and no compact story records for the specific TBK1 pathway anchors I used, so it did not contribute target-specific same-experiment interpretation.
- External mechanism literature from PubMed/NCBI E-utilities:
  - Pomerantz and Baltimore 1999, EMBO J, PMID 10581243, DOI 10.1093/emboj/18.23.6694: TBK1 as a TANK/TRAF-associated IKK-related kinase able to signal to NF-kB.
  - Freischmidt et al. 2015, Nat Neurosci, PMID 25803835, DOI 10.1038/nn.4000: human TBK1 loss-of-function/haploinsufficiency causes ALS/FTD and mutant alleles can lose expression or OPTN binding.
  - Richter et al. 2016, PNAS, PMID 27035970, DOI 10.1073/pnas.1523926113: TBK1 phosphorylates OPTN, SQSTM1/p62, CALCOCO2/NDP52, and TAX1BP1 to amplify selective autophagy of damaged mitochondria.
  - Vargas et al. 2019, Mol Cell, PMID 30853401, DOI 10.1016/j.molcel.2019.02.010: TBK1 facilitates NDP52/FIP200/ULK1 recruitment and activation during selective autophagy.
  - Nguyen et al. 2023, Mol Cell, PMID 37207627, DOI 10.1016/j.molcel.2023.04.021: OPTN can initiate PINK1/Parkin mitophagy through TBK1 and the class III PI3K complex.

## Computation over the supplied dataset

The focal endpoint table has 1,674 training perturbations. Its counts are highly sparse and zero-inflated: 1,205 perturbations have `n_degs = 0`, the median is 0, the mean is 14.05, the 75th percentile is 1, and the 95th percentile is 18. Therefore a prediction for a target with no close broad-response analog should stay near zero.

To get TBK1-relevant within-dataset evidence, I inspected every present training target on the direct TBK1 innate immune axis and the closest autophagy module members available in the training set. For each such target I counted significant focal-cell genes from the Parquet using:

```sql
SELECT gene_target, SUM(pvals_adj < 0.05) AS degs
FROM read_parquet('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

The targeted Parquet query returned 17,259 measured genes per inspected focal-cell perturbation. The endpoint counts matched the training CSV and the strongest signed Wilcoxon scores for the silent genes all had `pvals_adj = 1` or high nonsignificant FDRs, rather than a hidden coherent signature close to threshold.

## Target-specific reasoning: Tbk1

`Tbk1` encodes TANK-binding kinase 1. Mechanistically it sits at the convergence of TRAF/MAVS/TLR/STING innate-immune signaling to IRF3 and NF-kB, and it also phosphorylates autophagy receptors such as OPTN and SQSTM1 during selective autophagy/mitophagy. That made three classes of training perturbation biologically relevant:

| training analog | observed n_degs in 151 TH Prkcd Grin2c Glut | interpretation for Tbk1 |
|---|---:|---|
| `Traf3` | 0 | Upstream TBK1/IRF3 adaptor in antiviral signaling; no focal-cell DEG response. |
| `Irf3` | 0 | Canonical TBK1 transcription-factor substrate; no response argues against tonic IRF3-driven expression in these neurons. |
| `Nfkb1` | 0 | NF-kB family branch downstream/parallel to TBK1; no response. |
| `Rel` | 0 | NF-kB family branch; no response. |
| `Chuk` | 0 | IKK/NF-kB pathway kinase; no response. |
| `Tlr3` | 0 | Endosomal innate receptor using TRIF/TBK1 signaling; no response. |
| `Tlr4` | 0 | TLR with TRIF-dependent TBK1 access; no response. |
| `Tlr7` | 0 | Endosomal innate receptor; no response. |
| `Nod2` | 0 | Innate signaling/autophagy crosstalk gene; no response. |
| `Xiap` | 0 | Innate/autophagy and NOD pathway-associated ubiquitin regulator; no response. |
| `Stat1` | 1 | Interferon response transcriptional effector; essentially silent. |
| `Stat2` | 0 | Type I interferon effector; no response. |
| `Irf1`, `Irf2`, `Irf5`, `Irf8`, `Irf9` | 0 each | IRF/interferon family members present in the library; all silent. |
| `Ifnar1`, `Ifnar2`, `Ifngr1`, `Ifngr2` | 0 each | Interferon receptors; all silent. |
| `Atg5` | 0 | Core autophagosome-conjugation factor; no broad focal response. |
| `Becn1` | 0 | Class III PI3K/autophagy initiation; no response. |
| `Atg16l1` | 0 | Core autophagosome-conjugation factor; no response. |
| `Map1lc3a` | 1 | LC3-family autophagy gene; essentially silent. |
| `Sqstm1` | 1 | Selective-autophagy receptor phosphorylated by TBK1; the one DEG was `Sqstm1` itself. |
| `Rb1cc1` | 4 | FIP200/ULK autophagy-initiation scaffold; produced only four DEGs (`Calr`, `Hspa5`, `Rb1cc1`, `Pdia6`), a small ER-proteostasis-like signature rather than a broad TBK1-like inflammatory state. |
| `Lamp2` | 0 | Lysosomal/autophagy endpoint gene; no response. |
| `Vps35` | 17 | Endolysosomal trafficking produced a small nonzero signature, but Vps35 is a retromer core subunit rather than a TBK1 kinase substrate or adaptor, so it is an upper counterexample rather than the best analog. |
| `Mtor` | 2 | Nutrient/autophagy regulator; nearly silent. |
| `Tsc2` | 86 | A strong mTORC1 regulator with a broader neuronal growth/metabolic role; too far upstream and directionally different to use as the expected TBK1 count. |

The direct molecular consequence of a `Tbk1` guide is partial loss of TBK1 kinase function. In a pathogen- or cytosolic-DNA-stimulated immune cell this would propagate to IRF3/NF-kB and interferon programs; in a cell under mitochondrial or cargo damage it would also weaken OPTN/SQSTM1/CALCOCO2/TAX1BP1 selective autophagy. The experiment, however, perturbs sparse postnatal NeuN-positive neurons under baseline in vivo conditions, and the endpoint samples only recovered, class-assigned nuclei. The relevant training perturbations show that neither TLR/IRF/NF-kB genes nor interferon receptors produced measurable focal-cell transcriptional breadth. The autophagy branch also stayed at zero or one for `Atg5`, `Becn1`, `Atg16l1`, `Map1lc3a`, `Sqstm1`, and `Lamp2`, with only a tiny four-gene `Rb1cc1` response. That pattern supports a zero call more strongly than assigning a moderate nonzero count from TBK1's disease importance.

The main counterexamples are `Tardbp` at 210 DEGs and `Matr3` at 149 DEGs, because they are ALS-associated genes like `Tbk1`, and `Tsc2` at 86 DEGs, because it has an autophagy/mTOR relationship. I rejected these as quantitative analogs: `Tardbp` and `Matr3` are nuclear RNA-binding proteins whose direct loss immediately changes RNA processing and transcript levels, while TBK1 is a signaling kinase with stimulus-dependent immune and cargo-clearance outputs. `Tsc2` directly derepresses mTORC1 and caused a distinct metabolic/growth program. Neither is a candidate-specific same-endpoint prior for acute partial `Tbk1` loss in unstimulated thalamic neurons.

## Prediction and limits

The predicted count for `Tbk1` is `0`.

The decision is mostly driven by within-dataset endpoint evidence: all direct TBK1 innate-immune comparators in the training set are at zero, interferon response genes are at zero or one, and the closest autophagy machinery genes are zero to four. External TBK1 literature was used to choose those comparators and to avoid treating unrelated ALS or endolysosomal genes as closer than they are.

This is still an extrapolation. The training set did not include `Ikbke`, `Tank`, `Optn`, `Tax1bp1`, `Calcoco2/Ndp52`, `Mavs`, `Tmem173/Sting1`, or `Ticam1/Trif`, which would have been closer direct tests. The assay reads nuclear RNA at a single 3-to-4-week time point in survivor nuclei, so a TBK1 effect on mitophagy flux, stress sensitivity, or cell survival could be missed. The sparse AAV-CRISPR design also makes a zero DEG call a power- and endpoint-specific prediction, not a claim that TBK1 is unimportant in neurons or neurodegeneration.
