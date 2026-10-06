# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The requested prediction is the integer number of genes expected to pass
Benjamini-Hochberg FDR 0.05 in the `151 TH Prkcd Grin2c Glut` Wilcoxon contrast
after each held-out gene perturbation.  The single held-out target in
`the single-target request` is `Stim1`.  Its own differential-expression rows and held-out
`n_degs` value are absent from the supplied inputs by construction, so I treated
the focal-cell training count CSV as the directly observed endpoint for
non-held-out perturbations and the Parquet signatures as endpoint-matched
analogs and counterexamples.  Expression signatures, Findings, and reports from
the internal `perturbai-july-260713-sourceguard-1773-v1` corpus are alternate
same-experiment representations, not independent validation.

I did not use the unavailable ranked-supervision workbench, ordering validator,
or predictive graph-review tools because this is a scalar count prediction with
an unranked one-gene target list.

## Sources used

- Direct endpoint: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Direct expression evidence:
  `training differential-expression dataset`,
  especially `151 TH Prkcd Grin2c Glut` rows for non-held-out calcium-store and
  calcium-signaling perturbations.
- Internal corpus: `perturbai-july-260713-sourceguard-1773-v1` Findings and
  resolved Evidence/References for the measured `Atp2a2`, `Itpr1`, and
  `Ppp3r1` perturbations.
- External mechanism: STIM1/STIM2/Orai SOCE reviews by Kraft 2015,
  DOI 10.1080/19336950.2015.1071747, PMID 26218135; Serwach and
  Gruszczynska-Biegala 2020, DOI 10.3389/fnmol.2020.617422, PMID 33424550; and
  Korshunov and Prakriya 2025, DOI 10.1146/annurev-physiol-022724-105330, PMID
  39586031.  For the UPR/ISR relationship of ER stress I used Hetz, Zhang and
  Kaufman 2020, DOI 10.1038/s41580-020-0250-z, and Pakos-Zebrucka et al. 2016,
  DOI 10.15252/embr.201642195, PMID 27629041.

## Quantitative calibration

The focal-cell training table contains 1,674 non-held-out perturbations.  It is
zero-inflated and heavy-tailed: median `n_degs` = 0, 75th percentile = 1, 90th =
2, 95th = 18, mean = 14.05, and maximum = 2,677.  Thus a positive point
prediction needs a close endpoint-matched analog, not just a broadly important
neuronal gene.

I queried the Parquet for genes in the ER calcium, plasma-membrane calcium,
ryanodine/IP3 receptor, calmodulin, calcineurin/NFAT, and CaMK neighborhoods.
The relevant measured focal counts at FDR 0.05 were:

| training target | relationship to `Stim1` | `151` `n_degs` |
|---|---|---:|
| `Atp2a2` | SERCA2 ER Ca2+ pump that directly refills ER stores | 187 |
| `Atp2b1` | plasma-membrane Ca2+ ATPase, removes cytosolic Ca2+ | 22 |
| `Calm1` | calmodulin isoform upstream of many Ca2+-dependent enzymes | 14 |
| `Ppp3r1` | calcineurin regulatory subunit downstream of Ca2+/calmodulin | 9 |
| `Ppp3ca` | calcineurin catalytic subunit | 4 |
| `Calm2`, `Itpr1`, `Nfatc3`, `Camk2a`, `Camk2g`, `Ryr2`, `Ryr3` | calcium sensors, release channels, or downstream effectors | 0 |
| `Calm3`, `Camk2b` | other Ca2+-responsive genes | 1 |

The focal `Atp2a2` signature was broad and stress-like.  Its top rows included
the self transcript `Atp2a2` at logFC -1.256 and FDR 1.78e-19, followed by
strong induction of `Cars`, `Ddit3`, `Shmt2`, `Chac1`, `Xbp1`, `Herpud1`,
`Hspa5`, `Asns`, `Vegfa`, `Slc38a2`, `Mthfd2`, `Slc38a1`, and the lower-FDR
part of an ATF4/ISR nutrient program.  The internal `Atp2a2` report described
that same program as ER-stress/UPR and amino-acid/one-carbon ISR induction, and
reported same-direction convergence with proteasome and ER glycosylation
perturbations rather than with ER Ca2+ release-channel perturbations.  In the
same report, `Itpr1`, `Ryr2`, `Ryr3`, `Atp2b2`, and `Atp2c1` did not phenocopy
SERCA2 loss, and `Atp2b1` produced only a small `151` signature without the
`Ddit3`/`Hspa5`/`Xbp1` module.

For the measured counterexamples, the focal Parquet had no FDR 0.05 downstream
genes for `Itpr1`, `Ryr2`, `Ryr3`, `Nfatc3`, `Camk2a`, or `Camk2g`, despite
reasonable matched perturbed-cell counts in `151` for several of them
(`Itpr1` 203, `Ryr3` 151, `Nfatc3` 172, `Camk2a` 122).  `Ppp3r1` had only nine
DEGs and its internal report showed a small `Pcsk1n`/synaptic-remodeling
signature that did not expand into the canonical NFAT or immediate-early
program.  `Ppp3ca`, `Ppp3cc`, and `Nfatc3` did not phenocopy `Ppp3r1`.

The causal transfer model was:

`Stim1` CRISPR loss of function -> reduced STIM1 ER Ca2+ sensing and reduced
recruitment of Orai-containing store-operated Ca2+ entry complexes after ER
store depletion -> impaired refill or altered local ER/plasma-membrane Ca2+
microdomains, with basal refill partly buffered by STIM2 and other isoforms ->
possible changes in activity-, calcineurin-, CaMK-, or ER-stress-responsive
transcription in the exposed thalamic neurons that survive and are recovered ->
FDR 0.05 DEG count.

That chain is weaker than the chain for `Atp2a2`: loss of SERCA2 directly
removes the pump that fills ER stores, whereas loss of STIM1 removes a
store-depletion sensor/recruiter that is most engaged after substantial
depletion or strong activity.  The review literature also emphasizes STIM2 as a
basal neuronal SOCE/homeostasis sensor and STIM1 as a stronger-depletion or
activity-coupled sensor.  Because the Perturb-seq readout is a basal
3-4-week nuclear RNA state rather than a calcium-flux or evoked-activity assay,
the more appropriate measured comparators are the flat IP3R/RYR release-channel
and weak calcineurin/CaMK branches, not the broad ER-pump UPR state.

## Target-specific prediction

### `Stim1`

Biologically relevant measured analogs were:

- `Atp2a2`, 187 focal DEGs: a mechanistic upper-bound/counterexample.  It
  directly limits ER Ca2+ refilling and produced a broad `151` UPR/ISR program.
  `Stim1` lies in ER Ca2+ sensing and SOCE activation, but its loss is not
  equivalent to directly depleting ER stores with SERCA2 loss, so I did not
  transfer this high count.
- `Atp2b1`, 22 focal DEGs: a modest Ca2+-homeostasis response dominated by
  activity-like up-regulated genes including `Fos`, `Vgf`, `Nr4a1`, and `Syt7`,
  without the SERCA2 UPR module.  PMCA1 loss should raise cytosolic Ca2+ by
  impairing extrusion, the opposite first-order sign from STIM1 SOCE loss.
- `Itpr1`, `Ryr2`, and `Ryr3`, 0 focal DEGs each: ER release-channel lesions
  in the same broad calcium organelle neighborhood, all flat in `151`; the
  `Itpr1` internal report also found no meaningful global transcriptional
  neighbor and no Atp2a2-like UPR.
- `Ppp3r1` and `Ppp3ca`, 9 and 4 focal DEGs: Ca2+/calmodulin-calcineurin
  branch perturbations.  They showed only a small thalamic signature and did
  not form a large NFAT-like state.
- `Calm1`, `Calm2`, `Calm3`, `Camk2a`, `Camk2b`, and `Camk2g`, 0-14 focal
  DEGs: upstream calmodulin and CaMK perturbations were buffered or
  isoform-specific rather than broad UPR or SOCE surrogates.

These observations make a high `Atp2a2`-like prediction inappropriate.
`Stim1` could still perturb calcium flux or synaptic physiology, but the focal
endpoint only counts genes whose basal survivor-conditioned nuclear RNA shifts
reach FDR 0.05.  Given the zero-inflated training distribution and the flat
same-cell outcomes for ER release channels and several downstream Ca2+
effectors, the point prediction is 0 DEGs.

## Limits and extrapolation

No `Stim2`, `Orai1/2/3`, `Trpc`, `Saraf`, or `Tmem110` perturbation was present
in the non-held-out training target set, so there was no direct SOCE-complex
analog.  The closest strong in-dataset calcium hit, `Atp2a2`, perturbs a pump
rather than an ER-store sensor and therefore provides only an upper-bound stress
analogy.  The external STIM literature is largely calcium-imaging,
electrophysiology, glia, or specific-neuron work rather than the exact P16
mosaic CRISPR/snRNA-seq thalamic assay.  Finally, a zero DEG-count prediction
does not mean STIM1 is unimportant or unedited; it means I expect its resting
`151 TH Prkcd Grin2c Glut` transcriptomic response to be below the assay's FDR
0.05 detection threshold.
