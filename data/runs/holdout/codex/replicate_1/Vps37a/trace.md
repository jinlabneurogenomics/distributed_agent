# Vps37a direct DEG-count forecast

## Target and endpoint

- Target manifest: `Vps37a`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: count of measured genes in the focal population with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Declared target signature and target count were not used; the target was absent from the declared training count table and training DE parquet.

## Biology used

The declared biology bundle supports substantial on-assay reach but only a moderate expectation of a survivor transcriptional aftershock.

- `Vps37a` was exactly measured in the focal non-target thalamic population with `97.8209%` of non-target nuclei expressing it, mean raw UMI `5.1237`, mean log1p-CP10K `1.3715`, and pseudobulk CPM `321.123`. This makes the target transcript observable in this cell class, while not by itself establishing editing efficiency.
- The functional-stock adjudication called VPS37A a dynamic ESCRT-I component whose stock should be `likely_substantially_depleted` over the P16 to P37-P44 window.
- Source-card facts place VPS37A in ESCRT-I endosomal sorting and receptor down-regulation, and give the VPS37A N-terminal UEVL region a separable ESCRT-dependent autophagosome-closure role.
- A Vps37a UEVL-domain mouse mutant produced neurological abnormalities and brain pathology by the postnatal period, with inflammatory markers elevated at about two weeks; that supports neural relevance within the Perturb-seq window but is germline, systemic, domain-selective, and not thalamus-specific.
- Redundancy remains unresolved: VPS37B-D are alternative VPS37-family components of ESCRT-I, and no matched juvenile thalamic-neuron experiment in the bundle proves or excludes compensation for Vps37a loss.

## Training measurements used

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contains 1,674 observed training perturbations in the focal class. Its distribution is sharply zero-inflated:

- `1,205 / 1,674` have `0` DEGs.
- `1,512 / 1,674` have at most `2` DEGs.
- `1,596 / 1,674` have at most `20` DEGs.
- The mean is `14.054`, but the median is `0`; the top few high-burden perturbations dominate the mean.

I used endosomal, lysosomal, autophagy, and VPS-trafficking training perturbations as the closest observed comparators. Their exact focal-class counts at `pvals_adj < 0.05` were:

| training perturbation | focal n_degs |
| --- | ---: |
| Atg16l1 | 0 |
| Atg5 | 0 |
| Becn1 | 0 |
| Chmp4b | 0 |
| Lamp2 | 0 |
| Vps35l | 0 |
| Vps41 | 0 |
| Vps53 | 0 |
| Sqstm1 | 1 |
| Rb1cc1 | 4 |
| Vps35 | 17 |
| Vps54 | 31 |
| Rab7 | 501 |

The underlying Parquet rows confirmed these counts in `151 TH Prkcd Grin2c Glut`, with 17,259 measured features per selected comparator and matched perturbed-nucleus counts ranging from 93 to 259 for this comparator panel.

## Same-experiment corpus context

The corpus findings are a semantic layer over the same experiment, not an independent replicate. I used them only to interpret the training counts.

- `Chmp4b` had no robust recurrent ESCRT/autophagy/cargo transcriptional signature.
- `Atg5`, `Atg16l1`, `Becn1`, `Lamp2`, `Rb1cc1`, and `Sqstm1` findings repeatedly described sparse or uncoupled autophagy/lysosomal responses rather than a common stress module.
- `Vps35l`, `Vps41`, and `Vps53` were also sparse or flat in the focal thalamic class.
- `Vps35` and `Vps54` showed modest 151-TH-biased signatures.
- `Rab7` was the clear exception, producing a broad late-endosomal/lysosomal, sterol/lipid, proteasome, and stress response; Vps35 and Vps54 reports both described only partial overlap with Rab7 rather than full phenocopy.

## Synthesis

`Vps37a` is expressed enough, and the biology bundle makes a null edit plausible by harvest, so I did not treat the target as uneditable or out of reach. The measured training perturbations argue against transferring a large generic autophagy/endolysosomal program: direct autophagy nodes, `Chmp4b`, `Lamp2`, `Vps35l`, `Vps41`, and `Vps53` were 0 in the exact focal count table, while `Sqstm1` and `Rb1cc1` were only 1 and 4. I treated `Rab7 = 501` as an outlying hub phenotype at the late-endosome/autolysosome intersection, not as the expected effect size for a family-exchangeable ESCRT-I VPS37 subunit.

Balancing the high exact Vps37a transcript reach and likely stock depletion against the mostly flat pathway-proximal training evidence, I placed the target just above a hard zero and below the modest `Vps35`/`Vps54` signatures.

Predicted `n_degs`: `1`
