# Q3 literature agreement methods

## Eligibility

I loaded the assigned target manifest exactly as written from `[local file: n0030.targets.json]` and filtered the full DE parquet to `gene_target in ['Psmb4', 'Tpr', 'Ppp2r1a', 'Prpf6', 'Zbtb7a', 'Pomp', 'Ap2s1', 'Yy1', 'Snrnp70', 'Eef2', 'Gatad1', 'Tuba1a', 'Eif4e', 'Kmt2b', 'Adarb1', 'Zfp423', 'Zeb2', 'Cacna1g', 'Tfrc', 'Tnrc6a', 'Nr1d1', 'Arid1a', 'Syn2', 'Wac', 'Hivep3', 'Xpo1', 'Gigyf2', 'Ank3', 'Myef2', 'Ddx23']` and `group_name` in the 23 allowed cell groups. A pair was eligible when at least one row satisfied:

```python
pvals_adj < 0.10 and names.casefold() != gene_target.casefold()
```

That query produced **244** eligible perturbation x cell-type pairs. `q3_cell_type_specificity.jsonl` emits **244** rows, one for each eligible pair, and no rows for pairs whose only significant row was the perturbed target transcript. No pair was incompletely reviewed.

## Phenotype Characterization

For each eligible pair I sorted downstream FDR-significant genes by adjusted p-value and inspected their log-fold-change signs and perturbed/control nucleus counts. Evidence rows report the number of downstream hits and up to eight genes consisting of recurrent target-level module genes, when present in that cell type, followed by the most significant remaining hits. This retained the central modules for repeated phenotypes, including ADARB1-filamin, TUBA1A-tubulin-isotype, YY1-Peg3-domain, PPP2R1A-Jun/AP-1, PSMB4/POMP-proteasome-stress, PRPF6/SNRNP70/DDX23-spliceosome, XPO1-snRNP/RNA-export, WAC-neuronal-state, and ZBTB7A-Gpc1/Pnck/Atp1b2 responses, while still recording isolated singleton responses such as `Syn2` to `Alg10b`.

## Literature Search

I searched PubMed or Entrez with a target name or common alias plus the measured recurrent genes or module terms, for example `ADAR2 filamin`, `YY1 Peg3`, `PP2A c-Jun JNK`, `AP2 clathrin transferrin receptor`, `POMP proteasome maturation`, `proteasome NFE2L1 bounce back`, `TUBA1A beta tubulin autoregulation`, `CRM1 snRNA export`, `TPR nuclear basket mRNA export`, `WAC RNF20 H2B ubiquitination`, `PRPF6 U5 spliceosome`, `SNRNP70 U1 snRNP`, `DDX23 U5 snRNP`, `NR1D1 NPAS2`, `ZFP423 cerebellar granule neuron`, and no-hit target/module searches such as `ZBTB7A PNCK GPC1`, `KMT2B STXBP2 EBF4`, `MYEF2 DZIP3`, `HIVEP3 R3HDM2`, `TNRC6A PTGES2 ATP1A3`, and `SYN2 ALG10B`. I reviewed the abstracts of the first 1 to 5 PubMed hits for positive searches, fetched the cited PubMed records, and kept only papers that supplied a target-to-response or target-to-mechanism relationship rather than background function alone.

## Flag Rules

`Agree` was used when a target-specific paper or a complete mechanistic chain predicted the observed direction: proteasome impairment to NFE2L1 proteasome-gene bounce-back for `Psmb4` and `Pomp`, REV-ERB loss to `Npas2` derepression for `Nr1d1`, YY1 loss to `Peg3` derepression for the YY1 pairs with significant `Peg3`, and PP2A-A alpha loss to JNK/AP-1 induction for Ppp2r1a pairs with significant `Jun` up-regulation.

`Inferred` was used for biologically specific but incomplete bridges. Examples include ADARB1 editing of `Flnb`/`Flna` transcripts without proof that total `Flnb` mRNA should fall, tubulin autoregulation without a direct acute `Tuba1a` knockdown experiment, AP-2/transferrin-receptor endocytosis without measured `Tfrc` transcription, spliceosome membership of PRPF6/SNRNP70/DDX23 without directional compensation rules, XPO1-dependent snRNA export without direct mammalian neuronal `Snrnp70` or `Nxf1` transcription predictions, and WAC-RNF20/RNF40 transcription-coupled H2B ubiquitination without a documented `Eno2`/`Lgi3` module.

`No Literature` was used only after the target plus observed-gene search failed to find a direct or specific partial bridge. General evidence that a target is a transcription factor, chromatin regulator, ion channel, microRNA effector, or translation factor was not treated as sufficient support for isolated genes or unrelated recurrent modules.

## Multi-module Pairs and Low-confidence Areas

When a pair contained several significant modules, I assigned the pair-level flag from the strongest FDR-supported target-specific relationship and disclosed uncaptured modules in the summary text when that mattered. For broad stress responses, the proteasome bounce-back arm was used for `Psmb4`/`Pomp`; for `Yy1`, only pairs with significant `Peg3` were upgraded to `Agree`, and Wsb1-dominant pairs remained `No Literature`; for `Ppp2r1a`, only `Jun`-positive pairs were treated as directional `Agree`, while other Amy1/Leng8/RNA-processing cells remained `Inferred`.

The most difficult low-confidence calls were the broad spliceosome/nuclear-export/chromatin categories, where the perturbed target is mechanistically connected to the affected machinery but individual compensatory transcripts were not documented, and the sparse singleton pairs for `Tfrc`, `Syn2`, `Hivep3`, and `Zeb2`, where searches found no useful bridge. These were still reviewed; the incomplete-review count is **0**.

## Totals

- Eligible pairs: 244
- Emitted pair rows: 244
- Incompletely reviewed pairs: 0
- Flag counts: {'Agree': 43, 'Inferred': 106, 'No Literature': 95}
- Evidence rows: 244
- Referenced literature rows: 19
