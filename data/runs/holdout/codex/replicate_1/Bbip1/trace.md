# Bbip1 n_degs forecast

## Target and endpoint

- Holdout manifest target: `Bbip1`.
- Requested context: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with `pvals_adj < 0.05` in the focal thalamic class.

## Biology prior used

The canonical Bbip1 bundle makes functional loss plausible in the screen window but does not make a broad RNA response obligatory.

- `Bbip1` is expressed in the exact assayed non-target population: 16,951 / 23,679 focal nuclei express it, with mean 0.933 CP10K, mean raw 1.445 UMI, and pseudobulk CPM 90.55.
- BBIP1/BBS18 is an obligate scaffold-like BBSome component that contacts BBS4 and BBS8/TTC8.
- The adjudicated stock prior was `likely_substantially_depleted` by P37-P44 because a P16 edit stops new BBIP1 supply to a dynamic BBSome trafficking complex; the caveats were that pre-edit complexes can persist initially and no endogenous neuronal BBIP1 degradation half-life was found.
- Congenital mouse evidence supports postnatal neuronal ciliary-cargo consequences in hypothalamic and hippocampal neurons, but the matched thalamic P16 edit-to-effect timing and the basal nuclear RNA endpoint were not directly established.

I therefore treated `Bbip1` as a reachable BBSome perturbation, not as a failed or absent target, but expected its best quantitative analogs to be other BBSome/ciliary-trafficking perturbations rather than globally strong transcriptional regulators.

## Same-experiment quantitative anchors

The training count table for this cell class has 1,674 targets. It is highly zero-inflated: median `n_degs = 0`, 469 / 1,674 have at least one DEG, 106 have at least 10, and 43 have at least 100. The mean is 14.05 only because of a long high-response tail.

Closest represented BBSome/BBSome-regulator anchors in the focal count table were essentially null:

| target | role | 151 TH `n_degs` |
|---|---:|---:|
| `Bbs5` | core BBSome subunit | 0 |
| `Ttc8` | BBSome/BBS8 subunit | 1 |
| `Lztfl1` | BBSome trafficking regulator | 0 |

The single `Ttc8` hit was the `Ttc8` transcript itself, not a downstream marker. In the focal Parquet slice:

| target | significant genes | minimum adjusted p | self-transcript row |
|---|---:|---:|---|
| `Bbs5` | 0 | 0.220 | `Bbs5` LFC -0.425, FDR 1 |
| `Ttc8` | 1 | 3.07e-05 | `Ttc8` LFC -0.663, FDR 3.07e-05 |
| `Lztfl1` | 0 | 0.195 | `Lztfl1` LFC -0.406, FDR 1 |

Broader ciliary transport and transition-zone anchors were also null in the same count table: `Ift43`, `Ift81`, `Ift88`, `Dync2h1`, `Dync2i1`, `Kif3b`, `Cep290`, `Rpgrip1l`, and `Pkd1` all had 0 focal-class DEGs. In the same Parquet slice, 11 / 12 selected BBSome/IFT/ciliary anchors had zero FDR < 0.05 genes; only `Ttc8` had one.

## Profile and corpus checks

The profile comparison over the 12 selected ciliary anchors used the `151 TH Prkcd Grin2c Glut` Parquet rows, Wilcoxon `scores` as signed profiles, and `pvals_adj < 0.05` as the significance column. It found no missing profiles, 66 / 66 pairwise observations, 11 nodes with no significant features, and one node with 1 to 9 features.

The focal BBSome/BBS-regulator rows did not show a hidden shared signed program with the wider ciliary set:

- For 27 Bbs5/Ttc8/Lztfl1 versus IFT/dynein-2/transition-zone/ciliary peers, every positive and negative FDR-significant program intersection was 0.
- Whole-profile Pearson/cosine values were small. The largest among those 27 comparisons was `Lztfl1` versus `Ift88`, Pearson 0.104 and cosine 0.101; most absolute correlations were far lower.
- Across all 66 ciliary pairs, the median top-tail overlap coefficient was 0.01 for positive tails and 0.02 for negative tails, with no significant-program overlap.

The report corpus had no `Bbip1` report entry or direct Bbip1-to-Bbs5/Ttc8 Finding edge, so I did not treat it as target-specific measurement. It did independently confirm that the measured BBS/ciliary anchor cohort is biologically curated rather than a name-only grouping: the 12 chosen targets formed one dense explicit-reference component, and Bbs5/Ttc8/Lztfl1 reports describe a flat or singleton-only BBSome/IFT/transition-zone response landscape. Those statements are summaries of the same Perturb-seq experiment, so they supported interpretation of the measured rows but were not counted as replication.

## Forecast

The biology bundle argues against a hard zero from absent target engagement: Bbip1 is expressed in the focal population, the BBSome is dynamic, and loss should matter for ciliary trafficking by harvest. The training data argue that this kind of defect usually does not appear as a basal postnatal neuronal nuclear-RNA DEG burden. The closest focal rows, `Bbs5` and `Lztfl1`, were both zero; `Ttc8` contributed only a self-transcript hit; and the broader IFT/dynein/transition-zone rows were all zero.

`Bbip1` could gain a single DEG if its own nuclear transcript is significantly reduced, but self-transcript FDR is inconsistent even among nearby ciliary anchors and is not evidence for a downstream BBSome response. With no matched evidence for a recurrent BBSome mRNA module and no matched Bbip1 timing data that would push beyond the Bbs5/Ttc8/Lztfl1 scale, I chose the mode of the direct anchors:

`predicted_n_degs = 0`.
