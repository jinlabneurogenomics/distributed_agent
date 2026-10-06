# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The requested endpoint is the held-out `n_degs` for each requested perturbation in
`151 TH Prkcd Grin2c Glut`: the number of measured genes with Wilcoxon
Benjamini-Hochberg adjusted `pvals_adj < 0.05` in perturbed nuclei versus the
matched non-targeting controls.

The only requested held-out target in this shard is `Nfkb2`. Its own DEG rows
and count are absent from the supplied training parquet and focal training-count
CSV, so I treated its requested focal-cell count as absent from the declared
inputs and inferred it from non-held-out pathway neighbors and external
mechanism.

## Sources used

- Declared DEG-count training CSV:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This gives the directly observed focal `n_degs` for 1,674 non-held-out
  perturbations.
- Declared differential-expression parquet:
  `training differential-expression dataset`.
  I queried exact rows for `151 TH Prkcd Grin2c Glut` to confirm the relevant
  NF-kappaB/TNFR/TLR perturbations were true FDR-null profiles rather than
  targets with a few large corrected effects.
- Run-local dataset context and measurement registry. These defined the assay as
  sparse P16 AAV-CRISPR loss of function in postmitotic NeuN-positive mouse
  neurons, with P37-P44 snRNA-seq readout, and made clear that self-transcript
  knockdown is not an editing-efficiency filter.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`. I used bounded target Findings
  and reports for `Nfkb1`, `Chuk`, `Traf3`, `Rel`, `Cd40`, and `Tnfrsf1a`.
  This corpus is a packaged interpretation of the same experiment, not
  independent replication of the parquet.
- External literature:
  Sun 2012, Immunological Reviews, DOI `10.1111/j.1600-065X.2011.01088.x`,
  PMID `22435551`, for the NIK/IKKalpha/TRAF3/p100-p52 noncanonical
  NF-kappaB pathway; Sun 2010, Cell Research, DOI `10.1038/cr.2010.177`,
  PMID `21173796`, for `Nfkb2` p100 as both the p52 precursor and a RelB
  inhibitor; Mukherjee et al. 2017, EMBO Journal, DOI
  `10.15252/embj.201796919`, PMID `29061763`, for RelB-dependent LTbetaR
  noncanonical signaling and the inhibitory role of unprocessed p100; Snow et
  al. 2013, Molecular Neurobiology, DOI `10.1007/s12035-013-8555-y`, PMID
  `24122352`, for the activity-dependent character of neuronal NF-kappaB in
  synaptic plasticity and memory.

## Computation over the declared dataset

I first read the requested-target CSV and found a single target, `Nfkb2`. I then
queried the focal training-count table for NF-kappaB and upstream receptor
perturbations represented in this split.

Direct focal-cell counts from the training CSV:

| training perturbation | observed `n_degs` in `151 TH Prkcd Grin2c Glut` | relationship to `Nfkb2` |
|---|---:|---|
| `Nfkb1` | 0 | NF-kappaB-family p105/p50 paralog/partner axis; tests whether an NF-kappaB transcription-factor subunit is tonically required |
| `Rel` | 0 | Rel-family NF-kappaB transcription factor; not the RelB:p52 dimer, but a direct NF-kappaB nuclear-family comparator |
| `Chuk` | 0 | IKKalpha, the kinase directly downstream of NIK that phosphorylates p100 to trigger p52 generation |
| `Traf3` | 0 | upstream negative regulator of NIK; a useful opposite-sign comparator because its loss can release noncanonical signaling |
| `Cd40` | 0 | TNFR-family receptor capable of noncanonical NF-kappaB activation in immune contexts |
| `Tnfrsf1a` | 0 | TNF receptor with canonical NF-kappaB/MAPK/death signaling, included as a receptor-level NF-kappaB counterexample |
| `Map3k7` | 0 | TAK1, upstream of canonical IKK/NF-kappaB and MAPK signaling |
| `Tlr2`, `Tlr3`, `Tlr4`, `Tlr5`, `Tlr7`, `Tlr8` | all 0 | receptor-level innate-immune inputs that should expose a stimulus-responsive inflammatory module if it were constitutively on in these neurons |

For the focal raw parquet rows I selected these targets, counted
`pvals_adj < 0.05`, and inspected nominal leaders and candidate NF-kappaB-panel
genes. The row counts agreed with the training CSV: every listed comparator had
0 FDR 0.05 genes in `151 TH Prkcd Grin2c Glut`. The best corrected focal rows
were still nonsignificant: `Chuk` had one top nominal gene, `Cops2`, at
FDR 0.727; `Rel` had one subthreshold row, `Ptcd3`, at FDR 0.140; `Nfkb1`,
`Traf3`, `Cd40`, `Tnfrsf1a`, `Map3k7`, and the TLR perturbations had minimum
focal adjusted P values of 1.0. Directly assayed pathway-panel rows such as
`Nfkb2`, `Nfkb1`, `Rel`, `Relb`, `Rela`, `Chuk`, `Traf3`, `Traf2`, `Cd40`, and
`Tnfrsf1a` were also uncorrected in these perturbations, so the zero-count calls
are not masking a focal compensatory `Nfkb2`/`RelB`/TNFR expression program.

The training distribution itself was zero-heavy: 469 of 1,674 non-held-out
perturbations were positive, the median was 0, the 75th percentile was 1, and
the mean of 14.1 was inflated by a small tail of very broad perturbations such
as `Uba5`, `Tpr`, and `Sin3a`. That means a pathway neighborhood of repeated
zeros is informative for a zero prediction, while a small positive integer
would require a specific reason that `Nfkb2` escapes the local NF-kappaB null.

## Target-specific reasoning

### `Nfkb2`

`Nfkb2` encodes p100, the precursor of p52. In the noncanonical NF-kappaB
pathway, a subset of TNF-receptor-family inputs stabilizes NIK, NIK activates
IKKalpha/`Chuk`, and IKKalpha-dependent p100 processing yields p52/RelB dimers
that enter the nucleus. Basally, TRAF3-containing ubiquitin ligase complexes
keep NIK levels low; loss of `Traf3` is therefore mechanistically opposite to
loss of the downstream p100/p52 substrate. This causal layout makes `Chuk` the
closest represented same-branch loss-of-function analog for held-out `Nfkb2`,
with `Traf3`, `Cd40`, and `Tnfrsf1a` serving as upstream tests of whether the
noncanonical/TNF receptor module is active in the assayed neuronal state.

The within-dataset evidence argues for a focal zero:

- `Chuk` loss produced 0 focal DEGs despite targeting the kinase needed for
  stimulus-induced p100 processing. In the same-experiment corpus, `Chuk` was
  also a pan-measured neuronal null: 0 downstream FDR 0.10 genes across the
  22 recovered neuronal groups, and a curated panel including `Nfkbia`,
  `Nfkbie`, `Nfkb1`, `Nfkb2`, `Rel`, `Rela`, `Relb`, `Tnfaip3`, `Birc3`,
  `Ccl2`, `Ccl5`, `Cxcl10`, `Il6`, `Tnf`, `Nos2`, `Ptgs2`, and `Icam1` was
  absent from the `Chuk` surface.
- `Nfkb1` loss produced 0 focal DEGs and was reported in the same-experiment
  corpus as 0 downstream FDR 0.10 genes in all 22 recovered neuronal groups.
  It is not the same subunit as NFKB2/p100-p52, but it is a direct test of
  whether an NF-kappaB transcription-factor precursor/subunit is tonically
  driving the P16->P37/44 neuronal transcriptome.
- `Rel` loss, another NF-kappaB-family nuclear subunit, produced 0 focal DEGs;
  its best focal row was only FDR 0.140.
- `Traf3` loss produced 0 focal DEGs. Because TRAF3 loss should release NIK and
  favor noncanonical activation where the branch is poised, this opposite-sign
  perturbation is an important counterexample: neither removing the available
  `Chuk` effector nor releasing an upstream brake produced a corrected focal
  expression response.
- `Cd40`, `Tnfrsf1a`, `Tnfrsf11a`, `Tnfrsf13c`, `Tnfrsf4`, `Tnfrsf9`, and the
  training TLRs were also 0 in the focal count table. Their biology is more
  peripheral to `Nfkb2`, but all point in the same direction: unchallenged,
  NeuN-enriched juvenile thalamic neurons do not show a tonic TNFR/TLR/NF-kappaB
  module in this CRISPR screen.

External mechanism does not provide a strong reason to override those zeros.
`Nfkb2` is essential in ligand-activated noncanonical NF-kappaB, immune,
stromal, B-cell, and osteoclast contexts; the experiment instead sparsely
perturbed postmitotic neurons after early development, supplied no LTbetaR,
CD40, BAFFR, RANK, TNF, TLR, injury, seizure, or pathogen-mimic stimulus, and
depleted glia and immune cells with NeuN-positive sorting. In that causal
context the path from `Nfkb2` loss to a measured focal DEG count would require
basal p100/p52/RelB activity in recovered `151 TH Prkcd Grin2c Glut` nuclei;
the available `Chuk`, `Traf3`, `Nfkb1`, `Rel`, and receptor perturbations all
argue that this branch is off or strongly buffered. I therefore predict no
genes pass FDR 0.05 for held-out `Nfkb2`.

Final point prediction: `Nfkb2 = 0`.

## Limits and uncertainty

- `Nfkb2` itself was held out. There is no direct `Nfkb2` CRISPR signature in
  either declared input, and the best unavailable comparators, `Relb`,
  `Map3k14`/NIK, `Ikbkb`, `Ikbkg`, `Birc2`, `Birc3`, and TNF/LTbeta receptors
  central to the noncanonical branch, were also absent as perturbation targets
  in this training split.
- The NF-kappaB comparators have focal matched perturbed-cell counts in the
  156-226 range. That is adequate to reject a broad `Uba5`- or `Sin3a`-scale
  response, but a very small signature could still fail the FDR cutoff.
- `Chuk` is upstream of p100 processing rather than p100 itself, and complete
  loss of p100 can remove both precursor substrate and inhibitory IkappaBdelta
  functions. The prediction assumes that in basal focal neurons the p100
  inhibitory and p52 activating roles are both too weak to cross the Wilcoxon
  FDR threshold after partial mosaic CRISPR.
- Same-experiment reports are semantic summaries of the same parquet. I used
  them to target interpretation of `Nfkb1`, `Chuk`, `Traf3`, `Rel`, `Cd40`, and
  `Tnfrsf1a`, not as independent evidence.
- A receptor, inflammatory, injury, activity, or glial co-culture challenge
  could expose NF-kappaB2 biology that this basal NeuN-positive screen was not
  designed to measure.
