# Question

Predict the held-out endpoint `n_degs` for the requested perturbation in
`151 TH Prkcd Grin2c Glut` nuclei. I treated `n_degs` exactly as the focal CSV
does: the count of measured genes with Benjamini-Hochberg-adjusted Wilcoxon
`pvals_adj < 0.05` in the focal cell group. The only requested held-out target
in `060_Dnm2.csv` is `Dnm2`, and the prediction below is a point estimate for
the same acute AAV CRISPR perturbation and snRNA-seq test, not a prediction of a
germline null phenotype.

# Sources Used

- Supplied endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Supplied differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest:
  `[local file: 060_Dnm2.csv]`.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`. I queried
  target-neighbor and story tables for `Dnm2`; this release contained no direct
  `Dnm2` claims, so it did not provide a same-corpus mechanistic comparator.
- PubMed literature:
  - Ferguson et al. 2007, *Science*, DOI `10.1126/science.1140621`, PMID
    `17463283`.
  - Raimondi et al. 2011, *Neuron*, DOI `10.1016/j.neuron.2011.04.031`, PMID
    `21689597`.
  - Milosevic et al. 2011, *Neuron*, DOI `10.1016/j.neuron.2011.08.029`, PMID
    `22099461`.
  - Bhave et al. 2020, *Molecular Biology of the Cell*, DOI
    `10.1091/mbc.E20-06-0363`, PMID `32579424`.
  - Bitoun et al. 2009, *Human Mutation*, DOI `10.1002/humu.21086`, PMID
    `19623537`.

# Computational Reasoning

I first verified that `Dnm2` is absent from both the training endpoint table and
the DE parquet, as expected for a held-out perturbation. The focal endpoint is
very sparse: among 1,674 non-held-out perturbations, 469 had any focal DEGs, the
median was 0, the 75th percentile was 1, the 95th percentile was 18, and the
large tail was enriched for chromatin, RNA-processing, proteasome, and other
broad cell-state regulators.

To avoid using irrelevant cell groups, I pruned the 616M-row parquet by Parquet
row-group metadata and then read only

```python
(group_name == "151 TH Prkcd Grin2c Glut")
& gene_target.isin(candidate_endocytosis_and_counterexample_targets)
```

The focal cell group occupied 28,562,358 DE rows. For 13 mechanistic candidates
I recomputed `sum(pvals_adj < 0.05)` from the parquet and matched those counts
to the focal CSV. I also used the Distributed Agents runtime `profile_compare` /
`profile_inspect` tools on the focal signatures to compare whole-profile
correlations and signed top-feature overlap among the observed candidates.

The endpoint counts of the relevant training perturbations were:

| training perturbation | focal n_degs | interpretation for Dnm2 |
|---|---:|---|
| `Dnm1` | 1 | closest paralog and synaptic-vesicle fission dynamin in neurons; only `Dnm1` itself passed FDR |
| `Synj1` | 1 | phosphoinositide phosphatase coupled to dynamin/endophilin during vesicle uncoating; only `Synj1` itself passed |
| `Bin1` | 1 | BAR/SH3 endocytic adaptor that can recruit dynamin; only `Bin1` itself passed |
| `Ap1b1` | 1 | adaptor-complex trafficking gene; only `Ap1b1` itself passed |
| `Ap1s2` | 0 | adaptor-complex trafficking gene with no detected focal response |
| `Cltc` | 3 | core clathrin heavy chain; weak nonzero focal response, with 3 secondary genes and no broad state shift |
| `Syp` | 1 | abundant synaptic-vesicle protein; only `Syp` itself passed |
| `Stxbp1` | 1 | synaptic vesicle release machinery; only `Stxbp1` itself passed |
| `Vps35` | 17 | retromer endosomal recycling; broader than clathrin-vesicle-scission comparators |
| `Vps54` | 31 | GARP/endosome-to-Golgi trafficking; broader than the direct dynamin module |
| `Rab7` | 501 | late endosome/lysosome perturbation with a qualitatively broad stress response |
| `Grin1` | 89 | glutamatergic receptor perturbation, included as a focal-cell positive-response counterexample |

Selected same-experiment details that anchored the calibration:

- `Dnm1`: 194 perturbed and 23,679 control nuclei, 1 significant gene.
  The only FDR hit was the target transcript itself
  (`Dnm1` log2FC -0.712, adjusted p `4.09e-25`).
- `Synj1`: 90 perturbed nuclei, 1 significant gene, again the target itself
  (`Synj1` log2FC -0.583, adjusted p `3.11e-07`).
- `Bin1`: 276 perturbed nuclei, 1 significant gene, the target itself
  (`Bin1` log2FC -0.331, adjusted p `3.0e-06`).
- `Cltc`: only 32 perturbed nuclei and 3 significant genes
  (`Gabra4`, `Rbms1`, `Ero1b`), consistent with a small detectable footprint but
  not a strong transcriptional program.
- `Vps35`, `Vps54`, and `Rab7` produced 17, 31, and 501 DEGs respectively.
  They show that intracellular trafficking genes can score above the low
  endocytic baseline, but those broader hits are late endosome/lysosome or
  retromer/GARP perturbations rather than the plasma-membrane or synaptic
  vesicle scission step closest to `Dnm2`.

The profile comparison was useful mostly as a boundary check. `Cltc` and
`Synj1` were close within this candidate set by whole-profile metrics
(`pearson = 0.660`, `cosine = 0.742`), and `Dnm1` also had moderate whole-vector
similarity to `Synj1`, `Bin1`, and AP-1/endosomal targets. However, the
significant-gene overlap among `Dnm1`, `Synj1`, `Bin1`, and `Cltc` was
essentially zero because each had only one to three hits. Thus I did not
average in the high `Rab7` count just because it had some whole-profile
similarity to `Dnm1`; `Rab7` is a stronger endolysosomal perturbation with
501 significant genes and is a counterexample, not the proper magnitude anchor.

# Target-Specific Prediction

## Dnm2

`Dnm2` encodes the ubiquitously expressed dynamin 2 large GTPase, which mediates
membrane fission during clathrin-mediated endocytosis and other membrane
trafficking steps. `Dnm1` and `Dnm3` are the brain-enriched dynamins. The mouse
neuronal data in Ferguson et al. 2007 show that loss of `Dnm1` strongly impairs
synaptic-vesicle endocytosis during intense activity, while Raimondi et al. 2011
show that `Dnm1` and `Dnm3` jointly account for the overwhelming majority of
brain dynamin and that very low `Dnm2` can still support some essential neuronal
functions in their absence. Bhave et al. 2020 further support that `Dnm1` and
`Dnm2` share the core clathrin-mediated endocytosis machinery but are
isoform-specialized, while Bitoun et al. 2009 connect pathogenic human `DNM2`
mutations to impaired clathrin-mediated receptor endocytosis. Milosevic et al.
2011 links the dynamin partner network to endophilin and synaptojanin during
synaptic vesicle uncoating, making `Synj1` an appropriate within-dataset
neighbor.

The best in-dataset analog is therefore `Dnm1`, not `Rab7`: it is the closest
dynamin paralog measured in the training data and in this exact cell group it
gave one DEG, the on-target decrease of `Dnm1`. `Synj1` and `Bin1` also gave one
DEG apiece, and AP-1/clathrin comparators ranged from zero to three. This
cluster says that partial acute perturbation of the vesicle-scission and
clathrin adaptor machinery is usually detected, if at all, as loss of the
target transcript rather than as a broad compensatory program.

I am predicting a nonzero count because `Dnm2` is a well-expressed core dynamin
and should have a reasonable chance of showing the same self-transcript FDR hit
seen for `Dnm1`, `Synj1`, and `Bin1`. I kept the magnitude at 1 because mature
neurons can buffer partial loss of one dynamin isoform, because the direct
within-dataset endocytic analogs were all at 0-3 DEGs, and because broader
endolysosomal stress programs such as `Rab7` do not match the molecular step of
`Dnm2`.

Predicted `n_degs`: 1.

# Limits

- There was no direct `Dnm2` expression signature in the supplied training data
  and no Dnm2-centered Distributed Agents corpus claim, so the prediction extrapolates
  from paralogs and pathway neighbors.
- `Dnm1` is the only dynamin paralog present in the focal training counts;
  `Dnm3`, `Amph`, endophilins, AP-2 subunits, `Itsn1/2`, and `Picalm` would have
  been more direct calibration points if measured.
- Several low-count analogs owe their single DEG to successful detection of the
  target transcript itself. If the held-out guide pool produced weaker `Dnm2`
  mRNA depletion than those analogs, the true value could be 0; if `Dnm2` is
  less buffered in these TH/Prkcd/Grin2c glutamatergic neurons than `Dnm1`, it
  could plausibly produce a handful of secondaries.
- Whole-profile correlations among near-null perturbations are dominated by
  weak, nonsignificant ranks and should not be over-interpreted. I used them to
  reject the broad `Rab7` state as an analog, not to estimate a precise count.
