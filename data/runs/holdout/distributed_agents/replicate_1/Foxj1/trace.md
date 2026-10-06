# DEG-count prediction trace

## Question and endpoint

The requested prediction is the focal-cell DEG burden caused by acute CRISPR loss
of `Foxj1` in `151 TH Prkcd Grin2c Glut` cells. I interpreted
`predicted_n_degs` as the integer number of measured genes expected to pass
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in that one thalamic
glutamatergic class. The `Foxj1` perturbation itself was held out from the
training differential-expression parquet and from the focal-cell DEG-count CSV,
so no `Foxj1` target rows were used.

This is a scalar response-breadth prediction, not a ranked nomination task:
`dataset.perturbseq_features`, `corpus.predictive_graph_review`, and
`synthesis.ordering_validate` were not authorized in the run capability manifest.

## Sources used

- Declared training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This is the direct observed endpoint for non-held-out perturbations.
- Declared DE parquet:
  `training differential-expression dataset`.
  I filtered it to `group_name == "151 TH Prkcd Grin2c Glut"` for biologically
  nominated non-held-out targets and checked their adjusted P values and
  leading nominal genes.
- Run-local held-out manifest:
  `single-target request for Foxj1`,
  which contains only `Foxj1`.
- Internal same-experiment interpretation corpus:
  PerturbAI July `260713_sourceguard_1773_v1` Findings/Evidence reports for
  visible targets `Foxa2`, `Foxj3`, `Foxp2`, `Rfx3`, `Ift88`, `Kif3b`, `Ttc8`,
  and `Ttc19`. I used these reports only as packaged interpretation of the
  same Perturb-seq experiment, not as independent replication.
- External mechanism literature from PubMed:
  Stubbs et al. 2008, `doi:10.1038/ng.267`, PMID 19011629; Cruz et al. 2010,
  `doi:10.1242/dev.051714`, PMID 21098568; Abdi et al. 2018,
  `doi:10.1038/s41467-018-03812-w`, PMID 29695808; Lemeille et al. 2020,
  `doi:10.1093/nar/gkaa625`, PMID 32725242; Rayamajhi et al. 2024,
  `doi:10.1371/journal.pbio.3002468`, PMID 38271330.

## Training calibration and analog checks

The focal-cell training distribution is very sparse: among 1,674 visible
non-held-out biological targets, 1,205 have `n_degs = 0`, the median is 0, the
75th percentile is 1, and the 90th percentile is 2. Therefore a nonzero
prediction needs a target-specific reason rather than just membership in a large
developmental gene family.

I pulled focal-cell rows for the closest training perturbations I could map onto
`Foxj1` biology:

| training target | focal `n_degs` | relevance to `Foxj1` |
|---|---:|---|
| `Foxj3` | 0 | closest visible `Foxj*` forkhead target; the July corpus calls the whole surface an FDR-flat postmitotic-neuron null |
| `Foxa2` | 0 | forkhead factor with cilia/floor-plate/Shh developmental context but no acute focal effect |
| `Foxp2` | 0 | neuronal forkhead TF expressed in thalamic/basal-ganglia lineages; no focal DE despite known neuronal biology |
| other `Fox*` targets: `Foxc2`, `Foxe3`, `Foxi1`, `Foxk2`, `Foxl1`, `Foxl2`, `Foxn1`, `Foxp3` | 0 each | family counterexamples showing that forkhead TF status alone did not create thalamic DE in this assay |
| `Rfx3` | 0 | transcription factor upstream of many ciliary genes in mouse ependymal cells; no FDR genes in the focal parquet slice |
| `Rfx7` | 0 | visible RFX-family comparator; no focal response |
| `Ift88`, `Ift81`, `Ift43`, `Kif3b`, `Ttc21b`, `Bbs5`, `Cep290` | 0 each | IFT, kinesin-2, retrograde IFT, BBSome, and transition-zone ciliary machinery were transcriptionally buffered in the focal group |
| `Ttc8`, `Ttc19` | 1 each | the one significant focal hit was the self-transcript; these do not provide a multi-gene ciliary response |
| `Dnal1`, `Cfap69`, `Trp73` | 0 each | motile-cilia/ependymal candidates represented in the screen; focal nulls |

The direct focal-cell parquet rows agreed with the count table. For `Foxj3`,
`Foxa2`, `Foxp2`, `Rfx3`, `Ift88`, `Ift43`, `Ift81`, `Kif3b`, `Ttc21b`,
`Bbs5`, `Cep290`, `Dnal1`, `Cfap69`, and `Trp73`, no measured gene had
`pvals_adj < 0.05`; the best adjusted P values for most of these targets were
1.0 or far above 0.05. `Ttc8` and `Ttc19` each had exactly one focal hit, their
own self-transcript, which I treated as a weak isolated detection rather than as
evidence for a downstream Foxj1-like program.

Two same-experiment corpus checks were especially relevant:

- `Rfx3`: the RFX3 report found no FDR<0.10 downstream genes in any of 22
  recovered postmitotic neuronal groups. Its curated 29-gene ciliary panel,
  including `Foxj1`, `Ift88`, `Ift140`, `Kif3a`, `Kif3b`, dynein heavy chains,
  and radial-spoke/CFAP genes, had 0 FDR<0.10 hits over 638 Rfx3 gene-by-group
  tests. This is the closest visible test of whether the Foxj1/RFX ciliogenic
  transcriptional module is basally active in NeuN+ neurons.
- `Kif3b`/`Ift88`/`Ttc8`: visible IFT, BBSome, dynein-2, kinesin-2 and
  transition-zone perturbations were zero-to-singleton responders. The Kif3b
  report also noted that the exact kinesin-2 partners `Kif3a`, `Kif3c`, and
  `Kifap3` were not present as training perturbations, so the ciliary analog
  set is informative but not complete.

I also checked `Foxj1` as a measured transcript in the focal rows of the 1,674
training perturbations. It was never FDR-significant, consistent with the idea
that the canonical `Foxj1` ciliated-cell program is not a strong regulated
program in recovered `151 TH Prkcd Grin2c Glut` nuclei.

## Target-specific reasoning

### Foxj1

`Foxj1` encodes a forkhead transcription factor that is best established as a
determinant of motile ciliogenesis. Stubbs et al. showed that Foxj1 is
sufficient to induce a motile-cilia gene program in frog embryos and is needed
for left-right organizer cilia in Xenopus and zebrafish. Abdi et al. showed that
mature mouse ependymal cells require continued Foxj1 maintenance to preserve
their multiciliated state. Lemeille et al. placed RFX1/2/3, especially RFX2 and
RFX3, in the mouse ependymal motile-ciliogenesis transcriptional hierarchy that
regulates many Foxj1-associated ciliary genes. Rayamajhi et al. extended Foxj1
biology to olfactory sensory neurons, where it controls olfactory cilia and
cell-type differentiation.

The intervention-to-readout chain for this experiment breaks before a large
focal-cell transcriptional response. The CRISPR intervention was delivered at
P16 and read out 3-4 weeks later in NeuN-enriched brain nuclei; the focal class
is a thalamic glutamatergic neuronal class, not ependyma, choroid plexus,
airway/testis/oviduct multiciliated epithelium, floor plate, or olfactory
sensory epithelium. If Foxj1 loss impaired motile cilia in ependymal cells, that
cell type was not the assayed focal population. If Foxj1 affected primary cilia
or ciliary signaling indirectly in mature neurons, the closest represented
effectors argue that such perturbations generally do not become a stable basal
snRNA-seq program in this screen: `Rfx3`, `Ift88`, `Ift81`, `Ift43`, `Kif3b`,
`Bbs5`, `Cep290`, and `Ttc21b` were all 0-DEG focal perturbations. The two
single-gene exceptions, `Ttc8` and `Ttc19`, were self-depletion events and are
not mechanistically close to a Foxj1 transcription-factor module.

Forkhead-family membership was also not a positive signal. Every visible
non-held-out forkhead target I found in the focal count table had `n_degs = 0`;
this included the nearest same-subfamily training target `Foxj3`, the strongly
neuronal `Foxp2`, and the Shh/floor-plate-associated `Foxa2`. The corpus
interpretation for `Foxp2` showed that postnatal transcription-factor
responsiveness is factor-specific rather than universally absent, so the flat
forkhead surfaces are informative target context, not just a failure to detect
any transcription-factor phenotype.

I therefore predict `Foxj1` will sit with the focal-cell null analogs rather
than with broad thalamic responders such as `Rora` or `Ctnnb1`.

Predicted `n_degs`: **0**.

## Limits and uncertainty

The prediction extrapolates from related ciliary machinery and forkhead/RFX
training targets; `Foxj1` itself was held out, and the exact upstream/downstream
motile-cilia regulators `Rfx1`, `Rfx2`, `Rfx4`, `Mcidas`, and `Gmnc` were not
training perturbations. Many motile-cilia transcripts are expected to be near
the expression floor in thalamic neuronal nuclei, so a null snRNA signature
would not exclude effective editing, altered cilium length, altered receptor
localization, ependymal phenotypes, embryonic/floor-plate phenotypes, or
olfactory sensory-neuron phenotypes. It only predicts that recovered
`151 TH Prkcd Grin2c Glut` nuclei will have no robust FDR<0.05 steady-state
nuclear mRNA response to acute sparse `Foxj1` loss.
