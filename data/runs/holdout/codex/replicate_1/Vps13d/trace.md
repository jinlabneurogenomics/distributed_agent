# Direct forecast for Vps13d in 151 TH Prkcd Grin2c Glut

## Target and endpoint

- **Manifest target:** `Vps13d`, from the declared one-row holdout manifest.
- **Endpoint:** `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.
- **Outcome blindness:** `Vps13d` was absent from the 1,674-row declared training count table; no Vps13d expression signature or Vps13d DEG count was available in the declared training Parquet.

## Target biology used

The declared canonical Vps13d biology bundle was used in `biology` view only. It says the exact focal-population baseline reach is high: `Vps13d` is detected in 20,815 of 23,679 non-targeting 151 TH nuclei, `87.9049%`, with mean raw UMI `2.5206` and pseudobulk CPM `157.974`.

The same bundle supports a real perturbation prior rather than treating the edit as invisible: VPS13D supports mitochondrial fission/clearance and peroxisome biogenesis at organelle contacts, postnatal conditional mouse neural loss has mitochondrial abnormalities by six weeks, and the stock adjudication calls harvest-time functional stock `likely_substantially_depleted`. I treated this as upward evidence for at least a small transcriptional response in the 21-28 day P16-to-P37/P44 window. The caveats are substantial: VPS13D protein half-life in juvenile thalamic neurons is unknown, pre-existing organelles can persist, the closest mouse phenotype is forebrain rather than thalamus, and survivor conditioning can attenuate a nuclear-RNA signature if badly perturbed neurons are depleted before capture.

## Training-scale evidence

The focal training count table is highly zero-inflated:

- 1,674 training targets.
- 1,205 targets with `n_degs = 0`.
- Median `n_degs = 0`; mean `14.05`.
- 1,481 targets, or `88.5%`, had `n_degs <= 1`.
- A small number of broad stress perturbations dominate the right tail, with `Rab7 = 501`, `Opa1 = 37`, `Vps35 = 17`, and `Vps54 = 31` among biologically adjacent endomembrane or mitochondrial anchors.

I nominated Vps13d analogs against the actual training universe with the deterministic gene-analog skill. That returned 166 training-available nominees, all in the weakest `broad_functional_fallback` tier. No exact complex, exact paralog, narrow-module, direct-interaction/dependency, or reciprocal same-corpus comparator was available, so I treated these as weak scale bearings rather than direct donors.

The strongest annotated lipid-transfer and autophagy nominees were mostly silent in the declared count table:

| training target | relationship to Vps13d prior | `n_degs` |
|---|---:|---:|
| `Vps13a` | phospholipid/intermembrane lipid transfer, VPS13-family | 0 |
| `Vps13c` | phospholipid/intermembrane lipid transfer, VPS13-family | 0 |
| `Mttp` | phospholipid/intermembrane lipid transfer | 0 |
| `Abca1` | phospholipid transfer | 0 |
| `Abca7` | phospholipid transfer | 0 |
| `Slc25a4` | positive regulation of mitophagy | 1 |
| `Nod2` | positive regulation of mitophagy | 0 |
| `Stub1` | positive regulation of mitophagy | 1 |
| `Atg5` | macroautophagy | 0 |
| `Becn1` | macroautophagy/endosome membrane | 0 |
| `Atg16l1` | macroautophagy/endosome membrane | 0 |
| `Vps41` | macroautophagy/endosome membrane | 0 |

Additional hand-checked curated sets matched the same pattern. The represented peroxisome-organization targets had `Abcd3 = 0` and `Pex14 = 1`. Positive-mitophagy targets excluding the held-out `Vps13d` had `Nod2 = 0`, `Slc25a4 = 1`, and `Stub1 = 1`; `Prkn` was not in the count table. Positive mitochondrial-fission targets were mostly null (`Ddhd1 = 0`, `Ddhd2 = 0`, `Kdr = 0`, `Mff = 0`, `Rala = 0`) with `Vps35 = 17` as a modest exception.

## Same-experiment corpus checks on training targets

I used the July sourceguard corpus only for visible training perturbations, not to query a Vps13d report. The packaged Vps13a/Vps13b/Vps13c Findings and their shared Claim report that the represented VPS13 single-gene perturbations were flat or non-phenocopying in this acute juvenile neuronal assay; in the focal count table all three are exactly zero. Those records also emphasize a boundary I kept: Vps13d itself was absent from those represented-family comparisons, so the Vps13a/b/c nulls are downward training evidence, not a measured Vps13d result.

The corpus provided two positive boundaries. `Rab7` anchors a late-endosomal/lysosomal compensation state with recurrent lysosomal, sterol, ISR/UPR, amino-acid, autophagy, redox, and proteasome transcripts and is very large in 151 TH (`501` DEGs). `Opa1` anchors a mitochondrial ATF4/ISR-like stress program detectable in this assay, but its 151 TH count is only `37`, and many represented mitochondrial comparators cited against Opa1 are null. `Vps35` is a modest, branch-specific retromer response in this same 151 TH class rather than a generalized lysosomal program.

## Profile check

I symmetrically compared the leading 30 Vps13d nominees in the declared 151 TH Parquet rows using `gene_target` x `names` signed log-fold-change profiles and `pvals_adj < 0.05`. The profile comparison found all 30 profiles but the activity distribution was still sparse:

- 15 of 30 had no significant features.
- 10 of 30 had 1-9 significant features.
- 4 of 30 had 10-49 significant features.
- 1 of 30 had at least 50 significant features.

The cohort diagnostic over all 435 pairs did not reveal a coherent high-count module: median positive top-tail overlap was `0.04`, median negative top-tail overlap was `0.08`, and median significant-program overlap was zero in both directions. This made `Rab7`'s 501-count lysosomal profile an outlier rather than a quantitatively transferable proxy for Vps13d.

## Numeric synthesis

The closest visible measurements argue for a very small forecast: Vps13a/Vps13b/Vps13c were `0`, the highest-priority lipid-transfer nominees were all `0`, and the specific peroxisome/mitophagy/fission sets were mostly `0` or `1`. I did not choose a hard zero because the target itself is more broadly expressed in the exact focal class than a missing-reach target, VPS13D has a postnatal mouse neuronal phenotype that is stronger than the represented VPS13-family nulls, and the training atlas can detect a small-to-modest organelle stress state after Opa1 or Vps35 perturbation.

Balancing those bearings, I forecast a single-digit but nonzero response: **3 DEGs**.
