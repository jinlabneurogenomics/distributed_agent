# Reasoning trace

## Question and interpretation

The held-out target list for this run contains one mouse perturbation, `Relb`.
The requested endpoint is the number of genes in `151 TH Prkcd Grin2c Glut`
whose Wilcoxon BH-adjusted p-value is below 0.05 after acute AAV CRISPR loss of
function. `Relb` is absent from both supplied training tables, so I estimated
its count by looking for non-held-out NF-kappaB/noncanonical-NF-kappaB
perturbations with observed signatures in the same focal cell group.

I treated zero as "no measured gene is expected to pass q < 0.05 in this assay",
not as a claim that Relb is biologically irrelevant or unedited.

## Sources used

- `training_de_all_cell_groups.parquet`: per-gene differential expression for
  non-held-out perturbations. I used this for focal-cell signed profiles of
  NF-kappaB pathway comparators.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: exact training endpoint,
  used to read the observed `n_degs` values for comparator perturbations.
- `197_Relb.csv`: requested-target manifest; it contained only `Relb`.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`: queried for `Relb`; it had no
  target-scoped finding, claim, or explicit reference for this held-out target.
- PubMed-indexed external literature:
  - Sun 2012, PMID 22435551, DOI `10.1111/j.1600-065X.2011.01088.x`.
  - Bista et al. 2010, PMID 20185819, DOI `10.1074/jbc.M109.076091`.
  - Fusco et al. 2016, PMID 27678221, DOI `10.1126/scisignal.aad9413`.
  - Engelmann et al. 2020, PMID 32145043, DOI `10.1002/dvdy.170`.
  - Mockenhaupt et al. 2021, PMID 34198987, DOI `10.3390/cells10071609`.

## Dataset computations

1. Read the requested-target manifest and confirmed the only held-out target is
   `Relb`.
2. Read the focal training DEG-count CSV and searched for direct NF-kappaB
   family or noncanonical pathway genes. The focal count distribution is very
   sparse: 1,205 of 1,674 training targets have 0 DEGs, the median is 0, the
   90th percentile is 2, and the 95th percentile is 18.
3. Found the pathway comparators available as training perturbations:
   `Rel`, `Nfkb1`, `Chuk`, and `Traf3`. Each has `n_degs = 0` in the supplied
   focal count table.
4. Used the run-local Distributed Agents profile comparison tool on the focal parquet
   slice for those four observed targets. For each target the tool compared
   signed `logfoldchanges` over 17,259 measured features and counted significant
   features using `pvals_adj < 0.05`.
5. Independently pulled the focal parquet rows for the same four targets to
   check q-value margins and matched nucleus counts.

Observed focal comparator evidence:

| training perturbation | relationship to `Relb` | focal `n_degs` | expression-pattern evidence |
| --- | --- | ---: | --- |
| `Rel` | another transcriptional member of the NF-kappaB/Rel family; a better family comparator than unrelated Rel-homology-domain proteins but more canonical/T-cell biased than RelB | 0 | 17,259 focal features; 0 significant; best q = 0.140; 205 matched perturbed nuclei |
| `Nfkb1` | p105/p50 NF-kappaB family member, primarily canonical rather than the `Nfkb2` p100/p52 partner used by RelB | 0 | 17,259 focal features; 0 significant; best q = 1.0; 181 matched perturbed nuclei |
| `Chuk` | IKKalpha, the kinase downstream of NIK that phosphorylates NFKB2/p100 during noncanonical NF-kappaB activation | 0 | 17,259 focal features; 0 significant; best q = 0.727; 156 matched perturbed nuclei |
| `Traf3` | basal inhibitor of NIK/noncanonical NF-kappaB; loss can derepress the pathway, so it is an opposite-direction test of pathway activity rather than a same-direction analog | 0 | 17,259 focal features; 0 significant; best q = 1.0; 211 matched perturbed nuclei |

The four profiles were not isolated missing rows: all had complete focal
profiles and substantial matched control coverage. Whole-profile cosines among
them were 0.698 to 0.741 and Pearson correlations were 0.635 to 0.684, but all
of that agreement was subthreshold. Every pair had zero same-direction
significant-program overlap because no comparator had any q < 0.05 gene.

## Target-specific reasoning

### Relb

RelB is a terminal NF-kappaB transcription-factor subunit and a principal
effector of the noncanonical pathway as a p52/RelB heterodimer. In the standard
pathway model, TNF-receptor-family signals stabilize NIK, NIK with CHUK/IKKalpha
drives NFKB2/p100 processing to p52, and TRAF3-containing complexes keep NIK
low in unstimulated cells; RelB participates in both inactive p100-containing
complexes and active p52/RelB dimers. That makes `Chuk` a mechanistic upstream
same-direction comparator and `Traf3` an informative opposite-direction
counterexample, while `Rel` and `Nfkb1` test broader NF-kappaB-family dependence.

The assay evidence argues against a detectable RelB-dependent transcriptional
program in recovered `151 TH Prkcd Grin2c Glut` nuclei:

- `Chuk` loss caused 0 DEGs and had no near-threshold q-values.
- `Traf3` loss also caused 0 DEGs; if the noncanonical module were basally
  poised and visible in these neurons, removing an upstream brake would be a
  plausible way to perturb it.
- The observed NF-kappaB transcription-factor comparators `Rel` and `Nfkb1`
  were also null, so the focal class did not show a general sensitivity to this
  TF family.

External biology does keep the prediction as a real extrapolation rather than a
proof. RelB can be expressed in specific developing and adult mouse brain
domains, and reviews of neuroinflammation describe RelB functions in CNS cell
types. Those facts show that a neuronal RelB phenotype is biologically possible.
However, the noncanonical NF-kappaB pathway is best established in immune,
stromal, epithelial, and inflammatory contexts; this screen sampled sparse,
postnatal NeuN+ nuclei rather than inflammatory glia or lymphoid stromal cells.
The closest observed pathway perturbations are therefore stronger calibration
than immune-system Relb-null phenotypes for this particular endpoint.

Prediction: `Relb = 0`.

## Limits and weak points

- `Nfkb2`, `Rela`, and `Map3k14` were not available in the focal training-count
  table, so the exact p52 partner of RelB and NIK itself could not be used as
  observed analogs.
- `Traf3` is an opposite-direction upstream perturbation, not a RelB knockout
  mimic: TRAF3 loss can activate NIK and canonical LTBR signaling in some cells.
  Its null profile is evidence that this module was not easily engaged here, but
  it is not equivalent to measuring `Relb`.
- The huge absolute log-fold changes seen for a few low-information genes in
  the null profiles all had q = 1 and were not used as biological evidence.
- Absence of q < 0.05 DEGs is power- and assay-dependent. The available
  perturbations had 156 to 211 matched perturbed nuclei in the focal class, so
  this is useful internal evidence, but it does not rule out a smaller RelB
  effect below the Wilcoxon/BH threshold.
- RelB effects can be stimulus-dependent. AAV CRISPR loss of function in
  postmitotic thalamic glutamatergic neurons without a TNFR-family inflammatory
  stimulus may miss programs that are prominent in immune or injury models.
