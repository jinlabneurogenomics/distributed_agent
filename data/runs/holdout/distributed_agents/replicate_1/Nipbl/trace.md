# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The held-out perturbation list for this run contains one mouse target, `Nipbl`.
I interpreted the requested value as the integer number of measured genes that
would have passed BH-adjusted Wilcoxon `pvals_adj < 0.05` in recovered
`151 TH Prkcd Grin2c Glut` nuclei after the P16 AAV-CRISPR loss-of-function
perturbation. The `Nipbl` perturbation was held out from both supplied input
tables, so I did not have direct `Nipbl` expression rows or its focal DEG count.

The endpoint is directly observed for non-held-out training perturbations in
`151 TH Prkcd Grin2c Glut`; it is absent for `Nipbl`. I therefore used the
training endpoint table as the quantitative calibration surface and used the
declared differential-expression parquet plus same-experiment report corpus to
check whether candidate analogs had matching focal expression patterns.

## Sources

- Declared training endpoint CSV:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared all-cell differential-expression parquet:
  `training differential-expression dataset`.
- Run-local task bindings, coverage, capability manifest, and measurement
  registry under `codex_runtime/pipeline/`.
- Internal same-experiment corpus:
  `july_260713_sourceguard_1773_v1`, queried through `corpus.findings` and
  `corpus.report_evidence` for `Smc1a`, `Stag2`, and `Ctcf`. I used this as
  packaged interpretation of the same training experiment, not as independent
  replication.
- External biological literature from PubMed:
  Davidson et al. 2019, DOI `10.1126/science.aaz3418`, PMID 31753851;
  Shi et al. 2020, DOI `10.1126/science.abb0981`, PMID 32409525;
  Luppino et al. 2022, DOI `10.1371/journal.pgen.1010528`, PMID 36449519;
  Alonso-Gil et al. 2023, DOI `10.1038/s41467-023-36900-7`, PMID 36898992;
  Alonso-Gil and Losada 2023, DOI `10.1016/j.tcb.2023.03.006`,
  PMID 37062615. I used these papers only for the prior that NIPBL/MAU2
  activates cohesin ATPase and loop extrusion and that NIPBL reduction is an
  upstream perturbation of cohesin-mediated genome folding and gene regulation.

## Quantitative calibration from the training data

The focal training counts are highly zero-inflated. Among the 1,674 visible
training perturbations, 469 had any focal DEG, the median was 0, the 75th
percentile was 1, the 95th percentile was 18, and only a small tail reached
hundreds or thousands of DEGs. I therefore treated low two-digit counts as
already being above the ordinary response background in this endpoint.

For each biologically selected analog, I counted rows in the DE parquet grouped
by `gene_target` and `group_name`, using both the requested `pvals_adj < 0.05`
threshold and a permissive `pvals_adj < 0.10` boundary threshold:

```sql
SELECT gene_target, group_name,
       COUNT(*) FILTER (WHERE pvals_adj < 0.05) AS n_degs,
       COUNT(*) FILTER (WHERE pvals_adj < 0.10) AS n_fdr10
FROM read_parquet($training_de_all_cell_groups)
WHERE gene_target IN ($candidate_targets)
GROUP BY 1, 2;
```

The most relevant focal training perturbations were:

| training perturbation | focal `n_degs`, FDR<0.05 | focal FDR<0.10 | interpretation |
| --- | ---: | ---: | --- |
| `Smc1a` | 24 | 35 | core cohesin SMC subunit; small, focal thalamic response |
| `Stag2` | 37 | 55 | alternative SA2/STAG cohesin subunit; small, focal thalamic response |
| `Stag1` | 0 | 1 | STAG paralog; only a marginal `Gabra1` call and no `Smc1a`-module overlap |
| `Pds5a` | 0 | 0 | cohesin regulator; flat in the focal group |
| `Hdac8` | 0 | 0 | SMC3 deacetylase/CdLS cohesin-cycle gene; flat in the focal group |
| `Ctcf` | 270 | 360 | loop-boundary factor; much broader, Pcdh-heavy counterexample |

The same-experiment corpus reported the key `Smc1a`/`Stag2` signature
relationship in the focal class: `Stag2` had 55 FDR<0.10 downstream genes and
`Smc1a` had 35; 14 genes overlapped in the same direction and none overlapped
oppositely. In the stricter `pvals_adj < 0.05` rows I directly recovered nine
shared same-direction genes: `Adamts19`, `Adamts2`, `Inhbb`, `Necab2`, `Ptprm`,
`Sema5a`, `Smtn`, `Sox13`, and `Utp14b`. These were mostly down-regulated
adhesion, extracellular-matrix, and neuronal-signaling genes, with the secondary
up-regulated `Inhbb` arm.

`Ctcf` was an important upper-bound counterexample rather than the main
calibrator. Although CTCF and cohesin cooperate at loop boundaries, the
training `Ctcf` focal perturbation had 270 DEGs and a large Pcdh-cluster
program that was not phenocopied by measured cohesin-machinery perturbations.
I therefore did not transfer the `Ctcf` count wholesale to `Nipbl`.

Directly analogous perturbations that would have improved the estimate were not
available in the training parquet: `Smc3`, `Rad21`, `Nipbl`, `Mau2`, `Wapl`,
and `Pds5b` were absent as visible `gene_target` values.

## Target-specific reasoning

### `Nipbl`

`Nipbl` encodes the major NIPBL cohesin-loader/ATPase-activating factor.
Biochemical reconstitution showed that cohesin and NIPBL-MAU2 form a holoenzyme
that extrudes DNA loops (Davidson et al. 2019), and structural work showed
extensive NIPBL/cohesin/DNA contacts that stimulate cohesin ATPase-head
engagement (Shi et al. 2020). Loss of NIPBL therefore has a direct upstream
causal route to impaired cohesin loop extrusion and altered enhancer/TAD-scale
gene regulation. Cell-culture depletion experiments further show that reducing
NIPBL is transcriptionally consequential but not identical to every other
cohesin perturbation; NIPBL and WAPL have opposing effects on cohesin activity,
and reducing WAPL or CTCF can offset much of NIPBL-linked misexpression in
HCT116 cells (Luppino et al. 2022). Alonso-Gil et al. 2023 specifically found
that low NIPBL reduces cohesin-STAG2 genome-wide while cohesin-STAG1 can still
accumulate at CTCF sites, providing a mechanistic reason that a NIPBL
perturbation could resemble the measured `Stag2` response more than the flat
`Stag1` perturbation.

The experimental transfer chain I used was:

1. Acute P16 CRISPR edits `Nipbl` in postmitotic thalamic glutamatergic neurons.
2. Lower NIPBL activity impairs cohesin ATPase activation and loop extrusion.
3. Reduced loop extrusion propagates to a subset of chromatin-loop-dependent
   neuronal adhesion, synaptic, and signaling genes.
4. The snRNA-seq DE test observes expression among recovered cells 3 to
   4 weeks later, so catastrophic proliferative cohesion or viability effects
   are not expected to dominate this NeuN-positive postmitotic endpoint.
5. The focal DEG count is therefore expected to be small but nonzero, matching
   direct cohesin perturbations rather than the broad `Ctcf`/`Sin3a`/`Yy1`
   tail.

The decisive within-dataset analogs were `Smc1a` and `Stag2`: they are direct
cohesin complex perturbations, both responded selectively in the requested
thalamic cell group, and their focal signatures converged on the same
same-direction module. Their strict FDR<0.05 counts, 24 and 37, give the scale
for a direct cohesin-looping perturbation under this sparse AAV-CRISPR assay.

The counterexamples push the estimate down and keep it near the low end.
`Stag1` had zero FDR<0.05 DEGs, one marginal FDR<0.10 gene, and no overlap with
the 34-gene `Smc1a` FDR<0.10 signature. `Pds5a` and `Hdac8` had no focal genes
even at FDR<0.10 despite being annotated cohesin-cycle regulators. These nulls
show that not every single-gene perturbation adjacent to cohesin produces a
detectable effect in recovered postnatal thalamic neurons. They are weaker
counterevidence for `Nipbl`, however, because NIPBL is required to activate
cohesin loop extrusion directly, whereas PDS5A/PDS5B and HDAC8 act through more
context-specific residence-time and acetylation-cycle mechanisms.

I assigned `31` DEGs, essentially the midpoint between the two nonzero direct
cohesin subunit analogs. The prediction is nonzero because `Nipbl` is upstream
of the same limiting cohesin-looping function perturbed by `Smc1a` and
`Stag2`; it is kept in the tens rather than hundreds because the measured
`Smc1a`/`Stag2` responses are compact and because the large `Ctcf` Pcdh program
did not transfer cleanly to measured cohesin perturbations.

## Limits and uncertainty

The dominant uncertainty is effective perturbation strength: `Nipbl` itself was
withheld, so no matched-cell count, target transcript row, or guide performance
row is available for this target. The parquet and corpus are two views of the
same screen, not independent measurements. The best analogs are incomplete:
`Smc1a` removes part of the core ring, `Stag2` removes one alternative SA
subunit, and neither is the loader; `Mau2`, `Rad21`, `Smc3`, `Wapl`, and `Pds5b`
would have been better tests of whether weakening loop extrusion upstream of
both STAG-containing cohesin complexes gives a stronger or weaker focal count.
External NIPBL studies were biochemical or in proliferating human cell lines,
so they define the molecular prior but do not calibrate the exact FDR-count
response in P16 mosaic mouse thalamic neurons.
