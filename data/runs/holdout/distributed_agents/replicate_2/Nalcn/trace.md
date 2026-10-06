# Trace

## Question

The held-out endpoint is the number of genes with `pvals_adj < 0.05` after each
held-out CRISPR perturbation in `151 TH Prkcd Grin2c Glut` cells. The manifest
for this run contains one target, `Nalcn`, so the output is a single
integer-valued prediction for the same focal cell group and the same FDR 0.05
counting rule as
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.

I treated `n_degs` as the assay-specific count of all significant measured
genes, including the perturbed gene if its own transcript passed FDR. I did not
interpret a target self-transcript decrease as editing efficiency or use it to
upweight a biological phenotype; it matters only because the requested endpoint
counts that row when it is significant.

## Sources Used

- Raw training endpoint counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Raw DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Held-out manifest:
  `[local file: 143_Nalcn.csv]`.
- Distributed Agents same-experiment semantic corpus,
  release `perturbai-july-260713-sourceguard-1773-v1`. This release had no
  direct `Nalcn` Finding or Claim, so I used it for training-target reports and
  for claims about the calcium-, sodium-, KCNQ-, and ATPase-neighborhood
  surfaces.
- Distributed Agents Runtime observed-profile tools. I ran a focal
  `151 TH Prkcd Grin2c Glut` profile comparison over the training ion-channel
  and ion-homeostasis cohort and inspected the resulting bounded flat tables:
  `profile_compare_ion_channel_cohort.json`,
  `profile_inspect_sodium.json`, `profile_inspect_calcium.json`,
  `profile_inspect_k_hcn.json`, and `profile_inspect_broad_refs.json`.
- NCBI PubMed literature for external NALCN biology:
  Lu et al. 2007, Cell, DOI `10.1016/j.cell.2007.02.041`, PMID `17448995`;
  Lu et al. 2010, Neuron, DOI `10.1016/j.neuron.2010.09.014`,
  PMID `21040849`; Chua et al. 2020, Science Advances,
  DOI `10.1126/sciadv.aaz3154`, PMID `32494638`; Wie et al. 2020,
  Nature Communications, DOI `10.1038/s41467-020-17105-8`,
  PMID `32620897`; Kschonsak et al. 2021, Nature,
  DOI `10.1038/s41586-021-04313-5`, PMID `34929720`; Wu et al. 2024,
  Anesthesiology, DOI `10.1097/ALN.0000000000005015`, PMID `38625708`.

## Computational Checks

I first loaded the requested-target CSV and verified that it contained exactly
one target, `Nalcn`.

For the training count table I computed the empirical calibration of the focal
endpoint:

- 1,674 training perturbations.
- Median `n_degs` = 0.
- 75th percentile = 1.
- 90th percentile = 2.
- 95th percentile = 18.
- 469/1,674 training targets had any FDR 0.05 hit.

I then pulled focal DE rows for biologically relevant represented analogs from
the parquet by filtering
`group_name == "151 TH Prkcd Grin2c Glut"`, `gene_target in analog_set`, and
`pvals_adj < 0.05`. This established which singleton counts were just the
target transcript and which targets had downstream genes. Finally, I compared
the full 17,259-gene focal log-fold-change profiles for the observed sodium,
calcium, KCNQ/BK, HCN, NMDA, and ATPase perturbations. That comparison was used
as a falsification step: weak whole-profile correlations and modest top-tail
overlaps did not reveal a reusable NALCN-like channel module that should
override the exact DEG counts.

## Nalcn

### External Function

`Nalcn` encodes a nonselective sodium leak channel that contributes a
TTX- and cesium-resistant background Na current and helps set neuronal resting
membrane potential. Germline `Nalcn` mutant mice have disrupted respiratory
rhythm and neonatal lethality, and cultured mutant hippocampal neurons lose the
background Na leak current and fire less (Lu et al. 2007, PMID `17448995`).
The pore requires the auxiliary proteins FAM155A, UNC79, and UNC80 for robust
function; UNC79/UNC80 are large cytoplasmic channelosome components required
for NALCN localization and gating (Lu et al. 2010, PMID `21040849`; Wie et al.
2020, PMID `32620897`; Chua et al. 2020, PMID `32494638`; Kschonsak et al.
2021, PMID `34929720`). The outside thalamic literature is mechanistically
consistent with relevance to the focal thalamic glutamatergic class:
virus-mediated NALCN knockdown in paraventricular thalamic glutamatergic
neurons reduced neuronal activity and delayed emergence from sevoflurane
anesthesia (Wu et al. 2024, PMID `38625708`).

### Training Perturbations Considered

The cleanest analogs, the same channelosome subunits `Unc79`, `Unc80`,
`Fam155a`, and `Fam155b`, were absent from the focal training count table.
Therefore I used represented channels and ion-homeostasis genes as imperfect
proxies:

| training target(s) | focal FDR 0.05 DEG counts | expression-pattern evidence | interpretation for `Nalcn` |
| --- | ---: | --- | --- |
| `Cacna1g` | 12 | The 12 significant genes included `Cacna1g` itself, `Ptprn`, `Stmn4`, `Cpne7`, `Ly6e`, `Jun`, `Zdhhc22`, `Iyd`, `Lrrc7`, `Serpine2`, `Notum`, and `Irag1`. The Distributed Agents corpus also reported that this was a narrow thalamic `151` response at FDR 0.10, not a pan-neuronal stress program. | Best same-cell positive counterexample: an ion channel that is central in thalamic electrophysiology can make a real but small nuclear RNA footprint. It is a voltage-gated T-type calcium channel, not a leak Na channel or NALCN-complex member, so I treated 12 as an upper neighborhood value rather than as a direct estimate. |
| `Cacna1a`, `Cacna1d`, `Cacna1e`, `Cacna2d1`, `Cacna2d2`, `Cacnb2`, `Cacnb4`, `Cacng2`, `Cacng3` | 0, 0, 0, 1, 0, 0, 1, 0, 0 | The only `Cacna2d1` FDR 0.05 hit in the focal class was `Cacna2d1` itself; the other represented CaV pore and auxiliary perturbations were flat or singleton. The corpus claim for the same family explicitly rejected a generic CaV-family transcriptional module. | Channel-family or complex membership alone is usually insufficient in this assay. This pushed the estimate far below the broad Grin1/Atp1a3 range. |
| `Scn1a`, `Scn1b`, `Scn2a`, `Scn3a`, `Scn8a` | 1, 2, 1, 0, 1 | `Scn1a`, `Scn2a`, and `Scn8a` were self-transcript-only singletons; `Scn1b` added `Jun` as one downstream gene; `Scn3a` was zero. The profile comparison kept these signatures in the `0_to_9` DEG or null response class. | The closest sodium-channel family targets did not produce downstream excitability remodeling in `151`. NALCN is mechanistically different from voltage-gated sodium channels, but this is strong evidence against predicting dozens of DEGs for another sodium conductance. |
| `Kcnq2`, `Kcnq3`, `Kcnma1`, `Hcn1`, `Hcn2` | 1, 1, 1, 0, 1 | Each positive call was the perturbed channel transcript itself. In the cohort profile comparison, these targets did not cluster into a high-DEG expression module, and the Distributed Agents KCNQ/Kv claims described sparse, paralog-specific outputs rather than a shared channel-loss program. | These are resting-potential or excitability comparators. Their focal counts make a pure zero or self-only outcome more likely than a broad NALCN nuclear response. |
| `Grin1` | 89 | `Grin1` had 89 focal FDR 0.05 genes with both synaptic-gene down-regulation and growth/stress-linked up-regulation; the corpus described a dominant but subunit-specific thalamic NMDAR response. | `Grin1` proves that `151` can mount an electrophysiology-linked thalamic response, but NMDAR loss gates synaptic calcium and plasticity programs much more directly than a leak channel, so it is a positive counterexample rather than a numerical analog. |
| `Atp1a1`, `Atp1a2`, `Atp1a3`; `Atp2a2`, `Atp2b1` | 1, 0, 80; 187, 22 | `Atp1a3` remodeled ion-channel and secretory transcripts in `151`, while `Atp1a1` and `Atp1a2` did not phenocopy it. `Atp2a2` and `Atp2b1` were broader calcium-pump exceptions. | Loss of core ion pumps can create a much wider homeostatic or ER-stress state, but the strong responses are pump- and stress-specific. I did not transfer their high counts to `Nalcn`. |

### Decision

The evidence separates two claims:

1. `Nalcn` is likely to be biologically engaged in thalamic glutamatergic
   neurons because the channel directly controls resting Na leak current and
   thalamic neuronal excitability.
2. In this exact postnatal sparse CRISPR snRNA-seq endpoint, represented
   channels near membrane excitability usually produced zero or a singleton
   self-transcript hit in `151 TH Prkcd Grin2c Glut`.

Because the true same-complex partners were absent, I did not assign a
`Cacna1g`-like 10-plus-gene count. Because NALCN is an expressed thalamic
leak-channel pore rather than an unrelated buffered voltage-gated subunit, I
also did not make the call a strict zero. The most defensible point estimate is
therefore a self/narrow singleton response:

`Nalcn`: predicted `n_degs = 1`.

## Limits

- The held-out `Nalcn` perturbation itself and the NALCN-channelosome genes
  `Unc79`, `Unc80`, `Fam155a`, and `Fam155b` were not represented in the
  training endpoints, so there is no same-complex empirical calibration.
- The Distributed Agents corpus had no direct same-experiment `Nalcn` Finding or Claim;
  its evidence here is entirely from neighboring training perturbations.
- Most outside NALCN studies measured currents, respiratory neurons,
  paraventricular thalamic excitability, or structure rather than juvenile
  mosaic CRISPR in the focal Allen taxonomy group. Those papers establish
  plausibility of engagement, not the number of snRNA-seq DEGs after 3-4 weeks.
- Whole-profile similarities among nearly flat perturbations are dominated by
  thousands of non-significant genes. I used those comparisons only to reject a
  hidden coherent ion-channel module, not to average the signatures.
- The prediction may be wrong in either direction: an undetected Nalcn
  transcript drop would make the right endpoint zero, while a focal thalamic
  homeostatic state analogous to `Cacna1g` could create several downstream hits.
