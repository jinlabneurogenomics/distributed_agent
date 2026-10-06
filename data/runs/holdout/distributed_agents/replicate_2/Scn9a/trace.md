# Scn9a held-out DEG-count prediction

## Question and interpretation

The manifest `202_Scn9a.csv` requested one held-out perturbation:

| target_name | predicted_n_degs |
|---|---:|
| Scn9a | 0 |

I interpreted `n_degs` exactly as in the training endpoint: the number of measured genes in `151 TH Prkcd Grin2c Glut` with `pvals_adj < 0.05` in the Wilcoxon differential-expression table, including the target transcript itself if it was measured and passed FDR. `Scn9a` was absent as a perturbed `gene_target`, so there is no observed Scn9a knockout signature in the parquet; rows where `names == "Scn9a"` under other perturbations were used only to check whether the transcript behaved detectably in the focal group.

## Sources used

- Differential-expression table: `[local file: training_de_all_cell_groups.parquet]`.
- Focal training counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Held-out manifest: `[local file: 202_Scn9a.csv]`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, queried for `Scn1a`, `Scn1b`, `Scn2a`, `Scn3a`, `Scn8a`, and sodium-channel claims.
- Distributed Agents runtime profile comparison, schema `distributed_agents-node-profile-comparison-v10`, used to compare the focal-cell log2 fold-change vectors of `Scn1a`, `Scn1b`, `Scn2a`, `Scn3a`, and `Scn8a`.
- PubMed literature:
  - Nassar et al. 2004, PNAS, DOI `10.1073/pnas.0404915101`, PMID `15314237`: nociceptor-specific mouse Nav1.7 deletion increased mechanical and thermal pain thresholds and suppressed inflammatory pain responses, supporting a peripheral nociceptor-centered loss-of-function phenotype.
  - Cox et al. 2006, Nature, DOI `10.1038/nature05413`, PMID `17167479`: homozygous human SCN9A nonsense mutations abolish Nav1.7 currents and cause congenital inability to experience pain.
  - Lein et al. 2006, Nature, DOI `10.1038/nature05453`, PMID `17151600`: Allen Mouse Brain Atlas in situ expression resource, used as a general adult-mouse brain-expression reference.

## Computations over the input data

- Confirmed the held-out manifest contains only `Scn9a`.
- Read the 1,674-row focal training-count CSV. It is zero-heavy: 1,205 perturbations had `n_degs = 0`, 469 had at least one DEG, the median was 0, the 75th percentile was 1, and the maximum was 2,677.
- Queried the parquet with `group_name = '151 TH Prkcd Grin2c Glut'`. The focal slice has 28,891,566 rows: 1,674 training perturbations x 17,259 measured genes.
- Tabulated voltage-gated sodium-channel and nearby excitability targets in the focal training counts. The represented Nav genes were:

| training target | focal n_degs | focal expression-pattern evidence |
|---|---:|---|
| Scn1a | 1 | The sole FDR hit was the self transcript, `Scn1a`, log2FC -1.075, FDR 5.87e-38. `Scn9a` in this perturbation had FDR 1.0. |
| Scn1b | 2 | The two FDR hits were the self transcript, `Scn1b`, log2FC -1.436, FDR 7.36e-70, and `Jun`, log2FC +0.518, FDR 0.0156. `Scn9a` had FDR 1.0. |
| Scn2a | 1 | The sole FDR hit was the self transcript, `Scn2a`, log2FC -0.401, FDR 6.46e-06. `Scn9a` had FDR 1.0. |
| Scn3a | 0 | No measured gene passed FDR 0.05 in the focal group. |
| Scn8a | 1 | The sole FDR hit was the self transcript, `Scn8a`, log2FC -0.458, FDR 1.34e-05. `Scn9a` had FDR 1.0. |

- Compared those five represented sodium-channel signatures with the Distributed Agents profile tool over the same 17,259 focal features. Their significant-feature counts were 1, 2, 1, 0, and 1, matching the CSV. No pair shared a significant positive or negative feature at FDR 0.05; the continuous tail overlaps were low and dominated by nonsignificant extreme log-fold-change rows, so there was no hidden recurrent Nav-family module to project onto `Scn9a`.
- Checked counterexample excitability and synaptic genes in the same focal count table. Several ionic or synaptic perturbations are detectable when they remodel these thalamic neurons: `Cacna1g` had 12 DEGs, `Grin1` had 89, `Atp1a3` had 80, and `Atp2a2` had 187. Therefore the near-zero Nav counts are not just a global failure of the focal group or the Wilcoxon/FDR workflow to call channel-related responses.

## Same-experiment corpus evidence

The Distributed Agents corpus had no target-scoped finding for the held-out `Scn9a`, which is expected because it was fully withheld.

The relevant same-experiment claim for the measured analogs was `claim:c242237a097b38ee7b64`: perturbations of represented Nav-channel subunits and intracellular FHF modulators produced sparse, target- and cell-context-specific neuronal RNA responses rather than a shared pan-Nav or Nav-complex transcriptional module. This claim was supported by:

- `Scn1a:F003`: `Scn1b`, `Scn2a`, `Scn3a`, `Scn8a`, and `Fgf13` failed to phenocopy `Scn1a` in the sparse `Scn1a` responder GABAergic groups.
- `Scn1b:F006`: canonical Nav alpha subunits did not phenocopy the beta1 perturbation, even though beta1 associates with Nav1.1/Nav1.2/Nav1.3/Nav1.6.
- `Scn2a:F004`: `Scn1a`, `Scn1b`, `Scn3a`, and `Scn8a` did not share `Scn2a` downstream genes.
- `Scn3a:F002` and `Scn8a:F003`: the already narrow `Scn3a` and `Scn8a` surfaces were nonconvergent with the measured sodium-channel relatives.

Those reports matter for the held-out prediction because `Scn9a` is another voltage-gated sodium-channel alpha subunit, but the directly observed central Nav genes already show that biochemical family membership does not create a broad 3-4 week postnatal snRNA-seq signature.

## Target-specific prediction

### Scn9a

`Scn9a` encodes Nav1.7, a voltage-gated sodium-channel alpha subunit. The closest in-dataset alpha-subunit paralogs were `Scn1a`, `Scn2a`, `Scn3a`, and `Scn8a`; the closest assayed beta partner was `Scn1b`. In the requested `151 TH Prkcd Grin2c Glut` group these analogs sat at 0-2 DEGs, and nearly every FDR call was direct depletion of its own transcript. The strongest central-brain alpha-subunit analogs, `Scn2a` and `Scn8a`, each had a target-self call but no downstream FDR genes. The fetal/developmental paralog `Scn3a` was completely silent. `Scn1a`, though critical in inhibitory channelopathy biology, was also only a self hit in the focal thalamic glutamatergic group.

The appropriate counterexamples are the focal responses to `Cacna1g`, `Grin1`, `Atp1a3`, and `Atp2a2`. They show that this cell group can produce a detectable thalamic excitability or calcium-stress RNA program, so I should not simply round every channel to zero. However, the Nav-family pattern is consistently much flatter than those non-Nav ionic perturbations, and the Distributed Agents corpus explicitly warns that the represented Nav/FHF genes do not form a pan-Nav transcriptional module.

External gene-function knowledge further pushes `Scn9a` below the represented CNS Nav alpha genes. Nav1.7 loss of function has a very strong phenotype in peripheral damage-sensing neurons: conditional Scn9a loss in Nav1.8-positive nociceptors reduces mouse pain behaviors (Nassar et al. 2004), and human biallelic nonsense SCN9A alleles eliminate Nav1.7 currents and cause congenital inability to experience pain (Cox et al. 2006). Those are essential electrical phenotypes, but they are outside the core compartment sampled here: NeuN-positive postnatal brain nuclei from whole brain minus olfactory bulb and hindbrain, with non-neuronal and peripheral sensory neurons absent. The Allen Mouse Brain Atlas context also makes a broad thalamic `Scn9a` RNA effect less plausible than a response to `Scn1a`, `Scn2a`, or `Scn8a`, which are central neuronal channel genes and still produced only self or zero DEGs in the exact focal group.

The held-out target transcript itself is the only plausible DEG for a very weak channel perturbation. I predicted zero rather than one because `Scn9a` is not a core thalamic glutamatergic sodium-channel transcript, and measured `Scn9a` rows under the assayed `Scn1a`, `Scn1b`, `Scn2a`, `Scn3a`, and `Scn8a` perturbations all had focal FDR 1.0. Unlike `Scn1a`, `Scn2a`, and `Scn8a`, I do not expect enough baseline `Scn9a` mRNA in this cell group for the CRISPR self-depletion row to clear FDR.

Final point prediction: `Scn9a -> 0`.

## Limits and extrapolation

- `Scn9a` was fully held out, so the prediction is an extrapolation from paralogs and pathway context, not a measured profile.
- The matched analogs are imperfect. `Scn1a`, `Scn2a`, `Scn3a`, and `Scn8a` encode other sodium-channel alpha subunits with different developmental timing, subcellular localization, and cell-type enrichment; `Scn1b` is a beta subunit and adhesion molecule rather than a pore-forming alpha subunit.
- The experiment measured steady-state nuclear RNA 3-4 weeks after sparse P16 CRISPR loss. It did not measure DNA indels, Nav1.7 protein, axonal localization, membrane currents, spike threshold, pain circuitry, or edited-cell viability.
- A zero predicted count does not mean Nav1.7 is biologically unimportant. It means I expect no measured nuclear transcript in this focal thalamic cell group to pass BH-adjusted Wilcoxon FDR 0.05 under this sparse juvenile brain perturbation design.
