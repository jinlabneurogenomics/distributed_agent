# Sry DEG-count prediction

## Question and endpoint

The requested held-out perturbation list contains one target, `Sry`, and the required endpoint is the integer number of FDR-significant measured genes in `151 TH Prkcd Grin2c Glut` after acute P16 AAV-CRISPR loss of function and P37-P44 snRNA-seq. I treated `n_degs` as the assay-specific breadth endpoint defined in the task: the count of measured genes with `pvals_adj < 0.05` in the Wilcoxon contrast against the matched non-targeting controls. The `Sry` rows themselves are intentionally absent from both supplied training inputs, so this is a transfer prediction from non-held-out perturbations.

The focal atlas name is interpreted as thalamic `Prkcd`/`Grin2c` glutamatergic neurons. I did not interpret `TH` as tyrosine hydroxylase.

## Sources used

- The declared training endpoint table, `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, was the direct source of observed DEG burdens for the 1,674 non-held-out perturbations in the focal cell group.
- The declared parquet, `training differential-expression dataset`, was queried directly for focal signatures, all-cell-group signatures of selected analogs, matched focal nucleus counts, and confirmation that `Sry` is absent as a perturbation and as a measured focal transcript.
- The run-local PerturbAI July corpus release `perturbai-july-260713-sourceguard-1773-v1` was used as a same-experiment interpreted layer for SOX and dopaminergic-lineage perturbations. Its Findings are not independent replication of the parquet; they summarize the same experiment.
- PubMed literature was used for external mechanism priors: SRY/SOX9 sex-determination biology from Sekido and Lovell-Badge 2008, DOI `10.1016/j.tig.2008.10.008`; SRY/SF1 activation of a Sox9 enhancer from Sekido and Lovell-Badge 2008, DOI `10.1038/nature06944`; SRY as a SoxA/HMG transcription factor and embryonic gonadal switch from Sekido 2009, DOI `10.1016/j.biocel.2009.12.005`; and adult male Sry expression in substantia nigra tyrosine-hydroxylase-positive neurons from Dewing et al. 2006, DOI `10.1016/j.cub.2006.01.017`. Tao et al. 2011, DOI `10.1002/jnr.22729`, was used as weaker cell-culture support that SRY can modulate dopamine-neuron oxidative-stress and PD-related expression programs.

## Dataset calculations

I first inspected the supplied target list and found exactly one requested target:

```text
Sry
```

I then summarized the focal training counts. The endpoint is very sparse in this class: 1,205/1,674 training perturbations had `n_degs = 0`; the median was 0, the 75th percentile was 1, the 90th percentile was 2, and even the nonzero median was 1. This calibration makes a zero prediction plausible unless a held-out gene has a close analog with a robust focal response.

The narrow parquet aggregation was:

```sql
SELECT gene_target,
       count(*) AS n_rows,
       sum(CAST(pvals_adj < 0.05 AS INTEGER)) AS n_degs,
       any_value(n_pert_matched) AS n_pert_matched,
       any_value(n_ctrl_matched) AS n_ctrl_matched
FROM parquet_scan(?)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

That query confirmed all focal signatures had 17,259 measured genes and the same 23,679 matched controls. It also confirmed `Sry` is completely held out (`0` rows with `gene_target = 'Sry'`) and is not itself a measured gene in the focal training parquet rows (`0` rows with `group_name = '151 TH Prkcd Grin2c Glut' AND names = 'Sry'`).

## Target-specific reasoning

### Sry

**Closest in-dataset HMG/SOX analogs.** `Sry` encodes the founding HMG-box SOX transcription factor; in canonical development its best-established pathway is an early gonadal, SF1-cooperative activation of `Sox9`, not a postnatal neuronal program. The non-held-out SOX-family training perturbations were almost all silent in `151 TH Prkcd Grin2c Glut`:

| comparator | focal `n_degs` | matched perturbed nuclei | most relevant focal signature evidence |
|---|---:|---:|---|
| `Sox2` | 2 | 173 | `Tnnt1` down, adjusted `p = 2.77e-6`; `Stam` down, adjusted `p = 1.47e-2` |
| `Sox5` | 2 | 184 | `Dgkh` up, adjusted `p = 5.37e-4`; `Tnnt1` up, adjusted `p = 2.84e-2` |
| `Sox4` | 0 | 230 | no focal gene below FDR 0.05 |
| `Sox9` | 0 | 252 | no focal gene below FDR 0.05 |
| `Sox10` | 0 | 226 | no focal gene below FDR 0.05 |
| `Sox11` | 0 | 324 | no focal gene below FDR 0.05 |
| `Sox17` | 0 | 276 | no focal gene below FDR 0.05 |
| `Sox18` | 0 | 289 | no focal gene below FDR 0.05 |

The same-experiment July corpus summarized the two-gene `Sox2` and `Sox5` signals as extremely narrow thalamic responses and explicitly reported that the represented SOX-family perturbations did not phenocopy one another. In the direct parquet aggregation, `Sox2` and `Sox5` had nonzero DEGs in only this one class, with a maximum of 2 DEGs across all measured classes; `Sox4`, `Sox10`, `Sox11`, `Sox17`, and `Sox18` had zero FDR-significant genes in every measured class. This makes generic HMG/SOX DNA-binding similarity a weak transfer basis.

`Sox9` is the downstream embryonic Sertoli-cell effector most tightly connected to Sry biology, but its acute postnatal neuronal perturbation had `0` DEGs in the focal class. This is the most direct in-dataset counterexample to carrying the canonical Sry-Sox9 gonadal axis into thalamic postmitotic neurons.

**Known adult neuronal activity of Sry.** Dewing et al. showed `Sry` expression in adult male substantia nigra TH-positive dopaminergic neurons and a reduction of tyrosine hydroxylase after local rat substantia nigra Sry knockdown. I considered whether this made the held-out `Sry` perturbation analogous to dopaminergic-lineage or dopaminergic-maintenance factors. In the training data those factors did not produce a focal thalamic glutamatergic response:

| comparator | focal `n_degs` | matched perturbed nuclei | relationship to Sry |
|---|---:|---:|---|
| `Pitx3` | 0 | 184 | mDA maintenance regulator downstream/parallel to TH-positive identity |
| `Foxa2` | 0 | 213 | mDA developmental determinant |
| `Lmx1b` | 0 | 271 | mDA developmental/maintenance determinant |
| `En1` | 0 | 242 | mDA survival and maintenance factor |
| `Nr4a1` | 0 | not used for count transfer | NUR-family comparator in dopamine-neuron regulatory space |
| `Nr4a3` | 0 | not used for count transfer | NUR-family comparator; only one DEG in one non-focal group |

The PerturbAI corpus also reported that `Pitx3` was FDR-flat across the 23-cell-group taxonomy and did not recover the expected dopaminergic terminal differentiation program even in the `215 MB Dopa` group. Thus the best-supported adult neural action of Sry maps to a different neuronal lineage, and analogous perturbations of represented dopamine-lineage transcription factors do not yield a robust postnatal survivor-state transcriptional signature in this focal thalamic glutamatergic population.

**Other sex-linked analogs.** The training panel did not contain close Y-chromosome homologs such as `Ddx3y`, `Kdm5d`, `Uty`, or `Eif2s3y`, so I could not transfer from male-specific Y paralogs in-dataset. The weaker X-linked comparators did not look Sry-like mechanistically: `Ddx3x` produced only 8 DEGs in the focal class and the corpus tied that response to synaptic/neurite and `Ctnnb1` convergence, while `Kdm5c` produced 18 DEGs dominated by cryptic or lineage-atypical genes. These are not HMG/SOX or dopamine-lineage responses, so I treated them as loose counterexamples rather than close supports for a positive call.

## Causal transfer model and prediction

The causal chain for an `Sry` perturbation is:

1. **Intervention:** P16 AAV-CRISPR loss of the Y-linked `Sry` locus in a mosaic pool. Only male nuclei can carry the target; female nuclei lack the Y target and are an internal dilution/background for an otherwise sex-limited perturbation.
2. **Direct molecular consequence:** loss of an HMG-box transcription factor. The dominant known direct SRY transcriptional target is the gonadal `Sox9` enhancer with SF1 in embryonic Sertoli precursors, not a postnatal thalamic enhancer program.
3. **Propagation:** a possible adult neuronal consequence exists for substantia nigra dopaminergic TH regulation, but the requested class is thalamic glutamatergic. Perturbations of `Pitx3`, `Foxa2`, `Lmx1b`, and `En1` in the training set argue that this dopaminergic axis is not measurably active as a broad DEG program in the focal cells.
4. **Exposure and selection:** the target is male-specific, so any on-target cell-autonomous effect is expected to be diluted in the mixed-sex pool.
5. **Measured endpoint:** the focal class and the in-dataset SOX/dopamine analogs are heavily zero-inflated; no close comparator produces a broad FDR-supported survivor-state signature.

The zero/nonzero decision is therefore driven mostly by within-dataset evidence from the flat `Sox9`, broader SOX, and dopaminergic-lineage perturbations, with external literature limiting Sry's plausible neuronal transfer to substantia nigra dopaminergic biology. I predict no genes crossing FDR 0.05:

| target | predicted `n_degs` |
|---|---:|
| `Sry` | 0 |

## Limits

This is an extrapolation because no Y-linked Sry-family perturbation was visible in the training set and the parquet contains no held-out `Sry` signature. A very small male-only `Sry` response in the focal class could be diluted below significance, and Sry can act outside the embryonic gonad in a specific dopaminergic population. The closest screened SOX genes are not obligate SRY partners in postnatal thalamic neurons, so their zero or two-gene responses are analog evidence, not proof. The final point prediction is consequently a low-count qualitative transfer call calibrated to a zero-inflated endpoint rather than a mechanistic certainty.
