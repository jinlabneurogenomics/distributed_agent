# Held-out DEG-count prediction

## Question and endpoint

The held-out target for this run was `Dlx5`. I interpreted the requested value as
the integer count of `151 TH Prkcd Grin2c Glut` measured-gene rows whose
Benjamini-Hochberg adjusted Wilcoxon p-value would have been below 0.05 after a
P16 sparse AAV CRISPR loss-of-function perturbation and P37-P44 single-nucleus
RNA-seq readout. `Dlx5` was absent as a `gene_target` in the differential
expression parquet and absent from the focal-cell training-count CSV, so its own
signature and count were not available.

The requested endpoint is directly observed for visible training perturbations
in `151 TH Prkcd Grin2c Glut`; for `Dlx5` itself it is absent by construction.
I therefore used the focal-cell training `n_degs` values as direct quantitative
calibration and used the all-cell differential-expression parquet to inspect
appropriate training analogs. The same-experiment July PerturbAI corpus was used
only as a packaged interpretation of those Perturb-seq results, not as
independent replication. I used PubMed literature as prior biological context for
the DLX5/DLX6 developmental program.

## Sources used

- Declared focal-cell training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet:
  `training differential-expression dataset`.
- Requested-target manifest:
  `single-target request for Dlx5`.
- Internal same-experiment corpus: `perturbai-july-260713-sourceguard-1773-v1`,
  queried through `corpus.findings`, `corpus.report_evidence`, and the bounded
  read-only graph entrypoint for comparator identity around visible `Dlx6`.
- External literature:
  Zerucha et al. 2000, J Neurosci, PMID:10632600, DOI:10.1523/JNEUROSCI.20-02-00709.2000;
  Poitras et al. 2007, Development, PMID:17409112, DOI:10.1242/dev.02845;
  Wang, Dye et al. 2010, J Neurosci, PMID:20392955, DOI:10.1523/JNEUROSCI.5963-09.2010;
  Wang, Lufkin and Rubenstein 2011, J Comp Neurol, PMID:21452241, DOI:10.1002/cne.22618;
  Le et al. 2017, J Neurosci, PMID:28821666, DOI:10.1523/JNEUROSCI.2125-16.2017;
  Aouci et al. 2022, Cells, PMID:35681437, DOI:10.3390/cells11111739.

## Computations

The focal-cell training table had 1,674 perturbations. It was highly sparse:
1,205/1,674 had `n_degs = 0`, 1,481/1,674 had `n_degs <= 1`, and only 469 had
any FDR 0.05 DEG. This background set the base rate but did not determine the
prediction.

I first checked close or mechanistically adjacent visible targets in the
training-count CSV. The Dlx paralogs and forebrain inhibitory-development
comparators visible in this run were null in the focal thalamic glutamatergic
class:

| training target | focal `n_degs` | relevance to `Dlx5` |
|---|---:|---|
| `Dlx6` | 0 | closest visible partner of `Dlx5` at the linked `Dlx5/Dlx6` locus and in the forebrain Dlx1/2/5/6 GABAergic-development program |
| `Dlx3` | 0 | weaker Dlx-family counterexample; not a canonical forebrain Dlx factor |
| `Arx` | 0 | downstream/parallel interneuron specification and migration regulator |
| `Gad2` | 0 | direct GABAergic biochemical target class downstream of DLX biology |
| `Nkx2-1` | 0 | MGE-patterning transcription factor upstream of Lhx6/Pvalb interneuron identity |
| `Six3` | 0 | forebrain developmental transcription-factor comparator named in the Dlx6 same-experiment report |
| `Isl1` | 0 | basal ganglia developmental transcription-factor comparator |
| `Pax6` | 0 | neurodevelopmental transcription-factor counterexample in the same focal group |
| `Lhx3`, `Lhx4`, `Otx2` | 0 | homeobox developmental transcription-factor counterexamples |
| `Mef2c` | 1 | assay-sensitivity counterexample showing that a developmental transcription-factor perturbation can cross FDR in this focal group |

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and
the same analog targets. Each Dlx-related null had 17,259 measured rows in the
focal cell class. `Dlx6`, with 294 matched perturbed nuclei and 23,679 matched
controls, had 0 genes at FDR < 0.05 or FDR < 0.10; its lowest adjusted p-value
was 1.0. `Dlx3` likewise had 0 genes at FDR < 0.10 with 161 perturbed nuclei.
The focal `Dlx6` signature did not move `Dlx5`, `Dlx6`, `Gad1`, `Gad2`,
`Slc32a1`, `Pvalb`, `Sst`, `Lhx6`, `Arx`, `Nkx2-1`, `Fos`, `Npas4`, `Nr4a1`,
or `Vgf`: all of those candidate readout rows had adjusted p = 1.0. Thus the
nearest in-dataset analog did not show a subthreshold DLX/GABA or
activity-regulated program hiding just outside the focal-cell DEG cutoff.

The same-experiment July report for `Dlx6` supplied the broader all-cell
cross-check over the same parquet. `Dlx6` had rows in all 23 measured neuronal
groups and had 0 downstream genes at FDR < 0.10 everywhere. In the forebrain
GABAergic groups most compatible with known Dlx biology, `Dlx5`, `Gad1`,
`Gad2`, `Slc32a1`, `Pvalb`, and `Sst` rows were nonsignificant. The corpus also
reported that unbiased whole-universe signed-Wilcoxon neighbors of `Dlx6` had
near-zero correlations, so there was no weak but coherent expression module to
transfer into `Dlx5`. The same report explicitly contrasted visible `Dlx6` with
`Dlx3`, `Gad2`, `Arx`, `Nkx2-1`, `Six3`, and `Mef2c`; these were used here as
candidate analogs or falsifiers, not as graph-ranked candidates.

## Target-specific rationale

### `Dlx5`

The strongest in-dataset anchor for `Dlx5` is `Dlx6`. `Dlx5` and `Dlx6` are the
linked distal-less homeobox pair induced by the Dlx forebrain regulatory network:
Zerucha et al. showed that conserved `Dlx5/Dlx6` intergenic enhancers reproduce
forebrain expression and lose activity in `Dlx1/Dlx2` mutants, and Poitras et
al. showed that DLX autoregulation and Ascl1/MASH1 inputs maintain Dlx enhancer
activity in ventral forebrain precursor domains. Le et al. further showed that
DLX1/2 directly activate `Gad1` and `Gad2`, placing GABA synthesis downstream of
the canonical Dlx program.

That biology makes `Dlx5` important in the developing inhibitory forebrain, but
the causal chain does not point to a broad singleton effect in the requested
cells. The perturbation here is delivered at P16 to sparse postmitotic neurons;
the focal endpoint is a recovered thalamic glutamatergic class rather than a
ventral-telencephalic progenitor, cortical interneuron, or olfactory bulb
interneuron population. Wang, Dye et al. found strong phenotypes for combined
or developmental Dlx5/6 loss in parvalbumin cortical interneuron development,
and Aouci et al. found adult GABAergic phenotypes after Vgat-Cre manipulation
of Dlx5/6 dosage. Those studies support a DLX5/6 GABAergic developmental prior,
but they are in a different stage, perturbation strength, and inhibitory-cell
context from a Dlx5-only perturbation in `151 TH Prkcd Grin2c Glut`.

The all-cell `Dlx6` singleton surface is therefore especially informative.
Despite `Dlx6` being the visible partner most likely to share `Dlx5` function,
the Perturb-seq screen observed no FDR < 0.10 downstream genes for `Dlx6` in
any neuronal group and no `Dlx5`, `Gad1/Gad2`, `Slc32a1`, `Pvalb`, or `Sst`
movement in the GABAergic groups where a postnatal maintenance effect would
have been most plausible. The `151 TH Prkcd Grin2c Glut` row itself was also
fully null for `Dlx6`, `Dlx3`, `Arx`, `Gad2`, and `Nkx2-1`. `Mef2c` with
`n_degs = 1` shows that the focal group was not completely unable to produce
FDR calls for developmental transcription factors, but it does not establish a
DLX-like thalamic glutamatergic program.

I therefore predict a zero-count outcome:

- within-dataset driver: `Dlx6` in the focal class had 294 perturbed nuclei,
  23,679 controls, and 0 DEGs; its broad DLX/GABA marker rows were all FDR = 1.0;
- analogs and counterexamples: `Dlx3`, `Arx`, `Gad2`, `Nkx2-1`, `Six3`, `Pax6`,
  `Isl1`, `Lhx3`, `Lhx4`, and `Otx2` were also 0 in the focal class;
- external prior: DLX5/6 phenotypes are strongest during embryonic/early
  GABAergic development or in paired `Dlx5/Dlx6` dosage changes, while the
  requested class is postnatal and glutamatergic;
- point estimate: `Dlx5 -> 0` DEGs.

## Limits and uncertainty

`Dlx5` itself was held out, as were the exact forebrain partners `Dlx1` and
`Dlx2`, so the closest observed singleton perturbation was `Dlx6` rather than
`Dlx5` or a paired `Dlx5/Dlx6` cut. Sparse CRISPR may leave a gene's nuclear RNA
unchanged even when frameshift alleles are present, so I did not treat flat
Dlx-family self-transcripts as failed editing. The assay sampled recovered
NeuN-positive nuclei after P16; it did not test embryonic progenitors, olfactory
bulb, non-neuronal neural-crest derivatives, circuit physiology, cell density,
or behavioral phenotypes. A paired Dlx5/6 perturbation in adult GABAergic cells
could have a real phenotype that a Dlx5-only perturbation in thalamic
glutamatergic survivors would miss.
