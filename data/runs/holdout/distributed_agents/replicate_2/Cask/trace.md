# Prediction trace

## Question and resolved ambiguities

The requested manifest contains one held-out perturbation, `Cask`. I interpreted the
endpoint as the exact training CSV endpoint: the number of measured genes, including
the perturbed target transcript if present in the DE table, with `pvals_adj < 0.05`
in `151 TH Prkcd Grin2c Glut`.

`Cask` was not present in the training count CSV, not present as a `gene_target` in
the supplied DE parquet, and had no same-experiment target context in the Distributed Agents
corpus for this run. The prediction is therefore an analog transfer from represented
perturbations.

## Sources

- Local endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Local DE table:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested-target manifest:
  `[local file: 030_Cask.csv]`
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`
- Distributed Agents runtime `profile_compare`/`profile_inspect` over the focal-cell DE rows
- NCBI PubMed for external CASK-complex literature

## Computation over the parquet and count table

The focal training distribution is very sparse: 1,205 of 1,674 non-held-out
targets have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 95th
percentile is 18, and the maximum is 2,677. A prediction of one DEG is therefore
a weak but detectable target-only class rather than a broad response.

I used Parquet row-group statistics to find the blocks spanning
`151 TH Prkcd Grin2c Glut` and read only row groups 546-580, retaining these
columns:

```python
["names", "gene_target", "logfoldchanges", "pvals_adj", "scores", "group_name"]
```

Within the focal group I then filtered to CASK-neighborhood candidates and counted
`pvals_adj < 0.05` for each training perturbation. For the most relevant genes:

| training target | focal `n_degs` | focal FDR<0.05 genes | interpretation for `Cask` |
| --- | ---: | --- | --- |
| `Caskin1` | 1 | `Caskin1`, logFC -0.564, q=0.00076 | Direct CASK-binding active-zone scaffold; the only focal hit was target RNA. |
| `Nrxn1` | 1 | `Nrxn1`, logFC -0.518, q=2.7e-23 | Neurexin is a direct CASK ligand; only target RNA passed. |
| `Nrxn2` | 0 | none; best q=0.17 | Neurexin paralog counterexample. |
| `Nrxn3` | 0 | none; best q=0.091 | Neurexin paralog counterexample. |
| `Nlgn3` | 1 | `Nlgn3`, logFC -0.896, q=4.8e-11 | Neurexin-ligand adhesion comparator; target-only. |
| `Dlg4` | 1 | `Dlg4`, logFC -0.444, q=1.1e-08 | Core postsynaptic MAGUK scaffold; target-only. |
| `Dlgap4` | 2 | `Dlgap4`; `Vgf`, logFC -0.409, q=0.029 | PSD scaffold with one extra isolated neuropeptide hit. |
| `Shank2` | 0 | none | PSD scaffold counterexample. |
| `Shank3` | 2 | `Shank3`; `Uba5`, logFC +0.419, q=0.029 | Mostly target depletion plus one non-synaptic singleton. |
| `Syngap1` | 0 | none; own transcript q=0.12 | PSD/Ras-GAP counterexample. |
| `Magi2` | 0 | none | Synaptic MAGUK/PDZ scaffold counterexample. |
| `Grin1` | 89 | 49 down, 40 up | Strong counterexample showing this cell group can mount an NMDA-loss RNA response. |
| `Grin2a` | 1 | `Grin2a`, logFC -0.492, q=0.002 | NMDAR subunit mostly target-only in this group. |
| `Grin2b` | 2 | `Grin2b`; `Pianp`, logFC -0.334, q=0.017 | CASK/Tbr1-linked subunit, but still tiny in this group. |
| `Grin2d`, `Grin3a` | 0, 0 | none | NMDAR subunit counterexamples. |
| `Tbr1` | 0 | none | CASK nuclear partner, flat in the focal thalamic group. |
| `Camk2a`, `Camk2b`, `Camk2g` | 0, 1, 0 | only `Camk2b` self | CASK has a CaMK-like domain, but represented CaMKII genes did not induce a module. |
| `Calm1`, `Calm2`, `Calm3` | 14, 0, 1 | `Calm1` gave a modest broader state | Calmodulin biology is not enough to make CASK look like `Calm1`. |

I also compared 23 CASK-adjacent observed signatures in the Distributed Agents runtime using
`logfoldchanges` over the focal group, with `pvals_adj` at 0.05 to mark significant
features. In the `Caskin1`, `Nrxn1`, `Nlgn3`, `Dlg4`, and `Grin1` inspection against
ten scaffold/receptor peers, there were no same-direction significant intersections:
the target-only genes did not form a recurrent FDR-level CASK/neurexin/MAGUK module,
and the large `Grin1` focal signature did not overlap these scaffold calls. The
whole-vector nearest-neighbor scores were treated only as a check for hidden structure,
because the top nominal features of target-only perturbations generally had
`pvals_adj = 1`.

## Same-experiment corpus evidence

`Cask` itself was absent from the Distributed Agents corpus release, as expected for the
held-out target. The represented CASK-adjacent cohort was well connected in the
corpus graph: `Caskin1`, neurexins, `Dlg4`/`Dlgap4`, `Shank2`/`Shank3`, `Syngap1`,
`Magi2`, `Grin1`/`Grin2a`/`Grin2b`, `Nlgn3`, and `Tbr1` all appeared in one induced
component. I kept the semantic direction of those edges:

- `Caskin1:F002` reported that thalamic and midbrain glutamatergic groups, including
  `151 TH Prkcd Grin2c Glut`, buffered `Caskin1` RNA depletion with no broad
  downstream transcriptome.
- `Caskin1:F003` explicitly tested available biochemical/receptor/scaffold proxies
  for CASKIN1 biology, including `Nrxn1`, `Nrxn2`, `Nrxn3`, `Dlg4`, `Shank2`,
  `Shank3`, `Camk2a`, `Camk2b`, and `Gria1-3`, and found them nonconvergent.
- `Nrxn1:F002` and `Nrxn1:F003` described `Nrxn1` as transcriptomically sparse and
  lacking a robust neurexin-family or adhesion-neighborhood phenocopy.
- `Dlg4:F001`, `Dlg4:F002`, and `Dlg4:F004` found acute `Dlg4` loss to be globally
  downstream-flat and grouped `Syngap1`, `Shank2`, `Magi2`, `Nlgn3`, and `Nrxn2` by
  shared near-zero RNA surfaces, not by a shared signed DEG program.
- `Nlgn3:F001` and `Nlgn3:F002` reported a pan-surface `Nlgn3` downstream null and
  flat or sparse behavior among expected neurexin/neuroligin/scaffold relatives.
- `Grin1:F001` through `Grin1:F008` were used as the strongest boundary: the screen
  can detect a true 151-dominated NMDAR response, but `Grin1:F007` showed that even
  NMDA receptor subunits are subunit- and cell-context-specific rather than
  interchangeable signatures.
- `Tbr1:F001`, `Tbr1:F006`, and `Tbr1:F007` showed that postnatal `Tbr1` has a
  small cortical signature but not a focal thalamic one, and that it did not recover
  a canonical embryonic `Auts2`/`Grin2b`/`Reln` fate program.

These same-experiment findings argue that CASK's location in synaptic adhesion and
PSD biology predicts a target-only or null snRNA-seq outcome unless CASK engages the
Grin1-like thalamic stress/plasticity branch. The represented direct interactors do
not support that broader branch.

## External biological rationale

CASK is a membrane-associated guanylate kinase scaffold with a CaMK-like N-terminus
and PDZ/SH3/GK domains. Hata, Butz, and Sudhof identified it as a binding partner of
the intracellular tails of neurexins (1996; DOI 10.1523/JNEUROSCI.16-08-02488.1996;
PMID 8786425). CASK also forms LIN-2/LIN-7/LIN-10-like complexes with Mint/X11 and
mLin-7/Veli proteins in mammalian brain (Borg et al., 1998; DOI
10.1074/jbc.273.48.31633; PMID 9822620), and the KIF17/Mint complex links this
scaffold neighborhood to NR2B-containing NMDA-receptor vesicle transport (Setou et
al., 2000; DOI 10.1126/science.288.5472.1796; PMID 10846156).

The represented training gene `Caskin1` is the closest assayed proxy. Tabuchi,
Biederer, Butz, and Sudhof showed that Caskin1 is a brain CASK-binding adaptor that
coassembles with CASK on the neurexin-1 cytoplasmic tail and competes with Mint1 for
the CASK CaMK-domain binding site (2002; DOI
10.1523/JNEUROSCI.22-11-04264.2002; PMID 12040031). Stafford, Ear, Knight, and
Bowie mapped a short Caskin1 peptide sufficient for CASK binding, reinforcing that
this is a direct biochemical analog rather than only a family label (2011; DOI
10.1016/j.jmb.2011.07.005; PMID 21763699).

CASK can also translocate to the nucleus and cooperate with TBR1/CINAP to regulate
genes such as `Grin2b`/NR2B and `Reln` in cultured hippocampal or cortical neurons
(Wang GS et al., 2004; DOI 10.1016/S0896-6273(04)00139-4; PMID 15066269; Wang TF et
al., 2004; DOI 10.1111/j.1471-4159.2004.02845.x; PMID 15584924). I treated this as
a reason not to force an absolute zero, but the matched perturbations `Tbr1`,
`Grin2b`, and the CaMK/CaM genes did not show a CASK-like broad program in the
focal cell group.

## Target-specific decision

For `Cask`, the strongest within-dataset analog was `Caskin1`, whose perturbation
produced exactly one focal DEG: its own transcript. The presynaptic ligand side
(`Nrxn1/2/3`) and neurexin-ligand side (`Nlgn3`, `Lrrtm1/3/4`, `Cadm2`,
`Cntnap1/2`) were all zero- or one-gene surfaces in this cell group, and the PSD
scaffold comparators around NMDARs (`Dlg4`, `Dlgap4`, `Shank2`, `Shank3`,
`Syngap1`, `Magi2`, `Homer2`, `Lrrc7`, `Cacng2`) were also 0-2 DEG perturbations.
Their significant genes were nearly always self-RNA loss, not recurrent downstream
state genes.

The main reason to predict a nonzero rather than a strict zero is that a direct CASK
perturbation could deplete `Cask` mRNA in the nucleus just as `Caskin1`, `Nrxn1`,
`Nlgn3`, `Dlg4`, `Grin2a`, `Grin2b`, `Camk2b`, and several adhesion genes depleted
their own transcripts. The main reason to keep the value at one is that the external
developmental/synaptic importance of CASK is carried largely by protein localization,
synapse structure, receptor trafficking, and early developmental phenotypes. Those
mechanisms are not well captured by an acute, sparse, P16 loss-of-function,
NeuN-enriched single-nucleus RNA endpoint, and the direct same-experiment synaptic
neighbors were transcriptomically buffered.

Predicted `n_degs` for `Cask`: **1**.

## Limits

- `Cask` was held out, and the Distributed Agents corpus had no direct same-experiment
  `Cask` finding. The prediction extrapolates from `Caskin1`, neurexins, and PSD
  scaffolds rather than from a measured CASK signature.
- Several very close complex members were unavailable as perturbations in the
  training count table, including `Caskin2`, `Apba1`/Mint1, and `Lin7` family
  members.
- The `Caskin1` and neurexin comparators are biochemical neighbors, not paralogs of
  `Cask`; CASK's nuclear TBR1/CINAP role could have consequences not reproduced by
  CASKIN1 or neurexin loss.
- `151 TH Prkcd Grin2c Glut` is not cortex or hippocampus, where much of the
  TBR1-CASK-GRIN2B literature was developed.
- The endpoint counts single-gene target depletion events. A prediction of 1 should
  be read as "probably target-only or one isolated transcript", not as evidence for
  a robust CASK downstream module.
