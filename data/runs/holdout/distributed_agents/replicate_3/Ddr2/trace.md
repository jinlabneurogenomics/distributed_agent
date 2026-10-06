# Ddr2 prediction trace

## Question and resolved ambiguities

The held-out manifest for this run contains one requested perturbation:

```tsv
target_name
Ddr2
```

I therefore predicted the number of genes with `pvals_adj < 0.05` after `Ddr2`
loss in `151 TH Prkcd Grin2c Glut` cells. The requested target is absent
from both supplied training files, so I treated the supplied count CSV and
parquet as analog evidence only; I did not assume any direct `Ddr2` expression
or DEG count was available. The count to predict is assay-specific and includes
whatever measured gene rows pass the Wilcoxon Benjamini-Hochberg cutoff in the
focal cell group.

## Sources used

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, giving observed focal-cell
  `n_degs` for 1,674 non-held-out perturbations.
- `training_de_all_cell_groups.parquet`, filtered to `151 TH Prkcd Grin2c Glut`
  and to candidate ECM, receptor-tyrosine-kinase, and Ras/MAPK perturbations.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
  `Ddr2` itself was held out and had no target-centered Distributed Agents context, but
  the corpus contained relevant same-experiment claims for `Fbn1`, `Adamts17`,
  `Braf`, `Map2k1`, `Ntrk2`, FGF/ERBB/RET/insulin-IGF receptor perturbations,
  and TGF-beta/BMP-SMAD perturbations.
- Distributed Agents runtime `profile_compare` / `profile_inspect` over 20 held-in
  candidate analogs in the focal group, used to inspect signed log-fold-change
  neighborhoods and verify that zero-DEG ECM/receptor genes did not hide an
  obvious shared FDR-level module.
- External DDR biology from the primary DDR discovery papers and review
  literature: DDR family receptors are collagen-activated receptor tyrosine
  kinases rather than ligand-gated neurotrophin or FGF receptors
  (Vogel et al. 1997, doi:10.1016/S1097-2765(00)80003-9; Shrivastava et al.
  1997, doi:10.1016/S1097-2765(00)80004-0), and DDR signaling is usually tied
  to collagen-rich extracellular-matrix remodeling, Src/Shc/ERK and related
  cascades rather than to a dedicated constitutive neuronal transcription
  program (Fu et al. 2013, doi:10.1074/jbc.R112.444158).

## Computations over the supplied dataset

I first summarized the training endpoint in the focal cell group. The distribution
was highly zero-inflated: 1,205 of 1,674 held-in targets had `n_degs = 0`, 276 had
one DEG, 87 had 2 to 9 DEGs, and only 106 had at least 10. The median was 0, the
75th percentile was 1, and the 95th percentile was 18.

I then assembled a candidate set around the expected `Ddr2` biology: collagens
and other ECM genes (`Col11a1`, `Col2a1`, `Fbn1`, `Adamts17`), integrin or
matrix-linked receptors (`Itga2`, `Itgb1`, `Pdgfrb`), TGF-beta/BMP-SMAD
components, other receptor tyrosine kinases, and Ras/MAPK nodes. The direct
paralog `Ddr1` was not in the held-in 1,674-target count table, so there was no
same-family paralog response to copy.

For the focal rows in the parquet, I used a narrow Parquet filter:

```python
pq.read_table(
    parquet_path,
    columns=[
        "names",
        "gene_target",
        "logfoldchanges",
        "pvals_adj",
        "n_pert_matched",
        "n_ctrl_matched",
    ],
    filters=[
        ("group_name", "=", "151 TH Prkcd Grin2c Glut"),
        ("gene_target", "in", candidate_targets),
    ],
)
```

Each profiled candidate had 17,259 measured focal-cell rows. The zero-call ECM
and receptor candidates still had adequate matched perturbed nuclei for this
assay, for example `Fbn1` 217, `Adamts17` 191, `Col11a1` 167, `Col2a1` 304,
`Itga2` 154, `Itgb1` 110, `Pdgfrb` 195, `Fgfr1` 210, `Fgfr2` 202, `Fgfr3` 183,
`Erbb3` 202, `Erbb4` 193, `Ntrk1` 177, and `Ret` 240, all against 23,679
matched controls.

## Target-specific analog evidence

### Ddr2

`Ddr2` encodes discoidin domain receptor 2, a collagen-activated receptor
tyrosine kinase. The most literal missing analog would have been the other
discoidin-domain receptor, `Ddr1`, but `Ddr1` was absent from the training-count
universe. I therefore treated same-pathway evidence as calibration rather than
as a direct paralog imputation.

The extracellular-matrix lane was almost completely flat in the same focal cell
group.

| held-in perturbation | focal `n_degs` | expression evidence and relevance |
| --- | ---: | --- |
| `Fbn1` | 0 | A major matrix glycoprotein and TGF-beta/latent-complex scaffold; no `151 TH Prkcd Grin2c Glut` row had `pvals_adj < 0.05`. The Distributed Agents `Fbn1:F003` finding reports that `Fbn1` did not phenocopy represented TGF-beta receptors, SMADs, integrin `Itgb1`, or `Adamts17`, and claim `claim:2f795acb1af0a8d532a9` summarizes the absence of an ECM/TGF-beta/BMP-SMAD module in postmitotic neurons. |
| `Adamts17` | 0 | ECM metalloprotease/microfibril-associated comparator; no focal FDR-significant rows. The corpus pairs it with `Fbn1` as another matrix perturbation that failed to engage the expected ECM-linked BMP/TGF-beta transcriptional program. |
| `Col11a1`, `Col2a1` | 0, 0 | Collagen structural genes, both with no focal FDR-significant rows. They are imperfect because they are ligands/ECM components rather than collagen receptors, but their flatness argues that single-gene disruption of matrix genes represented in this NeuN-enriched assay does not by itself create a broad nuclear RNA response in the thalamic neurons. |
| `Itga2`, `Itga6`, `Itga7`, `Itga8`, `Itga9`, `Itgb1` | all 0 | Integrins are the other major collagen/ECM receptor layer. `Itga2` and `Itgb1` were directly inspected in the parquet in the focal group and had zero FDR-significant rows; the count table also had zeros for the other represented alpha integrins. These are receptor counterexamples to a generic ECM-contact perturbation effect. |
| `Pdgfrb` | 0 | A mesenchymal/vascular RTK comparator, not a DDR-family member. It was flat in the focal neurons, supporting the idea that cell-type-displaced RTKs tied to matrix or vascular biology are usually silent in this NeuN-positive context. |

The receptor-tyrosine-kinase and Ras/MAPK lanes supplied useful positive
controls without moving the prediction above zero. The assay can detect a tiny
RTK/MAPK-like output in the focal group: `Ntrk2` had 3 DEGs
(`Ntrk2`, `Atp2a2`, `Vgf` all down), `Braf` had 4 (`Atp2a2`, `Ptpn5`, `Vgf`,
`Unc13a` down), and `Map2k1` had 4 (`Vgf`, `Ptpn5`, `Etv5`, `Unc13a` down).
The Distributed Agents corpus describes this as a sparse `Vgf`/`Ptpn5`/`Unc13a` thalamic
module shared by `Braf` and `Map2k1`, with partial `Ntrk2` overlap
(`claim:5f4082f202c79d3b3fcc`).

Those positives were bounded by many flat upstream receptors and pathway
neighbors. `Fgfr1`, `Fgfr2`, `Fgfr3`, `Erbb3`, `Erbb4`, `Ntrk1`, `Ntrk3`, `Ret`,
`Met`, `Axl`, `Mertk`, `Igf1r`, `Insr`, `Sos1`, `Hras`, `Kras`, `Raf1`,
`Map2k2`, `Mapk1`, and `Mapk9` all had `n_degs = 0` in `151 TH Prkcd Grin2c
Glut`. The internal corpus independently states that the focal `Braf`/`Map2k1`
RNA module was not reproduced by upstream receptor or RAS perturbations
(`claim:4c017eca385896deb7a3` and `claim:4af1e0ceaef9adda14b9`) and that
represented FGF/FGFR/RAS/ERK, ERBB, insulin/IGF/PI3K-AKT, RET/GDNF, and
Trk-family receptors are mostly buffered or receptor-specific rather than
members of one shared receptor-level basal neuronal transcriptome.

I also checked TGF-beta/BMP-SMAD genes because matrix receptors can couple to
latent TGF-beta/ECM remodeling biology in non-neuronal settings. `Tgfbr1`,
`Tgfbr2`, `Tgfbr3`, `Bmpr1a`, `Bmpr1b`, `Bmpr2`, `Acvr1`, `Acvr2a`, `Smad3`,
`Smad4`, and `Smad9` all had zero focal DEGs; `Smad2` had only one
(`Cpne7`, log2FC -0.411, FDR 0.0167). The Distributed Agents claims for
TGF-beta/activin/BMP receptor-SMAD perturbations likewise describe no coherent
shared basal transcriptional module in postnatal neuronal snRNA-seq.

Taken together, these data make a `Ddr2` nonzero call unlikely. The strongest
biological prior for `Ddr2` points to collagen-ECM receptor signaling, but the
held-in ECM, integrin, collagen, and matrix-associated receptor analogs are
zero in the focal group. The only receptor/MAPK axis with a detectable focal
effect is a tiny TrkB/BRAF/MEK1-centered module, and the training data show that
most upstream RTKs, including FGFR and ERBB receptors much closer to canonical
neuronal signaling than DDR2, do not reach even a one-gene FDR response. I
therefore predict that acute sparse `Ddr2` loss in these NeuN-enriched thalamic
glutamatergic neurons will have no FDR<0.05 DEGs:

```tsv
target_name	predicted_n_degs
Ddr2	0
```

## Limits of the reasoning

- No held-in `Ddr1` perturbation was available, so the prediction extrapolates
  from pathway neighbors rather than from a true DDR-family paralog.
- The local ECM comparators are imperfect: collagens and `Fbn1` perturb matrix
  ligands/scaffolds rather than the receptor kinase, while integrins sense ECM
  through different adhesome machinery.
- snRNA-seq after P16 sparse CRISPR measures durable nuclear RNA abundance. It
  cannot exclude DDR2 effects on collagen binding, receptor phosphorylation,
  dendrite morphology, or local signaling that never become FDR-significant
  nuclear transcripts.
- The profile-neighbor output for zero-DEG perturbations contains weak
  full-vector correlations and large unadjusted log-fold changes for rare
  genes; I treated those as noise-scale or non-specific unless the corresponding
  genes survived BH correction or formed a Distributed Agents-supported module.
- The prediction assumes the NeuN-enriched focal nuclei do not become dependent
  on a strong collagen-DDR2 autocrine loop under the viral CRISPR conditions.
  That is the best-supported assumption from the training matrix/RTK analogs,
  but it is still an extrapolation because `Ddr2` itself was held out.
