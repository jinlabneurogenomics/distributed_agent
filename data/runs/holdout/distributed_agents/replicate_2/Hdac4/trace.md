# Hdac4 held-out DEG prediction

## Question and resolved ambiguities

The run asks for the number of FDR-significant genes expected after acute AAV
CRISPR loss of each held-out target in `151 TH Prkcd Grin2c Glut` cells.  The
manifest contains one requested target:

- `Hdac4`

I treated `n_degs` exactly as in the supplied training CSV: all measured genes
with `pvals_adj < 0.05` in the focal cell group, including the targeted
transcript itself if it passes the threshold.  `Hdac4` is absent from both the
training counts and the parquet `gene_target` column by construction, so the
estimate below transfers evidence from non-held-out perturbations.

## Sources used

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, the focal-cell training
  endpoint for 1,674 represented targets.
- `training_de_all_cell_groups.parquet`, filtered to
  `group_name == "151 TH Prkcd Grin2c Glut"` for exact per-gene Wilcoxon
  statistics of selected mechanistic comparators.
- The Distributed Agents same-experiment semantic corpus,
  `perturbai-july-260713-sourceguard-1773-v1`.  I used the `target_context`
  records for `Hdac5`, `Mef2a`, and `Mef2c`; there is no corpus record for the
  held-out `Hdac4`.
- A run-local Distributed Agents profile comparison over signed Wilcoxon-score vectors
  for represented class-IIa/MEF2/CaMK/calcineurin/CREB comparators.
- PubMed-indexed literature for external HDAC4 biology:
  - Youn, Grozinger, and Liu, 2000, JBC, DOI `10.1074/jbc.C000304200`,
    PMID `10825153`: HDAC4 and related repressors bind MEF2 and are controlled
    by calcium/calmodulin.
  - Chawla et al., 2003, Journal of Neurochemistry, DOI
    `10.1046/j.1471-4159.2003.01648.x`, PMID `12641737`: neuronal activity
    regulates HDAC4/HDAC5 nuclear export through CaM-kinase-sensitive
    shuttling.
  - Sando et al., 2012, Cell, DOI `10.1016/j.cell.2012.09.037`, PMID
    `23141539`: HDAC4 nuclear occupancy represses central synaptic genes and
    affects synaptic plasticity and memory.
  - Chen et al., 2014, Journal of Neuroscience, DOI
    `10.1523/JNEUROSCI.0569-14.2014`, PMID `25392500`: basal NMDA receptor
    activity regulates class-IIa HDACs including HDAC4; HDAC4 contributed to a
    subset of basal-NMDAR-dependent expression changes in cultured neurons.
  - Penrod et al., 2017, Addiction Biology, DOI `10.1111/adb.12522`, PMID
    `28635037`: HDAC4 and HDAC5 are close class-IIa relatives but are regulated
    differently by cocaine/cAMP signaling in striatum.

## Computational steps over the supplied data

I first verified that the manifest has only `Hdac4`, and that likely direct
comparators in the focal training endpoint had these exact counts:

| training target | focal `n_degs` | relevance to `Hdac4` |
| --- | ---: | --- |
| `Hdac5` | 0 | closest represented class-IIa HDAC paralog |
| `Hdac8` | 0 | represented HDAC-family counterexample, weaker because it is not class IIa |
| `Mef2a` | 4 | MEF2-family transcription factor repressed by class-IIa HDACs |
| `Mef2c` | 1 | MEF2-family activity and synapse regulator |
| `Mef2d` | 0 | MEF2-family paralog |
| `Camk2a` | 0 | activity/CaMK pathway upstream of class-IIa HDAC export |
| `Camk2b` | 1 | activity/CaMK pathway |
| `Camk2g` | 0 | activity/CaMK pathway |
| `Ppp3ca` | 4 | calcineurin catalytic subunit, activity-dependent MEF2 regulator |
| `Ppp3r1` | 9 | calcineurin regulatory subunit |
| `Ppp3cc` | 0 | calcineurin catalytic subunit |
| `Prkaca` | 1 | PKA pathway, HDAC5/CREB-adjacent upstream comparator |
| `Creb1` | 10 | CREB-dependent activity-regulated transcription factor |
| `Crebbp` | 8 | CREB/p300 chromatin coactivator |
| `Sin3a` | 1433 | broad chromatin-repressor counterexample |

The same lookup showed that the most direct missing nodes, `Hdac3`, `Hdac7`,
`Hdac9`, `Ncor1`, and `Ncor2`, were not present in the focal training-count
CSV, so they could not supply same-dataset endpoint counts.

Next I filtered the parquet to the focal group and those candidate
`gene_target` values, counted `pvals_adj < 0.05` and `< 0.10`, inspected the
best adjusted p values, and retained matched perturbed/control nucleus counts.
The represented HDAC and class-IIa upstream analogs were not threshold-near
misses:

- `Hdac5`: 289 matched perturbed nuclei, 0 genes at FDR 0.05 or 0.10; the best
  row was the `Hdac5` transcript itself, log2FC `-0.327`, `q = 0.273`.
- `Hdac8`: 111 matched perturbed nuclei, 0 genes at FDR 0.05 or 0.10; best
  row `Tbkbp1`, `q = 0.362`.
- `Mef2d`: 262 matched perturbed nuclei, 0 genes at FDR 0.05 or 0.10; all
  adjusted p values were 1 in the top-score tail.
- `Camk2a`, `Camk2g`, `Ppp3cc`, and `Syngap1`: 0 focal DEGs and no genes at
  FDR 0.10.
- `Mef2a`: 4 genes at FDR 0.05 and 7 at FDR 0.10, driven by a tiny mixed
  thalamic signature (`Gpr4`, `Prkcg`, `Ogt`, `Sez6` at FDR 0.05).
- `Mef2c`: 1 gene at FDR 0.05 and 4 at FDR 0.10; the lone FDR 0.05 row was
  the `Mef2c` transcript itself.
- `Ppp3ca`, `Ppp3r1`, `Prkaca`, `Creb1`, and `Crebbp` produced weak focal
  responses from 1 to 10 DEGs, rather than a large shared activity-like state.

As a sanity check on endogenous `Hdac4` expression, I also queried rows where
the measured gene `names == "Hdac4"` across all 1,674 non-held-out focal
perturbations.  `Hdac4` was never an FDR 0.05 downstream gene in this group
under any training perturbation; its minimum adjusted p value was 0.1269.
That does not prove the `Hdac4` guide pool will fail to reduce `Hdac4` RNA, but
it argues against `Hdac4` being a common sensitive marker of the focal
survivor states.

Finally, I ran a Distributed Agents profile comparison using signed Wilcoxon-score
vectors over the 17,259 focal measured genes for the represented HDAC/MEF2
neighborhood.  `Hdac5` and `Hdac8` were both classified as
`no_significant_features`; `Mef2a` and `Mef2c` were in the `1_to_9` bin.
`Hdac5` showed near-zero whole-vector similarity to the mechanistic peers:
Pearson `r = 0.027` with `Hdac8`, `r = -0.014` with `Mef2a`, `r = 0.0076` with
`Mef2c`, and absolute `r <= 0.045` against the CaMK/calcineurin/CREB peers
included in the comparison.  There were no FDR-significant shared-feature
intersections with `Hdac5`, because its focal FDR set was empty.

## Target-specific reasoning

### Hdac4

`Hdac4` encodes a class-IIa HDAC and is biologically close to `Hdac5`.  HDAC4
and HDAC5 can repress MEF2 transcription factors, and neuronal activity can
drive CaM-kinase-sensitive nuclear export of both proteins (Youn et al. 2000;
Chawla et al. 2003).  External work also makes HDAC4 a plausible neuronal gene:
nuclear HDAC4 represses synaptic transcription in cultured neurons and mutant
HDAC4 models (Sando et al. 2012), basal NMDAR activity can control HDAC4-linked
expression (Chen et al. 2014), and HDAC4/HDAC5 localization can be stimulus
regulated in striatal reward circuitry (Penrod et al. 2017).

Those mechanisms do not compel a broad basal Perturb-seq response in this
assay.  They are strongly localization-, stimulus-, and context-dependent:
loss of `Hdac4` at P16 in sparse recovered postmitotic nuclei is not the same
experiment as forcing HDAC4 into the nucleus, depolarizing neurons, blocking
basal NMDAR signaling, or challenging adult nucleus accumbens with cocaine.
The same-experiment `Hdac5` record is the most useful anchor because it tests a
close class-IIa paralog with the same CRISPR modality.  `Hdac5` gave no focal
DEGs at FDR 0.05 or 0.10, and the Distributed Agents corpus notes that even screen-wide
it produced only a single-gene `Chd5` response in a different limbic
glutamatergic group.  The corpus also reports that represented MEF2, CaMK, and
PKA perturbations did not phenocopy the `Hdac5` signature, and that basal
`Hdac5` loss did not induce canonical activity/MEF2 genes such as `Npas4`,
`Bdnf`, `Arc`, or `Fos`.

The MEF2 arm supplies the closest downstream counterfactual.  If loss of a
class-IIa HDAC in 151 thalamic glutamatergic cells were converted into a clean
MEF2 transcriptional output, `Mef2a`, `Mef2c`, or `Mef2d` perturbation should
look related.  Instead, the exact focal counts were 4 for `Mef2a`, 1 for
`Mef2c`, and 0 for `Mef2d`, with no profile-scale convergence to `Hdac5`.
Calcineurin and CaMK perturbations were similarly flat to weak.  A broad
chromatin regulator can be highly visible in this cell group, as `Sin3a` had
1,433 DEGs, so the `Hdac5`/MEF2 near-null is not simply a failure of the focal
cell group to detect transcriptional regulators.

My zero/nonzero decision is therefore a zero.  The call is driven primarily by
within-dataset evidence from `Hdac5`, `Mef2a`, `Mef2c`, `Mef2d`, CaMK, and
calcineurin perturbations; external HDAC4 literature is used as a prior that
identifies those as relevant analogs, not as a reason to override the flat
basal CRISPR signatures.  The expected count is closest to `Hdac5` and
`Mef2d`: no focal genes clearing FDR 0.05.  A one-gene self-transcript call is
plausible, but the target-transcript knockdown in this experiment is too
variable to justify moving the point estimate away from zero.

## Limits of the inference

- `Hdac5` is the only direct class-IIa HDAC perturbation in the training CSV;
  `Hdac7`, `Hdac9`, `Hdac3`, `Ncor1`, and `Ncor2` are absent.  The comparison
  is therefore paralog transfer, not a full complex-level interpolation.
- HDAC4 has cytoplasmic and nuclear functions, and the snRNA-seq endpoint
  cannot observe subcellular HDAC4 redistribution, dendritic phenotypes,
  synaptic physiology, survival before sorting, or stimulus-gated
  transcription.
- The perturbation is acute, mosaic AAV CRISPR with weak average target-RNA
  reduction; no functional indel or protein measurement is available for the
  hidden `Hdac4` guide pool.
- The count is an FDR-thresholded, power-dependent scalar.  The difference
  between 0 and 1 DEGs may be a self-target p-value crossing rather than a
  qualitatively distinct biological state.
- The biological prior is extrapolated from hippocampal, striatal, cultured
  neuron, and gain-of-nuclear-HDAC4 studies into juvenile thalamic glutamatergic
  nuclei.  That makes the zero call more uncertain than the observed `Hdac5`
  zero itself.

## Final point prediction

`Hdac4`: 0 DEGs.
