# Prediction trace for `151 TH Prkcd Grin2c Glut`

## Question and ambiguity resolved

The held-out manifest contains one target, `Tubb2a`. I interpreted
`n_degs` exactly as the supplied training endpoint: the count of measured genes
in `151 TH Prkcd Grin2c Glut` with `pvals_adj < 0.05`, including the
perturbed gene's own transcript when that row passes FDR. This is important
because the closest represented beta-tubulin perturbations have one DEG in the
training count, and that one gene is the self-transcript.

## Sources

- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Focal training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Requested held-out targets:
  `[local file: 252_Tubb2a.csv]`
- Internal same-experiment semantic layer: Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`
- External literature from NCBI PubMed:
  Brock et al. 2020, DOI `10.1136/jmedgenet-2019-106740`,
  PMID `32571897`; Maillard et al. 2022,
  DOI `10.1016/j.semcdb.2022.07.009`, PMID `35915025`;
  Lin et al. 2019, DOI `10.1126/science.aaz4352`,
  PMID `31727855`; Hoepfler et al. 2023,
  DOI `10.1016/j.molcel.2023.05.020`, PMID `37295431`.
- Additional same-corpus literature references used as background:
  Bittermann et al. 2019, PMID `31386652`, on differential tubulin-gene
  requirements in mouse forebrain; Hausrat et al. 2021,
  DOI `10.1002/dneu.22745`, PMID `32293117`, on alpha- and beta-tubulin
  isotype expression during mouse brain development.

## Dataset computations

I first checked the manifest and training universe. `Tubb2a` is absent from the
1,674-target training-count table, as required by the holdout. The focal-cell
training endpoint is very zero-inflated: 1,205/1,674 training targets have
`n_degs = 0`; 469 have at least one DEG; 276 have exactly one DEG; only 106
reach 10 or more DEGs.

I then sliced the focal group from the parquet for the represented structural
tubulins and nearby microtubule or motor perturbations:

```python
import pyarrow.dataset as ds
import pyarrow.compute as pc

expr = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin([
        "Tuba1a", "Tuba4a", "Tubb4b", "Tubb5", "Tbcd",
        "Dctn1", "Atxn10", "Mapt", "Map1b", "Map6", "Mapre2",
        "Stmn2", "Kif1a", "Kif1b", "Kif2a", "Kif3b", "Kif5a",
        "Kif5c", "Dync2h1", "Dync2i1", "Ttll5", "Nin",
    ])
)
table = ds.dataset(parquet_path, format="parquet").to_table(
    columns=["names", "gene_target", "logfoldchanges", "pvals_adj", "scores"],
    filter=expr,
)
```

This was used to separate self-transcript calls from downstream calls and to
inspect the tubulin rows that define the `Tuba1a` compensation signature.

## Target-specific analogs

`Tubb2a` encodes a beta-tubulin microtubule subunit. It was not represented as
a perturbation in either the raw DE input or the Distributed Agents corpus, so the main
question was whether it should behave like the alpha-tubulin positive control
`Tuba1a`, the represented beta-tubulins `Tubb4b` and `Tubb5`, or a broader
microtubule-neighborhood stress state.

Biologically relevant training perturbations in the focal group:

| training target | observed `n_degs` | focal expression-pattern evidence | interpretation for `Tubb2a` |
|---|---:|---|---|
| `Tubb5` | 1 | The only FDR<0.05 row was `Tubb5` itself: logFC -1.478, FDR 7.71e-23. Distributed Agents `Tubb5:F003` contrasted this directly with `Tuba1a`: in `151 TH Prkcd Grin2c Glut`, `Tubb5` had zero downstream genes even though the self row was strongly depleted. | Closest measured beta-tubulin analog. Supports one self row and no downstream tubulin-feedback cascade. |
| `Tubb4b` | 1 | The only FDR<0.05 row was `Tubb4b` itself: logFC -0.597, FDR 1.07e-7. Distributed Agents `Tubb4b:F002` and `Tubb4b:E025` report that candidate alpha- and beta-tubulin compensatory transcripts failed after `Tubb4b` perturbation: 0/176 `Tuba1a`, `Tuba4a`, `Tubb2a`, `Tubb2b`, `Tubb3`, `Tubb4a`, `Tubb5`, and `Tubb6` rows reached FDR<0.10 across the measured `Tubb4b` groups. | Another direct beta-tubulin analog. It argues that a postnatal beta-tubulin transcript can be reduced without inducing other tubulin genes. |
| `Tuba4a` | 2 | `Tuba4a` itself fell, logFC -0.710, FDR 2.43e-6, and the only downstream focal call was `Mast1`, logFC +0.304, FDR 0.0367. `Tuba4a:F004` showed that this alpha-tubulin paralog did not phenocopy the `Tuba1a` tubulin-isotype module. | An alpha-tubulin counterexample: even a direct alpha paralog had a sparse singleton downstream response rather than a broad compensation program. |
| `Tuba1a` | 7 | FDR<0.05 rows were the self row, logFC -0.967, FDR 2.78e-20, plus six up-regulated tubulin paralogs: `Tubb3` +0.576, `Tubb2a` +0.523, `Tuba4a` +0.696, `Tubb4a` +0.506, `Tubb4b` +0.513, and `Tubb5` +0.620. Distributed Agents `Tuba1a:F004` summarizes that `Tuba4a`, `Tubb4b`, and `Tubb5` do not phenocopy this module in the matched responder groups. | Positive control for assay visibility. It proves the focal group can show tubulin-isotype compensation, but its divergence from the beta-tubulin perturbations makes it a poor count donor for `Tubb2a`. |
| `Tbcd` | 12 | `Tbcd`, a tubulin-folding cofactor, induced `Tuba1a` and `Tuba1b` but not `Tubb2a` in the focal cell group; `Tubb2a` logFC was +0.042 with FDR 1. | A mechanistic neighbor but not a beta-tubulin-subunit phenocopy. It supports tubulin dosage sensitivity in the assay, not a broad `Tubb2a` prediction. |
| `Dctn1` | 75 | `Dctn1` triggered a sterol/lipid response (`Insig1`, `Msmo1`, `Hmgcr`, `Sqle`, and related genes) rather than a tubulin-paralog response. | Counterexample showing cytoskeletal transport can be transcriptionally visible while direct tubulin loss remains much narrower. |
| `Mapt`, `Map1b`, `Mapre2`, `Stmn2`, `Kif1a`, `Kif5a`, `Kif5c` | 1 each | Each had a one-gene focal count in the training table, dominated by the perturbed self-transcript for the self-expressed genes I inspected. `Map6`, `Kif2a`, `Kif3b`, `Dync2h1`, `Dync2i1`, `Ttll5`, and `Nin` had zero. Distributed Agents claims around `Tubb4b`, `Tuba4a`, `Mapt`, and `Mapre2` describe this broader microtubule-neighborhood set as flat, sparse, or nonconvergent rather than one coherent mRNA module. | These make a broad injury/stress response unlikely merely because `Tubb2a` is a microtubule gene. |

External biology was used only to choose which internal comparisons mattered.
TUBB2A pathogenic variants cause tubulinopathy/neurodevelopmental phenotypes
with epilepsy, cortical malformations, and variable dysgyria in humans
(Brock et al. 2020; Maillard et al. 2022). Those observations make `Tubb2a` a
real neuronal microtubule gene, but they mostly describe heterozygous missense
alleles acting during fetal brain development; they do not imply that a sparse,
partial P16 CRISPR loss-of-function in surviving juvenile thalamic neurons
should create hundreds of nuclear RNA DEGs. Tubulin abundance is also governed
by TTC5-linked co-translational mRNA autoregulation and SCAPER/CCR4-NOT
recruitment (Lin et al. 2019; Hoepfler et al. 2023), making tubulin transcript
feedback plausible in principle. The decisive observation is that this feedback
was selective in the dataset: strong after `Tuba1a`, absent after `Tubb5` and
`Tubb4b`, and minimal after `Tuba4a`.

## Zero/nonzero decision and point estimate

I predicted a nonzero count for `Tubb2a` because all four represented
structural tubulin perturbations that were assayed in this focal group had a
detectable self-transcript row at FDR<0.05:

- `Tuba1a`: -0.967, FDR 2.78e-20
- `Tuba4a`: -0.710, FDR 2.43e-6
- `Tubb4b`: -0.597, FDR 1.07e-7
- `Tubb5`: -1.478, FDR 7.71e-23

`Tubb2a` itself was a well-measured downstream transcript in the same focal
group: it rose after `Tuba1a` perturbation, logFC +0.523 and FDR 2.68e-7, and
fell after `Atxn10` perturbation, logFC -0.307 and FDR 0.0266. That makes a
self row plausible if its guide set causes any comparable mRNA loss.

I did not add any downstream genes to the point estimate. The nearest measured
beta-tubulin perturbations, `Tubb5` and `Tubb4b`, were exactly self-only in
the focal endpoint and lacked the `Tubb2a`/`Tubb3`/`Tuba4a`/`Tubb4a`/
`Tubb4b`/`Tubb5` compensation pattern that followed `Tuba1a` loss. The sparse
`Tuba4a`, MAP, stathmin, kinesin, dynein, and dynactin counterexamples also
argue against a generic microtubule damage or neuronal injury program.

Predicted value: `Tubb2a -> 1`.

## Limits and extrapolation

- `Tubb2a` was absent from the supplied DE table, training count table, and
  Distributed Agents target cards, so the prediction is necessarily extrapolated from
  other tubulin isotypes.
- The closest paralogs `Tubb2b` and `Tubb3` were not available as perturbation
  targets in the 1,674-gene training set; `Tubb3` and `Tubb2a` were available
  only as measured response genes.
- The one-count prediction depends on the unobserved `Tubb2a` CRISPR guides
  producing a self-RNA decrease large enough for FDR<0.05. The experiment does
  not provide indel or protein depletion measurements, and the dataset warns
  that target mRNA loss is neither required nor sufficient for functional
  editing.
- A zero downstream prediction means "no measured nuclear RNA row is expected
  to cross this assay's FDR threshold", not that TUBB2A is biologically
  dispensable. Microtubule polymerization, axonal transport, morphology,
  late behavioral phenotypes, and dominant-negative missense mechanisms are
  mostly outside this snRNA-seq endpoint.
- FDR thresholding is brittle for singleton effects such as `Tuba4a -> Mast1`;
  a weak `Tubb2a` secondary marker could land on either side of 0.05.
