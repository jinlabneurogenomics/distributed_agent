# Prediction target

The held-out target list contains a single perturbation, `Hnrnpa1`. I therefore
predicted the number of genes that would have `pvals_adj < 0.05` for an acute
AAV-CRISPR loss-of-function perturbation of `Hnrnpa1` in `151 TH Prkcd Grin2c
Glut` nuclei. I treated the value as the same assay endpoint as the training
CSV, not as a generic measure of neuronal importance, lethality, or edit
success.

The main ambiguity I resolved was how far to transfer from other RNA-binding
protein perturbations. `Hnrnpa1` is an hnRNP and an ALS/multisystem-proteinopathy
gene, but the same-experiment corpus repeatedly shows that hnRNP-family or
ALS-linked RBP membership was not enough to make broad perturbations
interchangeable in this postnatal whole-brain snRNA-seq readout. I therefore
used strong RBPs such as `Hnrnpu`, `Hnrnpc`, `Tardbp`, and `Matr3` mostly as
counterexamples and used `Hnrnpa2b1` as the closest focal calibration point.

# Sources

- Input training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest:
  `[local file: 106_Hnrnpa1.csv]`.
- Internal same-experiment semantic layer:
  Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
  Direct `target_context` lookup for `Hnrnpa1` had no Claims, Findings, or
  explicit comparator references, which is expected for this held-out target.
- Internal runtime profile:
  `profile_neighbors` over the focal parquet rows compared observed RNA-binding
  anchors `Hnrnpa2b1`, `Hnrnpc`, `Hnrnpu`, `Tardbp`, and `Matr3` against all
  1,674 focal training perturbations.
- External literature:
  Mayeda et al. 1993, DOI `10.1128/MCB.13.5.2993-3001.1993`, PMID `8474457`;
  Michael et al. 1995, DOI `10.1016/0092-8674(95)90119-1`, PMID `8521471`;
  Izaurralde et al. 1997, DOI `10.1083/jcb.137.1.27`, PMID `9105034`;
  Kim et al. 2013, DOI `10.1038/nature11922`, PMID `23455423`;
  Liu et al. 2017, DOI `10.1098/rsob.160303`, PMID `28077597`.

# Dataset calculations

The focal training endpoint is highly zero-inflated. Among 1,674 non-held-out
targets, 1,205 have zero DEGs, 363 have 1 to 9, 63 have 10 to 89, and 43 have at
least 100. The median is 0, the 90th percentile is 2, and the 95th percentile is
18. Thus a count near 10 is already above most training perturbations.

For exact focal analog counts, I read only the `151 TH Prkcd Grin2c Glut`
row groups from the parquet, selected RNA-binding and RNA-processing comparators,
and recounted `pvals_adj < 0.05`. The computed counts matched the training CSV:

| training perturbation | focal `n_degs` | role for `Hnrnpa1` |
| --- | ---: | --- |
| `Hnrnpdl` | 1 | same broad hnRNP family but essentially flat; lower bound/counterexample |
| `Hnrnph2` | 4 | hnRNP-family, weak and mechanistically farther |
| `Hnrnpa2b1` | 11 | closest observed A/B hnRNP paralog and best anchor |
| `Hnrnpc` | 122 | visible nuclear hnRNP response, but not A/B-like |
| `Matr3` | 149 | ALS-linked nuclear matrix RBP; partial disease-family comparator, not A/B paralog |
| `Tardbp` | 210 | ALS-linked RBP; broad, stress/ER-lysosomal state, not a close LoF phenocopy |
| `Snrnp70` | 213 | spliceosome comparator |
| `Prpf6` | 454 | core spliceosome comparator |
| `Hnrnpu` | 733 | hnRNP-family scaffold with a very broad secondary stress signature |
| `U2af2` | 828 | core 3-prime-splice-site factor |
| `Rnpc3` | 868 | minor-spliceosome factor |

The observed `Hnrnpa2b1` focal signature contained 11 FDR-significant genes:
`Rbm25`, `Hnrnpa1`, `Parp6`, `Snx29`, `Hnrnpu`, `Fam193b`, `Tcerg1`, `Atp11b`,
`Ttc8`, `Gga1`, and `Drosha`. `Hnrnpa1` itself was the second strongest hit
after `Hnrnpa2b1` perturbation in this cell group
(`log2FC = 1.080`, `pvals_adj = 3.0e-5`) and was reported by Distributed Agents
`Hnrnpa2b1:F002` as a recurrent marker of the main Hnrnpa2b1 glutamatergic
responders. That makes `Hnrnpa2b1` the only observed perturbation with a direct
A/B-family compensation signal involving the held-out gene.

The same focal `Hnrnpa2b1` signature had little FDR-level overlap with broad
RBP responses: only 2 of 122 `Hnrnpc` DEGs, 4 of 733 `Hnrnpu` DEGs, 1 of 210
`Tardbp` DEGs, and 1 of 149 `Matr3` DEGs overlapped the 11 `Hnrnpa2b1` DEGs.
Those overlaps agree with corpus Findings `Hnrnpa2b1:F004`, `Hnrnpc:F008`,
`Hnrnpu:F009`, and `Matr3:F007`: related nuclear RBPs were detectable under the
same workflow, but the broad RBP signatures did not collapse into one generic
hnRNP or ALS-family module.

# Target-specific rationale

`Hnrnpa1` encodes a shuttling A/B hnRNP with two RNA-recognition motifs and a
glycine-rich low-complexity domain. HNRNPA1 can regulate splice-site choice
opposite SR proteins in classic splicing assays (Mayeda et al. 1993; Caceres
et al. 1994, PMID `8085156`) and its M9 domain is sufficient for nuclear export
and import behavior consistent with messenger-RNP shuttling (Michael et al.
1995; Izaurralde et al. 1997). Pathogenic mutations in the prion-like domains
of HNRNPA1 and HNRNPA2B1 were found in multisystem proteinopathy and ALS and
increase fibrillization and stress-granule recruitment (Kim et al. 2013).
Germline `Hnrnpa1` knockout in mice is embryonic lethal with muscle-development
splicing defects, and that study did not find simple Hnrnpa2b1 expression
compensation in the mutant animals (Liu et al. 2017).

Those external facts support a nonzero prior: `Hnrnpa1` is not a dispensable
neuronal passenger gene, and its closest paralog is itself an observed focal
responder. They do not support copying the `Hnrnpu`, `Tardbp`, `Matr3`, or
core-spliceosome counts, because this snRNA-seq endpoint measures whole-gene
abundance in surviving postnatal neurons and the same experiment already showed
that many RNA-binding perturbations have distinct, sometimes nearly flat,
gene-abundance outputs.

I therefore predicted just above the `Hnrnpa2b1` count of 11:

- Zero is unlikely because the `Hnrnpa2b1` perturbation produced a reproducible
  A/B-hnRNP compensation signal and because focal 151 cells clearly recover
  RNA-processing perturbations.
- A weak 1 to 9 call seemed too low because loss of `Hnrnpa1` may be less
  reciprocally buffered by `Hnrnpa2b1` than the reverse direction in this assay.
- A medium or strong broad response seemed unlikely because `Hnrnpa2b1` had
  only 11 DEGs, `Hnrnpdl` and `Hnrnph2` had only 1 and 4, and the strong
  comparators were annotated as separate RNP/spliceosome/proteostasis states.

The final point prediction was `14` DEGs: a low nonzero focal response, close to
the measured `Hnrnpa2b1` analog and far below the broad `Hnrnpc`/`Hnrnpu`/core
spliceosome range.

# Limits

The strongest limitation is that no `Hnrnpa1` perturbation profile is present in
the training parquet or Distributed Agents target corpus, so the prediction extrapolates
from an asymmetric paralog relationship. `Hnrnpa2b1` up-regulated `Hnrnpa1`,
but the experiment cannot tell whether `Hnrnpa1` loss would be rescued by
`Hnrnpa2b1`, by `Hnrnpa3`, or by a non-A/B splicing factor. The endpoint is
gene-level 10x snRNA-seq, so direct alternative-splicing defects may be missed
even when HNRNPA1 function is perturbed. Germline mouse lethality and human ALS
proteinopathy literature are developmental or toxic-gain contexts rather than
P16 mosaic neuronal CRISPR loss-of-function, so they only justify a low
nonzero prior rather than a large DEG count.
