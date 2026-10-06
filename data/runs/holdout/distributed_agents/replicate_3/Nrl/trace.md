# Prediction trace

## Question and resolution

The held-out manifest for this run contains one requested perturbation:
`Nrl`. I interpreted the requested endpoint as the exact held-out count
`n_degs` for acute AAV-PHP.eB CRISPR loss of `Nrl` in `151 TH Prkcd Grin2c
Glut`, where `n_degs` counts measured genes with Scanpy Wilcoxon
Benjamini-Hochberg `pvals_adj < 0.05`.

`Nrl` is absent from both supplied training tables, so I did not use an observed
`Nrl` endpoint. I transferred from held-in perturbations in the same focal cell
group and from the known NRL photoreceptor transcriptional hierarchy.

## Sources used

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed focal-cell
  `n_degs` for 1,674 non-held-out targets.
- `training_de_all_cell_groups.parquet`: Wilcoxon scores, log2 fold changes,
  adjusted p-values, and matched cell counts for focal-cell signatures.
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`.
- Distributed Agents runtime `profile_compare` / `profile_inspect`: signed Wilcoxon
  score-vector comparisons among candidate retinal and bZIP analogs in the
  focal cell group.
- NCBI PubMed literature searches for retinal NRL/CRX/NR2E3 biology.

External literature grounding:

- Mears et al., 2001, Nature Genetics, DOI `10.1038/ng774`, PMID `11694879`:
  mouse `Nrl` deletion eliminates rod function and converts the retinal rod
  program toward S-cone-like photoreceptors.
- Oh et al., 2008, Brain Research, DOI `10.1016/j.brainres.2008.01.028`,
  PMID `18294621`: NRL binds the `Nr2e3` promoter, cooperates with CRX, and
  places `Nr2e3` downstream of NRL in rod-versus-cone fate control.
- Hennig, Peng, and Chen, 2007, Brain Research, DOI
  `10.1016/j.brainres.2007.06.036`, PMID `17662965`: CRX-associated
  photoreceptor regulatory networks center on CRX with rod-enriched NRL and
  NR2E3 as subtype regulators.

## Dataset computations

I first read the held-out manifest and verified that the only target is `Nrl`.
Then I summarized the training endpoint CSV:

- 1,674 held-in perturbations in `151 TH Prkcd Grin2c Glut`.
- 1,205/1,674 had `n_degs = 0`.
- The median was `0`; the 75th percentile was `1`; the 95th percentile was
  `18`; the maximum was `2,677`.

For focal-cell expression evidence, I filtered the parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and to candidate analog
`gene_target` values. Each complete focal profile had 17,259 measured genes.
I used the adjusted p-values to avoid overinterpreting very large log-fold
changes on unsupported rare genes.

I also queried the same focal group with `names` in retinal sentinels
`Nrl`, `Crx`, `Nr2e3`, `Rho`, `Gnat1`, `Pde6b`, `Opn1sw`, `Opn1mw`, `Otx2`,
`Rorb`, and `Thrb` across all 1,674 training perturbations. `Nrl` itself was
measured but never moved: its minimum adjusted p-value across all held-in
perturbations was exactly `1.0`, with scores from `-0.0059` to `0.2456`.
`Crx`, `Gnat1`, `Nr2e3`, `Opn1sw`, and `Otx2` also had minimum adjusted
p-value `1.0`; `Rho` bottomed out at `0.970`.

Finally, I compared signed Wilcoxon score vectors for the candidate analog
cohort with Distributed Agents runtime profile tools. Among 18 observed retinal/bZIP
targets, 17 had no FDR-significant focal features; `Mafg` had one
FDR-significant positive feature. Pairwise score correlations among the
`Crx`/`Nr2e3`/`Otx2`/`Rorb`/MAF neighborhood were tiny rather than a coherent
module: for example, the largest `Crx` whole-profile Pearson among inspected
photoreceptor or MAF peers was `0.049` against `Rxra`, and `Nr2e3` was
similarly near zero against its closest inspected peers.

## Target-specific reasoning

### Nrl

Biology:

`Nrl` is a neural-retina leucine-zipper transcription factor with its decisive
loss-of-function phenotype in rod photoreceptors. In that native context, NRL
acts with CRX and activates `Nr2e3`; loss of NRL removes rod function and
pushes rod precursors toward an S-cone-like program. This is a strong retinal
mechanism, but it is expected to require photoreceptor or pineal lineage
context, not generic postmitotic thalamic glutamatergic neurons.

Held-in analogs and counterexamples in `151 TH Prkcd Grin2c Glut`:

| comparator | observed `n_degs` | expression evidence and interpretation |
| --- | ---: | --- |
| `Crx` | 0 | Direct NRL partner in the photoreceptor network; focal profile had 0/17,259 FDR-significant genes and minimum adjusted p-value `1.0`. |
| `Nr2e3` | 0 | Canonical NRL downstream rod nuclear receptor; focal profile had 0/17,259 FDR-significant genes and minimum adjusted p-value `0.830`. |
| `Otx2` | 0 | Upstream/related photoreceptor homeobox regulator connected to CRX expression; focal profile had 0 significant genes and minimum adjusted p-value `1.0`. |
| `Rorb` | 0 | Retinal photoreceptor fate regulator and ROR-family nuclear receptor; despite broader brain expression, its focal perturbation had 0 significant genes and minimum adjusted p-value `1.0`. |
| `Thrb`, `Rxra`, `Rxrb`, `Rxrg` | 0 each | Cone/retinoid/nuclear-receptor comparators represented in training; all were FDR-silent at the endpoint. |
| `Neurod1`, `Neurod2` | 0 each | Photoreceptor/neurogenic transcription-factor comparators; both had 0 significant focal genes and minimum adjusted p-value `1.0`. |
| `Maf`, `Mafa`, `Mafb` | 0 each | MAF/bZIP family comparators; all were silent in the focal endpoint, arguing against a shared MAF-family response in this cell type. |
| `Mafg` | 1 | Small-MAF comparator with only a single significant feature, `Lamp2`, not a retinal state or NRL-like module. |
| `Nfe2l1`, `Nfe2l2`, `Bach2`, `Jund`, `Atf6`, `Fosl2` | 0 each | More distant bZIP counterexamples; useful mostly to keep the MAF/bZIP-family prior low. |
| `Rora`, `Nr1d1` | 278, 116 | Positive nuclear-receptor controls in the same training count table; these show that the assay can detect transcription-factor and nuclear-receptor effects in this cell group, but they are not close NRL analogs and should not pull `Nrl` upward. |

Distributed Agents same-experiment corpus:

The corpus has no frozen `Nrl` claims or related-target edges. It does,
however, connect `Crx` and `Nr2e3` through a high-confidence claim that the
postnatal neuronal screen lacks the lineage context needed to recover canonical
CRX/NR2E3 photoreceptor transcriptional programs. `Crx` has an additional
corpus finding that retinal comparators represented in the parquet, including
`Otx2`, `Rorb`, `Neurod1`, `Nr2e3`, `Rxrg`, and `Thrb`, did not reveal a hidden
CRX-like module in postnatal brain DE surfaces. These are the most relevant
observed analogs for held-out `Nrl`.

Decision:

The dataset evidence dominates here. Every direct NRL retinal-network partner
available in the held-in focal endpoint is at 0 DEGs, and the measured retinal
sentinel genes are inert across the whole training set. The one nearby
exception, `Mafg`, has only a singleton non-retinal feature. General bZIP or
nuclear-receptor membership is too broad to overcome the much more specific
CRX/NR2E3/Otx2/Rorb evidence.

Predicted `n_degs`: **0**.

## Limits

- The prediction extrapolates from `Crx`, `Nr2e3`, and other retinal regulators
  because `Nrl` itself is held out and has no observed same-experiment
  signature.
- The assay measured acute, sparse, postnatal neuronal CRISPR loss of function;
  it cannot test embryonic retinal rod genesis, purified rods, or a germline
  `Nrl` knockout.
- Some comparators are imperfect: `Otx2`, `Rorb`, `Thrb`, and `Neurod` genes
  have functions outside photoreceptors, while MAF/small-MAF/NFE2L/AP-1
  proteins share bZIP architecture without being true substitutes for NRL.
- The conclusion is about the FDR-count endpoint. It does not prove absence of
  editing or absence of any small molecular consequence below the Wilcoxon
  FDR threshold.
