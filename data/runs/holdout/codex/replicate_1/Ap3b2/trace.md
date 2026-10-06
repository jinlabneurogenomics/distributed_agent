## Target and endpoint

- Target manifest: `Ap3b2`
- Population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in this population
- Withheld target status: the `Ap3b2` perturbation profile and count were absent from the declared training count table and Parquet-derived training measurements used here.

## Evidence used

### Ap3b2 biology

The declared biology bundle supports Ap3b2 as a plausible but not high-burden thalamic transcriptional perturbation:

- Exact focal-population reach is high: in non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Ap3b2` was detected in 22,147 / 23,679 cells, 93.53%, with mean raw UMI 3.492 and pseudobulk CPM 218.856.
- AP3B2 is the neuron-specific beta3B subunit of cytosolic AP-3B, a dynamic adaptor involved in synaptic-vesicle and neuronal-process cargo sorting.
- The stock card adjudicates functional stock by harvest as `likely_substantially_depleted`: the P16 disruptive edit should stop beta3B resupply, and 21-28 elapsed days is longer than the broad mouse-brain protein lifetime proxy.
- That stock conclusion is only partial: no AP3B2-specific acute protein-depletion curve was found, and a stabilized neuronal-process pool could blunt short-window loss.
- Mouse `Ap3b2` loss has postnatal neural phenotypes and selected synaptic-cargo phenotypes, but the closest evidence is germline/cortical-hippocampal or spontaneous-null seizure evidence rather than P16-induced thalamic snRNA-seq.

### Training counts in the same cell class

The focal count table contains 1,674 non-held-out targets. Its empirical mass is near zero:

- 1,205 / 1,674 targets have `n_degs = 0`.
- 276 / 1,674 targets have `n_degs = 1`.
- The median is 0, the 75th percentile is 1, and the 90th percentile is 2.
- The mean is 14.05 only because a very small outlier tail reaches hundreds to thousands of DEGs.

The closest measured AP-3 / synaptic-vesicle comparators in this class are quiet:

| training target | `n_degs` | focal Parquet interpretation |
| --- | ---: | --- |
| `Ap3b1` | 0 | no BH-significant measured genes |
| `Clcn3` | 0 | no BH-significant measured genes |
| `Stx1b` | 0 | no BH-significant measured genes |
| `Cplx1` | 1 | the only significant gene is `Cplx1` itself |
| `Dnajc5` | 1 | the only significant gene is `Dnajc5` itself |
| `Syn1` | 1 | the only significant gene is `Syn1` itself |
| `Syp` | 1 | the only significant gene is `Syp` itself |

Thus perturbing synaptic-vesicle machinery in this exact population is measured as 0 or a self-transcript-only 1 DEG, not as the high-burden spliceosome/proteasome-like tail of the table.

## Synthesis

I treated the extreme count tail as a poor analog because AP3B2 is a synaptic-vesicle adaptor subunit rather than a global RNA-processing, proteasome, ubiquitin, or chromatin regulator. I also did not transfer the germline mouse phenotype to a large acute nuclear-RNA footprint: AP-3B cargo-routing failure can be real and postnatal while producing little survivor-conditioned transcriptional remodeling over the assay window.

The exact thalamic expression makes the `Ap3b2` transcript itself readily measurable, so a one-gene self-feature call is plausible. The matched AP-3/cargo/synaptic training set does not justify a broader downstream count above the 0-1 range. I therefore placed the point forecast at 1 DEG rather than 0 to reflect high target reach and likely functional realization, but kept it at the low end because all observed close functional comparators in this cell class are silent or self-only.

Predicted `n_degs`: 1
