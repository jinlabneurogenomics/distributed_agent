# DEG-count prediction for held-out Atf2

## Question and interpretation

The run asks for the held-out value of `n_degs` for each requested target in
`151 TH Prkcd Grin2c Glut`: the number of measured genes with
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after the target is
perturbed by sparse AAV CRISPR-Cas9 in postnatal mouse neurons.  The manifest
contains one requested held-out perturbation, `Atf2`, and it is absent from both
the training DEG Parquet and the training count CSV.

I treated the endpoint as a measured response breadth in this exact screen, not
as a direct score for Atf2 biological importance.  The focal training endpoint
is sparse: 1205 of 1674 training perturbations have zero DEGs in this cell
group, so the zero/nonzero decision was calibrated against closely related
within-screen perturbations rather than a transcription-factor prior alone.

## Sources used

- `training_de_all_cell_groups.parquet`, filtered to
  `group_name == "151 TH Prkcd Grin2c Glut"`, was used for the signed
  differential-expression signatures and the identities of FDR-significant
  measured genes.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` was used as the
  authoritative observed DEG count for all non-held-out perturbations in the
  focal cell group.
- `019_Atf2.csv` supplied the requested target order.
- The internal Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1` was used for curated
  cross-perturbation claims over CREB/AP-1, KAT3 coactivators, Ras/MAPK, and
  stress-MAPK nodes.
- The Distributed Agents run-local profile tools were used as a sanity check on a
  caller-selected cohort of CREB/AP-1/MAPK comparator perturbations in the focal
  cell type.
- External mechanism was checked against PubMed literature.  Key mechanisms:
  ATF2 is a bZIP CREB/ATF-family transcription factor that can homodimerize or
  heterodimerize with Jun/Fos-family AP-1 proteins (Hoeffler et al. 1991,
  PMID:1828107; De Cesare et al. 1995, PMID:7624151); CBP can directly bind
  and potentiate ATF2 and other bZIP factors (Sano et al. 1998,
  DOI:10.1074/jbc.273.44.29098, PMID:9786917); JNK and p38 are canonical ATF2
  kinases in stress-activated MAPK signaling (Gupta et al. 1995,
  DOI:10.1126/science.7824938, PMID:7824938; Morton et al. 2004,
  DOI:10.1016/j.febslet.2004.07.031, PMID:15304344; Kirsch et al. 2020,
  DOI:10.1038/s41467-020-19582-3, PMID:33188182).

## Computational steps

I read the focal training-count CSV to get the observed `n_degs` values and
queried the Parquet only for `151 TH Prkcd Grin2c Glut` rows belonging to a
curated analog set:

`Atf6, Creb1, Crebbp, Ep300, Fosl2, Jund, Mafg, Map2k1, Map2k2, Map2k6,
Map3k7, Mapk1, Mapk9, Mef2a, Mef2c, Mef2d, Nr4a1, Nr4a3`.

For each comparator I counted rows with `pvals_adj < 0.05` and inspected the
actual significant genes.  The closest missing direct comparators, `Atf1`,
`Atf7`, `Jun`, `Junb`, `Fos`, `Fosb`, and `Jdp2`, were not training targets in
the focal count file, so they could only serve as external biological priors.
For the observed comparators I also computed Pearson correlations of Wilcoxon
`scores` across the shared measured genes to avoid over-weighting extreme
low-expression `logfoldchanges` with adjusted P values of 1.

The CREB/AP-1/MAPK comparator signatures were nonconvergent.  The focal
score-space correlations were near zero for the most relevant pairs:

| pair | score Pearson r |
|---|---:|
| Creb1-Crebbp | 0.015 |
| Creb1-Fosl2 | 0.029 |
| Creb1-Jund | -0.023 |
| Creb1-Map2k1 | -0.067 |
| Creb1-Mapk9 | 0.039 |
| Crebbp-Ep300 | 0.090 |
| Crebbp-Fosl2 | 0.038 |
| Crebbp-Jund | -0.025 |
| Fosl2-Jund | -0.006 |
| Jund-Map2k1 | 0.010 |
| Map2k1-Mapk9 | -0.021 |

This matched the internal Distributed Agents corpus claims that represented CREB/AP-1/EGR
and related bZIP/MAPK perturbations do not form a shared postnatal neuronal
loss-of-function module, that `Crebbp`, `Ep300`, and `Creb1` are not
interchangeable in this assay, and that the detectable basal Ras/MAPK RNA output
is limited to a sparse `Braf`/`Map2k1` thalamic branch rather than being shared
across ERK, MEK2, RAS, RAF1, or broader RASopathy perturbations.

## Atf2-specific analogs and counterexamples

### CREB/ATF and KAT3 coactivator axis

- `Creb1`: 10 DEGs.  Significant genes were `Crem` up, `Vwc2l` up, the
  self-transcript `Creb1` up, and seven down-regulated genes
  (`Tmem181a`, `Txndc12`, `Chkb`, `Nceh1`, `Ppox`, `Sez6l2`, `Rnf139`).
  `Creb1` is the strongest represented CRE-binding bZIP analog in the training
  set, so it shows that a CRE-family transcription factor can make a detectable
  but still very small 151 TH response.
- `Atf6`: 0 DEGs, despite being an ATF/CREB bZIP stress-response transcription
  factor.  It is an ER-stress branch rather than the JNK/p38 ATF2 branch, so it
  is only a boundary case, but it argues against every ATF-family perturbation
  being visible as basal snRNA-seq DE.
- `Crebbp`: 8 DEGs; `Stxbp2` was the top hit, with no overlap with the `Creb1`
  DEG set.  CBP can coactivate ATF2 biochemically, but in this same screen its
  single-gene perturbation produced a separate small signature.
- `Ep300`: 0 DEGs.  As the CBP paralog and a broad KAT3 coactivator, it is a
  strong counterexample to assigning ATF2 a response purely from possible
  CBP/p300 dependence.

### AP-1 and activity-regulated transcription factors

- `Jund`: 0 DEGs.
- `Fosl2`: 0 DEGs.
- `Mafg`: 1 DEG, `Lamp2`.
- `Nr4a1`: 0 DEGs.
- `Nr4a3`: 0 DEGs.

ATF2 can bind AP-1-like sites with Jun-family proteins, but the represented
AP-1 and immediate-early/activity-regulated transcription-factor targets were
mostly silent in this basal juvenile neuron readout.  `Jund` and `Fosl2` are not
the nearest biochemical partners, because `Jun`, `Junb`, `Fos`, `Fosb`, `Atf1`,
and `Atf7` were not in the training count file, but the observed negatives keep
the expected `Atf2` response near zero.

### JNK, p38, ERK, and Ras/MAPK signaling

- `Mapk9`/JNK2: 0 DEGs.
- `Map2k6`, an upstream p38 MAPK kinase: 0 DEGs.
- `Map3k7`/TAK1: 0 DEGs.
- `Map2k1`: 4 DEGs, all down-regulated: `Vgf`, `Ptpn5`, `Etv5`, and `Unc13a`.
- `Braf`: 4 DEGs in the same corpus-defined thalamic MAPK module.
- `Ntrk2`: 3 DEGs, partially related to the same module.
- `Shoc2`: 1 DEG.
- `Map2k2`, `Mapk1`, `Raf1`, `Hras`, `Kras`, `Rasa2`, `Sos1`,
  `Spred1`, and `Spred2`: all 0 DEGs in the focal training counts.

ATF2 is a phosphorylation-dependent substrate of JNK and p38, but the training
data do not show a standing stress-MAPK transcriptional module in these
unstimulated postnatal neurons.  The ERK/BRAF/MEK thalamic state is real but
tiny, and its significant genes are neurotrophin/ERK readouts rather than
ATF2-like CREB/AP-1 targets.

### Other activity-dependent TF controls

`Mef2a` produced 4 DEGs and `Mef2c` produced 1 self-transcript DEG, while
`Mef2d` produced 0.  These are not direct ATF2 paralogs, but they set a useful
scale for transcription factors with known neuronal roles under the same
postnatal sparse-CRISPR design: detectable effects were singleton to
10-gene-scale, not hundreds of genes.

## Prediction

The positive case for `Atf2` is that it is a real bZIP transcription factor with
CRE/AP-1 partners and stress-MAPK regulation, and the `Creb1` and `Crebbp`
single-gene perturbations prove that small CRE-associated transcriptional
effects can clear FDR in this focal cell group.

The stronger within-dataset evidence, however, is negative.  The closest
represented AP-1/bZIP factors (`Jund`, `Fosl2`, `Atf6`) were zero; the stress
kinase-side comparators (`Mapk9`, `Map2k6`, `Map3k7`) were zero; p300 was zero;
and the only repeated Ras/MAPK transcriptional branch was the separate
`Braf`/`Map2k1` 4-gene `Vgf`/`Ptpn5`/`Unc13a` state.  The internal corpus also
explicitly rejects a shared CREB/AP-1/EGR/bZIP/MAPK loss-of-function module in
this juvenile neuronal assay.  I therefore predict that acute partial `Atf2`
loss will sit below the BH 0.05 threshold in `151 TH Prkcd Grin2c Glut`.

Point prediction: `Atf2 = 0` DEGs.

## Limits

The main direct paralogs and partners that would have made the comparison
sharper, especially `Atf7`, `Atf1`, `Jun`, and `Junb`, were not training
perturbations in the focal endpoint.  `Atf2` might also act under stress,
activity, DNA-damage, or inflammatory stimulation; this experiment measured
basal NeuN-positive nuclei after P16 AAV CRISPR and did not measure ATF2
phosphorylation, JNK/p38 flux, chromatin binding, or immediate early induction.
The predicted zero is therefore a screen-specific expectation of no genes
passing FDR 0.05, not a claim that ATF2 is dispensable in neurons.
