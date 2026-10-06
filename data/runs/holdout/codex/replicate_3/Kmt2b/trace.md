# Kmt2b direct DEG-count forecast

## Target and endpoint

- Target manifest: `Kmt2b`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Forecast: `18`

I treated the count table and Parquet as the endpoint measurements and the July corpus as the same-experiment interpretive layer, not as independent replication. I did not use a `Kmt2b` same-experiment signature, target DEG count, endpoint-selection artifact, or labeled target outcome.

## Kmt2b biology prior

The declared canonical `Kmt2b` bundle supports an observable but delayed chromatin perturbation:

- Kmt2b is present in the exact focal population: 19,448 of 23,679 non-target `151 TH Prkcd Grin2c Glut` nuclei expressed it, with 82.13% expressing cells, 1.995 mean raw UMI, and 125.03 pseudobulk CPM. This removes target absence as a reason to forecast a strict null, while not measuring editing efficiency.
- KMT2B is an H3K4 di- and trimethylation/COMPASS-family enzyme with documented postnatal forebrain neuronal relevance, so an H3K4-writer analogue is biologically more appropriate than a generic chromatin regulator.
- The functional-stock adjudication was `partially_depleted_or_leading_edge`: P16 editing should stop new KMT2B production, and neuronal H3.3 turnover over 2-4 weeks creates a renewal front that could fail to reacquire KMT2B-dependent marks, but existing KMT2B protein and pre-edit H3K4me2/3 are not directly erased. Unknown KMT2B protein residence and methyl-mark persistence make a massive 21-28 day response less likely than an immediate loss of an unstable effector.

## Training measurements used

The declared 151 count table has 1,674 training targets. It is heavily zero-inflated:

- median `n_degs`: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- maximum: 2,677

I focused on KMT2/H3K4 and nearby chromatin regulators visible in the training table and verified their exact 151 rows in the declared Parquet:

| comparator | reason used | 151 n_degs |
| --- | --- | ---: |
| `Kmt2a` | closest measured Trithorax-family promoter H3K4 writer | 24 |
| `Kmt2c` | measured KMT2-family H3K4/enhancer writer boundary | 0 |
| `Setd1a` | SET1/MLL H3K4 writer but corpus-reported broad non-phenocopy | 368 |
| `Setdb1` | histone lysine methyltransferase with a moderate 151 footprint | 22 |
| `Nsd1` | histone lysine methyltransferase with a moderate 151 footprint | 23 |
| `Kdm5c` | H3K4-axis eraser/chromatin disease comparator | 18 |
| `Mecp2` | postnatal chromatin-reader comparator | 16 |
| `Crebbp` | chromatin coactivator boundary | 8 |
| `Dnmt3a`, `Ep300` | chromatin regulators silent in the same group | 0 |

The `Kmt2a` Parquet rows formed a real but modest 151 program headed by down-regulated `Nr2f1`, `Pcdh7`, `Lhx9`, `Camk2d`, `Pcdh10`, and `Grik2`, not just a self-target hit. The packaged `Kmt2a` report described this as a sparse, glutamatergic-biased response and reported that `Kmt2a` did not phenocopy represented H3K4 relatives: `Setd1a` was much broader and largely non-overlapping, while `Kmt2c` was nearly flat. The packaged `Setd1a` report likewise placed `Setd1a` away from measured KMT2 writers and toward RNA-biogenesis and organelle-maintenance states.

## Synthesis

`Kmt2a` received the most weight because KMT2A is the closest measured promoter H3K4 writer and its 24-gene 151 response matches the expected sign of losing an activating writer at selected neuronal identity and connectivity genes. I discounted `Setd1a` and broad chromatin responders such as `Brd4` or `Phf12` because the corpus and Parquet show that their large responses are not interchangeable with KMT2-family loss. I used `Kmt2c`, `Dnmt3a`, `Ep300`, and other zero/near-zero chromatin regulators as a boundary that H3K4 or chromatin membership alone does not guarantee an acute postmitotic response.

For `Kmt2b`, exact focal expression and postnatal neural KMT2B biology favor a nonzero footprint. Partial functional-stock depletion by P37-P44, uncertainty about thalamic transfer from forebrain evidence, and the idiosyncrasy of KMT2-family signatures argue against a broad `Setd1a`-scale count and place the point slightly below the 24-gene `Kmt2a` anchor. I therefore forecast `18`, the 151 training-table 95th percentile and a moderate rare response.
