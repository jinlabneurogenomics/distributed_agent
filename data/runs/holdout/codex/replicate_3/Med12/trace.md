# Med12 held-out DEG-count forecast

## Target and endpoint

- Target perturbation: `Med12`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in this focal thalamic glutamatergic class.

## Evidence used

The target biology bundle supports a realized perturbation but also flags dilution risk in the exact assayed population. MED12 is a dynamic Mediator kinase-module scaffold/regulatory subunit, so a P16 disruptive edit should stop new functional supply to a renewable nuclear complex. The functional-stock card judged substantial depletion by the P37-P44 harvest as likely but only partially evidenced because a native thalamic-neuron MED12 half-life was not found. The exact focal expression measurement was weak and sparse: mean CP10K 0.139 and 4,548 of 23,679 non-target `151 TH Prkcd Grin2c Glut` nuclei expressing `Med12`, or 19.2%.

The declared training count table is very sparse in this class: among 1,674 training targets the median count is 0, the 75th percentile is 1, and the 90th percentile is 2. The upper tail is real but unusual, so a high count needs a close same-endpoint reason rather than a generic transcription-regulator prior.

Typed analogue nomination put the training-available Mediator neighbors at the top. The closest direct nominees and their declared `151 TH Prkcd Grin2c Glut` counts were:

| training target | relationship to the Med12 biology bundle | n_degs |
| --- | --- | ---: |
| `Med13` | Mediator / kinase-module physical or complex neighbor | 11 |
| `Cdk8` | native Mediator complex member and kinase-module partner | 0 |
| `Med23` | Mediator complex component | 13 |
| `Med15` | Mediator complex component | 19 |
| `Med13l` | Mediator-related paralog/complex neighbor | 1 |

Other exact-complex or high-priority co-regulator nominees were mostly null in the same count table: `Rxrb`, `Ep300`, `Ncoa1`, `Sox9`, `Esr1`, `Esr2`, and `Vdr` had 0; `App` had 1 and `Thra` had 3. `Brd4` and `Ctnnb1` were much larger, at 311 and 383, but those are broader chromatin or Wnt/co-regulator states rather than equal-scale MED12 kinase-module lesions.

The focal Parquet slice for the core Mediator comparators confirmed that all five had full feature coverage in this class, with 17,259 measured genes per target. The nonzero Mediator programs were small and predominantly down-regulated: `Med13` had 10 down and 1 up, `Med23` 13 down, `Med15` 19 down, and `Med13l` 1 down, while `Cdk8` had no FDR-significant genes. The same few negative thalamic markers recurred across `Med13`, `Med23`, and `Med15`, including `Prkcd`, `Grm1`, `Pcp4`, `Plekhg1`, and `Atp2a2`.

Observed profile comparison over the direct Mediator set supported a weak common negative program, not a high-burden hidden module. Across the 10 pairwise comparisons among `Med13`, `Cdk8`, `Med23`, `Med15`, and `Med13l`, negative top-tail overlap coefficients were small but nonzero, with median about 0.20. The significant negative programs of `Med13`, `Med23`, and `Med15` shared seven to eight genes in their strongest pairings; `Cdk8` and `Med13l` contributed little FDR-level breadth. In the same comparison, `Brd4` and `Ctnnb1` shared parts of this negative tail but had hundreds of significant features, making them upper-scale context rather than point donors.

## Synthesis

I treated `Med13`, `Cdk8`, `Med23`, `Med15`, and `Med13l` as the scale-bearing training comparators because they are the available Mediator/kinase-module-centered perturbations. Their counts bracket a low response from 0 to 19 DEGs. The realized-stock evidence for `Med12` and the recurrence of the `Med13`/`Med23`/`Med15` down-program argue against a zero forecast. The weak exact `Med12` expression reach, the null `Cdk8` result, the one-gene `Med13l` result, and the off-axis nature of the 311-383 DEG `Brd4`/`Ctnnb1` states argue against borrowing a broad high-count response.

I therefore placed `Med12` below the 11-19 DEG nonzero core-Mediator band but above the null/one-gene kinase-module floor, giving a point forecast of 8 DEGs.
