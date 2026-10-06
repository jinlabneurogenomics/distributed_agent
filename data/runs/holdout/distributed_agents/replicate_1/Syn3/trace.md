# Prediction target

I interpreted the task as a scalar held-out prediction for `Syn3` in `151 TH Prkcd Grin2c Glut` cells. The requested endpoint is the exact focal-class count of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`; the count includes the perturbed transcript itself when that row crosses FDR. The held-out `Syn3` perturbation was absent from both supplied inputs, so its DEG count was not directly observed in the model-visible data.

I treated the focal training-count CSV as direct endpoint evidence for non-held-out perturbations, and the all-cell differential-expression Parquet as direct same-experiment expression evidence for those visible perturbations. The selected internal same-experiment interpretation layer was `perturbai-july-260713-sourceguard-1773-v1`; I used it only for bounded reports and evidence records around visible training analogs (`Syn1`, `Syn2`, `Syp`, `Sv2a`). It is a packaged view of the same Perturb-seq experiment, not an independent replicate. I used NCBI PubMed and NCBI Bookshelf for external mechanism priors on synapsins and presynaptic-vesicle genes.

# Dataset calibration

The focal `151 TH Prkcd Grin2c Glut` count table contains 1,674 visible training perturbations. It is heavily zero-inflated: 1,205/1,674 have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the maximum is 2,677. Thus a prediction above one DEG needs a candidate-specific reason that the held-out target should create a broader recovered-nucleus RNA state than its closest visible analogs.

I first selected training targets with direct synapsin, synaptic-vesicle, SNARE/priming, and postsynaptic roles and read their focal `n_degs` values from the CSV:

| training target | focal `n_degs` | relevance to `Syn3` |
|---|---:|---|
| `Syn1` | 1 | closest visible paralog; synaptic-vesicle phosphoprotein/reserve-pool regulator |
| `Syn2` | 0 | closest visible paralog; reserve-pool regulator |
| `Syp` | 1 | abundant synaptic-vesicle membrane protein; mostly protein-trafficking phenotype |
| `Sv2a` | 1 | broad synaptic-vesicle release protein |
| `Vamp1` | 1 | vesicular SNARE homolog visible in the focal class |
| `Cplx1` | 1 | presynaptic fusion clamp/facilitator |
| `Cplx2` | 0 | presynaptic fusion clamp/facilitator |
| `Stxbp1` | 1 | MUNC18-1, a more central SNARE-fusion factor and a positive counterexample in other cells |
| `Unc13a` / `Unc13b` / `Unc13c` | 0 / 0 / 0 | MUNC13 vesicle-priming family |
| `Stx1b` | 0 | plasma-membrane SNARE |
| `Bsn`, `Pclo` | 0 / 0 | presynaptic active-zone scaffolds |

I then queried the declared Parquet, filtered to the focal cell class, visible analog targets, and `pvals_adj < 0.10`. In the focal class the only FDR<0.05 hits for `Syn1`, `Syp`, `Sv2a`, `Vamp1`, `Cplx1`, `Stxbp1`, and `Dlg4` were the corresponding self transcripts; `Syn2`, `Cplx2`, `Bsn`, `Pclo`, and the `Unc13` targets had none. The focal rows also showed strong self-RNA depletion for many one-hit comparators without a broader module, for example `Syn1` log2FC -0.834, FDR 1.59e-24; `Syp` -1.776, FDR 7.95e-66; `Sv2a` -1.048, FDR 1.86e-38; `Stxbp1` -0.663, FDR 9.38e-19; and `Cplx1` -0.863, FDR 4.29e-24. In the same focal class, `Syn2` had a negative but non-significant self row, log2FC -0.497 with BH FDR 0.425. None of these perturbations changed `Syn3` RNA itself in the focal class (`pvals_adj = 1.0` for the measured `Syn3` row under `Syn1`, `Syn2`, `Syp`, `Sv2a`, `Stxbp1`, `Vamp1`, `Cplx1`, and `Cplx2` perturbation).

I also checked the broader all-cell DE surface for the nearest analogs. `Syp`, `Sv2a`, and `Syn1` were frequently self-only across many recovered cell groups; `Syn2` had only three groups with any FDR<0.05 gene, each with a single DEG. `Stxbp1` was the main positive presynaptic counterexample, with multi-gene responses in some cortical, Pvalb, Sst, and midbrain classes, but still only one DEG in `151 TH Prkcd Grin2c Glut`. This separates an essential SNARE/MUNC18 fusion gatekeeper from synapsin-family reserve-pool loss for the focal scalar endpoint.

# Same-experiment analog reports

The internal `perturbai-july-260713-sourceguard-1773-v1` corpus agreed with the direct queries:

- `Syn1:F005` reported that `Syn1` did not phenocopy `Syn2` or the broader presynaptic-vesicle comparator set, and that `Stxbp1` was the only broad DE outlier among `Syn2`, `Syp`, `Sv2a`, `Stx1b`, `Stxbp1`, `Dnm1`, `Bsn`, `Pclo`, `Cplx1`, `Cplx2`, `Syt2`, `Vamp1`, `Rab3gap1`, `Rab3gap2`, and `Synj1`.
- `Syn2:F002` and `Syn2:F003` reported that large `Syn2` self-transcript drops in some non-focal groups did not propagate to downstream FDR<0.10 genes, and that `Syn2`, `Syn1`, `Syp`, `Sv2a`, `Dnm1`, `Cplx1`, and `Unc13a` were self-only or nearly flat while `Stxbp1` produced 140 downstream FDR<0.10 genes in Syn2-matched groups.
- `Syp:F004` and `Sv2a:F004` likewise placed visible synapsins and vesicle-cycle perturbations in a mostly flat response class, with protein-trafficking or electrophysiology as the expected phenotype rather than a broad resting nuclear RNA program.

Those findings are not independent of the Parquet; I used them to verify that the raw focal counts were part of a consistent all-cell pattern rather than a single underpowered focal exception.

# Biology of `Syn3`

`Syn3` is a synapsin-family synaptic-vesicle phosphoprotein. The family regulates vesicle clustering, the synaptic-vesicle reserve pool, and short-term release probability rather than acting as a transcription factor or chromatin regulator; this functional assignment comes from Syn1/Syn2 knockout and biochemical work summarized by Baldelli in NCBI Bookshelf (2013) and by Zhang and Augustine (2021, DOI: 10.3390/cells10030658), with classic mouse Syn1/Syn2 knockout evidence in Rosahl et al. 1995 (DOI: 10.1038/375488a0). `Syn3` itself was cloned as a third synapsin with the conserved vesicle-associated domain structure by Kao et al. 1998 (PNAS, DOI: 10.1073/pnas.95.8.4667; PMID 9539796), and Feng et al. showed that Synapsin-III knockout alters the recycling pool and inhibitory postsynaptic currents in cultured neurons while also delaying axon outgrowth (J Neurosci 2002, DOI: 10.1523/JNEUROSCI.22-11-04372.2002; PMID 12040043). Pieribone et al. reported that adult mouse Synapsin-III is punctate at nerve terminals but is especially enriched in immature neurogenic-region neurons (J Comp Neurol 2002, DOI: 10.1002/cne.10417; PMID 12412137), and later vertebrate work links `Syn3` to dopaminergic neuron development rather than to a broad postmitotic glutamatergic transcriptional program (Faustini et al. 2022, DOI: 10.3390/cells11233902; PMID 36497160).

These priors make `Syn1` and `Syn2` the right first analogs: all three synapsins act at vesicle pools, share partial reserve-pool biology, and are represented in the same molecular branch. The same priors also limit the expected RNA effect size. `Syn3` loss is expected to perturb presynaptic vesicle trafficking or release, and possibly earlier axon-growth/dopaminergic developmental processes, not to acutely force a large cell-state transition in sparse postnatal thalamic glutamatergic nuclei.

# Target-specific prediction

## `Syn3`: predicted `n_degs = 0`

The causal transfer chain I used was:

`Syn3` CRISPR loss in sparse P16 postmitotic thalamic glutamatergic neurons -> partial reduction of Synapsin-III function at presynaptic vesicle pools -> altered reserve-pool or release behavior at some terminals, with weaker expectation for Syn3-specific immature-neuron or dopaminergic-development functions in this focal class -> surviving P37-P44 NeuN+ nuclei assayed by snRNA-seq -> FDR-controlled mRNA changes.

The first two steps are supported by external synapsin biology. The last propagation step is where the evidence weakens: the visible paralogs show that loss of a reserve-pool synapsin is usually buffered before it becomes a broad nuclear RNA program. In `151 TH Prkcd Grin2c Glut`, `Syn1` had exactly one DEG and it was the `Syn1` transcript itself; `Syn2` had zero. The wider presynaptic analogs were the same in the focal class: `Syp`, `Sv2a`, `Vamp1`, `Cplx1`, `Stxbp1`, and `Dlg4` had one self-gene hit each and no downstream FDR<0.05 genes; `Cplx2`, `Stx1b`, `Bsn`, `Pclo`, and `Unc13a/b/c` had zero. Those are appropriate counterexamples because several, especially `Syp` and `Sv2a`, had very strong focal self-transcript depletion yet still no downstream transcriptome, showing that target-RNA knockdown in vesicle proteins need not create a multi-gene DE burden.

I therefore predicted a null focal FDR count rather than a one-hit self-only count. `Syn3` could in principle register as a single DEG through its own transcript, as `Syn1`, `Syp`, `Sv2a`, `Vamp1`, and `Cplx1` did. I down-weighted that outcome because `Syn2`, another paralog, was already negative in this focal class despite a raw negative self shift, and because adult Synapsin-III is more regionally restricted than Synapsin-I/II, with stronger literature support in immature neurons and dopaminergic development than in mature thalamic glutamatergic cell-state control. With no evidence that `Syn3` loss should exceed the `Syn1`/`Syn2` focal range or cross the `Stxbp1`-like boundary into a broader RNA response, the point estimate is:

`Syn3  0`

# Limits

This is an extrapolation from related visible perturbations, not a direct readout of withheld `Syn3`. The all-cell Parquet contains no `Syn3` perturbation rows in the model-visible data, the assay did not measure DNA editing, Synapsin-III protein, vesicle reserve pools, synaptic release, axon growth, or pre-assay loss of edited cells, and sparse recovered-nucleus snRNA-seq can miss electrophysiological or terminal-localization phenotypes. A one-DEG result driven only by the `Syn3` target transcript would be plausible if the guide pool achieved a strong detectable transcript drop in this focal class. A response above one DEG would require `Syn3`-specific propagation from presynaptic dysfunction to a postmitotic thalamic nuclear program; neither the visible synapsins nor the represented vesicle-cycle comparators support that as the default.
