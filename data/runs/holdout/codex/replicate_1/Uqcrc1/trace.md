# Direct DEG-count forecast for Uqcrc1

## Target and endpoint

- Target: `Uqcrc1`
- Focal cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes with Wilcoxon `pvals_adj < 0.05`
- Declared measurement scope: acute sparse P16 neuronal CRISPR loss of function, assayed 21-28 days later in recovered NeuN-positive thalamic nuclei

## Evidence used

### Canonical Uqcrc1 biology bundle

The target bundle identifies UQCRC1 as core protein 1 of mitochondrial respiratory complex III, installed in the obligate complex-III dimer and respiratory supercomplexes. Uqcrc1 loss has postnatal neural relevance: adult heterozygous mouse brain had reduced complex-III formation/activity and ATP, cognitive phenotypes, and worse ischemic outcomes.

That same bundle argues against expecting an immediate full null state in this experiment. By the P16 edit, UQCRC1-containing complex III is already present; the edit should block new UQCRC1 synthesis but does not directly remove pre-existing assembled complexes. Adult brain mitochondrial proteins and ETC complexes have mixed turnover, with a long-lived ETC fraction stabilized in respiratory supercomplexes, and no UQCRC1-specific neuronal clearance time was found for the 21-28 day P16-to-harvest window. The functional-stock adjudication therefore places Uqcrc1 on a partially depleted / leading-edge state at harvest, with considerable residual function plausible.

The exact allowed focal-expression measurement shows `Uqcrc1` is readily assayed in the target class: 23,218 of 23,679 non-target nuclei express it, `pct_cells_expressing = 98.05`, `mean_raw_umi = 6.29`, and `pseudobulk_cpm = 394.17`. I used this only as focal reach; it does not establish editing efficiency or downstream response size.

### Training count table

The requested thalamic class is zero-inflated even though it is one of the high-yield classes:

- 1,674 visible training perturbations
- 1,205 with `n_degs = 0`
- median `n_degs = 0`
- 75th percentile `n_degs = 1`
- 90th percentile `n_degs = 2`
- mean `n_degs = 14.05`, driven by a long tail such as `Uba5 = 2677`

The biologically closest visible structural respiratory-chain perturbations were far below the global mean in this same cell class:

```text
Coa8 0   Cox11 0   Cox4i1 0   Cox5a 1   Cox6a1 0   Cox7b 0
Cox8a 0 Lrpprc 0  Ndufa10 1 Ndufa11 0  Ndufa12 0  Ndufa4 1
Ndufa6 1 Ndufa8 0 Ndufa9 0  Ndufaf2 0 Ndufaf4 0 Ndufaf5 0
Ndufb10 1 Ndufb11 1 Ndufb3 0 Ndufb7 0 Ndufb8 1 Ndufb9 1
Ndufc2 1 Ndufs2 1 Ndufs4 0 Ndufs7 0 Ndufs8 1 Ndufv1 0
Ndufv2 1 Sdha 1 Uqcrb 0 Uqcrc2 1 Uqcrfs1 0 Uqcrh 0 Uqcrq 1
```

So the represented Cox/Nduf/Sdh/Uqcr/Lrpprc/Coa8 set contributed 15 total FDR < 0.05 genes across 37 matched structural OXPHOS targets in `151 TH Prkcd Grin2c Glut`, with 22/37 at zero and every nonzero member at one. Adding the nearby complex-III genes `Cyc1` and `Ttc19` keeps the same scale: 17 total FDR < 0.05 genes across 39 targets.

### Focal Parquet rows for selected respiratory-chain comparators

For the nearest complex-III or respiratory-chain comparators, the raw focal Parquet slice showed that one-count responses were mostly self-transcript calls rather than downstream programs:

| perturbation | focal significant row at FDR < 0.05 |
| --- | --- |
| `Uqcrc2` | `Uqcrc2` only |
| `Cyc1` | `Cyc1` only |
| `Ttc19` | `Ttc19` only |
| `Cox5a` | `Cox5a` only |
| `Ndufs2` | `Ndufs2` only |
| `Ndufs8` | `Ndufs8` only |
| `Sdha` | `Sdha` only |
| `Uqcrq` | `Gpr180` only |
| `Uqcrfs1`, `Uqcrb` | no focal FDR < 0.05 genes |

`Uqcrc2` is the closest assayed complex-III core paralogue/homologue. Its only focal `pvals_adj < 0.05` row was `Uqcrc2` itself (`logfoldchanges = -0.576`, `pvals_adj = 0.002997`), and the next focal genes were far from significant.

### Same-experiment report layer

The packaged Uqcrc2 report interpreted the same experiment as a complex-III buffering pattern rather than a Uqcrc2-only accident:

- `Uqcrc2:F001`: Uqcrc2 produced no robust downstream single-gene DE in any measured neuronal group.
- `Uqcrc2:F002`: canonical ATF4/ISR, UPRmt-like, protease/chaperone, redox, and mitophagy sentinel genes were absent after Uqcrc2 perturbation at FDR < 0.10.
- `Uqcrc2:F003`: represented complex-III relatives `Uqcrb`, `Uqcrfs1`, `Uqcrh`, `Uqcrq`, `Cyc1`, and `Ttc19` each had only 0-1 downstream genes in Uqcrc2-matched groups.
- `Uqcrc2:F004`: `Opa1` can activate the mitochondrial ATF4/ISR marker set in the same assay, so the complex-III flatness is not a generic inability of this snRNA-seq workflow to detect mitochondrial stress.

The bottom-up Claim `claim:34681374c398d1920b0b` summarizes those findings as: represented respiratory complex III components are largely transcriptionally buffered in neuronal nuclei and do not induce a shared complex-III depletion RNA signature.

## Forecast

I put Uqcrc1 with the buffered structural complex-III comparators, not with the `Opa1` mitochondrial-stress pattern. The focal reach measurement makes the transcript observable, but the partial functional-stock call and the measured Uqcrc2/Cyc1/Uqcrfs1/Uqcrb/Uqcrq/Ttc19 pattern argue for zero broad downstream DEGs over 21-28 days.

Because `n_degs` includes the target transcript itself and several comparably quiet OXPHOS perturbations landed at exactly one self hit, I assign one total FDR < 0.05 gene as the point forecast rather than zero. I treat 0-1 as the main uncertainty band and counts above a few genes as unlikely.

Predicted `n_degs`: 1
