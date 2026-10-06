# Direct n_degs forecast for Guk1

Endpoint: number of genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Declared target

- Target: `Guk1`.
- Exact focal-population reach from the declared biology bundle: the `Guk1` feature is present in `151 TH Prkcd Grin2c Glut`, with mean log1p(CP10k) 0.401, mean raw UMI 1.007, and 13,809 of 23,679 non-target nuclei expressing it, or 58.3%.
- Functional-stock adjudication: loss of new cytosolic and mitochondrial Guk1 synthesis is expected to matter by the P37-P44 harvest because Guk1 supplies renewable GMP/dGMP phosphorylation capacity; the card concludes that functional stock is likely substantially depleted, but with only partial evidence because no matched P16 postmitotic thalamic Guk1 time course or target-specific protein half-life was found.
- Biological caveat: the strongest phenotypic evidence is systemic mouse preweaning lethality and human biallelic GUK1 deficiency with mtDNA depletion in fibroblasts, not an acute postnatal thalamic-neuron loss experiment. The exact expression reach establishes availability of the target transcript, not the downstream DEG count.

## Training measurements used

The declared 151 TH count table contains 1,674 held-in biological perturbations. Its mass is strongly concentrated at zero: 1,205/1,674 targets have `n_degs = 0`, 469 are nonzero, 106 have at least 10 DEGs, 43 have at least 100, and only 3 exceed 1,000. The mean is 14.1 because of a long positive tail; the median and 70th percentile are both 0.

There was no close measured guanylate-kinase paralog. I therefore used a conservative local panel of nucleotide-adjacent and mitochondrial/metabolic perturbations whose functions should have produced flux defects but which were represented in the same training count table:

- `Adk`: 0 DEGs, the nearest purine-adjacent comparator in the table.
- `Nt5c2`: 0 DEGs, referenced in the same Adk/purine-adjacent corpus finding.
- BCAA/organic-acid mitochondrial enzymes: `Auh`, `Bckdhb`, `Bckdk`, `Ivd`, `Mmaa`, and `Pcca` all had 0 DEGs; the packaged claim over these targets states that represented BCAA/leucine and organic-acid catabolic nodes were broadly buffered at the postnatal neuronal nuclear-RNA level.
- Complex-IV structural or assembly comparators were also essentially flat in this focal count table: `Cox4i1`, `Cox6a1`, `Cox7b`, `Cox8a`, `Cox11`, and `Coa8` had 0 DEGs, while `Cox5a` and `Ndufa4` each had 1.
- Fe-S/iron-homeostasis comparators were likewise near-null: `Abcb7`, `Lyrm4`, `Nfs1`, and `Tfrc` had 0 DEGs and `Isca2` had 1.

The same count table also shows that the assay can produce moderate mitochondrial or stress-like responses for some specific triggers in this class, for example `Opa1` 37, `Esrra` 57, `Nrf1` 138, `Atp2a2` 187, `Elp2` 150, `Elp1` 645, and `Thap11` 478. Those were useful positive scale checks but not direct operation-level analogs for soluble Guk1 nucleotide phosphorylation.

I also compared a 21-target metabolic/stress cohort in the declared expression parquet within `151 TH Prkcd Grin2c Glut`. Thirteen of those 21 selected nodes had no significant feature in this exact focal group, three had 1-9, one had 10-49, and four had at least 50. The selected cohort was not a hidden shared transcriptional module: over 210 profile pairs, median positive top-tail overlap was 0.020 and median negative top-tail overlap was 0.025, with median same-direction significant-program overlap equal to 0. I therefore treated the repeated nulls as endpoint scale evidence and did not infer a synthetic Guk1 profile from their residual score vectors.

## Synthesis

The exact expression and stock card make a real perturbation plausible: Guk1 is expressed in the assayed thalamic nuclei, lacks an identified close mammalian same-reaction paralog in the card, and should lose renewable enzymatic capacity across the 21-28 day edit-to-harvest interval. Those points keep the forecast slightly above an unconditioned blind median.

The endpoint-specific evidence pushes harder downward. The closest measured nucleotide-pool perturbations available were flat, the broader represented mitochondrial metabolic modules repeatedly resolved to 0 or 1 DEG in this neuronal snRNA-seq endpoint, and the corpus explicitly warns that those biochemical defects can be buffered or displaced at the nuclear-RNA level. If complete Guk1 loss is more severe than the represented null enzymes, survivor conditioning and sparse editing could also attenuate the recovered signature.

My point estimate is therefore the mode of this near-null posterior rather than the long-tailed table mean: `Guk1` is predicted to produce no BH-significant downstream genes in the focal 151 TH Prkcd Grin2c Glut contrast.
