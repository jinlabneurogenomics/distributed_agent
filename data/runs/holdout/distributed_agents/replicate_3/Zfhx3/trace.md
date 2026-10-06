# Task interpretation

The requested held-out endpoint is the number of genes in `151 TH Prkcd Grin2c Glut` whose
Wilcoxon Benjamini-Hochberg-adjusted p value is below 0.05 after sparse AAV CRISPR loss of
each held-out target.  The run manifest contains one held-out target, `Zfhx3`.  I treated the
answer as a point prediction for the missing `Zfhx3` focal-cell DEG count, not as a prediction
of target mRNA knockdown or organismal phenotype.

Two ambiguities were resolved conservatively:

- The focal cell label was interpreted with the atlas vocabulary: `TH` is thalamus and
  `Glut` is glutamatergic, so SCN, striatal, peripheral DRG, and olfactory/vomeronasal ZFHX
  biology are indirect.
- Large developmental or germline phenotypes were used only as priors for whether a gene can
  matter in neurons.  The quantitative prediction was calibrated to P16-to-P37/44 mosaic
  postmitotic NeuN+ perturbations in the supplied Perturb-seq data.

# Sources

- Input manifest:
  `[local file: 267_Zfhx3.csv]`.
- Focal-cell training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Full non-held-out DE surface:
  `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents same-experiment semantic corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`.
- PubMed-indexed ZFHX3/ZFHX2 literature:
  Miura et al. 1995, DOI `10.1074/jbc.270.45.26840`;
  Ido et al. 1994, DOI `10.1006/dbio.1994.1134`;
  Zhang et al. 2019, DOI `10.1016/j.expneurol.2019.113055`;
  Wilcox et al. 2017, DOI `10.1177/0748730417722631`;
  Perez Baca et al. 2024, DOI `10.1016/j.ajhg.2024.01.013`;
  Komine et al. 2012, PMID `23300874`;
  Habib et al. 2018, PMID `29253101`.

# Computations over the training data

I first read the focal training count CSV and the one-row held-out manifest.  `Zfhx3` is absent
from the 1,674 training targets, as expected.  The focal endpoint is strongly zero-inflated:
median `n_degs = 0`, 75th percentile `= 1`, 90th percentile `= 2`, and only 469/1,674 training
perturbations are nonzero.  Therefore a nonzero prediction needs target-specific support.

I queried the focal-cell DE rows in the parquet for literature-guided analogs and counters:
`Zfhx2`, `Zfp423`, `Tcf7l2`, `Ctnnb1`, `Rora`, `Bmal1`, `Nr1d1`, `Klf7`, and smaller
developmental transcription-factor comparators.  I also used `profile_compare` on the focal
cell score vectors for `Zfhx2`, `Zfp423`, `Tcf7l2`, `Rora`, `Bmal1`, and `Klf7`, with
`scores` as the signed profile value, `names` as features, and `pvals_adj < 0.05` as the
significance rule.  This computed full signed-profile correlations, positive/negative tail
overlaps, and significant-feature counts within exactly the held-out readout context.

The main observed counts at FDR 0.05 in `151 TH Prkcd Grin2c Glut` were:

| training target | focal `n_degs` | relevance to `Zfhx3` |
| --- | ---: | --- |
| `Zfhx2` | 0 | closest represented ZFHX-family perturbation; same zinc-finger/homeobox class but different biological axis |
| `Zfp423` | 150 | large zinc-finger developmental regulator with a strong thalamic state; not a ZFHX paralog |
| `Tcf7l2` | 106 | Wnt/TCF thalamic terminal-state regulator |
| `Ctnnb1` | 383 | beta-catenin partner response that validates Wnt/TCF sensitivity in the same cells |
| `Rora` | 278 | thalamic/circadian nuclear-receptor state, useful positive counterexample |
| `Bmal1` | 103 | core clock perturbation with a 151 response; only an indirect analogy to SCN Zfhx3 |
| `Nr1d1` | 116 | REV-ERB/core-clock comparator |
| `Klf7` | 1 | small postnatal thalamic TF response |
| `Brd1` | 4 | small chromatin-linked thalamic response |
| `Zfx` | 15 | small zinc-finger response |
| `Zfp148` | 8 | small zinc-finger response |
| `Zfp236` | 19 | small zinc-finger response |
| `Zfp521`, `Foxp2`, `Pou3f3`, `Pax6`, `Zic2`, `Rarb`, `Rarg`, `Ebf1`, `Ebf2`, `Ebf3` | 0 each | developmental TF/cofactor counters |

For `Zfhx2` specifically, the focal matched sample size was 203 perturbed nuclei versus 23,679
controls and no row passed FDR 0.05.  Its leading nominal focal scores also looked weak after
correction: `Gap43` score 3.65, `Inpp5a` score 3.35, `Dgkh` score -3.22, all with
`pvals_adj = 1.0`; `Zfhx3` and `Zfhx4` transcripts under `Zfhx2` perturbation had
`pvals_adj = 1.0`.  In the profile comparison, `Zfhx2` had no significant focal features and
only near-origin similarities to the stronger TF anchors; for example its whole-profile Pearson
correlations were 0.071 to `Rora`, 0.039 to `Zfp423`, 0.0004 to `Bmal1`, -0.011 to `Klf7`,
and -0.050 to `Tcf7l2`.

# Target-specific reasoning

## `Zfhx3`

**Relevant family analog: `Zfhx2`, observed `n_degs = 0`.**  `Zfhx2` is the strongest
within-family evidence because the other canonical ZFHX family member, `Zfhx4`, was not present
as a training perturbation.  The Distributed Agents corpus records `Zfhx2` as essentially flat in the
sampled central-brain screen: a single weak FDR<0.10 `Nt5c3` up-regulation in another
glutamatergic population and no broad transcriptional program.  Its known pain/nociceptor
biology was treated as off-axis because DRG neurons were not sampled; Habib et al. 2018 linked
ZFHX2 to a human pain-insensitivity disorder and DRG pain/neuropeptide targets, but those are
peripheral sensory contexts.  In the focal parquet slice, `Zfhx2` had zero DEGs and no
convincing low-FDR shadow signature.  The same corpus also reports that `Zfhx2` perturbation did
not cause compensatory `Zfhx3` or `Zfhx4` transcript rebound in any measured Zfhx2 group, so
acute ZFHX-family compensation is not visible at the mRNA level here.

**Positive thalamic TF counters: `Zfp423`, `Tcf7l2`/`Ctnnb1`, `Rora`, and
`Bmal1`/`Nr1d1`.**  These show that the focal thalamic cells are capable of producing strong
postmitotic TF-linked responses.  However, their Distributed Agents findings are pathway-specific rather
than a generic developmental-TF signature.  `Tcf7l2` and `Ctnnb1` converge on a beta-catenin/TCF
Wnt response with many down-regulated thalamic excitability and synaptic genes; `Zfp423`
rewires a distinct thalamic subtype/cell-surface state and is not phenocopied by its obvious
EBF, BMP/SMAD, retinoic-acid, ZIC, `Zfp521`, or `Chd4` neighborhood; `Rora`, `Bmal1`, and
`Nr1d1` define ROR/REV-ERB/circadian contrasts.  Those observed counts keep the baseline from
collapsing to zero for every transcription factor, but they are imperfect analogs for `Zfhx3`.

**Small-response TF counters: `Klf7`, `Brd1`, `Zfx`, `Zfp148`, and `Zfp236`.**  These calibrate
the low positive range.  `Klf7` is a neuronal developmental factor with external axon-growth
biology, yet the matching P16 thalamic perturbation has only one FDR<0.05 row in the training
endpoint.  `Brd1`, `Zfx`, `Zfp148`, and `Zfp236` similarly sit in the 4-19 DEG range.  If
`Zfhx3` retained a weak autonomous role in 151 cells, this is the range I would expect.

**Flat developmental counters.**  Numerous developmental transcription factors that are famous
in embryonic neurogenesis or sensory-system patterning were flat in the same endpoint
(`Pax6`, `Pou3f3`, `Foxp2`, `Zic2`, `Rarb`, `Rarg`, `Ebf1`/`2`/`3`, `Zfp521`).  This matters
because published ZFHX3 positives are also strongly context-tied.  ATBF1/ZFHX3 is induced
during neuronal differentiation in P19 cells and developing brain (Ido et al. 1994; Miura et al.
1995), Zfhx3 conditional knockout disrupts embryonic/early postnatal late-born D1 striatal MSN
differentiation and survival (Zhang et al. 2019), adult deletion alters SCN circadian period
and rhythmicity (Wilcox et al. 2017), and human ZFHX3 haploinsufficiency causes syndromic
intellectual disability with ZFHX3 binding near nervous-system-development promoters
(Perez Baca et al. 2024).  These are credible neuronal priors, but they do not specifically
nominate a thalamic glutamatergic maintenance program at P37-P44 after sparse P16 editing.

Putting those together, I predict that acute `Zfhx3` loss in recovered `151 TH Prkcd Grin2c Glut`
nuclei will behave more like the silent `Zfhx2`/developmental-TF group than like the large
`Zfp423`, Wnt/TCF, or ROR/clock states.  I therefore make the zero/nonzero call as **zero**.
The closest alternative would be a singleton or very small Klf7-like call, but the exact family
analog is zero and the assay-wide median is zero, so the integer point prediction is:

`Zfhx3 -> 0`.

# Limits

- `Zfhx3` itself was absent from both supplied training inputs and from the selected Distributed Agents
  corpus release; this is a genuine extrapolation from `Zfhx2`, unrelated thalamic TFs, and
  external biology.
- `Zfhx4`, the other close ZFHX paralog, was not available as an observed focal perturbation.
- The `Zfhx2` family analog is imperfect: ZFHX2 is tied to DRG pain biology, whereas ZFHX3 has
  stronger links to neuronal differentiation, SCN circadian coupling, human haploinsufficiency,
  and ataxia repeat-expansion disease.
- Strong `Zfp423`, `Tcf7l2`, `Ctnnb1`, `Rora`, `Bmal1`, and `Nr1d1` responses prove the 151
  cell group has enough power for some transcriptional regulators, but they do not establish a
  shared mechanism with `Zfhx3`.
- The endpoint counts only FDR<0.05 nuclear RNA changes in recovered cells.  A prediction of
  zero does not mean ZFHX3 is biologically irrelevant, unexpressed in every neuron, or
  unedited; it means I do not expect any measured gene to cross this assay's focal FDR cutoff.
