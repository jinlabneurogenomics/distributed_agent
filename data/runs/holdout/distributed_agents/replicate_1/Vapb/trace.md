# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

I interpreted the requested endpoint as one scalar point prediction for each
held-out perturbation: the number of measured genes in `151 TH Prkcd Grin2c
Glut` with Wilcoxon Benjamini-Hochberg adjusted `pvals_adj < 0.05`. The target
manifest for this run contains only:

| target_name |
|---|
| Vapb |

The held-out `Vapb` signature is absent from both supplied input files, so the
prediction below transfers from non-held-out perturbations in the same Parquet
plus external knowledge about VAPB biology. `n_degs` is assay- and
power-dependent; I did not treat target-RNA reduction as an editing-efficiency
score.

## Sources used

- Declared training count table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
  with 1,674 visible perturbations in the focal group.
- Declared differential-expression Parquet:
  `training differential-expression dataset`.
  I queried only rows from `151 TH Prkcd Grin2c Glut` and visible candidate
  analog targets.
- Run-local manifests: `codex_runtime/pipeline/task_bindings.json`,
  `coverage.json`, `measurement_registry.json`, and `capabilities.json`.
- Packaged same-experiment July corpus
  `perturbai-july-260713-sourceguard-1773-v1`, specifically bounded Finding
  ledger summaries for visible training genes `Tardbp`, `Atxn2`, `Vcp`,
  `Sqstm1`, `Tmem106b`, `Chmp4b`, and `Osbpl2`. This corpus is an interpreted
  representation of the same screen, not an independent experiment.
- External functional priors from the VAP/FFAT and ALS literature: Nishimura
  et al. 2004 identified dominant VAPB mutations in ALS8
  (doi:10.1086/425287); Loewen et al. 2003 defined the FFAT interaction axis
  between ER VAP proteins and lipid-binding proteins
  (doi:10.1093/emboj/cdg201); Murphy and Levine 2016 reviewed VAPA/VAPB as
  redundant ER membrane-contact adaptors for FFAT-containing partners
  (doi:10.1016/j.bbalip.2016.02.009); De Vos et al. 2012 connected VAPB with
  PTPIP51 at ER-mitochondria contact sites and calcium exchange
  (doi:10.1093/hmg/ddr559).

External PubMed/EuropePMC lookups timed out from this run, so those citations
were used from prior biological knowledge rather than live retrieval.

## Quantitative checks over the supplied data

The focal training endpoint is highly zero-inflated:

| statistic | value |
|---|---:|
| visible focal perturbations | 1,674 |
| `n_degs == 0` | 1,205 |
| `n_degs > 0` | 469 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

I checked that the Parquet contains 28,891,566 focal rows, matching
`1,674 x 17,259` measured genes. I then pulled all focal rows for the most
relevant visible analogs with the following Arrow filter:

```python
flt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(analog_targets)
)
```

Visible VAP paralogs were not available: `Vapa` was absent from the supplied
training count table. Several other textbook ER-contact or ALS genes that would
have been direct comparators were also absent, including `Mfn1`, `Mfn2`, `Fus`,
and `C9orf72`. The decision therefore rests on indirect contrasts.

## `Vapb`

### Visible training analogs and counterexamples

| training perturbation | observed `n_degs` in 151 | focal expression-pattern evidence | interpretation for `Vapb` |
|---|---:|---|---|
| `Tardbp` | 210 | Strong signature headed by `Ppp6c`, target `Tardbp`, `Gabpa`, `Usp15`, `Fam135a`, `Brms1l`, and `Uggt2`; July corpus describes a recurrent secretory/ER-lysosomal trafficking arm. | A disease-axis counterexample. TDP-43 loss can secondarily stress ER and trafficking programs, but it is an RNA-binding autoregulatory perturbation, not loss of an ER FFAT docking protein. |
| `Atxn2` | 8 | The eight FDR 0.05 genes were `Syt7`, `Srsf11`, `Coro6`, `Crmp1`, `Tspoap1`, `Rsrp1`, `Sncb`, and `Cspg5`; the July corpus notes that TDP-43/stress-granule and UPR/ISR markers were not robustly induced. | A closer ALS modifier than most genes but still weak. Its compact, non-UPR 151 response argues against making every ALS-linked cytoplasmic/ER-contact factor a broad `Tardbp`-like hit. |
| `Vcp` | 2 | Only `Rasgef1b` up and `Nsmf` down passed FDR 0.05 in 151; the corpus reports no canonical UPR, heat-shock, p62/LC3, lysosomal-cathepsin, or TDP-43 RNA program at FDR 0.10. | A buffered proteostasis/ERAD counterexample. Even an essential p97 perturbation did not create a broad survivor-state transcriptome in young 151 neurons. |
| `Sqstm1` | 1 | Only the self transcript `Sqstm1` passed FDR 0.05 in 151; no broad NRF2, autophagy, lysosomal, UPR, or ISR program was detected in the corpus. | Basal p62 loss is close to ALS/autophagy stress biology yet nearly silent at this endpoint. |
| `Tmem106b` | 1 | Only target `Tmem106b` passed FDR 0.05 in 151; the corpus reports absence of canonical lysosomal, TFEB/MiT, autophagy, ISR, and UPR markers. | Lysosomal trafficking perturbation can have a protein/organelle phenotype without a broad 151 nuclear-RNA footprint. |
| `Chmp4b` | 0 | No FDR 0.05 genes in 151; minimum adjusted p-value 0.174 among 17,259 focal genes. | ESCRT/autophagy cargo sorting is an indirect membrane-trafficking comparison and was flat in the focal class. |
| `Osbpl2` | 0 | No FDR 0.05 genes in 151; minimum adjusted p-value 0.411. July corpus found no sterol/SREBF or autophagy RNA program across sampled neurons. | ORP-family lipid transport is one of the few represented FFAT/VAP-adjacent lipid themes and was transcriptionally silent. |
| `Vps13a`, `Vps13b`, `Vps13c` | 0, 0, 0 | No FDR 0.05 genes in 151; minimum adjusted p-values were 0.896, 0.374, and 0.484. | VPS13 contact-site lipid transport is a broad mechanistic cousin but not a VAPB obligate complex; these nulls support a low baseline for partial acute contact-site perturbations. |
| `Atp2a2` | 187 | Large 151 UPR/ISR-like induction with `Ddit3`, `Xbp1`, `Herpud1`, `Hspa5`, amino-acid-stress genes, and many additional calls. | Positive control for a directly ER-stressing perturbation. The assay can detect ER stress in 151, so a zero prediction for `Vapb` is not because UPR transcripts are invisible. |
| `Rab7` | 501 | Broad lysosomal/endosomal response with `Atp6v1b2`, `Ptgds`, `Dpp7`, `Scpep1`, `Dusp1`, `Insig1`, and other genes. | Positive control showing that endolysosomal trafficking can be visible when the perturbed node is a stronger limiting regulator. |

### Biological transfer

VAPB is a tail-anchored endoplasmic-reticulum membrane protein that, like
VAPA, binds FFAT-motif proteins to organize ER contacts with Golgi, endosome,
mitochondrial, and plasma-membrane membranes. The acute intervention here is a
sparse CRISPR loss-of-function starting at P16, not a germline null and not a
dominant VAPB P56S ALS8 allele that can aggregate and trap VAP-family proteins.
The causal chain I used was therefore:

`Vapb` editing -> partial loss of one ER FFAT adaptor -> altered lipid-transfer
or ER-mitochondria contact efficiency only where VAPA and alternative adaptors
do not compensate -> possible organelle stress in recovered postmitotic
neurons -> FDR-level nuclear RNA changes in the 151 survivor population.

That chain has two weak links for a broad DEG response. First, VAPA/VAPB have
overlapping ER-contact functions, so a `Vapb` single-gene knockout should often
leave enough VAP activity for basal lipid transfer. Second, the strong human
VAPB literature is dominated by ALS8 missense/proteinopathy mechanisms; those
do not imply that partial wild-type `Vapb` loss in otherwise unstressed juvenile
thalamic glutamatergic neurons will trigger a TDP-43-like or ATXN2-like
transcriptome. The visible perturbations agree with that expectation: basal
loss of several autophagy, lysosomal, FFAT-adjacent lipid, and contact-site
genes sits at 0 to 2 DEGs in this exact focal cell group, while the large
responses come from more direct ER calcium, endosomal, RNA-binding, or
proteasome/UFMylation perturbations.

I therefore predict a true endpoint at the zero boundary:

| held-out target | predicted `n_degs` |
|---|---:|
| Vapb | 0 |

## Limits and extrapolation

The prediction is extrapolative because the best paralog, `Vapa`, is not a
visible training perturbation, and no supplied target directly removes both
VAPA and VAPB. snRNA-seq also cannot measure lipid flux, ER-mitochondria
calcium transfer, FFAT-partner recruitment, protein aggregation, or
pre-harvest loss of vulnerable edited cells. A low DEG count for `Vapb` would
mean only that recovered 151 nuclei did not mount a large FDR 0.05 RNA program;
it would not rule out a membrane-contact phenotype. Conversely, I did not
promote `Vapb` toward `Tardbp`, `Rab7`, or `Atp2a2` because those are stronger
or different causal interventions, and the visible weak `Vcp`, `Sqstm1`,
`Tmem106b`, `Chmp4b`, `Osbpl2`, and VPS13-family perturbations show that
membership in trafficking, lysosomal, contact-site, or ALS biology alone is
not sufficient for a broad 151 transcriptional response.
