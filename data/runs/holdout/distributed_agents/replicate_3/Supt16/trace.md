# Prediction task

I interpreted the task as a scalar held-out readout prediction for the requested
perturbation in `151 TH Prkcd Grin2c Glut` neurons:

- target to predict: `Supt16`
- endpoint: the number of measured genes with `pvals_adj < 0.05` in this focal
  cell group
- assay: the acute, sparse P16-to-P37/P44 AAV-CRISPR neuronal Perturb-seq
  experiment, not a germline knockout, a synchronized cell-line FACT depletion,
  or a pharmacologic curaxin exposure

The only requested-target ambiguity was the mouse/human name: the manifest uses
mouse `Supt16`, the ortholog of human `SUPT16H` and S. cerevisiae `SPT16/CDC68`.
I kept the manifest spelling in the final table.

# Sources used

- `[local file: 228_Supt16.csv]`
  showed that this run requests only `Supt16`.
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  provided the observed focal-cell DEG counts for 1,674 non-held-out training
  perturbations.
- `[local file: training_de_all_cell_groups.parquet]`
  provided the actual signed Wilcoxon profiles. I queried the exact
  `151 TH Prkcd Grin2c Glut` rows for pathway-adjacent training perturbations.
- Same-experiment semantic layer: Distributed Agents corpus
  `perturbai-july-260713-sourceguard-1773-v1`. The corpus had no `Supt16`
  page, which was expected because `Supt16` is held out, but it did have
  annotated reports for `Brd4`, `Wac`, `Setd2`, `Chd8`, `Smarca4`, and `Cdk13`.
- Distributed Agents run-local profile comparison over the focal parquet profiles,
  written to `profile_compare_supt16_analogs.json`, to check whether the chosen
  chromatin/transcriptional anchors were genuinely similar in the raw Wilcoxon
  signature space.
- PubMed literature for FACT biology:
  Orphanides et al. 1999, DOI `10.1038/22350`, PMID `10421373`;
  Belotserkovskaya et al. 2003, DOI `10.1126/science.1085703`, PMID `12934006`;
  Winkler et al. 2011, DOI `10.1074/jbc.M111.301465`, PMID `21969370`;
  Zhou et al. 2022, DOI `10.1093/nar/gkac645`, PMID `35904816`.

# Computation over the training data

First I read the target manifest and the focal training-count CSV. The count
distribution is very sparse:

- 1,205 / 1,674 training perturbations had 0 DEGs.
- 363 had 1-9 DEGs.
- 63 had 10-89 DEGs.
- 43 had at least 100 DEGs.
- The median was 0, the 75th percentile was 1, the 95th percentile was 18, and
  the maximum was `Uba5` with 2,677.

This made the prediction a two-step problem: decide whether acute `Supt16` loss
should clear the focal FDR gate at all, then decide how far into the heavy tail
to put it.

I also scanned the training count table for direct FACT and transcription-coupled
chromatin comparators. The crucial absence is that the exact FACT partner and
canonical histone-chaperone comparators were not training targets in this focal
count table:

- absent: `Ssrp1`, `Chaf1a`, `Chaf1b`, `Hira`, `Ubn1`, `Ubn2`, `Nasp`,
  `Asf1a`, `Asf1b`, `Hjurp`
- absent: core PAF1 members `Paf1`, `Cdc73`, `Ctr9`, `Leo1`, `Rtf1`, `Wdr61`
- present FACT/pathway-adjacent anchors and their observed focal counts:
  `Brd4` 311, `Wac` 384, `Setd2` 1, `Thoc1` 303, `Cdk13` 56

For the focal signed profiles, I read only the selected `gene_target` rows from
the parquet with an exact `group_name` filter:

```python
ds.dataset(parquet).to_table(
    columns=["names", "gene_target", "logfoldchanges", "pvals_adj", "scores",
             "n_pert_matched", "n_ctrl_matched"],
    filter=(pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
           & pc.field("gene_target").isin(anchor_targets),
)
```

The queried raw signatures confirmed the focal counts in the CSV and showed
their directionality. `Brd4` had 311 DEGs, biased down in its FDR genes
including `Omg`, `Plch2`, `Rnf112`, `Irag1`, and `Lgi3`. `Wac` had 384 DEGs
with a mixed but down-biased neuronal-maintenance arm led by `Lgi3`, `Eno2`,
`Grid2ip`, `Rnf112`, `Ptpn3`, and `Septin5`. `Setd2` had exactly one DEG:
`Septin5` up. `Chd8`, `Cdk13`, `Smarcc2`, and `Arid2` occupied an intermediate
range of 56-185 DEGs, whereas `Smarca4`, `Chd7`, `Cdk8`, `Ep300`, `Kat6a`,
`Kat6b`, `Smarcc1`, and `Smarcad1` had no focal DEGs.

The run-local profile comparison gave two useful checks:

- `Brd4` and `Wac` were the most FACT-relevant high-count pair. Their full
  focal profiles were only modestly similar, Pearson `0.102`, but they shared
  46 same-direction significant negative genes, such as `Rnf112`, `Lgi3`,
  `Plch2`, `Mt3`, `Coro6`, `Omg`, `Ache`, and `Slc6a7`.
- `Setd2` did not align with `Brd4` or `Wac`; `Brd4`-`Setd2` Pearson was only
  `0.020`, and there was no same-direction FDR-level overlap. So
  transcription-coupled histone-mark biology alone was not enough to predict a
  broad response in this assay.

# Target-specific reasoning

## `Supt16`

### External mechanism

`Supt16` encodes the large subunit of FACT. Human FACT was biochemically defined
as a heterodimer of SPT16/SUPT16H and SSRP1 that binds nucleosomes and
H2A-H2B dimers to facilitate Pol II elongation through chromatin
(Orphanides et al. 1999, DOI `10.1038/22350`, PMID `10421373`). FACT can
destabilize a nucleosome enough to remove one H2A-H2B dimer during Pol II
passage and can redeposit histones on DNA; both SPT16 and SSRP1 are required
for that activity in vitro (Belotserkovskaya et al. 2003,
DOI `10.1126/science.1085703`, PMID `12934006`). Biophysical work further
supports FACT as a histone/DNA/nucleosome-binding chaperone whose SPT16 acidic
C-terminal domain helps reorganize nucleosomes (Winkler et al. 2011,
DOI `10.1074/jbc.M111.301465`, PMID `21969370`).

Those facts made a zero hard to justify: `Supt16` is not a peripheral tissue
marker or a glial gene displaced from the assayed NeuN-positive population. It
is a core chromatin-transcription factor, and the focal class is the highest
yield class in this dataset. On the other hand, FACT is also used during DNA
replication and repair. This screen harvested postmitotic neurons 3-4 weeks
after sparse P16 editing, so cell-cycle FACT biology and acute cancer-cell death
programs are imperfect priors for the surviving nuclei. Zhou et al. 2022
reported a SUPT16H-BRD4 relationship in epithelial/NK antiviral signaling
(DOI `10.1093/nar/gkac645`, PMID `35904816`), supporting proximity to a `Brd4`
axis but in a non-neuronal and interferon-heavy context.

### Within-dataset analogs

`Brd4`, 311 DEGs, was the closest measured chromatin-coupled Pol II elongation
anchor with a corpus-supported focal response. The Distributed Agents corpus reports
that `Brd4` loss in this experiment was concentrated in `151 TH Prkcd Grin2c
Glut`, `155 MB Glut`, and `191 MB P MY GABA`, with a dominant decrease of
neuronal process, adhesion, channel, and synaptic genes. It also notes that
`Brd4` did not phenocopy generic bromodomain, Mediator, or MYC-axis
perturbations. This supports the idea that a basal elongation reader can produce
hundreds of focal DEGs, but it also argues against simply copying 311 onto every
nearby chromatin factor.

`Wac`, 384 DEGs, was another high-count analog because WAC connects H2B
monoubiquitination with transcription/chromatin output. In the same-experiment
corpus, `Wac` is strongest in the same `151`, `155`, and `052 Pvalb` groups,
down-regulates mature neuronal and synaptic marker transcripts, and shares a
non-obvious proteostasis/chromatin neighborhood with `Psmc1`, `Psmb4`, and
`Sin3a`. The raw profile comparison showed real overlap with `Brd4` on a
negative neuronal arm. I used `Wac` as evidence that weakening chromatin-coupled
transcription can be visible in `151` neurons, not as a direct FACT-complex
surrogate.

`Setd2`, 1 DEG, was the strongest counterexample. SETD2 is tied to
transcription-coupled chromatin through H3K36 methylation, but the corpus
records that canonical SETD2 programs were buffered from broad whole-gene
transcriptional remodeling after P16 neuronal knockout; in the focal group only
`Septin5` passed FDR. `Setd2` also opposed `Wac` at the single `Septin5`
coordinate. This pulled the `Supt16` estimate well below the broad `Brd4` and
`Wac` counts.

`Cdk13`, 56 DEGs, was a co-transcriptional RNA-processing/Pol II analog. Its
corpus report describes a real but regionalized response and convergence with
`Wac` and `Snrnp70`, not a pan-neuronal collapse. I treated it as a better scale
for a non-obligate elongation perturbation in surviving postmitotic neurons than
the much broader stress-like `Sin3a` 1,433 and `Yy1` 720 profiles.

The chromatin-remodeler comparators set the boundaries. `Smarcc2` had 185,
`Chd8` had 61, `Arid2` had 56, `Kmt2a` had 24, `Smarce1` had 11, while
`Smarca4`, `Smarcc1`, `Chd7`, `Cdk8`, and `Ep300` were zero in the focal group.
The same-experiment reports for `Chd8` and `Smarca4` explicitly warn that
same-family chromatin genes are not interchangeable in this P16 neuronal assay.

### Final call

I predict that `Supt16` will be nonzero but closer to `Kmt2a`/Mediator-sized
responses than to the 300-400 DEG `Brd4`/`Wac` responses. The exact FACT partner
`Ssrp1` was unavailable as a training anchor; direct histone-chaperone
comparators such as CAF-1, HIRA, NASP, ASF1, and PAF1-complex members were also
unavailable. Because the positive evidence is pathway-adjacent and the strongest
counterexample, `Setd2`, was essentially flat, I placed the point prediction at
the top of the low-to-medium chromatin-regulator group:

`Supt16 -> 24 DEGs`.

# Limits

- No `Ssrp1` or exact FACT-complex perturbation was present in the supplied
  training endpoint, and the Distributed Agents corpus had no held-out `Supt16` finding.
  The prediction is therefore extrapolation from adjacent chromatin and
  elongation perturbations.
- The external FACT literature is dominated by in-vitro biochemistry,
  proliferating cells, DNA-replication/repair contexts, cancer cell lines, or
  immune/epithelial signaling. Those mechanisms need not appear as a stable
  whole-gene snRNA-seq abundance signature in sparse, postmitotic juvenile
  mouse neurons.
- Single-gene CRISPR in this assay is mild and survivor-conditioned. FACT loss
  that was too damaging could reduce recovery without leaving many DEGs among
  surviving nuclei; a null or weak RNA signature would not prove failed editing.
- The exact count is assay-power dependent. `Supt16` could land anywhere from a
  Setd2-like one-gene response to a Brd4/Wac-like multi-hundred response if FACT
  engages the same neuronal-maintenance program. My integer is the calibrated
  middle of those imperfect analogs, not a mechanistic constant.
