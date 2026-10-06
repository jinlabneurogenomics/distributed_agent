# Question and resolved ambiguities

This run asks for the held-out `n_degs` value for every target in
`201_Satb1.csv`, in the focal cell group `151 TH Prkcd Grin2c Glut`.  The
manifest contains one held-out target:

| target_name |
|---|
| Satb1 |

I interpreted `n_degs` exactly as in the training endpoint:
the number of measured genes whose Wilcoxon Benjamini-Hochberg adjusted
`pvals_adj` is below 0.05 for the pooled perturbation `gene_target` in the
focal cell group.  I counted the target transcript itself when it passed the
threshold, matching the supplied training counts.  I did not interpret a weak
target-row RNA change as failed editing, because this assay reports a pooled,
sparse AAV CRISPR loss of function rather than a homogeneous full knockout.

# Sources used

- Input endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Held-out manifest:
  `[local file: 201_Satb1.csv]`.
- Distributed Agents same-experiment corpus,
  `perturbai-july-260713-sourceguard-1773-v1`.  `Satb1` was absent from this
  corpus release: `target_context(Satb1)`, `related_targets(Satb1)`, and
  lexical claim search for `Satb1` all returned zero records.
- Distributed Agents Runtime profile tools, used to compare selected non-held-out focal
  signatures by signed log-fold-change and FDR activity.
- NCBI PubMed for external SATB1 literature:
  Close et al. 2012, DOI 10.1523/JNEUROSCI.3583-12.2012, PMID 23223290;
  Denaxa et al. 2012, DOI 10.1016/j.celrep.2012.10.003, PMID 23142661;
  Gongrich et al. 2020, DOI 10.1083/jcb.201905002, PMID 31676717;
  Huang et al. 2011, DOI 10.1016/j.neures.2011.05.015, PMID 21658419;
  Turovsky et al. 2021, DOI 10.3390/ijms22115968, PMID 34073140.

# Computational checks

The training endpoint has 1,674 perturbations for the focal cell group.  The
distribution is zero-heavy: mean 14.1 DEGs, median 0, 75th percentile 1,
90th percentile 2, and 469/1,674 perturbations are nonzero.  Thus a held-out
gene needs specific evidence to move away from zero, and a singleton count is
already above the bulk of the distribution.

For focal-cell rows in the DE parquet, I used the adjusted p-value threshold
from the endpoint, grouped by `gene_target`, and checked that the sums matched
the training CSV for the queried genes.  Example query shape:

```sql
select gene_target,
       sum(pvals_adj < 0.05) as de_count,
       min(pvals_adj) as min_q
from read_parquet($training_de)
where group_name = '151 TH Prkcd Grin2c Glut'
  and gene_target in ($selected_training_genes)
group by gene_target;
```

I also inspected, for `Satb1` and its analogs, the target transcript rows and
the measured `Satb1` rows across all non-held-out focal perturbations.  Four
training perturbations significantly up-regulated measured `Satb1` in this
cell group: `Cic` with 576 total DEGs and `Satb1` log2FC +0.581,
q = 0.00250; `Tnpo3` with 618 total DEGs and `Satb1` log2FC +0.757,
q = 0.00314; `Atxn1` with 187 total DEGs and `Satb1` log2FC +0.512,
q = 0.0103; and `Tbcd` with 12 total DEGs and `Satb1` log2FC +0.752,
q = 0.0177.  Those are not mechanistic loss-of-SATB1 analogs, but they show
that `Satb1` is detectable enough in the focal data to move at FDR 0.05.
Across all 1,674 training perturbations in this cell group, the measured
`Satb1` row had 54 raw p values below 0.05 and 4 BH-significant values;
`Satb2`, by contrast, had no raw p value below 0.05 and no BH-significant
values as a measured gene.

The observed-profile comparison over `Satb2`, `Smad2`, `Smarca2`, `Smarca4`,
`Mecp2`, `Ctcf`, and `Yy1` used `logfoldchanges` as signed values and
`pvals_adj < 0.05` to mark active features.  The relevant activity counts were
exactly the training endpoint counts: `Satb2`, 0 significant features;
`Smad2`, 1; `Smarca2`, 1; `Smarca4`, 0; `Mecp2`, 16; `Ctcf`, 270; and `Yy1`,
720.  This profile view was mainly a check that the closest biological analogs
were genuinely in the no/low-response part of the assay, not hidden among
large shared signatures.

# Satb1-specific analogs and counterexamples

| training perturbation | focal `n_degs` | focal expression evidence | interpretation for `Satb1` |
|---|---:|---|---|
| `Satb2` | 0 | No significant focal features; the `Satb2` target row had log2FC -1.161 but q = 1, and the measured `Satb1` row in `Satb2` knockout was unchanged, log2FC -0.0048, q = 1.  `Satb2` also had zero significant DEGs in every profiled cell group in the input parquet. | Closest paralog and same AT-rich DNA-binding SATB family.  This is the strongest within-dataset argument against a broad SATB-family response in `151 TH Prkcd Grin2c Glut`.  It is imperfect because `Satb2` and `Satb1` have different spatial expression and developmental roles. |
| `Bcl11a` | 0 | No focal feature passed FDR; `Satb1` row log2FC +0.087, q = 1. | Projection-neuron/cortical developmental transcription-factor counterexample.  Supports the idea that many lineage TFs are inert in this postnatal thalamic assay. |
| `Bcl11b` | 0 | No focal feature passed FDR; `Satb1` row log2FC -0.138, q = 1. | Same as above; a counterexample to assigning many DEGs solely because the gene is a neuronal TF. |
| `Tbr1` | 0 | No focal feature passed FDR; `Satb1` row log2FC +0.017, q = 1. | Another cortical developmental TF with no focal effect. |
| `Smad2` | 1 | The only focal DEG was `Cpne7`, log2FC -0.411, q = 0.0167; `Satb1` row log2FC +0.236, q = 1. | Activin/SMAD signaling can interact with SATB1 in SST-interneuron specification, but the actual focal response to `Smad2` loss is a singleton and is not a SATB1-like profile. |
| `Acvr1`, `Acvr2a`, `Acvr2b`, `Tgfbr1`, `Tgfbr2`, `Smad1`, `Smad3`, `Smad4`, `Smad9` | 0 each | Each had zero focal DEGs; `Smad1` was the only one in this set with min q below 1, but its best q was still 0.561. | Counterexamples for TGF/activin pathway membership.  They argue that the SATB1-linked activin mechanism is not strongly engaged in this thalamic glutamatergic readout. |
| `Smarca2` | 1 | The only focal DEG was `Smarca2` itself, log2FC -0.690, q = 1.05e-5; measured `Satb1` was unchanged, q = 1. | Shows that even a chromatin remodeler can give a singleton self-dominated response here. |
| `Smarca4` | 0 | No focal feature passed FDR; min q = 0.686. | Additional counterexample to treating all chromatin regulators as broad-effect nodes. |
| `Ctcf` | 270 | A clear positive-control signature in this cell group, with 270 DEGs and min q = 5.3e-30. | Boundary case: a ubiquitously important genome organizer is detectable in the assay, so the low counts for the SATB-family and pathway analogs are not caused by an inability to detect transcriptional regulators in general. |
| `Yy1` | 720 | Very broad focal signature, min q = 8.1e-24. | Same boundary case for a broad transcription factor/chromatin regulator. |
| `Mecp2` | 16 | Small but real focal signature, min q = 1.4e-6. | A neuronal chromatin regulator can produce a modest response.  This supports a small nonzero prediction for `Satb1` more than a large one. |
| `Grin1`, `Grin2a`, `Grin2b`, `Grin2d`, `Grin3a`, `Gria1`, `Gria2`, `Gria3` | 89, 1, 2, 0, 0, 0, 0, 0 | Mostly zero or near-zero, except for the obligate NMDA receptor subunit `Grin1`. | Turovsky et al. found SATB1/SATB2-dependent regulation of glutamate receptor genes in cortical cultures.  The receptor-gene training perturbations themselves do not imply a large receptor-driven secondary program in this focal group. |
| `Cic`, `Tnpo3`, `Atxn1`, `Tbcd` | 576, 618, 187, 12 | These were the only focal perturbations that significantly changed the measured `Satb1` row, and all increased it. | Evidence that `Satb1` is measurable and can vary in strong focal states, but not a direct guide for loss of SATB1 because the direction is opposite and the perturbations are mechanistically broad. |

# Biological rationale and prediction

SATB1 is a nuclear AT-rich DNA-binding transcriptional and chromatin organizer.
In the developing cortex it has a well documented role in MGE-derived
interneuron maturation: it is induced downstream of LHX6, promotes terminal
differentiation of SST and PV interneurons, and conditional interneuron loss
reduces SST cells and cortical inhibition by early postnatal stages
(Denaxa et al. 2012; Close et al. 2012).  Activin/ALK4 signaling can connect to
this program through SMAD2 and SATB1 nuclear repositioning at the `Sst`
promoter in MGE-derived interneurons (Gongrich et al. 2020).  SATB1 is also
present in selected adult CNS neurons, including small thalamic populations,
and absent from glia by immunohistochemistry (Huang et al. 2011).  In cortical
neuronal culture, deletion of `Satb1` or `Satb2` changed neurotransmitter
receptor gene expression and calcium responses (Turovsky et al. 2021).

Most of that biology is developmental, cortical, or GABAergic, whereas the
requested readout is an acute P16-to-P37/P44 sparse perturbation in postmitotic
`151 TH Prkcd Grin2c Glut` neurons.  The directly analogous training data
therefore get priority over the published knockout phenotypes.  The strongest
same-assay evidence, `Satb2`, had no FDR-significant expression response, and
the BCL11/TBR1 developmental TFs plus TGF/SMAD genes were all zero or
singleton responses.  That makes a broad `Satb1` knockout state unlikely.

I nevertheless do not set `Satb1` to zero.  The measured `Satb1` transcript,
unlike `Satb2`, did move significantly in several focal perturbations; and in
the training set a singleton `n_degs` is often just the perturbed transcript
or one immediate low-amplitude downstream feature.  The low-count analogs
`Smad2`, `Smarca2`, `Cux2`, and `Zic1` show that this part of the endpoint is
populated by exactly such isolated features.  My point prediction is therefore
`1`: one FDR-significant DEG, not a SATB1-driven thalamic transcriptional
program.

# Limits of the reasoning

- There is no curated `Satb1` node in the Distributed Agents same-experiment corpus, so
  there was no same-experiment claim graph for SATB1 itself.
- `Satb2` is the closest paralog but is not an interchangeable perturbation:
  SATB2 is best known for different cortical projection-neuron programs, and
  its zero-count training signature could reflect lower focal expression.
- SATB1's strongest published neuronal phenotypes are germline or conditional
  developmental manipulations in cortical interneurons or in vitro cortical
  neurons.  The supplied experiment is acute, partial, mosaic CRISPR in
  postmitotic juvenile neurons, so developmental cell-loss or subtype-fate
  phenotypes should not be ported literally.
- The focal group may include only a subset of the thalamic SATB1-positive
  neurons described by Huang et al.; without baseline expression counts for the
  held-out `Satb1` perturbation, the predicted singleton is an extrapolation
  from detectability of measured `Satb1` under other perturbations.
- The low predicted count is assay-specific.  It should not be read as saying
  SATB1 is biologically unimportant in neurons, only that this focal
  single-nucleus DE endpoint is expected to record at most a minimal response.
