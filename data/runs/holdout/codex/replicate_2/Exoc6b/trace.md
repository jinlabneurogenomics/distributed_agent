# Exoc6b direct DEG-count forecast

## Target and endpoint

- Target: `Exoc6b`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`

The one-row holdout manifest and the biology bundle both identify `Exoc6b` as the held-out perturbation. `Exoc6b` is absent from the 1,674-row `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, so its focal-class differential-expression signature and count were not used.

## Evidence used

### Biology bundle

The declared `Exoc6b` biology bundle says that EXOC6B is a Sec15-family exocyst component participating in dynamic vesicle docking/tethering at the plasma membrane. The functional-stock card judged the pre-edit protein pool more likely substantially depleted than preserved by the P37-P44 harvest after P16 editing, but with sparse evidence: no EXOC6B-specific neuronal half-life or postnatal mouse-neuronal loss series was found.

The same bundle gives exact focal-population expression rather than a qualitative reach estimate. In non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Exoc6b` was detected in 19,493 of 23,679 cells, 82.3219%, with mean raw UMI 1.9927, mean CP10k 1.2759, and pseudobulk CPM 124.8918. That makes the target transcript available to the assay in this population, though it does not establish editing efficiency or downstream dependence.

The main downward caveats in the bundle were unmatched external phenotypes and buffering uncertainty: the available mouse phenotype is systemic germline preweaning lethality, not a postnatal neuronal conditional phenotype, and EXOC6 can buffer EXOC6B for constitutive cargo delivery in cultured human cells without a matched thalamic-neuron compensation test.

### Same-experiment corpus

The selected same-experiment corpus had no `Exoc6b` Findings, Claims, or explicit related-target records, so there was no packaged semantic result that directly described the held-out perturbation.

The packaged Findings for measured training comparators supported using membrane-trafficking genes as a mostly near-null local background rather than a large-response module:

- `Trappc6b`, `Trappc9`, and `Trappc10` were reported as buffered or one-hit perturbations and did not converge on a TRAPP/UPR/autophagy transcriptional program.
- `Cplx1`, `Vamp1`, `Unc13a`, and represented SNARE-adjacent genes were mostly buffered; the Stxbp1 report explicitly notes that canonical release-machinery perturbations largely failed to phenocopy Stxbp1.
- `Vps35` and `Vps54` were the only stronger vesicle-traffic examples in this local group, but their reports describe restricted 151-TH programs tied to retromer/GARP biology, receptor/excitability or mature-neuronal transcripts, and not a generic trafficking-collapse state.
- `Sec63` was a separate ER-chaperone/UPR response, not an exocyst analogue.

These reports are curated summaries of the same experiment, not independent replication of the Parquet counts below.

### Training counts and Parquet profiles

In the declared count table for `151 TH Prkcd Grin2c Glut`, the global training distribution was extremely sparse: 1,205/1,674 targets had 0 DEGs and 276/1,674 had exactly 1 DEG. The median was 0, the 75th percentile was 1, the 90th percentile was 2, and the mean was pulled up to 14.05 by a small high-count tail.

I then inspected a functionally local training cohort from the same count table and the expression Parquet:

`Ap1b1`, `Ap1s2`, `Ap3b1`, `Ap4s1`, `Bsn`, `Cplx1`, `Cplx2`, `Dnm1`, `Rab18`, `Rab27a`, `Rab3gap1`, `Rab3gap2`, `Sec23a`, `Sec63`, `Stx16`, `Stx1b`, `Stx5a`, `Stxbp1`, `Syn1`, `Syn2`, `Synj1`, `Syt14`, `Syt2`, `Trappc10`, `Trappc6b`, `Trappc9`, `Unc13a`, `Unc13b`, `Unc13c`, `Vamp1`, `Vps13a`, `Vps13b`, `Vps13c`, `Vps35`, `Vps35l`, `Vps41`, `Vps53`, `Vps54`.

For that 38-target cohort, the exact focal-class counts were:

- 27 targets with 0 DEGs.
- 8 targets with 1 DEG.
- 3 targets above 10 DEGs: `Sec63` 11, `Vps35` 17, `Vps54` 31.
- Median 0; mean 1.763.

The Parquet rows at `pvals_adj < 0.05` matched the count table exactly for this cohort. All eight 1-DEG cases in the cohort were target-transcript-only calls in this cell class: `Ap1b1`, `Cplx1`, `Dnm1`, `Stx16`, `Stxbp1`, `Syn1`, `Synj1`, and `Vamp1`.

The symmetric Parquet profile comparison over the same 38 nodes also found that 27/38 profiles had no significant features, 8/38 had 1-9 significant features, and 3/38 had 10-49. Top-tail overlap across the cohort was weak, consistent with isolated self-transcript or idiosyncratic effects rather than a coherent exocytic-trafficking DEG module.

## Synthesis

`Exoc6b` is expressed enough in the assayed thalamic population for its own transcript to be testable, and the stock card makes complete non-realization less likely than it would be for a stable pre-installed protein. Those considerations push the forecast above a hard zero.

The downstream signature expectation is still very small. The closest measured trafficking and synaptic-vesicle perturbations in the exact same cell class were dominated by zero or one DEG, and the one-DEG cases were self-transcript calls rather than shared downstream responses. The moderate local outliers, `Sec63`, `Vps35`, and `Vps54`, represent ER translocation/UPR, retromer, and GARP biology with curated same-experiment programs that are not close exocyst/Sec15 analogues. The unresolved EXOC6 buffering and absence of a matched postnatal neuronal phenotype also argue against inflating the point estimate into the `Vps35`/`Vps54` range.

I therefore forecast a near-null response carried, if anything, by a single significant measured gene, most plausibly the self transcript:

`predicted_n_degs = 1`
