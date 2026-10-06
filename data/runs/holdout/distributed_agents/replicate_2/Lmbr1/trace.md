# Reasoning trace

## Question and resolved ambiguities

The task asks for a point prediction of `n_degs`, the number of measured genes
with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05`, for held-out
perturbations in the focal `151 TH Prkcd Grin2c Glut` population. The only
requested held-out target in
`[local file: 126_Lmbr1.csv]`
is:

| target_name |
| --- |
| Lmbr1 |

I treated `n_degs` exactly as the endpoint in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: target self-transcripts are
included if they pass `pvals_adj < 0.05`. When I mention "downstream" genes
below, I explicitly mean significant genes after excluding the perturbed target
itself.

## Sources used

- Differential-expression Parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
  I queried it directly for focal-cell rows from biologically selected
  Hedgehog/ciliary/LMBR-domain training perturbations.
- Training DEG counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  These gave the exact focal-cell endpoint for represented non-held-out
  perturbations.
- Requested-target manifest:
  `126_Lmbr1.csv`.
- Same-experiment Distributed Agents corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`. The corpus had no `Lmbr1` card,
  so I used its cards for relevant represented Hedgehog and ciliary targets:
  `Cdon`, `Gli1`, `Gli2`, `Gpr161`, `Ift43`, `Ift81`, `Ift88`, `Kif3b`,
  `Ptch1`, `Ptch2`, `Smo`, and `Lmbrd1`.
- PubMed literature for the external mechanism of the `Lmbr1` locus.

Key external references:

- Lettice et al. 2003, PMID: 12837695, DOI: `10.1093/hmg/ddg180`: identified
  the ZRS long-range limb enhancer for `Shh` within intron 5 of `Lmbr1`; ZRS
  point mutations drive ectopic anterior `Shh` expression in the limb bud and
  preaxial polydactyly.
- Xu et al. 2019, PMID: 31395945, DOI: `10.1038/s41436-019-0626-7`: a human
  ZRS variant produced preaxial polydactyly through enhanced `SHH` expression in
  a developing-limb model.
- Ushiki et al. 2021, PMID: 33863876, DOI: `10.1038/s41467-021-22470-z`:
  acheiropodia-associated noncoding deletions around ZRS in the human `LMBR1`
  locus disrupt CTCF/RAD21-mediated contacts between ZRS and the `SHH`
  promoter.
- Tseng et al. 2013, PMID: 24078630, DOI: `10.1074/jbc.M113.479527`, and
  Buers et al. 2016, PMID: 27061115, DOI: `10.1111/jcmm.12844`: define
  `Lmbrd1`/LMBD1 as an LMBR-domain, multi-pass membrane protein with cobalamin
  and insulin-receptor-trafficking biology. This makes `Lmbrd1` the nearest
  named LMBR-domain training perturbation, but only a weak functional analog for
  `Lmbr1`.

## Computational checks

The training-count CSV was extremely sparse in this focal cell group:

| count class | training perturbations |
| --- | ---: |
| `n_degs = 0` | 1205 |
| `1 <= n_degs < 10` | 363 |
| `10 <= n_degs < 100` | 63 |
| `n_degs >= 100` | 43 |

I then queried the raw DE Parquet for mechanistic comparators. The non-obvious
operation was the Parquet scan over the focal cell type only:

```sql
SELECT gene_target,
       COUNT(*) FILTER (WHERE pvals_adj < 0.05) AS n_fdr05,
       COUNT(*) FILTER (WHERE pvals_adj < 0.10) AS n_fdr10,
       MIN(CASE WHEN names='Lmbr1' THEN pvals_adj END) AS lmbr1_fdr,
       MIN(CASE WHEN names='Shh' THEN pvals_adj END) AS shh_fdr,
       MIN(CASE WHEN names='Gli1' THEN pvals_adj END) AS gli1_fdr,
       MIN(CASE WHEN names='Ptch1' THEN pvals_adj END) AS ptch1_fdr,
       MIN(CASE WHEN names='Ptch2' THEN pvals_adj END) AS ptch2_fdr,
       MIN(CASE WHEN names='Hhip' THEN pvals_adj END) AS hhip_fdr
FROM read_parquet(...)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

Exact focal-cell training counts and expression evidence for the analogs were:

| training perturbation | observed `n_degs` in `151 TH Prkcd Grin2c Glut` | focal expression-pattern evidence |
| --- | ---: | --- |
| `Lmbrd1` | 1 | The single FDR<0.05 row was `Lmbrd1` itself, logFC -0.606, FDR 0.00338; `Shh`, `Gli1`, `Ptch1`, `Ptch2`, `Hhip`, and `Lmbr1` all had FDR 1.0. |
| `Ptch1` | 0 | 159 perturbed nuclei; no gene passed FDR<0.05 or FDR<0.10; `Shh`, `Gli1`, `Ptch1`, `Ptch2`, `Hhip`, and `Lmbr1` all had FDR 1.0. |
| `Ptch2` | 0 | 192 perturbed nuclei; no gene passed FDR<0.05 or FDR<0.10; all queried canonical Hedgehog reporter rows had FDR 1.0. |
| `Smo` | 0 | 284 perturbed nuclei; no gene passed FDR<0.05 or FDR<0.10; all queried canonical Hedgehog reporter rows had FDR 1.0. |
| `Gli1` | 0 | 234 perturbed nuclei; no gene passed FDR<0.05 or FDR<0.10; all queried canonical Hedgehog reporter rows had FDR 1.0. |
| `Gli2` | 0 | 205 perturbed nuclei; no gene passed FDR<0.05 or FDR<0.10; all queried canonical Hedgehog reporter rows had FDR 1.0. |
| `Cdon` | 0 | 190 perturbed nuclei; no gene passed FDR<0.05 or FDR<0.10; all queried canonical Hedgehog reporter rows had FDR 1.0. |
| `Gpr161` | 0 | Training count was zero; the Distributed Agents corpus labels it a pan-measured non-responder and a Hedgehog/GLI uncoupling in juvenile NeuN-enriched neurons. |
| `Kif3b` | 0 | Training count was zero; the Distributed Agents corpus labels it a pan-neuronal transcriptomic null and reports absent Hedgehog and neuronal ciliary-marker responses. |
| `Ift43` | 0 | 328 perturbed nuclei; no focal gene passed FDR<0.05 or FDR<0.10. The corpus reports no canonical Hedgehog/GLI or neuronal ciliary-GPCR panel after `Ift43` perturbation. |
| `Ift81` | 0 | 152 perturbed nuclei; no focal gene passed FDR<0.05 or FDR<0.10. The corpus reports 0/22 measured groups with FDR<0.10 downstream genes. |
| `Ift88` | 0 | 143 perturbed nuclei; no focal gene passed FDR<0.05 or FDR<0.10. The corpus reports that the one adjusted `Ift88` hit elsewhere was a single `155 MB Glut` `Pcsk1n` upregulation. |
| `Rfx3` | 0 | Training count was zero; useful as another represented ciliary transcriptional regulator with no focal response. |
| `Mmaa` | 0 | Training count was zero; useful as a cobalamin-pathway counterpoint to `Lmbrd1`. |

As counterexamples for scale, the same focal analysis readily detects broad
signatures when the perturbation couples to this cell state: the top training
counts include `Uba5` 2677, `Tpr` 1768, `Sin3a` 1433, `Rnpc3` 868, and
`Zbtb7a` 841 DEGs. `Kmt2a`, a chromatin regulator with developmental roles, had
24 DEGs. Thus the zero calls for the Hedgehog/ciliary set are not a global
failure of the cell group to produce DEGs.

## Target-specific reasoning

### Lmbr1

`Lmbr1` was held out from the DE Parquet and from the focal training-count CSV,
and the Distributed Agents same-experiment corpus had no target-specific `Lmbr1`
finding. The prediction therefore had to be transferred.

The best-known biology of the locus is regulatory, not an acute coding response:
ZRS, a long-range limb enhancer for `Shh`, sits in intron 5 of `Lmbr1` and acts
over roughly a megabase in developing limb buds. Human and mouse limb
malformations at this locus are driven by ZRS point variants, noncoding
deletions around ZRS, and altered `SHH` enhancer-promoter communication
(Lettice et al. 2003; Xu et al. 2019; Ushiki et al. 2021). The experiment in
question used postnatal AAV-CRISPR loss of gene coding function in sparse
postmitotic NeuN+ neurons, not engineered limb-enhancer alleles in embryonic
limb mesenchyme. It would not be expected to reproduce an ectopic limb-bud
`Shh` enhancer phenotype.

Direct same-experiment Hedgehog comparators point the same way. Loss of the
canonical receptor/transducer/effectors `Ptch1`, `Ptch2`, `Smo`, `Gli1`, and
`Gli2` each produced 0 focal DEGs at FDR<0.05; the co-receptor `Cdon`, ciliary
Hedgehog/cilia genes `Gpr161`, `Kif3b`, `Ift43`, `Ift81`, `Ift88`, and `Rfx3`
were also zero in the focal group. In the raw rows for the direct `Ptch1`,
`Ptch2`, `Smo`, `Gli1`, `Gli2`, and `Cdon` comparisons, the canonical reporters
I checked - `Shh`, `Gli1`, `Ptch1`, `Ptch2`, and `Hhip` - all had adjusted
P values of 1.0. The Distributed Agents corpus independently summarizes these training
perturbations as buffered/null or singleton responders with no recovered
canonical Hedgehog/GLI module.

The closest represented LMBR-domain target, `Lmbrd1`, is at most a structural
family comparator because its known function is lysosomal cobalamin handling
and receptor trafficking rather than the `Lmbr1` ZRS enhancer. Even so, it was
also a practical null in the focal group: its single focal DEG was its own RNA,
with no downstream genes below FDR 0.05 or 0.10. That weak family comparator
does not supply evidence for a broad `Lmbr1` RNA program.

Taken together, I predict no FDR<0.05 genes for `Lmbr1` in
`151 TH Prkcd Grin2c Glut`: the relevant in-dataset pathway nodes are all
silent in the focal cell group, the external mechanism that makes the `Lmbr1`
locus famous is a noncoding embryonic limb `Shh` enhancer mechanism, and there
is no represented analog that suggests an acute postnatal thalamic neuronal
transcriptional state.

Point prediction: `Lmbr1 = 0`.

## Limits and extrapolation

- `Lmbr1` itself was held out, so there is no direct `Lmbr1` signature, focal
  target-RNA row, perturbed-cell count, or Distributed Agents target card.
- `Shh` ligand loss was not available as a represented focal training
  perturbation; the strongest pathway transfer comes from receptors,
  transducers, GLI factors, and ciliary components.
- `Lmbrd1` is only an LMBR-domain paralog/family comparator. Its cobalamin and
  receptor-trafficking biology is not the same mechanism as the `Lmbr1`-ZRS
  locus, so its null response is supportive but not decisive.
- The assay does not measure DNA indels, SHH enhancer-promoter contacts,
  protein abundance, ciliary trafficking, or ligand secretion. A zero here
  means no expected BH-significant nuclear RNA signature among recovered
  `151 TH Prkcd Grin2c Glut` nuclei, not absence of all molecular consequences
  of editing `Lmbr1`.
