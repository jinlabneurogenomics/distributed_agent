# Pomp forecast

## Target and endpoint

- Target: `Pomp`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in this target-class contrast.

The declared holdout manifest names only `Pomp`; `Pomp` is absent from the declared `151 TH Prkcd Grin2c Glut` training count table, and its expression signature is not used.

## Evidence used

### Pomp biology prior

The declared Pomp biology bundle makes Pomp loss a plausible direct proteasome-biogenesis lesion in this postnatal neuronal window:

- Pomp is expressed in the focal non-target nuclei: 13,943 of 23,679 cells, 58.88%, had detectable `Pomp`; mean expression was 0.625 CP10K / 0.991 raw UMI.
- POMP is a dedicated 20S core and immunoproteasome assembly chaperone, is consumed during proteasome maturation, and has no close mouse paralog after the bundle's Ensembl search.
- The functional-stock card adjudicates stock at harvest as `likely_substantially_depleted`: loss of new POMP should block new 20S assembly by P37-P44, while already mature cores are not immediately inactivated.
- The main dampening uncertainty is latency: the measured mature-core half-lives come from cultured human lymphoid cells, and the direct postnatal neural phenotype evidence in the bundle is for `Psmc1`, not `Pomp`.

That combination argues for a real recovered-cell transcriptional state, but not for an unbuffered instantaneous collapse.

### Training-count anchors

The exact same-cell-class training table is sparse:

- 1,205 / 1,674 training targets have 0 DEGs.
- Only 43 / 1,674 have at least 100 DEGs.
- Only 18 / 1,674 have at least 430 DEGs.

Among training perturbations related to Pomp, the direct proteasome-subunit anchors are large:

| target | `151 TH Prkcd Grin2c Glut` `n_degs` |
|---|---:|
| `Psmb4` | 742 |
| `Psmc1` | 430 |

The better stress-branch controls were quiet in the same count table:

| target | `n_degs` |
|---|---:|
| `Hspa8` | 9 |
| `Hspa5` | 5 |
| `Vcp` | 2 |
| `Sqstm1` | 1 |
| `Nfe2l1` | 0 |
| `Nfe2l2` | 0 |

So I treated Pomp as closer to direct 20S/26S damage than to isolated perturbation of an upstream sensor, heat-shock component, or autophagy/ubiquitin accessory gene.

### Same-experiment reports for training anchors

The packaged training reports support using `Psmb4` and `Psmc1` as the quantitative bracket:

- `Psmb4` loss induced proteasome bounce-back, integrated-stress / heat-shock / redox genes, autophagy-lysosome genes, p53 / apoptosis-risk genes, and repression of synaptic and neuronal-function genes.
- `Psmc1` induced the same broad proteotoxic state: other proteasome-associated mRNAs, `Ubc` / `Uchl1`, autophagy-endolysosomal genes, heat-shock and ISR genes, redox / p53 arms, and synaptic-withdrawal genes.
- The report layer describes `Psmb4` as the top data-driven neighbor of `Psmc1` and notes that accessory proteostasis nodes such as `Nfe2l1`, `Nfe2l2`, `Vcp`, `Hspa5`, `Hspa8`, `Ube3a`, `Ube2e2`, and `Sqstm1` did not reproduce the `Psmb4` program by themselves.

### Parquet profile checks

In the declared Parquet restricted to `151 TH Prkcd Grin2c Glut`, the two direct anchors had the expected stress coordinates:

- `Psmb4`: 742 DEGs, with 357 up and 385 down.
- `Psmc1`: 430 DEGs, with 231 up and 199 down.
- Both significantly induced proteotoxic / ISR or compensatory genes in this exact class, including `Ddit3`, `Zfand2a`, `Sqstm1`, `Psmc6`, and `Optn`.
- Both significantly repressed neuronal-function genes such as `Atp1a3`, `Gria2`, and `Slc17a6`.

In the caller-selected cohort profile comparison, `Psmb4` and `Psmc1` shared 88 positive and 127 negative FDR-significant genes in the same direction with zero significant direction conflicts. They also overlapped 163 / 500 positive-tail and 148 / 500 negative-tail features. In contrast, `Hspa5`, `Hspa8`, `Vcp`, `Nfe2l1`, and `Sqstm1` had essentially no FDR-level overlap with the direct proteasome anchors.

## Numeric synthesis

I put Pomp in the direct proteasome-insufficiency regime rather than the near-null accessory-regulator regime. Its no-paralog, in-assay-expressed, POMP-dependent 20S assembly role is closest to `Psmb4` and `Psmc1`; the 21-28 day window is long enough for finite mature-core buffering to decay. I did not set it above `Psmb4` because POMP removal should stop resupply of new mature cores but leaves pre-existing mature cores initially functional, and no matched Pomp neural loss time course is available.

That led me to use a point just below the `Psmb4`/`Psmc1` midpoint while still in the high-response tail:

`predicted_n_degs(Pomp, 151 TH Prkcd Grin2c Glut) = 560`
