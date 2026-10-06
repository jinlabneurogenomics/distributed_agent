# Task interpretation

The requested held-out target list contained one gene, `Drd3`. I treated the
requested value as the focal endpoint `n_degs`: the number of measured genes
with Scanpy/Wilcoxon Benjamini-Hochberg adjusted `pvals_adj < 0.05` in
`151 TH Prkcd Grin2c Glut` after a sparse postnatal CRISPR loss-of-function
perturbation.

`Drd3` was held out from both supplied files, so I did not try to read a `Drd3`
signature. The prediction is an extrapolation from observed focal-cell
perturbations of dopamine receptors and the Gi/o-cAMP pathway, plus outside
biology on D3 dopamine-receptor function. A prediction of `0` means I expect no
genes to pass this particular FDR threshold; it does not mean that D3R has no
electrophysiologic, cAMP, behavioral, or stimulus-evoked function.

# Sources

- Supplied training DEG counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Supplied all-cell differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested-target manifest:
  `[local file: 062_Drd3.csv]`
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`. `target_context(Drd3)` returned
  no direct Drd3 findings; I therefore used it only as a negative coverage
  check for the held-out gene and queried represented analogs such as `Drd2`,
  `Drd4`, `Adcy5`, and `Gnao1`.
- PubMed literature on D3 biology:
  Accili et al. 1996, DOI `10.1073/pnas.93.5.1945`, showed that germline
  disruption of the mouse D3 dopamine receptor produces increased locomotor and
  rearing behavior.
  Robinson and Caron 1997, DOI `10.1124/mol.52.3.508`, showed that D3R can
  inhibit type V adenylyl cyclase through a pertussis-toxin-sensitive Gi-family
  mechanism in a defined heterologous system.
  Ahlgren-Beckendorf and Levant 2004, DOI `10.1081/RRS-200029953`, reviewed
  D3R coupling to Gi/Go, adenylyl cyclase, ion channels, and MAPK while noting
  that signaling in brain remained less completely resolved.
  Demotes-Mainard et al. 1996, DOI `10.1016/0165-3806(96)00041-7`, mapped
  postnatal D3 receptor expression in mouse brain and found highest early
  expression in islands of Calleja/olfactory tubercle, with lower and regionally
  restricted expression including anterior thalamic complex.

# Focal-cell training-data checks

I first loaded the manifest and focal training counts. The manifest contained
only `Drd3`; the training endpoint contained 1,674 observed perturbations, of
which 1,205 had `n_degs = 0`. The median training count was 0, the 75th
percentile was 1, the 95th percentile was 18, and only the strongest few
essential nuclear/proteostasis perturbations had hundreds of DEGs.

For candidate analogs I filtered the parquet to:

```python
group_name == "151 TH Prkcd Grin2c Glut"
gene_target in candidate_genes
```

This pulled 17,259 measured-gene rows per candidate without loading the full
616 M-row parquet. I also computed a runtime profile comparison over the same
focal rows for 22 dopamine/cAMP/immediate-early candidates using
`logfoldchanges` as signed values and `pvals_adj < 0.05` as significance. The
comparison was used only to audit whether near-null candidates had hidden shared
FDR features; it did not select the final estimate automatically.

Key focal counts were:

| observed perturbation | focal `n_degs` | expression-pattern evidence in `151 TH Prkcd Grin2c Glut` |
| --- | ---: | --- |
| `Drd2` | 0 | D2-like receptor; no FDR hits. Its own row was `logFC=-0.458`, `p_adj=1`. |
| `Drd4` | 0 | D2-like receptor; no FDR hits. Its own row was not detectably depleted, `p_adj=1`. |
| `Drd5` | 0 | D1-like dopamine receptor counterexample; no FDR hits. |
| `Adcy5` | 0 | Type V adenylyl cyclase, a direct biochemical effector for D3 in heterologous systems; no FDR hits. |
| `Adcy1`, `Adcy3` | 0, 0 | Other represented membrane adenylyl cyclases; no FDR hits. `Adcy3` itself was nominally reduced but did not pass BH correction, `p_adj=0.112`. |
| `Gnao1` | 1 | Gi/o-family alpha subunit; the only hit in the focal cell group was its own transcript, `logFC=-0.591`, `p_adj=9.42e-7`, not a downstream activity module. |
| `Gnal`, `Gnas`, `Gnb5`, `Rgs6` | 0, 0, 0, 0 | Related heterotrimeric G-protein or regulator perturbations; no downstream focal DEGs. |
| `Pde10a`, `Pde1c`, `Pde4b`, `Pde4d` | 0, 0, 0, 0 | cAMP phosphodiesterase perturbations; all silent at FDR 0.05 in the focal group. |
| `Comt` | 1 | Dopamine catabolism; the only focal hit was strong depletion of `Comt` itself, `logFC=-0.806`, `p_adj=1.98e-14`. |
| `Creb1`, `Crebbp` | 10, 8 | Weak positives on the nuclear CREB arm. These are broader transcriptional regulators downstream of many pathways, not membrane dopamine-receptor phenocopies. |
| `Nr4a1`, `Nr4a3`, `Egr2`, `Fosl2` | 0, 0, 0, 0 | Activity/immediate-early transcription factors often downstream of cAMP or dopamine stimulation; no focal FDR hits. |

The profile audit agreed with the count table. Eighteen of the 22 candidates had
no significant focal features. The three observed dopamine receptors and
`Adcy5` had zero significant features, and the `Drd2` comparisons to `Drd4`,
`Drd5`, `Adcy5`, `Gnao1`, `Comt`, and `Creb1` had zero shared significant
features and no direction conflicts because the receptor side had no
significant genes. The top-200 signed-tail overlaps were small and came from
non-significant sparse rows, so I did not interpret them as a coherent
subthreshold module.

The Distributed Agents same-experiment corpus pointed in the same direction outside this
one focal group. `Drd4:F001` summarized a taxonomy-wide D4R null at FDR<0.10,
and `Drd4:F002` contrasted `Drd4` with `Drd2`, `Drd5`, `Gnao1`, `Gnal`,
`Gnas`, `Adcy1`, `Adcy3`, `Adcy5`, and cAMP phosphodiesterases, concluding that
represented dopamine receptors did not converge with represented cAMP
effectors. `Adcy5:F001/F003` reported that single loss of the represented
membrane adenylyl-cyclase paralogs was buffered across recovered neuronal
groups. `Gnao1:F002/F003` reported that most neuronal groups were buffered after
`Gnao1` and that obvious Gi/o and cAMP relatives did not phenocopy the narrow
`Gnao1` response.

# Target-specific reasoning

`Drd3` encodes the dopamine D3 receptor, a D2-family GPCR. Mechanistically the
nearest represented receptor analogs are `Drd2` and `Drd4`; both are D2-like
dopamine receptors expected to couple through Gi/o rather than Gs. They are much
better analogs than the D1-like `Drd5`, but all three observed dopamine
receptors produced `0` focal DEGs. That zero is not an isolated accident in the
focal count table: the Distributed Agents corpus found D4R loss to be FDR-clean across
the sampled neuronal taxonomy and found no dopamine-receptor/cAMP convergence
among represented receptor paralogs.

Downstream, D3R can inhibit ADCY5 in a Gi-sensitive manner. The represented
proximal effector `Adcy5` was exactly silent in the focal group, as were
`Adcy1`, `Adcy3`, `Pde10a`, `Pde1c`, `Pde4b`, `Pde4d`, `Gnal`, `Gnas`, `Gnb5`,
and `Rgs6`. `Gnao1` and `Comt` are the only one-DEG positives in this local
neighborhood, and in both cases the single significant row is the target mRNA
itself. That pattern argues against a durable receptor-to-CREB or
receptor-to-immediate-early transcriptional response in these thalamic
glutamatergic nuclei.

External biology prevents treating `Drd3` as an inert gene: D3R loss has mouse
behavioral consequences, and D3R can signal through Gi-family adenylyl-cyclase
control. The same biology also makes a large focal snRNA-seq response unlikely
here. D3R expression in mouse brain is limbic and relatively restricted, with
thalamic D3 receptor signal described only in selected nuclei during postnatal
development; the requested population is a `TH Prkcd Grin2c Glut` class, not a
ventral striatal or islands-of-Calleja D3R-enriched class. The assay measured a
basal nuclear-RNA endpoint three to four weeks after sparse P16 editing, without
dopamine stimulation or electrophysiology. The represented receptors and second
messenger genes show that this experiment often leaves acute neuromodulatory
GPCR pathways transcriptionally buffered.

I therefore predicted `Drd3` to behave like the local receptor/cAMP nulls,
rather than like the rare broad nuclear perturbations or the weak `Creb1` /
`Crebbp` positives:

| held-out target | primary analogs and counterexamples | zero/nonzero decision |
| --- | --- | --- |
| `Drd3` | `Drd2=0`, `Drd4=0`, `Drd5=0`, `Adcy5=0`, `Adcy1=0`, `Adcy3=0`, `Pde10a=0`, `Gnao1=1` self-only, `Comt=1` self-only, `Creb1=10` and `Crebbp=8` as broader downstream positives | `0`; same-family and proximal cAMP perturbations are silent in the focal group, and the few positives are either target-only or too nuclear/general to justify moving an unobserved D3 receptor above the FDR threshold. |

# Limits

The direct `Drd3` DE profile is completely absent by design, and the Distributed Agents
corpus has no internal Drd3 entry. The `Drd2` and `Drd4` rows are analogs, not
duplicates: D3R has distinct affinity, regional expression, and possible
heteromerization from D2R/D4R. Several desirable components were not represented
as focal training perturbations, including `Drd1`, the `Gnai` genes, arrestins,
and GRKs. The own-transcript depletion rows indicate that some receptor/cyclase
targets were not strongly detectable in this cell group, so part of the null
could be expression/power rather than pathway buffering. Finally, the endpoint
is a basal P37-P44 snRNA-seq FDR count; it will miss acute cAMP, phosphorylation,
ion-channel, synaptic, network, and behavior phenotypes that are well within D3R
biology.
