# Question and setup

I interpreted the task as a scalar prediction problem for the held-out target
`Notch3`: predict the number of genes in `151 TH Prkcd Grin2c Glut` cells whose
Wilcoxon Benjamini-Hochberg adjusted `pvals_adj` will be below 0.05 after
sparse AAV-CRISPR loss of `Notch3`. `Notch3` is absent from both the parquet of
per-gene differential-expression rows and the focal-cell DEG-count training CSV,
so I used the focal signatures and counts of related non-held-out perturbations,
plus prior Notch and NOTCH3 biology, to transfer a count.

The endpoint is an assay-specific RNA response breadth. I therefore treated
"0" as "no measured gene is expected to pass this screen's FDR 0.05 threshold",
not as proof that Notch3 is biologically irrelevant, unedited, or always
transcriptionally inert.

# Sources used

- Training DEG counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Training per-gene DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested-target manifest:
  `[local file: 155_Notch3.csv]`
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`, queried with `target_context`
  and reference-ledger lookups for Notch-pathway targets.
- Distributed Agents runtime `profile_neighbors`, run locally on the focal
  `151 TH Prkcd Grin2c Glut` rows to compare signed Wilcoxon-score profiles of
  Notch receptors and pathway comparators.
- Reactome, "Signaling by NOTCH1", `R-HSA-1980143`, for the canonical
  ligand/ADAM/gamma-secretase/NICD/RBPJ-MAML transcriptional scheme.
- Kopan and Ilagan 2009, Cell, PMID 19379690, doi:10.1016/j.cell.2009.03.045:
  canonical Notch activation by ligand-triggered proteolysis and nuclear
  NICD/RBPJ/MAML target-gene regulation.
- Joutel et al. 1996, Nature, PMID 8878478, doi:10.1038/383707a0: NOTCH3
  mutations as the cause of CADASIL.
- Domenga et al. 2004, Genes & Development, PMID 15545631,
  doi:10.1101/gad.308904: Notch3 is required cell-autonomously for arterial
  vascular smooth-muscle differentiation and maturation in mice.
- Chabriat et al. 2009, Lancet Neurology, PMID 19539236,
  doi:10.1016/S1474-4422(09)70127-9: CADASIL review describing NOTCH3 as
  primarily expressed in systemic arterial smooth-muscle cells and CADASIL as a
  small-vessel disorder with NOTCH3 extracellular-domain accumulation.
- Koo et al. 2005, Development, PMID 16000382: Mib1 is an E3 ligase required to
  generate active endocytosed Delta/Jagged Notch ligands.
- Zheng et al. 2012, Journal of Biological Chemistry, PMID 22505716: postnatal
  excitatory-neuron conditional Notch1/Notch2 deletion did not cause a broad
  neurodegenerative phenotype, a useful prior boundary for acute postmitotic
  neuronal Notch receptor loss.

# Computational checks

The focal-count training set had 1,674 non-held-out targets. It was very
zero-inflated: 1,205 targets had `n_degs = 0`, 363 had 1-9 DEGs, 63 had 10-99,
and 43 had at least 100.

I extracted the `151 TH Prkcd Grin2c Glut` parquet rows for the represented
Notch receptors and immediate pathway analogs, then counted
`pvals_adj < 0.05` per perturbation:

```python
analog = [
    "Notch1", "Notch2", "Notch4", "Dll1",
    "Adam10", "Psen1", "Mib1", "Fbxw7", "Tm2d1", "Ctnnb1",
]
focal = parquet[
    (parquet.group_name == "151 TH Prkcd Grin2c Glut")
    & parquet.gene_target.isin(analog)
]
n_sig = focal.groupby("gene_target").pvals_adj.apply(lambda x: (x < 0.05).sum())
```

Observed focal counts and the first matched perturbed/control-cell counts were:

| training perturbation | focal `n_degs` | matched perturbed cells | role for `Notch3` |
| --- | ---: | ---: | --- |
| `Notch1` | 0 | 143 | Notch receptor paralog; canonical receptor LoF analog |
| `Notch2` | 0 | 278 | Notch receptor paralog; canonical receptor LoF analog |
| `Notch4` | 0 | 324 | Notch receptor paralog; vascular-biased Notch receptor analog |
| `Dll1` | 0 | 250 | upstream Delta ligand; tests cell-autonomous ligand loss |
| `Adam10` | 0 | 69 | S2 protease required for canonical Notch cleavage |
| `Psen1` | 0 | 89 | gamma-secretase catalytic subunit downstream of ADAM cleavage |
| `Fbxw7` | 1 | 154 | NICD E3-ligase/substrate regulator; near-null counterexample |
| `Tm2d1` | 1 | 132 | Notch/gamma-secretase literature neighbor; weak singleton counterexample |
| `Mib1` | 27 | 148 | Notch-ligand E3 ligase but a sterol-module counterexample |
| `Ctnnb1` | 383 | 171 | unrelated Wnt effector showing this cell group can respond broadly |

All 10 rows above shared the same `n_ctrl_matched = 23679`. Thus the Notch
receptor zeros were not because the focal class was generally powerless:
`Ctnnb1` had a broad 383-gene Wnt/beta-catenin response at a similar perturbed
cell count, and `Mib1` had a 27-gene response with fewer cells than `Fbxw7` or
`Notch1`.

The canonical Notch readout genes I checked in the focal parquet were `Hes1`,
`Hes5`, `Hey1`, `Hey2`, `Heyl`, `Dtx1`, `Nrarp`, `Rbpj`, `Ascl1`, `Neurog2`,
`Neurod1`, and `Neurod2`. For `Notch1`, `Notch2`, `Notch4`, `Dll1`, `Adam10`,
`Psen1`, `Fbxw7`, `Tm2d1`, and `Mib1`, every one of these marker rows had
`pvals_adj = 1.0` in the focal cell type. That is a direct within-dataset check
that the represented Notch receptor/ligand/protease perturbations did not
engage a HES/HEY/RBPJ Notch-effector program in the held-out readout context.

I also compared the focal signed Wilcoxon-score vectors of the mechanistic
comparators with Distributed Agents `profile_neighbors`. All receptor/core-pathway
whole-profile Pearson correlations were near zero. For example, the top
Notch-receptor/canonical-neighbor Pearson similarities were only:

- `Notch1`: nearest among the tested set was `Tm2d1`, r = 0.0296; `Dll1`, r =
  0.0238; `Ctnnb1`, r = 0.0231.
- `Notch2`: `Ctnnb1`, r = 0.0382; `Psen1`, r = 0.0303; `Mib1`, r = 0.0244.
- `Notch4`: `Mib1`, r = 0.0156; `Adam10`, r = 0.0096; `Notch2`, r = 0.0024.
- `Adam10` and `Psen1`, which should sit immediately upstream of receptor NICD
  release, correlated only r = 0.0118 with each other.

These tiny dense-profile correlations match the direct FDR counts: in the focal
cell type the represented Notch core behaves as a null cloud rather than as a
subthreshold shared module.

# Same-experiment pathway evidence

The Distributed Agents corpus had no direct `Notch3` record because this target was
held out, but it did summarize the represented Notch neighborhood:

- `Notch2:F001` reported that `Notch2` produced a whole-surface neuronal null:
  every one of 23 recovered neuronal groups had zero downstream genes at the
  looser FDR 0.10 threshold.
- `Notch2:F002` and the shared claim over `Notch2`/`Notch4` reported that
  canonical HES/HEY, `Dtx1`, `Rbpj`, `Maml1`, `Ascl1`, `Neurog2`, `Neurod1`,
  and `Neurod2` outputs were not regulated by Notch receptors in assayed
  postnatal neurons.
- `Notch1:F003`, `Notch2:F004`, and `Notch4:F004` found that `Notch1`,
  `Notch2`, `Notch4`, `Dll1`, `Adam10`, `Psen1`, and `Fbxw7` were flat,
  singleton, or mutually nonconvergent rather than forming a receptor/ligand/
  cleavage transcriptional module.
- `Dll1:F001`/`F002` reported that acute `Dll1` LoF was transcriptionally silent
  across all 23 recovered juvenile-to-young-adult neuronal cell groups and did
  not move HES/HEY or proneural Notch markers.
- `Adam10:F001` reported no BH-supported downstream response in any of the nine
  neuronal groups in which `Adam10` was recovered, and `Adam10:F002` reported no
  convergent Adam10-like RNA module among Notch, APP, or synaptic-adhesion
  relatives.
- `Psen1:F001` reported zero downstream FDR-supported genes in every recovered
  neuronal group after acute `Psen1` perturbation.
- `Mib1:F001`/`F002` made `Mib1` an explicit counterexample: it is a Notch-ligand
  E3 ligase by prior biology, but in this screen its detectable response was
  recurrent SREBF2-like cholesterol-gene up-regulation and was uncoupled from
  `Dll1`, Notch receptors, `Adam10`, and `Psen1`.

# Target-specific reasoning for `Notch3`

`Notch3` encodes a Notch-family transmembrane receptor, so the best direct
training analogs are the represented Notch receptors rather than all genes with
Notch somewhere in their annotation. In the exact held-out cell group,
`Notch1`, `Notch2`, and `Notch4` each had `n_degs = 0`; the focal whole-profile
shape of `Notch1` was nearly uncorrelated even with `Notch2`; and none of the
receptors shifted canonical `Hes`/`Hey`/`Dtx1`/`Nrarp` targets. This strongly
argues that acute, sparse loss of a single Notch receptor is below the
transcriptional-response threshold in `151 TH Prkcd Grin2c Glut`.

The upstream and downstream processing analogs point the same way. `Dll1`,
`Adam10`, and `Psen1` each had `n_degs = 0` in the focal class, with all
canonical Notch-output marker adjusted p-values equal to 1.0. If these cells had
tonic, cell-autonomous Notch signaling at a level detectable by 3-4 week
snRNA-seq, perturbing a ligand, a receptor, the S2 protease, or presenilin would
be expected to show at least a small shared HES/HEY-class footprint. They did
not.

`Mib1` is the main positive Notch-adjacent perturbation in the focal cell type:
it yielded 27 DEGs. I did not transfer that count to `Notch3`, because the DEGs
were `Insig1`, `Dhcr24`, `Fdft1`, `Ldlr`, `Msmo1`, `Hmgcs1`, `Hmgcr`, `Cyp51`,
`Sqle`, `Srebf2`, and other sterol/cholesterol genes. The same-experiment
corpus specifically concluded that this Mib1 module is uncoupled from canonical
Dll1-Notch signaling. `Fbxw7`, an E3 ligase that regulates NICD and other
substrates, had a single focal hit, `Trp53inp2`; `Tm2d1` had a single focal hit,
`R3hdm2`. These singleton responses are more appropriate upper-bound
counterexamples than phenocopies.

External biology also favors the receptor-zero transfer. NOTCH3 is a CADASIL
gene and a vascular Notch receptor; Joutel et al. identified NOTCH3 mutations in
CADASIL, Chabriat et al. describe the disease as primarily affecting small
arterial smooth-muscle cells with NOTCH3 extracellular-domain accumulation, and
Domenga et al. showed in mice that Notch3 is required for arterial vascular
smooth-muscle maturation. The focal experiment sampled NeuN-enriched neuronal
nuclei from postnatal brain and largely excluded vascular smooth muscle,
pericytes, endothelium, astroglia, microglia, and neural progenitors. It also
used acute LoF, not CADASIL-like extracellular-domain missense accumulation.
Those differences make a large `Notch3`-driven RNA response in TH/Prkcd/Grin2c
glutamatergic neurons less likely than the vascular NOTCH3 literature would
suggest in its native cell types.

Given exact zeros for the three measured Notch receptors and for `Dll1`,
`Adam10`, and `Psen1` in the focal cell type, no canonical Notch-marker movement,
and only off-axis singleton or sterol counterexamples among Notch-adjacent
nodes, I predict that held-out `Notch3` will also have no measured genes passing
FDR 0.05 in `151 TH Prkcd Grin2c Glut`.

Prediction:

| target | predicted `n_degs` |
| --- | ---: |
| `Notch3` | 0 |

# Limits of the reasoning

This is still an extrapolation. `Notch3` itself was held out, `Rbpj`, `Maml1`,
`Psen2`, `Ncstn`, `Psenen`, `Jag1`, `Jag2`, `Dll3`, and `Dll4` were not focal
training perturbations, and receptor paralogs are imperfect substitutes because
Notch receptors differ in expression and ligand use. The screen measured
steady-state nuclear RNA in recovered NeuN-positive nuclei, not Notch3 protein,
NICD cleavage, vascular tone, CADASIL extracellular-domain aggregation, DNA
indels, or non-cell-autonomous signaling from edited neurons to neighboring
cells. A transient developmental, activity-evoked, vascular, glial, or protein-
level NOTCH3 effect could be invisible here. Within the requested focal RNA
endpoint, however, the mechanistically closest measured LoF perturbations are
flat enough that zero is the best point prediction.
