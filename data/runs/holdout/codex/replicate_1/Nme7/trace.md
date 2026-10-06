# Nme7 direct DEG-count forecast

## Target and endpoint

- Target: `Nme7`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05` in this focal population.

The Nme7 target signature and Nme7 count were withheld. I used the declared Nme7 biology bundle, the focal training count table, the declared expression Parquet, and same-experiment corpus Claims for non-held-out ciliary training perturbations.

## Nme7 biology prior

The Nme7 bundle supports ciliary and microtubule biology, but not a strong acute postnatal thalamic RNA response:

- Exact focal-population reach is moderate: in non-target `151 TH Prkcd Grin2c Glut` nuclei, `Nme7` is detected in 10,333 of 23,679 cells, or 43.64%, with mean raw UMI 0.628 and mean log1p CP10K 0.268.
- NME7 is a kinase-active regulator associated with the gamma-tubulin ring complex and with basal-body/primary-cilium function; cultured-cell perturbations support roles in microtubule nucleation, primary-cilium assembly, and ciliary microtubule stability.
- Mouse loss evidence is developmental and ependymal/ciliary: germline Nme7-null mice have hydrocephalus and laterality phenotypes, but this does not establish a post-P16 requirement in NeuN-positive thalamic neurons.
- Functional realization by the P37-P44 harvest is unresolved. The bundle specifically finds no transferable measurement of NME7, gamma-TuRC-bound NME7, basal-body, or ciliary-pool turnover in postmitotic neurons, so a P16 edit stops new NME7 supply but does not prove that pre-existing operative pools are gone by the 21-28 day readout.

That combination makes Nme7 biologically reachable but downward-weighted for this nuclear-RNA endpoint: the assay can express the target, yet the closest direct evidence is ciliary and developmental, and the stock/latency bridge into acute postnatal thalamic neurons is uncertain.

## Task-matched ciliary training evidence

The focal training count table is sparse overall:

- 1,205 of 1,674 training perturbations have `n_degs = 0`.
- The median is 0, the 75th percentile is 1, the 90th percentile is 2, and the mean is 14.05 because a small number of perturbations have very large responses.

I then selected the available training genes most closely matching the Nme7 operation through primary cilium, IFT/dynein, transition-zone, basal-body, and ciliary Hedgehog signaling biology:

`B9d1`, `Bbs5`, `Cep290`, `Cplane1`, `Cspp1`, `Dync2h1`, `Dync2i1`, `Gli2`, `Gpr161`, `Ift43`, `Ift81`, `Ift88`, `Kif3b`, `Lztfl1`, `Ptch1`, `Rpgr`, `Rpgrip1l`, `Sclt1`, `Smo`, `Ttc21b`, `Ttc8`.

Their exact focal `n_degs` values were 20 zeros and one singleton:

- `Ttc8`: 1
- every other member of the 21-gene set: 0

The same-experiment corpus supports this as a pathway-class observation rather than an alphabetical accident. Claim `claim:78305cab7c1c7b98458d` states that represented ciliary transport, BBSome, transition-zone, ciliary-GPCR, and Hedgehog-adjacent perturbations in postnatal NeuN-positive neurons were largely buffered at basal nuclear RNA and did not form a shared ciliary transcriptional module. Its contributing non-held-out targets include `Cep290`, `Dync2i1`, `Ift43`, `Ift88`, `Kif3b`, `Ttc21b`, and `Ttc8`. This corpus layer is a packaged interpretation of the same experiment, not independent replication.

I also compared those 21 profiles directly in the declared Parquet for `151 TH Prkcd Grin2c Glut` using `logfoldchanges` as the signed value and `pvals_adj < 0.05` as the significance definition. All 21 profiles were available over 17,259 measured features. The comparison recovered the count-table pattern: 20 nodes had no significant feature and `Ttc8` alone had a one-gene negative program. The ciliary cohort had no significant-program overlap; across all 210 pairs, the positive-tail overlap coefficient had mean 0.072 and median 0.075, while the negative-tail overlap coefficient had mean 0.122 and median 0.128. Thus the expression Parquet did not reveal a recurrent positive Nme7-like module hidden underneath the DEG counts.

## Synthesis

The best local scale anchor for Nme7 is the near-null ciliary/IFT/Hedgehog cohort, whose arithmetic mean is 0.048 DEGs and whose squared-log natural center is also effectively zero. Nme7 is not an exact IFT or Hedgehog receptor gene, but its characterized acute function is closer to ciliary microtubule capacity than to the high-yield transcriptional, splicing, proteasome, or chromatin perturbations that dominate the upper tail of the focal count table.

Moderate Nme7 expression in 43.64% of focal nuclei prevents treating the perturbation as unexpressed, so a singleton response is plausible. However, the matched training ciliary components are overwhelmingly 0, the corpus explicitly bounds the basal neuronal ciliary module as transcriptionally buffered, and the Nme7-specific card leaves within-window depletion unresolved. There was no stronger task-matched positive anchor to lift the integer point above zero.

Predicted `n_degs`: 0.
