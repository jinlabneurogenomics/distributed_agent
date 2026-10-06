# Held-out DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and resolved ambiguities

The requested manifest contains one held-out perturbation, `Klrk1`. I interpret
the endpoint as the exact focal-cell count in the training CSV: the number of
measured genes with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`. I used the
0.05 threshold for the final prediction even when the Distributed Agents corpus described
some same-experiment findings at FDR < 0.10.

Because `Klrk1` was completely held out from the supplied parquet and focal
training count table, I did not try to infer a self-row or read out a
`Klrk1` signature. The prediction is an extrapolation from non-held-out immune
and lymphocyte receptor perturbations plus the known biology of mouse Klrk1/NKG2D.

## Sources used

- Supplied focal training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Supplied DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest:
  `[local file: 120_Klrk1.csv]`.
- Distributed Agents same-experiment semantic corpus
  `perturbai-july-260713-sourceguard-1773-v1`.
- Distributed Agents runtime profile comparison over focal-cell Wilcoxon score vectors,
  written locally to `profile_compare_immune_analogs.json` and inspected through
  `profile_inspect_immune_analogs.json`.
- UniProtKB/Swiss-Prot entry `O54709` for mouse KLRK1/NKG2D, queried as a
  reviewed database entry.
- Literature on NKG2D ligands, expression, and adaptor usage:
  Bauer et al. 1999, Science, doi:10.1126/science.285.5428.727, PMID:10426993;
  Wu et al. 1999, Science, doi:10.1126/science.285.5428.730, PMID:10426994;
  Cerwenka et al. 2000, Immunity, doi:10.1016/S1074-7613(00)80222-8,
  PMID:10894171; Diefenbach et al. 2000, Nature Immunology,
  doi:10.1038/77793, PMID:11248803; Jamieson et al. 2002, Immunity,
  doi:10.1016/S1074-7613(02)00333-3, PMID:12150888; Gilfillan et al. 2002,
  Nature Immunology, doi:10.1038/ni857, PMID:12426564; Diefenbach et al. 2002,
  Nature Immunology, doi:10.1038/ni858, PMID:12426565; Rosen et al. 2004,
  Journal of Immunology, doi:10.4049/jimmunol.173.4.2470, PMID:15294961.

## Dataset calibration

The manifest has exactly one target:

```text
Klrk1
```

The focal training table has 1,674 non-held-out biological targets. It is highly
zero-inflated: 1,205/1,674 targets have `n_degs = 0`; the median is 0; only
469/1,674 have any FDR 0.05 DEG; and 1,512/1,674 have two or fewer DEGs.

For focal-cell analog checks, I queried the parquet with:

```sql
select gene_target,
       any_value(n_pert_matched) as n_pert_matched,
       sum(pvals_adj < 0.05) as n_fdr05,
       min(pvals_adj) as min_fdr,
       sum(pvals_adj < 0.10) as n_fdr10
from read_parquet('training_de_all_cell_groups.parquet')
where group_name = '151 TH Prkcd Grin2c Glut'
  and gene_target in (<immune comparators>)
group by gene_target;
```

The most relevant focal observations were:

| training target | why inspected | `n_degs` at FDR 0.05 in the focal cell group |
|---|---:|---:|
| `Cd247` | ITAM-bearing lymphocyte receptor adaptor; TCR/CD3 analog | 0 |
| `Cd3d` | same CD3/TCR complex class | 0 |
| `Cd3e` | same CD3/TCR complex class | 0 |
| `Cd3g` | same CD3/TCR complex class | 0 |
| `Cd4` | lymphocyte coreceptor | 0 |
| `Cd79a` | BCR immunoreceptor subunit | 0 |
| `Cd79b` | BCR immunoreceptor subunit | 0 |
| `Cblb` | immune-receptor negative regulator linked to PI3K/Src signaling | 0 |
| `Fyn` | Src-family kinase and pleiotropic proximal immunoreceptor kinase | 0 |
| `Tlr2`, `Tlr3`, `Tlr4`, `Tlr7` | innate immune receptor controls | all 0 |
| `Ifnar1`, `Ifngr1` | cytokine receptor controls | both 0 |
| `Nfkb1`, `Irf8` | immune transcriptional effectors | both 0 |
| `Ptprc`, `Itgb2`, `Csf1r`, `Cx3cr1` | leukocyte or microglial lineage receptors | all 0 |
| `Stat1` | IFN/JAK-STAT effector; boundary case | 1, and the one gene was `Stat1` itself |
| `Clec16a` | rejected superficial "Clec" name match; intracellular autophagy/proteostasis gene | 0 |

The selected lymphoid/innate candidate rows each had 17,259 measured genes in
the focal group, so these zeros are not missing profiles. Matched perturbed-cell
counts for the table above ranged from 89 to 258 nuclei. I also compared 15
available immune analogs by their focal-cell Wilcoxon `scores` vectors. Fourteen
had no FDR 0.05 feature; `Stat1` had one. Pairwise score cosines between
`Cd247` or `Cd3e` and CD3/BCR/TLR/IFN candidates were small, roughly
-0.04 to 0.05 in the inspected pairs, and no positive or negative FDR 0.05
feature was shared. That argues against a weak, recurrent, subthreshold
lymphocyte-receptor module hiding below the hard count threshold.

The same-experiment Distributed Agents corpus gave the same interpretation at a broader
atlas scale. It had no `Klrk1` target context, as expected for this held-out
gene, but it did contain relevant negative modules:

- For `Cd247`, `Cd3e`, `Cd3d`, `Cd3g`, `Cd4`, `Cd79a`, and `Cd79b`, the corpus
  summarized that represented CD3/TCR, Cd4/MHC, and BCR/immunoreceptor
  perturbations were flat, sparse, or nonconvergent in NeuN-positive neuronal
  nuclei rather than forming a latent immune-receptor RNA program.
- For `Tlr4`, the corpus summarized that represented TLR/CD14 and innate
  receptor perturbations under unchallenged neuronal conditions did not form a
  coherent TLR/PRR-to-NF-kappaB/IRF module.
- For `Stat1`, the corpus summarized that basal loss of represented IFN
  receptor, STAT, and IRF pathway genes did not engage a coherent neuronal
  IFN/ISG/MHC-I inflammatory transcriptional module.
- For `Fyn`, the corpus reported no downstream FDR<0.10 response in any
  recovered neuronal brain group and no convergence with either
  immunoreceptor or NMDAR/Reelin candidate pathways in the snRNA-seq readout.

## Target-specific reasoning

### Klrk1

`Klrk1` encodes mouse NKG2D, a type II C-type lectin-like activating receptor.
The known protein biology is strongly lymphoid and myeloid rather than neuronal:
NKG2D is expressed on NK cells, activated CD8+ alpha-beta T cells, subsets of
gamma-delta T cells/NKT cells, and activated macrophages; its ligands include
stress-induced Rae1 and H60 family proteins on tumor or injured cells
(Cerwenka et al. 2000; Diefenbach et al. 2000; Jamieson et al. 2002). The
canonical signaling receptor is multisubunit: DAP10/`Hcst` supports NKG2D
surface expression and PI3K recruitment, and short mouse NKG2D isoforms can
also associate with DAP12/`Tyrobp` to signal through protein tyrosine kinases
(Wu et al. 1999; Gilfillan et al. 2002; Diefenbach et al. 2002; Rosen et al.
2004). UniProtKB/Swiss-Prot `O54709` likewise curates KLRK1 as an NK/T-cell
activating and costimulatory cell-surface receptor.

The perfect internal comparisons would have been `Hcst`, `Tyrobp`, KLR-family
paralogs, and NKG2D ligands such as `Raet1*` or `H60*`, but those were not
available as training perturbations. I therefore used four weaker but informative
negative neighborhoods.

First, the TCR/CD3 and BCR immunoreceptor components are the closest represented
lineage-matched receptors. They are not NKG2D subunits, but they test whether
lymphocyte receptor adaptors can trigger a cryptic cell-autonomous RNA program
in NeuN-enriched postnatal neurons. `Cd247`, `Cd3d`, `Cd3e`, `Cd3g`, `Cd79a`,
and `Cd79b` all had `n_degs = 0` in `151 TH Prkcd Grin2c Glut`. The corpus
also reported that these targets jointly fail to form a latent TCR/CD3/BCR-like
module across NeuN-positive neuronal nuclei. That is the central within-dataset
evidence for a `Klrk1` zero.

Second, proximal immunoreceptor signaling nodes did not show a focal response.
`Fyn` had `n_degs = 0` at FDR 0.05 in the focal group, with only one FDR 0.10
near-miss. `Cblb`, `Nfkb1`, and `Itgb2` were also 0. These are pleiotropic
genes and imperfect NKG2D analogs, but their flatness means the screen was not
silently recovering a broad Src/PI3K/NF-kappaB immune-receptor state.

Third, non-lymphoid immune receptors were also silent in the same focal group:
`Tlr2`, `Tlr3`, `Tlr4`, `Tlr7`, `Ifnar1`, `Ifngr1`, `Csf1r`, `Cx3cr1`, and
`Ptprc` were all 0. The single `Stat1` DEG was `Stat1` itself, not a broader
interferon-stimulated gene set. That is a counterexample boundary rather than
positive evidence for `Klrk1`: immune genes can be represented in the library
and still lack a ligand- and lineage-gated transcriptional program in the
unstimulated thalamic glutamatergic neurons assayed here.

Fourth, I explicitly rejected a superficial C-type lectin name match. `Clec16a`
is an intracellular autophagy/endolysosomal and proteostasis-associated gene,
not an NK cell activating receptor. It had no FDR 0.05 focal DEGs, but its
biology and the Distributed Agents corpus place it in a weak proteostasis/autophagy
neighborhood rather than the NKG2D adaptor axis, so I did not use it as a
positive or quantitative `Klrk1` analog.

Together, the biological prior and the training data point in the same
direction. The focal cell type is a thalamic glutamatergic neuronal class from a
NeuN-positive sort, while KLRK1 needs an NK/T/macrophage receptor complex and
stress-ligand context that the assay essentially omitted. Because the available
lymphocyte receptors and innate immune receptors almost all produced exactly
zero FDR 0.05 genes in this same cell group, my point prediction for `Klrk1` is
`0`.

## Limits of the extrapolation

- The direct NKG2D adaptors `Hcst`/DAP10 and `Tyrobp`/DAP12, KLR-family
  paralogs, and Rae1/H60/Mult1 ligand genes were not in the focal training set,
  so the best comparisons are pathway and lineage proxies rather than
  same-complex perturbations.
- The supplied data do not include raw per-nucleus expression, gRNA indels,
  protein loss, receptor trafficking, phosphorylation, or NK/T-cell cytotoxic
  readouts. A protein or immune-cell assay would be the natural context for
  KLRK1; this is a juvenile postmitotic neuronal nuclear-RNA assay.
- The zero is a prediction for measured genes passing FDR 0.05 in recovered
  `151 TH Prkcd Grin2c Glut` nuclei. It should not be read as evidence that
  KLRK1 is biologically unimportant in NK cells, activated T cells, macrophages,
  tumors, viral infection, or autoimmune diabetes models.
- Sparse CRISPR editing could in principle produce rare or survival-selected
  states that are invisible to the Wilcoxon DEG count. The internal immune
  analogs make a broad focal-cell response unlikely, but they cannot exclude
  nontranscriptional or cell-nonautonomous consequences.
