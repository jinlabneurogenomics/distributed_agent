# Uqcc2 DEG-count forecast

## Target and endpoint

- Target: `Uqcc2` from the declared one-row manifest.
- Cell group: `151 TH Prkcd Grin2c Glut`.
- Endpoint: integer count of focal-class measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- The target perturbation itself is absent from the focal count table; the forecast below did not use a Uqcc2 same-experiment outcome.

## Biology prior used

The declared Uqcc2 bundle places the edit in P16-to-P37/P44 postmitotic mouse thalamic neurons and reports exact focal expression of `Uqcc2` in non-target nuclei: mean raw UMI 1.423, mean CP10K 0.884, and expression in 16,471 of 23,679 cells, or 69.56%. That makes the target transcript observable in this class, but expression reach is not an editing-efficiency measurement.

The functional-stock card favors substantial depletion by harvest in successfully edited expressing cells: UQCC2 is an assembly factor for cytochrome-b/complex-III biogenesis, the edit should prevent new UQCC2-dependent assembly, and the available respiratory-chain assembly-factor/complex-III turnover proxies are multi-day rather than multi-week. The same card preserves uncertainty because mature pre-edit complex III is not directly destroyed by the edit, the kinetics are heterologous human-cell proxies, and the assay sees survivor-conditioned nuclear RNA.

I therefore treated Uqcc2 as a realized complex-III-assembly perturbation whose expected transcriptional scale should be read from measured complex-III or nearby OXPHOS perturbations, not from generic mitochondrial severity.

## Training evidence that set the scale

I used the focal training count table and the declared Parquet in the exact `151 TH Prkcd Grin2c Glut` context.

The full focal count table is sparse: 1,205 of 1,674 training perturbations are zero, the median is zero, the 75th percentile is one, and only the high tail reaches hundreds to thousands of DEGs.

A Uqcc2 analog-nomination pass over the training universe found no exact complex or paralog replacement; every top nominee was a broad functional fallback. The strongest mechanistic nominee was `Ttc19` from the `mitochondrial respiratory chain complex III assembly` term. Close training-available complex-III comparators and their focal counts were:

| comparator | focal `n_degs` | interpretation |
| --- | ---: | --- |
| `Ttc19` | 1 | self-target singleton in the focal Parquet slice |
| `Cyc1` | 1 | self-target singleton |
| `Uqcrc2` | 1 | self-target singleton |
| `Uqcrq` | 1 | one downstream singleton, `Gpr180` |
| `Uqcrfs1` | 0 | no focal DEG |
| `Uqcrb` | 0 | no focal DEG |
| `Uqcrh` | 0 | no focal DEG |

The primary complex-III/assembly branch therefore has median one and range zero to one. Same-experiment packaged Findings for these measured comparators were concordant with that interpretation: `Ttc19`, `Uqcrc2`, `Uqcrfs1`, `Uqcrb`, `Uqcrh`, and `Uqcrq` all lacked a broad mitochondrial ISR, UPRmt, redox/HIF, or shared complex-III stress program, and the few singleton downstream hits were private rather than recurrent.

Neighboring mitochondrial and OXPHOS boundaries were also quiet in the focal count table: `Rmnd1` 0, `Lrpprc` 0, `Ndufa9` 0, `Ndufv1` 0, `Cox4i1` 0, `Cox5a` 1, and `Sdha` 1. In contrast, generic stress or regulatory positives were off-scale and off-mechanism for Uqcc2: `Opa1` had 37 focal DEGs, `Nrf1` had 138, and `Bmal1` had 103.

The profile comparison kept the seven complex-III nodes as primary and the broader mitochondrial/regulatory nodes only as boundaries. All primary complex-III pair profiles were available; their selected-cohort tail overlaps were weak and their FDR-significant programs had zero overlap, so the relevant shared observation was flatness rather than a coherent latent response module.

## Point forecast

I set the point at **1 DEG**.

The count is not raised above one because Uqcc2 most directly maps to a represented complex-III branch that is uniformly 0-1 focal DEGs and explicitly lacks a recurrent mitochondrial-stress transcriptome. `Opa1`, `Nrf1`, and `Bmal1` show that the focal class can mount larger programs, but their mechanisms and observed signatures are divergent boundaries rather than Uqcc2 scale donors.

I chose one rather than zero because the held-out target is well expressed in the focal nuclei and the closest assembly/subunit comparators often contributed exactly one significant self-transcript row without any broader downstream program. Self-target RNA loss was used only as a count contribution, not as a measure of functional editing strength.
