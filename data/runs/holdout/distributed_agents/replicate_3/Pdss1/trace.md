# Pdss1 DEG-count prediction trace

## Question and held-out target

The requested readout is the integer number of genes that would pass
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after each held-out
perturbation in `151 TH Prkcd Grin2c Glut` cells.

The held-out manifest
`[local file: 173_Pdss1.csv]`
contains a single requested target:

| target_name |
|---|
| Pdss1 |

## Sources used

- Endpoint training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  with 1,674 non-held-out targets.
- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
  There were no direct `Pdss1` findings or graph neighbors in this release, but
  the release had detailed within-dataset findings for `Coq5`, `Hmgcr`, and
  `Gpx4`.
- Distributed Agents runtime profile comparisons over the focal-cell DE signatures.
- PubMed and GeneReviews for external CoQ biology:
  Saiki et al. 2005, DOI `10.1111/j.1742-4658.2005.04956.x`, PMID 16262699;
  Nguyen et al. 2014, DOI `10.1016/j.bbalip.2014.08.007`, PMID 25152161;
  Malicdan et al. 2018, DOI `10.1002/humu.23345`, PMID 29044765;
  Salviati et al., *Primary Coenzyme Q10 Deficiency Overview*, GeneReviews
  2017, updated 2023;
  Mantle et al. 2023, DOI `10.3390/antiox12081652`, PMID 37627647;
  Munch et al. 2023, DOI `10.3390/antiox12030718`, PMID 36978966;
  Nardecchia et al. 2020, DOI `10.1002/acn3.51232`, PMID 33285023;
  Bellusci et al. 2021, DOI `10.1002/jmd2.12216`, PMID 34765390;
  Fessler et al. 2020, DOI `10.1038/s41586-020-2076-4`, PMID 32132706;
  Sasaki et al. 2020, DOI `10.1042/BSR20201289`, PMID 33165592.

## Dataset computations

The focal training endpoint is strongly zero-inflated: among the 1,674
training targets the median was 0 DEGs, the 75th percentile was 1, the 90th
percentile was 2, the 95th percentile was 18, and the maximum was 2,677.
Therefore the prior for a random held-out perturbation in this neuronal class
is "no detectable transcriptional response", and a nonzero call needs either a
same-pathway responder or a compelling analog with a broad focal signature.

I then searched the training table for CoQ biosynthesis, electron-transport,
mevalonate/prenylation, and redox/ferroptosis targets.  `Coq5` was the only
direct CoQ-biosynthesis enzyme represented in the focal training-count table;
`Pdss2`, `Coq2`, `Coq3`, `Coq4`, `Coq6`, `Coq7`, `Coq8a`, `Coq8b`, `Coq9`,
`Coq10a`, `Coq10b`, and `Hpdl` were not present as non-held-out focal
endpoints.

For the biologically relevant targets that were present, I queried the parquet
for the focal cell group and counted focal rows with `pvals_adj < 0.05` and
`pvals_adj < 0.10`.  The query was a direct filtered scan of the parquet by
`group_name` and a candidate `gene_target` list, followed by a groupwise count
over the 17,259 measured genes for each target.  I also inspected the smallest
adjusted-p rows per target to distinguish true downstream programs from
self-target RNA depletion.

| training perturbation | focal n_degs | focal FDR 0.10 genes | focal expression-pattern evidence |
|---|---:|---:|---|
| `Coq5` | 0 | 0 | Direct CoQ enzyme; no gene passed even FDR 0.10 in the focal group. |
| `Hmgcr` | 0 | 0 | Upstream mevalonate entry point; the smallest focal adjusted p-value was `Ints8`, q = 0.126, not a sterol or CoQ program. |
| `Fntb` | 0 | 0 | Farnesylation branch downstream of the mevalonate pathway; no focal DEG. |
| `Srebf1` | 0 | 0 | Lipid transcription factor counterexample; no focal DEG. |
| `Srebf2` | 7 | 7 | Positive sterol counterexample: down-regulated `Srebf2`, `Dhcr24`, `Insig1`, `Hmgcs1`, `Msmo1`, etc., showing sterol transcripts were assay-visible when a transcriptional regulator, not an enzyme, was perturbed. |
| `Uqcrfs1` | 0 | 0 | Complex III Rieske subunit; no focal DEG. |
| `Uqcrc2` | 1 | 1 | The lone DEG was the perturbed transcript, `Uqcrc2` itself. |
| `Cyc1` | 1 | 1 | The lone DEG was the perturbed transcript, `Cyc1` itself. |
| `Uqcrq` | 1 | 1 | Single off-pathway hit, `Gpr180`; no ETC or mitochondrial-stress program. |
| `Ndufs2` | 1 | 1 | The lone DEG was the perturbed transcript, `Ndufs2` itself. |
| `Ndufa10` | 1 | 1 | The lone DEG was the perturbed transcript, `Ndufa10` itself. |
| `Ndufa9` | 0 | 0 | Complex I subunit; no focal DEG. |
| `Ndufv1` | 0 | 0 | Complex I subunit; no focal DEG. |
| `Sdha` | 1 | 2 | The FDR 0.05 call was `Sdha` itself; `Edem2` reached only FDR 0.10. |
| `Cox5a` | 1 | 1 | The lone DEG was the perturbed transcript, `Cox5a` itself. |
| `Clpp` | 0 | 0 | Mitochondrial protease and stress counterexample; no focal DEG. |
| `Lonp1` | 0 | 0 | Mitochondrial protease and stress counterexample; no focal DEG. |
| `Gpx4` | 0 | 0 | Ferroptosis/lipid-peroxide counterexample; no focal DEG. |
| `Atp2a2` | 187 | 285 | Positive ER/ISR-stress control; robust focal induction of `Ddit3`, `Shmt2`, `Chac1`, etc. |

I also ran an exact Distributed Agents runtime profile comparison of the 19 focal
profiles in the table using signed Wilcoxon `scores` and the top/bottom 200
features per target.  The selected candidate set was not a coherent
low-amplitude mitochondrial module: across all 171 pairwise comparisons, median
top-tail overlap was 0.025 in the positive tail and 0.025 in the negative tail,
and the direct `Coq5` versus ETC pairs were near zero
(`Coq5`--`Uqcrfs1` Pearson r = 0.008, `Coq5`--`Uqcrc2` r = -0.008,
`Coq5`--`Cyc1` r = 0.009, `Coq5`--`Ndufs2` r = 0.006).  The leading `Coq5`
features were all nonsignificant with `node_significance = 1.0`, confirming
that the `Coq5` vector itself is essentially null rather than a muted version
of a reproducible ETC or stress signature.

## Internal corpus evidence

The Distributed Agents corpus did not contain direct `Pdss1` reports, so I used it only
for observed pathway analogs:

- `Coq5:F001`: acute `Coq5` loss produced zero downstream genes at FDR < 0.10
  in all 22 measured neuronal groups.  This matters for `Pdss1` because `Coq5`
  is in the same primary CoQ10 biosynthetic pathway as PDSS1.
- `Coq5:F002`: the expected ATF4/CHOP mitochondrial ISR program was absent
  after `Coq5`, even though the assay detected `Atf4`, `Ddit3`, `Herpud1`,
  and `Shmt2`-class stress genes after other perturbations.  `Atp2a2` in the
  focal group was the clearest local example of this detectability.
- `Coq5:F003`: neither unbiased nearest-neighbor search nor obvious literature
  comparators such as `Uqcrfs1`, `Uqcrc2`, `Cyc1`, `Ndufs2`, `Lonp1`, and
  `Clpp` phenocopied `Coq5`; score-space correlations were approximately zero.
- `Hmgcr:F001`, `Hmgcr:F003`, and `Hmgcr:F004`: acute `Hmgcr` loss was nearly
  flat and did not recover the `Srebf2` cholesterol-biosynthesis transcriptional
  module, so upstream lipid or isoprenoid enzymes cannot be pooled with
  `Srebf2` as broad predicted responders.
- `Gpx4:F001` to `Gpx4:F004`: `Gpx4` and represented glutathione,
  ferroptosis, and NRF/redox perturbations were transcriptionally inert or
  orthogonal in basal postnatal neuronal nuclei.  This weakens any argument
  that loss of a CoQ antioxidant function should automatically yield a large
  ferroptosis-like DEG count in recovered nuclei.

## Biology of Pdss1

PDSS1 is one subunit of mammalian polyprenyl diphosphate synthase.  Saiki et al.
showed that the mouse and human long-chain prenyl diphosphate synthases are
heterotetramers containing the Dps1/Sps1/PDSS1 subunit and the
Dlp1/PDSS2-related subunit, and that the mammalian pair determines the
ubiquinone side-chain product.  PDSS1, PDSS2, and COQ2 catalyze the early
assembly and attachment of the polyisoprenoid side chain of coenzyme Q, while
COQ5 is a mitochondrial C-methyltransferase in the downstream benzoquinone
ring-modification part of the same biosynthetic pathway (Nguyen et al. 2014;
Munch et al. 2023).

This makes `Coq5` the best available training analog, but not a perfect one:
PDSS1 affects tail synthesis upstream of COQ2, whereas COQ5 modifies the ring
later.  Human biallelic PDSS1 or COQ5 variants cause primary CoQ10 deficiency
with neurologic disease (Malicdan et al. 2018; Nardecchia et al. 2020;
Bellusci et al. 2021; Salviati et al. GeneReviews 2023; Mantle et al. 2023).
Those clinical data establish biological importance, but they are chronic,
often biallelic systemic disease states and cannot be mapped directly to a
3-to-4 week, sparse, partial CRISPR perturbation in recovered postmitotic
neurons.

CoQ loss could in principle impair complex I/II-to-III electron transfer,
increase mitochondrial stress through the OMA1-DELE1-HRI/eIF2alpha route
described by Fessler et al. 2020, activate ATF4/CHOP-class ISR transcripts as
in Sasaki et al. 2020, perturb sulfide oxidation, or alter lipid-peroxide
defense.  The same-experiment evidence argues that these consequences did not
appear as broad nuclear RNA programs after partial acute CoQ-pathway editing:
`Coq5` was flat, complex I/III/IV perturbations were flat or only depleted their
own target RNA, and `Gpx4`/redox neighbors were flat.

## Target-specific prediction

### Pdss1

Closest direct analog: `Coq5`, 0 DEGs in `151 TH Prkcd Grin2c Glut`, 0 genes at
FDR < 0.10 in the same focal parquet slice, and no pan-neuronal FDR < 0.10
response in the Distributed Agents corpus.  The observed `Coq5` profile is the strongest
within-dataset evidence because it tests the primary CoQ10 biosynthetic pathway
itself.

Mechanistic counterexamples:

- Complex III perturbations that should report a downstream ETC bottleneck
  were tiny: `Uqcrfs1` had 0 DEGs, `Uqcrc2` had only its own knocked-down
  transcript, `Cyc1` had only its own knocked-down transcript, and `Uqcrq` had
  one noncanonical singleton.
- Complex I, II, and IV perturbations were likewise mostly 0 or target-only:
  `Ndufa9` 0, `Ndufv1` 0, `Ndufs2` 1, `Ndufa10` 1, `Sdha` 1, `Cox5a` 1.
- `Hmgcr` and `Fntb` show that acute perturbation of the isoprenoid or
  prenylation neighborhood does not itself recover a broad focal program.
  `Srebf2` is not a phenocopy; it is a transcription-factor positive control
  for sterol transcripts and had only 7 focal DEGs.
- `Atp2a2` produced 187 DEGs including ISR genes, so the focal cell group and
  Wilcoxon pipeline could detect an ER/ISR stress state; the absence of such a
  state after `Coq5`, `Clpp`, and `Lonp1` makes a hidden CoQ-triggered stress
  module unlikely.

The approximate count is therefore not a small but definite multi-gene program;
it is below the assay's FDR threshold.  I predict that `Pdss1` would behave like
the direct `Coq5` CoQ-biosynthesis analog and the many one-gene ETC
counterexamples, giving 0 detected focal DEGs at FDR < 0.05.

## Limits and extrapolation

- `Pdss1` and `Pdss2` were held out or absent, so the closest observed
  same-pathway target is `Coq5`, a downstream CoQ enzyme rather than the exact
  prenyl-tail synthase.
- CoQ abundance, ETC flux, sulfide oxidation, lipid peroxidation, indel
  efficiency, and protein abundance were not measured.  A flat snRNA-seq
  profile does not prove intact mitochondrial metabolism.
- Human PDSS1 and COQ5 disease genetics come from chronic biallelic deficiency
  across tissues; the Perturb-seq assay is juvenile, postmitotic, mosaic, and
  partial.  Protein and CoQ pool turnover could buffer a 3-to-4 week neuronal
  perturbation even if a complete chronic deficiency is severe.
- The assay profiles recovered NeuN-positive nuclei.  If a complete `Pdss1`
  knockout killed a subset of edited neurons before harvest, the surviving
  nuclei could understate toxicity.
- Some singleton ETC DEGs are self-target RNA depletion and should not be
  interpreted as downstream pathway programs.  I therefore used them as
  counterexamples to a broad stress response, not as evidence for a shared
  one-gene PDSS1 signature.
