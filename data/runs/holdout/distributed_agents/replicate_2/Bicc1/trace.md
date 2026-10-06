# Held-out DEG-count prediction

## Question and resolved ambiguities

The task is to predict, for each requested held-out perturbation, the number of
genes that would have passed Benjamini-Hochberg adjusted Wilcoxon `pvals_adj <
0.05` in the focal `151 TH Prkcd Grin2c Glut` neuronal group. The single
requested target in this run is `Bicc1`.

I treated `151 TH Prkcd Grin2c Glut` as the thalamic glutamatergic class from
the Allen-style taxonomy, not as a tyrosine-hydroxylase dopaminergic label. I
also treated `n_degs` as a response-breadth endpoint under the specific
postnatal AAV CRISPR and single-nucleus Wilcoxon assay. A flat signature is not
evidence that the guide pool failed, because the experiment measured nuclear
RNA in recovered neurons and target self-RNA depletion is known to be a weak
proxy for functional editing in this screen.

## Sources used

- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Focal-cell training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Requested target manifest:
  `[local file: 025_Bicc1.csv]`
- Distributed Agents same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`
- PubMed literature retrieved for Bicc1 biology:
  Maisonneuve et al. 2009, DOI `10.1242/dev.038174`, PMID `19666828`;
  Tran et al. 2010, DOI `10.1242/dev.046045`, PMID `20215348`;
  Kraus et al. 2011, DOI `10.1002/humu.21610`, PMID `21922595`;
  Piazzon et al. 2012, DOI `10.1093/jmcb/mjs027`, PMID `22641646`;
  Ota et al. 2014, DOI `10.1038/npp.2014.227`, PMID `25178406`;
  Rothe et al. 2015, DOI `10.1128/MCB.00341-15`, PMID `26217012`;
  Shen et al. 2018, DOI `10.1016/j.brainresbull.2018.10.004`, PMID
  `30316917`;
  Minegishi et al. 2021, DOI `10.1038/s41467-021-24295-2`, PMID `34210974`;
  Maerker et al. 2021, DOI `10.1038/s41467-021-25464-z`, PMID `34531379`;
  Dowdle et al. 2022, DOI `10.3389/fcell.2022.981696`, PMID `36158189`;
  Rothe et al. 2023, DOI `10.1371/journal.pbio.3002302`, PMID `37733651`.

The Distributed Agents corpus had no direct bottom-up claim, finding, or explicit
reference for `Bicc1`, so the internal evidence below comes from the raw
training matrix and from claims about represented Bicc1-adjacent perturbations.
The useful corpus claims were:

- `claim:a8a38aa8426e4484d967`: represented Wnt/Frizzled/ROR/RYK/PCP
  receptor-layer perturbations are largely transcriptionally buffered or
  nonconvergent in postnatal neuronal nuclear RNA.
- `claim:0c3fd06761c948f2fc28`: represented ciliary and ciliopathy genes do not
  form a shared postnatal neuronal RNA module.
- `claim:ad4a0296dcb7226557e1`: represented single-gene miRNA/RISC/TNRC6
  effectors are flat, sparse, or nonconvergent rather than one shared acute
  neuronal miRNA-loss state.
- `claim:7c7d49a966e1e00f2385`: adjacent mRNA decay and translation-control
  factors have factor-specific liabilities rather than one generic
  decay/translation-loss RNA module.

## Computational checks

I first read the requested manifest and found exactly one held-out target:
`Bicc1`. The focal training table contained 1,674 non-held-out perturbations;
1,205 of them had `n_degs = 0`, 363 had 1-9 DEGs, 63 had 10-99 DEGs, and 43
had at least 100 DEGs. The endpoint is therefore heavily zero-inflated in the
exact cell group being predicted.

The parquet has 616,253,184 rows, so I used PyArrow row-group statistics and
predicate filters rather than loading the whole table into memory. The focal
group occupies 35 row groups. For a declared set of Bicc1-adjacent training
targets, I read only these rows:

```python
dset = ds.dataset(parquet_path, format="parquet")
filt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(analogs)
)
tbl = dset.to_table(
    columns=["names", "gene_target", "logfoldchanges",
             "pvals_adj", "n_pert_matched"],
    filter=filt,
)
```

For each analog I then recomputed the focal FDR count as
`sum(pvals_adj < 0.05)` and checked the minimum adjusted p value to see whether
the training endpoint was exactly flat or just below the cutoff. The counts
matched the training CSV.

I also scanned `names == "Bicc1"` across all 1,674 focal training profiles.
`Bicc1` itself is a measured transcript in this cell group, but no training
perturbation significantly changed it; the smallest adjusted p value was
0.195, after `Zbtb7a` perturbation. Thus there was no measured upstream
knockout that cleanly created a Bicc1-low signature in the focal data.

## Bicc1 target reasoning

### Biology of the held-out gene

`Bicc1` encodes a conserved KH-domain and SAM-domain RNA-binding protein.
External work links it to three mechanisms:

- It can repress or stabilize selected 3-prime UTR targets through RNA-binding
  condensates and microRNA/Ccr4-Not/TNRC6-type machinery. For example, Bicc1
  regulates `Pkd2` by antagonizing miR-17 in kidney development, cooperates
  with Dicer1 and Ccr4-Not/Cnot3 to repress `Dand5`, and polymerizes through
  its SAM domain to localize and silence bound mRNAs
  (Tran 2010; Piazzon 2012; Rothe 2015; Minegishi 2021; Maerker 2021; Rothe
  2023).
- Bicc1 loss causes renal and left-right patterning phenotypes connected to
  ciliary signaling and polycystin biology (Maisonneuve 2009; Tran 2010; Kraus
  2011; Rothe 2023).
- Bicc1 can modulate Dvl/Wnt output, and has been implicated in neuronal
  stress/depression models through BICC1 expression changes and
  TrkB/mTOR/AMPA signaling in prefrontal cortex or hippocampus (Kraus 2011;
  Ota 2014; Shen 2018; Dowdle 2022).

Those mechanisms nominate plausible neighbors, but they also argue against a
very broad focal nuclear-RNA response. Much of the ciliary and left-right work
is embryonic or epithelial; the better-supported direct Bicc1 targets are
selected 3-prime UTRs rather than a global transcriptional program; and the
neuronal reports are cortical/hippocampal activity or depression paradigms
rather than sparse P16 loss-of-function in thalamic glutamatergic neurons.

### Wnt/PCP and ciliary analogs in the training set

The strongest same-experiment analogs for Bicc1's developmental cilia/Wnt
phenotypes were almost completely silent in the focal endpoint.

Wnt/PCP receptor-layer or receptor-adjacent training perturbations:

| target | focal `n_degs` | expression-pattern evidence |
| --- | ---: | --- |
| `Fzd2` | 0 | minimum focal `pvals_adj = 1.0` |
| `Fzd4` | 0 | minimum `pvals_adj = 1.0` |
| `Fzd6` | 0 | minimum `pvals_adj = 0.875` |
| `Fzd9` | 0 | minimum `pvals_adj = 0.357` |
| `Lrp5` | 0 | minimum `pvals_adj = 1.0` |
| `Lrp6` | 4 | only a weak four-gene response, minimum `pvals_adj = 0.0406` |
| `Ror1` | 0 | minimum `pvals_adj = 0.830` |
| `Ror2` | 0 | minimum `pvals_adj = 1.0` |
| `Ryk` | 0 | minimum `pvals_adj = 1.0` |
| `Prickle1` | 0 | minimum `pvals_adj = 1.0` |

The Distributed Agents Wnt/PCP claim over `Fzd2`, `Fzd6`, `Fzd9`, `Lrp5`, `Prickle1`,
`Ror1`, `Ror2`, and `Ryk` explicitly interprets these signatures as buffered,
sparse, or nonconvergent rather than a shared Wnt/PCP RNA module. This is the
most direct within-dataset warning against assigning `Bicc1` a positive count
just because it has a Wnt/Dvl mechanism in embryonic systems.

Primary-cilium, transition-zone, or polycystic/ciliopathy analogs in the same
focal group were even flatter:

| target | focal `n_degs` | expression-pattern evidence |
| --- | ---: | --- |
| `Pkd1` | 0 | minimum `pvals_adj = 1.0` |
| `Bbs5` | 0 | minimum `pvals_adj = 0.220` |
| `Ift43` | 0 | minimum `pvals_adj = 0.847` |
| `Ift81` | 0 | minimum `pvals_adj = 0.391` |
| `Ift88` | 0 | minimum `pvals_adj = 1.0` |
| `Kif3b` | 0 | minimum `pvals_adj = 1.0` |
| `Armc9` | 0 | minimum `pvals_adj = 1.0` |
| `Cep290` | 0 | minimum `pvals_adj = 0.650` |
| `Cspp1` | 0 | minimum `pvals_adj = 1.0` |
| `Lztfl1` | 0 | minimum `pvals_adj = 0.195` |
| `Ttc21b` | 0 | minimum `pvals_adj = 0.459` |

The corpus' ciliary claim, anchored by `Armc9`, `Cep290`, `Cspp1`, `Lztfl1`,
and `Ttc21b`, makes the same point at the semantic layer: acute postnatal
neuronal ciliary-gene perturbations can have isolated sparse effects, but they
are not a shared ciliopathy module. Bicc1 is not a structural IFT or
transition-zone component, so a stronger response than this entire measured
primary-cilium panel would be an extrapolation.

### RNA-silencing and translation-control analogs

Bicc1's direct molecular activity is post-transcriptional, so I also compared
it with represented miRNA/RISC, TNRC6, Ccr4-Not, exonuclease, and GIGYF-family
perturbations:

| target | focal `n_degs` | reason for comparison |
| --- | ---: | --- |
| `Ago1` | 1 | Argonaute core of miRNA repression |
| `Ago2` | 0 | Argonaute core of miRNA repression |
| `Dicer1` | 0 | miRNA biogenesis and reported Bicc1-Dicer cooperation |
| `Tnrc6a` | 0 | GW182/TNRC6 effector adjacent to Bicc1-mediated silencing |
| `Tnrc6b` | 0 | second represented TNRC6 effector |
| `Cnot1` | 0 | Ccr4-Not scaffold; Bicc1 can recruit Ccr4-Not through Cnot3 in node cells |
| `Xrn1` | 20 | general 5-prime-to-3-prime decay branch |
| `Gigyf1` | 0 | GIGYF-family translation repression scaffold |
| `Gigyf2` | 17 | related 4EHP/GIGYF translation-control scaffold |
| `Hbs1l` | 0 | ribosome rescue/quality-control neighbor used in the Gigyf2 corpus contrast |

The single-node miRNA effector controls were 0 or 1 DEG in the focal cell type;
the broader `Xrn1` and `Gigyf2` branches had small but real medium responses.
That pattern argues that the assay could see RNA-metabolism defects when they
spread into RNA-processing or protein-quality-control states, but that loss of
one sequence-specific or miRNA-adjacent repressor is usually buffered at
steady-state nuclear RNA. The Distributed Agents corpus reaches the same conclusion:
the represented miRNA/RISC/TNRC6 nodes do not define a shared acute neuronal
module, and adjacent mRNA decay/translation factors produce factor-specific
rather than generic signatures.

### Counterexamples I did not average into Bicc1

Several measured targets had much larger focal footprints, but they were poor
quantitative analogs for Bicc1.

- `Ctnnb1` and `Tcf7l2` had 383 and 106 DEGs respectively. These are direct
  nuclear effectors of beta-catenin/TCF transcription, whereas Bicc1 is an
  upstream RNA-binding modulator of selected Wnt/Dvl contexts. Their large
  responses show that the focal assay can detect a Wnt-transcription-factor
  phenotype, not that every upstream Wnt regulator should be assigned a
  beta-catenin-sized signature.
- `Tsc2` had 86 DEGs and `Mtor` had 2. Bicc1 has been linked to
  TrkB/mTOR/AMPA signaling in depression and ketamine models, but those reports
  used prefrontal or hippocampal signaling readouts and are less direct than
  the flat Wnt/ciliary/mRNA-decay training neighborhoods for this thalamic
  snRNA endpoint.
- `Psmb4`, `Psmc1`, and `Uba5` had 742, 430, and 2,677 DEGs. They overlap
  partially with the small `Gigyf2` stress/RNA-processing state in the
  Distributed Agents corpus, but they are proteasome/UFMylation stress perturbations,
  not direct Bicc1 pathway members.

## Final zero/nonzero decision

The within-dataset evidence favors no FDR-significant downstream genes for
`Bicc1` in `151 TH Prkcd Grin2c Glut`:

- all represented Bicc1-like ciliary and PKD controls in the focal group were
  exact zeros;
- all but one represented Wnt/PCP receptor-layer controls were exact zeros, and
  the exception `Lrp6` had only 4 DEGs;
- the represented miRNA/TNRC6/Ccr4-Not controls closest to Bicc1's silencing
  machinery were exact zeros or one-gene responses;
- the larger RNA-processing and Wnt-transcription-factor responses came from
  mechanistically more global or downstream nodes.

I therefore predict `Bicc1` will be below the FDR threshold in this cell group:

| target | predicted `n_degs` |
| --- | ---: |
| `Bicc1` | 0 |

## Limits

This is an extrapolation because `Bicc1` itself was completely held out, had no
same-experiment corpus entry, and lacked a measured close paralog or direct
`Pkd2`/`Cnot3`/`Dvl2`/`Anks3`/`Anks6` perturbation in the focal training counts.
The external Bicc1 literature is strongest in embryonic left-right organizers,
kidney epithelia, Xenopus embryos, and cortical or hippocampal depression
models, so it does not precisely match P16-to-P37/P44 mosaic loss in recovered
thalamic glutamatergic neuronal nuclei. The snRNA-seq Wilcoxon readout also
does not measure cilium geometry, P-body assembly, target 3-prime UTR binding,
translation, AMPA phosphorylation, or beta-catenin localization. A small
protein-level or subcellular phenotype after Bicc1 loss could therefore be
present even if the predicted DEG count is zero.
