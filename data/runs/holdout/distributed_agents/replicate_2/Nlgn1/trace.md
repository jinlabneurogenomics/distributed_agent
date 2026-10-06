# Nlgn1 DEG-count prediction

## Question interpreted

The requested target manifest contains one held-out perturbation:

| target_name |
|---|
| Nlgn1 |

I interpreted `n_degs` as the number of measured genes with `pvals_adj < 0.05` for the held-out CRISPR loss-of-function perturbation in `151 TH Prkcd Grin2c Glut`, using the same Scanpy/Wilcoxon output that produced the training count table. The target transcript itself can be counted when it is significantly depleted; several singleton training responses are exactly the perturbed gene. I did not treat a zero or weak target-mRNA fold change in the training data as failed editing, because the experiment reports only average RNA depletion and does not measure indels or protein abundance.

## Sources used

- Differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Focal training endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested held-out manifest: `[local file: 152_Nlgn1.csv]`.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`, especially its frozen claims for `Nlgn3`, `Nrxn2`, PSD-scaffold, and synaptic-adhesion findings.
- PubMed/NCBI literature searches for neuroligin-1, neurexin/neuroligin signaling, and Nlgn1 loss-of-function physiology.

## Dataset computations

1. I read the held-out manifest and confirmed that `Nlgn1` was the only requested target.
2. I summarized the focal training-count CSV to calibrate the response scale. The focal count distribution is very zero-inflated: among 1,674 non-held-out perturbations, 469 were nonzero, the median was 0, the 75th percentile was 1, the 90th percentile was 2, the 95th percentile was 18, and the maximum was 2,677.
3. I used the parquet row-group statistics to restrict differential-expression reads to `group_name == "151 TH Prkcd Grin2c Glut"`, then filtered to synaptic-adhesion, neurexin/neuroligin, LRRTM, contactin-associated, glutamate-receptor, and PSD-scaffold training perturbations. For each candidate analog I inspected the exact `pvals_adj < 0.05` rows, their `logfoldchanges`, and the matched cell counts.
4. I ran a run-local profile comparison for 20 represented synaptic candidates: `Nlgn3`, `Nrxn1`, `Nrxn2`, `Nrxn3`, `Lrrtm1`, `Lrrtm3`, `Lrrtm4`, `Dlg4`, `Dlgap4`, `Shank2`, `Shank3`, `Magi2`, `Cntnap1`, `Cntnap2`, `Ctnna2`, `Ctnna3`, `Ctnnd2`, `Syngap1`, `Grin2a`, and `Grin2b`. This was a guard against calling a single family member an analog without asking whether the measured log-fold-change surface actually had a coherent synaptic module. The comparison found no shared significant FDR genes across the neurexin/neuroligin/LRRTM/PSD set; `Nlgn3`, `Nrxn1`, and `Dlg4` each had exactly one significant negative feature in the focal cell group, while `Nrxn2` and `Nrxn3` had none.

## Nlgn1-specific reasoning

### Directly relevant training perturbations

| training target | focal `n_degs` | focal FDR<0.05 pattern | Why I used it |
|---|---:|---|---|
| `Nlgn3` | 1 | Only `Nlgn3` itself was significant, log2FC = -0.896, FDR = 4.79e-11 with 177 perturbed nuclei and 23,679 controls. | Closest represented neuroligin paralog. Like NLGN1, NLGN3 is a postsynaptic neurexin ligand, but its perturbation did not drive downstream nuclear remodeling in this focal glutamatergic group. |
| `Nrxn1` | 1 | Only `Nrxn1` itself was significant, log2FC = -0.518, FDR = 2.67e-23. | Presynaptic binding side of the neurexin/neuroligin trans-synaptic adhesion pair. |
| `Nrxn2` | 0 | No significant genes. | Neurexin paralog and NLGN ligand; a useful negative analog for the same adhesion layer. |
| `Nrxn3` | 0 | No significant genes. | Neurexin paralog and NLGN ligand; again flat in the focal endpoint. |
| `Lrrtm1` | 1 | A single non-coherent row, `R3hdm2`, FDR = 0.0269. | LRRTMs are neurexin-binding postsynaptic organizers; the singleton non-synaptic hit argues against a reusable LRRTM/neurexin RNA program. |
| `Lrrtm3` | 0 | No significant genes. | Same LRRTM/neurexin adhesion neighborhood, flat. |
| `Lrrtm4` | 0 | No significant genes. | Same LRRTM/neurexin adhesion neighborhood, flat. |
| `Dlg4` | 1 | Only `Dlg4` itself was significant, log2FC = -0.444, FDR = 1.15e-08. | PSD-95 is a postsynaptic scaffold linked to NLGN1 intracellularly. Its perturbation behaved as target-only rather than as a broad PSD compensation program. |
| `Dlgap4` | 2 | `Dlgap4` itself and `Vgf` passed FDR. | SAPAP/PSD95/SHANK scaffold member; sparse rather than a shared receptor-scaffold program. |
| `Shank2` | 0 | No significant genes. | Postsynaptic scaffold downstream of PSD organization; flat. |
| `Shank3` | 2 | `Shank3` itself and `Uba5` passed FDR. | SHANK family PSD scaffold; sparse and not a strong neurexin/neuroligin analog transcriptionally. |
| `Magi2` | 0 | No significant genes. | PDZ scaffold near glutamatergic postsynaptic organization; flat. |
| `Cntnap1` | 1 | Only `Cntnap1` itself was significant, log2FC = -0.822, FDR = 1.09e-11. | Cell-adhesion/contactin-associated counterpoint; target-only. |
| `Cntnap2` | 1 | Only `Cntnap2` itself was significant, log2FC = -1.087, FDR = 7.90e-06. | Autism-associated neuronal adhesion gene; target-only. |
| `Grid1` | 1 | Only `Grid1` itself was significant, log2FC = -0.487, FDR = 2.62e-05. | GluD/Cbln/neurexin-adjacent synaptic organizer; target-only. |
| `Grid2` | 0 | No significant genes. | GluD/Cbln/neurexin-adjacent synaptic organizer; flat. |
| `Grin2a` | 1 | Only `Grin2a` itself was significant, log2FC = -0.492, FDR = 0.0020. | NMDAR subunit and a functional postsynaptic comparator; target-only. |
| `Grin2b` | 2 | `Grin2b` itself and `Pianp` passed FDR. | NMDAR subunit; sparse. |
| `Grin1` | 89 | Broad response with `Grin1` self-depletion and many neuronal-state genes. | Important counterexample. The assay can detect a glutamatergic receptor perturbation when the hit is an obligatory receptor subunit, so the flat Nlgn3/neurexin/PSD patterns are not just a failure of the cell group or the Wilcoxon test. |

### Internal corpus evidence

`Nlgn1` itself was not present in the Distributed Agents corpus release, but the same-experiment corpus contains two high-confidence higher-order claims that are directly applicable to the represented analogs.

- `claim:60396794c5493932dc07`: "Represented postsynaptic scaffold and synaptic adhesion gene perturbations generally do not induce a shared steady-state neuronal RNA module in this P16 screen." Its `Nlgn3:F002` contribution states that obvious neurexin/neuroligin and scaffold neighbors were queried directly and were mostly flat or sparse rather than Nlgn3-like.
- `claim:da426d57898fc5cde54d`: "Represented synaptic adhesion and receptor-scaffold perturbations are largely buffered or off-axis in the postnatal neuronal nuclear transcriptome, lacking a shared broad downstream DE module." Its `Nrxn2:F003`, `Nlgn3:F002`, `Lrrtm3:F002`, `Lrrtm4:F002`, `Grid2:F004`, and `Cadm2:F003` contributions cover the same neurexin, LRRTM, neuroligin, GluD, CADM, and contactin-associated adhesion layer that I used as analogs.

This corpus context matters because it is same-experiment evidence, not just outside cell biology: the expected adhesion partners failed to become a common mRNA state under the same acute juvenile neuronal CRISPR design.

### External biological rationale

Neuroligin-1 is a postsynaptic cell-adhesion molecule at glutamatergic postsynapses that binds beta-neurexins and localizes with PSD-95 and NMDAR-containing postsynaptic densities (Song et al., 1999, PMID 9927700, doi:10.1073/pnas.96.3.1100). Neuroligins are important for synapse maturation and function rather than initial synapse formation in vivo (Varoqueaux et al., 2006, PMID 16982420, doi:10.1016/j.neuron.2006.09.003). Nlgn1 loss preferentially affects excitatory synapse function and NMDAR/AMPAR organization in mouse neurons and in vivo hippocampal circuits (Chubykin et al., 2007, PMID 17582332, doi:10.1016/j.neuron.2007.05.029; Jedlicka et al., 2015, PMID 25713840, doi:10.1007/s00429-013-0636-1), and conditional deletion of neuroligins reorganizes synaptic neurotransmitter receptors without large changes in synapse number (Chanda et al., 2017, PMID 28607166, doi:10.1523/JNEUROSCI.0125-17.2017).

That biology makes `Nlgn1` a very strong mechanistic neighbor of `Nlgn3`, `Nrxn1/2/3`, LRRTMs, and PSD scaffolds, but it points to local synaptic receptor localization and electrophysiology more than to a broad cell-autonomous nuclear transcriptional program. The focal training data quantify that distinction: the analogous adhesion and PSD perturbations were concentrated at 0 to 2 DEGs, with many singleton counts representing only the targeted transcript.

### Zero/nonzero and count decision

I predict a nonzero count, but only barely. The most probable FDR-supported event is CRISPR-mediated depletion of the `Nlgn1` transcript itself. `Nlgn3`, `Nrxn1`, `Dlg4`, `Cntnap1`, `Cntnap2`, `Grid1`, and `Grin2a` all produced singleton focal responses via their own targeted mRNA, establishing that a structural synaptic gene can be counted once even when no downstream state is visible.

I do not expect a second reproducible downstream DEG. `Nlgn3`, neurexins, LRRTMs, `Dlg4`, `Shank2`, `Magi2`, `Grid2`, `Cacng2`, and AMPAR subunits were flat or target-only; the Distributed Agents same-experiment claims explicitly treat the represented neurexin/neuroligin/LRRTM and PSD-scaffold neighborhood as buffered or off-axis for basal P16-to-P37/44 snRNA-seq. `Grin1` is the key counterexample with 89 DEGs, but it is an obligatory NMDA-receptor pore subunit and therefore a stronger route to a postsynaptic functional state than loss of one neuroligin isoform.

Final point prediction for `Nlgn1`: `1`.

## Limits of the prediction

- The held-out `Nlgn1` signature and true `n_degs` are absent, and the Distributed Agents corpus has no direct `Nlgn1` target record; this is extrapolation from `Nlgn3` and the represented neurexin/LRRTM/PSD neighborhood.
- NLGN1 and NLGN3 are close but not interchangeable. NLGN1 is more classically associated with excitatory PSD-95/NMDAR organization, whereas NLGN3 has additional isoform- and circuit-specific biology.
- `Nlgn2`, `Nlgn4`, and some neurexin splice-form-specific or cerebellin ligands were not direct training perturbations, so the measured analog set samples the adhesion layer incompletely.
- The single-nucleus readout measures steady-state nuclear mRNA 3-4 weeks after sparse AAV CRISPR in postmitotic neurons. It does not measure protein depletion, synaptic localization, receptor currents, plasticity, spine morphology, or network compensation, which are exactly the endpoints where Nlgn1 phenotypes are best established.
- The zero-versus-one boundary depends on whether `Nlgn1` mRNA is expressed and captured well enough in `151 TH Prkcd Grin2c Glut` nuclei for its own knockdown to pass FDR. The prediction of one DEG is mostly a target-transcript call; downstream transcriptional evidence supports near-zero breadth rather than a hidden multi-gene program.
