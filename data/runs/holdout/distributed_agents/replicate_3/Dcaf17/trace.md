# DEG-count prediction trace

## Question and resolution of setup

The task is to predict, for each gene in the held-out manifest, the integer
`n_degs` that would have been observed in `151 TH Prkcd Grin2c Glut` after
acute P16 AAV-PHP.eB CRISPR-Cas9 loss of that gene.  `n_degs` is the number of
measured genes with Wilcoxon Benjamini-Hochberg adjusted `pvals_adj < 0.05` in
the focal cell group, including the target transcript if it was measured and
passes that threshold.

This manifest contains one target:

| target_name |
|---|
| Dcaf17 |

The held-out `Dcaf17` signature and endpoint count are absent from both supplied
training inputs, so I treated every `Dcaf17` conclusion as a prediction from
nearby assayed perturbations plus external function.  I interpreted `151 TH
Prkcd Grin2c Glut` as the thalamic glutamatergic population described by the
dataset context, not as tyrosine hydroxylase expression.  I also did not use
target-transcript depletion as a proxy for editing efficiency, because the
atlas documentation explicitly says self RNA loss is not quantitatively
coupled to downstream transcriptional breadth.

## Sources used

Same-experiment sources:

| source | use |
|---|---|
| `training_de_all_cell_groups.parquet` | Direct DE statistics for all non-held-out perturbations. I filtered this table to the focal group and inspected FDR-significant rows for biologically relevant comparators. |
| `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` | Exact training endpoint counts in the focal group. This was the calibration target for all analogs. |
| Distributed Agents same-experiment corpus release `perturbai-july-260713-sourceguard-1773-v1` | Curated same-atlas Findings and Claims for assayed neighbors such as `Dcaf8`, `Ddb2`, `Nop56`, `Wdr26`, `Ddx3x`, and `Copg1`. `Dcaf17` itself had no corpus finding, as expected for a held-out target. |
| Distributed Agents runtime profile-neighborhood tool | I compared several observed anchors in the same focal context to check for hidden FDR-level neighborhoods. Whole-vector similarities were not used quantitatively because low-expression, non-significant tails can dominate raw log-fold-change cosines; the significant-feature counts agreed with the endpoint table. |

External sources:

| source | use |
|---|---|
| NCBI PubMed E-utilities search | Literature on DCAF17/C2orf37, Woodhouse-Sakati syndrome, DCAF17 as a DDB1-CUL4-associated factor, and mouse Dcaf17 knockout biology. |
| Alazami et al. 2008, DOI `10.1016/j.ajhg.2008.10.018`, PMID `19026396` | Identified loss-of-function `C2orf37`/`DCAF17` mutations as the cause of Woodhouse-Sakati syndrome and described DCAF17 as a nucleolar protein of unknown function. |
| Ali RH et al. 2016, DOI `10.1111/cge.12700`, PMID `26612766` | Reported a biallelic DCAF17 deletion in Woodhouse-Sakati syndrome and interpreted the truncation as disrupting residues needed for DDB1 interaction. |
| Ali A et al. 2018, DOI `10.1038/s41598-018-27379-0`, PMID `29907856` | Generated Dcaf17-null mice, found strongest Dcaf17 expression in testis, and showed male infertility from abnormal spermatid development. |
| Kohil et al. 2023, DOI `10.1186/s13023-023-02614-8`, PMID `36721231` | Systematic review of Woodhouse-Sakati genetics and clinical heterogeneity caused by DCAF17 variants. |

## Computation over the supplied dataset

The endpoint CSV has 1,674 training perturbations.  The focal class is sparse:

| focal `n_degs` class | count |
|---|---:|
| 0 | 1205 |
| 1-9 | 363 |
| 10-99 | 63 |
| >=100 | 43 |

I then filtered the parquet with PyArrow to the focal cell group and a hand
picked comparator set:

```python
dataset.to_table(
    columns=["names", "gene_target", "logfoldchanges",
             "pvals_adj", "scores", "n_pert_matched", "n_ctrl_matched"],
    filter=(ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
           & ds.field("gene_target").isin(candidates),
)
```

For each comparator, I recounted rows with `pvals_adj < 0.05` and verified the
count against the training endpoint file.  `Dcaf17` itself is a measured gene in
the focal rows of training perturbations, so a self-transcript-only call would
be possible in principle; I did not force it because related DCAF perturbations
were often transcriptionally silent.

## Dcaf17-specific analogs and counterexamples

`Dcaf17` is a DDB1-CUL4-associated factor mutated in Woodhouse-Sakati syndrome.
External literature points to a nucleolar protein and a DDB1 interaction, but
does not define a neuronal substrate or a ribosome-biogenesis complex that
would map one-to-one onto an assayed perturbation.  Its mouse null phenotype is
most clearly spermiogenic rather than an acute brain transcriptome phenotype:
Ali A et al. found the highest expression in testis and infertility with
abnormal sperm development in Dcaf17-null males.

The most relevant focal training counts were:

| training target | focal `n_degs` | expression-pattern evidence in `151 TH Prkcd Grin2c Glut` | relevance to `Dcaf17` |
|---|---:|---|---|
| `Dcaf8` | 0 | No gene passed FDR 0.05 in the focal rows; the Distributed Agents corpus calls it a zero-downstream-gene perturbation in every recovered postmitotic neuronal group at FDR 0.10, with no meaningful whole-universe signature neighbor. | Closest direct CRL4/DCAF substrate-receptor analog in the training table. Its complete null is strong evidence that an acute DCAF loss does not automatically create a visible thalamic signature. |
| `Ddb2` | 0 | No focal FDR 0.05 genes; the same-experiment corpus reports a pan-neuronal basal transcriptomic null despite recovery of the Ddb2 transcript itself. | DDB2 is a DDB1-CUL4 receptor for nucleotide-excision repair. It is not a DCAF17 substrate receptor, but it is a direct DDB1-CUL4 family boundary. |
| `Crbn` | 0 | The focal endpoint count was zero. Corpus findings around `Crbn` use `Ddb2` and `Dcaf8` as DCAF/CRL4 comparators and report nonconvergence of these receptors. | A second DDB1-CUL4 substrate-receptor family member; flatness supports family-specific rather than generic DCAF output. |
| `Dnmt3a` | 0 | Zero focal DEGs and reported by the `Dcaf8` corpus as flat in a CRL4/chromatin comparison where `Setdb1` was active. | A chromatin counterexample: not DCAF, but checked because Dcaf8 has reported CRL4DCAF8/H3K9 connections outside neurons. |
| `Setdb1` | 22 | A narrow protocadherin/Atf7ip/Tasor response that did not match `Dcaf8`. | Positive control that chromatin-linked targets can produce a focal signal, but the module is Setdb1-specific and not a good `Dcaf17` prior. |
| `Nop56` | 25 | The focal signature included decreases of RNA-processing/splicing transcripts such as `Rsrp1`, `Ddx17`, `Srsf5`, `Srsf11`, `Ddx5`, `Srsf6`, `Pabpn1`, and `Clk4`; it did not activate canonical nucleolar-stress, p53/apoptosis, ISR, or autophagy programs. | Best positive counterexample for a nucleolar/RNA-processing perturbation. It argues that such biology is detectable in 151 TH, but its box C/D snoRNP role is much more specific than DCAF17's known function. |
| `Rbm28`, `Las1l`, `Taf1b` | 0, 0, 0 | Focal endpoint counts were zero; the corpus uses `Rbm28`/`Las1l`/`Nop56` and `Taf1b`/`Nop56` contrasts to show that rRNA/ribosome-production factors are not interchangeable in the atlas. | These are important boundaries on the nucleolar prior: even literature-obvious rRNA-processing genes are often buffered. |
| `Polr3b` | 8 | A small focal endpoint. | Shows that RNA-production perturbations can be nonzero but weak; not a direct DCAF17 analog. |
| `Ddx3x` | 8 | Compact 151 TH response: `Ddx3x`, `Grin2b`, `Synpo2`, `Plekhg1`, `Tcea2`, and `Ccdc136` decreased while `Ypel3` and `Tmsb10` increased. The corpus reports no FDR-supported ISR/UPR, heat-shock, stress-granule, or broad eIF4F-wide program. | RNA-helicase/neurodevelopmental counterexample. The small count is a ceiling only if DCAF17 behaves as an RNA-regulatory NDD gene, which is not established. |
| `Ddx39b` | 0 | No focal FDR 0.05 genes; the corpus reports that represented DEAD-box and eIF4F comparators do not phenocopy `Ddx3x`. | Boundary against transferring all RNA-related disease-gene activity to DCAF17. |
| `Wdr26` | 13 | Focal significant rows included `Grin2b`, `Cyc1`, `Hnrnpu`, `Peg3`, `Kcna2`, `Abca7`, `Gabra4`, and `R3hdm2` decreases plus a few induced markers. Corpus summaries tie Wdr26 loss to RNA-processing/nuclear-transport, synaptic, mitochondrial, and CTLH/proteostasis modules. | A WD-repeat ubiquitin-adaptor counterexample that clearly responds in selected neurons, but WDR26 is a CTLH substrate adaptor, not a CRL4-DCAF17 receptor. |
| `Fbxw7` | 1 | One focal FDR 0.05 gene. | A generic E3-substrate-receptor boundary; ubiquitin-ligase adaptor status alone is insufficient for a broad response. |

## Prediction

The same-experiment evidence favors a zero for `Dcaf17`.  The two most direct
DDB1-CUL4 comparators available in the training table, `Dcaf8` and `Ddb2`, both
had zero focal DEGs, and `Dcaf8` was silent across the broader recovered
neuronal taxonomy in the same-experiment corpus.  The one CRL4-adjacent positive
training signal in this reasoning set was indirect `Setdb1`, but that module was
explicitly absent from `Dcaf8`/`Ddb2`/`Dnmt3a` comparisons and has no known
DCAF17-specific rationale.

The nucleolar clue from Woodhouse-Sakati literature pushes the call away from a
purely gene-family null, but only weakly.  `Nop56` proves that 151 TH can report
a small nucleolar/RNA-processing state, yet nearby ribosome-biogenesis
perturbations such as `Rbm28`, `Las1l`, and `Taf1b` were flat.  DCAF17 is not a
known box C/D snoRNP core factor, polymerase component, or SR-splicing regulator.
Human WSS and mouse spermatogenesis show DCAF17 is biologically real, but they
come from chronic developmental, endocrine, reproductive, or germline contexts,
not sparse postmitotic thalamic neurons 3-4 weeks after partial CRISPR loss.

Because the closest matched perturbations are zero and the mechanistic
alternatives are either weak or nonmatching, I predict no focal FDR 0.05 calls:

| target | predicted `n_degs` |
|---|---:|
| Dcaf17 | 0 |

## Limits

`Dcaf17` had no held-out expression profile or corpus finding, so this is
extrapolation.  Core CRL4 components such as `Ddb1`, `Cul4a`, and `Cul4b` were
not present as focal training-count analogs, and the actual DCAF17 substrates in
neurons remain unknown.  Nucleolar localization may reflect a genuine RNA or
ribosome-associated function that is closer to `Nop56` than current literature
allows me to see.  The assay is survivor-conditioned and measures nuclear RNA,
so a protein-level, nucleolar, chronic neurodegenerative, or endocrine
phenotype could be missed even if DCAF17 is essential in another setting.
