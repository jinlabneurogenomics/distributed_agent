# Gpr12 held-out DEG-count prediction

## Question interpreted

The requested target manifest contains one held-out perturbation:

```text
Gpr12
```

I interpreted the endpoint as the assay-specific count of measured genes with
`pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` cells after sparse postnatal
AAV-CRISPR loss of the listed target. A value of zero therefore means no
measured gene is expected to pass the Wilcoxon BH threshold in that focal group,
not that GPR12 has no neuronal role.

`Gpr12` is absent from the training endpoint CSV and absent as a trained
`gene_target` in the differential-expression parquet by construction. The
closest paralogs, `Gpr3` and `Gpr6`, were not available as training
perturbations either, so the prediction has to transfer from less direct GPCR,
lysophospholipid-receptor, and cAMP-pathway perturbations.

## Sources used

* Requested-target manifest:
  `[local file: 095_Gpr12.csv]`.
* Training endpoint file:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
* Full non-held-out DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
* Distributed Agents corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`. This release had no direct
  `Gpr12` target context, but it did have same-experiment claims for GPCR,
  G-protein, adenylyl-cyclase, PDE, PKA, and receptor-family comparators.
* Distributed Agents runtime profile comparison
  `gpr12_gpcr_camp_profile_compare.json`, generated in this run for the
  GPCR/cAMP comparison set in `151 TH Prkcd Grin2c Glut`.
* PubMed literature for GPR12 biology:
  * Saeki et al. 1993, FEBS Lett, DOI `10.1016/0014-5793(93)80828-i`.
  * Ignatov et al. 2003, J Neurosci, DOI `10.1523/JNEUROSCI.23-03-00907.2003`.
  * Song et al. 1995, Genomics, DOI `10.1006/geno.1995.1154`.
  * Tanaka et al. 2007, J Biol Chem, DOI `10.1074/jbc.M700911200`.
  * Martin et al. 2015, PLoS One, DOI `10.1371/journal.pone.0138463`.
  * Morales et al. 2018, Drug Metab Rev, DOI
    `10.1080/03602532.2018.1428616`.
  * Hsiao et al. 2020, Cell, DOI `10.1016/j.cell.2020.09.011`.
  * Li et al. 2022, Sci Bull, DOI `10.1016/j.scib.2022.12.023`.
  * Frank et al. 2012, PLoS One, DOI `10.1371/journal.pone.0042395`.

## Computation over the supplied DE data

I first read the focal training endpoint CSV and extracted all obvious
same-assay GPCR/cAMP comparisons: available `Gpr*` targets, lipid GPCRs,
Gs/Golf transducers, membrane adenylyl cyclases, PDEs, PKA/Epac genes, and
several cAMP-coupled receptor families. The focal endpoint table has 1,674
training targets, with a median of 0 DEG and 75th percentile of 1 DEG; zeros
are therefore common, so I did not use sparsity alone as the decision rule.

I then scanned the parquet only for the focal cell group and the selected
candidate comparators:

```python
filt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(comparator_targets)
)
dataset.to_table(
    columns=[
        "names", "gene_target", "logfoldchanges",
        "pvals_adj", "n_pert_matched", "n_ctrl_matched",
    ],
    filter=filt,
)
```

That returned 17,259 measured genes for each requested comparator. I used the
rows with `pvals_adj < 0.05` to confirm whether nonzero endpoint counts were
real downstream programs or simply self-transcript calls.

I also ran Distributed Agents runtime `profile_compare` over 34 represented GPCR/cAMP
perturbations in the focal cell group, using `logfoldchanges` as the signed
profile and `pvals_adj < 0.05` as significance. In that cohort, 26/34
perturbations had no FDR-significant features in the focal group; only two had
10 to 49 features. The positive-tail overlap across the full cohort was weak
and FDR-level program overlap was essentially absent, so the comparison set did
not define a coherent GPR12-like expression module that should override the raw
endpoint counts.

Finally, I checked `Gpr12` as a measured feature. It was present in all 1,674
non-held-out focal signatures, which means a `Gpr12` self-transcript effect
could in principle count toward `n_degs`; the held-out file simply has no
`Gpr12` perturbation row.

## Target-specific reasoning

### Gpr12

**External mechanism.** GPR12 belongs to the small GPR3/GPR6/GPR12 orphan
class-A GPCR subfamily, whose members are predominantly brain expressed and
constitutively stimulate adenylyl cyclase/cAMP signaling in heterologous assays
and neurons (Song et al. 1995; Tanaka et al. 2007; Martin et al. 2015; Morales
et al. 2018). Li et al. resolved an agonist-free GPR12-Gs structure and
confirmed high constitutive Gs coupling and intracellular cAMP elevation for
GPR12. Ignatov et al. proposed sphingosylphosphorylcholine as a GPR12 ligand
and reported developmental CNS expression, although Morales et al. review that
the endogenous ligand status of this orphan subfamily remains unsettled. Hsiao
et al. found that thalamic Gpr12 modifies short-term memory and thalamus-PFC
synchrony in mice. Those data make a thalamic neuronal effect biologically
plausible, but they point mainly to cAMP, PKA, neurite, excitability, and
circuit readouts rather than to a known large cell-autonomous basal mRNA
program three to four weeks after a sparse postmitotic loss-of-function edit.
Frank et al. also found only modest organism-level effects in C57BL/6-enriched
Gpr12 mutant mice.

**Closest same-experiment analogs.** Direct paralog transfer from `Gpr3` or
`Gpr6` was impossible because neither was a training perturbation. The represented
`Gpr*` perturbations are not true GPR3/GPR6/GPR12 paralogs, so I used them as
weak receptor-buffering controls rather than as primary family evidence.

| training target | focal `n_degs` | focal expression evidence |
| --- | ---: | --- |
| `Gpr156` | 0 | no FDR gene; best adjusted p-value 0.339 |
| `Gpr158` | 1 | the only FDR gene was the target transcript itself, `Gpr158`, logFC -0.991, q 3.4e-26 |
| `Gpr161` | 0 | no FDR gene; best adjusted p-value 1.0 |
| `Gpr179` | 0 | no FDR gene; best adjusted p-value 0.519 |
| `Gpr45` | 0 | no FDR gene; best adjusted p-value 1.0 |
| `Gprasp2` | 1 | the only FDR gene was the target transcript itself, logFC -0.491, q 0.0071 |
| `Gprc5b` | 0 | no FDR gene; best adjusted p-value 1.0 |

The within-corpus `Gpr158` findings likewise describe the GPR158 surface as
near-null across juvenile NeuN+ brain and non-phenocopied by represented
GPR/RGS, mGluR, and cAMP-pathway comparators. Thus even receptor perturbations
with a measurable receptor self-row did not produce a broader transcriptional
program in this screen.

The sphingolipid/lysophospholipid receptor comparison was also flat but weak:
`S1pr2` had `0` DEG and `Lpar6` had `0` DEG in the focal group. The Distributed Agents
corpus describes `S1pr2` as a pan-neuronal transcriptomic null in this
postnatal screen and emphasizes that S1PR2/Nogo-like effects are not recovered
as a stable uninjured neuronal RNA program. These are pathway-adjacent
counterexamples, not direct GPR12 paralogs, especially because GPR12 is an
orphan receptor and the sphingosylphosphorylcholine connection is disputed.

The strongest mechanistic analogs in the training set were the represented
Gs/cAMP arm perturbations that should sit downstream of constitutively active
GPR12:

| training target | focal `n_degs` | focal expression evidence |
| --- | ---: | --- |
| `Gnas` | 0 | no FDR genes |
| `Gnal` | 0 | no FDR genes |
| `Adcy1` | 0 | no FDR genes; minimum q 0.139 |
| `Adcy3` | 0 | no FDR genes; `Adcy3` self q 0.112 |
| `Adcy5` | 0 | no FDR genes |
| `Pde1c` | 0 | no FDR genes; minimum q 0.180 |
| `Pde4b` | 0 | no FDR genes |
| `Pde4d` | 0 | no FDR genes |
| `Pde10a` | 0 | no FDR genes; minimum q 0.304 |
| `Rapgef4` | 0 | no FDR genes |
| `Prkaca` | 1 | the only FDR gene was `Prkaca` itself, logFC -0.940, q 7.9e-22 |
| `Prkar1a` | 1 | the only FDR gene was `Prkar1a` itself, logFC -0.569, q 0.0014 |

The same Distributed Agents corpus release had high-confidence and moderate-confidence
claims from `Adcy3`, `Gnas`, and `Pde1c` analyses that represented
dopamine/GPCR/cAMP/PDE perturbations do not collapse into one durable basal
neuronal cAMP transcriptome, and that acute biochemical linkage to cAMP or
CREB is insufficient to predict chronic basal CREB/immediate-early mRNA
responses in this assay. Those claims are directly aligned with the focal
counts above: `Gnas`, membrane `Adcy` genes, and PDEs were all exact zeros in
`151 TH Prkcd Grin2c Glut`.

Other cAMP-coupled receptor controls reinforced the same point. `Adrb2`,
`Adrb3`, `Drd2`, `Drd4`, `Drd5`, `Htr6`, and `Htr7` each had `0` DEG. The
class-C/metabotropic receptor controls were similarly sparse: `Grm5` and
`Grm8` were `0`, while `Grm1` and `Grm7` had a single self-transcript DEG each.
In contrast, the focal group could report real transcription-factor
perturbations: `Creb1` had 10 DEGs, headed by `Crem` at q 3.8e-7, and `Klf9`
had 19 DEGs. I treated these as positive assay counterexamples: the absence of
a `Gnas`/`Adcy`/PDE response was not simply because the focal group was unable
to yield any DEGs.

**Zero/nonzero decision.** I predicted `0`, not `1`, because the available
GPR/cAMP perturbations almost never generated downstream FDR genes in the focal
group, and the one-DEG cases were mostly target self-depletion rows. GPR12 is
measured in this cell group, but the compact single-exon architecture reported
for human GPR3/GPR6/GPR12 and avian GPR-family orthologs makes this subfamily a
poor case for assuming nonsense-mediated target-mRNA decay from a CRISPR
frameshift. The endpoint also cannot rely on evoked Gs/cAMP signaling: the
analogous proximal cAMP targets were buffered at basal snRNA-seq. I therefore
expect no feature to cross q < 0.05 for held-out `Gpr12`.

## Limits and extrapolation

* The closest biological paralogs, `Gpr3` and `Gpr6`, were not trained
  perturbations, so the prediction uses pathway neighbors and more distant GPCR
  controls.
* The GPR12 literature contains thalamic and cAMP biology, but those studies
  used heterologous expression, cultured neurons, germline genetics, or circuit
  perturbations rather than the exact sparse P16 AAV-Cas9 loss-of-function
  snRNA-seq endpoint.
* The assay measures basal nuclear RNA after chronic sparse editing. It does
  not measure cAMP, phospho-PKA/phospho-CREB, receptor trafficking, neurite
  structure, thalamocortical synchrony, or evoked activity. A predicted zero is
  therefore compatible with altered GPR12 signaling.
* The target transcript itself is a residual uncertainty. If Gpr12 guides happen
  to destabilize the transcript unusually well in this focal cell group, the
  count could become one even without any downstream response. I did not see a
  data-driven reason to assume that self-DEG.

## Point prediction

`Gpr12` -> `0`
