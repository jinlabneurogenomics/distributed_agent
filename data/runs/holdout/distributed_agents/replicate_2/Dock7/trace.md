# Dock7 prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The held-out endpoint is the integer number of genes with `pvals_adj < 0.05` after a sparse postnatal CRISPR perturbation, measured by snRNA-seq in `151 TH Prkcd Grin2c Glut` neurons. The requested-target file for this run contains one target:

```text
Dock7
```

I treated this as a prediction of the actual assay-specific DEG count, not as a prediction of whether Dock7 is biologically important. A gene can be developmentally important, act through Rac/Cdc42 or cytoskeletal remodeling, or alter neuronal morphology without creating FDR-significant somatic nuclear mRNA changes in this P16-to-P37/P44 mosaic assay.

## Sources used

- `training_de_all_cell_groups.parquet`: filtered to `group_name == "151 TH Prkcd Grin2c Glut"` and to biologically relevant Rho/Rac/Cdc42, PAK, WAVE, GEF/GAP and guidance comparators, then counted `pvals_adj < 0.05` and inspected self-transcript log fold changes.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: used as the authoritative focal-cell training endpoint for the same perturbations.
- Distributed Agents Corpus, release `perturbai-july-260713-sourceguard-1773-v1`: used for same-experiment findings and claims about represented Rac/Cdc42-linked actin-cytoskeleton perturbations, especially `Dock3`, `Cdc42`, `Kalrn`, `Pak1`, `Pak2`, `Pak3`, `Rac1`, `Tiam1`, `Cyfip1`, `Cyfip2`, `Arhgap18`, `Arhgap32`, and `Arhgef9`.
- Distributed Agents run-local `profile_neighbors`: used to compare the focal-cell log-fold-change profiles of Dock3/Rac1/Cdc42/GEF/GAP/WRC/guidance nodes, confirming that the small signatures in this cohort were flat, self-transcript-only, or mutually weak rather than a coherent high-DEG module.
- NCBI PubMed literature searches for Dock7/DOCK7 function.

## Computational checks on the training data

For the mechanistic comparator set I filtered the parquet to the focal cell group and counted significant genes per training target:

```python
pd.read_parquet(
    training_de,
    columns=[
        "names", "group_name", "gene_target", "logfoldchanges",
        "pvals_adj", "n_pert_matched", "n_ctrl_matched",
    ],
    filters=[
        ("group_name", "==", "151 TH Prkcd Grin2c Glut"),
        ("gene_target", "in", comparator_targets),
    ],
)
```

The focal-cell counts matched the training CSV for the selected comparators. Perturbations closest to Dock7 biology had the following endpoints in `151 TH Prkcd Grin2c Glut`:

| training target | focal `n_degs` | expression evidence in focal group | relevance to Dock7 |
|---|---:|---|---|
| `Dock3` | 0 | 69 perturbed nuclei; no FDR<0.05 genes; `Dock3` self log2FC -0.43, adjusted p 0.71 | the only represented DOCK-family Rac GEF |
| `Rac1` | 0 | 193 perturbed nuclei; no FDR<0.05 genes | direct small-GTPase effector class for DOCK Rac-GEFs |
| `Cdc42` | 1 | 122 perturbed nuclei; the only hit was `Cdc42` itself, log2FC -0.59, adjusted p 8.6e-5 | Dock7 can couple to Cdc42 in some contexts |
| `Kalrn` | 0 | 152 perturbed nuclei; no FDR<0.05 genes; self log2FC -0.27, adjusted p 0.42 | postsynaptic Rac/Rho GEF and structural-plasticity comparator |
| `Tiam1` | 0 | 180 perturbed nuclei; no FDR<0.05 genes | Rac GEF comparator |
| `Pak1` | 1 | 172 perturbed nuclei; the only hit was `Pak1` itself, log2FC -0.60, adjusted p 5.0e-8 | Rac/Cdc42-activated PAK branch |
| `Pak2` | 0 | 163 perturbed nuclei; no FDR<0.05 genes | Rac/Cdc42-activated PAK branch |
| `Pak3` | 0 | 188 perturbed nuclei; no FDR<0.05 genes | neuronal group-I PAK |
| `Arhgef9` | 1 | 131 perturbed nuclei; the only hit was `Arhgef9` itself, log2FC -0.57, adjusted p 3.7e-8 | synaptic GEF; a counterexample showing a GEF target transcript can be called without downstream genes |
| `Arhgap18` | 0 | 201 perturbed nuclei; no FDR<0.05 genes | Rho/Rac/Cdc42-axis GAP |
| `Arhgap32` | 0 | 180 perturbed nuclei; no FDR<0.05 genes | Rho/Rac/Cdc42-axis GAP |
| `Cyfip1` | 0 | 192 perturbed nuclei; no FDR<0.05 genes | WAVE-regulatory-complex node downstream of Rac |
| `Cyfip2` | 1 | 218 perturbed nuclei; the only hit was `Cyfip2` itself, log2FC -0.49, adjusted p 4.4e-11 | WAVE-regulatory-complex node downstream of Rac |

I also inspected `Dock7` as a measured transcript across all 1,674 non-held-out signatures in this same cell group. It was FDR-significant in only 6/1,674 training perturbations, and the perturbations changing it were broad RNA-processing/proteostasis/chromatin responders such as `Matr3`, `Elp1`, `Uba5`, and `Ufc1`, not Rac/Cdc42-pathway perturbations. The central tendency was essentially flat (`Dock7` log2FC median -0.006; 5th to 95th percentile -0.138 to 0.120), so `Dock7` does not look like a recurrent marker of any local cytoskeletal perturbation state in this focal cell type.

## Dock7-specific biological reasoning

DOCK7 is an atypical guanine-nucleotide exchange factor in the DOCK family. Watabe-Uchida et al. showed that DOCK7 activates Rac in hippocampal neurons, becomes asymmetrically enriched in the nascent axon, promotes Stathmin/Op18 phosphorylation, and is required for axon formation in a developing-neuron polarity assay (Watabe-Uchida et al., 2006, DOI: 10.1016/j.neuron.2006.07.020). DOCK7 has also been linked to Rac1/Cdc42 control of actin-rich protrusions through Myosin VI in neuronal PC12 cells and hippocampal neurites (Majewski et al., 2012, DOI: 10.1139/o2012-009; Sobczak et al., 2016, DOI: 10.1016/j.bbamcr.2016.03.020), and to Rac/Cdc42/JNK signaling during Schwann-cell migration and myelination (Yamauchi et al., 2011, DOI: 10.1523/JNEUROSCI.2738-11.2011). A review by Gadea and Blangy summarizes DOCK proteins as Rho-family GEFs acting on actin, adhesion and migration rather than as obligate transcriptional regulators (Gadea and Blangy, 2014, DOI: 10.1016/j.ejcb.2014.06.003).

Those mechanisms make `Dock3`, `Rac1`, `Cdc42`, `Kalrn`, `Tiam1`, PAKs, GAPs and WRC subunits the right training counterfactuals. They are imperfect because Dock7 is a DOCK-C-family GEF with distinctive axon-polarity biology, whereas Dock3 is a DOCK-A-family Rac GEF and Kalrn/Tiam1 are conventional neuronal RhoGEFs. Still, they test the key question for this endpoint: whether loss of a Rac/Cdc42 cytoskeletal regulator in juvenile postmitotic neurons generally projects onto a detectable nuclear mRNA program.

The same-experiment answer is mostly no. The Distributed Agents Corpus reports that represented Rac/Cdc42-linked actin-cytoskeleton signaling perturbations were transcriptionally buffered in assayed juvenile neurons rather than forming a recurrent shared nuclear mRNA module. Its Dock3 findings specifically report no robust downstream snRNA-seq response in any recovered neuronal group and no convergence with Rac/WAVE/GSK3-beta nodes. Its Cdc42 findings report that Cdc42 had no robust downstream response across recovered neuronal classes and that the expected Rho/actin/spine circuit was silent at the mRNA level. Its Kalrn findings similarly report a completely FDR-flat nuclear transcriptome across neuronal groups despite Kalrn's known roles in Rac1-driven structural synapse biology.

## Prediction

I predict `Dock7` will have no FDR 0.05 DEGs in `151 TH Prkcd Grin2c Glut`: `predicted_n_degs = 0`.

The point prediction is driven mainly by same-dataset evidence. `Dock3`, `Rac1`, `Kalrn`, `Tiam1`, `Pak2`, `Pak3`, `Cyfip1`, `Arhgap18`, and `Arhgap32` were all zero in the focal group; `Cdc42`, `Pak1`, `Arhgef9`, and `Cyfip2` reached one DEG only through the perturbed gene's own transcript. The run-local profile comparison did not reveal a shared high-response expression state among these nodes. External literature makes Dock7 fit that local Rac/Cdc42 and cytoskeletal neighborhood, but it does not supply a reason to expect a chromatin, spliceosome, ribosome, proteostasis, or NMDAR-like broad transcriptional collapse after a sparse P16 neuronal loss-of-function.

## Limits

The main uncertainty is the self-transcript call. If the Dock7 gRNAs reduce a robustly detected nuclear Dock7 RNA in enough recovered `151 TH Prkcd Grin2c Glut` nuclei, the endpoint could plausibly be 1 even if every downstream gene is buffered. Dock3's self transcript was not significant, whereas Arhgef9, Cdc42, Pak1 and Cyfip2 were, so a self-only FDR hit is target-expression and power dependent. The held-out input contains no Dock7 perturbation cell count, gRNA efficiency, protein depletion, indel rate, or baseline per-cell expression, and I therefore did not have a direct way to predict that piece mechanistically.

The biological comparison is also incomplete. Dock7-specific axon-polarity work was largely done in developing hippocampal or cultured neuronal-lineage cells, while this screen perturbs already postmitotic juvenile neurons and reads nuclear RNA from brain-wide NeuN+ nuclei. A real local phenotype in axons, dendritic protrusions, Rac/Cdc42-GTP, JNK, Stathmin phosphorylation, or cytoskeletal organization could be completely missed by this endpoint. Conversely, the absence of Elmo, additional DOCK paralogs, and several WAVE-complex perturbations from the focal comparator list leaves gaps in the direct pathway coverage.
