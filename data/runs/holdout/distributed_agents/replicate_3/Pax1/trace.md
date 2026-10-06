# Prediction trace

## Question and interpretation

The requested readout is the integer number of genes with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after each held-out
acute AAV-CRISPR loss-of-function perturbation in the focal cell group
`151 TH Prkcd Grin2c Glut`.

The manifest for this run contains one target:

| target | status in supplied training data |
|---|---|
| Pax1 | absent from `training_de_all_cell_groups.parquet` and absent from `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` |

I treated the task as a point prediction for this exact Perturb-seq assay, not
as a prediction of germline knockout phenotypes, conditional embryonic loss, or
PAX1 biological importance in its endogenous developmental tissues.

## Sources used

- `training_de_all_cell_groups.parquet`: focal-cell differential-expression
  signatures for non-held-out perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed training
  `n_degs` values for the same cell group.
- `166_Pax1.csv`: requested held-out target order.
- Distributed Agents corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`: internal corpus claims over the
  same Perturb-seq knowledge layer. The corpus contained no direct Pax1
  findings, but it did contain claims summarizing Pax2/Pax8/Otx/Pitx/En,
  Pax3/Pax6/Pax7, and HOX/PBX/MEIS behavior in the postnatal neuronal assay.
- Distributed Agents runtime `profile_compare`/`profile_inspect`: signed profile
  comparison of Pax2, Pax3, Pax4, Pax6, Pax7, and Pax8 in the focal cell group.
- PubMed/NCBI literature for external Pax biology, especially the axial
  skeleton/sclerotome role of Pax1 and vertebrate Pax-family developmental
  context. Mechanistic citations used below are Ando et al. 2011,
  DOI `10.1016/j.mod.2010.11.005`; Nakamichi and Asahara 2020,
  DOI `10.1002/jsp2.1081`, PMID `32211592`; Ushiki et al. 2024,
  DOI `10.1016/j.celrep.2024.113907`, PMID `38461417`; and
  Monsoro-Burq 2015, DOI `10.1016/j.semcdb.2015.09.015`, PMID `26410165`.

## Local computations

The focal group contains 28,891,566 DE rows: 1,674 training perturbations times
17,259 measured genes. Across those 1,674 perturbations, the training endpoint
was strongly zero-inflated: 1,205 targets had `n_degs = 0`; 1,512 had at most
2 DEGs; only 42 had more than 100.

For biologically nominated analogs and counterexamples, I queried the parquet
with the focal cell group fixed and counted significant rows per training
target, for example:

```sql
select gene_target,
       count(*) as measured,
       sum(pvals_adj < 0.05) as n_sig,
       min(pvals_adj) as min_adj,
       min(n_pert_matched) as n_pert_matched
from read_parquet('training_de_all_cell_groups.parquet')
where group_name = '151 TH Prkcd Grin2c Glut'
  and gene_target in (...)
group by gene_target
order by gene_target
```

Every one of the closest assayed Pax-family comparators had no significant
features in the focal cells:

| training perturbation | observed `n_degs` | focal signature evidence |
|---|---:|---|
| Pax2 | 0 | 17,259 genes tested, min adjusted p = 0.936979 |
| Pax3 | 0 | 17,259 genes tested, min adjusted p = 1.000000 |
| Pax4 | 0 | 17,259 genes tested, min adjusted p = 1.000000 |
| Pax6 | 0 | 17,259 genes tested, min adjusted p = 1.000000 |
| Pax7 | 0 | 17,259 genes tested, min adjusted p = 1.000000 |
| Pax8 | 0 | 17,259 genes tested, min adjusted p = 1.000000 |

The runtime profile comparison reached the same conclusion from the full
signed profiles: Pax2, Pax3, Pax4, Pax6, Pax7, and Pax8 all had
`response_activity_status = no_significant_features` in the
`151 TH Prkcd Grin2c Glut` profile. Their largest apparent log-fold changes
were high-magnitude, non-significant tail calls with adjusted p-values of 1,
which I treated as sparse/noisy tail behavior rather than true shared PAX
biology.

I also checked nearby developmental patterning factors and possible
counterexamples in the same focal cell group:

| training perturbation set | observed `n_degs` in focal cells | reason for comparison |
|---|---:|---|
| Pbx1, Pbx3 | 0, 0 | TALE cofactors; a test for homeobox/cofactor developmental programs in the same assay |
| Meis1, Meis2 | 0, 0 | additional TALE developmental cofactors |
| Six3, Six5 | 0, 0 | developmental transcription factors around pharyngeal/craniofacial programs |
| Gli1, Gli2 | 0, 0 | SHH-pathway transcriptional effectors; SHH regulates sclerotome Pax1 during axial development |
| Hoxa1, Hoxa3, Hoxa13, Hoxb8, Hoxd10, Hoxd13 | all 0 | axial/anterior-posterior embryonic patterning TFs |
| Tbx1, Tbx2, Tbx3 | 0, 0, 0 | embryonic patterning TFs, including pharyngeal-region biology for Tbx1 |
| Foxa2, Foxp2 | 0, 0 | neuronal/developmental TF counterexamples in the same broad TF class |

The Distributed Agents corpus corroborated that the Pax-family null was not just a
focal-cell accident from a single paralog: claim `6bab61c7a1bdcf2a7ef2`
summarized that represented Pax3/Pax6/Pax7 perturbations were sparse or null
and not transcriptionally interchangeable in postnatal neuronal nuclei; claim
`a74e194700044572fe96` summarized that Pax2/Pax8/Otx/Pitx/En developmental
regulators did not recover canonical thyroid, retinal, Pax/Otx, or
midbrain-hindbrain programs in sampled postnatal neuronal groups; and claim
`000706d189e9650b75ed` summarized flat or near-zero HOX and TALE/PBX/MEIS
surfaces rather than a shared postnatal neuronal homeobox module.

## Pax1 reasoning

Pax1 is a paired-box transcription factor with well-established roles in
paraxial mesoderm, sclerotome, vertebral/intervertebral-disc development, and
other embryonic patterning contexts. Floor-plate/notochord signaling induces
sclerotome programs including Pax1 during axial-skeleton development
(Ando et al. 2011, DOI `10.1016/j.mod.2010.11.005`), Pax1 is part of the
transcription-factor network discussed for intervertebral-disc development
(Nakamichi and Asahara 2020, DOI `10.1002/jsp2.1081`), and deleting Pax1
skeletal regulatory elements perturbs the mouse tail/axial skeleton
(Ushiki et al. 2024, DOI `10.1016/j.celrep.2024.113907`). PAX factors more
broadly are developmental patterning regulators with paralog-specific tissue
uses rather than one generic postnatal neuronal module (Monsoro-Burq 2015,
DOI `10.1016/j.semcdb.2015.09.015`).

The mechanistically closest directly assayed genes in this dataset are Pax2,
Pax3, Pax4, Pax6, Pax7, and Pax8. None caused even a single FDR-significant
gene in `151 TH Prkcd Grin2c Glut`, despite 138-251 perturbed nuclei per Pax
contrast and 23,679 matched controls. Pax1 is not expected to be more central
than Pax6/Pax2/Pax8 in a postnatal thalamic glutamatergic neuron; its canonical
axial-skeletal and pharyngeal developmental functions are more off-context for
NeuN-positive P37-P44 neurons than the assayed Pax genes with known neural
roles. The SHH/GLI and HOX/TALE checks did not reveal an active axial
developmental module in these cells either.

Therefore I predicted that acute mosaic Pax1 loss will not produce any genes
passing FDR 0.05 in this focal cell group.

## Final prediction

| target | predicted `n_degs` |
|---|---:|
| Pax1 | 0 |

## Limits

- Pax1 and Pax9 were both absent from the training expression signatures, so
  the call is an extrapolation from assayed paralogs and from off-context
  developmental-pathway genes rather than a direct Pax1 nearest-neighbor
  transfer.
- The assay perturbs postnatal NeuN-positive nuclei only partially at the RNA
  level. A zero prediction does not mean Pax1 has no developmental function or
  that a germline or embryonic deletion would be weak.
- The high-magnitude log-fold-change tails in the null Pax profiles were not
  biologically interpreted because their adjusted p-values were 0.94-1.00 and
  they did not recur as significant signed features across Pax paralogs.
