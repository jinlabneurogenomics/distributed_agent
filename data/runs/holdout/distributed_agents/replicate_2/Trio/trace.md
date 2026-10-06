## Question and interpretation

The held-out target list for this run contains one perturbation, `Trio`. I
interpreted the task as predicting the integer number of genes with
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in
`151 TH Prkcd Grin2c Glut` after acute AAV-CRISPR loss of `Trio`.

I treated `n_degs` exactly as the supplied endpoint defines it: all measured
genes passing FDR 0.05 in this focal cell group, including the target transcript
itself when the self row passes. I did not use measured target-RNA loss as an
editing-efficiency estimate, because the experiment reports only modest and
variable mRNA knockdown after indel editing.

## Sources used

- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Focal-cell training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Requested target manifest:
  `[local file: 246_Trio.csv]`
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, especially the `Kalrn`, `Rac1`,
  `Cdc42`, and `Pak1` Finding summaries.
- NCBI PubMed literature for Trio/Kalrn/Rho-family biology.

## Computational checks

The manifest contained exactly:

```tsv
target_name
Trio
```

The focal count training table contained 1,674 non-held-out perturbations. Its
endpoint was highly zero-inflated: 1,205/1,674 were 0, 363 were 1-9, 63 were
10-99, and 43 were at least 100 DEGs. The median was 0 and the maximum was
2,677, so the decisive question for `Trio` was the zero/nonzero call.

I filtered the training counts for biologically selected comparators and then
queried the focal rows of the parquet for exact FDR-significant genes among
that comparator set:

```python
import pyarrow.dataset as ds

dset = ds.dataset(
    "[local file: holdout_task]"
    "Inputs/training_de_all_cell_groups.parquet",
    format="parquet",
)

targets = [
    "Kalrn", "Rac1", "Cdc42", "Pak1", "Pak2", "Pak3", "Dock3",
    "Arhgap18", "Arhgap32", "Arhgef9", "Dcc", "Ncam1",
    "Mapk1", "Mapk9", "Grin1", "Ctnnb1",
]

tbl = dset.to_table(
    columns=["gene_target", "names", "logfoldchanges", "pvals_adj", "scores"],
    filter=(
        (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
        & ds.field("gene_target").isin(targets)
        & (ds.field("pvals_adj") < 0.05)
    ),
)
```

I also ran the Distributed Agents runtime `profile_compare`/`profile_inspect` workflow on
the same focal-cell log-fold-change vectors for these targets. That comparison
confirmed that the Kalrn/Rac1/Cdc42/PAK/Dock/DCC/NCAM1 group had no shared
FDR-significant downstream feature in the focal group; the 1-DEG calls were
self-transcript hits rather than convergent response modules.

## Target-specific reasoning

### Trio

`Trio` itself was absent from the training counts and absent from the DE parquet
as expected for a held-out target. The same-experiment corpus also returned no
`Trio` target record in this filtered run.

Biological priors:

- TRIO is a large Dbl-family Rho guanine nucleotide exchange factor with two
  exchange domains; the N-terminal GEF1 activates Rac1/RhoG and the C-terminal
  GEF2 activates RhoA. That places it upstream of actin-remodeling and
  morphogenesis rather than directly in a nuclear transcription-factor module
  (van Rijssel and van Buul 2012, DOI `10.4161/cam.21418`; Katrancha et al.
  2017, DOI `10.1093/hmg/ddx355`).
- `Kalrn` is the closest measured paralog with the same overall
  multi-domain Trio/Kalirin GEF architecture. Trio and Kalirin duplicated from a
  common metazoan ancestor and retained related Rac/Rho GTPase biology
  (Kratzer et al. 2019, DOI `10.1016/j.gep.2019.02.004`).
- Trio couples DCC/netrin signaling to Rac1 activation and embryonic axon
  outgrowth/guidance; Fyn phosphorylation and Hsc70 regulate the same
  DCC-Trio-Rac branch (Briancon-Marjollet et al. 2008, DOI
  `10.1128/MCB.00998-07`; DeGeer et al. 2012, DOI
  `10.1128/MCB.01264-12`; DeGeer et al. 2015, DOI `10.1083/jcb.201505084`).
- Trio can also signal to RhoA downstream of Slit2 during embryonic
  telencephalic wiring, including thalamocortical axon pathfinding (Backer et
  al. 2018, DOI `10.1242/dev.153692`).

Training perturbations used as analogs or counterexamples in
`151 TH Prkcd Grin2c Glut`:

| Training target | Observed focal `n_degs` | Expression evidence and role in the comparison |
| --- | ---: | --- |
| `Kalrn` | 0 | Closest represented paralog and the best same-family comparator. It had no FDR 0.05 focal response. The Distributed Agents corpus also reports that acute P16 `Kalrn` loss was FDR-flat across neuronal groups and did not induce the Rac1/PAK/LIMK or PSD/NMDAR mRNA feedback that would have supported a shared Trio/Kalirin nuclear module. |
| `Rac1` | 0 | Direct downstream GTPase for Trio GEF1. It was focal-cell null. Corpus findings describe `Rac1` as buffered in postnatal neuronal snRNA-seq: its sparse event in another cell type did not generalize to represented Cdc42/PAK/WAVE/GEF/GAP relatives. |
| `Cdc42` | 1 | Adjacent Rho-family GTPase. The only focal significant row was `Cdc42` itself, logFC -0.593, adjusted P `8.62e-05`; there was no downstream focal program. |
| `Pak1` | 1 | Rac/Cdc42 effector kinase. The only focal significant row was `Pak1` itself, logFC -0.599, adjusted P `5.02e-08`. |
| `Pak2` | 0 | Group-I PAK effector; focal-cell null. |
| `Pak3` | 0 | Neuronal group-I PAK effector; focal-cell null. |
| `Dock3` | 0 | Neuronal Rac GEF adjacent to the Trio/Rac branch; focal-cell null. |
| `Arhgef9` | 1 | RhoGEF/scaffold at inhibitory postsynapses, used as a less direct GEF counterexample. Its lone focal hit was `Arhgef9` itself, logFC -0.571, adjusted P `3.70e-08`. |
| `Arhgap18`, `Arhgap32` | 0, 0 | Rho-family GAP comparators. Both were focal-cell null. |
| `Dcc` | 0 | Upstream netrin receptor for the embryonic DCC-Trio-Rac1 branch. Direct `Dcc` perturbation was focal-cell null, arguing that this guidance branch does not act as a basal transcriptomic driver in the P16-P37/P44 thalamic glutamate readout. |
| `Ncam1` | 1 | Axon/synapse adhesion comparator. Its only focal hit was `Ncam1` itself, not a secondary program. |
| `Mapk1`, `Mapk9` | 0, 0 | Signaling counterexamples downstream of many synaptic cues; both were focal-cell null and therefore did not argue for a broad kinase-driven analog to `Trio`. |
| `Grin1` | 89 | Counterexample showing this focal cell group can mount a medium response to direct perturbation of the NMDA receptor channel. It is not a close `Trio` analog: NMDAR subunit loss directly changes glutamatergic receptor function, whereas Trio is a local cytoskeletal GEF. |
| `Ctnnb1` | 383 | Counterexample showing that cell-adhesion/cytoskeletal proteins with direct Wnt transcriptional connections can have a large focal signature. This is a poor quantitative analog for Trio because beta-catenin is a transcriptional effector as well as an adhesion protein; Ctnnb1 loss down-regulated many Wnt/synaptic genes in the focal group, unlike the flat GEF/GTPase/PAK nodes. |

The most informative part of the same-experiment evidence is the silence of the
immediate biochemical neighborhood. `Trio` is expected to change GTP loading,
protein localization, actin assembly, growth-cone or spine structure, and
synaptic function. Those are precisely the phenotypes that the snRNA-seq
readout misses unless they are converted into a stable nuclear RNA state. In
the focal cell group, the direct paralog `Kalrn`, the GEF1 effector `Rac1`,
nearby small GTPase `Cdc42`, PAK effectors, `Dock3`, RhoGAP comparators, and
the upstream receptor `Dcc` all failed to produce a secondary FDR 0.05
transcriptional footprint. The Distributed Agents Kalrn/Rac1/Cdc42 findings reinforce
that this was not a peculiarity of one chosen target: represented
Rac/Cdc42-linked actin-cytoskeletal perturbations were generally buffered in
juvenile neuronal nuclear RNA rather than forming a recurrent pathway module.

The developmental literature does keep `Trio` from being a generic no-function
gene. Germline or embryonic Trio disruption affects axon guidance, commissural
tracts, thalamocortical wiring, and neurodevelopmental-disorder variant biology.
However, those phenotypes mostly occur earlier than the P16 AAV perturbation or
at a protein-signaling/morphology level. The closest assayed P16 single-gene
analogs therefore point to no measurable focal DEG rather than to the strong
Grin1/Ctnnb1 class.

## Prediction and limits

I predict `Trio` will have 0 DEGs in `151 TH Prkcd Grin2c Glut`.

The call is driven primarily by within-dataset evidence from `Kalrn`, `Rac1`,
`Cdc42`, `Pak1`/`Pak2`/`Pak3`, `Dock3`, RhoGAP/RhoGEF neighbors, and `Dcc`.
External biology supplies the mapping from `Trio` to that comparator set and
explains why a morphogenetic Rac/Rho GEF can be biologically important but
transcriptionally quiet in a sparse postnatal snRNA-seq loss-of-function assay.

The main uncertainty is that the exact direct GTPases `Rhoa` and `Rhog` and the
held-out `Trio` signature were not available in the training endpoint. A
significant self-transcript call for `Trio` alone could make the true value 1
even if there is no downstream response. Conversely, embryonic thalamocortical
or netrin/DCC phenotypes are imperfect analogs for juvenile recovered thalamic
neuronal nuclei, so this is an extrapolation from adjacent pathway perturbations
rather than a measured Trio profile.
