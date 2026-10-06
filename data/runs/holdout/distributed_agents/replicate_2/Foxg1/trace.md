# Reasoning trace

## Question and ambiguity resolution

The held-out target list contains one perturbation, `Foxg1`. I interpreted the requested value as a point prediction for the number of genes that would satisfy `pvals_adj < 0.05` after acute AAV-CRISPR loss of `Foxg1` in the focal `151 TH Prkcd Grin2c Glut` neuronal group. I therefore predicted the FDR-0.05 endpoint used in `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, not a less stringent FDR-0.10 count and not a qualitative FOXG1 disease severity score.

`Foxg1` was absent as a `gene_target` from both supplied training files, so no direct same-experiment `Foxg1` expression signature could be used. It was still present as a measured transcript in the parquet for other perturbations.

## Sources used

- Supplied endpoint CSV: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Supplied differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Supplied held-out manifest: `[local file: 079_Foxg1.csv]`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`. `Foxg1` itself had no corpus node, because it was held out, but the corpus contained Ctnnb1, Tcf7l2, Smad4, Smarca4, Chd4, and Foxp2 findings over the visible training perturbations.
- PubMed literature:
  - Tao and Lai 1992, DOI `10.1016/0896-6273(92)90210-5`: BF-1/Foxg1 is a forkhead factor with rostral neural-tube/telencephalon-restricted expression during development.
  - Xuan et al. 1995, DOI `10.1016/0896-6273(95)90262-7`: null BF-1/Foxg1 disrupts cerebral-hemisphere development through reduced telencephalic progenitor proliferation and premature differentiation.
  - Hebert and McConnell 2000, DOI `10.1006/dbio.2000.9732`: a Foxg1-Cre knock-in recombines in a Foxg1-like pattern dominated by telencephalon and discrete developing head structures.
  - Marcal et al. 2005, DOI `10.1128/MCB.25.24.10916-10929.2005`, and Roth et al. 2010, DOI `10.1242/dev.044909`: FOXG1/BF-1 can function with Groucho/TLE corepressors in cortical and ventral-telencephalic developmental programs.
  - Mariani et al. 2015, DOI `10.1016/j.cell.2015.06.034`: FOXG1 dosage shifts GABAergic/glutamatergic differentiation in human cortical organoids.
  - Schaffner et al. 2022, DOI `10.1038/s41380-022-01497-8`: FOXG1 dosage can affect adult neurogenic forebrain niches.

## Computational steps over the training data

1. I read the held-out manifest and confirmed that the only requested target was `Foxg1`.
2. I summarized the focal training endpoint. The 1,674 visible perturbations were highly zero-inflated: median `n_degs = 0`, the 75th percentile was 1, the 95th percentile was 18, and the maximum was 2,677.
3. I inspected the parquet row-group metadata. Row groups 547-580 all had `group_name == "151 TH Prkcd Grin2c Glut"`, so I restricted focal-cell queries to those 34 row groups.
4. Within those row groups I filtered for:
   - represented forkhead perturbations;
   - cortical and diencephalic developmental TFs;
   - Wnt/beta-catenin and TGF-beta/BMP/SMAD pathway members;
   - chromatin and thalamic-positive controls;
   - sentinel measured genes such as `Axin2`, `Lef1`, `Gabra4`, `Ramp3`, `Kcnc2`, `Cntnap2`, and `Foxg1`.
5. For selected analog perturbations I recomputed the FDR-0.05 counts from `pvals_adj < 0.05`, recorded `n_pert_matched`/`n_ctrl_matched`, and examined the top p-value-ranked genes to distinguish true broad programs from flat signatures with only nominal fluctuations.
6. I also examined every retained `names == "Foxg1"` focal row. Across 1,692 visible perturbation/control contrasts, the best adjusted p-value for the Foxg1 transcript was 0.632 and the best raw p-value was 0.0506, which is the pattern expected for a very weakly or sparsely detected gene in this thalamic class rather than a stable 151 marker.

The non-obvious parquet operation was the row-group filter:

```python
focal_rgs = [
    i for i in range(pf.num_row_groups)
    if pf.metadata.row_group(i)
         .column(group_name_index)
         .statistics.min == "151 TH Prkcd Grin2c Glut"
]
```

## Target-specific evidence and prediction

### Foxg1

**Within-dataset analogs and counterexamples**

| training perturbation | 151 n_degs | matched perturbed nuclei | focal signature evidence | interpretation for Foxg1 |
| --- | ---: | ---: | --- | --- |
| `Foxp2` | 0 | 245 | No FDR genes; all Wnt/SMAD/synaptic sentinels had `pvals_adj = 1`; the best nominal hit, `Senp7`, had `pvals_adj = 1`. | Closest represented neuronal forkhead TF. Its all-cell Distributed Agents context reported no FDR<0.10 genes in 22 measured neuronal groups, arguing that forkhead family membership alone did not create a postmitotic response. |
| `Foxk2` | 0 | 153 | No downstream FDR genes; even the self transcript was only nominal (`Foxk2` log2FC -0.70, adjusted p=0.146). | Represented forkhead comparator with clear focal coverage but no 151 program. |
| `Foxa2`, `Foxj3`, `Foxl2` | 0, 0, 0 | 213, 116, 273 | Each had no FDR genes in 151; top adjusted p-values were 1, 1, and 0.766. | Broader FOX-family controls; these are mostly developmental or non-thalamic factors and served as counterexamples to family transfer. |
| `Tbr1`, `Satb2`, `Bcl11b`, `Otx2`, `Six3`, `Nkx2-1`, `Pax6` | all 0 | 162-288 for `Otx2`, `Six3`, `Tbr1`, `Satb2`, and `Bcl11b`; comparable focal coverage for the others | All were flat in the focal thalamic class. `Tbr1`, for example, had 288 matched perturbed nuclei but no FDR gene in 151. | Developmental patterning and neuronal-identity TFs often timed out of this P16-to-P37/44 thalamic endpoint. `Foxg1` is closer to this class than to an essential RNA-processing or proteasome gene. |
| `Smad4`, `Smad1`, `Smad3`, `Smad6`, `Acvr2a`, `Acvr2b`, `Acvr1`, `Bmpr1a`, `Bmpr1b` | all 0 | `Smad4`: 123; `Acvr2b`: represented in 151 and flat | `Smad4` had no FDR genes in 151 and no Wnt/SMAD sentinel response; `Smad2` produced only a single `Cpne7` DEG. | FOXG1 can use TLE/Groucho-mediated repression and intersect with developmental signaling, but the visible TGF-beta/BMP/SMAD branch is not tonically active in this basal thalamic RNA readout. |
| `Ctnnb1` | 383 | 171 | Strong Wnt/TCF and thalamic excitability response: `Gabra4`, `Ramp3`, `Lef1`, `Kcnc2`, `Vangl1`, `Pcsk2`, `Prkcd`, `Grin2b`, and `Axin2` were FDR hits. | Positive control showing the focal class can respond strongly to a relevant transcriptional effector. The mechanism is beta-catenin/TCF, not FOXG1/TLE, so it is a counterexample rather than a phenocopy. |
| `Tcf7l2` | 106 | 111 | Shared 44 FDR<0.05 genes with `Ctnnb1`, 40 in the same direction; top hits included `Ramp3`, `Kcnc2`, `Pcsk2`, `Cpe`, `Spon1`, `Grin2b`, `Prkcd`, and `Lef1`. | Same positive-control conclusion: the 151 assay can detect a transcription-factor-like thalamic terminal-state response when the target is wired into the basal thalamic state. |
| `Lrp6`, `Gsk3b`, `Fzd2`, `Fzd4`, `Fzd6`, `Fzd9`, `Lgr4`, `Lrp5` | 4, 6, then 0s | 108-120 for `Gsk3b`/`Lrp6` | Upstream Wnt members were small or silent despite `Ctnnb1`/`Tcf7l2` activity. | Even a biologically plausible pathway relation was not enough to transfer a broad count unless the exact assayed branch was engaged. This argues against assigning Foxg1 hundreds of DEGs by developmental-pathway association. |
| `Rora`, `Grin1`, `Mecp2`, `Chd4`, `Smarcc2`, `Arid2`, `Arid1a` | 278, 89, 16, 100, 185, 56, 22 | represented in 151 | These were assay-positive thalamic or chromatin/disease perturbations. Distributed Agents also reported a Chd4/Adnp and BAF/PBAF thalamic module, while `Smarca4` was flat. | These are response-breadth anchors, not direct Foxg1 analogs. They prevent treating the cell group as globally insensitive but show that chromatin or neurodevelopmental labels do not transfer generically. |

**Biological rationale**

FOXG1 is a telencephalic forkhead transcriptional repressor. Its best-established functions are in early forebrain progenitor proliferation, timing of neuronal differentiation, and telencephalic ventral/dorsal patterning; these are embryonic and telencephalon-weighted processes rather than basal programs of a postnatal thalamic glutamatergic neuron. The focal cell class is labeled `TH`, and the direct parquet check found Foxg1 itself to be a nonresponsive, weakly detected measured transcript in the 151 contrasts. That is consistent with the canonical spatial restriction described for BF-1/Foxg1 by Tao and Lai and with the telencephalic Foxg1-Cre pattern from Hebert and McConnell.

The same-experiment training data put several guardrails on the extrapolation:

- Represented forkhead factors were silent in the focal group, and the Distributed Agents `Foxp2` context reported a screen-wide flat surface rather than a hidden forkhead response.
- Developmental TFs that are important in other forebrain or patterning contexts, including `Tbr1`, `Satb2`, `Bcl11b`, `Otx2`, `Six3`, `Nkx2-1`, and `Pax6`, had 0 DEGs in 151.
- The strongest thalamic transcription-factor-like module, `Ctnnb1`/`Tcf7l2`, was branch-specific in the Distributed Agents corpus and in my FDR-overlap calculation. It demonstrates assay sensitivity but does not supply a FOXG1 phenocopy.
- The TGF-beta/BMP/SMAD receptor-to-SMAD set was almost uniformly flat; thus the FOXG1/TLE developmental-repression literature should not be read as evidence for a broad tonic SMAD derepression state in these P16-perturbed neurons.

Given those points, I predicted that acute sparse `Foxg1` loss will not generate any focal genes below FDR 0.05.

Predicted `n_degs`: **0**

## Limits of the reasoning

- No direct `Foxg1` perturbation signature or count was visible; the prediction is an extrapolation from biological localization and from measured neighbors.
- Several true FOXG1 cofactors or paralogs were not in the represented perturbation set. I did not have direct `Tle1/Tle2/Tle3/Tle4`, `Foxp1`, or `Foxp4` knockouts, so the FOXG1/TLE argument was tested only indirectly through visible TGF-beta/SMAD and forkhead/developmental controls.
- The parquet reports differential expression, not absolute baseline expression. The `names == Foxg1` rows are therefore weak evidence for low focal expression, not a formal expression estimate.
- FOXG1 syndrome and germline heterozygous mouse models have broad developmental consequences, including postnatal circuit phenotypes, but those models perturb telencephalic development long before the P16 AAV delivery window and include cell-population, progenitor, and circuit effects that a sparse postmitotic thalamic snRNA contrast may miss.
- A zero DEG prediction does not mean perfect absence of biology. It means that any cell-autonomous effect in recovered 151 nuclei is predicted to be too small, too sparse, too protein-local, too developmental, or too absent from this thalamic population to pass BH-adjusted Wilcoxon FDR 0.05.
