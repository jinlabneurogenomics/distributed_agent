# DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and resolved ambiguities

The requested prediction is the integer number of measured genes expected to pass
BH-adjusted Wilcoxon `pvals_adj < 0.05` after a held-out `Rara` CRISPR
loss-of-function perturbation in `151 TH Prkcd Grin2c Glut` cells. I treated the
endpoint as the screen-specific `n_degs` count in the supplied training CSV, not
as a measure of RARalpha biological importance, viability, editing efficiency,
or absolute transcriptome shift.

The requested-target manifest contained one target:

| held-out target | semantics |
|---|---|
| `Rara` | unranked scalar count prediction |

`Rara` was held out completely, so neither the `Rara` expression signature nor
its focal `n_degs` count was present in the supplied parquet or count table.

## Sources used

- Declared differential-expression parquet:
  `training differential-expression dataset`.
- Declared focal training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared held-out target manifest:
  `single-target request for Rara`.
- Dataset portrait `perturbai-atlas-v5`, task bindings, compact coverage, and
  capability manifest in `codex_runtime/pipeline`.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, specifically its bounded
  Findings/report summaries for `Rarb`, `Rarg`, `Rxra`, `Rxrb`, `Rxrg`, and
  `Stra6`. This corpus is a semantic layer over the same Perturb-seq experiment;
  it was used for interpretation and cross-target summaries, not as independent
  replication.
- External PubMed literature for RAR/RXR molecular function and neuronal
  RARalpha biology: Petkovich and Chambon 2022,
  doi:10.1530/JME-22-0097, PMID 36149754; le Maire and Bourguet 2014,
  doi:10.1007/978-94-017-9050-5_3, PMID 24962880; Aoto et al. 2008,
  doi:10.1016/j.neuron.2008.08.012, PMID 18957222; Maghsoodi et al. 2008,
  doi:10.1073/pnas.0804801105, PMID 18840692; Poon and Chen 2008,
  doi:10.1073/pnas.0807740105, PMID 19073915; Soden and Chen 2010,
  doi:10.1523/JNEUROSCI.3660-10.2010, PMID 21159962; Sarti et al. 2013,
  doi:10.1523/JNEUROSCI.1710-13.2013, PMID 23843516; Hsu et al. 2019,
  doi:10.1073/pnas.1820690116, PMID 30782829; Suzuki et al. 2021,
  doi:10.1016/j.celrep.2021.109918, PMID 34731624; Duester 2023,
  doi:10.1016/j.yfrne.2023.101099, PMID 37647946.

## Quantitative calibration

The supplied count table contained 1,674 non-held-out perturbations for the
focal cell group. The focal endpoint was highly sparse:

| statistic | `n_degs` |
|---|---:|
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| mean | 14.05 |
| max | 2677 |
| training perturbations with `n_degs = 0` | 1205 / 1674 |

I then read the focal rows of the DE parquet for RAR/RXR relatives and related
nuclear receptors. Each focal perturbation had 17,259 measured genes and 23,679
matched control nuclei:

| training perturbation | focal perturbed nuclei | focal `n_degs` at FDR 0.05 | best focal adjusted p-value | reason for comparison |
|---|---:|---:|---:|---|
| `Rarb` | 273 | 0 | 1.000000 | closest assayed RAR paralog; all-trans-RA receptor that binds RXR partners |
| `Rarg` | 168 | 0 | 1.000000 | closest assayed RAR paralog; same receptor subfamily |
| `Rxra` | 247 | 0 | 1.000000 | obligate canonical RAR heterodimer partner |
| `Rxrb` | 249 | 0 | 0.541213 | RAR heterodimer partner and RXR paralog |
| `Rxrg` | 229 | 0 | 0.437463 | RAR heterodimer partner and neuronal RXR paralog |
| `Stra6` | 195 | 0 | 1.000000 | retinol-uptake/RA-availability comparator upstream of RAR signaling |
| `Nr2f1` | 306 | 2 | 0.009942 | nuclear-receptor counterexample with a tiny focal signal |
| `Thra` | 241 | 3 | 0.000002 | RXR-partner nuclear receptor with a tiny focal signal |
| `Rora` | not rechecked from parquet | 278 | not rechecked from parquet | unrelated neuronal nuclear receptor showing that this class can respond strongly |
| `Nr1d1` | not rechecked from parquet | 116 | not rechecked from parquet | unrelated nuclear-receptor counterexample with a broad focal response |

The six RA-axis comparators were also flat when considered outside the focal
group. A direct all-cell-group scan of the parquet for `Rarb`, `Rarg`, `Rxra`,
`Rxrb`, `Rxrg`, and `Stra6` covered 2,263,364 rows and 134 target-by-cell-group
tests. None had a gene at FDR 0.05. Only two single genes reached a looser
FDR 0.10 threshold: `Rarb` in `022 L5 ET CTX Glut` with best FDR 0.088013, and
`Rxrb` in `110 CNU-HYa HY MM Glut` with best FDR 0.095747. The same-experiment
July corpus summarized the same pattern: represented RAR/RXR-family
perturbations did not form a convergent acute neuronal retinoid module, `Rxra`
and `Rxrg` were globally buffered, `Rarg` was a stringent postnatal neuronal
null, and `Stra6` did not induce a neuronal RA-starvation transcriptome.

I also checked the focal expression of canonical RA feedback and metabolism
genes under the related perturbations. In `Rarb`, `Rarg`, `Rxra`, `Rxrb`,
`Rxrg`, and `Stra6` cells, `Dhrs3`, `Cyp26a1`, `Cyp26b1`, `Cyp26c1`,
`Crabp1`, `Crabp2`, `Rbp1`, `Aldh1a1`, `Aldh1a2`, `Aldh1a3`, `Rara`, `Rarb`,
`Rarg`, `Rxra`, `Rxrb`, `Rxrg`, and `Stra6` all had focal adjusted p-values of
1.0. Thus the zero counts were not hiding an obvious subthreshold RAR-feedback
state in the focal thalamic glutamatergic group.

## Target-specific reasoning

### `Rara`

`Rara` encodes RARalpha, one of the three retinoic-acid receptors. Classical RA
signaling uses RAR isotypes bound with RXR isotypes on RA-response elements,
with ligand-dependent exchange of corepressor and coactivator complexes
(Petkovich and Chambon 2022, PMID 36149754; le Maire and Bourguet 2014,
PMID 24962880). The closest direct training analogs are therefore `Rarb` and
`Rarg`; the strongest obligate-complex partners are `Rxra`, `Rxrb`, and `Rxrg`;
and `Stra6` is an upstream retinol-transport comparator that would be expected
to create a secondary RA-starvation signature if cell-autonomous retinol uptake
were limiting.

All of those exact analogs had `n_degs = 0` in the requested cell group. Their
focal signatures were essentially flat: `Rarb`, `Rarg`, `Rxra`, and `Stra6` had
minimum adjusted p-values of 1.0 across 17,259 focal measured genes; `Rxrb` and
`Rxrg` had only nonsignificant minima of 0.541 and 0.437. Across all assayed
cell groups, the RA-axis perturbations also lacked any FDR 0.05 gene, with only
two isolated FDR 0.10 singletons outside the focal thalamic group. These
training signatures are the main basis of the prediction. They say that acute
single-gene disruption of the RAR/RXR branch at P16 is not a limiting driver of
steady-state nuclear RNA in recovered juvenile neurons under basal conditions.

The same-experiment corpus supplied useful falsifiers. `Rarb` had one weak L5
extratelencephalic `Arhgef4` near-hit but no broad RA program and no shared
phenotype in represented RAR/RXR family members. `Rarg`, `Rxra`, `Rxrg`, and
`Stra6` were null or near-null over almost every neuronal group. `Rxrb` produced
only a one-gene `Pafah1b1` near-hit in a hypothalamic glutamatergic group. These
findings were endpoint-adjacent because they inspected the same DE readout and
the same single-gene CRISPR modality, but they were not used as graph scores or
relation counts.

External biology keeps the `Rara` prediction from being a generic "RAR genes do
nothing" statement. RARalpha has mature neuronal functions: activity blockade
can trigger neuronal RA synthesis and RARalpha-dependent, local translational
control of AMPA-receptor trafficking during homeostatic plasticity (Aoto et al.
2008, PMID 18957222; Maghsoodi et al. 2008, PMID 18840692; Poon and Chen 2008,
PMID 19073915); FMRP is required for the RA-dependent branch of that response
(Soden and Chen 2010, PMID 21159962); RA can suppress inhibitory transmission
through an RARalpha/FMRP-dependent mechanism (Sarti et al. 2013,
PMID 23843516); hippocampal RARalpha deletion perturbs enriched-environment
metaplasticity through mTOR-dependent AMPA-receptor expression (Hsu et al.
2019, PMID 30782829); and RARalpha activation can trigger synaptic scaling-like
rapid antidepressant physiology independently of eEF2K (Suzuki et al. 2021,
PMID 34731624). Those papers make `Rara` more plausible than `Rarg` as a mature
neuronal RA receptor, but the best-supported mechanism is hippocampal and
synaptic, partly non-genomic/local-translational, and often activity-challenge
dependent; Duester 2023 (PMID 37647946) also cautioned that the non-genomic
RARalpha model needs direct endogenous-ligand genetic validation. It therefore
does not override the flat single-gene RAR/RXR training perturbations for a
basal thalamic snRNA-seq DEG-count endpoint.

I considered two counterexamples before settling on a zero. First, other
nuclear receptors can be seen in the focal cell group: `Rora` had 278 DEGs,
`Nr1d1` had 116, `Thra` had 3, and `Nr2f1` had 2. This means the Wilcoxon
snRNA-seq assay can detect postmitotic nuclear-receptor perturbations in
`151 TH Prkcd Grin2c Glut`; it does not rescue `Rara`, because the retinoid
receptor branch itself was specifically buffered. Second, RARalpha can regulate
autophagy-related and synaptic pathways in external models. I found no matching
training evidence that the focal RA-axis knockouts induced Lamp2a/Hspa8,
AMPAR, immediate-early, Cyp26/Dhrs3, or RAR-feedback DE programs; among direct
components in the training count file, `Fmr1`, `Camk2a`, `Gria1`, and `Gria2`
were focal zeros and `Mtor` had only 2 DEGs, so those mechanisms were too
endpoint-mismatched to justify a positive count.

Prediction: `Rara` is most likely another buffered/near-null retinoid receptor
perturbation in the focal class. I predict `0` rather than a small positive
count because every exact RAR/RXR comparator was a focal zero, the focal
RA-target rows were FDR 1.0 under those comparators, and the broader
all-cell-group family surface had no FDR 0.05 event. A one- or two-gene outcome
would not be surprising given the skewed count distribution and RARalpha's
external neuronal roles, but the evidence did not support making it the point
prediction.

## Limits

- `Rara` itself was absent from the training expression and count inputs; this
  is an extrapolation from `Rarb`, `Rarg`, `Rxra`, `Rxrb`, `Rxrg`, `Stra6`, and
  related nuclear receptors.
- The RA-axis nulls are conditioned on sparse AAV CRISPR delivered at P16,
  3-4 weeks of recovery, NeuN-enriched surviving nuclei, and basal whole-brain
  sampling. They do not rule out embryonic RA patterning, hippocampal synaptic
  physiology, choroid-plexus or retinal retinoid transport, glial RXR biology,
  pharmacological RA stimulation, or compound RAR/RXR loss.
- Self-transcript changes were not used as editing readouts. DNA indels and
  protein loss were not directly measured.
- `151 TH Prkcd Grin2c Glut` is a broad thalamic glutamatergic class; a
  smaller RARalpha-sensitive subpopulation or an activity-dependent state could
  be diluted below FDR.
- The July corpus and the parquet are derived from the same Perturb-seq
  experiment, so agreement between them is consistency of representations, not
  replication.
