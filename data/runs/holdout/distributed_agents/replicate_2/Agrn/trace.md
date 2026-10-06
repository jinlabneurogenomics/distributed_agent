# DEG-count prediction for held-out Agrn

## Question and endpoint

The requested held-out perturbation was `Agrn`. I interpreted the endpoint as the
literal focal-cell-group DEG burden used in the training CSV:

- cell group: `151 TH Prkcd Grin2c Glut`
- perturbation modality: acute mosaic AAV CRISPR loss of function in postnatal
  mouse neurons
- point to predict: the number of measured genes with
  `pvals_adj < 0.05` in the Wilcoxon differential-expression table
- count convention: include any measured gene that passes the threshold,
  including the target transcript itself if it happens to pass

`Agrn` was present in the requested-target manifest and absent from the
training-count table, so no direct `Agrn` DEG count or `Agrn` expression
signature was used. I treated null signatures in the training data as
assay-conditioned observations, not as proof that the edited protein had no
local synaptic or extracellular effect.

## Sources used

- `training_de_all_cell_groups.parquet`: authoritative per-gene DE statistics.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: endpoint counts for the
  1,674 non-held-out training perturbations in the focal cell group.
- `006_Agrn.csv`: requested held-out targets; one row, `Agrn`.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`: packaged semantic reports and
  claims over the same Perturb-seq experiment. This supplied the prior
  comparisons involving `Lrp4`, `Musk`, `Dag1`, DGC/matriglycan genes, and NMJ
  AChR genes.
- Distributed Agents runtime `profile_neighbors`: a run-local observed-profile
  comparison over Wilcoxon score vectors in `151 TH Prkcd Grin2c Glut`.
- PubMed/NCBI literature for external biology of agrin, LRP4, and MuSK:
  - Zong and Jin 2012, DOI `10.1007/s00018-012-1209-9`: structural review of
    the agrin-LRP4-MuSK pathway for NMJ postsynaptic differentiation.
  - Li, Xiong, and Mei 2017, DOI `10.1146/annurev-physiol-022516-034255`:
    NMJ formation, maintenance, and disease biology.
  - Ohno, Ohkawara, and Ito 2017, DOI `10.1080/14728222.2017.1369960`:
    agrin-LRP4-MuSK signaling as an NMJ therapeutic target.
  - Neumann et al. 2001, DOI `10.1006/mcne.2000.0932`: the CNS-enriched
    transmembrane agrin isoform.
  - Daniels 2012, DOI `10.1016/j.neuint.2012.02.028`: review of agrin in CNS
    synaptic development, plasticity, and signaling.
  - Karakatsani et al. 2017, DOI `10.1242/dev.150110`, and Handara et al. 2018,
    DOI `10.1016/j.ydbio.2018.10.017`: LRP4/agrin/MuSK roles in embryonic
    cortical and hippocampal neurite and synapse assays.

## Computation over the supplied data

I first loaded the focal training-count CSV to calibrate the scale of the
endpoint. The 1,674 training perturbations were highly sparse: median `n_degs`
was 0, the 75th percentile was 1, 469 perturbations had any FDR 0.05 gene, and
the distribution had a long upper tail led by essential RNA/proteostasis or
regulatory targets such as `Uba5`, `Tpr`, and `Sin3a`.

I then sliced the parquet to the focal cell group for a hand-curated set of
`Agrn` analogs and counterexamples: receptor-side NMJ genes, muscle AChR
subunits, dystroglycan/matriglycan genes, laminin/integrin neighbors, Wnt
counterexamples, neurexin/neuroligin adhesion genes, and perturbations whose
same-experiment reports explicitly mentioned an `Agrn` axis. The parquet is
row-grouped by cell type, so the scan touched the `151 TH Prkcd Grin2c Glut`
row groups rather than loading the whole 616 million row atlas.

```python
dset = ds.dataset(training_parquet, format="parquet")
flt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(candidate_targets)
)
focal = dset.to_table(
    columns=[
        "names", "gene_target", "scores", "logfoldchanges", "pvals_adj",
        "n_pert_matched", "n_ctrl_matched",
    ],
    filter=flt,
).to_pandas()
summary = focal.groupby("gene_target").agg(
    n_degs=("pvals_adj", lambda q: int((q < 0.05).sum())),
    min_fdr=("pvals_adj", "min"),
    n_pert=("n_pert_matched", "max"),
)
```

For the selected 32 analog or counterexample targets, this yielded 17,259
measured rows per target in the focal group, matching the endpoint counts in
the training CSV. I also ran `profile_neighbors` over the same focal context
using the Wilcoxon `scores` vector and `pvals_adj < 0.05` as the significance
column, with `Lrp4`, `Musk`, and `Dag1` as anchors. This was used only as a
bounded profile check among biologically nominated candidates; it was not used
to create an aggregate model.

## Target-specific reasoning

### Agrn

**External biological prior.** `Agrn` encodes agrin, a heparan-sulfate
proteoglycan. Its best-established signaling role is extracellular and
synaptic: motor-neuron agrin binds muscle `Lrp4`, activates `Musk` with Dok7,
and clusters acetylcholine receptors at the neuromuscular junction
(Zong and Jin 2012; Li et al. 2017; Ohno et al. 2017). Agrin is also expressed
in brain, including a transmembrane isoform enriched in embryonic neurons
(Neumann et al. 2001), and CNS agrin/LRP4/MuSK biology has been reported in
embryonic cortical and hippocampal neurite/synapse assays (Karakatsani et al.
2017; Handara et al. 2018). Those roles are mostly developmental,
extracellular, morphological, or electrophysiological; they do not by
themselves imply a large steady-state nuclear RNA response three to four weeks
after sparse P16 editing in recovered thalamic glutamatergic neurons.

**Direct receptor-side comparators in the training set.** `Lrp4` and `Musk`
are the closest represented members of the canonical agrin pathway. Both were
measured in `151 TH Prkcd Grin2c Glut` and both had zero focal DEGs at the
task threshold:

| training perturbation | focal `n_degs` | focal profile evidence |
| --- | ---: | --- |
| `Lrp4` | 0 | 199 perturbed nuclei vs 23,679 controls; all 17,259 focal adjusted p-values were 1.0. |
| `Musk` | 0 | 204 perturbed nuclei vs 23,679 controls; all 17,259 focal adjusted p-values were 1.0. |

The same-experiment Distributed Agents corpus made the same receptor-side comparison
over the whole measured surface: `Lrp4` produced only a single FDR 0.10 event
anywhere, `Musk` produced only a single weak `Vps4a` event in `027
NP-CT-L6b-OB Glut`, and `Musk` did not phenocopy `Lrp4` or the represented
muscle AChR/NMJ genes. The corpus claim
`claim:9aea411fa0e464068554` summarizes this as a high-confidence internal
observation that single perturbations of represented muscle AChR/NMJ pathway
genes do not recover a shared muscle-channel or NMJ transcriptional module in
postnatal brain neurons. In the focal profile-neighbor run, `Lrp4` and `Musk`
were also nearly orthogonal to each other: their focal Wilcoxon-score Pearson
correlation was only 0.0468, with 1 of the top 100 positive features and none
of the top 100 negative features shared. This is strong within-dataset evidence
against assigning `Agrn` a broad focal count by transferring the muscle NMJ
pathway.

**Postsynaptic AChR and cholinergic/NMJ boundaries.** The represented muscle
acetylcholine receptor genes were also quiet in this exact cell group:
`Chrna1`, `Chrnb1`, `Chrnd`, `Chrne`, and `Chrng` each had `n_degs = 0`;
`Ache` had only one focal FDR 0.05 gene. The same corpus explicitly used
`Chrnb1`, `Chrnd`, `Chrne`, and `Chrng` reports as additional support that the
screen does not reconstruct a muscle endplate transcriptional program in
NeuN-positive brain nuclei. `Agrn` itself, `Rapsn`, `Dok7`, and `Colq` were not
available as training perturbations, which is an important gap, but the
measured receptor and AChR-side nodes point to zero or singleton behavior, not
to a multi-gene NMJ-like focal signature.

**Extracellular matrix and dystroglycan counterfactuals.** Agrin is an
extracellular heparan-sulfate proteoglycan and is also adjacent to
dystroglycan/matriglycan biology, so I checked the represented DGC and
alpha-dystroglycan glycosylation targets rather than relying only on `Lrp4`
and `Musk`.

| training perturbation | focal `n_degs` | relevance to `Agrn` |
| --- | ---: | --- |
| `Dag1` | 0 | major dystroglycan/ECM receptor; all focal adjusted p-values were 1.0. |
| `Dmd` | 0 | dystrophin-glycoprotein complex scaffold; fully null in the focal count despite a lower 64-cell perturbed recovery. |
| `Snta1` | 0 | DAPC member; no focal FDR 0.05 genes. |
| `Sgce` | 0 | brain sarcoglycan-family DGC member; no focal FDR 0.05 genes. |
| `Sgcd` | 0 | closest weak positive in this set, but only subthreshold `Sik2` and `Porcn` at FDR 0.0536 and 0.0752. |
| `Crppa`, `Fktn`, `Rxylt1` | 0 | matriglycan/glycosylation nodes; no focal FDR 0.05 genes. |
| `Large1` | 1 | the lone FDR 0.05 row was `Large1` itself, not a downstream ECM module. |
| `Itgb1`, `Itga6` | 0 | laminin/integrin-side comparators; no focal FDR 0.05 genes. |

The Distributed Agents corpus claims `claim:229054e11de208051691` and
`claim:621f38c75b4df7d88e36` summarize this broader result: represented
dystrophin-glycoprotein-complex and alpha-dystroglycan glycosylation
perturbations were flat, near-flat, or non-overlapping in the postnatal
neuronal snRNA-seq assay rather than a coherent shared module. Because `Dag1`
is an extracellular-matrix receptor for synaptic ligands and was fully flat,
and because its pathway comparators either were flat or produced isolated
non-shared hits, the DGC/matrix branch does not justify a nonzero `Agrn`
count in the focal group.

**Synaptic-adhesion counterexamples.** I also checked neurexin/neuroligin
neighbors because agrin is a synaptic extracellular organizer rather than only
an NMJ ligand. `Nrxn1`, `Nrxn2`, `Nrxn3`, and `Nlgn3` had focal counts of 1, 0,
0, and 1, respectively. Same-experiment reports for `Nrxn1`, `Nrxn3`, and
`Nlgn3` found that represented neurexin-family, neuroligin, and `Dag1`
neighbors were sparse and nonconvergent. That does not make them exact agrin
analogs, but it shows that extracellular synapse-organizing proteins in this
screen usually produced local/protein-level phenotypes, if any, without a
shared broad nuclear RNA state.

**Positive thalamic controls that I did not transfer.** `Lrp6`, `Ctnnb1`, and
`Tcf7l2` were included as counterexamples because they show that this focal
cell group can report Wnt/beta-catenin transcription when a core effector is
hit: focal counts were 4 for `Lrp6`, 383 for `Ctnnb1`, and 106 for `Tcf7l2`.
The corpus high-confidence claim `claim:3899d7f888c17c10585f`, however, notes
that the thalamic `Axin2`-containing Wnt/beta-catenin response is engaged by
`Lrp6` and `Ctnnb1` but not by `Lrp4`. Since canonical agrin signaling is
closest to `Lrp4`/`Musk`, not to `Lrp6`/`Ctnnb1`, the Wnt-positive nodes are
evidence that the assay can see thalamic signaling but are a boundary against
assuming that every LDL-receptor-family or MuSK-adjacent perturbation will be
nonzero.

**Agrn-as-marker reports.** Two same-experiment reports mentioned `Agrn` in
other perturbation contexts. `Myo9a` reports treated the MYO9A-Agrin/NMJ axis
as absent from sampled central neurons; `Myo9a` had `n_degs = 0` in the focal
group. A `Zc3h14` report found `Agrn` down in midbrain glutamatergic neurons,
while the focal `Zc3h14` response contained six RNA-processing-associated genes
and no direct agrin-receptor signature. These observations make `Agrn` a
possible downstream marker in a broad RNA-binding-protein perturbation, not a
reason to expect loss of agrin itself to drive the same focal state.

## Prediction

I predict `Agrn` will have **0** DEGs in `151 TH Prkcd Grin2c Glut` at
FDR 0.05.

The zero/nonzero decision is driven primarily by within-dataset evidence:
`Lrp4`, `Musk`, `Dag1`, the represented AChR/NMJ nodes, and the represented
DGC/matriglycan nodes were all zero or singleton perturbations in the focal
cell group and failed to form a shared expression-pattern module in the
same-experiment corpus. External agrin literature supports why those were the
right analogs, but it also cautions that agrin's best-established phenotypes
are extracellular synapse-organization, NMJ, developmental morphology, and
electrophysiology phenotypes rather than a direct postnatal thalamic nuclear
mRNA program.

## Limits of the reasoning

- `Agrn` was held out, so there is no direct `Agrn` signature to correlate
  with training perturbations.
- The closest unavailable perturbations were `Rapsn`, `Dok7`, and `Colq`; the
  inference uses the represented receptor-side nodes `Lrp4` and `Musk` plus
  AChR subunits as an incomplete NMJ pathway panel.
- The screen did not measure Agrin protein, heparan-sulfate chains,
  extracellular matrix deposition, acetylcholine receptor clusters, dendritic
  spines, miniature synaptic currents, or neuromuscular junctions. A zero DEG
  prediction is therefore a prediction about the snRNA-seq endpoint only.
- P16-to-P37/44 mosaic editing can miss embryonic functions of Agrin, LRP4, or
  MuSK in cortical and hippocampal development.
- Whole brain minus hindbrain, NeuN-positive FACS, and focal thalamic
  glutamatergic grouping under-sample motor neurons, muscle, Schwann cells,
  glia, and extracellular compartments in which agrin biology is strongest.
- Several null comparators had weak signatures themselves, so they are most
  informative collectively and mechanistically; no single zero count is enough
  to prove what `Agrn` must do.
