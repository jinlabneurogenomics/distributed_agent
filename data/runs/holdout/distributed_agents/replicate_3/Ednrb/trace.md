# Reasoning trace

## Question and resolved ambiguities

The endpoint to predict is the number of measured genes passing Benjamini-Hochberg FDR 0.05 in `151 TH Prkcd Grin2c Glut` cells after each held-out gene perturbation. In this run the manifest contains one held-out target, `Ednrb`.

I treated `n_degs` as the exact screen-specific count in the focal neuronal group, not as a generic estimate of whether the gene is important. The Ednrb perturbation was absent from the training endpoint CSV and absent as a `gene_target` in the differential-expression parquet; the transcript `Ednrb` can still appear as a measured gene in other perturbation signatures.

## Sources used

- `[local file: 066_Ednrb.csv]`: requested targets; one row, `Ednrb`.
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`: observed focal-cell DEG counts for 1,674 non-held-out targets.
- `[local file: training_de_all_cell_groups.parquet]`: row-level log2 fold changes and adjusted p values for non-held-out perturbations.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`. It had no frozen `Ednrb` or `Ednra` claims, but it did contain relevant assay-boundary claims for Sox10/Myrf glial or neural-crest regulators, vascular/lymphatic VEGF/endothelin-adjacent genes, and GPCR/cAMP genes.
- NCBI PubMed for external mechanism checks:
  - Davenport et al. 2016, "Endothelin", DOI `10.1124/pr.115.011833`, PMID `26956245`.
  - McCallion and Chakravarti 2001, DOI `10.1034/j.1600-0749.2001.140305.x`, PMID `11434563`.
  - Bondurand, Dufour and Pingault 2018, DOI `10.1016/j.ydbio.2018.08.014`, PMID `30171849`.
  - Stanchina et al. 2006, DOI `10.1016/j.ydbio.2006.03.031`, PMID `16650841`.

## Computations over the training data

The focal training endpoint has 1,674 perturbed genes. Of these, 469 have at least one DEG in `151 TH Prkcd Grin2c Glut`; the distribution is heavily zero-inflated, with mean `n_degs = 14.05` but a maximum of 2,677.

The parquet has 616,253,184 rows split into 712 row groups. Row-group statistics showed that `group_name` is sorted by row group, so I only scanned row groups whose min/max could contain `151 TH Prkcd Grin2c Glut`, then filtered exactly to the focal group:

```python
for i in range(pf.num_row_groups):
    st = pf.metadata.row_group(i).column(group_idx).statistics
    if st and st.min <= focal <= st.max:
        row_groups.append(i)
```

This identified row groups 546 to 580. I then retained complete focal signatures for a mechanistic comparison set of 23 assayed genes: `Ednra`, endothelin/GPCR second-messenger neighbors, Sox10/glial or neural-crest regulators, and vascular/VEGF/endothelin-adjacent genes. The parquet count of `pvals_adj < 0.05` matched the training-count CSV for all retained signatures.

Key focal counts among the curated analogs were:

| training target | observed `n_degs` | focal expression-pattern evidence |
|---|---:|---|
| `Ednra` | 0 | closest assayed endothelin receptor; all 17,259 measured genes had `q = 1.0` |
| `Sox10` | 0 | neural-crest/Schwann/oligodendrocyte regulator; no significant features |
| `Sox9` | 0 | glial-lineage regulator; no significant features |
| `Gfap` | 0 | astrocyte intermediate filament; no significant features, best focal `q = 0.57` |
| `Myrf` | 0 | oligodendrocyte-lineage regulator; no significant features |
| `Adgrg6` | 0 | neural-crest/Schwann-related GPCR; no significant features |
| `Egr2` | 0 | Schwann/peripheral myelin regulator; no significant features |
| `Sox18` | 0 | vascular/lymphatic transcription factor; no significant features |
| `Flt4` | 0 | VEGFR3, vascular/lymphatic receptor; no significant features |
| `Kdr` | 0 | VEGFR2, endothelial receptor; no significant features |
| `Nrp2` | 0 | neuropilin vascular/axon cue receptor; no significant features |
| `Vezf1` | 6 | vascular zinc-finger factor; very small response |
| `Gnas` | 0 | proximal GPCR/cAMP alpha subunit; no significant features |
| `Gnal` | 0 | GPCR alpha subunit; no significant features |
| `Gnao1` | 1 | only significant feature was `Gnao1` itself, `log2FC = -0.59`, `q = 9.4e-7` |
| `Adcy1` | 0 | adenylyl cyclase; no significant features |
| `Adcy3` | 0 | adenylyl cyclase; no significant features |
| `Plcb1` | 0 | PLC-beta; no significant features |

I also ran the Distributed Agents runtime profile comparison on these complete focal signatures. The comparison set contained 23 nodes and 253 pairwise signature comparisons; 20 of the 23 had no significant features, 2 had 1-9 significant features, and only `Mib1` had 10-49. The nearest-neighbor view around `Ednra`, `Sox10`, `Gfap`, `Gnas`, and `Gnao1` showed no intersections of significant positive or negative DE features with the mechanistic peers listed above. Whole-profile correlations among flat signatures were therefore not used as positive evidence for a shared Ednrb-like program.

Finally, I filtered the measured-gene rows for the endothelin markers. `Ednrb` itself was present as `names == Ednrb` in all 1,674 focal training signatures but never had an adjusted p value below 1.0; its Wilcoxon scores were near zero despite unstable low-count log-fold-change values. `Ednra` and `Edn3` behaved similarly as measured transcripts. This is consistent with these endothelin-system RNAs being uninformative or very sparsely detected in the focal neuronal nuclei.

## Target-specific reasoning

### Ednrb

`Ednrb` encodes endothelin receptor type B, a GPCR in the endothelin system. EDN1 and EDN2 can activate both ETA and ETB receptors, while EDN3 is relatively selective for ETB compared with ETA (Davenport et al. 2016). The strongest developmental genetics around `Ednrb` is the EDN3/EDNRB/SOX10 neural-crest module required for melanocyte and enteric nervous system development; loss of EDN3/EDNRB signaling causes Hirschsprung/Waardenburg phenotypes in mouse and human contexts (McCallion and Chakravarti 2001; Stanchina et al. 2006; Bondurand et al. 2018).

The best direct receptor analog available in the training screen is `Ednra`. In the same focal `151 TH Prkcd Grin2c Glut` neurons, `Ednra` had `n_degs = 0`: every focal feature had adjusted `q = 1.0` even with 130 perturbed nuclei against 23,679 controls. `Ednra` is an imperfect proxy because ETA and ETB differ in ligand preference and cell biology, but it is the only assayed endothelin receptor and it argues that loss of an endothelin GPCR did not produce a detectable basal postnatal neuronal RNA program.

The developmental EDN3/EDNRB evidence points mostly to neural-crest, melanocyte, enteric-neuron, Schwann-cell, glial, and vascular compartments rather than a TH/Prkcd/Grin2c glutamatergic neuron. That compartment mismatch is also visible inside the dataset. `Sox10`, `Sox9`, `Myrf`, `Adgrg6`, `Egr2`, and `Gfap` all had `0` DEGs in the focal group. The Distributed Agents same-experiment corpus independently summarized that represented Schwann-cell, oligodendrocyte, neural-crest, and myelin transcriptional programs were not recovered in this NeuN-enriched postnatal neuronal assay (`claim:2d6034ec908df8d8ef73`, `claim:0ea6dcfab0b7b9468b6a`). Vascular/lymphatic comparators were also flat or tiny: `Flt4`, `Kdr`, `Nrp2`, and `Sox18` had `0` DEGs and `Vezf1` had `6`, consistent with the corpus claim that vascular/lymphatic VEGF, neuropilin, and endothelin-adjacent pathway programs were not recovered as shared modules in assayed postmitotic neurons (`claim:ad9d02cb5022b86d9964`).

I considered generic GPCR signaling as a possible nonzero route because ETB is a G-protein-coupled receptor. The assayed proximal pathway perturbations again supported a near-zero prediction: `Gnas`, `Gnal`, `Adcy1`, `Adcy3`, and `Plcb1` each had `0` DEGs, while `Gnao1` had a one-gene, target-RNA-only response. The Distributed Agents corpus likewise reported that represented GPCR and cAMP-pathway perturbations did not collapse into a shared durable basal neuronal mRNA module in this juvenile snRNA-seq assay (`claim:5778f7e46773642bd0bd`).

Taken together, the within-dataset evidence dominates the prediction. The closest assayed receptor is exactly zero; developmentally related glial/neural-crest regulators are zero; vascular neighbors are absent or tiny; proximal GPCR/cAMP neighbors are zero; and measured `Ednrb` RNA is not detectably regulated across the entire focal training set. I therefore predict no FDR-significant genes for postnatal sparse CRISPR loss of `Ednrb` in `151 TH Prkcd Grin2c Glut` neurons.

Predicted count: `Ednrb = 0`.

## Limits

- `Ednrb` itself was held out, so this prediction is extrapolated from analogs rather than from an observed Ednrb signature.
- `Edn1`, `Edn2`, `Edn3`, `Ece1`, `Ece2`, `Gnaq`, `Gna11`, `Gna12`, and `Gna13` were not available as focal training perturbations. That removes the ligands, ligand-processing enzymes, and several canonical G-protein branches from direct calibration.
- `Ednra` is the most direct training analog but is not a paralog and is pharmacologically distinct from ETB.
- The strongest Ednrb biology is developmental and often non-neuronal. The assay perturbs sparse postnatal NeuN-positive nuclei after neural-crest and vascular patterning, so a zero DEG prediction here does not contradict known Ednrb requirements in embryonic neural crest, enteric neurons, melanocytes, glia, or vasculature.
- Similarity among flat expression signatures is not mechanistic convergence. I used the flat signatures as evidence of absent detectable endpoint response, not as proof that all these genes act in one module.
