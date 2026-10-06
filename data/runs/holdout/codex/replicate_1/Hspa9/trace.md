# Evidence and reasoning

## Target and endpoint

- Target: `Hspa9`.
- Focal cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes in the focal class with BH-adjusted Wilcoxon `p < 0.05`.
- Declared training table: 1,674 non-held-out perturbations for the same endpoint.
- The held-out `Hspa9` signature and `Hspa9` DEG count were absent from the declared training table and Parquet.

## Biology prior for Hspa9

- The declared biology bundle places HSPA9 at the mitochondrial import and matrix proteostasis step: mitochondrial HSP70 supports import, folding, complex assembly, quality control, and Fe-S machinery.
- Exact target-expression reach was nonzero but not ubiquitous in the focal class: `Hspa9` RNA was detected in 10,522 of 23,679 non-target nuclei, 44.436%, with mean CP10K 0.393 and pseudobulk CPM 40.970.
- Functional-stock adjudication called the P16-to-P37/P44 window only `partially_depleted_or_leading_edge`: editing should stop new HSPA9 production, but pre-edit mitochondrial HSPA9 can persist, and no matched juvenile-thalamus half-life was available.
- Postnatal neural sensitivity was plausible from mouse evidence, but the closest phenotype was lifelong heterozygosity in another neural system, not acute biallelic thalamic CRISPR. I treated this as support for possible observability, not as a high-count forecast.

## Same-endpoint training measurements

The `151 TH Prkcd Grin2c Glut` count table was highly zero-inflated:

- 1,205 / 1,674 training perturbations had `0` DEGs.
- 1,481 / 1,674 had `0` or `1` DEG.
- 106 / 1,674 had at least `10` DEGs.
- 59 / 1,674 had at least `50` DEGs.

The nearest assayed mitochondrial operations to HSPA9 were almost all silent in this exact class:

| training target | relationship to HSPA9 biology | 151 n_degs |
|---|---:|---:|
| `Dnajc19` | TIM23/PAM import motor neighbor | 0 |
| `Nfs1` | Fe-S biogenesis | 0 |
| `Aco2` | Fe-S/TCA client | 0 |
| `Abcb7` | Fe-S export-adjacent | 0 |
| `Isca2` | Fe-S biogenesis | 1 |
| `Lyrm4` | Fe-S biogenesis | 0 |
| `Mecr` | mtFAS / lipoate-adjacent | 0 |
| `Clpx` | HSPA9-linked ClpXP axis | 0 |
| `Clpp` | HSPA9-linked ClpXP axis | 0 |
| `Lonp1` | mitochondrial matrix protease | 0 |
| `Afg3l2` | mitochondrial protease | 0 |
| `Yme1l1` | mitochondrial protease | 0 |
| `Agk` | mitochondrial inner-membrane / TIM22-adjacent | 0 |
| `Opa1` | mitochondrial stress branch | 37 |

The positive stress controls showed that the focal population can respond, but their states were not close direct analogs of HSPA9 depletion:

| training target | response state | 151 n_degs |
|---|---:|---:|
| `Hspa5` | ER BiP / UPR arm | 5 |
| `Hspa8` | cytosolic HSP70 counterinduction | 9 |
| `Hsf1` | HSP90/HSP110 maintenance | 6 |
| `Nrf1` | noncanonical mitochondrial/proteostasis transcription factor response | 138 |
| `Atp2a2` | ER calcium / ATF4-like stress | 187 |
| `Gfpt1` | ER-load/glycosylation stress | 311 |
| `Dhdds` | ER-load/dolichol stress | 116 |
| `Sec63` | BiP-cycle ER stress | 11 |
| `Manf` | ER client-handling stress | 3 |
| `Uba5` | UFMylation/proteostasis stress | 2677 |
| `Ufc1` | UFMylation/proteostasis stress | 572 |
| `Psmb4` | core proteasome stress | 742 |
| `Psmc1` | core proteasome stress | 430 |

I used the large ER, UFMylation, and proteasome counts only as evidence that broad stress programs are measurable in `151`, not as magnitude donors: those operations perturb different compartments or core cytosolic quality-control machinery and would overstate an acute HSPA9 perturbation with residual mitochondrial protein stock.

## Same-experiment corpus context

The same-experiment corpus did not contain an `Hspa9` report or claim, so it did not provide a direct held-out analog. Its packaged interpretations of related training perturbations supported the count-table pattern:

- Represented mitochondrial carbon-entry, PDC, TCA, and Fe-S perturbations generally lacked a coherent postmitotic neuronal nuclear DE module.
- Single-gene Fe-S/ISC and iron-homeostasis perturbations did not form a shared neuronal iron-sulfur or iron-stress module.
- `Dnajc19` loss was globally transcriptome-buffered, and represented DNAJ-family or proximal mitochondrial comparators did not phenocopy it.
- `Clpx` and `Clpp` were flat or near-flat and did not show a generic ClpXP/UPRmt response.
- `Opa1` was the main mitochondrial exception, producing a branch-specific ISR-like response that was explicitly not a generic consequence of perturbing represented mitochondrial targets.

I treated these report/Claim summaries as interpretation of the same training experiment, not independent replication.

## Profile comparison

I also compared the selected mitochondrial, chaperone, ER-stress, UFMylation, and proteasome perturbations directly in the declared Parquet after filtering to `151 TH Prkcd Grin2c Glut`.

- The 27-node comparison contained no missing profiles.
- Twelve of the 27 selected comparators had no significant 151 feature; five had 1-9 features; two had 10-49; eight had at least 50.
- The proximal zero-count nodes such as `Dnajc19` and `Nfs1` had no significant feature overlap with the other retained candidates.
- Across all 351 selected pairs, the positive-tail overlap was weak; the mean top-tail overlap coefficient was 0.074 and the median was 0.070. Thus the observed profiles did not reveal a cohesive low-level HSPA9-like mitochondrial module masked by target names.

## Forecast

The proximal training evidence centers at zero: `Dnajc19`, `Nfs1`, Fe-S/OXPHOS-adjacent, ClpXP, and mitochondrial-protease perturbations were almost all `0` in the exact focal class. That strongly outweighed the large counts from `Nrf1`, ER stress, UFMylation, and proteasome damage, because those were different stress states.

I still placed `Hspa9` slightly above a strict zero because it is the mitochondrial HSP70 motor itself, is expressed in 44.4% of focal non-target nuclei, has continuous import/folding demand, and should lose at least the leading edge of newly synthesized functional stock over 21-28 days. Residual imported HSPA9 protein, survivor conditioning, and the lack of a shared acute mitochondrial nuclear-RNA program pulled the estimate back into the low-single-digit range.

Predicted `n_degs`: **3**.
