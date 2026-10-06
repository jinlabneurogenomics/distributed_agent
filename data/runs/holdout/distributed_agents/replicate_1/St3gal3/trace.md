# DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and endpoint

I interpreted the task as a scalar holdout prediction for `St3gal3`: predict the number of genes with Wilcoxon Benjamini-Hochberg `pvals_adj < 0.05` after acute AAV-CRISPR loss of `St3gal3` in `151 TH Prkcd Grin2c Glut` neurons. The held-out `St3gal3` rows were absent from both supplied inputs, so no expression vector or count from `St3gal3` itself was used. The requested endpoint is directly observed for the non-held-out training perturbations through `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; for the held-out perturbation the endpoint is absent by construction and must be inferred.

The count endpoint includes the perturbed transcript itself when that row passes FDR, as shown by `St3gal5` having `n_degs = 1` in the focal class and the only FDR < 0.05 row being `names == St3gal5`. I therefore allowed an on-target transcript to contribute one predicted DEG, but I did not treat self-transcript knockdown as an editing-efficiency score.

## Sources

- Declared training counts: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression Parquet: `training differential-expression dataset`.
- Requested-target manifest: `single-target request for St3gal3`.
- Run-local `perturbai-atlas-v5` dataset portrait and measurement registry.
- Internal same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`, especially the packaged `St3gal5` and `B3gat3` Findings/Evidence records.
- PubMed literature for ST3Gal and GM3-ganglioside biology.

Key external citations used for mechanism were:

- Kono et al. 1997, DOI `10.1093/glycob/7.4.469`: mouse ST3Gal I-IV substrate specificity; ST3Gal III and IV prefer type I/type II lactosamine acceptors rather than the GalNAc-centered type III acceptor preferred by ST3Gal I/II.
- Matsuhashi, Horii and Kato 2003, DOI `10.1046/j.1471-4159.2003.01257.x`, PMID `12485401`: ST3Gal II, III and V mRNAs are expressed in neurons throughout adult mouse brain, while other ST3Gal enzymes are more regionally restricted; epileptogenesis most strongly induced thalamic ST3Gal IV.
- Edvardson et al. 2012, DOI `10.1111/epi.12050`, PMID `23252400`: deleterious human `ST3GAL3` variants abolish ST3Gal-III activity and cause West syndrome/developmental epileptic encephalopathy.
- Yoo et al. 2015, DOI `10.1096/fj.15-270983`, PMID `25846372`: engineered `St3gal2`/`St3gal3` deficiency perturbs brain gangliosides, myelination and neuronal structure/function.
- van Diepen et al. 2018, DOI `10.1038/s41431-018-0220-5`, PMID `30089820`: patient-derived cortical neurons carrying an `ST3GAL3` variant show altered lectin staining and adhesion, linking ST3Gal-III deficiency to neuronal glycosylation rather than to a known acute transcription factor program.
- Indellicato et al. 2020, DOI `10.1093/glycob/cwz079`, PMID `31584066`: loss-of-function `ST3GAL3` can be partly replaceable by other ST3Gal enzymes for some glycan epitopes, supporting incomplete but real redundancy among ST3Gal family members.
- Bharathi et al. 2022, DOI `10.1016/j.ymgme.2022.10.006`, PMID `36335793`: germline GM3 synthase/`St3gal5` deficiency alters ganglioside biology and brain glucose metabolism, but in a complete developmental model.

## Computation over the declared inputs

The requested manifest had exactly one held-out target:

```tsv
target_name
St3gal3
```

I summarized the focal training counts and used the Parquet only for exact focal and pathway-comparator rows. The focal count distribution was sparse: among 1,674 training perturbations, 1,205 had zero DEGs, 276 had exactly one DEG, and 469 had any positive count.

The narrow Parquet query used to verify `St3gal5` and adjacent training targets was:

```sql
SELECT gene_target,
       count(*) FILTER (WHERE pvals_adj < 0.05) AS n_degs,
       min(pvals_adj) AS min_padj,
       arg_min(names, pvals_adj) AS min_gene,
       max(n_pert_matched) AS n_pert,
       max(n_ctrl_matched) AS n_ctrl
FROM read_parquet($declared_parquet)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN ('St3gal5','B3gat3','Gal','Galr1','Lgals3')
GROUP BY gene_target
ORDER BY gene_target;
```

The resulting focal counts were:

| training perturbation | focal `n_degs` | most significant focal row | recovered perturbed nuclei | interpretation |
| --- | ---: | --- | ---: | --- |
| `St3gal5` | 1 | `St3gal5`, FDR `1.96e-14`, logFC `-0.788` | 163 | Closest measured sialyltransferase/glycosphingolipid analog; only the self transcript crossed FDR 0.05 in the focal class. |
| `B3gat3` | 0 | minimum FDR 1 | 204 | Golgi glycosaminoglycan linker enzyme; biochemical extracellular-matrix defect did not produce a focal neuronal RNA response. |
| `Gal` | 0 | minimum FDR 1 | 149 | Neuropeptide, name overlap only; a counterexample to treating lexical `gal` hits as sialylation analogs. |
| `Galr1` | 0 | minimum FDR 1 | 266 | Galanin receptor, not a Golgi glycosyltransferase. |
| `Lgals3` | 0 | minimum FDR 1 | 169 | Lectin/glycan-binding protein, but glial and inflammatory roles make it a weak analog in NeuN+ neurons. |

`St3gal5` was also flat across the same-experiment atlas. In 22 assayed groups it usually showed on-target `St3gal5` RNA reduction but almost no secondary DEGs. In the internal corpus record `St3gal5:F002`, a targeted query found 39 ganglioside-enzyme, sphingolipid-catabolic, UPR/ISR, apoptosis, immediate-early, and glucose/mitochondrial sentinel transcripts; none reached FDR < 0.10 in any `St3gal5` group. `St3gal5:F003` further reported that training sphingolipid comparators `Sptlc2`, `Asah1`, and `Psap` did not phenocopy the weak `St3gal5` signature. This argues that acute loss of a ganglioside sialyltransferase can have a real primary lipid/glycan defect without forcing a broad nuclear stress response in the recovered postnatal neurons.

## Target-specific transfer for St3gal3

`St3gal3` encodes ST3Gal-III, a Golgi beta-galactoside alpha-2,3-sialyltransferase. Mechanistically it is an appropriate but imperfect transfer from `St3gal5`:

- Same direct molecular consequence class: both perturbations remove a sialyltransferase and should reduce specific alpha-2,3-sialylated glycoconjugates.
- Different limiting substrate: `St3gal5` is GM3 synthase at the lactosylceramide-to-GM3 step in ganglio-series ganglioside biosynthesis, whereas ST3Gal-III prefers terminal Gal beta 1,3/1,4 GlcNAc acceptors on type I/type II glycoprotein or glycolipid glycans. They are not an obligate protein complex and one enzyme is not downstream of the other.
- Propagation expectation: the most likely acute consequence of `St3gal3` loss in postmitotic neurons is changed cell-surface glycosylation/adhesion, not a large immediate transcriptional stress program. Human ST3GAL3 disease and ST3Gal2/3 mutant mice show that the biology matters in development, but those data are germline/developmental or patient-neuron settings and do not imply hundreds of FDR-significant nuclear RNAs after sparse P16 CRISPR.
- Exposure/sampling expectation: ST3Gal III is reported in neuronal cells broadly in adult mouse brain, including thalamic territories through the broad distribution seen by Matsuhashi et al.; with 23,679 matched focal control nuclei and enough focal power to call the `St3gal5` self transcript, one on-target `St3gal3` row is plausible if `St3gal3` is expressed in these nuclei.
- Counterexamples: same-experiment `B3gat3` showed that perturbing a Golgi glycan enzyme can be biochemically meaningful yet produce no focal RNA DEGs, and clinical epilepsy genes such as `Mecp2`, `Kcnq2`, `Cntnap2`, and `Cdkl5` did not reproduce the `St3gal5`-like sparse glycosylation surface in the focal class. Clinical overlap with epileptic encephalopathy therefore was not used to raise the count.

Because the training set did not contain `St3gal1`, `St3gal2`, `St3gal4`, `St3gal6`, `Ugcg`, `B4galt5`, `B4galt6`, `St8sia1`, `B4galnt1`, or `B3galt4`, there was no within-dataset direct test of the nearest `St3gal3` paralogs or its immediate glycan branch. The decision is therefore driven by one measured same-enzyme-class analog, `St3gal5`, plus external ST3Gal biology. The external data establish that `St3gal3` is neuronal and disease relevant, but also that glycan enzymes have substrate overlap and developmental/tissue dependencies. I predicted a nonzero count of 1 rather than zero because the best focal analog had exactly one FDR-significant row, and that row was the sialyltransferase transcript itself; I did not predict additional downstream genes because neither `St3gal5` nor `B3gat3` generated a broad focal glycosylation, UPR, apoptosis, metabolic, or activity-dependent signature.

## Final prediction

| target_name | predicted_n_degs |
| --- | ---: |
| `St3gal3` | 1 |

## Limits

The main weak point is the lack of a measured acute `St3gal3` paralog in the training set: `St3gal5` is the closest assayed sialyltransferase, but it acts on a different glycan substrate pool. All external ST3GAL3 evidence is either expression, congenital human disease, engineered mouse deficiency, or iPSC-derived cortical-neuron biology, not sparse AAV-Cas9 loss in juvenile thalamic glutamatergic neurons. The assay measures survivor-conditioned nuclear RNA and not the primary sialylated glycan products, ganglioside abundances, adhesion biochemistry, or pre-assay selection. Thus the one-DEG prediction is best read as "self transcript only, no confident secondary program" rather than as a prediction that `St3gal3` is biologically unimportant.
