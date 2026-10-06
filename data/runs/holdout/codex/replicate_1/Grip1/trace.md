# Direct forecast trace

## Target and endpoint

- Target: `Grip1`.
- Focal cell group: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes in this cell group with BH-adjusted Wilcoxon `p < 0.05`.
- Declared endpoint inputs: `Grip1` is absent from the 1,674-row 151-count training table and from the declared training Parquet profiles, so no target expression signature or target DEG count was used.

## Target biology used

The declared `Grip1` biology bundle identifies the perturbation as loss of the nuclear receptor coactivator Ncoa2/GRIP1 in postmitotic thalamic neurons after a P16 edit and P37-P44 harvest. Exact focal-population expression is present but not broad: the bundle reports `Grip1` expression in 10,194 of 23,679 non-target 151-class nuclei, 43.0508% of cells, with mean raw UMI 0.6396 and mean log1p CP10k 0.2704.

The same bundle supports a likely within-window decline of the functional coactivator pool because Ncoa2/GRIP1 is a dynamic transcription-complex component whose new supply is cut off by editing. This was weak direct evidence for any 151-class RNA response rather than a strong response prior, because the source facts are dominated by systemic mouse phenotypes and heterologous turnover data. The bundle explicitly leaves postnatal thalamic dependence, latency, survivor conditioning, and compensation by related p160 coactivators unresolved.

## Training perturbations that determined the point

I first used the 151-class training count table as the endpoint-matched evidence source.

Closest p160 and nuclear-receptor/coactivator comparators:

| training target | reason for comparison | 151 n_degs |
| --- | --- | ---: |
| `Ncoa1` | p160/SRC coactivator paralog, strongest family comparator available in the count table | 0 |
| `Ncoa3` | p160/SRC coactivator paralog represented in training | 0 |
| `Rxra` | high-priority nuclear-receptor module candidate from typed analog nomination | 0 |
| `Ep300` | CBP/p300 coactivator/chromatin comparator nominated near the same receptor-coactivator biology | 0 |
| `Esr1` | exact-complex candidate through projected ESR1-GRIP1-JUN CORUM evidence | 0 |
| `Ppara` | PPAR nuclear-receptor module candidate | 0 |
| `Pparg` | nuclear-receptor module candidate | 0 |
| `Ahr` | nuclear-receptor/AHR binding module candidate | 0 |
| `Arnt` | AHR/HIF nuclear cofactor module candidate | 0 |
| `Crebbp` | broader acetyltransferase coactivator fallback, active but not p160-specific | 8 |
| `Thra` | ligand-dependent nuclear receptor in the same 151 class | 3 |
| `Rora` | active nuclear receptor in the same 151 class, but a direct DNA-binding TF rather than a p160 coactivator | 278 |

The typed analog nominator placed `Ncoa1` near the top of the complete available-pool retrieval and recovered many receptor and coactivator links for `Grip1`; its priority was used only to inspect plausible training comparators. It did not provide an endpoint score or weight. After merging the nominated candidates with the count table, most of the leading receptor/coactivator candidates were 151-null: ranks 1, 2, 4-10, 12, and 14-20 among the analog receipt had `n_degs` of 0 or 1 except for broad fallback outliers `Bmal1` and `Ctnnb1`.

The same-experiment corpus had no `Grip1` report, so it did not expose the held-out target outcome. It did have reports for the two represented p160 paralogs: `Ncoa1` produced only one corrected downstream event outside 151 at FDR < 0.10, was exactly flat in 151, and had no meaningful transcriptome-wide module; `Ncoa3` likewise had a single off-151 event at FDR < 0.10 and no strong whole-profile neighbors. These reports are not independent measurements of the count table, but they support the interpretation that p160 coactivator perturbations were locally buffered in this screen.

I then compared signed 151-class Parquet profiles for a small exact cohort:
`Ncoa1`, `Ncoa3`, `Ep300`, `Crebbp`, `Rora`, `Thra`, `Brd4`, `Nr1d1`, and `Med13`.
In the matched 151 profile comparison:

- `Ncoa1`, `Ncoa3`, and `Ep300` had 0 significant features at `p_adj < 0.05`.
- `Thra` had 3; `Crebbp` had 8; `Med13` had 11.
- `Nr1d1`, `Rora`, and `Brd4` had 116, 278, and 311 respectively.
- Significant-gene overlap between the small `Crebbp` response and the broad `Rora` response was 0 in both directions; `Crebbp` shared only 1 positive and 2 negative significant genes with `Brd4`.

That profile evidence argued against treating the large `Rora` or `Brd4` burdens as the conditional magnitude for `Grip1`. Their broad thalamic programs were not a shared p160/coactivator program, while the direct p160 family members and many receptor module members were zero.

## Synthesis

The target bundle makes a realized `Grip1` perturbation biologically plausible: the target is expressed in a minority-large fraction of 151 nuclei, and the Ncoa2 protein pool should decline over 21-28 days if edited. However, the realized operation is a regulatable recruited coactivator with related Ncoa1/Ncoa3 alternatives, and the strongest available endpoint-matched analogs show no 151-class DEG burden. The count distribution for the whole training table is also zero-inflated, with 1,205 of 1,674 training targets at `n_degs = 0` and a median of 0.

I therefore forecast that `Grip1` will fall on the buffered p160/receptor-cofactor side rather than on the rare broad-response side, giving a point prediction of 0 FDR-significant genes in `151 TH Prkcd Grin2c Glut`.
