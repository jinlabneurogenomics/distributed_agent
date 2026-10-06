# DEG-count prediction trace

## Question and endpoint

The task asks for a point prediction of `n_degs` for each held-out perturbation in
`151 TH Prkcd Grin2c Glut` cells. I treated the endpoint as the exact training
CSV definition: the number of measured transcripts with Wilcoxon
Benjamini-Hochberg adjusted `pvals_adj < 0.05` for the perturbed target in this
cell group. The held-out target in this shard is:

| target_name |
|---|
| Fzd3 |

The requested `Fzd3` perturbation was absent from both the all-cell differential
expression parquet and the focal-cell training DEG-count CSV, so the endpoint is
not directly observed. It is predicted from non-held-out Perturb-seq
perturbations plus biological knowledge of Frizzled-3.

## Sources used

- Direct endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Direct differential-expression table:
  `training differential-expression dataset`.
- Run-local bindings, coverage, capabilities, and measurement registry under
  `codex_runtime/pipeline/`.
- Same-experiment interpretation corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, specifically the Fzd9,
  Celsr2, Ctnnb1, and Tcf7l2 reports and Findings used as curated summaries of
  the same Perturb-seq experiment, not as independent replication.
- External mechanism literature retrieved through PubMed:
  Wang et al. 2002, DOI 10.1523/JNEUROSCI.22-19-08563.2002, PMID 12351730;
  Tissir et al. 2005, DOI 10.1038/nn1428, PMID 15778712;
  Hua et al. 2014, DOI 10.1073/pnas.1406399111, PMID 24799694;
  Qu et al. 2014, DOI 10.1073/pnas.1402105111, PMID 25002511;
  Feng et al. 2016, DOI 10.1093/cercor/bhw132, PMID 27170656.

## Computational calibration

The endpoint is directly represented by the training count CSV. I loaded that
file and counted 1,674 training targets. The distribution in `151 TH Prkcd
Grin2c Glut` is sparse and heavy-tailed:

| statistic | n_degs |
|---|---:|
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2677 |
| nonzero targets | 469 / 1674 |

I then used a filtered Parquet query for the focal cell group and Wnt/Fzd/PCP
relatives to verify the counts, cell recovery, and score-vector behavior around
`Fzd3` analogs. The focal query selected rows with
`group_name == "151 TH Prkcd Grin2c Glut"` and `gene_target` in represented
Frizzled receptors, Wnt co-receptors, beta-catenin/TCF components, and PCP/Ror
relatives.

Relevant observed training perturbations were:

| training perturbation | n_pert_matched in 151 | n_degs at FDR 0.05 | relevance to Fzd3 |
|---|---:|---:|---|
| Fzd2 | 281 | 0 | assayed Frizzled receptor |
| Fzd4 | 188 | 0 | assayed Frizzled receptor |
| Fzd6 | 189 | 0 | assayed Frizzled receptor; closest represented core PCP receptor family member |
| Fzd9 | 242 | 0 | assayed Frizzled receptor with Wnt5a/spine biology |
| Celsr2 | 231 | 1 | partial forebrain-wiring/PCP analog; its sole 151 hit was self-target `Celsr2` |
| Prickle1 | 249 | 0 | represented PCP component |
| Ror1 | 167 | 0 | noncanonical Wnt receptor-relative comparator |
| Ror2 | 254 | 0 | noncanonical Wnt receptor-relative comparator |
| Ryk | 129 | 0 | Wnt receptor-relative comparator |
| Lrp5 | 230 | 0 | canonical Wnt co-receptor, nonconvergent in 151 |
| Lrp6 | 120 | 4 | weak canonical co-receptor response |
| Gsk3b | 108 | 6 | small intracellular Wnt-pathway response with opposite expected sign from Ctnnb1 loss |
| Tcf7l2 | 111 | 106 | downstream thalamic Wnt/TCF transcription factor; counterexample |
| Ctnnb1 | 171 | 383 | beta-catenin effector; strong downstream thalamic state, but not phenocopied by single Frizzled loss |

The zero Frizzled counts were not explained by unusually poor focal-cell
recovery: the represented `Fzd2`, `Fzd4`, `Fzd6`, and `Fzd9` perturbations had
188 to 281 matched perturbed nuclei, exceeding the matched counts for `Ctnnb1`
and `Tcf7l2`. Their leading nominal genes were weak and nonsignificant after
multiple testing; for example, the best `Fzd6` adjusted p-value was 0.875 and
the best `Fzd9` adjusted p-value was 0.357 in the 151 slice.

As a falsification step for the tempting Ctnnb1/Tcf7l2 transfer, I compared
score vectors for Wnt relatives against the strong `Ctnnb1` and `Tcf7l2`
signatures in the same Parquet slice. `Fzd2`, `Fzd4`, `Fzd6`, and `Fzd9` had
Spearman correlations from -0.028 to 0.033 against those two signatures across
17,259 shared measured genes. Over the 383 `Ctnnb1` FDR genes and the 106
`Tcf7l2` FDR genes, the Frizzled perturbations again had no FDR-supported
change; the smallest adjusted p-value in each Frizzled comparison was 1.0. In
contrast, `Lrp6`, `Tcf7l2`, and `Ctnnb1` showed detectable but branch-specific
coupling. This supports the same-experiment corpus interpretation that the
acute 151 Wnt response is strongest at beta-catenin/TCF nodes and is not
propagated equivalently from single represented Frizzled receptors.

## Target-specific reasoning

### Fzd3

`Fzd3` encodes Frizzled-3, a Wnt receptor with an established requirement in
forebrain axon tract development. Germline `Fzd3` deletion eliminates or
severely disrupts the thalamocortical, corticothalamic, nigrostriatal, anterior
commissure, corpus callosum, and related embryonic CNS tracts in mice
(Wang et al. 2002, PMID 12351730; Wang et al. 2006 was background only, not
needed for the count). `Celsr3` mutant mice show related forebrain wiring
defects (Tissir et al. 2005, PMID 15778712), and conditional experiments place
`Fzd3` and `Celsr2/3` in a Vangl-independent axon-guidance pathway that is
especially important in ventral telencephalic and Isl1-positive guidepost
territories, not simply as an autonomous thalamic terminal-state regulator
(Hua et al. 2014, PMID 24799694; Qu et al. 2014, PMID 25002511;
Feng et al. 2016, PMID 27170656).

That causal chain weakens direct transfer to this endpoint:

`embryonic Fzd3/Celsr2/3 perturbation -> guidepost/axon navigation failure ->
misrouted long-range tracts and secondary embryonic anatomy -> organismal tract
phenotype`

The requested experiment instead is:

`P16 sparse AAV CRISPR in already postmitotic NeuN+ neurons -> partial acute
cell-autonomous Fzd3 loss -> 3-4 week survivor-conditioned nuclear RNA readout
in 151 thalamic glutamatergic neurons`

The strongest Fzd3 biology is therefore at the embryonic axon-guidance and
guidepost stages of the chain. It is real biology, but much of it is upstream
of, non-cell-autonomous to, or earlier than the measured 151 endpoint. I
therefore treated it as a reason not to call Fzd3 biologically inert, but not
as evidence for a broad postnatal thalamic DEG count.

The most assay-proximal evidence comes from the training perturbations:

- Four represented Frizzled receptors, `Fzd2`, `Fzd4`, `Fzd6`, and `Fzd9`, each
  had `n_degs = 0` in 151 despite adequate recovered-cell counts.
- The same-experiment Fzd9 report explicitly found Fzd9 to be a screen-wide
  postmitotic neuronal transcriptional null and noted that it failed to induce
  a canonical 151 Wnt program even though `Ctnnb1`, `Tcf7l2`, `Gsk3b`, and
  `Lrp6` were detectable in that same class.
- `Celsr2`, the represented CELSR relative of the Fzd3-Celsr2/3 wiring module,
  was essentially flat in 151 with one FDR call, the self transcript, and the
  Celsr2 report found no robust downstream Celsr/Fzd/Vangl/Dvl/Prickle PCP
  feedback in juvenile neurons.
- `Prickle1`, `Ror1`, `Ror2`, `Ryk`, `Lrp5`, `Lgr4`, and `Gpc6` were also zero
  or essentially zero in 151.

The counterexamples are `Ctnnb1` and `Tcf7l2`, with 383 and 106 151 DEGs,
respectively. I did not transfer those counts to Fzd3 because beta-catenin and
TCF7L2 are intracellular transcriptional effectors or effectors plus adhesion
scaffold, not individual Frizzled receptors. The Parquet score-vector checks
showed that represented Frizzled perturbations did not move the Ctnnb1/Tcf7l2
FDR genes coherently, and the internal Ctnnb1 report reached the same
branch-specific conclusion: single Frizzled perturbations were not
interchangeable with beta-catenin/TCF loss in this P16 thalamic assay.

I therefore predict no FDR 0.05 genes for held-out `Fzd3` in `151 TH Prkcd
Grin2c Glut`.

## Limits

The prediction is a direct extrapolation because Fzd3 itself was held out and
`Celsr3`, the closest wiring partner, was not represented as a training
perturbation. Frizzled receptors are ligand- and context-specific, so the nulls
for `Fzd2/Fzd4/Fzd6/Fzd9` are not proof that `Fzd3` must be null. Conversely,
the strong Ctnnb1/Tcf7l2 signatures prove that the 151 assay can detect Wnt/TCF
transcriptional biology, but they do not show that upstream single-receptor
loss has the same direction, timing, or limiting function. The count endpoint is
also sensitive to power and survivor-conditioned sampling; a predicted zero
means no genes are expected to pass this exact FDR threshold, not that Fzd3 has
no postnatal neuronal function.
