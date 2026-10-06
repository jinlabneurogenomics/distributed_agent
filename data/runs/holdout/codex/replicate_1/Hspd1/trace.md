# Hspd1 direct `n_degs` forecast

## Target

- `gene_target`: Hspd1
- `group_name`: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`

## Evidence used

- The declared Hspd1 biology bundle places the perturbation in the mitochondrial matrix HSP60-HSP10 chaperonin. HSPD1 is a dynamic HSP60 ring component with continuing demand for imported and stress-unfolded matrix clients, so loss of new HSPD1 supply is biologically material in neurons.
- The same bundle argues against an instant full knockout: adult mouse brain HSPD1 half-lives of roughly 25-30 days make the 21-28 day P16-to-P37/P44 assay window only about one target half-life. I treated this as partial or leading-edge depletion of the pre-edit HSP60 stock.
- The exact focal expression measurement showed Hspd1 was within reach in this cell class, not absent: 13,638 of 23,679 non-target nuclei expressed Hspd1, `pct_cells_expressing = 57.595337640947676`, `mean_cp10k = 0.5866426131218335`, and `pseudobulk_cpm = 59.76736116449741`.
- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` was extremely zero-heavy: among 1,674 training targets, the median was 0, the 75th percentile was 1, the 95th percentile was 18, and only 43 targets had at least 100 DEGs. A teens-scale prediction is therefore a moderate positive response in this context.
- I used the declared Parquet to inspect exact matched 151-class profiles for observed mitochondrial and proteostasis comparators. Direct stress or chaperone comparators were small:
  - Hspa5: 5 DEGs
  - Hsf1: 6
  - Hspa8: 9 from the count table
  - Sec63: 11
  - Opa1: 37
- The same exact 151 counts put many mitochondrial loss perturbations at null or self-target-only scale:
  - Afg3l2: 0
  - Yme1l1: 0
  - Timmdc1: 0
  - Tomm40: 1
  - Sod2: 1
  - Park7: 1
  - Ppargc1a: 0
- Packaged same-experiment Findings gave the mechanistic meaning of those counts. Hspa5 induced an ER folding and ERAD module in 151; Opa1 induced an ATF4/ISR-like amino-acid stress program and was the clear positive mitochondrial-stress benchmark; Opa1 nevertheless did not induce a canonical Hspd1/Hspe1/Clpp mitochondrial UPR or Pink1/Prkn mitophagy transcriptome. Tomm40 loss was a measured import-pore perturbation that failed to induce ISR/ATF, UPRmt-chaperone/protease, proteasome, or TOM-subunit compensation genes.

## Synthesis

I called Hspd1 nonzero because the focal population expresses the gene and HSP60 is a nonredundant mitochondrial folding machine whose stock should begin to decline over the harvest interval. I kept it far below large ER-glycosylation and proteasome-like responders because the Hspd1 card supports only partial stock depletion by harvest, the strongest postnatal neural phenotype was late-onset after lifelong heterozygosity, and several mitochondrial training perturbations were transcriptionally buffered in the same assay.

The numerical anchor was the small chaperone/stress group: Hspa5, Hsf1, Hspa8, and Sec63 sit at 5-11 DEGs, while Opa1 at 37 DEGs is a stronger inner-membrane mitochondrial ISR donor rather than a direct HSPD1 phenocopy. I therefore placed Hspd1 modestly above the small chaperone donors but below a full Opa1-like state.

Point forecast: 14.
