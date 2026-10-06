# Prediction trace

## Question and resolved ambiguities

The requested held-out perturbation list contains one target, `Drd3`. I interpreted the endpoint as the integer number of measured genes in `151 TH Prkcd Grin2c Glut` with `pvals_adj < 0.05` after acute sparse AAV-CRISPR loss of the target. Because `Drd3` was fully held out, I did not look for a direct `Drd3` DEG count or signature in the training files; instead I used same-assay perturbations of dopamine receptors and proximal signaling nodes to calibrate the expected breadth of a Drd3 loss-of-function response in this cell group.

## Sources

- Training endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training DE matrix: `[local file: training_de_all_cell_groups.parquet]`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"`.
- Held-out manifest: `[local file: 062_Drd3.csv]`.
- Distributed Agents same-experiment corpus release `perturbai-july-260713-sourceguard-1773-v1`. It had no `Drd3` target context, but did contain Drd2, Drd4, Drd5, Gnal, Adcy5, Pde10a, and related findings and claims.
- External biological knowledge from PubMed-indexed literature:
  - Sokoloff et al. 1990, Nature, "Molecular cloning and characterization of a novel dopamine receptor (D3) as a target for neuroleptics", DOI 10.1038/347146a0, PMID 1975644.
  - Missale et al. 1998, Physiological Reviews, "Dopamine receptors: from structure to function", DOI 10.1152/physrev.1998.78.1.189, PMID 9457173.
  - Beaulieu and Gainetdinov 2011, Pharmacological Reviews, "The physiology, signaling, and pharmacology of dopamine receptors", DOI 10.1124/pr.110.002642, PMID 21303898.
  - Beaulieu et al. 2005, Cell, "An Akt/beta-arrestin 2/PP2A signaling complex mediates dopaminergic neurotransmission and behavior", DOI 10.1016/j.cell.2005.05.012, PMID 16051150.

## Computational checks

I read the 1,674-row focal training-count CSV to obtain observed `n_degs` for non-held-out targets and to verify which Drd3-adjacent genes were assayed. I then predicate-filtered the 7.8 GB parquet by `group_name = "151 TH Prkcd Grin2c Glut"` and selected the receptor/cAMP/Akt neighborhood around dopamine signaling. For each selected `gene_target`, I counted `pvals_adj < 0.05`, recorded the smallest adjusted p-value, and inspected the top-ranked genes plus canonical immediate-early and striatal dopamine markers.

The directly relevant focal-cell counts were:

| training target | why relevant | `n_degs` in `151 TH Prkcd Grin2c Glut` |
| --- | --- | ---: |
| Drd2 | closest represented D2-like paralog; same inhibitory dopamine receptor class as Drd3 | 0 |
| Drd4 | D2-like dopamine receptor paralog | 0 |
| Drd5 | represented D1-like dopamine receptor counterexample | 0 |
| Gnal | G-alpha-olf source arm into adenylyl cyclase | 0 |
| Gnao1 | Gi/o family G-alpha; the only focal hit was its own transcript | 1 |
| Gnas | Gs source arm into adenylyl cyclase | 0 |
| Adcy1, Adcy3, Adcy5 | adenylyl cyclases in the same second-messenger axis | 0, 0, 0 |
| Pde10a, Pde1c, Pde4b, Pde4d | cAMP/cGMP phosphodiesterases that bound cyclic-nucleotide signaling on the sink side | 0, 0, 0, 0 |
| Prkaca, Prkar1a | direct PKA subunits | 1, 1 |
| Akt3, Gsk3b, Ntrk2, Nr4a1 | beta-arrestin/Akt/neurotrophin/immediate-early counterexamples | 0, 6, 3, 0 |

In the exact focal parquet rows, `Drd2`, `Drd4`, and `Drd5` each had 17,259 tested features, 213 to 228 matched perturbed nuclei, and minimum `pvals_adj = 1.0`. All queried canonical response markers were also adjusted-p 1.0 under the three dopamine receptor perturbations: `Fos`, `Fosb`, `Egr1`, `Nr4a1`, `Nr4a2`, `Nr4a3`, `Arc`, `Crem`, `Bdnf`, `Penk`, and `Ppp1r1b`. Thus the zero counts are not just threshold edge cases; the receptor profiles in this cell group were FDR-clean nulls.

## Target-specific reasoning

### Drd3

`Drd3` is a D2-like dopamine GPCR. The D2/D3/D4 subfamily couples primarily to Gi/o proteins, inhibits adenylyl cyclase, can regulate K+ and Ca2+ conductances, and can also signal through beta-arrestin scaffolds that affect Akt/GSK3, while D1/D5 receptors are the classical Gs/olf-adenylyl cyclase branch. That classification makes `Drd2` and `Drd4` the most mechanistically appropriate assayed paralogs for a held-out `Drd3` knockout, and it makes `Gnao1`, `Gnal`, `Gnas`, `Adcy1/3/5`, PDEs, PKA subunits, `Akt3`, and `Gsk3b` useful pathway counterexamples.

The within-dataset evidence points strongly to a focal-cell null:

- `Drd2`, the closest represented D2-like paralog, had `0` DEGs in `151 TH Prkcd Grin2c Glut`. Distributed Agents `Drd2:F003` also reported that Drd2 deletion failed to induce cAMP/immediate-early, indirect-pathway, or dopamine-autoreceptor marker panels across the measured screen, and `Drd2:F002` reported non-convergence with represented dopamine-family receptors and D2 effector nodes.
- `Drd4` had `0` DEGs in this focal group. Distributed Agents `Drd4:F001` described a taxonomy-wide FDR<0.10 null for Drd4, and `Drd4:F002` found near-zero same-screen convergence with `Drd2`, `Drd5`, `Gnao1`, `Gnal`, `Gnas`, `Adcy1`, `Adcy3`, `Adcy5`, `Pde1c`, `Pde4b`, `Pde4d`, and `Pde10a`.
- `Drd5`, although D1-like rather than D2-like, was the other directly represented dopamine receptor class and also had `0` DEGs here. Distributed Agents `Drd5:F003` found that represented dopamine/cAMP relatives did not converge with Drd5, while the high-level corpus claim `claim:5778f7e46773642bd0bd` summarized that represented dopamine/GPCR and cAMP perturbations do not collapse into one shared durable basal neuronal mRNA module in this assay.
- Proximal source-arm and sink-arm nodes were silent or almost self-only in the same focal group: `Gnal`, `Gnas`, `Adcy1`, `Adcy3`, `Adcy5`, `Pde10a`, `Pde1c`, `Pde4b`, and `Pde4d` all had zero DEGs; `Gnao1`, `Prkaca`, and `Prkar1a` had one DEG each, corresponding to the perturbed transcript rather than a broad downstream program. `Gsk3b` and `Ntrk2` gave small 6- and 3-gene responses, showing that the focal group can call a handful of real DEGs for some signaling proteins but not a large dopamine-receptor-like state.

I therefore predict that `Drd3` loss will be FDR-flat in `151 TH Prkcd Grin2c Glut`, with `predicted_n_degs = 0`.

## Limits

This is an extrapolation from paralogs and pathway nodes, not a direct Drd3 observation. `Drd1`, `Gnai1/2/3`, beta-arrestins, GRKs, and `Ppp1r1b` were not represented as focal training targets, so one obvious D1-class receptor and several D2/D3-proximal effectors could not be checked by loss of the exact gene. The assay was basal juvenile NeuN+ snRNA-seq after mosaic postmitotic CRISPR; it does not test acute dopamine-evoked cAMP, electrophysiology, phospho-Akt/GSK3, receptor trafficking, or behavior. Drd3 is known for limbic/striatal functions, so a purified D3-rich nucleus or a ligand challenge could behave differently from the broad `151 TH Prkcd Grin2c Glut` focal group. Within those limits, the same-experiment evidence consistently argues that dopamine receptor and receptor-to-cAMP perturbations produce no broad durable transcriptional response in this cell group.
