# Cask n_degs forecast

## Target and endpoint

- Target: `Cask`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in the matched `151 TH Prkcd Grin2c Glut` contrast.

The target was held out from the declared training count table:
`[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
has 1,674 rows and no `Cask` row. I used the corresponding training
Parquet only for non-Cask perturbations.

## Biology of the held-out perturbation

The declared Cask biology bundle
`[local file: Cask.json]`
shows real target reach in the exact focal class: Cask is detected in
14,967 / 23,679 non-target `151 TH Prkcd Grin2c Glut` nuclei
(`63.2079%`; mean raw UMI `1.1611`, mean CP10K `0.7225`).

The same bundle adjudicates CASK functional stock as
`likely_substantially_depleted` by the P37-P44 harvest after a P16 edit. The
stock call is based on CASK being a renewable multidomain synaptic scaffold,
a measured 6.35-day CASK half-life in primary neurons, in vivo mouse-brain
turnover, and direct Cre-linked protein clearance in mouse neural culture.
Those facts make target engagement biologically plausible by 21-28 days, but
CASK loss is expected to perturb synaptic scaffold complexes rather than a
primary transcriptional regulator.

## Training-count scale

The observed training distribution for this cell class is sparse:

- `n = 1674` training perturbations
- 1,205 have `n_degs = 0`
- median `n_degs = 0`
- 90th percentile `n_degs = 2`
- 95th percentile `n_degs = 18`
- only 43 / 1,674 have `n_degs >= 100`

So the prior local scale is near zero, and a large forecast needs evidence
that Cask should fall into the rare transcriptionally broad tail.

## Cask analogs in the training table

I nominated training-available Cask analogs from the offline curated annotation
and selected-corpus substrate into `workbench/cask_analog_nominations.jsonl`;
this was used only as typed retrieval evidence. The most Cask-proximal
training genes were nearly all null or singleton responses in the declared
count table:

| relation to Cask | training target | n_degs |
|---|---:|---:|
| CORUM same-complex | Nrxn1 | 1 |
| CORUM same-complex | Grin2b | 2 |
| CORUM same-complex | Htr2c | 0 |
| STRING/direct or neurexin paralog context | Nrxn2 | 0 |
| STRING/direct or neurexin paralog context | Nrxn3 | 0 |
| direct interactor | Caskin1 | 1 |
| direct interactor | Tbr1 | 0 |
| PSD/neurexin module | Dlg4 | 1 |
| PSD/neurexin module | Nlgn3 | 1 |
| PSD/neurexin module | Shank3 | 2 |
| NMDA-receptor obligatory subunit | Grin1 | 89 |

The exact Parquet rows showed that the one-DEG entries were largely just
successful self-transcript hits, not downstream response programs:

- `Dlg4`, `Nlgn3`, `Nrxn1`, `Caskin1`, `Stxbp1`, `Syn1`, `Cpe`, `Cplx1`,
  `Grin2a`, and `Grm1` had only their own perturbed transcript significant.
- `Grin2b` had its own transcript plus one downstream gene, `Pianp`.
- `Shank3` had its own transcript plus one downstream gene, `Uba5`.
- `Atp2b1` was broader at 22 DEGs but came from a more generic calcium/PDZ
  branch rather than the Cask-containing MAGUK/neurexin complex itself.

Thus the analogs most specific to Cask point to a count of 0-2, with a single
self-transcript hit being the modal nonzero outcome.

## Matched-profile check

I symmetrically compared 28 typed Cask analogs in the declared Parquet for
`151 TH Prkcd Grin2c Glut` and projected them into
`workbench/cask_synaptic_profile_compare.json` plus
`workbench/cask_synaptic_profile_cohort.json`.

Among these 28 profiles:

- 14 had no FDR-significant genes.
- 12 had 1-9 significant genes.
- 1 had 10-49 significant genes.
- 1 had at least 50 significant genes.

Across the 378 analog-pairs, significant positive-program and
negative-program overlap both had median coefficient 0. The cohort shared a
broad negative tail, but not a recurrent FDR-supported thalamic program. That
made the singleton exact-complex observations more relevant for Cask than the
rare broader responses such as `Grin1` or `Atp2b1`.

## Point estimate

CASK is expressed and likely depleted by the harvest, so I did not treat the
perturbation as an inoperative null. But Cask is a postmitotic synaptic
scaffold; the observed Cask-complex, neurexin, PSD, and presynaptic-scaffold
perturbations in this exact class were mostly either 0 or a self-transcript-only
1. I therefore expect little or no downstream thalamic DEG program and predict
a single significant measured gene, most plausibly the target transcript
itself.

`predicted_n_degs = 1`
