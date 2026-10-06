# Ophn1 DEG-count prediction

## Question and endpoint

The requested held-out perturbation set contains one target, `Ophn1`. I
interpreted the endpoint as the exact focal-cell readout in
`151 TH Prkcd Grin2c Glut`: the number of measured genes, including the target
transcript itself if it passes the threshold, with Benjamini-Hochberg-adjusted
Wilcoxon `pvals_adj < 0.05`.

The held-out `Ophn1` perturbation is absent from both supplied training inputs,
so I predicted it by transferring from assayed perturbations in the same
Perturb-seq experiment. The only ambiguity that materially affects this target
is whether a singleton FDR hit should be expected from guide-induced depletion
of `Ophn1` mRNA itself even if the downstream RhoGAP program is silent. I did
not use target-RNA loss as an editing-efficiency score, but I did allow that it
can contribute one gene to this particular count because the training count CSV
does include self hits.

## Sources used

- Local training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Local DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested-target manifest:
  `[local file: 162_Ophn1.csv]`
- Distributed Agents same-experiment semantic corpus,
  `perturbai-july-260713-sourceguard-1773-v1`, via `target_context`.
- Distributed Agents runtime profile tools, via `profile_compare` and `profile_inspect`,
  to compare full focal-cell log-fold-change signatures for hand-selected
  RhoGAP/RhoGEF/GTPase, PAK/LIMK, WRC, and synaptic-scaffold perturbations.
- NCBI PubMed, via `bioeval_literature`, for external OPHN1 mechanism papers.

The filtered same-experiment corpus had no `Ophn1` record, so all corpus
evidence below comes from non-held-out analogs rather than from the hidden
target itself.

## Local computations

1. I read the requested-target CSV and confirmed that it contains only
   `Ophn1`.
2. I summarized the focal training counts. The distribution is very sparse:
   among 1,674 training perturbations, 469 have `n_degs > 0`; the median is 0,
   the 75th percentile is 1, the 95th percentile is 18, and the maximum is
   2,677. That makes a zero or singleton prediction the calibrated prior for a
   buffered signaling perturbation.
3. I inspected the exact focal counts for candidate analogs. The most relevant
   observed Rho-family and synaptic actin perturbations were all 0 to 2 DEGs:

   | training target | focal `n_degs` | why inspected |
   | --- | ---: | --- |
   | `Arhgap32` | 0 | neuronal RhoGAP, postsynaptic/trafficking analog |
   | `Arhgap18` | 0 | RhoGAP counterexample |
   | `Arhgef9` | 1 | Cdc42/RhoGEF and inhibitory synapse organizer |
   | `Cdc42` | 1 | direct small-GTPase effector axis |
   | `Rac1` | 0 | direct small-GTPase effector axis |
   | `Kalrn` | 0 | Rac/RhoGEF at excitatory synapses |
   | `Tiam1` | 0 | RacGEF at excitatory synapses |
   | `Dock3` | 0 | RacGEF |
   | `Fgd4` | 0 | Cdc42 GEF family member |
   | `Pak1`, `Pak2`, `Pak3` | 1, 0, 0 | group-I PAK effectors of Rac/Cdc42 |
   | `Limk1`, `Cfl2` | 0, 0 | PAK/LIMK/cofilin actin branch |
   | `Cyfip1`, `Cyfip2` | 0, 1 | WAVE-regulatory-complex / FMRP-associated actin branch |
   | `Fmr1`, `Syngap1`, `Dlg4`, `Dlgap4`, `Shank3` | 0, 0, 1, 2, 2 | synaptic ID scaffolds and boundary comparators |

4. I filtered the parquet to `group_name == '151 TH Prkcd Grin2c Glut'` and
   these candidate targets to find the material FDR hits and target self rows.
   Among the selected Rho/actin/synapse candidates, the FDR-significant focal
   rows were:

   | perturbation | significant focal row(s) |
   | --- | --- |
   | `Arhgef9` | self only, log2FC -0.571, q = 3.7e-8 |
   | `Cdc42` | self only, log2FC -0.593, q = 8.6e-5 |
   | `Cyfip2` | self only, log2FC -0.489, q = 4.4e-11 |
   | `Dlg4` | self only, log2FC -0.444, q = 1.1e-8 |
   | `Dlgap4` | self plus `Vgf` |
   | `Pak1` | self only, log2FC -0.599, q = 5.0e-8 |
   | `Shank3` | self plus `Uba5` |

   In contrast, direct Ophn1-pathway analogs with matched recovery of roughly
   150-200 perturbed nuclei, including `Arhgap32`, `Arhgap18`, `Rac1`,
   `Kalrn`, `Dock3`, `Limk1`, `Pak2`, and `Pak3`, had zero focal DEGs.
5. I verified that `Ophn1` was an output gene in the focal group for all 1,674
   training perturbations, so an Ophn1 self row would have been scorable in the
   hidden perturbation.
6. I used Distributed Agents runtime `profile_compare` on 18 mechanistically nominated
   training targets in the focal group
   (`Arhgap32`, `Arhgap18`, `Arhgef9`, `Cdc42`, `Rac1`, `Kalrn`, `Fmr1`,
   `Syngap1`, `Shank3`, `Cyfip1`, `Cyfip2`, `Dock3`, `Limk1`, `Pak1`, `Pak2`,
   `Pak3`, `Dlg4`, `Dlgap4`). The 18-node cohort had 11 nodes with no
   significant focal features and 7 with only 1-9 significant features. A
   focused inspection of `Arhgap32`, `Arhgap18`, `Arhgef9`, `Cdc42`, and
   `Rac1` against `Kalrn`, `Fmr1`, `Syngap1`, `Shank3`, `Cyfip1`, `Cyfip2`,
   `Dock3`, `Limk1`, `Pak1`, and `Pak2` found no shared significant
   non-self DEG set among the core Rho nodes. The whole-profile Pearson and
   cosine values between these nearly flat vectors were high but nonspecific,
   while the FDR-level overlaps and nearest-neighbor gene lists were consistent
   with null or self-only signatures; I therefore used the profile artifact as
   a boundary check, not as a quantitative averaging model.

## Same-experiment analog evidence

The most relevant corpus records were all on assayed analogs:

- `Cdc42`: the corpus summarizes `Cdc42` as having no robust downstream
  transcriptional response in any recovered neuronal class and explicitly
  states that represented Rho/Rac/Cdc42-axis relatives did not form a shared
  Cdc42-like module. The compared relatives included `Rac1`, `Pak1`, `Pak2`,
  `Pak3`, `Limk1`, `Cfl2`, `Cyfip1`, `Cyfip2`, `Tiam1`, `Kalrn`, `Dock3`,
  `Fgd4`, `Arhgap18`, `Arhgap32`, and `Arhgef9`.
- `Rac1`: the only reported experiment-wide FDR event was a sparse
  Sst-restricted `Ranbp1` response, and its `Rac1:F003` finding rejected a
  shared Rac/Cdc42/PAK/WRC/GEF/GAP transcriptional module.
- `Kalrn`: five findings treated acute `Kalrn` loss as FDR-flat across 22
  neuronal groups, with no detectable Rac1/PAK/LIMK or PSD/NMDAR feedback
  program. In the focal training endpoint `Kalrn` had 0 DEGs.
- `Arhgap32`: four findings treated `Arhgap32` as pan-surface negative and
  divergent from represented NMDAR, postsynaptic-density, GABA_A receptor, and
  Rho-GTPase perturbations. This is a close counterexample because it is also a
  neuronal RhoGAP with synaptic-trafficking disease biology, yet in the focal
  group its self row was nonsignificant and its count was 0.
- `Arhgap18` and `Arhgef9`: the corpus annotated `Arhgap18` as almost
  completely buffered and `Arhgef9` as downstream-null despite target
  transcript depletion. They show that a single RhoGAP or RhoGEF lesion can be
  functionally meaningful without inducing a multi-gene nuclear RNA response.
- `Pak1`: the group-I PAK findings show singleton, cell-type-restricted output
  and divergence among `Pak1`, `Pak2`, and `Pak3`, arguing against simply
  transferring a Rac/Cdc42 effector response to every upstream GAP.

There were two useful counterclasses. Direct ion-channel/NMDAR or core
structural perturbations can be seen in this focal class, for example `Grin1`
with 89 DEGs, `Ctnnb1` with 383, and `Dctn1` with 75. Ophn1 is downstream or
local to cytoskeletal/endocytic signaling rather than an ionotropic receptor
subunit or beta-catenin/dynactin node, so I used these as evidence that the
assay can respond in thalamic glutamatergic neurons, not as positive Ophn1
analogs.

## External Ophn1 biology

OPHN1 encodes a BAR-domain RhoGAP whose human loss-of-function mutations cause
X-linked intellectual disability. Billuart et al. 1998 identified OPHN1 as a
RhoGAP gene at Xq12 and proposed that loss of a Rho-GTPase activating protein
would dysregulate Ras/Rho-like signaling (Nature, DOI `10.1038/31940`, PMID
`9582072`). Govek et al. 2004 then showed that oligophrenin-1 is required for
dendritic spine morphogenesis in hippocampal neurons through RhoA/ROCK
signaling and interacts with the postsynaptic adaptor Homer (Nature
Neuroscience, DOI `10.1038/nn1210`, PMID `15034583`). Khelfaoui et al. 2009
showed that Ophn1 disruption impairs clathrin-mediated endocytosis, synaptic
vesicle retrieval, AMPA receptor internalization, and hippocampal LTD through
excess RhoA/ROCK signaling that can be rescued with ROCK inhibition (Human
Molecular Genetics, DOI `10.1093/hmg/ddp189`, PMID `19401298`).
Nakano-Kobayashi et al. 2009 placed OPHN1 at presynaptic vesicle endocytosis
through endophilin A1 and its RhoGAP activity (Current Biology, DOI
`10.1016/j.cub.2009.05.022`, PMID `19481455`).

Those studies make `Cdc42`, `Rac1`, `Pak1/2/3`, `Limk1`, `Cfl2`, `Kalrn`,
`Tiam1`, `Dock3`, `Arhgap18`, `Arhgap32`, `Arhgef9`, `Fmr1`, `Dlg4`,
`Dlgap4`, and `Shank3` mechanistically appropriate training comparators or
boundaries. They also caution that the most proximal Ophn1 phenotypes are
GTP-bound RhoA, ROCK/cofilin signaling, actin architecture, receptor or
vesicle endocytosis, spine morphology, and synaptic physiology, none of which
is measured directly by the basal snRNA-seq Wilcoxon endpoint.

## Target-specific decision

### Ophn1

My prediction is `0` DEGs.

The within-dataset evidence argues for no robust downstream focal program.
`Arhgap32` is the best single assayed analog: it is a neuronal RhoGAP with
synaptic receptor-trafficking biology, and it produced 0 focal DEGs with
`Arhgap32` itself nonsignificant. `Arhgap18`, a second RhoGAP, also produced
0 focal DEGs. The core GTPase and effector nodes in the same local pathway were
also zero or self-only: `Rac1` 0, `Cdc42` 1 self-only, `Kalrn` 0, `Tiam1` 0,
`Dock3` 0, `Limk1` 0, `Pak1` 1 self-only, `Pak2` 0, and `Pak3` 0. `Cyfip1/2`,
`Fmr1`, and the PSD scaffold genes provide synaptic-actin boundaries rather
than stronger positive support: `Cyfip1` was 0, `Cyfip2` was self-only,
`Fmr1` and `Syngap1` were 0, and `Dlg4`, `Dlgap4`, and `Shank3` were at most
two genes.

External biology says Ophn1 loss should affect RhoA/Rac/Cdc42 cycling,
endocytosis, and spines. The local dataset says that these post-translational
and structural branches are usually buffered at the nuclear RNA level after
acute P16 mosaic loss of a single component. I therefore expect any Ophn1
effect in `151 TH Prkcd Grin2c Glut` to be at the same scale as `Arhgap32`,
`Arhgap18`, and `Kalrn`, not at the `Grin1` or `Ctnnb1` scale.

I considered assigning `1` to account for possible self-transcript depletion:
several singleton focal counts in this neighborhood are the target gene itself.
I chose `0` because the closest RhoGAP/RhoGEF/GTPase neighbors more often
failed to cross FDR even for self rows, and no non-self Ophn1-like recurrent
feature was visible among the analogs. This is a prediction of a buffered
snRNA-seq surface, not of absent Ophn1 protein function.

## Limits

- The exact RhoA/ROCK nodes most directly downstream of Ophn1 were not
  available as training perturbations, so `Cdc42`, `Rac1`, PAK/LIMK, Kalirin,
  Dock, and other GAP/GEF genes are partial proxies.
- The endpoint includes the target transcript itself. Ophn1 self-depletion is
  intrinsically harder to transfer from unrelated genes because it depends on
  guide cutting, transcript abundance, nonsense-mediated decay, and the
  stability of mutant nuclear RNA. A hidden self hit would move this prediction
  from 0 to 1 even if the biological downstream state is null.
- The PubMed mechanism literature used stronger or different perturbations:
  germline mouse models, RNAi in hippocampal slices, pharmacologic ROCK
  rescue, and direct synaptic assays. Those mechanisms are informative for
  choosing local analogs, but they are displaced from sparse AAV-CRISPR loss in
  postnatal thalamic glutamatergic nuclei.
- Whole-profile log-fold-change correlations among nearly null perturbations
  can be dominated by shared background structure and pseudocount behavior.
  I used them only to check for a missing high-FDR-overlap module.
- Non-neuronal OPHN1 biology, including astrocytic and peripheral functions,
  is mostly outside this NeuN-enriched whole-brain assay and did not influence
  the focal neuronal count.
