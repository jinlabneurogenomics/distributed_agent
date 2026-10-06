# Trace

## Question interpreted

The task is to predict, for each target in
`[local file: 082_Fth1.csv]`,
the integer number of genes expected to pass `pvals_adj < 0.05` in the held-out
Perturb-seq contrast for `151 TH Prkcd Grin2c Glut` cells. The manifest
contains one target, `Fth1`.

I treated `n_degs` exactly as the training CSV defines it: all measured genes in
the focal cell class whose BH-adjusted Wilcoxon p-value is below 0.05,
including a possible self-target transcript. I did not treat the self row as an
editing-efficiency measurement or as evidence for a downstream biological
program.

## Sources

- Raw same-experiment DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Training endpoint counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Held-out manifest: `082_Fth1.csv`.
- Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`.
  The corpus had no direct `Fth1` claims, as expected for the held-out target,
  but did contain curated claims for represented iron, Fe-S, GPX4, ACSL4, and
  glutathione perturbations.
- Distributed Agents run-local profile tools. I computed signed log-fold-change profile
  comparisons in the exact focal context for iron/ferroptosis candidates present
  in the training set.
- NCBI PubMed for external biology:
  Ferreira et al. 2000, `doi:10.1074/jbc.275.5.3021`, PMID 10652280;
  Ferreira et al. 2001, `doi:10.1182/blood.v98.3.525`, PMID 11468145;
  Mancias et al. 2015, `doi:10.7554/eLife.10308`, PMID 26436293;
  Li et al. 2015, `doi:10.1371/journal.pone.0117435`, PMID 25629408;
  Rui et al. 2020, `doi:10.1111/jpi.12704`, PMID 33206394.

## Computation over the supplied dataset

1. I verified the focal class in the parquet has `28,891,566` rows:
   `1,674` training perturbations times `17,259` measured genes.

2. I summarized the training endpoint distribution. It is highly sparse in this
   cell class:

   - 1,205 of 1,674 perturbations had `n_degs = 0`.
   - 363 had `1 <= n_degs < 10`.
   - 63 had `10 <= n_degs < 100`.
   - 43 had `n_degs >= 100`.
   - The median was 0; the 75th percentile was 1; the 95th percentile was 18.

3. I selected a candidate panel centered on ferritin, iron entry or sensing,
   Fe-S biogenesis, heme/iron handling, NRF2/glutathione, and ferroptosis genes
   that were actually in the training endpoint file:

   `Tfrc`, `Ireb2`, `Abcb7`, `Reps1`, `Acsl4`, `Gpx4`, `Gstm5`, `Gclc`,
   `Gclm`, `Nfs1`, `Isca2`, `Lyrm4`, `Hjv`, `Slc22a17`, `Flvcr1`, `Aco2`,
   with `Nfe2l2` and `Hif1a` as broader counterexamples. Direct ferritin
   paralog perturbations were unavailable: `Fth1` was held out, and `Ftl1` and
   `Ftl2` were not in the focal measured-gene table.

4. For those analogs I read the focal `n_degs`, checked whether any significant
   gene was a self-target transcript, and extracted the significant rows:

   | training target | focal `n_degs` | significant row in `151 TH Prkcd Grin2c Glut` |
   | --- | ---: | --- |
   | `Tfrc` | 0 | none |
   | `Ireb2` | 1 | `Abhd12b` down, logFC -1.18, FDR 1.68e-4 |
   | `Abcb7` | 0 | none |
   | `Reps1` | 0 | none |
   | `Acsl4` | 1 | self only, logFC -0.99, FDR 3.83e-16 |
   | `Gpx4` | 0 | none |
   | `Gstm5` | 0 | none |
   | `Gclc` | 0 | none |
   | `Gclm` | 1 | `Fam91a1` up, logFC 0.56, FDR 0.0358 |
   | `Nfs1` | 0 | none |
   | `Isca2` | 1 | self only, logFC -0.70, FDR 0.0273 |
   | `Lyrm4` | 0 | none |
   | `Hjv` | 0 | none |
   | `Slc22a17` | 1 | self only, logFC -0.78, FDR 8.32e-26 |
   | `Flvcr1` | 0 | none |
   | `Aco2` | 0 | none |
   | `Nfe2l2` | 0 | none |
   | `Hif1a` | 0 | none |

   These contrasts had 90 to 269 matched perturbed nuclei and a common 23,679
   matched controls, comparable to the power expected for this endpoint.

5. I compared signed focal expression profiles for the 16 iron/ferroptosis
   candidates with the run-local `profile_compare` and `profile_cohort` tools,
   using `gene_target` as the node, `names` as the feature, `logfoldchanges` as
   the signed value, and `pvals_adj < 0.05` as the feature-significance
   threshold. Eleven of the 16 had no FDR-significant features and the other
   five had only one. Across all 120 candidate pairs, significant-program
   overlap was either absent or 0, indicating that these nearby perturbations do
   not share a recurrent downstream iron or ferroptosis DEG program in the
   focal cell type.

6. I explicitly checked measured sentinel genes in those same analogs. `Fth1`,
   `Tfrc`, `Ireb2`, `Aco1`, `Ncoa4`, `Slc11a2`, `Slc40a1`, `Hmox1`, `Keap1`,
   `Gpx4`, `Acsl4`, and `Slc22a17` were measured in the focal class. None of
   the candidate iron/Fe-S/GPX4 perturbations significantly changed `Fth1`,
   `Tfrc`, `Ncoa4`, `Slc11a2`, or `Hmox1`; for example, `Fth1` had
   `pvals_adj = 1` in the `Tfrc`, `Ireb2`, `Abcb7`, `Acsl4`, `Gpx4`, `Hjv`,
   `Slc22a17`, `Flvcr1`, and `Aco2` contrasts. This argues against a broad
   canonical iron-starvation, iron-overload, or NRF2 response being visible as a
   focal nuclear RNA state here.

## Same-experiment corpus evidence

I used the curated Distributed Agents corpus as interpretation of this same Perturb-seq
experiment, not as independent replication.

- Claim `claim:33d0bbb59a299fb02219` reports that acute perturbation of
  represented iron-entry, IRP2, Fe-S/heme-adjacent, and TfR-recycling-related
  genes, including `Abcb7`, `Ireb2`, `Reps1`, and `Tfrc`, did not elicit a
  shared canonical iron-homeostasis mRNA program in juvenile neurons.
- Claim `claim:8eb2170d6611ffb654e2` reports that `Tfrc`/`Hjv` iron-axis
  perturbations produced absent or highly punctate transcriptional responses.
- Claim `claim:a5ac55dc4ddd516d5ad3` reports that Fe-S/ISC and iron-homeostasis
  components, including `Abcb7`, `Isca2`, `Lyrm4`, `Nfs1`, and `Tfrc`, did not
  form a coherent Fe-S or iron-stress module.
- Claim `claim:4f4441a7c77bcae57d1e` reports that represented basal
  ferroptosis/glutathione/oxidative genes, including `Acsl4`, `Gpx4`, and
  `Gstm5`, did not trigger a detectable neuronal ferroptosis, NRF2/glutathione,
  iron-handling, or ISR transcriptional program.
- Claim `claim:9e7a214f550a5b5f7b37` similarly reports no shared basal
  glutathione/GPX4/ferroptosis/NRF-redox module for `Gclc`, `Gclm`, and `Gpx4`.

## Biology used for `Fth1`

`Fth1` encodes the ferritin heavy chain. The H subunit supplies ferroxidase
activity for oxidation of Fe(II) to Fe(III), while L subunits help nucleate and
stabilize the mineral core. Germline loss of mouse H ferritin is early
embryonic lethal, and L ferritin does not replace its function, showing that
loss of H ferritin is a real iron-buffering perturbation rather than a
redundant ferritin-family edit (Ferreira et al. 2000; Li et al. 2015).

The best direct pathway neighbor would be `Ncoa4`, because NCOA4 binds FTH1 and
delivers ferritin to lysosomes for ferritinophagy; Mancias et al. 2015 mapped
the NCOA4-FTH1 interaction and showed it is central for ferritin iron turnover.
`Ncoa4` itself was measured but was not a training perturbation, so I used
`Tfrc`, `Ireb2`, `Hjv`, `Slc22a17`, `Flvcr1`, `Abcb7`, `Nfs1`, `Isca2`,
`Lyrm4`, `Gpx4`, `Acsl4`, `Gclc`, and `Gclm` as imperfect surrounding
perturbations. These cover iron import or signaling, Fe-S dependency,
heme/iron export, and the ferroptosis execution and antioxidant arms. Their
near-silent focal-cell responses are the main within-dataset reason not to
predict a broad `Fth1` program.

`Fth1` is not identical to most of those analogs. Loss of FTH1 iron storage
should tend to increase the labile iron pool, while loss of `Tfrc` decreases
transferrin-mediated import and loss of `Ncoa4` would block ferritin turnover;
`Gpx4` and `Acsl4` alter lipid-peroxide handling rather than ferritin storage.
External work also shows that neuronal ferritin H deficiency can sensitize
neurons to ferroptosis after traumatic brain injury (Rui et al. 2020), a stress
regime absent from this basal P16-to-P37/P44 sparse AAV screen. Therefore I
used those perturbations as boundaries for expected basal RNA breadth, not as
strict phenocopies.

The remaining question is the self-target row. In the training set, singleton
responses were often just the target transcript; `Acsl4`, `Isca2`, and
`Slc22a17` are exactly of that form. `Fth1` is a highly expressed, measured
focal transcript, and a direct CRISPR perturbation could plausibly make `Fth1`
itself cross the BH threshold even if no downstream iron-handling gene does.
That is enough to move my point prediction from 0 to 1, but not enough to
predict a multi-gene program.

## Target-specific prediction

### `Fth1`

Relevant training perturbations and counts:

- `Tfrc`, `n_degs = 0`: iron-entry perturbation; no significant `Fth1`, `Aco1`,
  `Ncoa4`, `Slc11a2`, `Hmox1`, or broad iron-starvation response.
- `Ireb2`, `n_degs = 1`: core IRP regulator; only `Abhd12b` passed FDR, so IRP2
  loss was not a broad iron-regulatory profile.
- `Hjv`, `n_degs = 0`: iron/hepcidin-axis comparator in the corpus and silent
  in the focal endpoint.
- `Abcb7`, `Nfs1`, `Isca2`, `Lyrm4`, `Aco2`, `n_degs = 0, 0, 1, 0, 0`: Fe-S
  or mitochondrial iron-client comparators; the one nonzero count was
  `Isca2` self only.
- `Slc22a17` and `Flvcr1`, `n_degs = 1` and `0`: iron/lipocalin or heme-adjacent
  transport comparators; `Slc22a17` was self only.
- `Gpx4`, `Acsl4`, `Gclc`, `Gclm`, `Gstm5`, `Nfe2l2`, `n_degs = 0, 1, 0, 1, 0,
  0`: ferroptosis, glutathione, and NRF/redox counterexamples; the corpus and
  raw rows both showed no basal neuronal ferroptosis or NRF2 transcriptional
  module.

The internal data support a zero or near-zero downstream DEG burden. External
biology makes `Fth1` a credible iron-storage perturbation, but the appropriate
same-experiment comparators show that iron and ferroptosis biology is buffered
or survivor-conditioned in this basal neuronal nuclear RNA readout. I predict a
singleton dominated by direct loss of the `Fth1` transcript, with no detectable
multi-gene iron-stress program.

Point prediction: `Fth1 -> 1`.

## Limits

- There is no direct `Fth1`, `Ftl1`, `Ftl2`, or `Ncoa4` training perturbation in
  the focal endpoint, so the closest ferritinophagy comparison is extrapolated
  from surrounding import, IRP, Fe-S, heme, GPX4, ACSL4, and glutathione
  perturbations.
- Several external `Fth1` studies use germline or conditional knockout, injury,
  cultured cells, or ferroptosis challenge. Those contexts can reveal iron and
  survival phenotypes that this acute mosaic postnatal neuronal assay could
  miss.
- The single predicted DEG is especially uncertain because self-target RNA
  reduction is not a fixed consequence of CRISPR indels in this snRNA-seq
  design. A nonsignificant `Fth1` self row would make the correct count 0,
  while an unusually strong survivor stress response could make the answer
  larger than 1.
