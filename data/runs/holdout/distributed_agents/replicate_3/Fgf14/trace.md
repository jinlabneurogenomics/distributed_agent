# Fgf14 DEG-count prediction

## Question and resolved ambiguities

The requested held-out perturbation file contains one target:

```tsv
target_name
Fgf14
```

I interpreted the endpoint as the exact training CSV endpoint: for a perturbation target, count all measured genes with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`, including the targeted transcript itself when it passes the FDR threshold. The focal cell label is an Allen-style class label for thalamic glutamatergic neurons; `TH` is thalamus, not tyrosine hydroxylase.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`, the focal-cell training endpoint for 1,674 non-held-out perturbations.
- `[local file: training_de_all_cell_groups.parquet]`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` to inspect exact FDR-significant genes, target-transcript rows, and score correlations among Fgf14 analogs.
- The run-local Distributed Agents same-experiment semantic corpus `perturbai-july-260713-sourceguard-1773-v1`. `Fgf14` itself had no packaged Findings or Claims in this release, so I used the corpus for represented comparators such as `Fgf12`, `Fgf13`, `Scn1a`, `Scn1b`, `Scn2a`, `Scn8a`, `Kcnq2`, `Kcnq3`, and `Cacna1g`.
- PubMed-indexed external literature on FGF14/FHF4 and intracellular FGF biology:
  - Goldfarb et al. 2007, Neuron, DOI `10.1016/j.neuron.2007.07.006`, PMID `17678857`: FHF1/FHF4 proteins modulate voltage-gated sodium-channel inactivation and neuronal excitability.
  - Bosch et al. 2015, Journal of Neuroscience, DOI `10.1523/JNEUROSCI.2663-14.2015`, PMID `25926453`: acute adult Purkinje-cell Fgf14 knockdown impairs spontaneous and evoked firing and motor coordination without requiring developmental loss.
  - Pellerin et al. 2022, New England Journal of Medicine, DOI `10.1056/NEJMoa2207406`, PMID `36516086`: intronic FGF14 GAA repeat expansions cause late-onset cerebellar ataxia and reduce FGF14 RNA/protein in patient tissue/models.

## Local computations

I first read the focal training count table and selected biologically motivated Fgf14 comparators rather than using all FGF symbols together. The important split is between secreted/receptor FGF signaling (`Fgf1`, `Fgfr1`, `Fgfr2`, `Fgfr3`, `Fgfrl1`) and the intracellular FGF homologous factors, or FHFs (`Fgf12`, `Fgf13`, held-out `Fgf14`), which regulate neuronal ion-channel physiology.

For exact expression evidence I filtered the parquet with:

```python
filt = (
    ds.field("group_name") == "151 TH Prkcd Grin2c Glut"
) & ds.field("gene_target").isin(candidate_targets)
```

and counted `pvals_adj < 0.05`, extracted the significant rows, extracted self-transcript rows, and computed pairwise Pearson correlations over the signed Wilcoxon `scores` vector across 17,259 measured genes in the focal class.

The local endpoint counts for the main comparators were:

| comparator | focal `n_degs` | focal expression-pattern evidence |
| --- | ---: | --- |
| `Fgf12` | 0 | No FDR 0.05 genes; the target transcript was weakly lower but not significant, log2FC -0.223, `pvals_adj = 1`. The Distributed Agents corpus describes a singleton `Nmnat2` response in a different TH group, not this focal group. |
| `Fgf13` | 2 | Only `Fgf13` itself and `Rell2` were significant in 151 TH. The self transcript had log2FC -0.894 and `pvals_adj = 4.39e-12`; `Rell2` had log2FC -0.374 and `pvals_adj = 0.0398`. |
| `Scn1a` | 1 | Self transcript only; log2FC -1.075, `pvals_adj = 5.87e-38`. |
| `Scn1b` | 2 | Self transcript plus `Jun` up; `Scn1b` log2FC -1.436, `pvals_adj = 7.36e-70`; `Jun` log2FC 0.518, `pvals_adj = 0.0156`. |
| `Scn2a` | 1 | Self transcript only; log2FC -0.401, `pvals_adj = 6.46e-6`. |
| `Scn3a` | 0 | No focal FDR genes; the self transcript was unchanged, log2FC 0.099, `pvals_adj = 1`. |
| `Scn8a` | 1 | Self transcript only; log2FC -0.458, `pvals_adj = 1.34e-5`. |
| `Kcnq2` | 1 | Self transcript only; log2FC -0.776, `pvals_adj = 2.12e-28`. |
| `Kcnq3` | 1 | Self transcript only; log2FC -0.379, `pvals_adj = 0.00717`. |
| `Cacna1g` | 12 | A real but small thalamic calcium-channel signature with `Cacna1g` self-down and genes such as `Ptprn`, `Stmn4`, `Cpne7`, `Jun`, `Zdhhc22`, `Lrrc7`, `Notum`, `Serpine2`, and `Iyd`. This is a useful positive channel counterexample, but the same corpus reports it is Cav3.1-selective and not a generic ion-channel response. |
| `Fgf1`, `Fgfr1`, `Fgfr2`, `Fgfr3`, `Fgfrl1` | 0, 0, 0, 0, 0 | Secreted FGF/FGFR symbols were flat in the focal count table and are mechanistic boundaries, not close Fgf14 analogs. |

The focal whole-score correlations among `Fgf12`, `Fgf13`, `Scn1a`, `Scn1b`, `Scn2a`, `Scn3a`, and `Scn8a` were all weak: `Fgf12` versus `Fgf13` was `r = 0.0105`; `Fgf13` versus the Nav targets ranged from `r = -0.0096` to `0.0404`; the largest pair in this set was `Scn1b` versus `Scn8a`, `r = 0.1144`. There was no same-direction FDR-level shared response among those FHF/Nav comparators in the focal group. The `Scn1b`/`Cacna1g` pair shared `Jun`, but in opposite directions, so I treated `Cacna1g` as a detectable thalamic-channel counterexample rather than as a template for Fgf14.

As a guard against the possibility that `Fgf14` was simply absent as a measured RNA feature, I also filtered `names == "Fgf14"` in the focal parquet. `Fgf14` had one upstream perturbation with an FDR 0.05 effect in the 1,674-profile focal training set (`Zbtb7a`, log2FC -0.271, `pvals_adj = 0.0365`), confirming that the feature is represented in the measurement matrix even though the `Fgf14` perturbation was held out.

## Target-specific reasoning

### `Fgf14`

External knowledge makes `Fgf14` a member of the intracellular FHF/Nav axis, not the receptor-FGF branch. FGF14/FHF4 binds and tunes voltage-gated sodium-channel function; FHF loss shifts Nav inactivation and alters granule-cell firing in mouse cerebellum (Goldfarb et al. 2007), and acute Fgf14 knockdown in adult Purkinje neurons is sufficient to reduce firing and impair motor coordination (Bosch et al. 2015). Human intronic `FGF14` repeat expansions that reduce FGF14 RNA/protein cause SCA27B late-onset ataxia (Pellerin et al. 2022). These observations argue that `Fgf14` loss is biologically meaningful, but mainly through membrane excitability and axon-initial-segment/channel physiology.

The within-dataset evidence says that this kind of mechanism usually does not become a broad nuclear RNA state after sparse P16 CRISPR loss. The closest represented FHF, `Fgf13`, had only two focal DEGs, one of them the self transcript. `Fgf12` was completely flat in this focal thalamic group. Directly knocking out represented Nav alpha or beta genes in the same focal class generally produced only the target transcript itself (`Scn1a`, `Scn2a`, `Scn8a`) or the target plus one downstream marker (`Scn1b`). `Kcnq2` and `Kcnq3`, another axon-initial-segment/excitability channel pair, were also self-only. The same-experiment corpus explicitly warns that represented Nav-channel subunits and intracellular FHF perturbations were sparse and target-specific rather than a shared pan-Nav mRNA module; it also separates FHF perturbations from secreted FGF/FGFR perturbations. That matches the focal parquet: FHF/Nav score correlations were near zero and did not share FDR genes.

The nonzero part of the prediction is driven mostly by the focal training signatures themselves. Several channel comparators with no real downstream state still contributed one counted DEG through a significant self-transcript decrease. `Fgf13` did so very strongly in 151 TH, and `Fgf14` is a measurable gene in this focal group. I therefore do not predict an all-zero Fgf14 surface. The count is kept at one because neither Fgf13, Fgf12, the Nav subunits, nor KCNQ subunits justify a Cacna1g-like dozen-gene thalamic response; `Cacna1g` is a selective T-type calcium-channel exception rather than the local behavior of FHF/Nav loss.

Point prediction:

```tsv
target_name	predicted_n_degs
Fgf14	1
```

## Limits

- `Fgf14` had no direct Distributed Agents corpus Finding in `perturbai-july-260713-sourceguard-1773-v1`, so all same-experiment semantic evidence is transferred from represented relatives.
- `Fgf12` and `Fgf13` are the closest available FHF training perturbations, but `Fgf14` is not interchangeable with either: it has distinct expression, isoforms, channel-gating effects, and prominent cerebellar biology.
- The true hidden `Fgf14` target-transcript p-value could land on either side of the FDR threshold. The prediction of one DEG depends on target RNA being detectable and depleted enough in recovered 151 TH nuclei.
- The assay reads survivor-conditioned nuclear RNA 3 to 4 weeks after sparse postmitotic editing. It will miss fast electrophysiologic defects, altered Nav localization, and circuit effects that do not settle into a constitutive mRNA state.
- The matched perturbed-cell counts vary by target in training, and the hidden `Fgf14` power is unknown. I therefore used the DEG count pattern only for coarse calibration rather than fitting a count model.
