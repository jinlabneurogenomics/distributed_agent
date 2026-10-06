# Prediction trace

## Question and scope

The requested held-out target file contains one perturbation:

```text
Dgkd
```

I interpreted the task as a point prediction for the number of FDR<0.05
Wilcoxon differentially expressed measured genes after acute CRISPR loss of
`Dgkd` in `151 TH Prkcd Grin2c Glut` nuclei. `Dgkd` itself was completely held
out as a perturbation target, so I did not use a `Dgkd` expression signature or a
training count.

The endpoint is an assay-specific DEG count, not a direct estimate of lipid
kinase activity, developmental importance, excitability, or editing success. A
gene can be a real neuronal signaling gene and still produce zero steady-state
snRNA-seq DEGs in this 3-4 week mosaic postnatal assay.

## Sources used

- Training focal DEG counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest:
  `[local file: 055_Dgkd.csv]`.
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`, especially the curated `Dgke`
  reports `Dgke:F001` to `Dgke:F003` and the `Agk` lipid/mitochondrial
  contrast report `Agk:F003`.
- Distributed Agents runtime profile-neighbor calculation over the focal parquet rows,
  using `scores` as the signed expression vector and `pvals_adj<0.05` to label
  significant features.
- KEGG REST, `mmu:227333` in the 2026-09-23 KEGG GENES/KO release, for the
  placement of mouse `Dgkd` in the diacylglycerol kinase EC 2.7.1.107,
  glycerolipid, glycerophospholipid, phosphatidylinositol, and phospholipase D
  signaling annotations.
- UniProtKB, mouse `DGKD_MOUSE` / E9PUQ8, accessed 2026-09-23, for the
  curated biochemical annotation that DGKdelta phosphorylates DAG to
  phosphatidic acid and can modulate PKC/EGFR-related signaling.
- External literature:
  - Crotty et al. 2006, PNAS, DOI 10.1073/pnas.0604104103, PMID 17021016:
    germline `Dgkd` deficiency elevates DAG/PKC signaling and reduces EGFR
    abundance/signaling in mouse cells.
  - Leach et al. 2007, American Journal of Human Genetics, DOI
    10.1086/513019, PMID 17357084: disruption of `DGKD` was associated with
    seizures in a human translocation case, and `Dgkd` mutant mice showed
    abnormal electrographic activity.
  - Shulga et al. 2013, Biochemistry, DOI 10.1021/bi401178y, PMID 24090246:
    DGKdelta promoted lipogenesis in fibroblast/adipocyte contexts, whereas
    `Dgke` knockout mouse embryonic fibroblasts did not show the same lipid
    synthesis defect.
  - Sakai et al. 2018, Biochimie, DOI 10.1016/j.biochi.2018.05.017, PMID
    29859210: DGKdelta knockdown in C2C12 myoblasts affected cyclin D1,
    myogenin, and conventional/novel PKC phosphorylation during myogenic
    differentiation.

## Computational checks

1. The focal training table has 1,674 perturbations. Its DEG-count distribution
   is sparse: median 0, 75th percentile 1, 469/1,674 perturbations nonzero.

2. Searching the training counts for `Dgk*` perturbations found only one direct
   DGK-family perturbation:

   ```text
   Dgke  n_degs=1
   ```

   Thus no training `Dgkd`, `Dgka`, `Dgkb`, `Dgkg`, `Dgkh`, `Dgki`, `Dgkk`,
   `Dgkq`, or `Dgkz` signature was available.

3. To avoid a full read of the 616M-row parquet, I used Parquet row-group
   metadata to find the row groups whose `group_name` range overlapped
   `151 TH Prkcd Grin2c Glut` and scanned only row groups 546-580. I then
   filtered to biologically relevant analogs and counterexamples:
   `Dgke`, `Agk`, `Plcb1`, `Prkca`, `Prkcg`, `Kdr`, `Nrp1`, `C3`, `Npy1r`,
   `Limk1`, `Cfap69`, `Dnajc13`, `Slc25a4`, `Tomm40`, `Dnajc19`, `Afg3l2`,
   `Yme1l1`, `Clpp`, `Lonp1`, and `Micu1`.

   The focal rows had 17,259 measured genes for each of the 20 targets. The
   most relevant focal counts were:

   | perturbation | focal n_degs | n_pert | significant FDR<0.05 genes |
   | --- | ---: | ---: | --- |
   | `Dgke` | 1 | 225 | `Dgke` only |
   | `Plcb1` | 0 | 160 | none |
   | `Prkca` | 0 | 169 | none |
   | `Prkcg` | 1 | 175 | `Prkcg` only |
   | `Kdr` | 0 | 167 | none |
   | `Nrp1` | 0 | 182 | none |
   | `C3` | 0 | 231 | none |
   | `Agk` | 0 | 139 | none |
   | `Slc25a4` | 1 | 240 | `Slc25a4` only |
   | `Tomm40` | 1 | 224 | `Tomm40` only |
   | `Dnajc19` | 0 | 180 | none |
   | `Afg3l2` | 0 | 180 | none |
   | `Yme1l1` | 0 | 106 | none |
   | `Clpp` | 0 | 166 | none |
   | `Lonp1` | 0 | 270 | none |
   | `Micu1` | 0 | 171 | none |

4. I used Distributed Agents runtime `profile_neighbors` on the focal group to inspect
   whole-vector Pearson/cosine similarities and signed top-tail overlaps for
   `Dgke`, `Agk`, `Plcb1`, `Prkca`, `Prkcg`, `Kdr`, `Nrp1`, and `C3`. `Dgke`
   was the only direct DGK anchor. Its closest whole-profile neighbors in this
   run were numerically weak: `Six5`, `Zkscan1`, and `Lrp4` had Pearson
   correlations of only 0.0758, 0.0707, and 0.0671 to `Dgke`, with 100-gene
   signed-tail overlap coefficients of 0.03 or less in the positive tail and
   0.02 in the negative tail. Its best 100-gene tail overlaps were also only
   0.09 or lower. I used this as evidence against a hidden broad DGK-like
   transcriptional module in the focal group.

## Target-specific reasoning

### Dgkd

`Dgkd` encodes the type II diacylglycerol kinase DGKdelta, which converts DAG
to phosphatidic acid and thereby tunes signaling through DAG effectors such as
PKC; this KEGG/UniProt placement is supported experimentally by Crotty et al.
2006 for PKC/EGFR signaling. It is not biologically inert: Leach et al. 2007
linked `DGKD` disruption to seizures and reported abnormal electrographic
activity in `Dgkd` mutant mice.

Those external phenotypes do not map cleanly onto a large acute transcriptional
response in this dataset. The strongest available same-pathway readout is
`Dgke`, the sole measured DGK-family perturbation in the focal training set.
`Dgke` had only 1 focal DEG, and that DEG was `Dgke` itself
(`log2FC=-0.586`, `p_adj=5.97e-8`). The same-experiment Distributed Agents corpus
classified `Dgke` as a buffered response across all recovered neuronal groups:
its curated report notes that no non-`Dgke` gene reached FDR<0.10 in 23 measured
cell groups, even where the target transcript itself was detectably depleted.
That is the closest direct evidence for how the DAG-to-PA kinase family behaves
under this postnatal neuronal CRISPR design.

I then checked pathway neighbors that could have argued for a nonzero
prediction even if `Dgke` were too specialized. Upstream PLC/DAG production and
downstream conventional PKC signaling were still flat in the focal group:
`Plcb1` had 0 DEGs, `Prkca` had 0, and `Prkcg` had only self knockdown as its
single DEG. Vascular/PI-cycle comparators from the same `Dgke` report were also
flat (`Kdr`, `Nrp1`, and `C3` all 0). `Agk`, another lipid kinase that also
converts DAG to phosphatidic acid but in a mitochondrial setting, had 0 DEGs in
this focal group and was flat rather than convergent with `Dgke` in the
Distributed Agents corpus.

This makes a large `Dgkd` response unlikely. The external developmental,
EGFR/PKC, lipogenesis, and myogenic literature mainly concerns germline,
embryonic, fibroblast, adipocyte, skeletal-muscle, beta-cell, or evoked
electrophysiological contexts. The held-out assay is a partial, sparse,
juvenile, postmitotic neuronal loss-of-function perturbation and measures
basal nuclear RNA at 3-4 weeks, so it can miss lipid pool changes, protein-level
EGFR turnover, basal synaptic physiology, and seizure susceptibility.

The one remaining reason to predict 1 instead of 0 is self-transcript depletion:
`Dgke`, `Prkcg`, `Slc25a4`, `Tomm40`, and `Dnajc13` are examples where a flat
downstream response still yielded exactly the target gene as a DEG. I left the
point prediction at zero because self-knockdown is target-expression- and
guide-dependent, most flat perturbations in the training distribution did not
register even a self-DEG, and the within-dataset DAG/PKC perturbations did not
show a reproducible downstream state that could add genes beyond a possible
`Dgkd` row.

Prediction for `Dgkd`: **0 DEGs**.

## Limits

- `Dgkd` itself was held out, and `Dgke` was the only `Dgk*` perturbation in
  the focal training counts. The direct paralog evidence is therefore thin and
  comes from a DGK isoform with different regulatory domains and lipid
  specificity.
- The screen has no lipidomics, indel sequencing, DGKdelta protein abundance,
  DAG/PA compartment readout, EGFR turnover assay, electrophysiology, or evoked
  activity measurement. A zero RNA prediction does not exclude altered DAG-PKC
  signaling.
- The external positive evidence for `Dgkd` comes largely from germline
  disruption or proliferative non-neuronal cells. Those systems are useful for
  mechanism but imperfect analogs for sparse AAV CRISPR in postmitotic Allen
  `151 TH Prkcd Grin2c Glut` nuclei.
- The exact zero-versus-one call is dominated by whether the `Dgkd` transcript
  itself would pass the single-cell Wilcoxon FDR threshold. The training data
  show both outcomes among otherwise buffered genes, so this is the weakest
  part of the prediction.
