# Pdhx direct n_degs prediction

Target and endpoint:

- Target: `Pdhx`, from the one-row manifest and canonical biology bundle.
- Population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the focal population.

Evidence used:

1. `codex_runtime/pipeline/dataset_context.md` defines `151 TH Prkcd Grin2c Glut` as a thalamic glutamatergic class and cautions that the PerturbAI readout is acute, sparse, mosaic postnatal CRISPR loss of function in recovered NeuN+ nuclei. Self-target RNA reduction is QC context only and is not a quantitative editing-efficiency or downstream-effect measure.

2. The canonical `biology_bundles/Pdhx.json`, also retrieved through `distributed_agents_runtime.characterization_bundle(view="biology")`, identifies PDHX/E3BP as a noncatalytic pyruvate-dehydrogenase-complex core component that anchors E3. Pdhx is present in the focal class, with `70.8307%` of non-target nuclei expressing it and `mean_cp10k = 0.86995`. Existing PDHX-containing PDC is expected to persist initially after editing and then decline as the complex turns over; by the P37-P44 harvest, functional stock is only adjudicated as `likely_substantially_depleted` with partial evidence because PDHX-specific neuronal residence time was not measured.

3. The same-experiment corpus around measured PDH/carbon-metabolism comparators reports sparse or null postmitotic nuclear RNA responses rather than a shared PDC/TCA transcriptional program:

   - Pdha1, Dlat, Dld, and Mpc1 immediately bracket mitochondrial pyruvate entry and the PDC, but Pdha1/Dlat/Dld/Mpc1 and neighboring TCA targets were flat or singleton-only.
   - Dlat had a narrow Jarid2 response at the looser FDR<0.10 reporting layer, but canonical PDC/TCA comparators did not phenocopy it in `151`.
   - Aco2, Dld, Mpc1, Ogdh, and Pdha1 Claims jointly support a broad interpretation that represented mitochondrial carbon-entry, PDC, TCA, DLD-linked, and Fe-S perturbations generally fail to induce a coherent nuclear DE module in this atlas, with only isolated target-specific exceptions.

4. The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` gives the following strict focal counts for a manually chosen PDC/TCA/BCAA/OXPHOS-adjacent cohort:

   | target | n_degs |
   | --- | ---: |
   | Aco2 | 0 |
   | Bckdhb | 0 |
   | Bckdk | 0 |
   | Dlat | 1 |
   | Dld | 0 |
   | Dlst | 0 |
   | Idh3a | 1 |
   | Mdh2 | 1 |
   | Mpc1 | 0 |
   | Ndufs4 | 0 |
   | Ogdh | 0 |
   | Pdha1 | 1 |
   | Sdha | 1 |
   | Sucla2 | 1 |
   | Suclg1 | 0 |

   This cohort has 6 DEGs across 15 perturbations, mean `0.4`, median `0`, and 9/15 complete zeros.

5. A direct Parquet query over the same 15 training perturbations in `151 TH Prkcd Grin2c Glut` found exactly six `pvals_adj < 0.05` rows, and every one was the self-target transcript: `Dlat`, `Idh3a`, `Mdh2`, `Pdha1`, `Sdha`, and `Sucla2`. Thus the count of 1 for the nearest measured PDC subunits at this stricter endpoint is explained by occasional detectable self-RNA reduction, not by a downstream metabolic stress program.

6. A run-local symmetric profile comparison of the 15-node mitochondrial cohort confirmed the lack of a shared expression state: in 105 selected pairs the mean top-tail overlap was only `0.0257` for positive tails and `0.0295` for negative tails, and the significant-program overlap was zero where defined.

Synthesis:

Pdhx is expressed and should be at least partly functionally realized by harvest, so I did not treat it as absent or unperturbable. However, the most adjacent measured genes show that acute mosaic disruption of PDH/TCA carbon flow in recovered postmitotic neurons is usually transcriptionally silent in this focal population. At the exact `p_adj < 0.05` count endpoint, the nearest cohort produced no downstream DEGs; counts above zero came only from self-transcript rows, and detectable self reduction was inconsistent even among essential mitochondrial enzymes.

I therefore forecast no downstream genes and placed the chance of a Pdhx self-row below even odds. The resulting point prediction is:

`predicted_n_degs = 0`
