# DEG-count prediction trace

## Question and resolved ambiguities

The requested held-out target set contains one perturbation, `Eif4e`. I interpreted the task as a scalar prediction of the number of genes that would satisfy `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` cells if the held-out `Eif4e` perturbation were present in the supplied differential-expression table. The endpoint is direct for non-held-out training perturbations in `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` and absent for `Eif4e`; the held-out `Eif4e` DE rows themselves were not used. The count includes the perturbed gene if that measured transcript passes FDR, as illustrated by `Eif4a2`, `Eif4g1`, and `Cyfip2`, whose focal counts include their self transcript.

## Sources

- Declared training DEG-count table: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet: `training differential-expression dataset`.
- Requested-target manifest: `single-target request for Eif4e`.
- Run-local task bindings, coverage, capability manifest, dataset portrait, and measurement registry.
- Internal same-experiment semantic corpus: `perturbai-july-260713-sourceguard-1773-v1`. Its calibration was checked, and a story-count query for the relevant training analogs (`Eif4a2`, `Eif4g1`, `Eif4h`, `Eef2`, `Mtor`, `Tsc2`, `Fmr1`, `Cyfip1`, `Cyfip2`) returned no Claim/Finding records, so it did not move the prediction.
- PubMed literature for external mechanism:
  - Pestova et al. 2001, PNAS, DOI `10.1073/pnas.111145798`, PMID `11416183`: cap-dependent translation initiation uses eIF4F, containing cap-binding eIF4E with eIF4A and eIF4G.
  - Merrick 2015, JBC, DOI `10.1074/jbc.R115.675280`, PMID `26324716`: retrospective review of eIF4F biochemistry and 4E-BP control of eIF4E/eIF4F assembly.
  - Yang et al. 2022, Biomolecules, DOI `10.3390/biom12060802`, PMID `35740927`: mTOR-mediated translational regulation converges on 4E-BP and S6K branches.
  - Chao and Avruch 2019, F1000Research, DOI `10.12688/f1000research.16109.1`, PMID `30647914`: Rheb activates mTORC1, which phosphorylates 4E-BP and S6K substrates.
  - Napoli et al. 2008, Cell, DOI `10.1016/j.cell.2008.07.031`, PMID `18805096`: CYFIP1, together with FMRP, binds eIF4E and represses neuronal translation initiation in an activity-regulated synaptic complex.
  - Li et al. 2021, Development, DOI `10.1242/dev.190793`, PMID `34013332`: complete `Eif4e` loss in mouse embryos blocks development, supporting essential cap-dependent translation activity while coming from a non-neuronal developmental setting.

## Dataset calculations

The requested-target CSV had one exact row, `Eif4e`. The focal training table contained 1,674 unique non-held-out biological targets. It was strongly zero-inflated: 1,205 perturbations had `n_degs = 0`, the median was 0, the 75th percentile was 1, the 90th percentile was 2, and only the 95th percentile reached 18 DEGs.

I filtered the parquet to:

```python
(group_name == "151 TH Prkcd Grin2c Glut") &
    gene_target.isin(analog_targets)
```

and counted `pvals_adj < 0.05` in the retained rows to verify the training endpoint and inspect which genes drove each count. The focal row-group pruning limited the calculation to the focal cell group and yielded 17,259 measured genes for each analog. Genome-wide Spearman correlations of the signed Wilcoxon `scores` among `Eif4a2`, `Eif4g1`, `Eif4h`, `Mtor`, `Fmr1`, `Cyfip1`, and `Cyfip2` were all close to zero; for example, `Eif4a2` versus `Eif4g1` was 0.021 and `Eif4a2` versus `Eif4h` was 0.057. Thus these cap-translation perturbations did not share a broad, reproducible focal expression pattern in the training data.

## Target-specific reasoning

### Eif4e

`Eif4e` encodes the cap-binding subunit of eIF4F, with `Eif4g1` acting as the large scaffold and `Eif4a2` as an RNA helicase subunit or paralog within the eIF4F initiation machinery. That made the assayed `Eif4a2` and `Eif4g1` perturbations the closest in-dataset structural analogs. In the focal training endpoint they were both very small effects:

| training perturbation | focal `n_degs` | focal FDR-significant rows | relevance to `Eif4e` |
| --- | ---: | --- | --- |
| `Eif4a2` | 2 | `Eif4a2` log2FC -0.629, q `1.23e-07`; `Cadm4` log2FC -0.392, q `0.0122` | eIF4F helicase component; the significant signal was almost entirely the self transcript plus one other gene |
| `Eif4g1` | 1 | `Eif4g1` log2FC -0.764, q `0.00702` | eIF4F scaffold; only the self transcript passed FDR |
| `Eif4h` | 1 | `Hexim1` log2FC 0.744, q `0.0208` | eIF4A accessory factor; more peripheral than eIF4E/eIF4G/eIF4A |
| `Mtor` | 2 | `Rims3` log2FC 0.300, q `0.0185`; `Tmed8` log2FC -0.821, q `0.0265` | upstream mTORC1 kinase that regulates eIF4E availability through 4E-BP phosphorylation |
| `Rptor` | 0 | none below FDR 0.05 | mTORC1 scaffold; a counterexample to expecting broad DE from partial mTORC1 impairment |
| `Eef2` | 9 | 9 rows including `Ranbp2`, `Ufd1`, `Mul1`, and `Prkcsh` | translation elongation rather than cap initiation; useful only as an upper bound for another core translation perturbation |
| `Fmr1` | 0 | none below FDR 0.05 | neuronal post-transcriptional regulator; regulates subsets of translated mRNAs rather than replacing eIF4E |
| `Cyfip1` | 0 | none below FDR 0.05 | FMRP partner that can bind eIF4E as a translational repressor |
| `Cyfip2` | 1 | `Cyfip2` log2FC -0.489, q `4.39e-11` | paralogous FMRP/eIF4E-associated regulator; only self was significant |

The cap-initiation evidence favors a nonzero but very small prediction. External mechanism says a full `Eif4e` null is not interchangeable with mild mTOR inhibition or with loss of a CYFIP repressor: eIF4E is the direct 5-prime-cap binder and can be limiting for eIF4F assembly. However, the experiment is acute, sparse, postmitotic, and assayed only in recovered nuclei, with modest average transcript downregulation. In exactly that setting, the assayed core translation and mTORC1 components did not create a broad BH-significant transcriptional response. The most transferable empirical pattern is therefore `Eif4a2`/`Eif4g1`, where disrupting an eIF4F component produced one self-transcript row and at most one additional focal DEG.

`Tsc2` was the main mechanistic counterexample, with 86 focal DEGs. I did not transfer that count to `Eif4e` because the intervention has the opposite causal sign at the key node: `Tsc2` loss removes TSC inhibition of Rheb and can activate mTORC1, whereas `Eif4e` loss should limit cap recognition downstream of 4E-BP release. Broad PI3K-AKT inputs were also quiet in the focal table (`Akt3`, `Pik3cb`, `Pik3r1`, and `Pik3r2` all had 0 DEGs), which argues against inflating `Eif4e` merely because it sits under a famous growth pathway.

My point prediction is `1`: I expect either the `Eif4e` transcript itself or one immediate stress/translation-response gene to cross FDR 0.05, but I do not expect a multi-dozen-gene response.

## Limits and uncertainty

The held-out endpoint itself is absent, and none of the exact `Eif4e` paralog targets were available in the focal training table. The strongest within-dataset analogs perturb neighboring eIF4F or mTOR proteins, not the eIF4E cap-binding subunit itself. The literature showing `Eif4e` essentiality is from early embryos or biochemical systems and overstates what should be visible after partial mosaic loss in postnatal recovered thalamic neurons. Conversely, a severe `Eif4e` effect that depleted edited neurons before snRNA-seq would be attenuated or even hidden in this survivor-conditioned DE endpoint. For those reasons, the exact integer is uncertain, but the training evidence makes a 0-2 DEG prediction much more defensible than a broad `Tsc2`-like count.
