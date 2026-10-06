# Reasoning trace

## Question and endpoint

The held-out target in this shard is `Ergic1`. I interpreted the task as a
point prediction of the number of genes that would pass
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in the focal
`151 TH Prkcd Grin2c Glut` class if the acute sparse AAV-CRISPR experiment had
included an `Ergic1` perturbation. The answer therefore predicts an
assay- and power-dependent DEG count among recovered thalamic glutamatergic
neurons, not editing efficiency, cell survival, biological essentiality, or a
bulk ER-to-Golgi trafficking phenotype.

`Ergic1` was absent from both supplied training surfaces:

- It is the only value in the requested-target CSV.
- It is not a row in the `151 TH Prkcd_Grin2c_Glut_deg_counts_training.csv`
  endpoint table.
- Its held-out perturbation signature is not in the declared differential
  expression parquet.

The requested endpoint is absent for `Ergic1` by construction. The focal
training `n_degs` table and the non-held-out parquet rows are direct
measurements of the same endpoint and adjacent expression patterns for
training genes; external biology is used only to choose which visible
perturbations are mechanistically relevant analogs.

## Sources used

Internal same-experiment sources:

- Supplied focal endpoint table,
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Supplied training differential-expression parquet,
  `training differential-expression dataset`.
- The run-local dataset portrait, task bindings, coverage summary,
  capability manifest, and measurement registry under `codex_runtime/pipeline`.
- The selected same-experiment report/ledger corpus,
  `perturbai-july-260713-sourceguard-1773-v1`, queried only for reports around
  visible analog perturbations because no packaged `Ergic1` report was present.

External mechanism sources:

- Breuza et al. 2004, J. Biol. Chem.,
  DOI `10.1074/jbc.M406644200`, PMID `15308636`: ERGIC-32/ERGIC1 is a cycling
  ER-Golgi intermediate compartment protein related to yeast Erv41p/Erv46p
  and interacts with human Erv46.
- Bi, Corpina and Goldberg 2002, Nature,
  DOI `10.1038/nature01040`, PMID `12239560`: Sar1-GTP recruits the
  Sec23/Sec24 COPII prebudding complex that selects cargo and SNAREs for
  ER-derived vesicles.
- Cai et al. 2007, Nature,
  DOI `10.1038/nature05527`, PMID `17287728`: Sec23-marked COPII vesicles are
  coupled to TRAPPI tethering en route to the Golgi.

## Quantitative calibration from the focal training table

The 1,674 visible training perturbations in `151 TH Prkcd Grin2c Glut` were
heavily zero inflated:

| Summary | n_degs |
|---|---:|
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2677 |

`469 / 1674` training perturbations had any focal FDR 0.05 hit, while
`1205 / 1674` had zero. Thus a held-out trafficking gene should be assigned a
large count only if it matches a measured training branch with a broad
survivor-state transcriptional program.

## Mechanistic analogs inspected for Ergic1

ERGIC1 is positioned at the ER-Golgi intermediate compartment, adjacent to the
COPII ER-export machinery and the COPI retrieval route rather than in the ER
chaperone system itself. I therefore compared it primarily with visible
ER-to-Golgi/COPI/COPII perturbations and then used ER-proteostasis targets as
counterexamples that prove this neuronal assay can detect UPR/ISR expression
when the perturbed gene actually triggers it.

### Direct early-secretory analogs

Focal `n_degs` for the most relevant visible genes were:

| Training perturbation | Focal n_degs | Relation to Ergic1 | Expression-pattern evidence |
|---|---:|---|---|
| `Sec23a` | 0 | Inner COPII coat adaptor downstream of Sar1; functionally upstream of ERGIC arrival | 0 focal FDR 0.05 genes among 17,259 measured transcripts. The strongest own-transcript trend had `logfoldchanges = -0.351`, `pvals_adj = 0.8735`. |
| `Sar1b` | 0 | COPII initiation GTPase upstream of SEC23/SEC24 recruitment | 0 focal FDR 0.05 genes. The `Sar1b` self row trended down but was not FDR-significant at 0.05 (`logfoldchanges = -0.615`, `pvals_adj = 0.108`). |
| `Copa` | 0 | alpha-COP subunit of COPI retrieval from Golgi/ERGIC toward the ER | 0 focal FDR 0.05 genes. No ER-stress or interferon gene reached significance in the focal class. |
| `Copg1` | 1 | gamma-COP subunit of the same COPI coatomer as COPA | Exactly 1 focal FDR 0.05 gene among 17,259 rows, and the only significant row was `Copg1` itself (`logfoldchanges = -0.668`, `pvals_adj = 9.24e-17`). |
| `Lman2l` | 0 | ERGIC/cargo-receptor-adjacent secretory pathway gene, less direct than ERGIC1 | 0 focal DEGs in the endpoint table. |
| `Stx5a` | 0 | ER-Golgi SNARE-family traffic component | 0 focal DEGs in the endpoint table. |
| `Tango2` | 0 | trafficking-associated Golgi/mitochondrial stress gene, indirect for ERGIC1 | 0 focal DEGs in the endpoint table. |

These are imperfect one-gene knockouts, but they all perturb the same transport
axis at positions where a strong ER-to-Golgi block would be expected to create
cargo retention, KDEL retrieval defects, or UPR/ISR signaling. The three
closest core analogs in the training endpoint, `Sec23a`, `Sar1b`, and `Copa`,
were strict focal zeros, while same-coatomer `Copg1` only crossed FDR through
its own target transcript. This makes a multi-dozen DEG `Ergic1` response
unlikely.

The selected PerturbAI July corpus independently summarized the visible
analogs as assay-specific nulls or near-nulls, not as hidden stress programs:
`Sec23a` produced no adjusted downstream response in any measured postmitotic
neuronal group and failed to induce the UPR/ERAD markers that were detectable
after `Hspa5` or `Sec63`; `Sar1b` produced no robust downstream response across
its 20 recovered groups and did not induce a COPII, UPR, or ISR compensation
program; `Copa` produced a whole-transcriptome null across recovered neuronal
classes and did not reproduce the ER-stress/STING outputs associated with COPA
syndrome models; and `Copg1` did not induce canonical COPI-failure UPR or
type-I-interferon genes in the neuronal assay.

### Stress-positive counterexamples

I did not transfer from every ER-stress gene to `Ergic1`, because ERGIC1 is a
cycling ERGIC cargo/sorting protein, whereas `Hspa5` and `Sec63` directly
support ER protein folding and translocation. They are still important
counterexamples for assay sensitivity:

| Counterexample perturbation | Focal n_degs | Why it bounds the prediction |
|---|---:|---|
| `Hspa5` | 5 | Loss of the BiP ER chaperone directly activates ER proteostasis signaling and gave a small but real focal ER-stress signature. |
| `Sec63` | 11 | Perturbing the Sec61/Sec62-associated HSP40 factor gave a focal UPR/chaperone response. |
| `Gfpt1` | 311 | This produced a broad focal ER/ISR-like stress signature and shows that hundreds of focal DEGs are possible when a perturbation enters a strong stress branch. |

The focal parquet confirmed that stress markers such as `Hspa5`, `Ddit3`,
`Xbp1`, `Atf4`, and `Herpud1` were FDR-significant in multiple strong stress
or proteostasis perturbations, but not after the measured `Sec23a`, `Sar1b`,
`Copa`, or `Copg1` perturbations. Therefore the early-secretory nulls are not
explained by a wholesale inability of `151 TH Prkcd Grin2c Glut` nuclei to
report ER stress.

## Target-specific prediction

### Ergic1 -> predicted 0 DEGs

The causal chain for an `Ergic1` perturbation is:

`Ergic1` loss of function -> altered ERGIC/early secretory sorting with a
possible ERGIC-32/Erv46 complex defect -> partial disruption of cargo cycling
between ER, ERGIC, and cis-Golgi -> possible ER export/retrieval stress in
neurons if the defect is limiting -> recovery of surviving, class-assigned
thalamic glutamatergic nuclei 3-4 weeks after sparse P16 CRISPR -> Wilcoxon
DEG calls in the nuclear RNA endpoint.

The first two steps are biologically plausible: Breuza et al. localized
ERGIC-32/ERGIC1 to the ERGIC and showed interaction with Erv46, so it belongs
on the early secretory path rather than being an arbitrary membrane protein.
However, the measured dataset steps argue for buffering. `Sec23a` and `Sar1b`
act upstream in COPII vesicle formation, a stage structurally tied to ER export
by Sar1 and Sec23/Sec24; `Copa` and `Copg1` act on the opposing COPI retrieval
route through the same ERGIC/cis-Golgi compartment. All four were focal zeros
or self-only near-zeros. An `Ergic1` perturbation is less likely than
`Hspa5`, `Sec63`, or `Gfpt1` loss to create a primary UPR/ISR transcriptional
state because it is not itself the luminal BiP chaperone, an ER translocon
cofactor, or a hexosamine/protein-glycosylation enzyme.

I therefore predict no genes will pass FDR 0.05. I kept the count exactly at
0, rather than 1-5, because the direct training perturbations closest to
ER-to-Golgi traffic were dominated by exact zeros; the single `Copg1` focal
hit was the guide-targeted transcript itself, not a downstream stress marker.

## Limits and extrapolation

The largest limitation is that the best ERGIC1 complex partners were not
training perturbations: `Ergic2`, `Ergic3`, canonical ERGIC cargo receptors,
and most COPI/COPII paralogs were absent from the visible focal endpoint table.
Thus the prediction extrapolates from neighboring transport machinery, not
from a matched ERGIC1-family knockout.

The parquet is a differential-expression summary over recovered nuclei. It
does not measure DNA indels, ERGIC1 protein, protein secretion, ER-to-Golgi
transport rates, or nuclei lost before sequencing, so a predicted zero only
means a zero FDR 0.05 nuclear-RNA burden among recovered
`151 TH Prkcd Grin2c Glut` cells. A severe `Ergic1` editing event followed by
early cell loss or a purely post-transcriptional trafficking defect could be
missed by this endpoint.

Finally, ERGIC1 might have cargo-selective neuronal functions not reproduced
by `Sec23a`, `Sar1b`, `Copa`, or `Copg1`, and the average AAV-CRISPR effect is
partial. Those uncertainties would move the true value within the sparse
near-zero range, but they do not justify a broad DEG prediction from the
available training analogs.
