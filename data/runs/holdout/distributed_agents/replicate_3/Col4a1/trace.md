# DEG-count prediction trace

## Question and endpoint

I predicted the held-out endpoint for `Col4a1` in `151 TH Prkcd Grin2c Glut`: the number of measured genes with `pvals_adj < 0.05` in the focal cell group after acute AAV-CRISPR loss of function.

Two ambiguities were resolved explicitly:

- The requested CSV contains one target, `Col4a1`, and it is absent from both supplied training tables as intended.
- The endpoint in `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` counts every measured feature passing FDR 0.05, including a perturbed target's own transcript if it passed. I did not exclude self-transcript hits when reading the count CSV, but I treated same-gene down-regulation as endpoint calibration rather than proof of downstream pathway activation.

## Sources used

- The training DEG-count CSV, `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`, for exact observed `151 TH Prkcd Grin2c Glut` counts among the 1,674 non-held-out perturbations.
- The full training DE parquet, `[local file: training_de_all_cell_groups.parquet]`, for focal-cell per-gene FDRs, matched perturbed nucleus counts, and absence of near-threshold ECM or receptor signatures.
- The selected same-experiment Distributed Agents corpus, release `perturbai-july-260713-sourceguard-1773-v1`, for curated negative findings and cross-perturbation contrasts over the exact Perturb-seq atlas.
- NCBI PubMed literature searches for COL4A1/COL4A2 and type-IV collagen biology.

External references used for mechanism:

- Gould et al. 2005, `Science`, DOI `10.1126/science.1109418`, PMID `15905400`: semidominant `Col4a1` mutations disrupt vascular basement membranes and cause perinatal cerebral hemorrhage/porencephaly in mice and humans.
- Volonghi et al. 2010, `Current Medicinal Chemistry`, DOI `10.2174/092986710790936293`, PMID `20166936`: review of COL4A1 stroke syndrome; COL4A1 and COL4A2 are abundant basement-membrane type-IV collagens forming a 2:1 heterotrimer.
- Mao et al. 2015, `Current Topics in Membranes`, DOI `10.1016/bs.ctm.2015.09.002`, PMID `26610912`: type-IV collagens are major basement-membrane components and basement-membrane disease mechanisms are strongly tissue- and cell-context dependent.
- Jeanne et al. 2015, `Circulation`, DOI `10.1161/CIRCULATIONAHA.114.013395`, PMID `25753534`: Col4a1/Col4a2 mutant mouse models develop vascular defects and intracerebral hemorrhage linked to mutant collagen accumulation in vascular endothelial cells and pericytes.
- Branyan et al. 2022, `Matrix Biology`, DOI `10.1016/j.matbio.2022.11.007`, PMID `36435425`: collagen alpha1-alpha1-alpha2(IV) is a regulator of TGF-beta signaling in CNS vascular pathology in `Col4a1` mutant mouse models.

## Computation over the training data

I first loaded the requested-target manifest and the focal-cell training counts. `Col4a1` was the only requested target and did not appear in the 1,674 training counts.

I then queried candidate analogs in the training count CSV. Because `Col4a1` and its obligate partner `Col4a2` were both held out, I used weaker but mechanistically relevant families:

- structural ECM/collagen perturbations available in training: `Col2a1`, `Col11a1`;
- collagen or basement-membrane integrin receptors available in training: `Itga2`, `Itga6`, `Itgb1`, plus the broader available integrin set `Itga2b`, `Itga7`, `Itga8`, `Itga9`, `Itgb2`;
- TGF-beta/BMP receptors and SMADs, because Col4a1 vascular disease can elevate TGF-beta signaling: `Tgfbr1`, `Tgfbr2`, `Tgfbr3`, `Smad1`, `Smad2`, `Smad3`, `Smad4`, `Smad6`, `Smad9`.

The key parquet operation was a predicate scan restricted to the focal cell class and the selected observed analogs:

```python
dataset.to_table(
    columns=[
        "names", "scores", "logfoldchanges", "pvals_adj",
        "group_name", "gene_target", "n_pert_matched", "n_ctrl_matched",
    ],
    filter=(
        (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
        & ds.field("gene_target").isin(candidates)
    ),
)
```

For these selected targets I counted `pvals_adj < 0.05`, inspected the smallest adjusted p-values, and checked whether any significant rows were only self-target RNA. I also ran `profile_compare`/`profile_inspect` from `mcp__distributed_agents_runtime` over 13 ECM, integrin, TGF-beta receptor, and SMAD perturbations in the focal context. That response-activity audit reported 12 of 13 nodes with `no_significant_features`; only `Smad2` was in the weak `1_to_9_significant_features` class.

Observed focal counts among the material analogs:

| training target | `n_degs` in 151 TH | focal parquet evidence | role for `Col4a1` |
|---|---:|---|---|
| `Col2a1` | 0 | 304 perturbed vs 23679 controls; no focal gene at FDR 0.05; minimum focal `pvals_adj = 0.9846` | ECM collagen counterexample: a structural collagen perturbation was silent in NeuN+ thalamic neurons. |
| `Col11a1` | 0 | 167 perturbed vs 23679 controls; no focal gene at FDR 0.05; minimum focal `pvals_adj = 1.0` | ECM collagen counterexample; Distributed Agents `Col11a1:F001` reports no downstream FDR 0.10 transcriptome in any measured postnatal NeuN+ group. |
| `Itga2` | 0 | 154 perturbed vs 23679 controls; no focal gene at FDR 0.05; minimum focal `pvals_adj = 0.8832` | `Itga2` is an alpha subunit of a collagen/laminin receptor; its complete neuronal null argues against a generic collagen-adhesion nuclear response. Distributed Agents `Itga2:F001` also called it FDR-null across sampled neuronal groups. |
| `Itga6` | 0 | 165 perturbed vs 23679 controls; no focal gene at FDR 0.05; minimum focal `pvals_adj = 1.0` | Laminin/basement-membrane receptor comparator; not a collagen-IV ligand receptor but tests the closest represented basement-membrane adhesion axis. |
| `Itgb1` | 0 | 110 perturbed vs 23679 controls; no focal gene at FDR 0.05; minimum focal `pvals_adj = 1.0` | Core beta1 ECM receptor. Distributed Agents `Itgb1:F001` reported a pan-measured FDR-null nuclear transcriptome and `Itgb1:F002` found represented integrins did not expose a shared beta1/focal-adhesion module. |
| `Itga2b`, `Itga7`, `Itga8`, `Itga9`, `Itgb2` | all 0 | every one had 0 focal FDR 0.05 genes | Broader integrin controls; useful as boundaries, not direct COL4A1 analogs. |
| `Tgfbr1`, `Tgfbr2`, `Tgfbr3` | all 0 | every one had 0 focal FDR 0.05 genes; `Tgfbr1` minimum focal `pvals_adj = 0.8913`, `Tgfbr2 = 1.0`, `Tgfbr3 = 1.0` | Tests whether the TGF-beta receptor side of COL4A1 vascular biology is basally transcriptionally active in this NeuN+ assay. It was not. |
| `Smad1`, `Smad3`, `Smad4`, `Smad6`, `Smad9` | all 0 | no focal FDR 0.05 genes | SMAD pathway boundaries. |
| `Smad2` | 1 | one focal hit, `Cpne7`, `logfoldchanges = -0.411`, `pvals_adj = 0.0167` | Weak positive counterexample showing that the receptor/SMAD set was not impossible to score, but a single non-canonical focal hit did not establish a broad TGF-beta-like program. |

The same-experiment corpus was concordant with the direct focal reads:

- `Col2a1:F001`: postnatal `Col2a1` loss was essentially flat in NeuN-enriched neurons, with only two FDR 0.10 downstream genes across 23 groups and no UPR/chondrocyte ECM-marker program.
- `Col11a1:F001`: `Col11a1` loss produced no FDR 0.10 downstream transcriptome in any measured postnatal NeuN+ brain neuronal group.
- `Itga2:F001`: `Itga2` was transcriptomically silent at FDR 0.10 in every sampled neuronal group.
- `Itgb1:F001` and `Itgb1:F002`: beta1-integrin loss and represented integrin relatives were pan-null or singleton-only rather than a shared focal-adhesion transcriptomic state.
- `Tgfbr1:F003`: represented TGF-beta/BMP receptor-SMAD perturbations were nearly silent in basal neuronal nuclei.

I rejected nominal profile neighbors that appeared only in rank-overlap/correlation views after the runtime audit, because for the ECM/integrin nodes the leading positive and negative genes had `pvals_adj = 1.0` and were dominated by very low-support pseudo-count log-fold changes. They were noise-floor directions, not robust expression-pattern evidence.

## Target-specific prediction

### `Col4a1`

`Col4a1` encodes collagen IV alpha 1. Together with `Col4a2`, it forms the major alpha1-alpha1-alpha2(IV) basement-membrane heterotrimer. Pathogenic COL4A1/COL4A2 biology in the brain is real but largely explained by basement-membrane and vascular mechanisms: focal vascular basement-membrane disruption in `Col4a1` mutant mice and human porencephaly families, mutant collagen retention in vascular endothelial cells and pericytes, and altered vascular TGF-beta signaling.

That biology is an imperfect match to this experiment. The readout is juvenile-to-young-adult NeuN-enriched nuclei recovered after sparse postnatal AAV-CRISPR perturbation; vascular, meningeal, endothelial, pericyte, astrocyte, and microglial compartments where type-IV collagen basement membranes are most interpretable are absent or under-sampled. The knockout is also a sparse loss-of-function perturbation, not a germline dominant glycine-substitution collagenopathy that secretes or retains a misfolded matrix chain during development.

Within the training data, the most relevant observed ECM and receptor perturbations favored a zero call:

- structural collagen comparators `Col2a1` and `Col11a1` were both focal zeros, and the Distributed Agents corpus found no recurring postnatal NeuN+ ECM or UPR response for them;
- collagen/basement-membrane adhesion comparators `Itga2`, `Itga6`, and `Itgb1` were all focal zeros despite adequate matched controls, and represented integrin relatives were also focal zeros;
- the TGF-beta/SMAD axis implicated by vascular Col4a1 mutant models was inactive as a basal neuronal single-gene knockout module: `Tgfbr1`, `Tgfbr2`, `Tgfbr3`, and all available SMADs except one `Smad2` singleton had zero focal DEGs.

I therefore predict no gene crossing BH FDR 0.05 for `Col4a1` in `151 TH Prkcd Grin2c Glut`.

Point prediction: `Col4a1 -> 0`.

## Limits and extrapolation

- The ideal analog `Col4a2` was also held out, so no true type-IV collagen partner perturbation was available in the training endpoint.
- Most direct basement-membrane ligands and matrix assembly partners, including laminins, nidogens, `Hspg2`, and `Serpinh1`, were absent from the focal training-count CSV, so the comparison had to use more distant structural collagens, integrins, and TGF-beta/SMAD pathway members.
- `Col4a1` disease alleles often behave through dominant matrix misfolding or secretion defects. The Perturb-seq perturbation is sparse loss of function, so the prediction applies only to this CRISPR design and endpoint.
- A zero DEG-count prediction is not a claim that COL4A1 is unimportant in the brain. It is a claim that sparse postnatal `Col4a1` loss is unlikely to produce a recovered-nucleus, BH-significant transcriptional footprint in NeuN+ `151 TH Prkcd Grin2c Glut` cells under this assay's power and filtering.
