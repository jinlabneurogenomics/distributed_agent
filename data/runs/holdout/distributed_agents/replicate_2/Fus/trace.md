# Fus held-out DEG-count prediction

## Question and endpoint

The manifest for this run contains one held-out perturbation:

```text
Fus
```

I interpreted the requested value as the focal-cell endpoint in
`151 TH Prkcd Grin2c Glut`: the count of measured genes with
`pvals_adj < 0.05` after knocking out the requested mouse target by the same
P16 AAV-PHP.eB sparse CRISPR loss-of-function design. `Fus` is held out, so
its count and DE signature are absent from both the focal training-count CSV
and the differential-expression parquet.

The main ambiguity is that `n_degs` is not an intrinsic effect size. It is the
number of whole-gene snRNA-seq Wilcoxon hits in recovered, class-assigned
nuclei, so the prediction has to be shrunk toward what this assay recovers
from partial, mosaic postnatal knockouts rather than toward embryonic-null or
ALS-mutant phenotypes.

## Sources used

- Authoritative training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Authoritative training DE statistics:
  `[local file: training_de_all_cell_groups.parquet]`.
- Held-out manifest:
  `[local file: 083_Fus.csv]`.
- Distributed Agents same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`. I queried `target_context`
  for `Fus`, `Tardbp`, `Hnrnpu`, `Hnrnpa2b1`, and `Snrnp70`; `Fus` had no
  corpus entry in this held-out run.
- Distributed Agents Runtime profile comparison:
  `profile_neighbors` over the focal-cell rows of the parquet, using signed
  `logfoldchanges`, `pvals_adj < 0.05`, and all 1,674 eligible training
  perturbations from the focal count CSV.
- External literature retrieved through NCBI PubMed:
  - Kwiatkowski et al. 2009, Science, DOI `10.1126/science.1166066`,
    PMID `19251627`: FUS/TLS mutations cause familial ALS and mutant FUS
    accumulates in neuronal cytoplasm.
  - Vance et al. 2009, Science, DOI `10.1126/science.1165942`,
    PMID `19251628`: FUS mutations cause ALS6 and connect FUS to RNA
    splicing/transport and TARDBP-like RNA dysregulation.
  - Hoell et al. 2011, Nature Structural and Molecular Biology, DOI
    `10.1038/nsmb.2163`, PMID `22081015`: FUS, EWSR1, and TAF15 form the FET
    RBP family and have broadly similar RNA-binding profiles.
  - Lagier-Tourenne et al. 2012, Nature Neuroscience, DOI `10.1038/nn.3230`,
    PMID `23023293`: FUS/TLS binds thousands of RNAs in mouse and human brain;
    FUS and TDP-43 both affect long neuronal pre-mRNAs but also regulate many
    distinct RNAs.
  - Schwartz et al. 2014, Annual Review of Biochemistry, DOI
    `10.1146/annurev-biochem-060614-034325`, PMID `25494299`: FUS, EWSR1,
    and TAF15 are low-complexity FET proteins involved in transcription,
    RNA processing, and RNA fate.
  - Kapeli et al. 2016, Nature Communications, DOI `10.1038/ncomms12143`,
    PMID `27378374`: TAF15 and FUS have overlapping and distinct intronic
    binding and RNA-metabolism effects relative to TDP-43.

## Computation over the input parquet

I first read the focal training count CSV and used its 1,674 rows as the
eligible perturbation universe. The distribution was strongly zero-inflated:
1,205 of 1,674 training perturbations had `n_degs == 0`; only 63 were in the
10-99 medium band and 43 were at least 100.

For the detailed analog table, I filtered the DE parquet to the focal cell
group and to hand-selected RNA-processing or ALS/RBP comparators:

```python
import pyarrow.compute as pc
import pyarrow.dataset as ds

targets = [
    "Tardbp", "Hnrnpu", "Hnrnpa2b1", "Fmr1", "Snrnp70", "U2af2",
    "Rnpc3", "Thoc1", "Prpf6", "Cdc40", "Matr3", "Hnrnpc",
    "Atxn2", "Tia1", "Ddx3x", "Hnrnph2", "Snrpb", "Ddx39b",
]

filt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(targets)
)
tbl = ds.dataset(PARQUET).to_table(
    columns=[
        "gene_target", "names", "logfoldchanges", "scores",
        "pvals_adj", "n_pert_matched", "n_ctrl_matched",
    ],
    filter=filt,
)
```

I then recomputed `sum(pvals_adj < 0.05)` per target, split each count by
the sign of `logfoldchanges`, inspected the top FDR rows, and counted exact
FDR-gene overlaps among plausible analogs. The recomputed counts match the
CSV for all inspected perturbations.

## Same-experiment analogs for Fus

| training perturbation | focal `n_degs` | focal expression-pattern evidence | how it informed `Fus` |
|---|---:|---|---|
| `Tardbp` | 210 | 131 up, 79 down; top genes include `Ppp6c`, self `Tardbp` down, `Gabpa`, `Usp15`, `Uggt2`; measured `Fus` itself was down after `Tardbp` loss, logFC `-0.379`, FDR `9.46e-06`. | Best measured single-gene analog. FUS and TDP-43 are both ALS-linked nuclear RBPs with overlapping long-pre-mRNA biology, but Lagier-Tourenne et al. showed their RNA targets are only partly shared. The corpus also reported that `Tardbp` did not phenocopy most represented ALS/stress-granule relatives, so I did not simply transfer 210. |
| `Matr3` | 149 | 105 up, 44 down; very strong `Ddhd1`, `Atp9b`, `E2f4`, `Rsrp1` response; exact focal overlap with `Tardbp` was only 13 genes. | ALS-linked nuclear-matrix/RBP counterweight: it shows that a disease RBP can be a medium focal responder, but with a state distinct from `Tardbp`. |
| `Hnrnpc` | 122 | 77 up, 45 down; `Rbm25` and `Luc7l2` were down, `Txnl1` was the strongest up gene. | A spliceosome-adjacent hnRNP response in the same 100-200 DEG range. It supports nonzero nuclear-RBP sensitivity without forcing a core-spliceosome-sized prediction. |
| `Hnrnpa2b1` | 11 | Sparse focal response; top genes were `Rbm25`, `Hnrnpa1`, `Parp6`, `Snx29`, `Hnrnpu`, `Tcerg1`, `Drosha`. | Important counterexample. Another ALS/MSP RBP was visible only weakly, and the Distributed Agents corpus explicitly found no robust whole-transcriptome neighbor for it. |
| `Atxn2`, `Tia1`, `Fmr1` | 8, 0, 0 | Stress-granule/translation-linked perturbations were nearly flat in this focal group. `Fmr1` had no FDR genes despite 178 matched perturbed nuclei. | Related RNA-granule or neuronal RNA-transport annotations alone are insufficient to call a response. This argues against a strong prediction based only on ALS/RBP labels. |
| `Snrnp70`, `Prpf6`, `Cdc40`, `U2af2`, `Rnpc3`, `Thoc1` | 213, 454, 624, 828, 868, 303 | Core spliceosome and mRNA-export perturbations were broad in the focal group. `Snrnp70` altered 213 genes with recurrent RNA-processing changes such as `Luc7l2` down and `Srek1` up; `Rnpc3` and `U2af2` were much larger. | These set the high-RNA-processing ceiling. FUS participates in RNA metabolism but is not a U1, minor-spliceosome, U2AF, PRP17/CDC40, PRPF6, or TREX core component, so the 300-900 DEG range looked too high. |
| `Hnrnpu` | 733 | Broad response with `Dmtf1`, `Rsrp1`, `Depdc5`, matrix/secretory and proteostasis genes; the corpus found convergence with RNA-processing perturbations but divergence from measured hnRNP-family knockouts. | A clear upper-bound counterexample. `Hnrnpu` combines hnRNP, chromatin-scaffold, ISR/proteostasis, and ECM-like modules that should not be assigned to `Fus` just because both proteins bind RNA. |

The focal exact-overlap checks also argued for moderation. `Tardbp` shared
46 FDR genes with `U2af2`, 58 with `Rnpc3`, and 34 with each of `Prpf6` and
`Cdc40`, but shared only 13 with `Matr3`, 15 with `Hnrnpc`, 1 with
`Hnrnpa2b1`, and 0 with `Fmr1` or `Tia1`.

## Fus-specific decision

I predict a nonzero `Fus` response. The strongest target-specific reason is
not generic RNA binding; it is the combination of external FUS/TDP-43 evidence
and the measured `Tardbp` focal response:

- FUS and TARDBP are both ALS genes discovered as RNA-binding proteins whose
  disease mutations disrupt neuronal RNA processing and nuclear/cytoplasmic
  localization.
- FUS depletion from mouse nervous system changes hundreds of RNA abundance or
  splicing events, and FUS and TDP-43 converge on some long neuronal pre-mRNAs
  while remaining mostly distinct.
- In this exact focal cell group, `Tardbp` is a medium responder with 210
  FDR genes and significantly represses measured `Fus`, showing that the FUS
  transcript is part of a recoverable TDP-43-linked RNA-processing state.

I did not predict a very large count because the best same-experiment evidence
places FUS outside the most penetrant core-spliceosome/nuclear-pore class:
`Rnpc3`, `U2af2`, `Cdc40`, `Prpf6`, `Thoc1`, and `Hnrnpu` each
carry broader modules than expected for partial FUS loss. I also shrank below
`Tardbp`, `Matr3`, and `Hnrnpc` because FUS has FET-family redundancy through
EWSR1 and TAF15 and because the CRISPR perturbation is a wild-type acute LOF,
not cytoplasmic ALS-mutant FUS aggregation.

The zero boundary is guarded mainly by the weak related RBPs: `Hnrnpa2b1` had
11 focal DEGs, `Atxn2` had 8, `Ddx3x` had 8, `Hnrnph2` had 4, and `Tia1`,
`Fmr1`, `Snrpb`, and `Ddx39b` had 0. Those counterexamples mean the FUS call
is extrapolative. However, the direct FUS/TDP-43 long-pre-mRNA literature and
the nonzero `Tardbp`/`Matr3`/`Hnrnpc` counts make a true zero less likely than
a medium but buffered response.

I therefore placed `Fus` in the low-to-mid medium band, below the 122-210 DEG
range of `Hnrnpc`/`Matr3`/`Tardbp` but above the 0-11 DEG weak RBP group:

```text
Fus: predicted n_degs = 84
```

## Limits

- The exact FET paralogs `Ewsr1` and `Taf15` were not usable as training
  analogs, so the FET-redundancy shrinkage comes from external biology rather
  than a direct same-experiment paralog knockout.
- The assay is whole-gene 3-prime snRNA-seq. FUS loss may cause intron
  retention or isoform changes without changing total gene abundance, so the
  DEG count can understate primary RNA-processing defects.
- Recovered-nucleus power matters. Hidden `Fus` matched-cell counts could move
  the realized DEG count across the 0.05 FDR threshold even with the same
  underlying effect size.
- ALS mutations in FUS often combine nuclear loss with cytoplasmic gain or
  aggregation. The requested perturbation is sparse CRISPR LOF in juvenile
  wild-type neurons, so disease-mutant literature is only a mechanistic prior.
- Same-experiment RNA-processing targets span 0 to 868 focal DEGs. This large
  spread is precisely why the final count is extrapolated rather than copied
  from a single analog.
