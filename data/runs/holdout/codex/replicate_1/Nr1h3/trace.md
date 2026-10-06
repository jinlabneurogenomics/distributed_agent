# Evidence and prediction

Target: `Nr1h3` in `151 TH Prkcd Grin2c Glut`.

Prediction: `n_degs = 0`.

## Evidence used

The supplied biology-only `Nr1h3` bundle says the P16 edit should plausibly deplete
new LXR-alpha protein supply by the P37-P44 harvest because NR1H3 is a renewable
RXR-heterodimer nuclear receptor and the 21-28 day window spans several average
mouse-brain protein lifetimes. That only establishes plausible target
realization, not a strong thalamic endpoint: the same card has no matched
postnatal neuronal Nr1h3 loss phenotype, no transferable timing anchor, and an
unresolved `Nr1h2` redundancy axis.

The exact focal-population reach is weak. In non-target `151 TH Prkcd Grin2c
Glut` nuclei, `Nr1h3` was detected in only 843 of 23,679 nuclei, with
`pct_cells_expressing = 3.5601`, `mean_raw_umi = 0.0381`, and
`pseudobulk_cpm = 2.3874`. This is the dominant quantitative downward bearing:
even a real cell-autonomous LXR-alpha effect should be diluted in the aggregated
thalamic class.

The same-class training count table is sparse overall: among 1,674 training
perturbations, the median `n_degs` is 0, the 75th percentile is 1, the 90th
percentile is 2, and only 106 perturbations have at least 10 DEGs. Therefore a
lowly expressed regulator needs specific same-axis evidence to move away from a
zero forecast.

The nearest represented LXR/RXR/lipid-axis perturbations were all flat in this
exact cell class except for the distinct SREBP2 sterol-output factor:

| training perturbation set | `151 TH Prkcd Grin2c Glut` outcome |
| --- | --- |
| `Nr1h2`, `Nr1h4`, `Nr1h5`, `Rxra`, `Rxrb`, `Rxrg` | all `n_degs = 0` |
| `Abca1`, `Abca7`, `Hmgcr`, `Lrp1`, `Lrp8`, `Sorl1`, `Srebf1` | all `n_degs = 0` |
| `Ppara`, `Ppard`, `Pparg` | all `n_degs = 0` |
| `Srebf2` | `n_degs = 7`, consisting of self plus six sterol-biosynthesis/feedback transcripts |

The focal Parquet rows agree with those counts: the LXR/RXR neighbors had no
gene with `pvals_adj < 0.05` in the focal class; several had a minimum adjusted
p-value of 1.0, and `Rxrb`, `Rxrg`, and `Abca7` still had minima of only 0.541,
0.437, and 0.334. By contrast `Srebf2` had a compact, clearly significant
sterol module headed by `Srebf2`, `Dhcr24`, `Insig1`, `Hmgcs1`, `Msmo1`,
`Cyp51`, and `Sqle`, so the assay can detect a neuronal cholesterol program
when that axis is actually engaged.

Packaged same-experiment findings support the same interpretation without using
the held-out `Nr1h3` outcome. `Nr1h2` was reported as a complete
postmitotic-neuronal transcriptional null at FDR < 0.10 across all 23 measured
groups, with the expected LXR cholesterol-efflux and sterol-regulatory
transcripts absent. `Rxra` was reported as having no robust downstream
transcriptome in any measured group, and `Rxrb` as only a one-gene edge response
outside the target cell class. The release also summarizes represented
retinoid/RAR/RXR and lipid nuclear-receptor single-gene perturbations as flat,
singleton, sparse, or nonconvergent rather than a coherent shared acute
neuronal receptor module.

## Reasoning

I weighted `Nr1h2` and the RXR paralogs most heavily because they are direct
LXR/RXR-operation analogs for NR1H3. Their same-class counts are all zero, and
the broader all-cell-class findings argue that this is not a missed local
module in `151` but a generally quiet basal neuronal LXR/RXR surface. I treated
`Srebf2` as an upper qualitative boundary rather than a matched donor: it proves
that cholesterol-biosynthesis RNAs can be recovered in postnatal neurons, but
its positive call is the direct loss of the sterol transcriptional activator
itself, whereas the LXR/RXR, PPAR, ABCA, and `Hmgcr` perturbations fail to
phenocopy it.

The biology card keeps the forecast from being a technical-failure null:
functional stock is likely substantially depleted by harvest. However, the
exact expression footprint says the target is present in only a small minority
of focal nuclei, and the same-axis training perturbations show little evidence
for tonic basal LXR/RXR control in this NeuN-enriched juvenile neuronal assay.
On a log-count scale the direct-neighbor evidence stays below one expected
significant gene, so the integer prediction is the background mode, 0.

I did not query or use any `Nr1h3` perturbation signature or `Nr1h3` DEG count;
the only `Nr1h3` measurement used was the declared endpoint-blind baseline
expression reach from the target bundle.
