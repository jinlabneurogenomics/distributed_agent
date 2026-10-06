# Prdm12 DEG-count prediction trace

## Question and resolved ambiguities

The held-out manifest for this run contains one target:

- `Prdm12`

The requested endpoint is the integer number of measured genes with
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after acute AAV/CRISPR
loss of `Prdm12` in `151 TH Prkcd Grin2c Glut` neurons. I treated `0` as a
literal prediction that no gene will survive FDR 0.05 in this cell group, not as
an assertion that PRDM12 has no biological function.

The held-out target is not present as a perturbation in either supplied input, so
I used only:

- focal-cell observed `n_degs` for non-held-out perturbations,
- focal-cell differential-expression signatures for those same non-held-out
  perturbations,
- perturbations of PRDM-family members and PRDM12-adjacent developmental or
  chromatin factors represented in the training universe,
- the same-experiment Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, and
- PubMed-indexed PRDM12 mechanism literature.

## Dataset operations

1. I read `185_Prdm12.csv` and confirmed that `Prdm12` was the only requested
   held-out target.

2. I read
   `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` to calibrate response
   breadth in the exact output space. Among 1,674 focal-cell training targets:

   - 1,205 targets had `n_degs = 0`.
   - The median was `0`.
   - The 75th percentile was `1`.
   - The 95th percentile was `18`.
   - Only very strong core processes produced hundreds to thousands of DEGs
     (`Uba5 = 2677`, `Tpr = 1768`, `Sin3a = 1433`, `Rnpc3 = 868`,
     `Zbtb7a = 841`).

   This distribution makes weak developmental TF perturbations default to zero
   unless there is direct same-context evidence for a maintained program.

3. The full parquet has 616,253,184 rows, so I used the parquet metadata to find
   the row groups containing `151 TH Prkcd Grin2c Glut`, then read only rows with
   `group_name == "151 TH Prkcd Grin2c Glut"` and candidate `gene_target`
   values. The focal signature has 17,259 measured genes per target.

4. I also read the rows where `names == "Prdm12"` in the focal cell group for
   every training perturbation. `Prdm12` is present as a measured feature in the
   matrix, but across all 1,674 non-held-out focal perturbations every adjusted
   p-value for that feature was `1.0`, and many rows had the same extreme
   low-count log-fold-change sentinel behavior seen for very sparse transcripts.
   That does not prove that the `Prdm12` guide failed or would have no protein
   effect, but it argues that this thalamic group does not carry a stable,
   measurable `Prdm12` RNA program comparable to the expressed target features
   that move in strong focal responders.

5. I used Distributed Agents Runtime `profile_compare` on a candidate panel of
   `Prdm10`, `Prdm2`, `Prdm5`, `Prdm16`, `Ehmt1`, `Rest`, `Neurod1`, `Isl1`,
   `Ptf1a`, and `Zic1` in the focal cell group. Among these, only `Prdm10`
   had at least 50 significant focal features, only `Ehmt1` and `Zic1` had 1-9
   significant features, and the remaining seven were zeros; significant
   feature intersections between the active PRDM/chromatin/developmental
   surfaces and the flat surfaces were absent. This supported treating the
   weak/zero analogs as separate small or null readouts rather than as hidden
   variants of the `Prdm10` module.

## Training perturbations used as analogs and counterexamples

### PRDM-family comparators

- `Prdm10`, `n_degs = 52`.
  This is the one assayed PRDM-family member with a clear focal response. Its
  top focal hits were a mostly down-regulated neuronal module:
  `Madd`, `Cadm3`, `Ptov1`, `Uchl1`, `Kcnt1`, `Rnasek`, and `Stmn2`.
  The Distributed Agents corpus reports that `Prdm10` loss creates a distinct recurrent,
  mostly down-regulated postnatal neuronal RNA module and specifically does not
  phenocopy represented `Prdm2`, `Prdm5`, or `Prdm16` perturbations. I therefore
  treated `Prdm10` as evidence that a PRDM-family perturbation can be detected in
  this assay, but not as a direct proxy for `Prdm12`.

- `Prdm2`, `n_degs = 0`; `Prdm5`, `n_degs = 0`; `Prdm16`, `n_degs = 0`.
  These were the direct same-family counterexamples. Their focal rows had no
  genes with `pvals_adj < 0.05`, matching the Distributed Agents claim that same PR/SET
  domain membership did not produce interchangeable juvenile neuronal
  signatures in this screen.

### PRDM12 chromatin cofactor and REST/chromatin-repressor axis

- `Ehmt1`, `n_degs = 4`.
  `Ehmt1` is the G9a/GLP-family H3K9 methyltransferase represented in the focal
  training set; the main focal hits were `Abhd12b`, `Endou`, `Smtn`, and
  `Stxbp2`, all up-regulated. In vitro work showed that PRDM12 can recruit G9a
  through its zinc-finger domains to methylate H3K9 (Yang and Shinkai 2013,
  doi:10.1247/csf.13010), while neural-crest `G9a` loss does not reproduce the
  sensory-ganglion phenotype of `Prdm12` loss (Tsimpos et al. 2024,
  doi:10.1186/s13064-023-00179-7). I therefore used `Ehmt1` only as a weak
  upper-bound analog for a chromatin-repressor-linked effect. Its four-gene
  count is already very small, and its signature does not look like a PRDM12
  sensory or POMC program.

- `Rest`, `n_degs = 0`.
  REST is a neural repressor with chromatin cofactors, but the Distributed Agents corpus
  records a pan-neuronal zero after acute P16 `Rest` loss and shows that `Rest`
  does not phenocopy measurable `Sin3a`, `Chd4`, `Zmynd8`, `Mecp2`, or `Ehmt1`
  signatures. This is a strong assay-context warning: repression programs that
  are important in progenitors or stress states need not yield FDR-level changes
  in healthy juvenile postmitotic neurons.

### Nociceptor and sensory-neuron developmental circuitry

- `Neurod1`, `n_degs = 0`; `Isl1`, `n_degs = 0`; `Ntrk1`, `n_degs = 0`.
  PRDM12 is required in developing nociceptors for initiation of a downstream
  pro-neuronal cascade including `Neurod1`, `Brn3a`/`Pou4f1`, and `Isl1`
  (Bartesaghi et al. 2019, doi:10.1016/j.celrep.2019.02.098), and it helps
  initiate and maintain `Ntrk1`/TrkA expression by modulating Neurog1/2 activity
  (Desiderio et al. 2019, doi:10.1016/j.celrep.2019.02.097). In the exact focal
  thalamic group, however, `Neurod1`, `Isl1`, and `Ntrk1` were all zero. The
  Distributed Agents corpus also records that `Neurod1` and its represented bHLH
  relatives were flat in mature postnatal neuronal nuclei, and that `Isl1` and
  represented LIM-homeodomain/embryonic identity factors were transcriptionally
  inactive or buffered in sampled postmitotic neuronal contexts.

- `Ntrk2`, `n_degs = 3`; `Ntrk3`, `n_degs = 0`.
  The broader Trk family was mostly silent. `Ntrk2` itself, `Atp2a2`, and `Vgf`
  were the three `Ntrk2` hits, but this was a BDNF/TrkB-autoregulation-like
  local response, not an NGF/TrkA nociceptor analog.

- `Phox2a`, `n_degs = 0`; `Phox2b`, `n_degs = 0`; `Runx3`, `n_degs = 0`.
  `Prdm12` normally represses visceral sensory determinants `Phox2a/b` in
  developing somatosensory ganglia (Vermeiren et al. 2023,
  doi:10.1016/j.isci.2023.108364). The lack of any `Phox2a` or `Phox2b`
  response in the focal training data again argues that the embryonic
  somatosensory fate switch is not active in these P16 thalamic neurons.

### V1 interneuron, retinoic-acid, and upstream Zic/Wnt candidates

- `Ptf1a`, `n_degs = 0`; `Lhx3`, `n_degs = 0`; `Nkx6-2`, `n_degs = 0`;
  `Pax6`, `n_degs = 0`.
  PRDM12 specifies p1/V1 interneurons through cross-repression with `Dbx1` and
  `Nkx6` genes in the embryonic hindbrain/spinal cord (Thelie et al. 2015,
  doi:10.1242/dev.121871), but the represented pieces of that spinal
  developmental neighborhood did not respond in the focal thalamic neurons.

- `Rxra`, `n_degs = 0`.
  PRDM12 can be induced by retinoic acid in P19 neural differentiation cultures
  (Yang and Shinkai 2013), but the focal training perturbation of `Rxra` was
  silent.

- `Zic1`, `n_degs = 2`; `Zic2`, `n_degs = 0`; `Zic3`, `n_degs = 0`;
  `Zic4`, `n_degs = 0`.
  Xenopus work places `prdm12` downstream of `zic1` and Wnt signaling in neural
  differentiation (Rahman et al. 2020, doi:10.1002/jdn.10048). In this mouse
  focal group, `Zic1` had only two hits, `Slc29a1` up and `Zic1` down, while
  the other assayed `Zic` factors were zero. I therefore did not propagate the
  much larger `Ctnnb1` and `Tcf7l2` focal counts to `Prdm12`; those Wnt-pathway
  perturbations were broad thalamic regulators in this assay, not direct
  postmitotic PRDM12 analogs.

### Known central PRDM12-positive cells are outside the focal group

PRDM12 has a central maintenance role in arcuate `POMC` neurons: PRDM12
co-expresses with POMC from development to adulthood, and POMC-neuron
conditional `Prdm12` loss markedly reduces `Pomc` and alters feeding and body
weight (Hael et al. 2020, doi:10.1016/j.molmet.2020.01.007). That literature is
real support for adult neuronal PRDM12 activity, but it points to specialized
hypothalamic melanocortin neurons rather than `151 TH Prkcd Grin2c Glut`
thalamic glutamatergic cells.

## Target-specific prediction

### `Prdm12`: predicted `n_degs = 0`

The decisive evidence is within-dataset:

- The focal endpoint distribution is dominated by zeros; a weak lineage TF has
  to clear a high bar before I should move it off zero.
- The assayed PRDM-family members other than `Prdm10` were all zero, and
  Distributed Agents reports that `Prdm10` is a sequence- and context-specific module,
  not a generic PR-domain phenotype.
- The closest PRDM12 developmental partners or downstream genes represented in
  training, including `Neurod1`, `Isl1`, `Ntrk1`, `Ptf1a`, `Phox2a`,
  `Phox2b`, `Pax6`, `Nkx6-2`, and `Rxra`, were also zeros in the focal cell
  group.
- `Ehmt1 = 4` and `Zic1 = 2` are the only small nonzero analog-ish surfaces, and
  both are tiny, mechanistically indirect, and have signatures unrelated to
  PRDM12 sensory-neuron or POMC-neuron outputs.
- As a measured RNA feature, `Prdm12` itself was never FDR-regulated by any of
  the 1,674 training perturbations in the focal group, consistent with
  little/no robust PRDM12 transcript in these nuclei.

The external mechanism sharpens the zero call. PRDM12 is essential for
embryonic nociceptor specification, TrkA/Ntrk1 maintenance in sensory neurons,
repression of Phox2 visceral fates in developing ganglia, p1/V1 spinal
interneuron specification, and Pomc maintenance in arcuate hypothalamic neurons
(Thelie et al. 2015; Bartesaghi et al. 2019; Desiderio et al. 2019; Hael et al.
2020; Latragna et al. 2021, doi:10.1097/j.pain.0000000000002536; Kokotovic et
al. 2021, doi:10.3389/fnmol.2021.720973; Vermeiren et al. 2023). Those are
strong but highly lineage-specific programs. The assayed cell type is a
postmitotic thalamic glutamatergic group edited at P16, and the same screen
shows repeated buffering of embryonic identity factors after P16 perturbation.

I therefore expect `Prdm12` loss in `151 TH Prkcd Grin2c Glut` to fall below
the FDR threshold entirely rather than to create even an `Ehmt1`- or
`Zic1`-sized mini-signature.

## Limits and extrapolations

- The corpus had no direct `Prdm12` target node, so the Distributed Agents evidence is
  through assayed relatives and counterexamples, not through a Prdm12-specific
  same-experiment finding.
- The available PRDM-family tests do not include every close relative or PRDM12
  cofactor; in particular they do not directly test a `Prdm12` chromatin-bound
  regulon.
- The supplied DE parquet reports perturbation-vs-control RNA statistics, not
  Cas9 indel rates or PRDM12 protein loss. A zero prediction can be wrong if
  `Prdm12` protein is maintained in these cells despite sparse nuclear RNA.
- Literature PRDM12 phenotypes come largely from germline or conditional models,
  embryonic ganglia/spinal cord, adult DRG nociceptors, Xenopus, or P19 cells.
  Those are imperfect analogs for sparse AAV CRISPR editing of juvenile mouse
  thalamic neurons.
- The estimate is a point prediction for this exact FDR-count endpoint. A tiny
  subthreshold state change, a nontranscriptional electrophysiological effect,
  or a rare subtype response diluted inside the broad `151 TH Prkcd Grin2c
  Glut` group would still be reported as `0`.
