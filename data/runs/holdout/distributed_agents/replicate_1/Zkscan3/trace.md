# Zkscan3 DEG-count prediction

## Question and endpoint

The requested prediction is the held-out `n_degs` for `Zkscan3` after acute AAV CRISPR-Cas9 loss of function in postnatal mouse `151 TH Prkcd Grin2c Glut` neurons. I interpreted `n_degs` exactly as the task defines it: the count of measured genes whose Wilcoxon Benjamini-Hochberg adjusted p-value is `< 0.05` for perturbed nuclei versus their matched safe/non-targeting controls in this single focal class.

There was one requested target:

```tsv
target_name
Zkscan3
```

The target is absent from both supplied training inputs, so no `Zkscan3` count or expression signature from the held-out experiment was available. The training count CSV is a direct observation of the endpoint for non-held-out perturbations. The Parquet is direct same-experiment differential-expression evidence for those non-held-out perturbations. The July PerturbAI same-experiment corpus is a packaged interpretation of the same experiment rather than an independent replicate. PubMed literature is an external mechanism prior.

## Sources used

- Declared focal endpoint file:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
- Declared all-cell differential-expression file:
  `training differential-expression dataset`
- Declared held-out target manifest:
  `single-target request for Zkscan3`
- Run-local task bindings, dataset portrait, measurement registry, compact source coverage, and capability manifest under `codex_runtime/pipeline`.
- Internal same-experiment corpus: `perturbai-july-260713-sourceguard-1773-v1`, queried with `corpus.calibration`, `corpus.findings`, `corpus.graph`, and `corpus.direct_evidence`.
- PubMed literature:
  - Chauhan et al. 2013, "ZKSCAN3 is a master transcriptional repressor of autophagy", *Molecular Cell*, DOI `10.1016/j.molcel.2013.01.024`, PMID `23434374`.
  - Barthez et al. 2020, "Human ZKSCAN3 and Drosophila M1BP are functionally homologous transcription factors in autophagy regulation", *Scientific Reports*, DOI `10.1038/s41598-020-66377-z`, PMID `32541927`.
  - Li et al. 2023, "Effect of Lacking ZKSCAN3 on Autophagy, Lysosomal Biogenesis and Senescence", *International Journal of Molecular Sciences*, DOI `10.3390/ijms24097786`, PMID `37175493`.

The July corpus had no direct `Zkscan3` Finding and no graph comparator records for `Zkscan3`; the target-specific decision therefore came from measured training analogs plus the external functional prior.

## Quantitative calibration

The focal training set contained 1,674 non-held-out perturbations. Its `n_degs` distribution was strongly zero-inflated:

```text
zero-count perturbations: 1205 / 1674
median: 0
75th percentile: 1
90th percentile: 2
95th percentile: 18
99th percentile: 436.5
maximum: 2677
```

I filtered the declared Parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and a bounded set of biologically relevant visible perturbations, then recomputed the focal count as:

```python
sum(pvals_adj < 0.05)
```

This matched the supplied endpoint CSV for the queried genes. I also inspected each signature's minimum adjusted p-value and FDR 0.10 count to separate complete nulls from nearly significant small responses.

## Biological comparison set

### Zkscan-family training analogs

The closest visible SCAN-domain training perturbations were both null in the focal cell group:

| training target | focal `n_degs` | focal FDR < 0.10 genes | pattern evidence |
|---|---:|---:|---|
| `Zkscan1` | 0 | 0 | every adjusted p-value was `1.0` in `151 TH Prkcd Grin2c Glut`; the top positive scores were small and non-significant, e.g. `Hsp90aa1` log2FC `0.176`, score `3.74`, padj `1.0` |
| `Zkscan16` | 0 | 0 | every adjusted p-value was `1.0` in the focal class; the top scores such as `Cadps` and `Ifrd1` were likewise padj `1.0` |

The same-experiment July corpus independently summarized the same null surface:

- `Zkscan1:F001`: `Zkscan1` produced 0 downstream genes at FDR < 0.10 in every one of the 22 recovered neuronal groups; `215 MB Dopa` was not recovered.
- `Zkscan1:F003`: represented SCAN-family perturbations did not phenocopy `Zkscan1`; `Zkscan16` had only two FDR < 0.10 genes and `Zscan26` had none across the matched groups, with full-score correlations to `Zkscan1` of `0.0116` and `0.0192`.
- `Zkscan16:F001`: `Zkscan16` loss produced a two-gene, two-cell-class surface, not a broad neuronal program.
- `Zkscan16:F006`: screened KRAB/SCAN, `Setdb1`, and `Mecp2` relatives did not phenocopy `Zkscan16`.

Within my focal extracted rows, the full-gene score correlation between `Zkscan1` and `Zkscan16` was also negligible, Spearman `0.055`, Pearson `0.059`. I therefore treated SCAN-family membership as a useful quiet-neighborhood prior, not as evidence of a shared specific program.

More generic visible zinc-finger perturbations were not as close mechanistically. In the focal endpoint, most were zero, while a few developmental or chromatin regulators were broad responders: `Zfp423 = 150`, `Zfp236 = 19`, and `Zfp148 = 8`. I used those as counterexamples against the idea that every DNA-binding zinc-finger gene is flat, but not as positive analogs for `Zkscan3`.

### Autophagy and lysosome analogs

External evidence places ZKSCAN3 in autophagy/lysosome transcriptional control. Chauhan et al. reported that human ZKSCAN3 represses a set of more than 60 autophagy and lysosome genes and directly regulates genes including `MAP1LC3B` and `WIPI2`; Barthez et al. found conserved ZKSCAN3/M1BP function in Drosophila but also noted that `Zkscan3` knockout mice lacked a discernible autophagy phenotype; Li et al. generated CRISPR `ZKSCAN3` knockout human cell lines and did not find significant induction of autophagic or lysosomal genes. I therefore considered ZKSCAN3 an autophagy/lysosome transcriptional regulator with strong cell-state dependence, not an obligate core autophagy component.

The focal training data argue that this neighborhood was mostly sparse in `151 TH Prkcd Grin2c Glut`:

| training target | focal `n_degs` | focal FDR < 0.10 genes | relevance |
|---|---:|---:|---|
| `Atg5` | 0 | 0 | core autophagy machinery; no focal response, minimum padj `0.105` |
| `Atg16l1` | 0 | 0 | ATG5-ATG12-ATG16L1 autophagosome elongation complex partner; no focal response, minimum padj `1.0` |
| `Becn1` | 0 | 0 | autophagy initiation/PI3K complex member; focal null |
| `Lamp2` | 0 | 2 | lysosome/autophagosome maturation gene; closest focal padj `0.0537`, just above the 0.05 endpoint threshold |
| `Rubcn` | 0 | 0 | autophagy regulator; focal null |
| `Map1lc3a` | 1 | 1 | one-gene focal response |
| `Sqstm1` | 1 | 2 | one FDR 0.05 focal response |
| `Rb1cc1` | 4 | 4 | small focal response |
| `Wdfy3` | 17 | 32 | the broadest inspected autophagy-linked focal response, still far below the long-tail high responders |

The same-experiment corpus supports the same interpretation: `Atg5:F002` reported no canonical autophagy, lysosome, p62, proteasome-rebound, or UPR/ISR transcriptional program after `Atg5`; `Atg16l1:F002` reported no detectable autophagy-lysosomal, UPR/ISR, or inflammasome mRNA aftershock; and `Atg16l1:F003` reported that obvious autophagy perturbations were sparse responders or flat and did not phenocopy `Atg16l1`.

### mTOR counterexamples

Because ZKSCAN3 and TFEB can oppose each other on lysosomal/autophagy genes, I also inspected the nutrient-growth axis that regulates TFEB and autophagy from upstream. The focal counts were mixed:

| training target | focal `n_degs` | interpretation |
|---|---:|---|
| `Rptor` | 0 | mTORC1 scaffold; complete focal null |
| `Mtor` | 2 | tiny focal signature, with `Rims3` and `Tmed8` passing FDR 0.05 |
| `Fkbp1a` | 1 | small response |
| `Akt3`, `Igf1r`, `Irs1`, `Pik3cb`, `Pik3r1`, `Pik3r2`, `Strada` | 0 each | same broad pathway, no focal response |
| `Srebf2` | 7 | small sterol-branch response |
| `Depdc5` | 13 | small-to-moderate mTORC1-regulator response |
| `Tsc2` | 86 | real mTORC1 derepression counterexample |

`Tsc2` is the strongest counterexample in this neighborhood. Its focal signature included 86 FDR 0.05 genes, with sterol and metabolic responders such as `Cyp51`, feedback/nutrient regulators such as `Pik3r3`, and a broader same-experiment mTORC1 response. I did not transfer the `Tsc2` count to `Zkscan3`, because the causal signs and pathway positions differ: loss of `Tsc2` removes an upstream brake on mTORC1, whereas loss of `Zkscan3` is expected to remove transcriptional repression on a subset of autophagy/lysosome genes. The internal corpus also flagged this separation: `Mtor:F005` reported that canonical same-pathway perturbations, including `Rptor` and multiple PI3K/AKT genes, did not phenocopy `Mtor`; `Tsc2:F007` reported that `Mtor`, `Rptor`, `Igf1r`, `Irs1`, and `Akt3` did not give a robust matched FDR overlap with `Tsc2`.

## Zkscan3 call

The causal transfer model I used was:

`Zkscan3` CRISPR loss -> possible partial loss of ZKSCAN3 transcriptional repression -> possible derepression of autophagy/lysosome target genes in edited, recovered postnatal thalamic glutamatergic neurons -> BH-corrected Wilcoxon hits among survivor nuclei.

Chauhan et al. make the first two biological links plausible in some contexts, but the later links are weak for this experiment. The known ZKSCAN3 autophagy program was largely defined in human cancer or stress models; Barthez et al. and Li et al. both caution that complete ZKSCAN3 loss need not generate a large autophagy/lysosome transcriptome in normal mammalian cells. In the declared Perturb-seq data, close visible SCAN-domain perturbations were focal nulls, and direct perturbation of core autophagy machinery in the same endpoint was also zero or nearly zero. The broader mTORC1 counterexample `Tsc2` shows that this cell group can report an endomembrane/metabolic response, but its effect arises from mTORC1 disinhibition and has no same-sign obligate transfer to `Zkscan3`.

I therefore predict that acute sparse `Zkscan3` loss will not put any measured gene below adjusted p-value 0.05 in `151 TH Prkcd Grin2c Glut`.

## Final prediction

```tsv
target_name	predicted_n_degs
Zkscan3	0
```

## Limits

- There is no held-out `Zkscan3` expression vector in the supplied Parquet and no direct `Zkscan3` Finding in the July same-experiment corpus.
- `Zkscan1` and `Zkscan16` are SCAN-domain relatives, not paralogs known to share ZKSCAN3 DNA-binding targets, so their nulls are a local weak-response prior rather than proof of functional equivalence.
- The most relevant external ZKSCAN3 autophagy studies were not performed in the same postnatal thalamic glutamatergic neuronal context or with the same low-efficiency mosaic CRISPR perturbation.
- Core autophagy perturbations being flat in recovered nuclei does not exclude unmeasured earlier selection, flux-level effects, or protein-level lysosomal changes. It only argues against a broad survivor-state snRNA-seq DEG count at this assay's FDR threshold.
- A very small positive outcome, such as one or two threshold-crossing genes, would not be biologically surprising, but the within-dataset analogs favor zero as the integer point estimate.
