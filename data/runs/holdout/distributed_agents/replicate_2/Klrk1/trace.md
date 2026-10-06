# Held-out DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and interpretation

The task asks for the number of FDR 0.05 Wilcoxon DEGs that the fully held-out perturbation `Klrk1` would have produced in the `151 TH Prkcd Grin2c Glut` focal class. I treated `n_degs` exactly as in the supplied focal training CSV: a raw count of measured genes with `pvals_adj < 0.05`, without trying to subtract the perturbed gene itself. Zero therefore means no measured transcript, including the target transcript, is expected to pass the assay's BH threshold.

The only requested target in `[local file: 120_Klrk1.csv]` was:

```tsv
target_name
Klrk1
```

## Sources used

- Raw within-experiment endpoint file:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Raw within-experiment DE table:
  `[local file: training_de_all_cell_groups.parquet]`.
- Same-experiment Distributed Agents semantic corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, queried by `target_context`.
  `Klrk1` itself had no corpus report in this held-out run; the useful
  reports were for represented analog/counterexample perturbations such as
  `Cd247`, `Il2rb`, `Stat5b`, `Tbx21`, and `Rorc`.
- External mechanism priors:
  - NKG2D/KLRK1 is an activating NK- and cytotoxic-T-cell receptor for stress
    ligands, rather than a canonical neuronal receptor: Bauer et al., 1999,
    Science, PMID:10426993, DOI:10.1126/science.285.5428.727.
  - Mouse NKG2D signals through the transmembrane adaptors DAP10/HCST and, for
    an alternatively spliced activated-NK isoform, DAP12/TYROBP: Gilfillan et
    al., 2002, Nature Immunology, PMID:12426564, DOI:10.1038/ni857.
  - The training-set immune transcription-factor comparators have the expected
    lymphoid rather than basal-neuronal wiring: T-bet/TBX21 directs Th1
    differentiation in Szabo et al., 2000, Cell, PMID:10761931,
    DOI:10.1016/S0092-8674(00)80702-3; RORgammat/RORC directs IL-17+ T-helper
    differentiation in Ivanov et al., 2006, Cell, PMID:16990136,
    DOI:10.1016/j.cell.2006.07.035.

## Dataset computations

I first calibrated the focal endpoint over all 1,674 non-held-out training
perturbations. The distribution is strongly concentrated at zero:

```text
median n_degs = 0
75th percentile = 1
90th percentile = 2
95th percentile = 18
zeros = 1205 / 1674
positive = 469 / 1674
```

The focal parquet rows were then filtered to training perturbations in
immune-receptor, gamma-chain cytokine, and JAK/STAT neighborhoods of `Klrk1`.
The relevant operation was:

```python
dset.to_table(
    columns=[
        "names", "gene_target", "logfoldchanges", "pvals_adj", "scores",
        "n_pert_matched", "n_ctrl_matched",
    ],
    filter=(
        (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
        & pc.field("gene_target").isin(targets)
    ),
)
```

I used the count CSV for the exact observed `n_degs` values and the filtered
parquet rows to check whether these were clean nulls or near-threshold
signatures.

### Relevant training perturbations

Direct mouse NKG2D signal-transduction partners `Hcst`/DAP10 and
`Tyrobp`/DAP12, and other `Klr*` family receptors, were not present as training
targets in the focal count CSV. The best available within-dataset analogs were
therefore immune-receptor adaptors, gamma-chain cytokine/STAT genes that
support NK-cell biology, and lymphocyte-lineage transcription factors.

| Training target | Focal `n_degs` | Focal expression-pattern evidence | Why it is informative for `Klrk1` |
|---|---:|---|---|
| `Cd247` | 0 | In 182 perturbed nuclei, every measured gene had `pvals_adj = 1.0`; the lowest nominal rows were nonsystematic genes such as `Kcnj12`, `Inpp5e`, and `Ap4s1`. | `Cd247` is an immunoreceptor ITAM adaptor. It is not the direct NKG2D adaptor, but it is the same broad class of lymphocyte receptor signaling, and the corpus reports `Cd247` as having no FDR<0.10 downstream gene in any of 22 measured NeuN+ neuronal groups. |
| `Cd3d`, `Cd3e`, `Cd3g`, `Cd4`, `Cd79a`, `Cd79b`, `Icos` | 0 each in the focal count CSV | Their focal endpoint is exactly flat at FDR 0.05. | Distributed Agents corpus claim `claim:5dc92c39ffb6bdb352d2` summarizes the same-experiment evidence that represented CD3/TCR, CD4/MHC, and BCR/immunoreceptor perturbations do not form a latent shared TCR/CD3/BCR-like neuronal RNA module. This argues that `Cd247` is not a lone failed member of an otherwise active immune-receptor cassette. |
| `Il2ra`, `Il2rb`, `Il2rg`, `Il21r`, `Il23r`, `Foxp3` | 0 each in the focal count CSV | `Il2rb` and `Il2rg` had no near-threshold focal genes at all: the best adjusted p-value in each focal signature was 1.0. `Il2ra` was also flat, with the best adjusted p-value 0.435 for a singleton `Calb1` row. | IL-2/IL-15 gamma-chain cytokine signaling is a major NK-cell survival/activation context for NKG2D+ cells, but the corpus reports an IL-2 receptor/gamma-chain/STAT5/Treg-axis null module in NeuN-enriched neuronal nuclei. |
| `Stat5b`, `Stat2`, `Stat3`, `Stat4` | 0 each in the focal count CSV | All four were focal nulls; for `Stat5b`, the top adjusted p-value was 1.0 despite 207 perturbed nuclei. | These are downstream cytokine transcription factors. Distributed Agents corpus findings for `Stat5b` report no FDR<0.10 genes in any assayed neuronal group and no shared JAK/STAT signature across cytokine receptors and STAT paralogs. |
| `Stat1` | 1 | The only focal DEG was `Stat1` itself (`log2FC = -1.30`, `pvals_adj = 0.027`); the next genes had `pvals_adj >= 0.435`. | This is a boundary case showing that a cytokine-family perturbation can register its self transcript without exposing a downstream cytokine-response program. It supports predicting `Klrk1` as zero rather than a broad nonzero response. |
| `Tbx21` | 0 | In 224 perturbed nuclei, the leading focal rows all had `pvals_adj = 1.0`. | T-bet is central to type-1 lymphoid/NK programs. The corpus reports that `Tbx21` loss produced no robust DE in 22 measured non-olfactory neuronal groups and no ectopic IFN-gamma/Th1-like module. |
| `Rorc` | 0 | In 195 perturbed nuclei, the leading focal rows all had `pvals_adj = 1.0`. | This is another lymphoid-lineage transcription factor counterexample: even a DNA-binding immune regulator with clear non-neuronal effector biology was transcriptionally silent in the focal thalamic neurons. |
| `Fcgr4`, `C3`, `Csf3r` | 0 each in the focal count CSV | `Fcgr4` had no focal gene below `pvals_adj = 1.0` in 162 perturbed nuclei. | These innate/myeloid comparators test whether immune or inflammatory receptors in general make nonspecific neuronal signatures in this assay; they do not. |

As an additional feature-level check, the measured `Klrk1`, `Hcst`,
`Tyrobp`, `Cd247`, `Nkg7`, `Prf1`, and `Gzmb` rows were present for every
training perturbation in the focal group, but none of them was FDR-significant
under any of the 1,674 training perturbations. Their minimum adjusted p-values
were 0.948 for `Cd247` and 1.0 for the others, consistent with a non-engaged
NK/cytotoxic transcript set in this NeuN-enriched thalamic population.

## Target-specific prediction

### `Klrk1` -> 0 predicted DEGs

`Klrk1` encodes NKG2D, an activating C-type lectin-like receptor used by NK
cells and cytotoxic T cells to detect stress-induced ligands. The represented
brain nuclei were NeuN+ neurons from whole brain excluding olfactory bulb and
hindbrain; glia, immune cells, and vascular cells were intentionally absent or
under-sampled. That makes a cell-autonomous `Klrk1` transcriptional response in
`151 TH Prkcd Grin2c Glut` neurons biologically unlikely.

The direct NKG2D adaptors `Hcst` and `Tyrobp` were not available as perturbation
targets, so the internal evidence is not a same-complex test. Still, the
available lymphocyte receptor and cytokine-signaling tests all point the same
way. `Cd247` and the other represented CD3/TCR/BCR-like receptor genes are
focal zeros and, in the Distributed Agents corpus, whole-neuronal nulls or nearly null.
The IL-2 receptor gamma-chain genes and downstream STATs are likewise flat:
`Il2ra`, `Il2rb`, `Il2rg`, `Stat2`, `Stat3`, `Stat4`, and `Stat5b` all have
zero focal DEGs, while `Stat1` has only its own self row. The NK/Th1 and
Th17/ILC-associated transcription factors `Tbx21` and `Rorc` are also exact
focal zeros. These are not expected to phenocopy NKG2D biochemically, but they
are strong negative controls for the possibility that the Perturb-seq platform
was uncovering a hidden basal lymphoid/NK-like module in thalamic neurons.

Given that the focal training distribution has a 72% zero rate, that the best
mechanistically available immune comparators are clean zeros rather than
near-threshold positives, and that `Klrk1` lacks a known autonomous role in
postnatal thalamic glutamatergic neurons, the calibrated point prediction is:

```text
Klrk1: 0 DEGs
```

## Limits and extrapolation

- The most direct `Klrk1` biochemical comparators, `Hcst`/DAP10,
  `Tyrobp`/DAP12, and other NKG2D-family `Klr*` targets, were not measured as
  non-held-out training perturbations. The prediction therefore extrapolates
  from adjacent immunoreceptor and cytokine modules rather than from a direct
  same-complex paralog.
- The absence of a focal snRNA-seq response does not show that Cas9 failed to
  cut `Klrk1` guides, that the target protein would be unchanged, or that NKG2D
  has no role in bona fide NK cells or neuroinflammatory conditions. It only
  predicts that sparse P16 CRISPR loss in recovered P37-P44 thalamic
  glutamatergic neuronal nuclei will not generate a transcript passing the
  single-nucleus Wilcoxon FDR 0.05 threshold.
- The `n_degs` endpoint includes occasional self-transcript-only events, as
  seen for `Stat1`, so a prediction of zero is slightly riskier than simply
  predicting "no downstream biology." I kept `Klrk1` at zero because its focal
  transcript row was unresponsive across all training perturbations and because
  the immune-receptor comparators were exact zeros rather than one-gene self
  positives.
