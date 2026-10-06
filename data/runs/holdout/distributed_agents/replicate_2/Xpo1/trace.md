# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and interpretation

The held-out manifest for this run contains one requested perturbation:
`Xpo1`. I interpreted `n_degs` as the number of measured genes in `151 TH
Prkcd Grin2c Glut` nuclei with Benjamini-Hochberg adjusted Wilcoxon
`pvals_adj < 0.05`, using the same matched-control, single-nucleus DE tables
as the training file. `Xpo1` itself is absent as a `gene_target` from the
supplied parquet and absent from the training count CSV, so the prediction is
an extrapolation from observed non-held-out perturbations.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for focal-cell observed counts in all non-held-out targets.
- `[local file: training_de_all_cell_groups.parquet]`
  for signed `151 TH Prkcd Grin2c Glut` expression profiles of candidate
  analogs and counterexamples.
- The Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`, for curated findings about
  `Tpr`, `Tnpo3`, `Thoc1`, `U2af2`, `Rnpc3`, `Cdc40`, `Ranbp2`, and `Xpo7`.
  `Xpo1` had no direct corpus card in this release, so all corpus evidence is
  comparator evidence.
- PubMed-indexed literature on XPO1/CRM1 biology:
  - Fung and Chook 2014, DOI `10.1016/j.semcancer.2014.03.002`, for CRM1/XPO1
    as the major RanGTP-dependent export receptor and for NES-cargo recognition.
  - Azizian and Li 2020, DOI `10.1186/s13045-020-00903-4`, for the summary
    that XPO1 transports hundreds of proteins and several RNA species.
  - Yang et al. 2023, DOI `10.1038/s41392-023-01649-4`, for nuclear pore,
    karyopherin, and Ran-system context and disease relevance of nuclear
    transport proteins.
  - van Oirsouw et al. 2025, DOI `10.1016/j.gim.2025.101555`, for human
    dominant XPO1 neurodevelopmental disease and neuron-specific Drosophila
    knockdown phenotypes.

## Computational steps

I first read the training count CSV to calibrate the endpoint. It contains
1,674 focal-cell training perturbations; the distribution is highly zero
inflated: median `0`, 75th percentile `1`, 95th percentile `18`, and maximum
`2,677`. Only 469 of 1,674 targets have any FDR<0.05 gene in this cell group,
so the prior for a generic target is zero.

I then materialized only an RNA-export/nuclear-transport/RNA-processing
candidate panel from the parquet with an Arrow predicate:

```python
filter = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(candidates)
)
```

The resulting balanced matrix had 18 training targets by 17,259 measured genes
per target. I compared both whole signed profiles and exact FDR-supported
overlaps. Whole-logFC correlations were not decisive because even null
profiles such as `Xpo7`, `Kpna3`, and `Ranbp2` correlated with the broad
profiles after no genes crossed FDR. FDR-supported same/opposite overlap and
Wilcoxon-score similarity were more useful.

## Target-specific reasoning

| held-out target | observed comparator in 151 | `n_degs` | expression-pattern evidence and interpretation |
| --- | --- | ---: | --- |
| `Xpo1` | `Tpr` | 1,768 | Strongest mechanistic analog among represented targets. `Tpr` is a nuclear-basket factor tied to mRNA export and nuclear-pore homeostasis. In the Distributed Agents corpus, `Tpr:F002` reports recurrent changes of nuclear transport/export genes, including `Xpo1` up-regulation, and `Tpr:F003` reports recurrent down-regulation of RNA-processing factors including `Nxf1`. In the focal parquet, `Tpr` itself up-regulated measured `Xpo1` strongly (`log2FC = 0.955`, `p_adj = 3.2e-14`), consistent with CRM1 being recruited as a compensatory arm of the Tpr response. |
| `Xpo1` | `Tnpo3` | 618 | A karyopherin comparator with a large 151 signature. The corpus finding `Tnpo3:F003` identifies `Tpr` as the strongest same-direction FDR-overlap neighbor of `Tnpo3`, with 610 same-direction and 22 opposite gene-cell pairs across its restricted signature; in 151 alone I observed 260 same-direction and 5 opposite significant overlaps between `Tpr` and `Tnpo3`. This supports a nuclear-logistics/RNA-processing state but shows it is not identical to XPO1 cargo export. |
| `Xpo1` | `Thoc1` | 303 | THOC1 is a TREX mRNA-export subunit, and `Thoc1:F002` describes a THO/TREX-compatible RNA-biogenesis signature with induced RNA-biogenesis genes and decreased `Nxf1`, `Rnpc3`, `Snrnp70`, `Srrm2`, and `Ddx17`. It partially phenocopied `Tpr` in the corpus and shared 103 same-direction versus 11 opposite FDR genes with `Tpr` in the 151 data, placing it on the same export/RNP axis but at smaller amplitude. |
| `Xpo1` | `U2af2`, `Cdc40`, `Rnpc3`, `Prpf6`, `Snrnp70` | 828, 624, 868, 454, 213 | These are spliceosome or spliceosome-adjacent perturbations that converged with TPR/TREX states in the corpus. In the focal data, `Tpr` shared 220 same-direction FDR genes with `U2af2`, 201 with `Cdc40`, 194 with `Rnpc3`, 161 with `Prpf6`, and 71 with `Snrnp70`. This matters because XPO1 exports snRNAs and ribosomal subunits as well as NES proteins, so direct `Xpo1` loss is more likely to enter a broad RNA-processing/nucleolar stress state than to look like a cargo-specific null. |
| `Xpo1` | `Psmb4`, `Psmc1`, `Uba5`, `Ufc1` | 742, 430, 2,677, 572 | These are not direct XPO1 machinery, but the same-experiment corpus repeatedly connected `Tpr` and `Tnpo3` to proteasome/UFMylation perturbations. They calibrate the broad, vulnerable-neuron stress range in 151. I treated `Uba5` as an upper counterexample rather than a point analog because UFMylation loss was broader than nuclear-export loss in the training data. |
| `Xpo1` | `Xpo7`, `Kpna3`, `Ranbp2`, `Ddx39b` | 0, 0, 0, 0 | These prevent a blanket "all nuclear transport/export genes are broad" rule. `Xpo7` is the closest exportin paralog represented, but the Distributed Agents corpus reports a sparse Xpo7 surface and no Hedgehog/Gli or cargo-knockdown phenocopy. `Ranbp2` is a cytoplasmic nucleoporin that had broad effects in other neuronal classes but exactly zero 151 DEGs. `Ddx39b` was TREX-adjacent but flat in 151. I used these as branch-selective boundary cases, not as evidence that `Xpo1` should be zero, because none has CRM1's central cargo load. |

XPO1/CRM1 is the dominant receptor for leucine-rich NES protein export and
also participates in export of multiple RNA classes through the RanGTP/nuclear
pore system. That mechanism is broader than `Xpo7` and `Kpna3`, and it is
closer to the dataset's vulnerable `Tpr`/RNA-processing/proteostasis axis than
to the flat represented transport branches. Human and fly data also argue that
partial XPO1 loss can be pathogenic to neurons, although those data are
developmental and organismal rather than the acute P16 mouse CRISPR setting.

I therefore predicted a strong nonzero signature, below `Tpr`'s 1,768 because
XPO1 cargo mislocalization will be only partly visible in 3-prime nuclear RNA
abundance and may deplete the most damaged edited nuclei before harvest, but
well above `Thoc1`/`Tnpo3` because CRM1 is a more central receptor than a single
TREX subunit or SR-protein import receptor. The final point estimate is
`1,420` DEGs.

## Limits

The evidence is extrapolative. There was no direct `Xpo1` perturbation profile
or Distributed Agents finding in the released same-experiment corpus, and the closest
unassayed biochemical partners for XPO1, such as `Ran`, `Ranbp3`, `Rangap1`,
`Nup214`, and `Nup88`, were not present in the focal training count table. The
`Tpr` analogy is also imperfect: TPR lies at the nuclear basket and couples
strongly to NXF1/TREX-dependent mRNA export, whereas XPO1 directly exports NES
protein cargoes plus selected RNAs. Conversely, the null `Xpo7` and `Ranbp2`
counterexamples show that the assay does not convert every transport-factor
perturbation into a 151 response. The point estimate should therefore be read
as a calibrated high-count prediction, not as a claim that XPO1 loss will
exactly phenocopy TPR loss.
