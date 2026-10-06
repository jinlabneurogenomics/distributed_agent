# Guk1 direct DEG-count forecast

## Task and endpoint

- Held-out manifest target: `Guk1`.
- Requested endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Declared same-cell training table: 1,674 non-`Guk1` perturbations.
- Training endpoint distribution in `151 TH Prkcd Grin2c Glut`: 1,205/1,674 were zero, the median was 0, the 75th percentile was 1, the 90th percentile was 2, and 469/1,674 were nonzero. The long upper tail was sparse, so the base rate favored a zero or one-gene call unless the biology pointed to one of the large recurrent stress or core-machinery states.

## Target biology

The declared biology-only `Guk1` bundle reported exact in-assay target reach in the focal population: `Guk1` RNA was available in `151 TH Prkcd Grin2c Glut`, with 13,809/23,679 non-target nuclei expressing the feature, 58.317% expression, mean raw UMI 1.0069, mean CP10K 0.6214, and pseudobulk CPM 63.11. This made target presence in the assayed thalamic population credible, but the bundle also explicitly states that baseline expression is not an editing-efficiency or endpoint observation.

The functional-stock card judged that a P16 disruptive edit should likely substantially deplete Guk1 enzymatic capacity by P37-P44 because Guk1 performs ongoing GMP/dGMP phosphorylation in cytosolic and mitochondrial nucleotide pools and no pre-edit permanent product stock protects the cell. The evidence was partial, however: the timing argument used a generic adult-brain proteome turnover proxy, not a Guk1-specific neuronal clearance measurement.

I treated the canonical loss evidence as enough to raise the forecast above an inert developmental/synaptic scaffold, but not enough to imply a large FDR signature. The source card identified systemic mouse preweaning lethality and human mitochondrial dNTP/mtDNA disease, not an acute postnatal thalamic-neuron phenotype; the observability card therefore left postnatal relevance, phenotype latency, and the best matched neuronal loss consequence unresolved. Survivor conditioning in the snRNA-seq design could also attenuate the recovered RNA signature from a metabolic defect.

## Training comparators

I used the packaged gene-analog nomination skill against the exact 1,674-gene training universe. It found no exact same-reaction paralog, no exact-complex/paralog candidate, and no reciprocal same-experiment corpus comparator for `Guk1`. The only narrow-module nominee was `Rac1` through Reactome azathioprine ADME, which is not a direct guanylate-kinase analogue, so I treated the meaningful candidate set as broad purine/nucleotide and mitochondrial-metabolism context rather than as scale-matched donors.

The most specific available nucleotide analogues were quiet in the focal endpoint:

| comparator set | focal `n_degs` |
| --- | ---: |
| `Nt5c2`, the only other training target annotated to both GMP and dGMP metabolism | 0 |
| `Fhit`, the other compact purine-nucleotide nominee | 0 |
| `Adk`, a purine/nucleotide Reactome member and `Nt5c2` corpus comparator | 0 |
| visible KEGG purine nominees `Adcy1`, `Adcy3`, `Adcy5`, `Gucy2c`, `Gucy2e`, `Npr2`, `Pde10a`, `Pde1c`, `Pde4b`, `Pde4d`, `Nt5c2`, `Fhit`, `Adk` | all 0 |

Direct Parquet checks for that same focal group confirmed that these visible purine/nucleotide genes had zero features at `pvals_adj < 0.05`; the smallest adjusted p-values among the directly checked purine members ranged from 0.1123 to 1.0, so this was not a count-table rounding artifact.

Same-experiment Findings supported the same interpretation. `Nt5c2` had only a one-gene L4/5 IT cortical response outside the focal thalamic class and did not induce the broad AMPK/mTOR/ISR/p53 or purine-enzyme RNA programs expected from an unbuffered nucleotide-pool imbalance. `Adk` produced no BH-significant downstream neuronal transcriptome in any of the 23 recovered cell groups, and its represented cAMP, phosphodiesterase, purine, and methylation-node perturbations failed to form a stable cell-autonomous RNA module. `Fhit` was also a pan-measured-neuronal transcriptional null.

As a secondary stress-test, nearby mitochondrial-metabolic genes that were present in the training table were also mostly silent in the same endpoint: `Afg3l2`, `Bckdk`, `Clpx`, `Coa8`, `Eif2ak4`, `Fars2`, `Lars2`, `Lonp1`, `Pcca`, `Rars2`, `Tpk1`, and `Yme1l1` all had 0 DEGs; `Atad1`, `Dap3`, `Got2`, `Hk1`, `Idh3a`, `Ndufb8`, `Ndufs2`, `Ndufs8`, and `Sucla2` had 1.

## Synthesis

The upward evidence is that `Guk1` is expressed in much of the focal population, has no clear same-reaction backup, and should lose soluble catalytic stock during the experiment. The downward evidence is stronger for this specific endpoint: the closest represented purine/nucleotide single-enzyme perturbations were zero in `151 TH Prkcd Grin2c Glut`, the corpus described purine neighbors as buffered rather than as a shared postnatal neuronal RNA-stress module, and many available mitochondrial/metabolic training targets were zero or singleton responders in the same cell class.

I therefore predict that Guk1 loss will be either fully buffered or below BH significance in the recovered thalamic nuclei, with a point forecast at the zero boundary:

`predicted_n_degs = 0`
