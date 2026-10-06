# Six1 held-out DEG-count prediction

## Question and resolved ambiguities

The requested endpoint is the integer number of measured genes with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after knockout of each
held-out target in `151 TH Prkcd Grin2c Glut` nuclei. The target list in
`207_Six1.csv` contains one held-out target:

```tsv
target_name
Six1
```

I interpreted `n_degs` exactly as the training CSV defines it: target rows are
not excluded unless they fail the same FDR test as any other measured gene, and
the prediction must be a single non-negative count rather than a response class
or interval. `Six1` is absent from both the training count table and the
training differential-expression parquet, so no direct `Six1` signature is
available for calibration.

## Sources used

- Input count table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Held-out manifest:
  `[local file: 207_Six1.csv]`.
- Run-local scalar calibration from the same training count table:
  `codex_runtime/pipeline/scalar_prior_calibration.json`.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`. This corpus had no bottom-up
  Claims for `Six1`, but it had Findings for the represented `Six3`, `Six5`,
  and `Dach1` perturbations.
- NCBI PubMed literature searches and PubMed metadata for `Six1`, `Eya1`,
  `Six3`, and retinal-determination/PAX-SIX-EYA-DACH biology.

## Computational checks on the supplied data

The focal training endpoint is highly zero-inflated:

- 1,674 non-held-out targets in `151 TH Prkcd Grin2c Glut`
- 1,205 targets with `n_degs = 0`
- 363 weak nonzero targets with `1 <= n_degs < 10`
- 63 medium targets with `10 <= n_degs < 100`
- 43 strong targets with `n_degs >= 100`

I used DuckDB against the parquet with column projection and
`group_name = '151 TH Prkcd Grin2c Glut'` predicates, because the full parquet
has 616,253,184 rows. For the closest available Six/Eya/Dach relatives, I
retrieved all focal rows and recomputed simple diagnostics:

```sql
select gene_target,
       count(*) filter(where pvals_adj < 0.05) as padj_lt_05,
       min(pvals_adj) as min_padj,
       min(pvals) as min_p,
       count(*) filter(where pvals < 0.01) as nominal_p_lt_01,
       count(*) filter(where abs(scores) > 3) as abs_score_gt_3
from read_parquet($training_parquet)
where group_name = '151 TH Prkcd Grin2c Glut'
  and gene_target in ('Six3','Six5','Dach1')
group by 1;
```

| training target | 151 perturbed nuclei | 151 controls | observed `n_degs` | minimum raw p | minimum BH FDR | nominal genes with raw p < 0.01 | genes with \|Wilcoxon score\| > 3 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `Dach1` | 173 | 23,679 | 0 | 6.52e-05, `Mier3` | 1.0 | 51 | 14 |
| `Six3` | 167 | 23,679 | 0 | 8.73e-05, `Rfx1` | 1.0 | 49 | 15 |
| `Six5` | 215 | 23,679 | 0 | 7.81e-05, `Mia3` | 1.0 | 74 | 23 |

Every row in each of these three focal signatures had `pvals_adj = 1.0`. Their
continuous Wilcoxon-score vectors were also mutually tiny, which argues against
a latent shared Six/Eya/Dach state hiding below the FDR threshold:

| score-vector pair in 151 | Pearson r |
| --- | ---: |
| `Dach1` vs `Six3` | 0.0164 |
| `Dach1` vs `Six5` | 0.0497 |
| `Six3` vs `Six5` | 0.0066 |

I also checked the focal training count table for a broader set of homeobox or
craniofacial/anterior developmental comparators. `Pax2`, `Pax3`, `Pax4`,
`Pax6`, `Pax7`, `Pax8`, `Otx2`, `Pitx2`, `Pitx3`, `Lhx3`, `Lhx4`, `Pou1f1`,
`Pou2f1`, `Pou2f2`, `Pou3f3`, `Pou3f4`, `Pou4f3`, `Pou5f1`, `Pou6f2`,
`Sall1`, `Sall4`, `Dlx3`, `Dlx6`, all assayed `Hox*`, and all assayed `Tbx*`
targets were zero in `151 TH Prkcd Grin2c Glut`. This was used only as weak
context: it says many lineage patterning TFs are buffered in this focal cell
group, but the decisive comparators are the Six/Eya/Dach-neighborhood genes.

## Same-experiment analogs

### `Six3`: close Six-family counterexample

`Six3` is a Six homeobox paralog in the training data and had `n_degs = 0` in
the held-out focal cell group, with 167 perturbed and 23,679 control nuclei. It
is not a perfect analog because SIX3 is best known for anterior
neuroectoderm/forebrain biology, whereas SIX1/SIX4 act prominently in cranial
placodes. It is still a useful counterexample because it tests whether a Six
homeobox TF can drive a broad postnatal neuronal transcriptional state in this
assay.

The Distributed Agents same-experiment corpus reports that `Six3` loss produced only one
robust downstream transcript across the experiment, `Slc6a6` in `007 L2-3 IT
CTX Glut`; represented SIX/homeobox and Wnt/BMP/SHH/FGF comparators failed to
phenocopy that singleton; and its whole-parquet Wilcoxon-score neighbors were
near zero, with top positive Pearson correlations around 0.03-0.04. The corpus
explicitly contrasts this result with literature showing that SIX3 represses
Wnt during anterior neuroectoderm formation and directly regulates `Shh` in the
ventral forebrain: Lagutin et al. 2003, DOI `10.1101/gad.1059403`; Geng et al.
2008, DOI `10.1016/j.devcel.2008.07.003`; Jeong et al. 2008, DOI
`10.1038/ng.230`.

For `Six1`, the implication is that even a Six factor with strong embryonic
forebrain patterning literature was nearly silent after P16 mosaic loss of
function in recovered juvenile neurons. That makes it less plausible that
`Six1` would produce a thalamic signature solely because it is a developmental
TF.

### `Six5`: assayed BOR/Six-Eya-neighborhood family member

`Six5` is an assayed SIX-family member in the BOR/Six-Eya neighborhood of
`Six1`. It had `n_degs = 0` in `151 TH Prkcd Grin2c Glut` with 215 perturbed
and 23,679 control nuclei. In the same-experiment corpus, `Six5` is a
pan-neuronal transcriptional null: all 23 measured neuronal groups had zero
downstream genes at FDR < 0.10, and its global response surface contained
388,046 rows with no downstream FDR < 0.10 calls after excluding the target
transcript.

That global null is directly relevant because SIX5 shares the Six-family
DNA-binding/Six-domain architecture and is a named branchio-oto-renal
candidate alongside EYA1 and SIX1, but it did not activate a cryptic Six-family
or MEF3/ARE response in this postmitotic mouse neuron assay. Klesert et al.
2000 connected Six5 loss primarily to cataract in mice rather than broad brain
transcriptional phenotypes, DOI `10.1038/75490`.

### `Dach1`: retinal-determination-network cofactor/counterexample

`Dach1`, an assayed Dach family member from the Pax/Six/Eya/Dach retinal
determination network, had `n_degs = 0` in the focal cell group with 173
perturbed and 23,679 control nuclei. The same-experiment corpus reports one
robust `Dach1` downstream transcript, `Ppdpf`, confined to a different cell
group, `017 CA3 CA2-FC DG Glut`, and no strong positive or negative
whole-transcriptome neighbor in the complete parquet: its strongest
non-control whole-surface cosines were only about +0.034 and -0.023. Those
nearest data-driven neighbors did not reproduce the CA3 `Ppdpf` edge.

This is a useful negative comparison for `Six1` because SIX, EYA, and DACH
proteins can form CREB-binding-protein-associated transcriptional complexes in
promoter assays, as shown by Ikeda et al. 2002, DOI
`10.1128/MCB.22.19.6759-6766.2002`, and the RDGN integrates with Wnt, Notch,
Hedgehog, EGFR, and TGF-beta programs in a context-specific way, as reviewed
by Silver and Rebay 2005, DOI `10.1242/dev.01539`. The training data show that
this developmental module is mostly absent from the acute postnatal neuronal
readout rather than being a broad expression program in `151 TH Prkcd Grin2c
Glut`.

## External `Six1` biology

`Six1` encodes a DNA-binding homeobox transcription factor with a conserved Six
domain used for protein-protein interactions. In mammals, the best-supported
roles of `Six1` and `Eya1` are developmental: branchio-oto-renal and
inner-ear/otic programs, kidney, craniofacial, and cranial placode induction.
Kochhar et al. 2007 reviewed the human BOR regulatory network involving `EYA1`
and `SIX1`, DOI `10.1002/ajmg.a.31561`, PMID `17238186`. Wong et al. 2012
reviewed the mammalian inner-ear EYA1-SIX1 transcriptional activation complex,
including proliferation, survival, and neurosensory fate induction, DOI
`10.1016/j.heares.2012.09.009`, PMID `23104013`. Sato et al. 2010 mapped
mouse `Six1` expression to the conserved embryonic pre-placodal region marked
by `Six1/4` and `Eya1/2`, DOI `10.1016/j.ydbio.2010.04.029`, PMID `20471971`.

Those mechanisms point to cranial placodes, sensory-neuronal induction, and
embryonic morphogenesis rather than to maintenance of transcriptomes in
already postmitotic P37-P44 thalamic glutamatergic neurons. The relevant Eya
cofactors (`Eya1`, `Eya2`, `Eya3`, `Eya4`) and closer `Six1` branch paralogs
`Six2`, `Six4`, and `Six6` were not in the focal training count table, so I
could not use them as direct same-cell anchors. However, the represented
`Six3`, `Six5`, and `Dach1` perturbations are exactly the right counterexamples
for asking whether the Six/Eya/Dach network is active in this assay.

## Target-specific prediction

### Six1 -> predicted `n_degs = 0`

Evidence supporting zero:

- The focal training set is zero-heavy, with 72.0% of non-held-out
  perturbations at zero.
- The most relevant assayed relatives in the Six/Eya/Dach neighborhood are
  `Six3`, `Six5`, and `Dach1`; all three had `n_degs = 0` in `151 TH Prkcd
  Grin2c Glut`.
- `Six3`, `Six5`, and `Dach1` each had >160 perturbed nuclei in the focal
  comparison, so their zero calls were not driven by the tiny 20-50-cell cases
  present elsewhere in the atlas.
- Their best raw focal p-values all BH-adjusted to 1.0, and their
  Wilcoxon-score correlations with one another were nearly zero, so there is
  no sign of a shared subthreshold Six/Eya/Dach signature in the focal cell
  group.
- Same-experiment corpus Findings generalize these negatives beyond the focal
  cell group: `Six5` was null in all 23 measured neuronal groups; `Six3` had
  only an isolated cortical `Slc6a6` edge and no convergent homeobox/Wnt-Hh
  state; `Dach1` had only a confined CA3 `Ppdpf` edge and no broad global
  neighbor.
- External literature puts `Six1` chiefly in embryonic placode/otic,
  craniofacial, renal, and neurosensory induction programs with EYA cofactors.
  Those are displaced from the P16-to-P37/P44 sparse AAV-CRISPR perturbation
  of already differentiated NeuN-positive thalamic neurons.

Evidence against a confident structural zero:

- `Six1` itself was held out, so the on-target transcript row, editing impact,
  and exact `Six1`-specific focal signature are unobserved.
- The closest `Six1` paralogs in the pre-placodal Six1/4 + Eya1/2 program,
  `Six4` and the Eya cofactors, were not available as training perturbations
  in the focal table.
- Some developmental regulators that look stage-displaced can still be active
  in `151 TH Prkcd Grin2c Glut`; for example `Ctnnb1`, `Gsk3b`, and `Tcf7l2`
  are Wnt-adjacent and have nonzero thalamic training counts in the atlas, so
  the decision cannot be made from "embryonic TF" alone.

I therefore assign `Six1` to the zero class, not merely to a low nonzero weak
class. A weak count of 1-3 would be plausible if `Six1` copied the singleton
behavior of `Six3` or `Dach1` in another cell type, but in the actual target
cell type every same-neighborhood perturbation was fully FDR-flat. The point
estimate is:

```tsv
target_name	predicted_n_degs
Six1	0
```

## Limits

This prediction is an extrapolation from paralogs and cofactors because the
`Six1` perturbation was deliberately hidden. It assumes the P16 mosaic CRISPR
loss-of-function context will buffer `Six1` in the same way it buffered
`Six3`, `Six5`, and `Dach1`; an unmeasured `Six1`-specific role in the
`TH Prkcd Grin2c Glut` state would make the estimate too low. The parquet
contains normalized single-nucleus RNA contrasts, not DNA indel rates, allele
phase, protein abundance, chromatin occupancy, embryonic lineage phenotypes,
or survival before nuclei recovery. A zero `n_degs` prediction should
therefore be read as "no genes are expected to pass this specific FDR 0.05
snRNA-seq endpoint", not as absence of SIX1 function in all contexts.
