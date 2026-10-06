# Ahdc1 DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolution of ambiguities

The held-out target manifest contains one perturbation, `Ahdc1`. I interpreted the requested endpoint as the integer number of measured genes that would have `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` differential-expression table if the acute AAV-CRISPR `Ahdc1` perturbation had not been withheld. The target's own mRNA, if significant, would count exactly like any other measured gene; no self-target exclusion was requested. I did not treat target-transcript knockdown as a quantitative editing-efficiency measure because the experiment is sparse, mosaic, postmitotic CRISPR and the supplied dataset context warns that self-mRNA loss is only weak QC context.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`: the authoritative training `n_degs` values for 1,674 non-held-out targets in the focal group.
- `[local file: training_de_all_cell_groups.parquet]`: focal-cell differential-expression rows for mechanistically selected training perturbations.
- `[local file: 007_Ahdc1.csv]`: the requested target list; it contains only `Ahdc1`.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`: `Ahdc1` had no anchored Claims, Findings, explicit related targets, or ledger rows in this filtered corpus, so the corpus was a checked negative source rather than a source of positive same-experiment Ahdc1 biology.
- PubMed-indexed literature for external biological priors:
  - Jiang et al. 2018, `10.1002/ajmg.a.38699`, PMID `29696776`: Xia-Gibbs syndrome is caused by de novo truncating variants in `AHDC1`; patients show developmental delay, intellectual disability, hypotonia, speech delay, and variably seizures/scoliosis.
  - Khayat et al. 2021, `10.1002/humu.24190`, PMID `33644933`: AHDC1 truncating alleles perturb nuclear localization of expressed protein fragments and produce a heterogeneous neurodevelopmental syndrome.
  - Khayat et al. 2021, `10.1016/j.xhgg.2021.100049`, PMID `34950897`: missense alleles clustered in conserved AHDC1 regions can also be diagnostic of Xia-Gibbs syndrome.
  - Collier et al. 2022, `10.1038/s41586-022-04727-9`, PMID `35585237`: Gibbin/AHDC1 is enhancer- and promoter-bound in a human pluripotent-stem-cell skin organoid model, interacts with zinc-finger transcription factors and methyl-CpG-binding proteins, and its loss increases DNA methylation at GATA3-dependent mesodermal genes.
  - Chander et al. 2022, `10.1002/humu.24461`, PMID `36054313`: contiguous deletions involving `AHDC1` show nontrivial expression compensation/regulatory behavior, reinforcing that AHDC1 dosage biology is not a simple one-readout proxy.
  - Li et al. 2023, `10.1152/ajpendo.00048.2023`, PMID `37819197`: survivable `Ahdc1`-deficient mice have post-weaning adiposity and metabolic phenotypes, supporting organismal relevance outside the nervous system.

## Computational checks on the training data

I first read the focal endpoint CSV and the held-out manifest and confirmed that `Ahdc1` is absent from the 1,674-row training count table. The focal training distribution is very sparse: 1,205/1,674 perturbations have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 95th percentile is 18, and only 43 training perturbations have at least 100 DEGs.

I then used parquet row-group statistics to restrict scans to `151 TH Prkcd Grin2c Glut`; the focal group spans row groups 546-580 and has 17,259 measured rows per selected perturbation. For a hand-curated comparator list I loaded:

```python
filter = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut") &
    pc.field("gene_target").isin(selected_comparators)
)
```

for `names`, `gene_target`, `logfoldchanges`, `pvals`, `pvals_adj`, and `scores`. I used those rows to verify the CSV counts, inspect the most significant focal genes for each comparator, and test DEG-set overlap among nonzero comparators.

The key focal training counts were:

| comparator class | training perturbation | focal `n_degs` | interpretation for `Ahdc1` |
| --- | ---: | ---: | --- |
| methyl-CpG / Collier-Gibbin neighborhood | `Mbd2` | 0 | close to the reported AHDC1 partner class, but transcriptionally silent in this readout |
| methyl-CpG / NDD | `Mbd5` | 0 | strong neurodevelopmental prior, no focal response |
| methyl-CpG / NDD | `Mecp2` | 16 | a real but small methyl-CpG response |
| GATA3-dependent Collier axis | `Gata3` | 0 | reported downstream developmental axis, silent here |
| NuRD-adjacent | `Gatad2b` | 1 | only the target transcript itself passed FDR |
| DNA/histone modification or coactivation | `Dnmt3a`, `Ep300`, `Hdac5`, `Hdac8`, `Crebbp` | 0, 0, 0, 0, 8 | mostly null; `Crebbp` weak |
| chromatin-remodeling NDD positives | `Chd4`, `Chd8`, `Chd2`, `Kmt2a` | 100, 61, 34, 24 | proves the assay can see chromatin KOs, but these are more direct remodelers/lysine methyltransferases |
| SWI/SNF | `Smarcc2`, `Smarce1`, `Arid1b`, `Smarca4` | 185, 11, 1, 0 | subunits vary widely; not an AHDC1 complex |
| broad chromatin/transcriptional counterexamples | `Setd1a`, `Zmynd8`, `Phf12`, `Sin3a`, `Zbtb7a` | 368, 74, 403, 1433, 841 | large focal signatures, but mechanistically too broad to use as direct AHDC1 surrogates |
| zero NDD/chromatin counterexamples | `Kat6a`, `Kat6b`, `Tcf4`, `Zfp462`, `Zmynd11`, `Bcl11a`, `Bcl11b`, `Mbd5` | all 0 | developmental/NDD status alone often fails to produce a focal DEG burden |

The nearest Collier-mechanism set was almost entirely silent: among `Mbd2`, `Mbd5`, `Mecp2`, `Gata3`, `Gatad2b`, `Dnmt3a`, `Ep300`, `Hdac5`, and `Hdac8`, 7 of 9 had zero DEGs, `Gatad2b` had one self-transcript DEG, and `Mecp2` had 16. In the broader 26-gene neurodevelopmental chromatin set I checked, 13 were exactly zero and the median was only 0.5, despite strong nonzero examples such as `Setd1a` and `Smarcc2`.

I also scanned `Ahdc1` as a measured downstream gene across all focal training perturbations. Only `Zbtb7a` and `Tpr`, both very broad high-burden perturbations, significantly changed `Ahdc1` RNA itself in the focal group. This gave no specific Ahdc1 pathway anchor.

Expression-pattern evidence sharpened which nonzero chromatin signatures should be discounted. `Smarcc2` and `Smarce1` shared 9 of `Smarce1`'s 11 DEGs, including a `Ptpn3`/`Reep2`/`Prkcd` SWI/SNF-like pattern, but other SWI/SNF subunits were null or self-only. `Chd4` had 100 DEGs and weak overlap with `Smarcc2` and `Zmynd8`, whereas the closer methyl-CpG/NuRD-adjacent `Mbd2` and `Gatad2b` perturbations were 0 and 1. The large `Sin3a`, `Zbtb7a`, `Phf12`, and `Setd1a` signatures showed that the cell class has statistical power for some nuclear regulators, but they do not recapitulate the AHDC1/Gibbin enhancer methylation mechanism.

## Ahdc1-specific reasoning

`Ahdc1` encodes the AT-hook protein AHDC1/Gibbin. Human genetics makes it a real neurodevelopmental dosage gene: de novo truncating and selected missense alleles cause Xia-Gibbs syndrome with delayed motor and speech development, intellectual disability, hypotonia, and variable seizures or brain-structure phenotypes. That prior argued against treating `Ahdc1` as an inert target.

The decisive evidence for this assay, however, is that AHDC1's best published molecular neighborhood did not map to an active focal training neighborhood. Collier et al. placed Gibbin at enhancers/promoters with zinc-finger and methyl-CpG-binding proteins and tied loss to methylation of GATA3-dependent mesodermal genes. In the focal postnatal thalamic neurons, `Mbd2`, `Mbd5`, `Gata3`, `Dnmt3a`, `Ep300`, `Hdac5`, and `Hdac8` were all exactly zero, while `Gatad2b` barely registered with only its own transcript. `Mecp2` was the only close methyl-CpG comparator with a downstream effect, and at 16 DEGs it was far below the broad chromatin cases.

I therefore viewed Ahdc1 as more likely to behave like the many developmental chromatin/NDD factors at the floor of the focal endpoint than like `Setd1a`, `Smarcc2`, `Sin3a`, or `Zbtb7a`. AHDC1 is not a core SWI/SNF subunit, a COMPASS-like catalytic subunit, or a ubiquitous transcriptional corepressor in the same sense as those strong training positives. Its clearest functional work is in embryonic/epithelial-mesodermal patterning and constitutive human disease, both imperfect matches to a 3-4 week partial CRISPR loss in surviving juvenile thalamic glutamatergic neurons.

Final zero/nonzero decision: predict no genes below BH FDR 0.05 for `Ahdc1`. I considered a very weak positive, around 1-5 DEGs, because the gene is a true nuclear disease gene and the focal endpoint can detect modest chromatin effects such as `Crebbp` = 8 and `Setd5` = 9. I chose 0 because the closest mechanism-driven comparators are null or self-only, and because the training endpoint is strongly zero-inflated.

## Limits

This prediction extrapolates from indirect biology. The selected Distributed Agents corpus had no Ahdc1-anchored Claims or Findings, and there is no Ahdc1 loss-of-function expression signature in the supplied training parquet. AHDC1 lacks a clean in-assay paralog, and the published Gibbin work is in human pluripotent-stem-cell-derived skin organoids and developmental chimeric mice rather than postnatal thalamic neurons. The true hidden response could therefore be a small nonzero count if AHDC1 regulates a neuron-specific enhancer program absent from the comparator set, or if a target-transcript/self row alone passes FDR.
