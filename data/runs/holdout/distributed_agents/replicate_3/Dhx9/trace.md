# Dhx9 prediction trace

## Question and setup

The requested held-out target file is
`[local file: 056_Dhx9.csv]`.
It contains one perturbation, `Dhx9`, and the requested endpoint is the integer
number of genes with `pvals_adj < 0.05` after acute CRISPR loss of function in
`151 TH Prkcd Grin2c Glut` neurons.

I treated `151 TH Prkcd Grin2c Glut` as a thalamic glutamatergic class and
interpreted `n_degs` strictly as this experiment's Wilcoxon/BH response breadth,
not as gene essentiality or as guide performance. `Dhx9` is absent from both the
per-gene DE parquet and the focal-cell training count CSV, so the prediction is
an interpolation from related, observed perturbations.

## Data and sources used

- Training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  This contained 1,674 non-held-out targets. The distribution is very sparse
  and heavy-tailed: median 0, 75th percentile 1, 95th percentile 18, 99th
  percentile 436, and maximum 2,677 DEGs.
- Per-gene DE:
  `[local file: training_de_all_cell_groups.parquet]`.
  I queried the parquet with DuckDB, restricted to
  `group_name = '151 TH Prkcd Grin2c Glut'`, and pulled `names`, `gene_target`,
  `logfoldchanges`, `pvals_adj`, `scores`, and matched nucleus counts for
  biologically selected analogs.
- Same-experiment semantic layer:
  Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
  `target_context(Dhx9)` returned no Dhx9-specific findings, claims, or
  explicit references in this release, so absence of a corpus story was treated
  as missing annotation rather than a null result.
- Profile tooling:
  Distributed Agents runtime profile comparison was run on the focused focal-cell
  expression table to audit significant-feature burden and signed overlap
  among selected analogs.
- External biology:
  PubMed literature on DHX9/RNA helicase A, R-loop metabolism, transcription,
  A-to-I editing, and related RNA-binding proteins.

The main parquet extraction was:

```sql
SELECT names, gene_target, logfoldchanges, pvals_adj, scores
FROM read_parquet($training_de)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN ($manually_selected_analogs)
```

This returned 17,259 measured genes per selected training target; recomputing
`SUM(pvals_adj < 0.05)` for each selected target reproduced the CSV counts.

## Within-dataset calibration

No close `Dhx9` paralog was available for direct calibration: the training count
CSV had no `Dhx*` targets and only two `Ddx*` targets, `Ddx3x` and `Ddx39b`.
The mechanistic comparison therefore had to use functional neighborhoods rather
than one-to-one paralogs.

Training targets most relevant to a nuclear RNA helicase/nuclear RBP mechanism:

| training target | observed DEGs | focal-cell expression evidence | interpretation for Dhx9 |
|---|---:|---|---|
| `Matr3` | 149 | 105 up and 44 down significant genes; top FDR hits included `Ddhd1`, `Atp9b`, `E2f4`, and `Rsrp1` | A DNA/RNA-binding nuclear matrix RBP and splicing regulator. This is the closest observed count-scale analog for a non-core nuclear RBP. |
| `Hnrnpc` | 122 | top hits included `Txnl1` up, `Rbm25` down, `Luc7l2` down | Another nuclear RNA-binding/splicing factor with a moderate, not genome-wide, response. |
| `Tardbp` | 210 | 210 DEGs, with strong self downregulation and changes in `Ppp6c`, `Gabpa`, `Usp15`, `Fam135a`, `Brms1l` | Multifunctional neuronal RBP; useful because it shows that disease-linked nuclear/cytoplasmic RBPs can land near a few hundred DEGs rather than the 700+ core-splicing range. |
| `Hnrnpu` | 733 | 483 up and 250 down significant genes; shared 174 significant genes with `Rnpc3` and 171 with `U2af2` | Chromatin-associated nuclear RBP with a much broader observed state. I treated this as an upper bracket, because DHX9 is nuclear but is not itself the HNRNPU scaffold. |
| `Rnpc3`, `U2af2`, `Cdc40`, `Prpf6`, `Thoc1`, `Snrnp70` | 868, 828, 624, 454, 303, 213 | The strongest pair, `Rnpc3`/`U2af2`, shared 194 significant genes, 157 in the same direction; `Rnpc3`/`Cdc40` shared 136; `Rnpc3`/`Prpf6` shared 127 | These are core spliceosome or mRNA export/splicing-complex perturbations and form a strong high-DEG module. DHX9 can influence splicing, but the literature does not make it a constitutive U2/U12 spliceosome component, so I did not copy their 300-900 counts. |

Counterexamples that were mechanistically informative:

| training target | observed DEGs | why this mattered |
|---|---:|---|
| `Ddx3x` | 8 | The only observed DExD/H helicase with any DEGs; a cytoplasmic translation/stress-granule helicase. Its weak response argues against assigning DHX9 a broad signature from helicase-family membership alone. |
| `Ddx39b` | 0 | DEAD-box splicing/export factor but no significant focal-cell DEGs. |
| `Setx` | 0 | R-loop resolution by itself was not enough to produce a detected focal-cell response in this assay. |
| `Adar`, `Adarb1` | 0, 4 | A-to-I/dsRNA regulators were mostly quiet. |
| `Dicer1`, `Cnot1`, `Fmr1`, `Fxr1` | 0, 0, 0, 0 | Other RNA-regulatory genes were null, another guard against a generic "RNA pathway" positive call. |
| `Wrn`, `Atrx`, `Crebbp`, `Ep300` | 0, 8, 8, 0 | R-loop/chromatin/transcriptional cofactor functions also include many focal-cell nulls. |

The significant-gene overlaps supported the same separation. Spliceosome-like
perturbations shared dozens to hundreds of FDR-significant genes in concordant
directions, for example `Rnpc3`/`U2af2` shared 194 and `Rnpc3`/`Hnrnpu` shared
174. In contrast, low-count counterexamples such as `Ddx39b`, `Setx`, `Adar`,
and `Dicer1` had zero shared significant genes with the main positive analogs.
The moderate nuclear RBPs were intermediate: `Matr3` shared 36 significant
genes with `Hnrnpu`, 32 with `U2af2`, and 21 with `Rnpc3`, far less than the
core spliceosome block but not wholly disconnected.

## External biological rationale for Dhx9

`Dhx9` encodes RNA helicase A, an abundant nuclear DExH-box DNA/RNA helicase.
The external literature pushes the prediction away from a focal-cell null:

- Dhx9/RNA helicase A homozygous loss causes early mouse embryonic lethality and
  apoptosis in embryonic ectoderm, showing that the gene is not a dispensable
  peripheral helicase in mammalian cells (Lee et al. 1998,
  DOI 10.1073/pnas.95.23.13709).
- Human monoallelic DHX9 variants cause neurodevelopmental disorder and
  Charcot-Marie-Tooth disease; disease variants can alter DHX9 localization,
  ATPase activity, R-loop levels, and DNA breaks, linking the protein to
  neuronal homeostasis as well as dividing-cell genome maintenance (Calame et
  al. 2023, DOI 10.1016/j.ajhg.2023.06.013).
- DHX9 is a multifunctional RNA helicase tied to transcriptional regulation,
  not only bulk RNA unwinding; Fuller-Pace 2006 specifically grouped Dhx9 with
  Ddx5/Ddx17-like transcriptional DExD/H-box helicases (DOI
  10.1093/nar/gkl460), and Wilson and Giguere 2007 showed functional-pathway
  linkage and direct interaction among DHX9, DDX5, and DDX17 in a splicing/
  transcriptional RNA-helicase context (DOI 10.1186/1471-2164-8-419).
- DHX9 binds RNA/DNA hybrids and can suppress aberrant R-loops and
  R-loop-associated DNA damage (Cristini et al. 2018,
  DOI 10.1016/j.celrep.2018.04.025).
- DHX9 also regulates A-to-I RNA editing in a substrate-dependent way (Hong et
  al. 2018, DOI 10.1093/nar/gky396) and can act as a nuclear transcriptional
  coactivator for NF-kappaB promoters by supporting RNA polymerase II
  recruitment (Ng et al. 2018, DOI 10.1093/nar/gky742).
- As a scale analog for the training positives, MATR3 is a nuclear matrix
  DNA/RNA-binding protein that regulates hundreds of alternative-splicing
  events (Coelho et al. 2015, DOI 10.15252/embj.201489852), while TDP-43 is a
  neuronal RBP involved in transcription, splicing, RNA transport, and RNA
  stability (Budini et al. 2011, DOI 10.2174/156720511795563719).

Taken together, this makes `Dhx9` a biologically plausible hit in the most
responsive thalamic population, but it is an imperfect match to the highest
training counts. DHX9 is not `Rnpc3`, `U2af2`, or `Prpf6`: it should not be
forced into the 450-870 DEG core spliceosome range. Conversely, the direct
R-loop counterexample `Setx = 0` and the RNA-editing counterexamples
`Adar = 0`, `Adarb1 = 4` should not drive it to zero because DHX9 sits at a
broader intersection of transcription, R-loops, ADAR substrate editing, and
neuronal disease.

## Prediction

I predict a moderate nonzero footprint, close to `Matr3`/`Hnrnpc`/`Tardbp` and
below the core-spliceosome factors:

- lower bracket: helicase/R-loop/editing controls, mostly 0-8 DEGs;
- central analogs: `Hnrnpc = 122`, `Matr3 = 149`, `Tardbp = 210`;
- upper bracket: `Thoc1 = 303`, `Prpf6 = 454`, `Cdc40 = 624`,
  `Hnrnpu = 733`, `U2af2 = 828`, `Rnpc3 = 868`.

The point estimate is `160` DEGs.

## Limits

This is an extrapolation. There was no held-out `Dhx9` expression signature, no
observed close `Dhx9` paralog in the training table, and the Distributed Agents
same-experiment corpus had no `Dhx9` record in this release. DHX9 has many
roles defined in cancer, fibroblasts, macrophages, and developmental systems,
and those are only priors for sparse postnatal neuronal CRISPR. The
spliceosome-like perturbations provide clear high-count examples, but their
shared expression pattern is not the same as a DHX9 loss state; the R-loop and
RNA-editing nulls are also imperfect because DHX9 has a broader nuclear RNP
portfolio than `Setx` or `Adar`. The exact integer therefore has more
uncertainty than the nonzero-but-moderate decision.
