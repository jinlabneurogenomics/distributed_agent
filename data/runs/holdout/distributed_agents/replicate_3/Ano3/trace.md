# Trace for held-out `Ano3`

## Question and endpoint

The requested held-out target is `Ano3`. I interpreted the task as a point prediction for the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` after acute sparse AAV-CRISPR loss of `Ano3`. The benchmark count includes the perturbed gene's own RNA if that transcript is FDR-significant; therefore a channel perturbation with no downstream response could still have `n_degs = 1` if only its own transcript is depleted detectably.

`151 TH Prkcd Grin2c Glut` was treated as an Allen thalamic glutamatergic class; `TH` was not read as tyrosine hydroxylase. `Ano3` was absent from both supplied training tables as expected.

## Sources used

- Held-out manifest: `011_Ano3.csv`, containing one target, `Ano3`.
- Training endpoint: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, 1,674 non-held-out targets.
- Training DE parquet: `training_de_all_cell_groups.parquet`, queried for the focal-cell signatures of ion-channel, chloride-transporter, calcium-homeostasis, and GABA_A counterexample perturbations.
- Internal same-experiment corpus: Distributed Agents `perturbai-july-260713-sourceguard-1773-v1`.
  - There was no `Ano3` card in the corpus.
  - I used KNa/KCa, CaV, Kv, and GABA_A claims from the corpus to avoid treating superficial channel-family membership as if it were a mechanistic expression match.
- Run-local profile comparison: I compared signed 151-class log-fold-change profiles for `Kcnt1`, `Kcnt2`, `Kcnma1`, `Kcnn2`, `Kcnn3`, `Kcnh1`, `Kcnh5`, `Cacna1g`, `Gabrb2`, `Slc12a2`, `Clcn3`, and `Clcn4`.
- External mechanism:
  - Charlesworth et al. 2012, PMID 23200863, DOI 10.1016/j.ajhg.2012.10.024: missense mutations in `ANO3` cause autosomal dominant craniocervical dystonia.
  - Huang et al. 2013, PMID 23872594, DOI 10.1038/nn.3468: TMEM16C/ANO3 facilitates Na+-activated K+ currents in rat sensory neurons and regulates pain processing, tying ANO3 biology to Slack/KNa channels.
  - Ousingsawat et al. 2025, PMID 39773217, DOI 10.1186/s12916-024-03839-5: ANO3 dystonia variants attenuate ORAI1-dependent Ca2+ influx, reinforcing that pathogenic ANO3 effects are channel/Ca2+-signaling physiology rather than an obvious transcription-factor-like module.

## Dataset calibration

The focal training endpoint is strongly zero-inflated:

- 1,674 training targets total.
- 1,205 have `n_degs = 0`.
- Median `n_degs = 0`; 75th percentile `n_degs = 1`.
- The mean is 14.1 but the maximum is 2,677, so the average is dominated by a small high-DEG tail of essential RNA-processing, proteostasis, and transcriptional regulators.

I first looked for direct anoctamin paralogs among training perturbations and found none: no `Ano1`, `Ano2`, `Ano4`, `Ano5`, `Ano6`, `Ano7`, `Ano8`, `Ano9`, or `Ano10` target was in the focal training count file. The prediction therefore has to be transferred from physiological analogs rather than from a close paralog.

For candidate analogs I then pulled exact 151-class parquet rows and counted FDR-significant genes, cross-checking against the count CSV:

| training target | focal `n_degs` | focal expression evidence | interpretation for `Ano3` |
|---|---:|---|---|
| `Kcnt1` | 0 | All 17,259 measured 151-class genes had `pvals_adj = 1.0` or non-significant values for this target. | Best available Slack/KNa pore analog; external ANO3/TMEM16C work connects ANO3 to Na+-activated K+ currents. |
| `Kcnt2` | 0 | All focal genes non-significant; the internal corpus reports `Kcnt1`/`Kcnt2` as a joint KNa transcriptomic null rather than a shared module. | Closest KNa paralog/counterpart to `Kcnt1`; supports the KNa-current neighborhood being buffered at the nuclear RNA level. |
| `Kcnma1` | 1 | The only focal hit was the target transcript itself, `Kcnma1` q = 0.014; the next genes were non-significant, q = 0.58 and q = 1. | Ca2+-activated K+ pore; a broader Ca-sensitive channel analog whose perturbation does not create a downstream 151 program. |
| `Kcnn2` | 0 | Minimum focal q = 0.708. | SK-family Ca2+-activated K+ channel, flat in the focal class. |
| `Kcnn3` | 0 | Minimum focal q = 0.409; `Kcnn3` self row q = 0.409. | SK-family Ca2+-activated K+ channel, flat in the focal class. |
| `Clcn3` | 0 | Minimum focal q = 0.620. | Intracellular chloride channel/transporter counterpoint; no chloride-homeostasis response. |
| `Clcn4` | 1 | The only focal hit was `Clcn4` itself, q = 6.7e-11; the next genes had q = 1. | Shows detectable self-depletion need not imply downstream chloride-state rewiring. |
| `Slc12a2` | 0 | All focal rows non-significant. | NKCC1 chloride importer; Distributed Agents GABA_A/chloride claims identify it as flat while GABA_A subunit hits can be detected. |
| `Gabrb2` | 4 | Significant genes were `Gabrb2`, `Nr4a1`, `Vgf`, and `Nalf1`. | Positive counterexample: loss of one inhibitory receptor subunit can trigger a small activity-associated 151 response. This looks like GABA_A disinhibition, not like a generic chloride-channel or Ano3 state. |
| `Cacna1g` | 12 | Significant genes included `Ptprn`, `Cacna1g`, `Stmn4`, `Cpne7`, `Ly6e`, `Zdhhc22`, `Jun`, `Iyd`, `Lrrc7`, `Serpine2`, `Notum`, and `Irag1`. | Positive counterexample: a thalamic CaV3.1 perturbation is visible in this same cell class, but Distributed Agents marks it as a selective T-type response not shared by `Cacna1a`, `Cacna1d`, `Cacna1e`, `Cacna2d1`, `Cacna2d2`, `Cacnb2`, or `Cacnb4`. |
| `Atp2b1` | 22 | Induced activity/Ca2+-linked genes such as `Fos`, `Vgf`, and `Nr4a1`. | PMCA calcium extrusion can cross the transcriptional threshold, but this is broader Ca2+ handling than an ANO3/Slick-Slack-type perturbation. |
| `Atp2a2` | 187 | Strong ER-stress/ISR genes such as `Ddit3`, `Chac1`, `Xbp1`, and `Hspa5`. | Strong calcium-homeostasis counterexample; rejected as an analog because SERCA2 loss perturbs ER Ca2+ load and proteostasis rather than local plasma-membrane conductance. |

The profile comparison of the channel cohort was useful mostly as a boundary check. `Kcnt1`, `Kcnt2`, `Kcnn2`, and `Kcnn3` each had zero significant focal features, `Kcnma1` had one negative significant feature, and there were no FDR-significant positive or negative feature intersections between those flat KNa/KCa nodes and the `Gabrb2` or `Cacna1g` positive counterexamples. Thus the few detectable activity or CaV signatures in this cell class were not shared by the closest ANO3-adjacent channel perturbations.

I also checked `Ano3` as a measured gene in the focal signatures. It is present in the 151-class feature universe, but across all 1,674 training perturbations its adjusted p-value was almost always 1.0; only `Psmb4` induced it at q = 0.029. That says `Ano3` RNA can be detected under a large proteasome-stress signature, but it does not show a recurrent 151 thalamic state that would favor a positive Ano3 count.

## Target-specific prediction

### `Ano3`: predicted `n_degs = 0`

External evidence makes `Ano3` a neuronal ion-channel/excitability gene: dominant ANO3 missense variants cause dystonia, and TMEM16C/ANO3 can facilitate Slack/KNa currents. The best available within-dataset analogs for that biology are therefore `Kcnt1` and `Kcnt2`, followed by calcium-activated K+ channel genes (`Kcnma1`, `Kcnn2`, `Kcnn3`) and chloride-homeostasis comparators (`Clcn3`, `Clcn4`, `Slc12a2`).

Those analogs point to a zero or self-only class:

- `Kcnt1` and `Kcnt2` were exact focal nulls.
- `Kcnn2`, `Kcnn3`, `Kcnh1`, `Kcnh5`, `Clcn3`, and `Slc12a2` were also exact focal nulls.
- `Kcnma1` and `Clcn4` each had one DEG, but that DEG was the self transcript, with no downstream program.
- The internal corpus independently summarizes represented KNa/KCa genes as flat or isolated rather than a recurrent channel-loss transcriptional module, and represented chloride/GABA_A perturbations as subunit-specific rather than a generic chloride-flux response.

The positive channel counterexamples do not transfer well to `Ano3`. `Cacna1g` gives a 12-gene CaV3.1 thalamic signature, and `Gabrb2` gives a 4-gene GABA_A disinhibition/activity signature, but both are receptor/channel-subtype-specific programs in the Distributed Agents corpus and in the raw 151 table. They show that the assay can see an activity-linked channel response in this class; they do not argue that every conductance perturbation becomes visible.

The remaining choice was 0 versus a self-transcript-only 1. I chose 0. `Ano3` is measurable but not a prominent recurrent DE feature in this focal class, direct anoctamin paralogs were missing, the most mechanistically relevant KNa genes were complete nulls rather than self-only hits, and a sparse postnatal mosaic LoF of a TMEM16C/ANO3 conductance modulator is more likely to be electrophysiologically buffered than to induce a stable single-nucleus RNA program 3-4 weeks later.

## Limits and extrapolation

- The decisive weakness is the lack of a measured `Ano3` signature or any measured `Ano` paralog signature in this holdout split; the prediction is a transfer from Slack/KNa, KCa, chloride, CaV, and GABA_A comparators.
- The screen measures basal nuclear RNA in recovered neurons. It does not measure Slack currents, Cl- conductance, lipid scrambling, ORAI1 Ca2+ influx, firing-pattern adaptation, dystonia-relevant basal-ganglia physiology, or pain sensory-neuron phenotypes.
- The focal class is thalamic glutamatergic, not necessarily the main cell type in which ANO3 dystonia or nociception mechanisms manifest.
- A zero prediction does not mean ANO3 is biologically inert, unedited, or unexpressed; it means I expect no measured gene, including `Ano3` itself, to cross BH FDR 0.05 in this particular 151-class endpoint.
