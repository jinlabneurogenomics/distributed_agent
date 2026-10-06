# Question and resolved ambiguities

The requested readout is the integer `n_degs` for each held-out perturbation in the
cell group `151 TH Prkcd Grin2c Glut`: the number of measured genes whose
Wilcoxon Benjamini-Hochberg adjusted p-value was below 0.05 in perturbed nuclei
versus matched controls.

This run has one requested held-out target:

| target_name | predicted_n_degs |
| --- | ---: |
| Uqcc2 | 1 |

I treated the gene knocked out by CRISPR as part of the tested expression
profile when it was present in the measured gene universe, because the training
DEG counts include on-target transcript decreases. In close respiratory-chain
comparators, several `n_degs = 1` calls were exactly this on-target decrease,
not a downstream stress program.

# Sources used

## Supplied data

- Held-out manifest:
  `[local file: 256_Uqcc2.csv]`
- Focal-cell training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Per-gene differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`

## Internal same-experiment corpus and runtime tools

- Distributed Agents corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`.
- The corpus had no direct bottom-up claims, findings, or first-hop related
  targets for `Uqcc2` itself.
- Corpus claim `claim:34681374c398d1920b0b`:
  represented complex III perturbations `Cyc1`, `Ttc19`, `Uqcrb`, `Uqcrc2`,
  `Uqcrfs1`, `Uqcrh`, and `Uqcrq` were largely buffered in neuronal nuclei and
  did not induce a shared complex-III depletion RNA signature.
- Corpus claim `claim:4818d59945fdf5715f28`:
  the sparse FDR-supported hits among represented complex-III-related targets
  were target-private rather than recurring across same-complex perturbations.
- Corpus claim `claim:30ab45a3b952026ae47a`:
  `Opa1` activated a detectable ATF4/mitochondrial ISR-like program in this
  neuronal snRNA-seq assay, whereas several other represented mitochondrial
  comparators did not cross that response threshold.
- Distributed Agents runtime profile comparison over the supplied focal-cell
  log-fold-change vectors for `Cyc1`, `Ttc19`, `Uqcrb`, `Uqcrc2`, `Uqcrfs1`,
  `Uqcrh`, and `Uqcrq`.

## External biology

- Tucker et al. 2013, PLoS Genetics, DOI 10.1371/journal.pgen.1004034,
  PMID 24385928: UQCC2 is a UQCC1-interacting complex III assembly factor
  related to yeast Cbp6p; UQCC1 and UQCC2 participate in cytochrome b biogenesis,
  and UQCC2-deficient fibroblasts have altered cytochrome b synthesis/stability.
- Wanschers et al. 2014, Human Molecular Genetics,
  DOI 10.1093/hmg/ddu357, PMID 25008109: UQCC3 acts downstream of UQCC1/UQCC2
  in complex III assembly and its loss impairs cytochrome b stability.
- Dennerlein et al. 2021, eLife, DOI 10.7554/eLife.68213,
  PMID 34969438: SMIM4 and C12orf73 interact with newly synthesized cytochrome b
  with UQCC1/UQCC2, placing UQCC2 in early complex III biogenesis.
- Liang et al. 2022, Cell Reports, DOI 10.1016/j.celrep.2022.111204,
  PMID 35977508: the COMA complex containing UQCC1/2 and C16ORF91 facilitates
  CYTB translation; later UQCC-containing complexes stabilize nascent CYTB and
  coordinate complex III biogenesis.
- Feichtinger et al. 2017, Oxidative Medicine and Cellular Longevity,
  DOI 10.1155/2017/7202589, PMID 28804536: human UQCC2 deficiency can produce
  severe neonatal disease with combined complex I/III biochemical deficiency,
  consistent with complex III assembly being required for respiratory-chain
  supercomplex stability.
- Fernandez-Vizarra and Zeviani 2015, Frontiers in Genetics,
  DOI 10.3389/fgene.2015.00134: review of nuclear structural subunits and
  assembly factors causing mitochondrial complex III deficiency.
- Quiros et al. 2017, Journal of Cell Biology,
  DOI 10.1083/jcb.201702058, PMID 28566324; Mick et al. 2020, eLife,
  DOI 10.7554/eLife.49178, PMID 32463360: mitochondrial dysfunction can engage
  ATF4/integrated-stress transcription, but engagement depends on the defect and
  metabolic context.

# Computational evidence

The training count table contained 1,674 focal-cell perturbations. Counts were
highly zero-inflated and heavy-tailed:

- 1,205 / 1,674 had `n_degs = 0`.
- 469 / 1,674 were nonzero.
- Median = 0; 75th percentile = 1; 90th percentile = 2; 95th percentile = 18.
- The largest broad responses, such as `Uba5` with 2,677 DEGs and `Tpr` with
  1,768, are outliers rather than representative mitochondrial behavior.

I queried the focal-cell training counts for complex III and respiratory-chain
genes. The direct complex III training analogs were:

| training target | role | observed `n_degs` in `151 TH Prkcd Grin2c Glut` |
| --- | --- | ---: |
| Cyc1 | complex III structural subunit | 1 |
| Ttc19 | complex III assembly/maintenance factor | 1 |
| Uqcrb | complex III structural subunit | 0 |
| Uqcrc2 | complex III core subunit | 1 |
| Uqcrfs1 | Rieske Fe-S complex III subunit | 0 |
| Uqcrh | complex III hinge protein | 0 |
| Uqcrq | complex III structural subunit | 1 |

The closest early complex III assembly factors were not available as perturbation
targets in the training count table:

- `Uqcc1`: absent
- `Uqcc3`: absent
- `Bcs1l`: absent
- `Lyrm7`: absent

I then read the focal-cell DE rows for the direct complex III analogs. There were
17,259 measured features per analog signature. The FDR-significant rows were
nearly all self hits:

| training target | significant row(s), `pvals_adj < 0.05` |
| --- | --- |
| Cyc1 | `Cyc1`, logFC -0.739, q = 2.94e-15 |
| Ttc19 | `Ttc19`, logFC -0.517, q = 1.42e-22 |
| Uqcrb | none |
| Uqcrc2 | `Uqcrc2`, logFC -0.576, q = 0.002997 |
| Uqcrfs1 | none; target row `Uqcrfs1` had logFC -0.340, q = 0.199 |
| Uqcrh | none |
| Uqcrq | `Gpr180`, logFC -0.466, q = 0.0429 |

This matters because it separates two possible sources of a one-count
prediction. `Cyc1`, `Ttc19`, and `Uqcrc2` did not reveal a broad complex III
stress state; their only significant gene was the edited transcript itself.
`Uqcrq` had a singleton downstream hit, but it was not shared by other complex
III perturbations.

I also computed signed expression-profile similarity among `Cyc1`, `Ttc19`,
`Uqcrb`, `Uqcrc2`, `Uqcrfs1`, `Uqcrh`, and `Uqcrq` using
`logfoldchanges` over the focal-cell rows. The runtime profile comparison used
the group filter

```text
group_name == "151 TH Prkcd Grin2c Glut"
```

with `gene_target` as the profile entity, `names` as the measured feature, and
`pvals_adj < 0.05` to mark FDR-supported features. Cosines between UQCR subunits
and `Cyc1`/`Ttc19` were moderate, roughly 0.66-0.74 for the inspected pairs, but
their top-tail overlap was small and the significant intersections were empty or
singletons. The profile evidence therefore supports a weak same-process
relationship among complex III genes while confirming the count-table result:
complex III perturbation did not drive a recurring FDR-scale transcriptional
state in this cell group.

As a mitochondrial positive counterexample, `Opa1` had 37 focal-cell DEGs with
clear ATF4/ISR-like genes such as `Asns`, `Mars1`, `Chac1`, `Ddit3`, aminoacyl
tRNA synthetases, and amino-acid transporters. That program was not seen for
complex III structural genes or `Ttc19`; other assayed OXPHOS and mitochondrial
targets in this same cell group were similarly flat or self-only, for example
`Coa8 = 0`, `Ndufv1 = 0`, `Ndufs2 = 1`, `Ndufa4 = 1`, `Sod2 = 1`, and
`Sucla2 = 1`.

# Target-specific reasoning

## Uqcc2

`Uqcc2` encodes an early complex III assembly factor. External work places UQCC2
with UQCC1 at the cytochrome b biogenesis step: Tucker et al. showed UQCC2
interacts with UQCC1 and is required for normal cytochrome b synthesis or
stability; Dennerlein et al. and Liang et al. later refined this into a COMA/COMB
early-assembly model in which UQCC1/2-associated proteins coordinate CYTB
translation and stabilization. UQCC3, assayed externally but not in the supplied
training set, acts downstream of UQCC1/UQCC2 in the same pathway. Those facts
make represented complex III perturbations the most appropriate within-dataset
analogs, especially `Ttc19` among the represented assembly/maintenance factors
and `Cyc1`, `Uqcrc2`, `Uqcrb`, `Uqcrfs1`, `Uqcrh`, and `Uqcrq` as structural
complex III boundaries.

The internal evidence argues strongly against a broad nonzero mitochondrial
stress response. All represented complex III comparators in the exact focal
cell group had 0 or 1 DEG. Their singleton calls were target-self decreases for
`Cyc1`, `Ttc19`, and `Uqcrc2`, no-call profiles for `Uqcrb`, `Uqcrfs1`, and
`Uqcrh`, and one nonrecurrent `Gpr180` call for `Uqcrq`. The same-experiment
Distributed Agents corpus summarizes this broader observation as high-confidence
evidence that represented respiratory complex III components are buffered at
the neuronal nuclear RNA level and do not induce a shared complex-III depletion
signature.

I therefore predicted no multi-gene downstream program for `Uqcc2`. I kept the
point estimate at `1` rather than `0` because `Uqcc2` itself was present in the
measured gene universe of this cell group, and several expressed complex III
neighbors crossed FDR only for their own transcript after editing. That is still
an extrapolation: `Uqcc2` target-RNA abundance and gRNA frameshift/NMD behavior
could make the self transcript miss the threshold, as happened for `Uqcrfs1`,
`Uqcrb`, and `Uqcrh`.

# Limits and uncertainty

- `Uqcc2` had no direct Distributed Agents target context in the internal corpus, and its
  closest same-pathway early assembly factors, `Uqcc1`, `Uqcc3`, `Bcs1l`, and
  `Lyrm7`, were not available as training perturbations.
- `Ttc19` is a complex III assembly/maintenance factor but is not a perfect
  phenocopy for UQCC2: TTC19 acts around UQCRFS1 turnover at mature complex III,
  while UQCC2 acts earlier at cytochrome b biogenesis.
- The supplied assay is sparse, acute, mosaic AAV CRISPR in juvenile
  postmitotic neurons with snRNA-seq as the endpoint. It does not directly
  measure complex III abundance, respiration, supercomplex stability, ROS, cell
  survival, or electrophysiology.
- The prediction hinges on a narrow threshold crossing. I expect no broad
  downstream FDR program; the difference between `0` and `1` is mainly whether
  the edited `Uqcc2` transcript itself would be called significant in this cell
  group.
