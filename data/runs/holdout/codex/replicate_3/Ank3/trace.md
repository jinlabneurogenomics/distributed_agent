target_name	predicted_n_degs
Ank3	1

## Evidence used

- The declared one-row holdout manifest is `Ank3`; `Ank3` is absent from the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` training count table.
- In the declared `151 TH Prkcd Grin2c Glut` count table, the response scale is sparse: among 1,674 observed training perturbations, 1,205 have 0 BH-significant genes, 276 have 1, 90 have 2-10, and 103 have more than 10.
- Recounting the declared Parquet in `151 TH Prkcd Grin2c Glut` showed that 237 of the 276 one-DEG responses are self-transcript-only and another 39 are single downstream genes. In total, 1,442 of 1,674 training targets have no downstream DEG after excluding the perturbed transcript.
- The closest measured AIS/nodal or excitability-associated perturbations in `151 TH Prkcd Grin2c Glut` had only null-to-tiny counts. `Ank1`, `Ank2`, `Sptb`, and `Add2` had 0 DEGs. `Cntnap1`, `Cntnap2`, `Dlg4`, `Dnm1`, `Kcnq2`, `Kcnq3`, `Map1b`, `Scn1a`, `Scn2a`, `Scn8a`, `Sptan1`, and `Sptlc2` each had exactly 1 DEG, always the self transcript in this queried set. `Nrcam` and `Scn1b` had 2 DEGs, consisting of the self transcript plus one additional feature.
- The outcome-blind Ank3 biology bundle makes target engagement plausible but attenuated. Ank3 is expressed in 23,624 of 23,679 non-target nuclei in the focal class, with mean raw UMI 11.317 and mean log1p CP10K 2.035, so the transcript itself is readily measurable. Biologically, Ank3 encodes an installed AIS/nodal scaffold; stopping new synthesis at P16 should produce a partial or leading-edge loss by P37-P44, because pre-existing Ank3-containing domains persist and can be partly buffered at nodes.

## Synthesis

Ank3 is not in the high-burden training families that dominate the upper tail of this cell class. The local training analogs argue against a broad survivor-cell transcriptional response from loss of an axon-initial-segment or nodal membrane-domain component: their significant calls are usually just the perturbed mRNA.

Because Ank3 is almost ubiquitously expressed in the matched thalamic control nuclei, the most likely detectable event is the self transcript if editing induces any nonsense-mediated decay. The functional-stock card weakens the case for many downstream DEGs over the 21-28 day window but does not make a complete molecular null more likely than a self-only call. I therefore predict one BH-significant measured gene.
