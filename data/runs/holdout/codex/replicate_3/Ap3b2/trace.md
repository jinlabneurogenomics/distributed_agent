# Ap3b2 direct focal DEG-count forecast

Target: `Ap3b2` in `151 TH Prkcd Grin2c Glut`.

## Biology prior

The declared `Ap3b2` biology bundle contained no target outcome, but it did make a realized perturbation plausible in the focal population:

- Exact non-target reach in `151 TH Prkcd Grin2c Glut`: `Ap3b2` was detected in 22,147 of 23,679 non-target nuclei, or 93.530%, with mean CP10K 2.180 and mean log1p(CP10K) 1.066.
- The functional-stock card adjudicated AP3B2 as a dynamic neuronal AP-3B beta3B coat-complex component whose supply should substantially decline over the 21-28 days from P16 editing to P37-P44 harvest, while preserving uncertainty about a stabilized residual pool.
- The observability card supported a postnatal mouse-neural requirement: AP3B2 loss has direct mouse neural and synaptic-vesicle cargo phenotypes, and the ubiquitous beta3 paralog `Ap3b1` does not fully replace beta3B-dependent AP-3 localization or selected synaptic cargo targeting in mouse neurons.

Those points make a silent assay failure less likely, but they do not imply a broad nuclear RNA response: AP3B2 is a selective synaptic-vesicle cargo adaptor, not a transcriptional regulator, and the curated phenotype evidence is mostly germline or forebrain/cortical rather than an acute P16 thalamic snRNA-seq perturbation.

## Training endpoint context

The visible focal count table has 1,674 training perturbations. It is highly zero-inflated:

- 1,205/1,674 training targets have `n_degs = 0`.
- 276/1,674 have `n_degs = 1`.
- median `n_degs = 0`; 75th percentile = 1; 90th percentile = 2.
- the mean, 14.05, is pulled upward by a small long tail of strong splicing, proteasome, transcriptional, and endosomal/lysosomal responses.

The deterministic analog nomination placed only `Ap3b1` in the exact-complex/paralog tier for `Ap3b2` within the training universe. Its focal endpoint was 0 DEGs. The next AP-3/BLOC or nearby cargo-sorting anchors also stayed near zero in the same `151 TH Prkcd Grin2c Glut` endpoint:

| perturbation | typed role used here | focal `n_degs` |
| --- | --- | ---: |
| `Ap3b1` | beta3 paralog / AP-3 adaptor-complex comparator | 0 |
| `Dtnbp1` | BLOC-1 / AP-3-adjacent cargo-sorting comparator | 0 |
| `Vps41` | HOPS / AP-3 late-endosome boundary | 0 |
| `Ap1s2` | AP/clathrin coat boundary | 0 |
| `Ap1b1` | AP/clathrin coat boundary | 1 |
| `Kif1a` | anterograde synaptic-vesicle transport boundary | 1 |
| `Kif1b` | anterograde transport boundary | 0 |
| `Synj1` | synaptic-vesicle recycling boundary | 1 |
| `Dnm1` | synaptic-vesicle endocytosis boundary | 1 |
| `Cltc` | broad clathrin endocytosis boundary | 3 |

The selected same-experiment corpus also supported this as a real local quiet branch rather than an isolated `Ap3b1` miss: reciprocal `Ap3b1` and `Dtnbp1` findings contributed to a moderate Claim that represented AP-3/BLOC-related or adjacent perturbations share a buffered juvenile neuronal transcriptomic outcome without an acute nuclear compensation program. That Claim explicitly does not test `Ap3b2`, so I used it only as a local training prior, not as target evidence.

I also inspected the matched focal expression profiles for `Ap3b1`, `Dtnbp1`, `Kif1a`, `Ap1s2`, `Synj1`, `Kif1b`, `Cltc`, `Dnm1`, `Vps41`, and `Ap1b1`. All ten profiles were present; five had no FDR<0.05 features and five had only 1-9. The exact AP-3/BLOC-adjacent nodes `Ap3b1`, `Dtnbp1`, `Ap1s2`, and `Vps41` were all 0, while the broader endocytosis and AP-1/clathrin comparators were 1-3.

## Synthesis

I discounted high lysosomal/endosomal outliers such as `Rab7` because the `Ap3b1` report itself separates beta3A AP-3 cargo selection from the late-endosome/lysosome-fusion failure program: `Rab7` was a dominant broader comparator, while `Vps41`, `Atp6v1a`, and the direct AP/BLOC anchors were sparse or silent. I likewise treated the `Kif1a`/`Kif1b` motor pair as a nearby synaptic-vesicle-transport boundary rather than an AP-3B subunit analogue.

My point estimate is therefore a near-null but not hard-zero response. The focal training measurements say the closest measured AP-3/BLOC cargo-sorting perturbations most often produce 0 DEGs, but high `Ap3b2` expression and incomplete paralog buffering make it slightly more plausible than `Ap3b1` to register one marginal downstream gene. I predict `n_degs = 1`.
