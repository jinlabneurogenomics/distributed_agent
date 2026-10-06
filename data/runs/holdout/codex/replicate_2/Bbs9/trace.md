# Bbs9 DEG-count forecast

## Declared target and endpoint

- Target: `Bbs9`
- Focal cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`
- Point forecast: `0`

## Evidence used

The outcome-blind Bbs9 biology bundle supports target reach but not a
high-amplitude nuclear RNA expectation in this postnatal thalamic assay.
BBS9 is an integral BBSome subunit for ARL6-regulated ciliary membrane-cargo
sorting, and functional stock is predicted to decline by the P37-P44 harvest
because the P16 edit should stop new BBS9 supply while BBSome subunits exchange
at ciliary assembly sites. The bundle also marks the key uncertainty: direct
postnatal mouse thalamic loss data and a BBS9-specific neuronal half-life are
missing. Exact focal expression is low but detectable: Bbs9 is observed in
7,699 of 23,679 focal non-target nuclei, 32.5%, with mean CP10K 0.281.

The exact training count table for `151 TH Prkcd Grin2c Glut` is strongly
zero-inflated. Among 1,674 training perturbations, 1,205 had `n_degs = 0`,
the median was 0, the 75th percentile was 1, the 90th percentile was 2, and
only 106 targets had at least 10 DEGs.

The BBSome/ciliary training perturbations in the same count table were the
decisive local quantitative reference set:

| target | n_degs |
|---|---:|
| Bbs5 | 0 |
| Cep290 | 0 |
| Cplane1 | 0 |
| Ift43 | 0 |
| Ift81 | 0 |
| Ift88 | 0 |
| Kif3b | 0 |
| Lztfl1 | 0 |
| Rpgrip1l | 0 |
| Ttc21b | 0 |
| Ttc8 | 1 |

Their mean focal count was 0.091 and their median was 0. The full expression
parquet confirmed that each of these eleven contrasts was actually measured
against 17,259 genes in the focal group with 99-328 perturbed nuclei and
23,679 matched controls. Ten had no FDR-significant genes; the closest
subthreshold adjusted p values among the zeros were still well above 0.05
(`Rpgrip1l` 0.184, `Lztfl1` 0.195, `Bbs5` 0.220). `Ttc8` had one significant
gene, its own target transcript, with `pvals_adj = 3.07e-05`; its downstream
program was otherwise flat.

The same-experiment corpus was consistent with the raw measurements rather
than adding independent replication. `Ttc8:F001` reported that acute postnatal
`Ttc8` perturbation was buffered across measured neuronal groups despite a
negative self-transcript; `Cep290:F003` reported that expected ciliary GPCR,
BBSome/IFT, and Hedgehog-effector transcription was absent or nearly absent
after `Cep290` and related ciliary perturbations; and `Bbs5:F003` reported
that represented BBSome/ciliary relatives did not form a shared neuronal DE
program.

## Synthesis

Bbs9 sits in an operative complex that should be affected by coding disruption
over the 21-28 day assay window, so I did not treat it as biologically inert.
The expected effect of losing BBS9, however, is ciliary cargo mislocalization
or altered evoked signaling, and the declared evidence did not establish a
fast resting thalamic nuclear-RNA consequence. The most directly relevant
training perturbations tested other BBSome, IFT, transition-zone, and ciliary
trafficking genes in the same endpoint and were essentially all zero, with the
single `Ttc8` focal DEG explained by target-transcript loss rather than a
downstream module. Bbs9 baseline RNA is present in only about one third of
focal control nuclei, making even the self-transcript an uncertain singleton.

I therefore put Bbs9 at the quiet end of the focal distribution and forecast
no BH-significant measured genes.
