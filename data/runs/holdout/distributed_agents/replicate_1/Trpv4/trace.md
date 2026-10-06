# DEG-count prediction trace

## Question and endpoint

The requested forecast is the held-out `n_degs` for `Trpv4` in `151 TH Prkcd Grin2c Glut` cells: the number of measured transcripts passing Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after acute mosaic CRISPR loss of `Trpv4`, delivered at P16 and assayed by NeuN-enriched whole-brain snRNA-seq at P37-P44.

I treated `n_degs` as an assay-specific response-breadth endpoint rather than as a direct measure of channel importance, editing efficiency, viability, or baseline expression. The held-out target has no own differential-expression rows in either supplied input, so all numerical evidence comes from non-held-out training perturbations in the same assay.

## Sources used

- Declared focal DEG-count table: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet: `training differential-expression dataset`.
- Run-local dataset portrait, task bindings, coverage summary, capability manifest, and measurement registry under `codex_runtime/pipeline/`.
- Same-experiment internal corpus `perturbai-july-260713-sourceguard-1773-v1` for packaged reports and Findings on represented analogs including `Trpv1`, `Trpm3`, `Trpm7`, `Pkd1`, and `Kcnma1`. This corpus is an interpretation layer over the same Perturb-seq experiment, not an independent replicate.
- External literature via PubMed:
  - White et al. 2016, Physiol Rev, DOI `10.1152/physrev.00016.2015`, PMID `27252279`: review of TRPV4 as a calcium-permeable polymodal nonselective cation channel activated by osmotic, mechanical, thermal, acidic, and chemical stimuli.
  - Dunn et al. 2013, PNAS, DOI `10.1073/pnas.1216514110`, PMID `23530219`: TRPV4-mediated calcium entry in astrocytic endfeet couples with IP3 receptors and contributes to neurovascular coupling.
  - Toft-Bertelsen et al. 2018, Channels, DOI `10.1080/19336950.2018.1438009`, PMID `29424275`: TRPV4 as a cell-volume sensor, with astrocytic swelling biology that is not equivalent to a constitutive neuronal nuclear RNA program.
  - Landoure et al. 2009, Nat Genet, DOI `10.1038/ng.512`, PMID `20037586`: human TRPV4 gain-of-function channel alterations can cause peripheral neuropathy, illustrating channel-current disease biology rather than a canonical loss-of-function transcription-factor axis.

## Training-set calibration

I first summarized the supplied `151 TH Prkcd Grin2c Glut` training counts because the task directly asks for the same scalar endpoint:

- 1,674 non-held-out perturbations had focal-cell `n_degs`.
- 1,205/1,674, 72.0%, had `n_degs = 0`.
- 1,481/1,674, 88.5%, had `n_degs <= 1`.
- 1,571/1,674, 93.8%, had `n_degs <= 10`.
- The median was 0, the 75th percentile was 1, the 95th percentile was 18, and the maximum was 2,677.

I then queried the parquet for focal-cell analog perturbations, counting `pvals_adj < 0.05` rows and recording matched recovered nuclei:

| training perturbation | focal `n_degs` | focal matched perturbed nuclei | relevance to `Trpv4` |
| --- | ---: | ---: | --- |
| `Trpv1` | 0 | 187 | closest represented TRPV-family perturbation; stimulus-gated vanilloid/TRP cation channel |
| `Trpa1` | 0 | 191 | thermo/nociceptor TRP channel comparator |
| `Trpm3` | 0 | 154 | TRP cation channel with sensory/heat biology |
| `Trpm7` | 0 | 81 | broadly important TRP channel-kinase but no focal corrected response |
| `Pkd1` | 0 | 136 | ciliary mechanosensory/polycystin Ca2+ signaling comparator |
| `Tmem63b` | 1 | 150 | mechanically activated/osmosensitive cation-channel family; focal hit was only its own transcript |
| `Tmem63c` | 0 | 243 | mechanically activated/osmosensitive cation-channel family |
| `Itpr1` | 0 | 203 | intracellular Ca2+-release channel downstream of Gq/IP3 signals |
| `Ryr2` | 0 | 100 | intracellular Ca2+-release channel |
| `Ryr3` | 0 | 151 | intracellular Ca2+-release channel |
| `Kcnma1` | 1 | 183 | Ca2+-activated BK channel; focal hit was only its own transcript |
| `Kcnma1` | 0 non-self | 183 | same row interpreted without counting the self-transcript |
| `Cacna1g` | 12 | 264 | thalamus-relevant T-type Ca2+ channel positive counterexample |

For every zero-count analog above, the top focal rows were subthreshold; for example, in `151 TH Prkcd Grin2c Glut`, the smallest adjusted p-values were 1.0 for `Trpv1`, 1.0 for `Trpa1`, 0.146 for `Trpm3`, 1.0 for `Trpm7`, and 1.0 for `Pkd1`. The two apparent singletons among mechanosensitive/Ca2+-dependent comparators were self-transcript rows (`Tmem63b`, FDR `4.16e-17`; `Kcnma1`, FDR `0.0139`), not multi-gene downstream programs.

The corpus reports were concordant with the count table. `Trpv1`, `Trpm3`, and `Trpm7` were nearly flat in this basal postnatal neuronal assay and did not form a shared TRP-channel or Ca2+-signaling transcriptomic state; `Pkd1` was flat across recovered neuronal classes despite strong ciliary and calcium-channel priors; `Kcnma1` loss was interpreted as a likely electrophysiological perturbation with no broad baseline snRNA signature. These same-experiment reports helped interpret the numerical zeroes, but the CSV/parquet rows were the direct source for the exact focal counts.

The main positive counterexample is `Cacna1g`: it is a thalamic voltage-gated Ca2+ channel, and its loss produced 12 focal DEGs including up-regulated `Ptprn` and down-regulated `Stmn4`, `Cpne7`, `Ly6e`, and `Zdhhc22`. That means this cell group and the DEG-count pipeline can detect a channel-loss state when it creates a stable focal RNA program. However, the magnitude was still low and the mechanism is more specific to the focal thalamic neurons than `Trpv4`, whose best-established CNS signaling is astrocytic endfoot calcium entry and mechanosensation/osmosensation.

## Target-specific prediction

### Trpv4

`Trpv4` encodes a calcium-permeable nonselective cation channel. External TRPV4 literature supports a role as a polymodal channel activated by osmotic, mechanical, thermal, and chemical cues, with CNS functions reported in astrocytic endfeet and neurovascular coupling rather than a canonical cell-autonomous transcriptional regulator in thalamic glutamatergic neurons.

The intervention in this assay is sparse P16 CRISPR loss of function in recovered NeuN-positive nuclei. The direct molecular consequence of a functional `Trpv4` knockout would be reduced TRPV4 channel conductance. That could propagate to calcium influx after swelling or mechanical/chemical stimulation, and in astrocytes could propagate through IP3 receptor-mediated endfoot calcium events to vascular coupling. The requested measurement occurs in resident `151 TH Prkcd Grin2c Glut` neuronal nuclei at a basal harvest point, after glial and vascular cells have been mostly removed. Therefore the expected channel, astrocytic swelling, or neurovascular phenotypes are displaced from the measured endpoint by cell lineage and modality.

The most relevant within-dataset analogs argue that a broad focal DE response is unlikely:

- `Trpv1`, `Trpa1`, `Trpm3`, and `Trpm7` are represented TRP-channel perturbations. All had `n_degs = 0` in `151 TH Prkcd Grin2c Glut`; their same-experiment reports further showed no shared basal TRP/Ca2+ transcriptional module.
- `Pkd1`, another mechanosensory/ciliary Ca2+-linked membrane protein with non-neuronal and epithelial biology, had `n_degs = 0` in the focal group and no robust neuronal transcriptomic response in the corpus report.
- `Tmem63b` and `Tmem63c`, mechanosensitive/osmosensitive cation-channel family members, produced 1 and 0 focal DEGs respectively; the single `Tmem63b` count was the `Tmem63b` self-transcript, not a downstream state.
- `Itpr1`, `Ryr2`, and `Ryr3` showed that perturbing intracellular Ca2+-release channels did not by itself create a stable focal DE program.
- `Kcnma1` was a useful electrophysiological counterexample: it can be an important neuronal channel, and its self-transcript was significantly reduced in the focal group, but it still had no focal downstream hits.
- `Cacna1g` prevents an overstrong "channels are always zero" rule because it had 12 focal DEGs. I did not transfer that count upward to `Trpv4`: `Cacna1g` is a thalamus-relevant voltage-gated channel with a direct firing-mode role, whereas TRPV4 is stimulus gated and has much stronger astrocyte, endothelial, peripheral sensory, and mechanical/osmotic priors than a basal thalamic glutamatergic cell-autonomous RNA prior.

I therefore predict no measured gene will pass FDR 0.05 after held-out `Trpv4` loss in `151 TH Prkcd Grin2c Glut`.

**Prediction: `Trpv4`, `predicted_n_degs = 0`.**

## Limits and uncertainty

This is an extrapolation because `Trpv4` itself was deliberately absent from the training parquet and the training DEG-count CSV. The represented TRP set did not include every TRPV paralog, so `Trpv1` is an imperfect family analog rather than an obligate-complex partner. None of the analogs directly tests TRPV4's tetrameric pore. The assay did not measure TRPV4 protein, channel current, osmotic or mechanical stimulation, neurovascular coupling, peripheral ganglia, astrocytes, endothelia, or vascular smooth muscle. A stronger, denser, evoked, or non-neuronal perturbation could expose TRPV4 biology that a basal NeuN-positive thalamic snRNA endpoint misses. Within the stated endpoint, the same-assay analogs make a zero-count outcome more likely than a low nonzero singleton or a Cacna1g-like dozen-gene response.
