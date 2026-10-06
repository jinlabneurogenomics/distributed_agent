# DEG-count prediction trace

## Question and interpretation

The held-out manifest `229_Syn3.csv` contains one perturbation target:

| target_name |
| --- |
| Syn3 |

I interpreted the requested endpoint as the exact focal-cell count used in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the number of measured
genes in `151 TH Prkcd Grin2c Glut` nuclei with `pvals_adj < 0.05` after
Benjamini-Hochberg correction of Wilcoxon rank-sum p-values. The perturbed
gene itself can count as one of those DEGs if its own transcript is
significantly depleted, as seen for several training perturbations in this
cell group. I did not treat a zero as failed editing; in this assay many
perturbations of vesicle or ion-channel genes affect physiology without a
broad steady-state nuclear RNA response.

The requested `Syn3` perturbation is fully held out, so I did not look for a
`Syn3` target signature in the parquet. I transferred from non-held-out
training perturbations, emphasizing the exact focal cell group.

## Sources used

- Input differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Input focal DEG-count CSV:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Held-out manifest:
  `[local file: 229_Syn3.csv]`
- Distributed Agents same-experiment corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`
- Distributed Agents runtime `profile_neighbors` analysis over the focal parquet rows,
  using Wilcoxon `scores` over all measured genes to test whether Syn1/Syn2
  and vesicle-cycle anchors had coherent low-amplitude neighbors.
- NCBI PubMed/Entrez literature search for Syn3 and synapsin biology.

## Computational checks over the training data

I loaded the training counts and confirmed that the focal endpoint is sparse:
1,205 of 1,674 training perturbations have `0` DEGs, the median is `0`, the
75th percentile is `1`, the 90th percentile is `2`, and only 5% of targets have
more than 18 DEGs. This makes a small presynaptic response more likely than an
intermediate one unless the target belongs to a globally disruptive pathway.

From the parquet, I filtered to:

- `group_name == "151 TH Prkcd Grin2c Glut"`
- a presynaptic comparator panel centered on synapsins and the synaptic vesicle
  cycle: `Syn1`, `Syn2`, `Syp`, `Sv2a`, `Stx1b`, `Stxbp1`, `Dnm1`, `Synj1`,
  `Vamp1`, `Cplx1`, `Cplx2`, `Syt2`, `Unc13a`, `Unc13b`, `Unc13c`, `Bsn`,
  `Pclo`, `Rab3gap1`, `Rab3gap2`, `Nsf`, `Cltc`, `Scamp5`, `Slc32a1`, and
  `Napb`.

For each comparator I counted `pvals_adj < 0.05`, identified whether the only
hit was the target transcript itself, and retained the guide-matched nucleus
counts. I also asked `profile_neighbors` to compare the signed Wilcoxon-score
vectors of 11 anchors against all 1,674 training targets in the same focal
group; this was a check for hidden transcriptomic convergence when FDR gene
sets were empty or singletons.

Key focal analogs:

| training target | focal n_degs | focal FDR<0.05 genes | why it was compared |
| --- | ---: | --- | --- |
| Syn1 | 1 | Syn1 only | closest assayed synapsin paralog; vesicle reserve-pool protein |
| Syn2 | 0 | none | closest assayed synapsin paralog |
| Syp | 1 | Syp only | abundant synaptic-vesicle membrane protein |
| Sv2a | 1 | Sv2a only | synaptic-vesicle glycoprotein |
| Dnm1 | 1 | Dnm1 only | synaptic-vesicle endocytosis dynamin |
| Synj1 | 1 | Synj1 only | synaptic-vesicle recycling phosphatase |
| Vamp1 | 1 | Vamp1 only | vesicle SNARE |
| Cplx1 | 1 | Cplx1 only | SNARE complex regulator |
| Cplx2 | 0 | none | complexin paralog |
| Stx1b | 0 | none | plasma-membrane SNARE |
| Syt2 | 0 | none | vesicular calcium sensor |
| Unc13a | 0 | none | Munc13 priming factor |
| Unc13b | 0 | none | Munc13 priming factor |
| Unc13c | 0 | none | Munc13 priming factor |
| Bsn | 0 | none | active-zone scaffold |
| Pclo | 0 | none | active-zone scaffold |
| Nsf | 0 | none | SNARE disassembly ATPase |
| Slc32a1 | 0 | none | vesicular GABA transporter, same vesicle-release axis but transmitter-specific |
| Napb | 0 | none | NSF attachment protein |
| Cltc | 3 | Ero1b, Gabra4, Rbms1 | broader clathrin-mediated endocytosis counterexample, still very small in this cell group |
| Scamp5 | 3 | Scamp5, Fyttd1, Gabra1 | vesicle protein with a detectable but tiny non-self response |
| Stxbp1 | 1 | Stxbp1 only | core Munc18-1 fusion factor and the whole-atlas presynaptic outlier; even it is self-only in `151 TH Prkcd Grin2c Glut` |

The direct synapsin paralogs were almost at the assay floor. `Syn1` had 182
perturbed nuclei versus 23,679 controls and one DEG, but that DEG was the
`Syn1` transcript itself (`log2FC = -0.834`, adjusted p =
`1.59e-24`). `Syn2` had 195 perturbed nuclei and no significant gene in this
cell group; its own transcript moved downward but did not pass the FDR
threshold (`log2FC = -0.497`, adjusted p = `0.425`). Thus the only exact
paralog evidence is one self-only count and one zero-count profile.

The wider vesicle-cycle comparators reinforced that pattern. `Syp`, `Sv2a`,
`Dnm1`, `Synj1`, `Vamp1`, and `Cplx1` each registered one focal DEG, and in
each case the one DEG was the knocked-out transcript. `Cplx2`, `Syt2`,
`Unc13a`, `Stx1b`, `Nsf`, `Bsn`, and `Pclo` had none. The small non-self
counterexamples, `Cltc` and `Scamp5`, had only 3 DEGs each and are not
synapsins: clathrin is a central endocytic coat protein with broader membrane
traffic roles, while Scamp5 is a vesicle membrane protein whose three-gene
signature was not shared by the Syn1/Syn2 anchors.

The profile-neighbor artifact also argued against a hidden Syn3-like
subthreshold module. In the focal cell group, `Syn2` had no FDR genes and its
best whole-profile Pearson neighbor was only `r = 0.060` (`Phox2a`); `Syn1`
had only its self hit and its top whole-profile neighbor, `Rora`, reached only
`r = 0.133` and was not a vesicle-cycle gene. Top positive/negative feature
overlap coefficients were low, generally `0.10` or below for the synapsin
anchors. This is the pattern expected from near-null score vectors rather than
a coherent presynaptic expression state.

The Distributed Agents corpus had no `Syn3` node, but its same-experiment Syn1/Syn2
findings were directly relevant. The corpus summarized a high-confidence
claim that most represented acute presynaptic vesicle-cycle and active-zone
perturbations lack broad neuronal nuclear RNA responses, with `Stxbp1` as a
transcriptionally visible outlier elsewhere in the atlas. Syn2 finding F003
specifically contrasted nearly flat `Syn2`, `Syn1`, `Syp`, `Sv2a`, `Dnm1`,
`Cplx1`, and `Unc13a` with the broader `Stxbp1` response across matched
groups. Syn1 finding F005 reached the same partition and noted that `Syn3`
itself was not represented. These corpus findings come from the same
Perturb-seq release and agree with the focal-cell extraction above.

## Syn3 biological rationale

`Syn3` encodes synapsin III, the third mammalian synapsin gene product, a
neuron-specific synaptic-vesicle-associated phosphoprotein identified by Kao
et al. 1998 (DOI `10.1073/pnas.95.8.4667`). Synapsin C domains can homo- and
heterodimerize across family members, supporting shared vesicle-surface
biology with Syn1 and Syn2 (Hosaka and Sudhof 1999, DOI
`10.1074/jbc.274.24.16747`).

Loss-of-function biology does not make Syn3 a strong broad-transcription
candidate in this assay. Syn3 differs from Syn1/Syn2 in developmental timing:
it is enriched early, localizes to growth cones, and Syn3 suppression impairs
axon specification in cultured hippocampal neurons (Ferreira et al. 2000, DOI
`10.1523/JNEUROSCI.20-10-03736.2000`). Germline Syn3 knockout changes the
synaptic vesicle recycling pool, reduces synaptic depression, strongly affects
IPSCs, and delays axon outgrowth in culture (Feng et al. 2002, DOI
`10.1523/JNEUROSCI.22-11-04372.2002`). Later work connected Syn3 especially to
dopaminergic release: deletion of Syn3 was sufficient to increase evoked
striatal dopamine release in synapsin knockout comparisons (Kile et al. 2010,
DOI `10.1523/JNEUROSCI.2071-09.2010`), and Syn3 cooperates with alpha-synuclein
in dopamine neuron synaptic function (Zaltieri et al. 2015, DOI
`10.1242/jcs.157867`).

Those mechanisms point to presynaptic vesicle trafficking, axon development,
and dopaminergic terminal physiology rather than direct transcriptional
control. The experiment perturbed sparse postmitotic NeuN+ neurons from P16 to
P37-P44 and scored nuclear RNA in a `TH Prkcd Grin2c` glutamatergic group, not
dense embryonic cultures or purified adult dopaminergic terminals. The
developmental and dopamine literature therefore increases confidence that
Syn3 is biologically real, but it does not outweigh the local evidence that
single presynaptic-vesicle perturbations are usually zero or self-only by this
endpoint.

## Target-specific prediction

### Syn3

I predict `0` DEGs.

The main in-dataset drivers are the two paralogs and the broader vesicle-cycle
panel. The closest in-family perturbation `Syn2` had zero DEGs in the exact
focal cell group. `Syn1` had one DEG, but the one gene was `Syn1` itself, so
there was no downstream transcriptional state to transfer. Other presynaptic
vesicle and SNARE-axis genes also sat at the same floor: `Cplx2`, `Syt2`,
`Unc13a`, `Unc13b`, `Unc13c`, `Bsn`, `Pclo`, `Nsf`, `Rab3gap1`, `Rab3gap2`,
`Slc32a1`, and `Napb` were zero; `Syp`, `Sv2a`, `Dnm1`, `Synj1`, `Vamp1`, and
`Cplx1` were self-only singletons. The `Stxbp1` outlier from the whole-atlas
presynaptic corpus was not an outlier in this focal group because it too had
only one significant gene, `Stxbp1`.

For the zero/nonzero decision, I treated the probability of a single
self-transcript hit as the only serious reason to predict above zero. I still
chose `0` because Syn3's major described roles are early axon outgrowth and
dopamine-vesicle regulation, which are imperfect matches to acute editing of
postmitotic TH/Prkcd/Grin2c glutamatergic nuclei. Syn3 is also developmentally
downregulated relative to Syn1/Syn2, so its own mRNA was less likely than
`Syn1`, `Syp`, or `Sv2a` to cross FDR as a target-depletion-only hit in this
cell group.

## Limits and extrapolations

- Syn3 itself was absent from the training parquet and from the Distributed Agents
  same-experiment corpus, so the prediction extrapolates from Syn1, Syn2, and
  pathway relatives.
- The endpoint is a thresholded single-cell Wilcoxon count. A prediction of
  zero does not mean Syn3 has no vesicle, release, or behavioral effect.
- Many Syn3 papers use germline knockout, embryonic or cultured neurons,
  dopaminergic terminals, or disease models with alpha-synuclein aggregation.
  Those differ from sparse AAV CRISPR loss in juvenile postmitotic brain.
- Guide efficiency and target-RNA detectability are target-specific. Because
  self-transcript depletion alone created the single DEG for `Syn1`, `Syp`,
  `Sv2a`, `Dnm1`, `Synj1`, `Vamp1`, `Cplx1`, and `Stxbp1`, the largest
  uncertainty is whether `Syn3` mRNA itself would have been captured strongly
  enough to count as one DEG.
