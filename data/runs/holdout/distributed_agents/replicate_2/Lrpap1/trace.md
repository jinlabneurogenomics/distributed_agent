## Question and resolved scope

The requested prediction is the integer number of genes with
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in
`151 TH Prkcd Grin2c Glut` nuclei after the held-out perturbation `Lrpap1`.
The count includes the target transcript when it is measured and significant;
it is an assay-specific snRNA-seq DEG burden, not a direct measure of protein
loss, cell survival, or biological importance.

This run has one requested target:

| target_name | in training-count CSV | parquet rows as `gene_target` |
|---|---:|---:|
| Lrpap1 | no | 0 |

Thus no `Lrpap1` perturbation profile or `Lrpap1` DEG count was used. I treated
the parquet as authoritative for expression-pattern evidence in training
perturbations, and used the focal count CSV as the exact observed endpoint for
those perturbations.

## Sources used

- `[local file: training_de_all_cell_groups.parquet]`: raw per-gene differential-expression rows for non-held-out perturbations.
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`: exact `151 TH Prkcd Grin2c Glut` `n_degs` for training perturbations.
- `[local file: 128_Lrpap1.csv]`: the requested target list.
- Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`: same Perturb-seq experiment, preinterpreted into Findings and Claims. I used it for LRP-family/Reelin/Sort1/Lrp1/Manf/Sec63 context, not as an independent replicate.
- PubMed literature searches for RAP/LRPAP1 biology, especially Bu and Schwartz-group papers defining RAP/LRPAP1 as an ER-resident folding chaperone for LDL receptor family members.

External biological references used for the mechanism:

- Bu, Geuze, Strous and Schwartz 1995, *EMBO Journal*, DOI `10.1002/j.1460-2075.1995.tb07221.x`, PMID `7774585`: the 39 kDa receptor-associated protein is an ER-resident molecular chaperone for LRP.
- Willnow et al. 1995, *PNAS*, DOI `10.1073/pnas.92.10.4537`, PMID `7538675`: RAP promotes functional LRP expression in vivo; RAP-deficient mouse liver and brain have reduced mature processed LRP.
- Bu and Rennke 1996, *Journal of Biological Chemistry*, DOI `10.1074/jbc.271.36.22218`, PMID `8703036`: RAP prevents LRP minireceptor aggregation and supports correct folding of LRP ligand-binding domains.
- Willnow et al. 1996, *EMBO Journal*, PMID `8654360`: RAP prevents premature ligand-induced ER retention/degradation of LDL receptor-related endocytic receptors.
- Obermoeller et al. 1997, *Journal of Biological Chemistry*, DOI `10.1074/jbc.272.16.10761`, PMID `9099728`: RAP has separable folding-chaperone and ligand-blocking functions.
- Birn et al. 2000, *Journal of the American Society of Nephrology*, DOI `10.1681/ASN.V112191`, PMID `10665926`: RAP is important for normal megalin/LRP2 processing in kidney proximal tubules.
- Jensen et al. 2009, *Biochemical Journal*, DOI `10.1042/BJ20090175`, PMID `19397492`: structural binding analysis of RAP domains and LRP complement repeats supports high-affinity RAP-LRP interactions.
- Xu et al. 2008, *PLOS ONE*, DOI `10.1371/journal.pone.0003159`, PMID `18776935`: partial RAP reduction in APP/PS1 mice modestly reduces RAP-dependent receptors such as LRP and SorLA/LR11 and increases amyloid deposition in an aged disease model.

## Computational steps

1. Read the manifest and confirmed it contained only `Lrpap1`.
2. Loaded the focal `n_degs` training CSV and summarized calibration. It has
   1,674 perturbations; 1,205 have `n_degs = 0`; the median is 0, the 75th
   percentile is 1, and the distribution has a long right tail. That makes the
   local baseline strongly zero-inflated.
3. Used parquet metadata to verify that `group_name` is row-group clustered,
   with `151 TH Prkcd Grin2c Glut` in row groups 546-580, and read only that
   focal row-group slice for a hand-selected comparator cohort.
4. Selected biologically motivated training targets before looking at their
   counts:
   - LDL receptor family and RAP-client/cargo-receptor comparators:
     `Lrp1`, `Lrp2`, `Lrp4`, `Lrp5`, `Lrp6`, `Lrp8`, `Vldlr`, `Sorl1`, `Sort1`.
   - Reelin-pathway nodes downstream or parallel to ApoER2/VLDLR:
     `Reln`, `Dab1`, `Fyn`.
   - ER and ER-associated perturbations that calibrate whether a specialized
     ER chaperone can induce an unfolded-protein or ERAD-like RNA response:
     `Sec63`, `Hspa5`, `Manf`, `Sil1`, `Amfr`, `Bcap31`.
   - Broader trafficking and lysosomal-delivery boundaries:
     `Cltc`, `Gnptab`.
5. For those 20 targets I computed `sum(pvals_adj < 0.05)` in the focal
   parquet, checked the recovered matched nucleus counts, and listed
   FDR-significant genes for the nonzero comparators.
6. Ran Distributed Agents Runtime `profile_compare` on the same 20 profiles within
   `group_name = "151 TH Prkcd Grin2c Glut"` using `logfoldchanges` as the
   signed value and `pvals_adj < 0.05` as significance. This confirmed that
   13/20 selected comparators had no significant focal features, 6 had only
   1-9 significant features, and only `Sec63` was in the 10-49 range. The
   profile inspection found no significant same-direction intersections between
   the LRP-family nulls and the weak ER-stress positives, except the known
   `Sec63`/`Manf` overlap on `Hspa5`.
7. Queried the Distributed Agents corpus for same-experiment Findings and Claims around
   `Lrp1`, `Lrp8`, `Vldlr`, `Sort1`, `Manf`, and `Sec63`. The corpus has no
   `Lrpap1` Claim, so the target-specific forecast is a transfer from related
   measured perturbations plus external RAP biology.

The only non-obvious parquet operation was the focal filtered slice:

```python
flt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(targets)
)
table = dataset.to_table(
    columns=[
        "names", "scores", "logfoldchanges", "pvals", "pvals_adj",
        "group_name", "gene_target", "n_pert_matched", "n_ctrl_matched",
    ],
    filter=flt,
)
```

## Comparator evidence

### LDLR-family and sorting-receptor branch

RAP/LRPAP1 is a specialized ER escort for LDL receptor-related proteins rather
than a global BiP-like chaperone. The direct implication of losing `Lrpap1` is
impaired maturation or ligand shielding of receptors such as LRP1/LRP2, and
possibly other LDLR-family clients, not a guaranteed generic UPR.

The exact focal training counts were:

| comparator | focal `n_degs` | expression-pattern evidence in 151 |
|---|---:|---|
| Lrp1 | 0 | no genes at FDR 0.05; corpus reports `Lrp1` has only a very restricted Vgf-up response in 155 MB Glut and 191 MB P MY GABA, and is not a Manf-like UPR perturbation |
| Lrp2 | 0 | no focal hits; `Lrp2` itself is effectively uninformative/very low in this class |
| Lrp4 | 0 | no focal hits |
| Lrp5 | 0 | no focal hits |
| Lrp6 | 4 | `Nrbp2`, `Nsmf`, `Atrnl1` down and `Chgb` up; small thalamic LDLR-family/Wnt-co-receptor signal but not a RAP/LRP1-LRP2/ER-chaperone state |
| Lrp8 | 0 | no focal hits; corpus places the only weak `Lrp8` event in 009 L2-3 IT PIR AON ENT Glut and states that ApoER2/LRP8, VLDLR, DAB1, RELN and FYN do not form a shared P16 Reelin RNA module |
| Vldlr | 0 | no focal hits; Distributed Agents Finding `Vldlr:F001` reports no downstream FDR 0.10 response in any recovered juvenile neuronal class |
| Sorl1 | 0 | no focal hits |
| Sort1 | 0 | no focal hits; even the self transcript had only `q = 0.0939` in 151; corpus reports Sort1 depletion in 151 without a downstream FDR 0.10 response |
| Reln | 0 | no focal hits |
| Dab1 | 0 | no focal hits |
| Fyn | 0 | no focal hits |

This is the closest same-assay evidence for `Lrpap1`. LRPAP1 clients and
biochemistry-adjacent LDLR/Reelin/Sortilin receptors are almost all focal
zeros. `Lrp6` is the only low nonzero exception and has a tiny, non-ER
signature; LRP5/6 are Wnt co-receptors and not the canonical LRPAP1-dependent
LRP1/LRP2 maturation branch. The corpus `Lrp1:F005` finding makes the same
boundary: represented LDLR-family relatives and sorting receptors did not
phenocopy `Lrp1` in the postnatal neuronal assay.

### ER-client and ER-stress branch

Because RAP is an ER-resident folding chaperone, I also compared perturbations
that do make ER load visible in this assay:

| comparator | focal `n_degs` | FDR 0.05 focal pattern |
|---|---:|---|
| Sec63 | 11 | `Hspa5`, `Rtn1`, `Canx`, `Hyou1`, `Chac1`, `Syt4`, `Thy1`, `App` and several structural/surface genes; clear but still small ER-client-translocation stress in 151 |
| Hspa5 | 5 | `Hsp90b1`, `Pdia4`, `Derl3`, `Nfe2l1`, and `Erc1`; direct BiP perturbation partly overlaps the Sec63 ER response |
| Manf | 3 | `Hspa5` and `Pdia6` induced plus `Manf` self down; an adaptive ER-chaperone response |
| Sil1 | 0 | no focal hits despite being a BiP nucleotide-exchange factor |
| Amfr | 1 | self transcript only |
| Bcap31 | 1 | self transcript only |
| Cltc | 3 | `Ero1b`, `Rbms1`, `Gabra4` down; a trafficking perturbation detectable but not LRP-family-like |
| Gnptab | 0 | no focal hits |

`Sec63`, `Hspa5`, and `Manf` prove that the 151 assay can detect a small ER
chaperone/protein-processing state. They are deliberately upper boundaries for
`Lrpap1`: SEC63 and BiP/HSPA5 are core translocation/folding machinery for a
large fraction of secretory clients, whereas LRPAP1 is a narrower escort for
LDLR-family endocytic receptors. `Amfr`, `Bcap31`, and `Sil1` are important
counterexamples showing that being ER-associated does not automatically create
a multi-gene ER-stress signature in this screen.

### Target-specific synthesis

External RAP literature says that LRPAP1/RAP is needed for efficient folding,
export, and functional maturation of LRP1 and LRP2/megalin. That made a
nonzero focal response plausible if loss of the escort simultaneously lowered
multiple receptor clients or created ER-retained aggregates. The within-dataset
evidence argues the opposite for this endpoint:

- Direct receptor targets closest to RAP biology are focal zeros:
  `Lrp1 = 0`, `Lrp2 = 0`, `Lrp8 = 0`, `Vldlr = 0`, `Sorl1 = 0`,
  `Sort1 = 0`.
- Reelin-core pathway perturbations around `Lrp8`/`Vldlr` are also focal
  zeros: `Reln = 0`, `Dab1 = 0`, `Fyn = 0`.
- The only LDLR-family focal signal, `Lrp6 = 4`, is a small Wnt-co-receptor
  style response and not a RAP/LRP1-LRP2 client-handling module.
- The ER-stress comparators show an upper scale of roughly 3-11 genes for
  broad ER-client stress in 151. LRPAP1 is narrower than `Sec63`, `Hspa5`, or
  `Manf`, so I did not transfer the `Sec63` count upward to `Lrpap1`.
- As a measured gene, `Lrpap1` was stable in the 151 training matrix: only
  3 of 1,674 other perturbations changed it at FDR 0.05. That does not
  determine whether `Lrpap1` targeting itself would depress the transcript, but
  it argues that `Lrpap1` is not a common downstream marker of the major strong
  transcriptional states.

I therefore predict that partial, mosaic P16 CRISPR loss of `Lrpap1` will not
push either LDLR-family receptor biology or a general UPR over the FDR 0.05
threshold in recovered 151 thalamic glutamatergic nuclei.

## Prediction

| target_name | predicted_n_degs |
|---|---:|
| Lrpap1 | 0 |

## Limits and uncertainty

The closest analogs are imperfect. No `Lrpap1` Claim was present in the
Distributed Agents corpus, and the parquet lacks the held-out target profile by design.
The receptor comparators test loss of single surface receptors, not combined
loss of LRPAP1-dependent maturation across several clients. Conversely, the ER
stress comparators perturb much broader machinery than RAP, so they are upper
boundaries rather than direct analogs.

The main residual uncertainty is a self-transcript-only call. The endpoint
includes the target RNA, and some focal training genes with no obvious
downstream program score as `n_degs = 1` through their own transcript, as in
`Amfr` and `Bcap31`. I assigned 0 rather than 1 because LDLR-family receptors
were almost uniformly flat, `Sort1` showed detectable but non-significant
self-depletion in 151, and the experiment's target RNA reduction is not a
reliable quantitative editing gauge. A one-gene answer would be a plausible
nearby alternative if `Lrpap1` happened to have stronger nonsense-mediated
decay than its pathway comparators.
