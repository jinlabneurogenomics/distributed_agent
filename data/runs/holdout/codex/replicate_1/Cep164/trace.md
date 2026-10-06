# Cep164 DEG-count forecast

## Requested endpoint

Target: `Cep164` in `151 TH Prkcd Grin2c Glut`.

Endpoint predicted here: the number of measured genes in this focal class with
Wilcoxon `pvals_adj < 0.05` after `Cep164` perturbation.

## Target biology and reach

The declared biology bundle places CEP164 at the distal appendage of the docked
basal body, where it supports an installed ciliary base and recruitment or
stabilization of IFT machinery. The P16 edit does not remove already-installed
distal-appendage/ciliary material immediately. The closest timed evidence in
postmitotic mouse neural tissue is photoreceptor Cep164 deletion: the cilium
initially persists, IFT support erodes over days, and the photoreceptor
outer-segment compartment deteriorates within roughly two to four weeks. That
supports substantial functional loss by the P37-P44 harvest, but it is only a
partial context match because photoreceptors have unusually high ciliary cargo
turnover compared with thalamic primary cilia.

The exact focal expression measurement also argues against a completely absent
target: `Cep164` was detected in 12,103 of 23,679 non-target `151 TH Prkcd
Grin2c Glut` nuclei, with 51.11% expressing, mean log1p CP10K 0.326, mean CP10K
0.487, and pseudobulk 48.5 CPM. I treated that as moderate dilution rather than
complete inaccessibility: a real cell-autonomous ciliary defect is plausible in
successfully edited target-positive cells, but only about half of the recovered
non-target nuclei had detectable transcript before allowing for sparse AAV
editing and survivor-conditioned sampling.

## Training measurements used

The declared count table for `151 TH Prkcd Grin2c Glut` has 1,674 training
perturbations. Its distribution is zero-inflated: 1,205 targets have `n_degs=0`,
the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the
right tail is driven by non-ciliary RNA-processing, proteostasis, and generic
homeostatic perturbations.

I used the ciliary, ciliopathy, and Hedgehog-adjacent perturbations represented
in the training table as the direct quantitative scale reference for `Cep164`.
Their `151 TH Prkcd Grin2c Glut` counts at the requested `pvals_adj < 0.05`
threshold were:

| target | n_degs |
| --- | ---: |
| Adcy3 | 0 |
| Alms1 | 0 |
| Arl3 | 1 |
| B9d1 | 0 |
| Bbs5 | 0 |
| Cep120 | 0 |
| Cep290 | 0 |
| Cplane1 | 0 |
| Cspp1 | 0 |
| Dync2h1 | 0 |
| Dync2i1 | 0 |
| Ift43 | 0 |
| Ift81 | 0 |
| Ift88 | 0 |
| Iqcb1 | 0 |
| Kif3b | 0 |
| Lztfl1 | 0 |
| Rpgr | 0 |
| Rpgrip1l | 0 |
| Smo | 0 |
| Ttc21b | 0 |
| Ttc8 | 1 |

The raw Parquet check in the focal class confirmed that each of these 22
perturbations had 17,259 measured rows. Only two rows among the whole comparator
set passed `pvals_adj < 0.05`: `Arl3` after `Arl3` perturbation
(`logfoldchanges=-0.418`, `q=0.0184`) and `Ttc8` after `Ttc8` perturbation
(`logfoldchanges=-0.663`, `q=3.07e-05`). Thus this ciliary scale is not hiding a
multi-gene downstream program in the same thalamic class; even its two positive
counts were self-transcript events.

The same-experiment corpus points the same way. Its ciliary Claim
`claim:78305cab7c1c7b98458d` states that acute perturbation of represented
ciliary trafficking and ciliary signaling genes in postnatal NeuN+ neurons is
largely buffered at the basal nuclear-RNA level and does not produce a coherent
shared ciliary transcriptional module. Target-centered Findings gave the
material examples behind that claim: `Adcy3:F003` reported that `Bbs5`, `Ttc8`,
`Ift88`, `Cep290`, and `Rpgrip1l` were essentially flat alongside `Adcy3`;
`Cep290:F003` found absent ciliary-GPCR, BBSome/IFT, and Hedgehog effector
transcription after `Cep290`; and `Dync2h1:F003` found no broad ciliary or
Hedgehog response among dynein-2, IFT, and Hedgehog comparators. Those corpus
records are the same experiment, not independent validation, and their caveat is
important: the screen measured basal survivor nuclear RNA, not cilium morphology,
ciliary protein localization, cAMP, or evoked Hedgehog/Gli signaling.

## Synthesis

`Cep164` has stronger short-window realization evidence than many ciliary genes
because post-ciliogenesis mouse photoreceptors lose CEP164-supported IFT on a
3-4 week timescale, and exact `151`-class expression is not negligible. Those
facts move the forecast above an unexpressed or unreached target.

The quantitative training surface moves it back to the floor. Every measured
IFT, dynein-2, BBSome, transition-zone, and ciliary-signaling comparator with a
`151` training count was zero except two self-transcript rows. Direct loss of
`Ift88`, `Ift43`, `Ift81`, `Dync2h1`, `Dync2i1`, `Kif3b`, `Cep290`, `Rpgrip1l`,
`Ttc21b`, `Bbs5`, `B9d1`, and `Adcy3` did not create any non-self BH-significant
gene in this focal class. Given the installed-stock lag for CEP164, lower
turnover of ordinary thalamic primary cilia than photoreceptor connecting cilia,
approximately half-cell expression reach, and the general ciliary-buffered
nuclear RNA surface, the modal focal-class count is no BH-significant measured
gene.

Predicted `n_degs`: 0.
