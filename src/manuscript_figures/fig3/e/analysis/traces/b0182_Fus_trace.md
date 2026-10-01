# DEG-count prediction trace

## Question

I interpreted the task as a scalar prediction: for each held-out perturbation,
predict the number of measured genes in `151 TH Prkcd Grin2c Glut` with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05`. The DEG count is an
assay-specific breadth endpoint from surviving, recovered 10x Flex nuclei after
P16 mosaic AAV-CRISPR loss of function. It is not a direct viability, protein,
editing-efficiency, or biological-importance measurement, so I did not use
target mRNA fold change as a filter for effective editing.

The requested-target manifest had one target:

```tsv
target_name
Fus
```

`Fus` is held out from both the differential-expression Parquet and the
training count CSV, so its own signature and true count are absent from the
declared inputs.

## Sources

- Declared dataset:
  `/gpfs/group/jin/asun/bioagents/debug/260901_predict/holdout_task/Inputs/training_de_all_cell_groups.parquet`.
  I queried rows from the focal cell group for `Fus`-adjacent training
  perturbations.
- Declared training endpoint:
  `/gpfs/group/jin/asun/bioagents/debug/260901_predict/holdout_task/Inputs/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This provided exact observed `n_degs` for non-held-out perturbations.
- Run-local manifest:
  `/gpfs/group/jin/asun/bioagents/runs/holdout-prediction/july-260713-adaptive-seed-260901/prepared/manifests/deg-count/bs001/b0182.csv`.
- Same-experiment semantic corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, queried through the declared
  `corpus.findings` and `corpus.report_evidence` capabilities. I used it only
  for interpretation of visible training perturbations; it had no `Fus` report.
- External literature and PubMed:
  - Kwiatkowski et al. 2009, Science, PubMed 19251627,
    DOI 10.1126/science.1166066.
  - Vance et al. 2009, Science, PubMed 19251628,
    DOI 10.1126/science.1165942.
  - Rogelj et al. 2012, Scientific Reports, PubMed 22934129,
    DOI 10.1038/srep00603.
  - Schwartz et al. 2014, Annual Review of Biochemistry, PubMed 25494299,
    DOI 10.1146/annurev-biochem-060614-034325.
  - Purice and Taylor 2018, Frontiers in Neuroscience, PubMed 29867335.
  - Geuens et al. 2016, Human Genetics,
    DOI 10.1007/s00439-016-1683-5.

## Quantitative calibration

The training endpoint table contained 1,674 non-held-out perturbations in
`151 TH Prkcd Grin2c Glut`: 469 had nonzero `n_degs` and 1,205 were zero. The
distribution was therefore zero-inflated and highly skewed. The largest
training responses were broad RNA-processing or proteostasis perturbations:

```tsv
target_name	n_degs
Uba5	2677
Tpr	1768
Sin3a	1433
Rnpc3	868
U2af2	828
Psmb4	742
Hnrnpu	733
Cdc40	624
Tnpo3	618
Prpf6	454
Psmc1	430
Snrnp70	213
Tardbp	210
Matr3	149
Hnrnpc	122
```

For the focal cell group I extracted the complete 17,259 measured-gene rows for
16 FUS-relevant training targets: `Tardbp`, `Matr3`, `Hnrnpu`, `Hnrnpc`,
`Hnrnpa2b1`, `Ddx3x`, `Hnrnph2`, `Hnrnpdl`, `Tia1`, `Rnpc3`, `U2af2`, `Cdc40`,
`Prpf6`, `Snrnp70`, `Psmc1`, and `Psmb4`. Their focal-cell FDR<0.05 counts
matched the training CSV:

```tsv
target_name	n_degs
Rnpc3	868
U2af2	828
Psmb4	742
Hnrnpu	733
Cdc40	624
Prpf6	454
Psmc1	430
Snrnp70	213
Tardbp	210
Matr3	149
Hnrnpc	122
Hnrnpa2b1	11
Ddx3x	8
Hnrnph2	4
Hnrnpdl	1
Tia1	0
```

The focal-cell overlaps among `Tardbp`, `Matr3`, `Hnrnpu`, and `Hnrnpc` were
modest but real. At FDR<0.05, `Tardbp` shared 13 significant measured genes
with `Matr3`, 45 with `Hnrnpu`, and 15 with `Hnrnpc`; `Matr3` shared 36 with
`Hnrnpu` and 6 with `Hnrnpc`; `Hnrnpu` shared 33 with `Hnrnpc`. Recurrent genes
included the RNA-processing factors `Rsrp1`, `Srsf11`, and `Dusp11`, the
secretory/proteostasis marker `Uggt2` in `Tardbp` and `Matr3`, and the focal
marker `Grin2c` down in `Tardbp`, `Matr3`, and `Hnrnpu`.

The counterexample set was important. Measured ALS or RBP perturbations that
are plausible by annotation alone were essentially flat in this readout:
`Hnrnpa2b1` 11, `Atxn2` 8, `Ddx3x` 8, `Hnrnph2` 4, `Vcp` 2, `Hnrnpdl` 1,
`Sqstm1` 1, `Stmn2` 1, `Grn` 1, `Kif5a` 1, `Sort1` 0, and `Tia1` 0. The
same-experiment corpus independently reported the same limitation: `Matr3`
partially converged with `Tardbp` through `Uggt2`, but `Hnrnpa2b1`, `Atxn2`,
`Tia1`, `Vcp`, `Sqstm1`, and `Kif5a` did not phenocopy the `Matr3` program;
`Tardbp` likewise overlapped much more with `Psmc1`, `U2af2`, and `Prpf6` than
with the obvious ALS-family comparators.

## Target-specific reasoning

### Fus

**Relevant visible analogs.** `Fus` encodes an ALS-linked FET-family nuclear
DNA/RNA-binding protein. FET proteins, including FUS, EWSR1, and TAF15, bind
RNA and contribute to transcription, RNA processing, cytoplasmic mRNA fate, and
DNA-damage responses (Schwartz et al. 2014). FUS mutations were discovered as
familial ALS causes in 2009; the mutant proteins mislocalize into cytoplasmic
neuronal inclusions, supporting overlap with RNA-binding ALS proteins while
not proving identical loss-of-function consequences (Kwiatkowski et al. 2009;
Vance et al. 2009).

The closest training perturbation is `Tardbp`, because TDP-43 is another
ALS/FTD nuclear RBP. In the focal cell group, `Tardbp` caused 210 DEGs. Its
visible report called a broad but uneven RNA-processing plus ER/lysosomal
compensation response, and the raw Parquet showed that `Fus` itself was one of
the `Tardbp` downstream genes in the focal cell group
(`logfoldchanges = -0.379`, `pvals_adj = 9.46e-06`). That makes `Tardbp` loss a
same-direction prior for losing at least part of FUS-linked nuclear RNP
function.

`Matr3` is the second strong analog. It caused 149 focal-cell DEGs and the
same-experiment corpus interpreted it as an RNA-processing perturbation with
secondary `Uggt2`/membrane/metabolic responses. MATR3 is not a FET protein, but
it is an ALS-associated nuclear RNA-binding scaffold; in this dataset it was
one of the only measured ALS-family perturbations with a genuine focal-cell
response. `Hnrnpc` is a weaker hnRNP analog with 122 DEGs and a gene-level
splicing/export/3-prime-end compensation program. `Hnrnpu` is mechanistically
less specific but proves that a neuronal hnRNP perturbation can be very broad
in this exact cell group: it caused 733 DEGs, induced `Taf15`, `Tardbp`,
`Srsf11`, `Hnrnpa2b1`, `Eif4a3`, and `Rnpc3`, and converged with spliceosome
targets.

The core-spliceosome perturbations `U2af2` 828, `Rnpc3` 868, `Cdc40` 624, and
`Prpf6` 454 set an upper scale. FUS controls nascent pre-mRNA processing but is
not itself an obligate spliceosome component, so I treated these as
high-breadth ceiling analogs rather than direct count estimates.

**Expression-pattern evidence.** In the same focal-cell rows, `Tardbp`,
`Matr3`, `Hnrnpu`, and `Hnrnpc` repeatedly changed RNP/stress genes but did not
collapse to one identical pattern: for example `Rsrp1` was FDR-significant in
all four, with opposite signs in `Tardbp` versus `Matr3`/`Hnrnpu`/`Hnrnpc`;
`Srsf11` was significant in all four; `Uggt2` was significant in `Tardbp` and
`Matr3`; and `Tardbp` loss itself decreased `Fus`. This fits an estimate near
the `Tardbp`/`Matr3`/`Hnrnpc` tier rather than the broader `Hnrnpu` or
spliceosome tier.

**Counterexamples.** Disease-family or RBP identity alone is not enough in this
dataset. `Hnrnpa2b1` had only 11 DEGs and `Tia1` had zero in the focal cell
group; `Atxn2`, `Vcp`, `Sqstm1`, `Stmn2`, `Sort1`, `Grn`, and `Kif5a` were
also near zero in the training endpoint. Those counterexamples keep the
prediction below a generic ALS/RBP average and argue against assigning FUS a
core-spliceosome-like count.

**External prior and endpoint transfer.** Rogelj et al. used iCLIP in mouse
brain and found that FUS binds along nascent RNAs and regulates alternative
splicing in `Fus-/-` brain, with targets enriched for neuronal-development
functions. They also reported that FUS and TDP-43 do not significantly overlap
in their RNA binding sites or regulated exons. I therefore transfer only the
intervention stage "loss of a nuclear RNA-processing RBP creates a postmitotic
RNP stress response" from `Tardbp` and `Matr3`; I do not assume that FUS will
copy the full TDP-43 or Matrin3 downstream gene set. That causal chain is:
P16 sparse CRISPR loss of FUS -> partial loss of a nuclear nascent-RNA binding
factor -> mis-splicing/RNP homeostasis stress and secondary compensation in
vulnerable thalamic glutamatergic nuclei -> moderate whole-gene abundance
changes among recovered P37-P44 nuclei -> an intermediate DEG count.

I therefore predict a nonzero intermediate focal-cell response for `Fus`,
closest to the `Tardbp` 210 / `Matr3` 149 / `Hnrnpc` 122 tier and below the
core spliceosome and `Hnrnpu` tier:

```tsv
target_name	predicted_n_degs
Fus	180
```

## Limits

- The requested endpoint is directly observed for training perturbations but
  absent for `Fus`; the prediction is a mechanistic transfer from nearby
  perturbations, not a direct measurement.
- The best FET-family analogs, `Ewsr1` and `Taf15`, were not perturbation
  targets in the supplied training counts, so the inference has to use the more
  distant `Tardbp`, `Matr3`, `Hnrnpc`, and `Hnrnpu` RNA-binding perturbations.
- Whole-gene 10x snRNA-seq is a poor direct reporter of the cryptic exons,
  alternative splice junctions, RNA localization defects, and protein
  aggregation phenotypes central to FUS/TDP-43 biology.
- Superficial ALS relatedness is not endpoint-bearing: `Hnrnpa2b1`, `Tia1`,
  `Atxn2`, `Vcp`, `Sqstm1`, `Stmn2`, `Sort1`, `Grn`, and `Kif5a` were all
  weak or null in this cell group. `Fus` is predicted to be nonzero because it
  is a direct nuclear RNA-processing factor and a Tardbp-downstream transcript,
  not merely because it is an ALS gene.
- The exact integer count is the weakest part of the answer. The zero/nonzero
  call is more secure than distinguishing roughly 120, 180, and 220 DEGs.
