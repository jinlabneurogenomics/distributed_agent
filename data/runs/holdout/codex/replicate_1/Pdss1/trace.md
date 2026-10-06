# Pdss1 direct DEG-count forecast

## Target and endpoint

- Target from the one-row manifest: `Pdss1`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counted as measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Declared expression reach in the focal non-target cells is real rather than absent: `Pdss1` is detected in 19,123 of 23,679 nuclei, 80.76% of cells, with mean raw UMI 2.03 and pseudobulk 127.43 cpm.

## Evidence used

`Pdss1` should be functionally reachable by this perturbation more than a generic mitochondrial structural gene. The biology-only card identifies PDSS1 as an obligate PDSS1/PDSS2 polyprenyl-diphosphate synthase subunit for CoQ side-chain synthesis, not a redundant paralog, and its functional-stock adjudication calls the downstream CoQ pool likely substantially depleted by the P37-P44 harvest because rat brain ubiquinone turns over on an approximately 90 h scale. The main caveat is that there is no matched postnatal mouse-thalamic conditional-loss phenotype or direct PDSS1 protein half-life, and the readout is survivor-conditioned nuclear RNA.

The measured 151-class count table is strongly zero-inflated: among 1,674 training perturbations, 1,205 have `n_degs = 0`, 1,481 have `n_degs <= 1`, 1,512 have `n_degs <= 2`, and the median is zero. A nonzero point therefore needs specific local support.

The closest biochemical training evidence points to a buffered, almost-null state. `Pdss2`, the exact physical partner, is absent from the training table. The narrow CoQ/ubiquinol training genes are also sparse: `Coq5 = 0`, `Ndufa9 = 0`, and `Stard7 = 0`; among adjacent terpenoid genes, `Cit = 0`, `Fntb = 0`, `Hmgcr = 0`, and only the dolichol/glycosylation gene `Dhdds` is broad at 116. The raw Parquet confirms that `Coq5` itself has 200 matched 151 perturbed nuclei and no focal FDR genes, so its zero is not a missing-row artifact.

The packaged same-experiment reports make the `Coq5` zero informative: `Coq5` had no downstream FDR<0.10 genes in 22 neuronal groups, lacked the expected mitochondrial ISR/UPR marker set, and did not uncover hidden convergence with UQCRC/CYC1/NDUF/LONP1/CLPP comparators. That is a closer match to PDSS1-dependent CoQ synthesis than `Opa1` or `Dhdds`.

Broader respiratory-chain comparators sit at the same floor in this focal endpoint. In the 151 count table, 45 represented `Nduf*`, `Cox*`, `Uqcr*`, `Sdh*`, and adjacent mitochondrial targets had a total of 19 DEGs, 26 zeros, and no single count above 1. Corpus reports for `Ndufs4` and `Uqcrc2` likewise place Complex I and Complex III perturbations in buffered classes rather than a shared acute OXPHOS-stress RNA program.

`Opa1` and `Dhdds` show the assay can detect stress states in these neurons, but they are not magnitude donors for `Pdss1`: `Opa1` is an inner-membrane dynamics stress branch with 37 focal DEGs, while `Dhdds` couples isoprenoid flux to dolichol-dependent ER glycosylation and reaches 116 focal DEGs through ER/ISR genes. PDSS1 loss should mostly deplete CoQ side-chain production, making `Coq5` and the buffered respiratory-chain class more relevant for count scale than the broad ER-quality-control branch.

## Synthesis

The target is expressed broadly enough, and its functional stock is plausible enough within 21-28 days, that I do not treat it as a categorical biological null. The strongest measured comparators, however, say that CoQ/OXPHOS lesions in this acute sparse postnatal neuronal assay usually fail to cross the nuclear RNA threshold. I therefore put the forecast at the upper edge of the exact CoQ/respiratory-chain floor rather than at the pathway-neutral median.

Predicted `n_degs`: 1
