# Rrn3 DEG-count prediction

## Question and interpretation

The requested manifest `[local file: 200_Rrn3.csv]` contains exactly one held-out target:

```text
Rrn3
```

I interpreted the task as a point prediction of `n_degs` for `Rrn3` knockout in the single focal cell group `151 TH Prkcd Grin2c Glut`, where `n_degs` means the number of measured nuclear mRNAs with `pvals_adj < 0.05` in the same Scanpy/Wilcoxon differential-expression pipeline used for the held-in training targets. `Rrn3` was absent from both the supplied DE parquet and the supplied focal-cell count table, so no expression row or count for `Rrn3` was used directly.

Two ambiguities were resolved conservatively:

- I treated the endpoint as the assay-specific count of polyadenylated snRNA-seq DEGs in surviving nuclei, not as a direct measurement of rRNA transcription, edited-cell fitness, or complete loss-of-function severity.
- I used zero to mean that no measured mRNA is expected to pass BH FDR 0.05. A small subthreshold biological response is therefore still compatible with a zero prediction.

## Sources

- Supplied focal endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Supplied DE table: `[local file: training_de_all_cell_groups.parquet]`.
- Held-out target manifest: `200_Rrn3.csv`.
- Distributed Agents same-experiment corpus release `perturbai-july-260713-sourceguard-1773-v1`. This release had no direct `Rrn3` finding, so I used it to inspect training perturbations around `Taf1b`, `Nop56`, `Rbm28`, `Polr3b`, `Myc`, and `Mycn`.
- Run-local observed-profile tools over the parquet, using `gene_target` as the profiled entity, `names` as features, and either Wilcoxon `scores` or `logfoldchanges` in the focal cell group.
- NCBI PubMed for external RRN3/TIF-IA and nucleolar-stress biology.

Key public literature used:

- Yamamoto et al. 1996, PMID: 8670901: yeast `RRN3` encodes an essential Pol I transcription factor that interacts with Pol I and promotes pre-initiation complex formation.
- Cavanaugh et al. 2002, DOI: 10.1074/jbc.M201232200, PMID: 12015311: mammalian Rrn3/TIF-IA phosphorylation controls formation of the Rrn3-Pol I complex and functions as a ribosome-biogenesis checkpoint.
- Hirschler-Laszkiewicz et al. 2003, DOI: 10.1074/jbc.M301093200, PMID: 12646563: human/mammalian Rrn3 is an essential rDNA transcription factor and is limiting and stoichiometrically inactivated during rDNA transcription.
- Stepanchick et al. 2013, DOI: 10.1074/jbc.M112.444265, PMID: 23393135: DNA binding by human Rrn3 is required for Pol I transcription.
- Engel et al. 2016, DOI: 10.1038/ncomms12129, PMID: 27418309: cryo-EM structure showing Rrn3 bound to Pol I and converting Pol I toward an initiation-competent monomeric complex.
- Mayer and Grummt 2005, DOI: 10.4161/cc.4.8.1925, PMID: 16205120: review of the nucleolus as a stress sensor and TIF-IA as a target through which stress down-regulates Pol I/rDNA transcription.
- Parlato et al. 2008, DOI: 10.1523/JNEUROSCI.2439-08.2008, PMID: 19036968: conditional TIF-IA ablation in the mouse nervous system impairs nucleolar activity, increases p53, and causes rapid apoptosis in neural progenitors but protracted degeneration in adult hippocampal neurons.
- Kreiner et al. 2013, DOI: 10.1038/cdd.2013.66, PMID: 23764776: conditional TIF-IA loss in medium spiny neurons triggers nucleolar stress with a p53/PTEN-dependent adaptive phase before degeneration.

## Supplied-data computations

The focal training table has 1,674 non-held-out targets. Its count distribution is highly zero-inflated:

| quantity | value |
|---|---:|
| zero-count targets | 1,205 / 1,674 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

This distribution means that a mechanistically important gene needs target-matched evidence before assigning any positive count. Most held-in perturbations are flat in this specific postnatal neuronal endpoint.

For focal rows from the huge parquet, I pushed both filters into the parquet reader rather than materializing the full 616M-row table:

```python
import pyarrow.parquet as pq

df = pq.read_table(
    "[local file: training_de_all_cell_groups.parquet]",
    columns=[
        "names", "gene_target", "logfoldchanges", "scores",
        "pvals_adj", "n_pert_matched", "n_ctrl_matched",
    ],
    filters=[
        ("group_name", "=", "151 TH Prkcd Grin2c Glut"),
        ("gene_target", "in", targets),
    ],
).to_pandas()
```

I used the count CSV for exact `n_degs`, then inspected leading FDR-ranked genes for Pol I, Pol III, ribosome-biogenesis, MYC, p53, and nucleolar/RNA-stress candidate comparators present in training.

## Rrn3-specific reasoning

`Rrn3` encodes TIF-IA, the Pol I initiation factor that bridges Pol I to the rDNA initiation machinery. Complete TIF-IA loss is therefore upstream of ribosomal RNA synthesis and nucleolar integrity, and severe conditional loss can activate p53 and kill neurons over time. The held-out experiment, however, perturbs juvenile postmitotic neurons mosaicly and measures nuclear polyadenylated mRNAs in recovered cells 3-4 weeks later. The direct question is not whether Rrn3 matters for rRNA transcription; it is whether the surviving `151 TH Prkcd Grin2c Glut` nuclei would show any BH-significant mRNA DEGs.

### Direct Pol I comparator: Taf1b

The closest represented training perturbation was `Taf1b`, a Selectivity Factor 1 / SL1 component required for Pol I promoter recognition. In the focal cell group:

| target | role relative to Rrn3 | n_pert | n_degs | leading focal evidence |
|---|---|---:|---:|---|
| `Taf1b` | same Pol I/rDNA initiation apparatus, upstream basal factor | 106 | 0 | top five genes all had `pvals_adj = 1.0`; the leading row was `Chga`, log2FC 0.408 |

The Distributed Agents corpus had a `Taf1b` negative-result finding: a de novo signature-neighbor search found no meaningful `Taf1b` co-signature or anti-signature, and literature-obvious MYC/rDNA comparisons were mostly flat. The same corpus also noted that `Nop56` and `Polr3b` could produce DE in related thalamic/midbrain groups, so the `Taf1b` zero is not simply because all RNA-production perturbations were invisible.

I therefore treated `Taf1b` as the highest-weight comparator. It is not a perfect substitute for Rrn3: SL1 and Rrn3 contact different components of the initiation complex, and Rrn3 is regulated by phosphorylation and Pol I association. But both are basal Pol I initiation factors, and a zero for `Taf1b` in the exact focal cell group argues that partial CRISPR disruption of the rDNA initiation apparatus often does not cross the mRNA-FDR threshold here.

### Nucleolar and ribosome-biogenesis comparators

The training set contained several downstream ribosome-biogenesis or nucleolar factors but not the closest same-complex genes one would ideally want, such as `Polr1a`, `Polr1b`, `Ubtf`, or `Tbp`.

| target | focal `n_degs` | focal expression evidence | interpretation for Rrn3 |
|---|---:|---|---|
| `Rbm28` | 0 | `min(pvals_adj) = 0.543`, 143 matched perturbed nuclei | A literature-obvious 60S/rRNA-processing gene can be fully flat in the same focal readout. This supports a zero or near-zero Rrn3 call. |
| `Las1l` | 0 | `min(pvals_adj) = 1.0`, 171 perturbed nuclei | Another large-subunit rRNA maturation factor is flat; again supports that nucleolar biology is not generically converted into a DEG burst. |
| `Nop56` | 25 | 15 down and 10 up DEGs; leading genes included `Rsrp1` down, `Ddx17` down, `Srsf5` down, `Tcea2` down, and `Chn1` up | Shows the assay can detect a modest nucleolar/RNA-processing response. It is downstream of rRNA modification and snoRNP biology rather than direct Pol I initiation, so I used it as an upper counterexample rather than the main analog. |

The corpus summary around `Nop56` is important: `Nop56`'s 151 TH signature was dominated by down-regulation of RNA-processing/splicing genes and converged most with `Tnpo3`, `Uba5`, and `Ufc1`, not with same-pathway 60S factors. It also lacked the canonical p53/apoptosis, integrated-stress-response, and autophagy program expected from acute severe nucleolar damage. That makes `Nop56` evidence for factor-specific neuronal tolerance, not evidence that `Rrn3` should inherit a 25-DEG count.

### RNA polymerase III and stress counterexamples

| target | focal `n_degs` | expression evidence | interpretation for Rrn3 |
|---|---:|---|---|
| `Polr3b` | 8 | mostly down-regulated neuronal adhesion/Rap-family genes; top FDR genes were `Adgrb1` and `Rap1gap` | A sparse response to another polymerase system, but Pol III-specific rather than Pol I/rDNA initiation. |
| `Bdp1` | 8 | amino-acid/ISR-like up-regulated genes: `Ddit3`, `Mars1`, `Iars`, `Lars`, `Aars` | Shows tRNA/Pol III initiation stress can call a few genes, but the program is not a direct Rrn3 analog. |
| `Uba5` | 2,677 | broad response with strong `Eef1a1` up and `Rsrp1` down | A stalled-ribosome/UFMylation stress positive control. It proves the focal assay has power but is too far downstream and too broad to transfer to Rrn3. |
| `Ufc1` | 572 | overlaps the `Nop56` RNA/stress branch, with `Srsf11` down and `Eef1a1` up | Similar counterexample: relevant to ribosome quality control, not to basal Pol I initiation. |
| `Tnpo3` | 618 | splicing/RNA export genes such as `Leng8`, `Srrm2`, and `Tcea2` down | Converges with the RNA-processing portion of `Nop56`; not a Pol I initiation analog. |
| `Hnrnpu` | 733 | broad RNA-binding perturbation, and a corpus anti-neighbor to `Nop56` | Counterexample showing RNA-associated broad responses exist but can be directionally unrelated. |

These positive controls prevent an over-simple "all housekeeping genes are zero" rule. They also make the direct `Taf1b`/`Rbm28`/`Las1l` nulls more specific: the focal group can respond strongly, but not every essential RNA or ribosome factor triggers a detectable mRNA response.

### MYC and p53 axis checks

Complete Pol I inhibition and TIF-IA ablation can couple to p53, cell death, and growth-control pathways. Those axes did not appear active for the represented training targets in this focal group:

| target | focal `n_degs` | focal evidence |
|---|---:|---|
| `Myc` | 0 | `min(pvals_adj) = 0.136` across 210 perturbed nuclei |
| `Mycn` | 0 | `min(pvals_adj) = 0.347` across 320 perturbed nuclei |
| `Trp53` | 0 | `min(pvals_adj) = 0.338` across 251 perturbed nuclei |

The Distributed Agents corpus also summarized `Myc` and `Mycn` as lacking a broad acute ribosome-biogenesis or proliferative program in assayed postmitotic neurons. I therefore did not add a positive bump for a presumed MYC/p53 transcriptional response after `Rrn3` loss.

## Decision

The strongest mechanistic transfer is from `Taf1b`, with support from flat `Rbm28`, flat `Las1l`, and flat MYC/p53 regulators. `Nop56`, `Bdp1`, `Polr3b`, `Uba5`, and `Ufc1` show that RNA/ribosome stress can be observed in `151 TH Prkcd Grin2c Glut`, but their signatures are either downstream, Pol III-specific, or quality-control/stalled-ribosome programs rather than Rrn3-like Pol I initiation loss.

Given that direct Pol I promoter machinery was silent at FDR 0.05 and most held-in focal counts are zero, I predict that partial mosaic `Rrn3` loss will not produce any BH-significant mRNA DEGs in this cell group.

```tsv
target_name	predicted_n_degs
Rrn3	0
```

## Limits and uncertainty

- There was no direct `Rrn3` same-experiment claim in the Distributed Agents corpus, and the target was absent from the parquet by design; this prediction is an extrapolation from neighboring machinery.
- `Taf1b` is the best represented Pol I initiation comparator, but it is an SL1 subunit rather than the Pol I-associated Rrn3 bridge. A full Rrn3 knockout could be more severe than `Taf1b` knockdown.
- The experiment measures polyadenylated nuclear mRNA. Primary rRNA synthesis, nucleolar morphology, translation, apoptosis of unrecovered cells, and protein abundance were not measured by the DEG endpoint.
- Conditional Cre-lox TIF-IA neuronal knockouts in the literature are much stronger perturbations than this P16 AAV CRISPR screen, whose average on-target RNA reduction is modest. I therefore used those studies to establish mechanism, not to scale the DEG count upward.
- Some close Pol I genes were unavailable in training, including `Polr1a`, `Polr1b`, and `Ubtf`, so the comparison set is incomplete.
