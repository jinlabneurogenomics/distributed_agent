# Direct DEG-count forecast for `Lmbr1`

## Target and endpoint

The one-row declared holdout manifest names `Lmbr1`. The requested endpoint is
`n_degs` in `151 TH Prkcd Grin2c Glut`: the count of measured genes with
Wilcoxon BH-adjusted `p < 0.05` in that thalamic glutamatergic class.

## Evidence used

1. **Canonical target biology-only bundle**:
   `[local file: Lmbr1.json]`
   with bundle SHA256 `ed2a84887e7e47ebbcab00309c90603cb864a26609abcacadbc110f1cb62e8b4`.
   The bundle reports that `Lmbr1` is detectably expressed in the focal
   non-target nuclei, with 8,203 of 23,679 nuclei expressing it
   (`34.6425%`), `mean_cp10k = 0.27536`, `mean_log1p_cp10k = 0.19502`,
   and `pseudobulk_cpm = 28.7628`. This makes focal-population engagement
   biologically possible.

2. **Functional-stock and biological-prior evidence from the same bundle**.
   LMBR1 is a poorly resolved LMBR1-like multipass membrane protein at a
   locus containing the distinct intronic ZRS enhancer for `Shh`; the
   available mouse functional evidence is embryonic limb/locus biology, not a
   postnatal thalamic neuronal requirement. The bundle adjudicates
   functional stock by P37-P44 as `indeterminate`, with no transferable
   P16-to-P37/P44 stock-loss clock, unresolved renewal demand, and only a
   related-family `Lmbr1l` paralog without a matched-context compensation
   test.

3. **Same-experiment corpus check**. The selected July corpus returned no
   `Lmbr1` target Findings, Claims, or explicit same-experiment references
   (`target_found = false`). I therefore did not have a packaged target
   report or same-corpus analog story to weight.

4. **Training count table for the matched cell class**:
   `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
   `Lmbr1` is absent from the 1,674 training targets. The distribution is
   dominated by null/near-null outcomes: 1,205/1,674 targets have 0 DEGs,
   1,481/1,674 have at most 1 DEG, 1,527/1,674 have at most 3 DEGs, and
   the median is 0. Large signatures exist but are a small high-effect tail
   driven by visibly central factors such as `Uba5`, `Tpr`, `Sin3a`,
   `Rnpc3`, proteasome/spliceosome/RNA-processing genes, and broad
   transcriptional regulators.

5. **Training-table and Parquet checks for the only available perturbations
   touching the target bundle's Shh/Hedgehog-side biology**. The closest
   available pathway-side perturbations had no significant focal-class DEGs in
   the matched count table; `Ptch1`, `Smo`, `Gli1`, and `Gli2` were then
   checked directly in
   `[local file: training_de_all_cell_groups.parquet]`
   and had no adjusted `p < 0.05` rows:

   | training perturbation | focal `n_degs` | focal adjusted p-value floor |
   | --- | ---: | ---: |
   | `Ptch1` | 0 | 1.0 |
   | `Ptch2` | 0 | not rescanned in Parquet |
   | `Smo` | 0 | 1.0 |
   | `Gli1` | 0 | 1.0 |
   | `Gli2` | 0 | 1.0 |
   | `Ift88` | 0 | not rescanned in Parquet |
   | `Gpr161` | 0 | not rescanned in Parquet |
   | `Cdon` | 0 | not rescanned in Parquet |

   `Lmbr1l`, `Shh`, `Gli3`, and several more direct embryonic-limb-locus
   comparators were absent from the training count table, so they could not
   provide measured focal-class counts.

## Synthesis

The focal expression measurement argues against treating `Lmbr1` as
unreachable in `151 TH Prkcd Grin2c Glut`, but the measured transcript level is
low-to-moderate and the biology bundle supplies no matched postnatal neuronal
loss mechanism, no clear rapid protein-stock turnover, and no direct measured
protein-family comparator. Its better-established biology is embryonic
limb/ZRS/`Shh` locus regulation, a context that is explicitly mismatched to the
P16-P37/P44 thalamic neuron assay.

Given that weakly interpretable training targets overwhelmingly produce 0 or 1
DEG in this exact class, and that every training-available Hedgehog-side target
I checked from the count table also had 0 focal DEGs, I placed `Lmbr1` in the
null/near-null part of the training distribution rather than in the rare
large-response tail. I used 0 rather than 1 because there was no
training-available direct LMBR1-like perturbation, no corpus Finding tying
`Lmbr1` to a same-experiment response program, and no adjusted-p evidence below
0.05 in the inspected pathway-side Parquet profiles.

**Predicted `n_degs`: 0**
