# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguity

The requested held-out target file contains one perturbation:

```text
Ffar1
```

I interpreted the task as a point prediction of the number of measured genes with
`pvals_adj < 0.05` after an acute AAV-CRISPR loss-of-function perturbation of
`Ffar1` in the focal `151 TH Prkcd Grin2c Glut` neuronal group.  I used the
training `n_degs` CSV as the endpoint calibration and used the full parquet only
for same-experiment expression-signature evidence from non-held-out
perturbations.  `Ffar1` was completely absent as a perturbation target from both
training inputs, so all use of the parquet below is through observed analogs or
counterexamples.

## Sources used

- Input endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Input differential-expression matrix:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested-target manifest:
  `[local file: 075_Ffar1.csv]`
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`.  I queried target context,
  related targets, claims, and findings for `Ffar1`; the release had no direct
  `Ffar1` claims or finding neighborhood, so no internal curated edge was used as
  positive evidence.
- Distributed Agents runtime profile comparison of selected observed receptor
  perturbations in `151 TH Prkcd Grin2c Glut`.
- PubMed literature for FFAR1/GPR40 biology:
  - Itoh et al. 2003, *Nature*, DOI `10.1038/nature01478`, PMID `12629551`.
  - Fujiwara et al. 2005, *American Journal of Physiology. Endocrinology and
    Metabolism*, DOI `10.1152/ajpendo.00035.2005`, PMID `15914509`.
  - Schnell et al. 2006, *Molecular and Cellular Endocrinology*, DOI
    `10.1016/j.mce.2006.09.013`, PMID `17101212`.
  - Aizawa et al. 2016, *Journal of Pharmacological Sciences*, DOI
    `10.1016/j.jphs.2016.09.007`, PMID `27979701`.
  - Nakamoto et al. 2017, *PLOS ONE*, DOI `10.1371/journal.pone.0180610`,
    PMID `28723961`.
  - Kimura et al. 2019, *Physiological Reviews*, DOI
    `10.1152/physrev.00041.2018`, PMID `31487233`.
  - Dragano et al. 2023, *Molecular Metabolism*, DOI
    `10.1016/j.molmet.2023.101840`, PMID `38036170`.

## Computational checks over the input data

1. Loaded the held-out manifest and confirmed that `Ffar1` is the only requested
   target.
2. Loaded the focal-cell endpoint CSV.  It contains 1,674 non-held-out
   perturbations.  The response distribution is sparse: 1,205/1,674 are zero,
   the median is 0, the 75th percentile is 1, the 90th percentile is 2, and only
   the top 5% exceed 18 DEGs.
3. Filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` with the
   columns `names`, `gene_target`, `logfoldchanges`, `pvals_adj`,
   `n_pert_matched`, and `n_ctrl_matched`.  The focal slice has
   28,891,566 rows: 1,674 perturbations by 17,259 measured genes.
4. Matched candidate analog names to the training count table, then inspected
   the focal parquet for their FDR-passing features:

   ```python
   focal = pd.read_parquet(
       training_de_parquet,
       columns=[
           "names", "group_name", "gene_target", "logfoldchanges",
           "pvals_adj", "n_pert_matched", "n_ctrl_matched",
       ],
       filters=[("group_name", "=", "151 TH Prkcd Grin2c Glut")],
   )
   significant = focal[focal.pvals_adj < 0.05]
   ```

5. Compared a representative GPCR panel with the Distributed Agents runtime profile tools
   using `logfoldchanges` as signed profile values and `pvals_adj < 0.05` as the
   significance call.  Because `Ffar1` itself is held out and has no observed
   profile, this was not a nearest-neighbor search for `Ffar1`; it tested whether
   related receptor knockouts form a recurring observed state.

## Same-experiment analogs and counterexamples

### Direct FFAR family

No `Ffar2`, `Ffar3`, or `Ffar4` perturbation was present in the training count
table, and there was no `Gpr40`/`Gpr120` alias target.  I therefore did not have
a true same-ligand FFAR paralog perturbation to transfer from.

### Neuronal and orphan GPCR perturbations

The closest broad class evidence came from observed GPCRs.  I treated these as
counterexamples rather than as strict paralogs: they are rhodopsin-like
cell-surface receptors with neuronal second-messenger coupling, but they do not
sense fatty acids.

| training target | observed `n_degs` | focal-cell expression evidence |
|---|---:|---|
| `Gpr156` | 0 | no measured gene passed FDR |
| `Gpr161` | 0 | no measured gene passed FDR |
| `Gpr179` | 0 | no measured gene passed FDR |
| `Gpr45` | 0 | no measured gene passed FDR |
| `Gprc5b` | 0 | no measured gene passed FDR |
| `Gpr158` | 1 | only `Gpr158` itself was significant, down by log2FC -0.991 |
| `Gprasp2` | 1 | only `Gprasp2` itself was significant, down by log2FC -0.491 |
| `Htr1a`, `Htr1b`, `Htr1f`, `Htr2a`, `Htr2b`, `Htr2c`, `Htr3a`, `Htr3b`, `Htr4`, `Htr6`, `Htr7` | 0 each | no measured gene passed FDR for any serotonin-receptor perturbation |
| `Drd2`, `Drd4`, `Drd5` | 0 each | no measured gene passed FDR |
| `Grm5`, `Grm6`, `Grm8` | 0 each | no measured gene passed FDR |
| `Grm1` | 1 | only `Grm1` itself was significant, down by log2FC -0.438 |
| `Grm7` | 1 | only `Grm7` itself was significant, down by log2FC -0.364 |
| `Chrm2`, `Chrm3` | 0 each | no measured gene passed FDR |
| `Galr1` | 0 | no measured gene passed FDR |
| `Sstr5` | 0 | no measured gene passed FDR |
| `Npy1r`, `Npy2r`, `Npy5r` | 0 each | no measured gene passed FDR |
| `Oprd1`, `Oprk1`, `Oprm1` | 0 each | no measured gene passed FDR |
| `Cnr1` | 1 | one significant non-target feature, `Srcap`, log2FC +0.300 |

Across these 37 receptor targets, 32 had 0 DEGs and the maximum was 1 DEG.  Four
of the five one-DEG cases were only the targeted receptor transcript.  That is
particularly important for `Ffar1`: `names == "Ffar1"` had zero rows in the
focal parquet slice, so the held-out endpoint cannot gain even a one-gene count
from direct target down-regulation.

The runtime profile comparison also failed to reveal a coherent receptor state.
For example, `Gpr156`, `Gpr161`, and `Htr2a` had no significant genes at all,
while `Gpr158` and `Gprasp2` had one each.  Pairwise receptor profiles had zero
overlap among positive or negative significant features; the apparent whole
profile correlations were driven by weak, non-FDR features rather than by a
shared FDR-passing signature.

### FFAR1 effector-side nodes

FFAR1/GPR40 is best established as a medium/long-chain fatty-acid GPCR that can
amplify secretion through G-protein, phospholipase C, and calcium signaling
(Itoh et al. 2003; Fujiwara et al. 2005; Schnell et al. 2006; Kimura et al.
2019).  I therefore also checked observed nodes on or near the receptor's
generic effector side:

| training target | observed `n_degs` | interpretation |
|---|---:|---|
| `Gnas` | 0 | heterotrimeric G-protein component; no broad focal response |
| `Gnao1` | 1 | only `Gnao1` itself was significant |
| `Plcb1` | 0 | proximal PLC arm; no focal response |
| `Itpr1` | 0 | IP3/calcium release arm; no focal response |
| `Camk2a`, `Camk2g` | 0 each | calcium/CaMK nodes; no focal response |
| `Camk2b` | 1 | only `Camk2b` itself was significant |
| `Prkca` | 0 | PKC node; no focal response |
| `Prkcg` | 1 | only `Prkcg` itself was significant |
| `Mapk1` | 0 | MAPK node; no focal response |
| `Map2k2` | 0 | MAPK node; no focal response |
| `Map2k1` | 4 | the small nonzero set was `Vgf`, `Ptpn5`, `Unc13a`, `Etv5` |
| `Pkd1` | 0 | no focal response |
| `Cd36` | 0 | fatty-acid transporter/scavenger node; no focal response |
| `Acsl4` | 1 | only `Acsl4` itself was significant |

The effector-side comparison is imperfect because many of these proteins are
shared by multiple receptors and some are not direct FFAR1 transducers in
neurons.  Still, the training data argue that partial loss of these signaling
nodes is usually not enough to push this focal cell group into a high-DEG state.

## Biological rationale for `Ffar1`

`Ffar1`, also called `Gpr40`, encodes a GPCR activated by medium- and long-chain
free fatty acids.  Its clearest acute signaling biology is in pancreatic beta
cells, where fatty acids activate GPR40/FFAR1 to raise intracellular calcium via
PLC- and calcium-channel-dependent mechanisms and amplify glucose-stimulated
insulin secretion (Itoh et al. 2003; Fujiwara et al. 2005; Schnell et al. 2006).
FFAR1 is also functional in the nervous system: germline `Ffar1` deficiency or
pharmacologic antagonism can alter pain and affective behaviors, and more recent
work shows that hypothalamic `Ffar1` in POMC neurons contributes to energy
balance under metabolic perturbation (Aizawa et al. 2016; Nakamoto et al. 2017;
Dragano et al. 2023).

Those mechanisms do not strongly imply a broad, cell-autonomous transcriptional
response in juvenile postmitotic `151 TH Prkcd Grin2c Glut` nuclei after sparse
acute CRISPR.  The positive brain papers are in specialized hypothalamic or
pain-modulatory circuits, often with germline knockout, pharmacology, shRNA, or
whole-animal metabolic/stress readouts.  The training dataset gives the more
direct calibration for this assay: perturbing comparable neuronal receptors
almost never yielded more than direct loss of the receptor transcript, and the
available G-protein/PLC/calcium/MAPK and lipid-handling nodes were similarly
silent or nearly silent in the focal cell group.

I therefore predict that `Ffar1` loss will be below the Wilcoxon/BH detection
threshold and will produce no FDR-significant measured genes:

```text
Ffar1 -> predicted_n_degs = 0
```

## Limits of the inference

- No true FFAR paralog perturbation was observed in training.  The receptor
  analogs above are class-level counterexamples rather than same-ligand-family
  substitutes.
- The Distributed Agents corpus had no direct curated `Ffar1` neighborhood in this
  release, so the target-specific decision relied on the raw training matrix and
  external FFAR1 literature.
- The parquet has no `Ffar1` measured-gene rows in the focal slice.  That helps
  exclude an auto-regulatory one-DEG outcome, but it also prevents any
  expression-pattern reasoning from the held-out gene's own abundance.
- GPCRs can be highly cell-state- and ligand-dependent.  If this Allen cell
  group unexpectedly expresses functional FFAR1 and receives an endogenous fatty
  acid signal in the experiment, a small response is possible; the prediction is
  that such a response will remain below the FDR 0.05 endpoint.
