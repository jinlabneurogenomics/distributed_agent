# Trace

## Local data used

The declared parquet contains 745,758,369 Wilcoxon differential-expression rows over 712 row groups. Row-group statistics showed that `151 TH Prkcd Grin2c Glut` is localized to row groups 546-580, so I queried only that group with DuckDB predicate pushdown rather than loading the whole table.

The thalamic slice contains 35,311,914 rows:

- 17,259 measured expression genes per perturbation.
- 2,046 perturbation labels.
- 100 `Safe_target_*` controls and no `Non_target` rows as a `gene_target`.

I used this table for two checks.

1. All predicted symbols had to be present as measured `gene_target` values in `151 TH Prkcd Grin2c Glut`.
2. The thalamic and pan-table Wilcoxon summaries were used as weak evidence for perturbations that still leave recovered nuclei with large expression phenotypes.

The strongest thalamic DE signatures were not identical to the revealed count-depletion list. For example, `Srsf1`, `Uba5`, and `Tpr` have thousands of adjusted-significant thalamic DE genes but are absent from the odd-ranked anchors, whereas the rank-1 `Atp6v1b2` perturbation has no adjusted-significant DE genes in recovered thalamic nuclei. I therefore treated DE magnitude as a tie-breaker and not as the depletion score itself.

## How the odd ranks drove the completion

The revealed list is the only direct endpoint evidence. I used it to infer pathway blocks that recur in the hidden even ranks:

- `Atp6v1b2` and `Atp6v1a` anchor vacuolar ATPase / lysosomal acidification hits, so I prioritized `Atp6v0c`, `Atp6v1e1`, `Atp6ap2`, and `Atp6v0a1`.
- `Psmb4` and `Pomp` anchor proteasome and proteostasis hits, so `Psmc1`, `Psmc5`, and other protein-homeostasis genes were promoted.
- `Cltc`, `Gbf1`, `Sec31a`, and `Stx5a` indicate vesicle, COPI/COPII, endosomal, and Golgi trafficking vulnerability, favoring `Copa`, `Copg1`, `Ap2s1`, `Ap2m1`, `Rab7`, and `Xpo1`.
- `Pafah1b1`, `Kif1a`, and `Tbcd` point to microtubule transport, so I kept `Dync1h1` and `Dctn1` high.
- `Chmp4b` and `Snf8` anchor an ESCRT/endosomal-sorter block, making `Vps37a` the closest measured ESCRT-I partner.
- `Taf1`, `Son`, `Tnpo3`, `Polr3b`, `Cnot1`, `Ddx23`, `Brd4`, `Cdk13`, and `Thoc1` made spliceosome, RNA-processing, transcriptional, and chromatin regulators plausible lower hits, including `Srsf1`, `Tpr`, `U2af2`, `Rnpc3`, `Prpf6`, `Hnrnpu`, `Snrnp70`, `Cdc40`, `Naa20`, `Sin3a`, `Yy1`, `Wac`, and `Trrap`.
- The lower revealed ranks include weaker or more context-specific anchors such as `Mc3r`, `Gal`, and `P2ry14`; for the tail of my list I preferred measured genes with both neuronal survival relevance and detectable thalamic expression response over unsubstantiated GPCR guesses.

## External evidence used

The external literature was used only to support pathway plausibility, not to identify a hidden rank table.

- Colacurcio and Nixon review that lysosomal pH is maintained by vacuolar ATPase and that neurons are vulnerable to persistent lysosomal acidification defects, supporting the high priority of `Atp6v0c`, `Atp6v1e1`, `Atp6ap2`, and `Atp6v0a1` next to the revealed `Atp6v1b2` and `Atp6v1a` hits. PMID: 27197071.
- Reiner and Sapir review the dosage-sensitive role of LIS1/PAFAH1B1 in cytoplasmic-dynein regulation and neuronal high-load transport, supporting the dynein/dynactin candidates `Dync1h1` and `Dctn1` around the revealed `Pafah1b1` and `Kif1a` anchors. PMID: 23973156.
- Christ et al. review ESCRT-I/II/III and VPS4 as membrane-scission machinery for multivesicular endosome biogenesis, membrane repair, nuclear-pore quality control, and neuron pruning, supporting `Vps37a` as an ESCRT partner of the revealed `Chmp4b` and `Snf8` hits. PMID: 27669649.
- Ingold et al. show that GPX4 activity protects specific neurons from hydroperoxide-induced ferroptosis, consistent with the revealed `Gpx4` depletion hit and with oxidative/proteostasis genes as a survival class rather than direct marker effects. PMID: 29290465.
- Giandomenico, Alvarez-Castelao, and Schuman review the special proteostasis burden of polarized neurons, supporting the proteasome and RNA/protein-quality-control placements that flank `Psmb4`, `Pomp`, `Hspa9`, `Ddx23`, and `Thoc1`. PMID: 34489114.

## Limitations

The DE parquet reports expression among nuclei that were still recovered after perturbation. It does not report how many nuclei were lost, and the strongest count-depletion hits can leave too few surviving cells to generate a large Wilcoxon signature. The even ranks are therefore a reconstruction from 50 odd endpoint anchors plus pathway membership, not an exact count-score calculation.
