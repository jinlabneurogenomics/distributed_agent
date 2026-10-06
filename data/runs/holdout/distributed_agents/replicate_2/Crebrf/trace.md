# Question

The held-out target list for this run contains one perturbation, `Crebrf`. I
interpreted the requested endpoint as the integer number of measured genes with
`pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` after acute P16 mosaic AAV
CRISPR loss of the target. The target itself was absent from both the
training-count CSV and from `training_de_all_cell_groups.parquet`, so I used
training perturbations of related ER-stress, chaperone, and CREB-pathway genes
to predict the held-out count.

I did not treat the string `CREB` as sufficient biology: `Crebrf` encodes
Luman/CREB3 recruitment factor rather than cAMP-response factor `Creb1`, so the
ER-bound CREB3/UPR axis was more relevant than the nuclear CREB1/CBP axis.

# Sources

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: exact `n_degs` at FDR
  0.05 for 1,674 non-held-out perturbations in the focal cell group.
- `training_de_all_cell_groups.parquet`: focal-cell log fold changes and
  adjusted p values used to inspect the actual ER-stress genes affected by
  analog perturbations.
- Requested-target manifest `047_Crebrf.csv`: confirmed that the only target was
  `Crebrf`.
- Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`: no `Crebrf` Findings, Claims, or
  same-experiment references were present; I used the curated `Atf6`, `Hspa5`,
  `Sec63`, `Manf`, and `Uba5` reports to interpret the represented UPR/ER
  proteostasis training perturbations.
- Distributed Agents runtime profile comparison artifact
  `crebrf_er_creb_profile_compare.json`: compared a hand-selected ER/CREB
  candidate set in the focal cell group using all measured log fold-change
  coordinates and FDR 0.05 activity.
- PubMed literature for external mechanism:
  - Audas et al. 2008, DOI `10.1128/MCB.01439-07`, PMID `18391022`.
    Identified LRF/CREBRF as a UPR-responsive CREB3-interacting protein that
    promotes Luman/CREB3 degradation and represses CREB3 transactivation; LRF
    loss in MEFs elevated `CHOP`, `EDEM`, and `Herp`.
  - Martyn et al. 2012, DOI `10.1128/MCB.01142-12`, PMID `23071095`. Showed
    that mouse Crebrf/LRF also represses glucocorticoid receptor activity and
    affects prolactin-mediated maternal behavior in a whole-animal knockout.
  - Frahm et al. 2020, DOI `10.1210/endocr/bqaa163`, PMID `32901804`. Found
    reduced anxiety-like behavior and altered corticosterone rhythms in adult
    global Crebrf-knockout mice.
  - Xue et al. 2016, DOI `10.3892/ijo.2016.3576`, PMID `27278737`. Placed
    CREBRF as a negative regulator of hypoxia-induced autophagy through a
    CREB3/ATG5 axis in glioblastoma cells.

# Computation over the training data

I first read the focal training count CSV and summarized the endpoint:

- 1,674 training perturbations were present.
- Median `n_degs` was 0; the 75th percentile was 1, the 90th percentile was 2,
  the 95th percentile was 18, and the distribution had a very long high tail
  with maximum 2,677.

I then pulled the exact FDR 0.05 genes for ER/CREB-adjacent perturbations from
the parquet with a predicate on the focal cell group, the selected
`gene_target`s, and `pvals_adj < 0.05`:

```python
dataset.to_table(
    columns=["names", "gene_target", "logfoldchanges", "pvals_adj", "scores"],
    filter=(
        (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
        & ds.field("gene_target").isin(targets)
        & (ds.field("pvals_adj") < 0.05)
    ),
)
```

The main local analogs had these exact focal-cell DEG counts:

| training target | n_degs | focal-cell evidence at FDR 0.05 |
|---|---:|---|
| `Atf6` | 0 | No corrected genes. The inspected ER marker logFCs were all small, for example `Atf6` -0.116, `Hspa5` -0.179, `Herpud1` 0.268, `Ddit3` 0.014. |
| `Hspa5` | 5 | Up-regulated `Hsp90b1`, `Nfe2l1`, `Pdia4`, and `Derl3`, with `Erc1` down. This is a direct BiP/ER folding perturbation but only a 5-gene footprint at the requested FDR. |
| `Sec63` | 11 | Up-regulated `Hspa5`, `Canx`, `Hyou1`, `Chac1`, `Thy1`, `App`, `Syt4`; down-regulated `Syne1`, `Nlgn2`, `Plekhg1`. This was the broadest close ER-client-handling analog. |
| `Manf` | 3 | Up-regulated `Hspa5` and `Pdia6`; `Manf` itself was down. This supports a very small adaptive ER-chaperone module. |
| `Creb1` | 10 | A weak cAMP/CREM/CBP counterexample, not a CREB3-family analog. |
| `Crebbp` | 8 | Another weak CREB-name counterexample; mechanistically nuclear CBP rather than Luman/CREB3. |
| `Hspa8` | 9 | Cytosolic Hsp70 paralog with a small heat-shock/chaperone signal, not an ER BiP perturbation. |
| `Hsp90ab1` | 1 | Only the self transcript passed FDR. |
| `Dnajc13`, `Dnajc5` | 1 each | Only the self transcript passed FDR for each. |
| `Dnajb4`, `Dnajb6`, `Dnajc19`, `Eif2ak4`, `Sar1b`, `Tango2` | 0 each | Chaperone, GCN2, and secretion-adjacent losses that did not pass FDR in this group. |

The measured UPR genes showed that focal thalamic neurons can produce a large
stress response when the primary lesion is severe. `Gfpt1`, `Atp2a2`, `Dhdds`,
`Elp1`, `Uba5`, and `Ufc1` had 311, 187, 116, 645, 2,677, and 572 DEGs,
respectively, and induced recurrent `Chac1`, `Ddit3`, `Herpud1`, `Hspa5`,
`Hyou1`, `Pdia4`, or `Pdia6` genes. The Distributed Agents reports likewise describe
`Uba5`/`Ufc1` as a broad UFMylation/ISR state and `Gfpt1`, `Dhdds`, `Atp2a2`,
`Hspa5`, and `Sec63` as converging on an ER quality-control stress state in
vulnerable neurons. These are useful positive controls, but they damage
N-glycan precursor supply, ER calcium loading, dolichol supply, UFMylation, or
ER-client translocation directly, whereas CREBRF is a regulatory brake on
CREB3/Luman.

I also asked whether `Crebrf` or the CREB3/UPR readouts themselves are common
members of focal-cell signatures. In the 1,674 training perturbations, measured
`Crebrf` was FDR-significant only after `Tpr`, `Tnpo3`, and `Uba5` perturbation;
measured `Creb3` was never significant. Broad ER markers were recurrent after
large ER-proteostasis perturbations, but not after `Atf6` or most single
chaperone cofactors.

# Target-specific reasoning

## `Crebrf`

CREBRF/LRF is a UPR-responsive, unstable Luman/CREB3-interacting factor. The
best biochemical prior is that losing CREBRF releases CREB3 activity rather than
removing a core folding enzyme: Audas et al. found that LRF promotes Luman
turnover and sequesters nuclear Luman in GRIP1-containing bodies, and that
`Chop`, `Edem`, and `Herp` rose in LRF-null MEFs. This argues for possible UPR
derepression, so I did not simply call it an unrelated null.

The local data moved the estimate sharply downward:

- The closest represented transcription-factor branch, `Atf6`, had exactly 0
  DEGs in `151 TH Prkcd Grin2c Glut`. The Distributed Agents `Atf6` report notes that
  the null was broad across recovered neuronal groups and that matched `Hspa5`
  perturbation proved ER-stress transcripts were detectable in this same assay.
- Direct ER-stress detector perturbations were small at the exact requested
  threshold: `Manf` 3, `Hspa5` 5, and `Sec63` 11 DEGs. They were the appropriate
  positive analogs because each up-regulated an ER chaperone/ERAD-like module
  in the same focal group, including `Hspa5`, `Pdia6`, `Hsp90b1`, `Pdia4`,
  `Derl3`, `Canx`, or `Chac1`.
- The Distributed Agents `Hspa5`, `Sec63`, and `Manf` reports all caution that the UPR
  module is recoverable but not generic: `Atf6`, `Edem3`, cytosolic `Hspa8`,
  `Sil1`, and several ER-associated genes do not recreate the `Hspa5`/`Sec63`
  response.
- Severe ER-load perturbations such as `Gfpt1`, `Atp2a2`, `Dhdds`, `Uba5`, and
  `Ufc1` formed a large-response counterexample set. CREBRF is upstream and
  regulatory; loss of it is not expected to create the same primary folding,
  calcium, N-glycosylation, or UFMylation bottleneck.
- The cAMP/CREB-name neighbors `Creb1` and `Crebbp` were weak, 10 and 8 DEGs,
  and do not share the Luman/CREB3 mechanism.
- Whole-animal Crebrf knockout phenotypes involving glucocorticoid signaling
  and anxiety-like behavior are real, but Martyn et al. and Frahm et al. used
  global/developmental endocrine contexts. They are imperfect for predicting a
  3 to 4 week sparse, postmitotic, cell-autonomous snRNA signature.

I therefore predict that acute `Crebrf` loss will not cross FDR 0.05 in this
focal neuronal group. The point estimate is `0`: a tiny 1 to 3 gene response
would be biologically plausible, especially if CREB3 derepression raises a
single ERAD transcript, but the focal training distribution is mostly zeros and
the direct `Atf6` branch is completely flat under basal unstressed conditions.

# Limits

`Crebrf` itself had no Distributed Agents same-experiment report, and no `Crebrf`,
`Creb3`, or `Creb3l*` perturbation was present in the training-count table, so
the prediction extrapolates from indirect UPR and CREB comparators. The PubMed
evidence for the direct LRF-CREB3 mechanism is from MEFs and tumor cells, and
the strongest mouse phenotypes come from global knockouts rather than P16
mosaic neuronal loss. The snRNA readout also misses Xbp1 splicing, ATF6
cleavage, eIF2alpha phosphorylation, DNA indels, edited-cell abundance, and
short-lived stress responses. The zero call should therefore be read as "no
durable focal-cell mRNAs expected to pass BH FDR 0.05", not as evidence that
CREBRF has no protein-level, endocrine, developmental, or stress-challenge
function.

# Final prediction

`Crebrf`: `0` DEGs.
