# Q3 literature assessment methods

## Eligibility

The input parquet was filtered to the ten targets in `[local file: n0010.targets.json]`: Srsf1, Uba5, Sin3a, Wdr26, Ogt, Thap11, Tnpo3, Tsc1, Thoc1, Atp6v0c. Eligible pairs were computed with this exact downstream query:

```sql
SELECT DISTINCT gene_target, group_name
FROM read_parquet('[local file: wilcoxon_de_results_group_name_final_data_no_multi_guide_cells.parquet]')
WHERE gene_target IN ('Srsf1','Uba5','Sin3a','Wdr26','Ogt','Thap11','Tnpo3','Tsc1','Thoc1','Atp6v0c')
  AND group_name IN (<23 allowed cell groups>)
  AND lower(names) != lower(gene_target)
  AND pvals_adj < 0.10;
```

This returned 144 eligible perturbation x cell-type pairs after the perturbed transcript itself was excluded case-insensitively. The JSONL output emits 144 pair rows and omits only measured target/cell-type combinations with no remaining downstream gene at `pvals_adj < 0.10`.

## Phenotype characterization

For every eligible pair I reread the FDR-significant downstream rows and recorded the perturbed/control nucleus counts, the number of up- and down-regulated downstream genes, the genes with the smallest adjusted p-values, and the largest absolute log-fold changes. Broad responses were summarized by the recurring top-FDR genes and by coherent target-level modules: Srsf1 and Tnpo3 RNA-processing/splicing-factor responses, Uba5 ER and mitochondrial stress, Sin3a chromatin and RNA-processing responses, Ogt O-GlcNAc/RNA-processing responses, Thap11 Ronin-HCF1 transcription/metabolism responses, Tsc1 mTORC1/lysosomal/sterol responses, Atp6v0c V-ATPase/lysosomal/autophagy responses, and Thoc1 THO/TREX mRNA-export responses. Very small signatures were summarized by their individual FDR-supported genes rather than forced into a module.

## Literature search

Searches used PubMed via the bioeval_literature gateway. I first searched target-specific mechanisms using queries such as `SRSF1 knockdown splicing`, `UBA5 UFM1 ER stress`, `TSC1 mTORC1 neuron knockout`, `ATP6V0C`, `O-GlcNAc splicing factors OGT`, `Sin3a neurons`, `Ronin HCF-1`, `TNPO3 splicing factor import`, `THOC1 mRNA export DNA damage`, and `WDR26`. I then searched exact target plus observed-gene combinations for sparse or unsupported pairs, including `ATP6V0C Rad52 Thpo`, several `OGT` plus sparse-hit queries, `THOC1 Igip Ncaph2 Rhot2 Evl Uchl1`, `TNPO3 Samm50 Clock Fam171b Ppp5c Rap1gap`, `TSC1 Spag5 Rsrp1`, `UBA5 Drosha H1f4 Scyl2 Nt5m`, and WDR26 queries with `Srrm2`, `Col11a2`, `Grin2b`, `Baiap3`, `Cacna1g`, and `extracellular matrix collagen neuron`. Roughly one to four mechanistic papers or abstracts were reviewed per target module; the exact-hit searches returned no target-specific bridge for the pairs marked No Literature.

## Flag rules

A pair was marked Inferred when the literature established a target-specific bridge to the observed response class but did not document the measured genes or their directions in a comparable acute postmitotic neuronal perturbation. Examples include OGT/O-GlcNAc control of detained-intron splicing for Ogt pairs with RNA-processing genes, TNPO3 import of SR proteins for Tnpo3 pairs with Srrm2/Srsf-family changes, and UBA5 control of UFM1 activation for Uba5 pairs with ER or mitochondrial stress features. Directionally interpretable mTORC1, V-ATPase, THO/TREX, SRSF1, SIN3A, and Ronin-HCF1 priors were not upgraded to Agree unless they predicted the central observed transcript module rather than only a broad phenotype or family process.

No Literature was used only after a pair-specific search failed to find a target-to-response bridge. This covered the Wdr26 pairs, where WDR26-CTLH literature documents chromatin and ubiquitin-ligase biology but not the observed Srrm2/Col11a2/Cacna1g modules, and isolated sparse hits such as Atp6v0c-Rad52/Thpo, Uba5-Drosha, Tnpo3-Fam171b/Ppp5c/Rap1gap, Thoc1-Evl, and Tsc1-Spag5.

## Multi-module pairs

When a pair had hundreds or thousands of DE genes, the pair-level flag follows the recurring, FDR-supported target-level module rather than a single largest-effect outlier. Largest-effect genes that were not part of the cited bridge are still listed in `q3_evidence.jsonl`; those outliers were not allowed to turn a module-level Inferred call into Agree or Disagree.

## Difficult or low-confidence pairs

The broad Srsf1, Sin3a, Thap11, Tnpo3, and Thoc1 signatures are low-confidence Inferred calls because published work usually describes alternative splicing, mRNA export, or chromatin state, whereas the screen measures steady-state single-nucleus mRNA abundance. Uba5 and Atp6v0c had several stress-like or organelle-like signatures, but exact Ddit3, Herpud1, Atp6v0a1, and Ecel1 directions after acute neuronal target loss were not documented. All 144 eligible pairs were inspected and emitted; incompletely reviewed pair count was 0.
