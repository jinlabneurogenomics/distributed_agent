# Pcyt2 n_degs forecast

## Requested target

- Target: `Pcyt2`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`

## Evidence used

### Target biology

The declared Pcyt2 biology bundle supports target reach in the exact focal
population: in matched non-target nuclei from `151 TH Prkcd Grin2c Glut`, Pcyt2
was detected in 20,185 of 23,679 cells, or 85.24%, with mean CP10K 1.51.
This makes lack of target expression an unlikely explanation for a flat result.

The same bundle does not support an all-or-none acute loss by the P37-P44
harvest. Pcyt2 supplies CDP-ethanolamine for de novo phosphatidylethanolamine
and ether-PE synthesis. Synaptic PE turns over within the 21-28 day perturbation
window, which favors an observable membrane-homeostasis response, but
pre-existing membrane PE, slower lipid pools, unmeasured residual Pcyt2 protein
clearance, and Pisd-dependent PE synthesis should buffer the knockout. The
functional-stock card therefore calls the realized stock
`partially_depleted_or_leading_edge`, not uniformly depleted.

### Training counts

The declared focal count table is highly sparse:

- 1,205 of 1,674 training targets had `n_degs = 0`.
- The median was 0.
- The 75th, 90th, and 95th percentiles were 1, 2, and 18.

Thus the empirical scale strongly penalizes a large count unless there is a
known broad RNA-processing, proteostasis, or vesicle/lysosome phenotype.

### Chosen training comparators

The closest measured pathway perturbation was `Selenoi`, the downstream
ethanolamine phosphotransferase in the same CDP-ethanolamine route. In the
training count table it had 5 DE genes in the focal class. Direct inspection of
the declared DE Parquet showed the 5 FDR<0.05 calls were `Insig1`, `Msmo1`,
`Selenoi`, `Fdft1`, and `Nos1ap`, with 172 matched Selenoi-perturbed nuclei and
23,679 matched controls. The packaged Selenoi report interpreted this as a
compact sterol-feedback state and explicitly not as a broad UPR, ISR,
autophagy-lysosome, redox, or Tardbp stress tail.

Other represented lipid or sterol comparators in the same reports were also
small in the count table:

- `Agps`: 1
- `Far1`: 2
- `Hmgcr`: 0
- `Srebf1`: 0
- `Srebf2`: 7

I treated broader sterol/endomembrane neighbors as boundary cases rather than
direct count anchors: `Mib1`, `Dctn1`, `Marchf6`, and `Rab7` carried 27, 75, 14,
and 501 DE genes respectively, but their signatures include strong
endolysosomal or sterol-control programs rather than isolated PE synthesis.

## Forecast

Pcyt2 should be more likely than a generic training perturbation to cross the
FDR threshold because it is well expressed in the focal thalamic population and
its lipid carrier pool partly renews during the assay. The buffering mechanisms
argue against a broad catastrophic signature, and the most direct measured
analog, Selenoi, was only a 5-gene responder. I therefore put Pcyt2 in the same
compact-response regime and predict **5 DE genes**.
