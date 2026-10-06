# DEG-count prediction trace

## Question and resolved ambiguities

The run asks for a point prediction of `n_degs`, the number of genes with
`pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` nuclei, for held-out
perturbations absent from both supplied training inputs. The manifest
`063_Dync1h1.csv` contains one requested target, `Dync1h1`, so the output table
must contain exactly one row in that order. I treated zero as a prediction that
no measured gene crosses FDR 0.05 and any positive integer as a nonzero focal
response in this same single-nucleus Wilcoxon/BH pipeline.

## Sources used

- Direct endpoint calibration: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  The focal training distribution has 1,674 targets; 1,205 are zero, 469 are
  positive, the median is 0, the 95th percentile is 18, and only 43 targets have
  at least 100 DEGs.
- Direct expression signatures: the focal slice of
  `[local file: training_de_all_cell_groups.parquet]`.
  I row-group filtered the 8.3 GB parquet to `group_name == "151 TH Prkcd
  Grin2c Glut"` and to a dynein/dynactin, kinesin, endolysosome/sterol, and
  microtubule candidate set, then counted `pvals_adj < 0.05` and intersected
  signed significant genes between candidates.
- Run-local profile tooling: `distributed_agents_runtime.profile_compare` and
  `profile_inspect`, using `gene_target` as the profiled entity, `names` as the
  feature, `logfoldchanges` as the signed value, and `pvals_adj < 0.05` as the
  significance criterion in the focal group. This reproduced the exact focal
  counts for the candidate cohort and showed that raw whole-profile similarity
  was dominated by sparse nonsignificant extreme logFC values, so I used exact
  FDR-level shared genes for the biological comparison.
- Same-experiment internal interpretation: Distributed Agents corpus
  `perturbai-july-260713-sourceguard-1773-v1`. There was no direct held-out
  `Dync1h1` target context, but the corpus contained `Dctn1`, `Htt`, `Kif1a`,
  and related cytoskeletal/transport claims from the non-held-out experiment.
- External mechanism literature from PubMed:
  - Waterman-Storer et al. 1997, DOI `10.1073/pnas.94.22.12180`, PMID
    `9342383`: p150Glued/dynactin antibodies disrupt dynein binding to
    dynactin and organelles and inhibit fast axonal transport.
  - Martin et al. 1999, DOI `10.1091/mbc.10.11.3717`, PMID `10564267`:
    genetic perturbation of cytoplasmic dynein heavy chain and Glued/dynactin
    disrupts fast axonal transport.
  - Urnavicius et al. 2015, DOI `10.1126/science.aaa4080`, PMID `25814576`:
    structural work showing the dynein-dynactin-BICD2 assembly.
  - Reck-Peterson et al. 2018, DOI `10.1038/s41580-018-0004-3`, PMID
    `29662141`: dynein-1 carries diverse interphase cargoes through dynactin
    plus cargo adaptors.
  - Zhao et al. 2016, DOI `10.1111/cns.12552`, PMID `27080913`, and Di Pizio
    et al. 2022, DOI `10.1242/jcs.260220`, PMID `36218033`: mouse `Dync1h1`
    alleles impair neuronal retrograde transport or DYNC1H1 dosage. I used
    these only as qualitative support that the heavy chain is limiting in
    neurons, not as quantitative germline-KO analogs.

## Same-assay computation

I first enumerated mechanistically relevant training targets from the focal
count CSV. There was no non-held-out dynein-1 subunit close to `Dync1h1`; the
closest represented cytoplasmic dynein partner was the dynactin p150Glued gene
`Dctn1`. Nearby counterexamples were mostly silent:

| training target | focal `n_degs` | interpretation |
| --- | ---: | --- |
| `Dctn1` | 75 | closest cytoplasmic dynein-1/dynactin motor-system analog |
| `Rab7` | 501 | broad endolysosomal/cholesterol response; useful as a module neighbor but less specific and much broader than dynein |
| `Tsc2` | 86 | mTOR/lysosome comparator that partially overlaps the sterol arm |
| `Mib1` | 27 | strong same-direction sterol overlap, not a transport-complex member |
| `Marchf6` | 14 | ER sterol-control comparator |
| `Selenoi` | 5 | compact same-direction sterol comparator |
| `Htt` | 3 | dynein/dynactin-linked trafficking gene with a very small focal sterol response |
| `Srebf2` | 7 | inverse sterol transcription-factor control, down where `Dctn1` is up |
| `Kif1a`, `Kif5a`, `Kif5c`, `Klc1`, `Klc2` | 1 each | measured kinesin/anterograde transport branch; almost all self-only |
| `Trak1`, `Rhot1`, `Hap1`, `Map6`, `Nin`, `Spast`, `Dync2h1`, `Dync2i1` | 0 each | cargo-adaptor, microtubule, and ciliary dynein counterexamples |
| `Tuba1a` | 7 | tubulin-isotype perturbation; a distinct tubulin compensation state |
| `Tuba4a` | 2 | sparse microtubule counterexample |
| `Map1b`, `Mapt`, `Mapre2` | 1 each | self-only or singleton microtubule counterexamples |

For the exact focal expression-pattern comparison I extracted the significant
rows for those candidates from the parquet. `Dctn1` had 49 upregulated and 26
downregulated DEGs. Its upregulated genes included a clear SREBF2/cholesterol
axis: `Insig1`, `Msmo1`, `Hmgcs1`, `Cyp51`, `Hmgcr`, `Fdft1`, `Fasn`, `Tecr`,
`Sqle`, `Dhcr24`, `Fdps`, `Ldlr`, `Stard4`, `Mvd`, `Dhcr7`, `Lss`, `Sc5d`,
`Nsdhl`, `Idi1`, and `Srebf2` itself. The smaller down arm included the target
`Dctn1`, plus neuronal/cytoskeletal genes such as `Plekhg1`, `Kcnc2`,
`Clasp2`, `Stmn4`, `Syt11`, `Gpm6a`, `Grin2b`, `Jun`, `Jund`, `L1cam`,
`Atg9a`, `Nin`, and `Atp2a2`.

The FDR-level overlaps separated real sterol neighbors from simple transport
neighbors:

- `Rab7` shared 39 of the `Dctn1` significant genes in the same direction,
  mostly sterol, lysosomal, and neuronal-state loci such as `Insig1`, `Msmo1`,
  `Hmgcs1`, `Cyp51`, `Hmgcr`, `Fdft1`, `Fasn`, `Sqle`, `Dhcr24`, `Fdps`,
  `Ldlr`, `Stard4`, `Dhcr7`, `Lss`, `Sc5d`, `Ptgds`, `Idi1`, `Lamp2`,
  `Srebf2`, and `Dpp7`; it also opposed 4 immediate-early/cytoskeletal genes.
- `Mib1` shared 21 same-direction sterol DEGs with `Dctn1`.
- `Tsc2` shared 13 and `Marchf6` shared 12 same-direction DEGs with `Dctn1`.
- `Selenoi` shared the compact positive set `Insig1`, `Msmo1`, and `Fdft1`.
- `Htt`, though focal-small, shared `Hmgcs1` and `Fasn` with `Dctn1`.
- `Srebf2` was the expected inverse control: `Insig1`, `Msmo1`, `Hmgcs1`,
  `Cyp51`, `Sqle`, `Dhcr24`, and `Srebf2` were significant in the opposite
  direction from `Dctn1`.
- `Kif1a`, `Kif5a`, `Kif5c`, `Klc1`, `Klc2`, `Trak1`, `Rhot1`, `Hap1`,
  `Map6`, `Nin`, `Tuba1a`, `Tuba4a`, `Dync2h1`, `Dync2i1`, `Map1b`, `Mapt`,
  `Mapre2`, and `Spast` had zero FDR-level overlap with the 75 `Dctn1` genes.

The Distributed Agents corpus mirrored this boundary. It reported that `Dctn1`
perturbation elicits a recurrent SREBF2-like sterol/cholesterol module that is
not a generic result of perturbing sampled cytoskeletal or trafficking genes;
that `Mib1`, `Dctn1`, `Htt`, `Marchf6`, `Rab7`, `Tsc2`, and `Selenoi`
neighborhoods repeatedly converge on cholesterol-homeostasis genes; that
`Srebf2` loss inversely validates the `Dctn1` sterol arm; and that represented
neuronal kinesin-1, Miro/TRAK, and Kif1a-related perturbations do not make a
shared soma-detectable transcriptional state in this assay.

## Target-specific reasoning for `Dync1h1`

### Why the prediction is nonzero

`Dync1h1` encodes the heavy chain of cytoplasmic dynein 1, the minus-end
microtubule motor that works with dynactin and activating adaptors to move many
membranous organelles and protein/RNA cargoes. `Dctn1`, the p150Glued subunit
of dynactin, is not just a remote cytoskeletal gene: dynactin physically couples
to dynein and cargo adaptors, and p150Glued/dynactin perturbation disrupts
dynein-dependent axonal transport. Because the only strong focal signature in
the measured cytoplasmic motor neighborhood is the `Dctn1` sterol/endolysosome
state, `Dync1h1` should be predicted to cross the FDR threshold rather than be
treated like the zero-heavy prior.

The expected program is not a pan-motor or pan-microtubule program. The
measured kinesin genes `Kif1a`, `Kif5a`, `Kif5c`, `Klc1`, `Klc2`, plus the
Miro/TRAK mitochondrial transport nodes `Rhot1` and `Trak1`, were all 0-1 DEG
in this focal class and shared none of `Dctn1`'s significant focal genes. The
ciliary dynein-2 heavy/intermediate genes `Dync2h1` and `Dync2i1` were also
zero. That pushes the estimate away from a broad "microtubule motor" heuristic
and toward a `Dctn1`-anchored cytoplasmic dynein-1 branch.

### Why the count is below broad endolysosomal hits

`Rab7` has 501 focal DEGs and intersects the `Dctn1` sterol arm strongly, but
it is a broader lysosome/endosome stress perturbation: its focal signature
contains hundreds of lysosomal, proton-pump, mTOR, stress, and synaptic genes
outside the 75-gene `Dctn1` surface. `Tsc2` also has 86 DEGs through
lysosome/mTOR biology but is not a direct motor-complex analog. I therefore did
not scale `Dync1h1` toward the `Rab7` 501 response.

I also put only limited weight on `Htt` and `Hap1`. Both are trafficking
partners in external biology, but `Htt` has only 3 focal DEGs and `Hap1` has 0;
the internal corpus explicitly notes that the HAP1/p150Glued/HTT relationship
does not suffice to make `Hap1` phenocopy `Dctn1` in this acute postnatal
transcriptomic assay.

### Count selected

The primary numeric anchor is `Dctn1` at 75 focal DEGs. I predicted a medium
nonzero `Dync1h1` response slightly below that anchor, 60 DEGs. The downward
adjustment reflects three assay-specific constraints:

- The readout is 3-4 weeks after sparse P16 CRISPR in postmitotic neurons; it
  can miss local axonal, organelle-positioning, or protein-turnover defects.
- Many directly assayed transport and microtubule perturbations were buffered
  at the nuclear RNA level despite canonical neuronal roles.
- `Dctn1` itself is the demonstrated same-assay sterol anchor, whereas
  `Dync1h1` is extrapolated from complex membership and dynein/dynactin
  mechanism rather than observed in the parquet.

The prediction is still close to `Dctn1` because `Dync1h1` is the core
dynein-1 motor, not a peripheral cargo adaptor, and a disruption of dynein
heavy chain should plausibly reach the same endolysosomal/sterol feedback
state as p150Glued loss in susceptible thalamic neurons.

## Limits

The largest uncertainty is that the best within-dataset analog, `Dctn1`, is a
dynactin subunit rather than a dynein heavy chain. The training perturbations
did not include cytoplasmic dynein-1 intermediate, light-intermediate, or light
chain genes as focal analogs, so I could not check a dynein-1 subcomplex series.
Conversely, ciliary dynein-2 genes are not mechanistically close enough to make
their zero responses decisive for cytoplasmic dynein 1.

The sterol state is also secondary. The focal parquet shows a robust
transcriptional SREBF2/cholesterol response after `Dctn1`, but it does not
measure dynein processivity, lysosome position, autophagic flux, sterol
content, protein abundance, indels, or selective loss of edited nuclei.
Therefore the prediction extrapolates from a same-experiment transcriptional
phenocopy to the held-out motor gene; it is not a direct estimate of biological
severity or viability.
