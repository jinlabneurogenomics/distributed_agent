# Held-out DEG-count prediction for Srgap3

## Question and endpoint

The requested scalar prediction is the number of measured genes with
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after perturbing the
held-out gene `Srgap3` in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic
neurons. I treated the count as an assay- and power-dependent snRNA-seq
response breadth in recovered nuclei. A count of one can be only the edited
target transcript; it is not necessarily a downstream state change.

There was one requested target in
`prepared/manifests/deg-count/the single-target request`, and the list was unranked:

| target_name |
| --- |
| Srgap3 |

I confirmed that `Srgap3` was absent as a `gene_target` in the declared training
parquet and therefore absent from the training focal-cell DEG-count CSV.

## Sources used

Direct experiment-derived sources:

* Declared differential-expression parquet:
  `training differential-expression dataset`.
  I used narrow DuckDB scans against the focal class and the mechanistic
  comparator targets.
* Declared focal-cell training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
* PerturbAI atlas July 260713 sourceguard 1773 v1 same-experiment corpus.
  `Srgap3` had no visible packaged Finding in this release. I used the packaged
  `Cdc42`, `Cyfip2`, and `Pak1` records only to interpret measured
  Rho/Rac/WAVE-axis quietness; this corpus is a curated representation of the
  same screen, not independent replication.

External mechanism literature:

* Soderling et al. 2007, Journal of Neuroscience, DOI
  `10.1523/JNEUROSCI.3209-06.2006`, PMID `17215396`: WRP/srGAP3 associates
  with WAVE1 and the Rac/Arp2/3 actin-remodeling pathway to regulate neuronal
  spine density, synaptic plasticity, and memory.
* Carlson et al. 2011, Journal of Neuroscience, DOI
  `10.1523/JNEUROSCI.4433-10.2011`, PMID `21325512`: WRP/srGAP3 inverse F-BAR
  activity promotes dendritic spine initiation; loss of WRP reduces mushroom
  spines and impairs learning and memory.
* Waltereit et al. 2012, FASEB Journal, DOI `10.1096/fj.11-202317`, PMID
  `22820399`: germline Srgap3 knockout mice have increased basal Rac1 activity
  and neurodevelopmental and behavioral phenotypes.
* Bacon et al. 2012, Mechanisms of Development, DOI
  `10.1016/j.mod.2012.10.005`, PMID `23127797`: review of srGAP3 as a
  Rac1-regulating Slit-Robo GAP involved in actin cytoskeletal organization,
  dendritic spines, neurite outgrowth, and Slit-Robo signaling.

## Local quantitative calibration

The focal class is sparse overall. In the training count table, 469 of 1674
non-held-out perturbations had any FDR 0.05 DEG in this class; the median count
was 0, the 75th percentile was 1, the 90th percentile was 2, and the 95th
percentile jumped to 18. This is a heavy-tailed endpoint: ordinary cytoskeletal
or signaling hits sit at 0-1 unless they trigger a broad nuclear state.

For Srgap3 I compared the biologically closest available perturbations rather
than the high-count tail. The closest training targets were the Rac/WRC/PAK and
Slit-Robo/Rho-GAP neighborhood, because Srgap3 encodes WRP/srGAP3, a neuronal
Rac GAP and WAVE-associated actin regulator.

| training target | focal `n_degs` | focal pattern |
| --- | ---: | --- |
| Cdc42 | 1 | the only FDR 0.05 gene was the target transcript `Cdc42`; next adjusted p-value was 1.0 |
| Cyfip2 | 1 | the only FDR 0.05 gene was the target transcript `Cyfip2`; next adjusted p-value was 1.0 |
| Pak1 | 1 | the only FDR 0.05 gene was the target transcript `Pak1`; next adjusted p-value was 0.323 |
| Robo1 | 1 | the only FDR 0.05 gene was the target transcript `Robo1`; next adjusted p-value was 0.890 |
| Arhgef9 | 1 | the only FDR 0.05 gene was `Arhgef9`; one weaker `Ralgps1` call reached only FDR 0.133 |
| Rac1 | 0 | no FDR 0.25 gene; minimum FDR was 1.0 |
| Cyfip1 | 0 | no FDR 0.25 gene; minimum FDR was 1.0 |
| Pak2 | 0 | no FDR 0.25 gene; minimum FDR was 0.807 |
| Pak3 | 0 | no FDR 0.25 gene; minimum FDR was 0.910 |
| Dock3 | 0 | no FDR 0.25 gene; minimum FDR was 0.584 |
| Robo2 | 0 | no FDR 0.25 gene; minimum FDR was 1.0 |
| Slit2 | 0 | no FDR 0.25 gene; minimum FDR was 0.724 |
| Arhgap18 | 0 | no FDR 0.25 gene; minimum FDR was 1.0 |
| Arhgap32 | 0 | no FDR 0.25 gene; minimum FDR was 0.607 |

This was a consistent near-null local neighborhood. The packaged Cdc42 report
also summarized that acute P16 Cdc42 loss did not induce a canonical Cdc42-Rho
actin/spine transcriptional program, and that represented Rac/PAK/CYFIP and
Rho-family relatives were flat or single-gene responders. The packaged Cyfip2
report made the parallel WAVE regulatory complex point: `Cyfip2` self-RNA could
be significantly reduced in several groups, but WRC-Arp2/3 and
FMRP/eIF4E-linked partner transcripts were not secondarily induced.

I also checked whether `Srgap3` itself is a measured focal-cell transcript.
It is present in the focal expression rows for all 1674 training perturbations.
Under unrelated perturbations its focal log-fold change distribution was
centered near zero, with mean 0.011, median 0.020, 5th to 95th percentile
-0.338 to 0.344, and 95th percentile absolute Wilcoxon score 1.62. It can be
moved detectably in this dataset by broad transcriptional regulators such as
`Cic` and `Sin3a`, but those are not biochemical analogs of Srgap3 loss. The
relevant question for the held-out knockout is therefore whether the guide pool
is likely to add a direct self-transcript call, not whether Srgap3 participates
in a high-DEG transcription-factor module.

## Target-specific reasoning

### Srgap3

Biology: Srgap3/WRP/MEGAP is a Slit-Robo family Rho GAP that binds the WAVE1
complex and down-regulates Rac1-dependent actin remodeling. Germline and
culture perturbations implicate it in dendritic filopodia, spine initiation,
spine density, neurite outgrowth, and cognitive behavior. The strongest causal
chain is:

`Srgap3 CRISPR LoF -> loss of srGAP3 Rac-GAP/F-BAR activity -> altered
Rac/WAVE/Arp2/3-dependent actin remodeling at dendrites/spines -> possible
postnatal synaptic structural phenotype in recovered neurons -> snRNA-seq
steady-state nuclear transcript counts`.

The first two steps are well supported by external Srgap3 literature. The last
step is weak: the requested readout is not spine density, Rac1-GTP, WAVE
activity, Arp2/3 activity, or synaptic physiology. The within-dataset analogs
argue that this biochemical module is buffered at the nuclear-RNA endpoint.
Direct Cdc42 and Rac effector perturbations, WRC-adjacent `Cyfip1/Cyfip2`,
PAK-family kinases, Slit/Robo perturbations, and other Rho regulators produced
zero or one DEG in the focal class, and the one-DEG cases were almost entirely
self-transcript knockdown calls.

That makes a broad Srgap3 response, for example tens of DEGs, unlikely. I did
not assign zero, however, because `Srgap3` is a measured neuronal transcript in
the focal class and the closest expressed analogs with enough focal nuclei
(`Cdc42`, `Cyfip2`, `Pak1`, `Robo1`, `Arhgef9`) each registered exactly their
own edited transcript as the only FDR 0.05 gene. The point prediction is
therefore one DEG: a likely self-transcript call with no reliable downstream
FDR-significant secondary program.

Prediction for `Srgap3`: `1`.

## Limits

The main extrapolation is target-mRNA behavior. The held-out Srgap3 guide
efficiency and recovered perturbed-nucleus count are not present in the
training inputs, and average target-mRNA reduction is not a direct editing
efficiency measurement. A less effective Srgap3 guide pool or low focal
expression would make the true count 0; unusually strong guide activity or an
unmeasured thalamic Srgap3-specific transcriptional feedback could push it
above 1.

The Rac/WAVE/Slit-Robo analogs are mechanistically close for cytoskeletal and
spine biology but are not obligate complex subunits of Srgap3. Their null
downstream RNA responses are strongest evidence that this actin-regulatory
axis does not usually become a broad steady-state nuclear transcriptome change
in the P16-to-P37/P44 NeuN+ assay; they do not rule out local synaptic,
post-translational, morphological, or survivor-selection phenotypes.
