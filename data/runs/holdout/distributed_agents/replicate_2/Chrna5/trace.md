# DEG-count prediction trace for `Chrna5`

## Question and endpoint

The requested held-out target list contains one perturbation, `Chrna5`. I
interpreted the endpoint as the exact assay-specific count of measured genes in
`151 TH Prkcd Grin2c Glut` with Benjamini-Hochberg adjusted Wilcoxon
`pvals_adj < 0.05`, using all measured genes including the target transcript
itself. The focal class label denotes thalamic glutamatergic neurons: `TH` is
thalamus, `Prkcd` and `Grin2c` are markers, and `Glut` is the transmitter
class.

The main ambiguity I resolved was how much to trust nicotinic-receptor family
membership. I treated it as a way to nominate candidate comparators, not as a
phenocopy rule: the same-experiment data show that represented nicotinic
subunits are nearly all transcriptionally buffered in the focal class.

## Sources used

- Input count table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  This is the authoritative source for the training endpoint at FDR 0.05.
- Input DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
  I queried focal-class rows for cholinergic and nicotinic training targets to
  identify which measured genes, if any, drove the observed counts.
- Held-out manifest:
  `[local file: 039_Chrna5.csv]`,
  confirming that the sole required row is `Chrna5`.
- Same-experiment Distributed Agents corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`, for packaged interpretations of
  `Chrna3`, `Chrna4`, `Chrna7`, `Chrnb2`, and cross-target nicotinic receptor
  findings. The corpus did not contain `Chrna5`, consistent with this being a
  held-out perturbation.
- Local Distributed Agents gene annotation tables:
  STRING v12.0 physical-interaction edges, CORUM v5.0 complexes projected to
  mouse with MGI one-to-one orthology classes downloaded 2026-09-13, and
  MyGene/GO annotations. These were used only to define mechanistic neighbors.
- PubMed literature on `Chrna5`/nAChR circuitry:
  Hsu et al. 2013, DOI 10.1523/JNEUROSCI.2927-13.2013, PMID 24227714;
  Fowler et al. 2011, DOI 10.1038/nature09797, PMID 21278726;
  Frahm et al. 2011, DOI 10.1016/j.neuron.2011.04.013, PMID 21555077;
  Morton et al. 2018, DOI 10.1523/JNEUROSCI.0023-18.2018, PMID 29954848;
  Husson et al. 2020, DOI 10.1523/JNEUROSCI.0356-19.2020, PMID 32184221.

## Computational checks

I loaded the manifest and the focal training count table directly. The training
set had 1,674 focal-class counts: 1,205 were zero and 469 were nonzero. Around
the cholinergic/nicotinic pathway, the focal FDR 0.05 counts were:

| training target | focal `n_degs` |
|---|---:|
| `Chrna3` | 0 |
| `Chrna4` | 2 |
| `Chrnb2` | 1 |
| `Chrna2` | 0 |
| `Chrna6` | 0 |
| `Chrna7` | 0 |
| `Chrnb3` | 0 |
| `Chrna1` | 0 |
| `Chrnb1` | 0 |
| `Chrnd` | 0 |
| `Chrne` | 0 |
| `Chrng` | 0 |
| `Ache` | 1 |
| `Chrm2` | 0 |
| `Chrm3` | 0 |

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and
those targets. The only adjusted focal hits among these comparators were:

- `Chrna4`: `Chrna4` log2FC -0.337, FDR 0.00373, and `Cyp46a1` log2FC -0.195,
  FDR 0.00373.
- `Chrnb2`: `Chrnb2` log2FC -0.517, FDR 7.37e-07, with no non-self FDR 0.05
  genes.
- `Ache`: `Ache` log2FC -0.674, FDR 0.00415, with no non-self FDR 0.05 genes.
- `Chrna3`, `Chrna2`, `Chrna6`, `Chrna7`, `Chrnb3`, the muscle nAChR
  subunits, and `Chrm2/3` had no focal gene with `pvals_adj < 0.05`.

The local annotation tables mark `Chrna5` as a measured protein-coding
perturbation target and place it in projected CORUM complexes
`CHRNA3-CHRNA5-CHRNB2` and `CHRNA3-CHRNA5-CHRNB4`. STRING v12.0 also gives
physical-interaction edges from `Chrna5` to `Chrna3`, `Chrna4`, `Chrnb2`,
`Chrnb4`, and other nicotinic subunits. `Chrnb4`, the closest beta4 partner for
alpha3/alpha5-containing habenular receptors, was absent from the training
count table, so the strongest assayed direct neighbors were `Chrna3`, `Chrnb2`,
and `Chrna4`.

## Target-specific analogs and rationale

### `Chrna5`

`Chrna5` encodes the alpha5 nicotinic acetylcholine receptor subunit, an
accessory subunit of pentameric nAChRs rather than an independently gating
homomeric receptor. Its best-known mouse circuit literature centers on
alpha5-containing nAChRs in the habenulo-interpeduncular nicotine-aversion
axis. Fowler et al. showed that `Chrna5` loss increased nicotine intake and
reduced IPN activation after nicotine, Frahm et al. tied alpha3/beta4/alpha5
signaling in the medial habenula to nicotine aversion, Hsu et al. found strong
alpha5 reporter expression in GABAergic interpeduncular/raphe/tegmental
neurons with only low medial-habenula mRNA, and Morton et al. showed that
`Chrna5`-expressing IP neurons mediate primed aversion and have markedly
reduced nicotinic responses in alpha5-null mice. Husson et al. similarly placed
beta4-containing nAChRs in MHb/IPN and VTA nicotine reinforcement control.

The best within-dataset analogs were:

- `Chrna3`, focal `n_degs = 0`: alpha3 is a close alpha5 partner in the
  alpha3/beta4/alpha5 and annotated alpha3/alpha5/beta receptor complexes.
  The Distributed Agents corpus summarizes `Chrna3` as a pan-surface basal
  transcriptome null with no FDR<0.10 downstream gene across the assayed
  postnatal neuronal groups. In the focal FDR 0.05 table it had zero hits.
- `Chrnb2`, focal `n_degs = 1`: beta2 is a direct annotated `Chrna5` complex
  member in CORUM and a major neuronal nAChR beta subunit. Its focal signal was
  only its own transcript; the corpus notes that every group with significant
  `Chrnb2` mRNA depletion had zero non-`Chrnb2` FDR<0.10 downstream genes.
  This is a strong counterexample to assuming that knocking out an nAChR
  subunit creates a receptor-homeostasis RNA program.
- `Chrna4`, focal `n_degs = 2`: alpha4 can coassemble with beta2-containing
  neuronal nAChRs and is the only represented nAChR alpha subunit with a focal
  non-self hit. That hit was the isolated thalamic sentinel `Cyp46a1`, not an
  acetylcholine-receptor, synaptic, or immediate-early gene module; the
  Distributed Agents corpus specifically reports that `Chrnb2` and other represented
  relatives did not reproduce the `Chrna4`/`Cyp46a1` response.
- `Chrna2`, `Chrna6`, `Chrna7`, and `Chrnb3`, focal `n_degs = 0`: these are
  less proximal but still neuronal nAChR subunits. They bound the receptor
  family null: no broad activity-regulated, cholinergic-subunit compensation,
  or shared downstream signature appeared in the focal class.
- `Ache`, focal `n_degs = 1`, and `Chrm2/3`, focal `n_degs = 0`: these are
  cholinergic-pathway but not same-complex comparators. Their near-null focal
  counts argue that simply perturbing acetylcholine signaling in this basal
  P16-to-P37/44 neuronal assay was not enough to create many FDR 0.05 DEGs.

I therefore predicted `Chrna5` as a zero rather than a 1-2 gene singleton. The
external mechanism says alpha5 loss should be most visible in receptor current,
nicotine response, and MHb/IPN circuitry; the focal cell class is thalamic
glutamatergic rather than the GABAergic interpeduncular population emphasized
by Hsu and Morton. The same-experiment training data say that even directly
assayed nAChR partners usually leave the delayed basal snRNA-seq transcriptome
flat in `151 TH Prkcd Grin2c Glut`, and the only plausible positive
counterexample, `Chrna4`, produced one non-self `Cyp46a1` hit that failed to
generalize to its beta2 partner or the receptor family.

### Limits and extrapolation

- `Chrna5` itself was completely held out, so the point estimate is an
  extrapolation from pathway neighbors plus external biology.
- `Chrnb4`, arguably the closest beta partner for alpha3/beta4/alpha5
  habenular receptors, was also absent from the focal training counts.
- The focal group is a coarse thalamic glutamatergic class. A rare
  alpha5-expressing subpopulation could be diluted below FDR significance, and
  the parquet does not provide raw single-nucleus expression or DNA indels.
- This prediction is for sparse postnatal CRISPR loss of function measured as
  basal nuclear RNA 3-4 weeks later. It should not be read as a prediction of
  nicotine-evoked currents, receptor trafficking, neurotransmitter release, or
  germline `Chrna5` behavioral phenotypes.
- The endpoint count includes possible self-transcript loss. I did not promote
  `Chrna5` to a one-gene prediction solely for a possible self row because
  self-RNA knockdown is an inconsistent CRISPR reporter in this experiment and
  the closest low-count comparators were split between self-only and complete
  focal nulls.

## Final point prediction

`Chrna5`: 0 differentially expressed genes at FDR 0.05 in
`151 TH Prkcd Grin2c Glut`.
