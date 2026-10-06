# Predicting held-out DEG counts for `151 TH Prkcd Grin2c Glut`

## Question

For each target in `155_Notch3.csv`, I predicted the number of genes that would
pass BH-adjusted Wilcoxon `pvals_adj < 0.05` in the held-out
`151 TH Prkcd Grin2c Glut` profile.  The manifest contains one held-out
perturbation:

```text
Notch3
```

I treated the output as a point prediction of the assay endpoint in the supplied
Perturb-seq experiment, not as a statement about biological essentiality,
editing efficiency, or germline Notch3 phenotypes.

## Sources and computational steps

- Same-experiment focal endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Same-experiment DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested-target manifest:
  `[local file: 155_Notch3.csv]`
- Distributed Agents same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, queried for `Notch3`,
  `Notch1`, `Adam10`, `Psen1`, and `Mib1`.
- External mechanism literature:
  Artavanis-Tsakonas et al. 1999, Science, DOI `10.1126/science.284.5415.770`;
  Joutel et al. 1996, Nature, DOI `10.1038/383707a0`;
  Domenga et al. 2004, Genes & Development, DOI `10.1101/gad.308904`;
  Itoh et al. 2003, Developmental Cell, DOI
  `10.1016/S1534-5807(02)00409-4`;
  Hartmann et al. 2002, Human Molecular Genetics, DOI
  `10.1093/hmg/11.21.2615`;
  De Strooper et al. 1999, Nature, DOI `10.1038/19083`.

I first verified that `Notch3` is absent from the training targets but that the
closest represented Notch nodes are present.  In the 1,674 focal-cell training
perturbations the count distribution is sparse: median `n_degs = 0`,
75th percentile `= 1`, 95th percentile `= 18`, and the mean is 14.05 because a
small number of chromatin, RNA-processing, proteostasis, and trafficking
perturbations have hundreds to thousands of DEGs.

I then compared Notch-proximal training perturbations in the focal parquet slice.
The following focal counts are exact from the supplied training CSV:

| training perturbation | biological relationship to Notch3 | n_degs |
|---|---:|---:|
| `Notch1` | Notch-family receptor paralog | 0 |
| `Notch2` | Notch-family receptor paralog | 0 |
| `Notch4` | Notch-family receptor paralog | 0 |
| `Dll1` | Delta ligand for Notch signaling | 0 |
| `Adam10` | S2 Notch receptor protease | 0 |
| `Psen1` | gamma-secretase catalytic component for NICD release | 0 |
| `Mib1` | E3 ligase needed for Delta ligand endocytosis | 27 |
| `Ctnnb1` | developmental transcriptional pathway counterexample, not a Notch phenocopy | 383 |

For these eight profiles I used the runtime profile comparison on the focal
`group_name == "151 TH Prkcd Grin2c Glut"` rows with `logfoldchanges` as the
signed profile value and `pvals_adj < 0.05` as the significance cutoff.  All
profiles had 17,259 measured features.  `Notch1`, `Notch2`, `Notch4`, `Dll1`,
`Adam10`, and `Psen1` each had zero significant features in this exact cell
group.  `Mib1` had 26 significant up-regulated genes and 1 down-regulated gene;
`Ctnnb1` had 100 up-regulated and 283 down-regulated genes.  Because the zero
profiles have no significant genes, none of them share an FDR-significant
intersection with the `Mib1` or `Ctnnb1` response.

To sanity-check the identity of the one nonzero Notch-adjacent response, I
looked at the lowest-FDR `Mib1` genes in this focal group.  They were a
cholesterol/sterol block:

```text
Insig1, Dhcr24, Fdft1, Ldlr, Msmo1, Hmgcs1, Hmgcr, Cyp51
```

That matches the Distributed Agents corpus Mib1 findings: the recurrent `Mib1` screen
signature is an SREBF2-like sterol/cholesterol-biosynthesis module that is
uncoupled from canonical Dll1-Notch transcription and does not collapse onto
`Dll1`, `Notch1`, `Notch2`, `Notch4`, `Adam10`, or `Psen1`.

Finally, I queried the focal parquet for `Notch3` as a measured transcript
across all 1,674 training perturbations.  `Notch3` had a median log2 fold change
near the assay floor (`-20.20`) and never had `pvals_adj < 0.05`, consistent
with essentially absent expression of this mural-cell receptor in the
NeuN-enriched thalamic glutamatergic cell group.

## Target-specific reasoning

### Notch3

`Notch3` encodes one of four mammalian Notch receptors.  Canonical Notch
activation is a contact-dependent developmental pathway: Delta/Jagged ligand
engagement, ligand endocytosis by `Mib1`, ADAM metalloprotease S2 cleavage, and
presenilin/gamma-secretase S3 cleavage release the Notch intracellular domain,
which enters the nucleus and acts with CSL/RBPJ/MAML cofactors to regulate
HES/HEY-class target transcription (Artavanis-Tsakonas et al. 1999; Itoh et al.
2003; Hartmann et al. 2002; De Strooper et al. 1999).

The prior biology that most distinguishes `Notch3` from `Notch1` and `Notch2`
is not a strong postmitotic-neuron role: `NOTCH3` mutations cause the cerebral
small-vessel disease CADASIL (Joutel et al. 1996), and mouse `Notch3` is
required for arterial vascular-smooth-muscle-cell identity and maturation
(Domenga et al. 2004).  Those mural and vascular contexts are outside the
NeuN-enriched nuclei used here and are largely absent from the focal
`151 TH Prkcd Grin2c Glut` readout.

The most direct within-dataset analogs all supported a zero call:

- `Notch1`, `Notch2`, and `Notch4` are receptor paralogs of `Notch3`; each had
  `n_degs = 0` in the focal training counts.
- `Dll1`, a represented Delta ligand, also had `n_degs = 0`.
- `Adam10`, the represented Notch S2 metalloprotease, had `n_degs = 0`.
- `Psen1`, the represented gamma-secretase catalytic subunit upstream of Notch
  intracellular-domain release, had `n_degs = 0`.
- `Mib1` is the important counterexample because it is a real Notch-ligand E3
  ligase but had `n_degs = 27`.  Its focal significant genes were
  sterol/cholesterol genes (`Insig1`, `Dhcr24`, `Fdft1`, `Ldlr`, `Msmo1`,
  `Hmgcs1`, `Hmgcr`, `Cyp51`), and the Distributed Agents Mib1 findings report the same
  screen-level separation of the `Mib1` sterol module from `Dll1`, Notch
  receptors, `Adam10`, and `Psen1`.  I therefore used `Mib1` as a boundary case,
  not as a receptor phenocopy.
- `Ctnnb1` had `n_degs = 383`, showing that this thalamic glutamatergic assay
  can detect a transcriptionally broad developmental signaling perturbation
  when the target is active.  The lack of response for Notch receptors and
  processing genes is therefore pathway/context-specific rather than a global
  inability of these nuclei to respond.

The Distributed Agents corpus had no direct `Notch3` target card in this release, so
this prediction extrapolates from the represented receptor paralogs and core
Notch processing nodes.  The corpus did, however, contain consistent
same-experiment Notch pathway observations for represented genes: `Notch1`
reports concluded that available `Notch2`, `Notch4`, `Dll1`, `Adam10`, and
`Psen1` perturbations did not form a shared postmitotic neuronal Notch RNA
module; `Adam10` reports likewise found no convergent APP/Notch/synaptic
adhesion RNA module; and `Psen1` reports found no neuronal FDR-supported
downstream transcriptome across recovered neuronal groups.

Given those direct focal zeros, the absent `Notch3` transcript in the measured
focal profiles, and the fact that `Notch3` biology is concentrated in vascular
mural cells rather than in postnatal NeuN+ thalamic glutamatergic neurons, I
predict no genes will pass BH-adjusted FDR 0.05 after sparse `Notch3` loss in
`151 TH Prkcd Grin2c Glut`.

Prediction: `Notch3 -> 0`

## Limits and uncertainties

- `Notch3` itself was held out, so there is no same-target DEG count or held-out
  expression signature to inspect.
- The strongest direct comparators are receptor paralogs and core processing
  nodes, not another `Notch3` paralog with identical vascular specificity.
- The screen reads nuclear RNA 3-4 weeks after sparse AAV-CRISPR perturbation.
  It can miss acute, protein-level, non-cell-autonomous, or ligand-sending versus
  ligand-receiving effects.
- Most HES/HEY effector perturbations, `Rbpj`, `Maml` genes, `Psen2`, `Ncstn`,
  and `Aph1` subunits were not represented in the focal training target table,
  so the canonical Notch cascade is incompletely tiled.
- `Mib1` proves that a Notch-adjacent gene can have a small nonzero neuronal
  RNA phenotype, but both the focal significant genes and the Distributed Agents corpus
  point to sterol homeostasis rather than to a Notch receptor response.
