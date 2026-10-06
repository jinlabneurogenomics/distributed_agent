# Cox6b1 DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and scope

I interpreted the task as one scalar held-out prediction: for the completely
withheld `Cox6b1` perturbation, predict the number of measured genes whose
Wilcoxon Benjamini-Hochberg adjusted p-value would be below 0.05 in the focal
`151 TH Prkcd Grin2c Glut` thalamic glutamatergic group. The endpoint is the
dataset's assay-specific DEG count, not Complex-IV activity, editing
efficiency, target RNA depletion, cell survival, or biological severity.

The supplied target list contained one row:

| target_name | predicted_n_degs |
|---|---:|
| Cox6b1 | 0 |

I resolved two important ambiguities as follows.

First, the count endpoint includes the perturbed gene's own transcript if that
row passes FDR. This matters because the small `n_degs=1` counts for several
respiratory-chain targets are self-depletion singletons rather than broad
downstream states. Second, `Cox6b1` itself is present in the measured-gene panel
for the focal class, including all 1,674 training perturbations, so predicting
zero is not forced by absence of the measured Cox6b1 transcript.

## Sources used

* Declared training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
* Declared differential-expression Parquet:
  `training differential-expression dataset`
* Declared held-out target manifest:
  `single-target request for Cox6b1`
* Run-local dataset portrait, task bindings, compact coverage, and capability
  manifest under `codex_runtime/pipeline/`.
* The same-experiment July PerturbAI semantic corpus
  `july_260713_sourceguard_1773_v1`, queried with `corpus.findings`,
  `corpus.calibration`, `corpus.graph`, and `corpus.report_evidence` entrypoints
  for non-held-out Cox and respiratory-chain analogs. No same-experiment
  semantic record was available for held-out `Cox6b1`.
* External PubMed literature for the Cox6b1 biological prior:
  Abdulhag et al. 2014, DOI `10.1038/ejhg.2014.85`, PMID `24781756`;
  Ghosh et al. 2015, DOI `10.1093/hmg/ddv503`, PMID `26669719`;
  Cunatova et al. 2025, DOI `10.1016/j.jbc.2025.111070`, PMID `41419202`.
* External curated database annotations bundled in the same-experiment corpus,
  especially Mouse Genome Informatics for Cox genes and UniProtKB reviewed
  entries for Complex-IV membership.

## Computation over the declared dataset

I first read the training CSV to calibrate the focal endpoint. It contains
1,674 non-held-out perturbations: 1,205 have `n_degs=0`, 469 have a positive
count, the median is 0, the 75th percentile is 1, and the distribution is
strongly right-skewed with a few very large responses such as `Uba5`,
`Tpr`, `Sin3a`, `Rnpc3`, and `Zbtb7a`. That means a mechanistic neighbor with
0-1 DEGs is informative; it is not just global shrinkage to the median.

I then queried the Parquet, restricting rows to `group_name =
'151 TH Prkcd Grin2c Glut'` and to respiratory-chain genes selected before
looking at hidden Cox6b1 data: Complex-IV structural or assembly analogs
`Cox4i1`, `Cox5a`, `Cox6a1`, `Cox7b`, `Cox8a`, `Cox11`, `Coa8`, and `Ndufa4`;
Complex-I counterexamples including `Ndufs2`, `Ndufs4`, `Ndufs7`, and
`Ndufv1`; Complex-III genes `Uqcrb`, `Uqcrc2`, `Uqcrfs1`, and `Uqcrh`; and
nearby mitochondrial-function genes `Sdha`, `Slc25a4`, and `Lrpprc`.

The operation was simply:

```sql
SELECT gene_target,
       sum(pvals_adj < 0.05) AS n_fdr05,
       min(pvals_adj) AS min_padj,
       avg(n_pert_matched) AS n_pert,
       avg(n_ctrl_matched) AS n_ctrl
FROM training_de_all_cell_groups.parquet
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (<respiratory-chain analog targets>)
GROUP BY gene_target;
```

Each queried target had 17,259 focal measured-gene tests and the same 23,679
matched control nuclei; perturbed nuclei ranged from 100 for `Cox7b` to 340 for
`Cox6a1`. The focal counts matched the training endpoint:

| target | focal FDR<0.05 genes | key focal evidence |
|---|---:|---|
| Cox11 | 0 | no FDR genes; lowest adjusted p-value 1.0 |
| Cox4i1 | 0 | the self row was lowest but did not pass, `padj=0.176` |
| Cox5a | 1 | single FDR hit was `Cox5a` itself, `padj=5.39e-21` |
| Cox6a1 | 0 | the self row was lowest, `padj=0.0726` |
| Cox7b | 0 | no focal FDR genes |
| Cox8a | 0 | no focal FDR genes |
| Coa8 | 0 | no FDR genes; lowest adjusted p-value 0.762 |
| Ndufa4 | 1 | single FDR hit was `Ndufa4` itself, `padj=1.08e-05` |
| Ndufs2 | 1 | single FDR hit was `Ndufs2` itself |
| Ndufs4 | 0 | no focal FDR genes |
| Ndufs7 | 0 | no focal FDR genes |
| Ndufv1 | 0 | no focal FDR genes |
| Sdha | 1 | single FDR hit was `Sdha` itself |
| Uqcrb | 0 | no focal FDR genes |
| Uqcrc2 | 1 | single FDR hit was `Uqcrc2` itself |
| Uqcrfs1 | 0 | no focal FDR genes |
| Uqcrh | 0 | no focal FDR genes |
| Slc25a4 | 1 | single FDR hit was `Slc25a4` itself |
| Lrpprc | 0 | no focal FDR genes |

Among the eight closest represented Complex-IV structural/assembly analogs,
six had `n_degs=0` and two had `n_degs=1`; across a broader set of 38 Cox,
Nduf, Sdh, Uqcr, Lrpprc, and Slc25a4 perturbations, the total focal DEG burden
was only 16 and no target exceeded 1 DEG. The occasional one-count cases are
therefore not mitochondrial-stress programs. The leading rows for Cox-family
perturbations also showed no shared downstream gene: `Cox5a`, `Cox4i1`, and
`Cox6a1` were led by their own transcripts, while `Cox11`, `Cox7b`, `Cox8a`,
and `Coa8` had no significant focal row at all.

## Same-experiment analogs and biological transfer

`Cox6b1` encodes a nuclear cytochrome-c-oxidase subunit facing the
intermembrane space. Severe COX6B1 loss is biologically capable of disrupting
Complex IV: Abdulhag et al. reported a human p.R20C COX6B1 patient with
isolated COX deficiency, barely detectable COX6B1 protein, and rescue by
wild-type COX6B1 cDNA; Ghosh et al. linked yeast Cox12/COX6B to COX2
biogenesis and copper-delivery interactions with Coa6/Sco proteins; and
Cunatova et al. found that COX6B1 knockout in human cells can abolish Complex
IV by affecting redox-sensitive early assembly as well as late stabilization.

The causal transfer model for the focal count is therefore:

`AAV CRISPR loss of a nuclear COX subunit -> reduced/stressed Complex-IV
assembly or stability -> possible electron-transport stress, ATF4/ISR,
UPRmt, redox, mitophagy, OXPHOS-compensation, or synaptic secondary programs
-> only edited neurons that survive and retain the 151-class state are sampled
3-4 weeks later -> Scanpy Wilcoxon FDR in nuclear RNA`.

The closest same-outcome priors are same-enzyme or same-assembly interventions
that should injure the same limiting terminal oxidase step if the P16 sparse
neuronal perturbation crosses the RNA-response threshold.

* `Cox4i1`, `Cox5a`, `Cox6a1`, `Cox7b`, `Cox8a`, and `Ndufa4` encode
  mammalian Complex-IV structural or associated subunits. The July corpus
  annotates `Cox4i1` as pan-neuronally downstream-null and explicitly reports
  that represented Complex-IV subunits and `Cox11` converged mainly by being
  flat, with no recurrent FDR gene module. In the focal count table the Cox
  structural genes were `0, 1, 0, 0, 0`; the single `Cox5a` DEG was the target
  itself. This is the strongest within-dataset evidence and points to `0` or
  at most a self-only count for `Cox6b1`.
* `Cox11` is a Complex-IV copper-insertion/assembly factor. It had
  `n_degs=0` in the focal group and the July corpus summarized it as producing
  no corrected neuronal transcriptional response in any of the 23 measured
  groups. That argues that even perturbing the COX assembly path did not
  generate a broad Cox/Atf4/Ddit3/Chac1/Trib3 stress state in this assay.
* `Coa8` had `n_degs=0`, and same-experiment Findings contrasted its flat
  profile with the strong `Opa1` mitochondrial-stress ISR in the same
  experiment. This is a counterexample to the idea that every mitochondrial
  perturbation must be silent because the readout cannot detect mitochondrial
  stress; the readout can detect it, but these single COX assembly/subunit
  interventions did not cross that threshold.
* The broader OXPHOS checks were also near-zero. Complex-I genes such as
  `Ndufs2` and `Ndufa4`, the Complex-II gene `Sdha`, the Complex-III gene
  `Uqcrc2`, and the ADP/ATP carrier `Slc25a4` showed only self-singleton
  counts, while `Ndufs4`, `Ndufs7`, `Ndufv1`, `Uqcrb`, `Uqcrfs1`, `Uqcrh`, and
  `Lrpprc` were at zero. This lowers the prediction for `Cox6b1`; there was no
  hidden recurrent OXPHOS-response module in the focal cells.

## Cox6b1 decision

I predicted `Cox6b1 = 0`.

The evidence for a biological effect is external and biochemical: COX6B1 is a
real Complex-IV subunit, and hard loss can destabilize Complex IV. The evidence
for the requested DEG-count endpoint is almost entirely within-dataset and it
points in the other direction. Acute, mosaic, postmitotic CRISPR perturbation
of the represented nuclear COX subunits and COX assembly factor produced a
focal count of 0 or a one-gene self-transcript count. These perturbations are
closer to Cox6b1 than generic mitochondrial disease or OXPHOS labels because
they hit the same terminal oxidase complex in the same cells, age window,
modality, readout, and FDR procedure.

I did not promote Cox6b1 to 1 solely for possible self-depletion. Cox6b1 was
measured in the focal group, but self-target depletion in this atlas is
uncorrelated with downstream effect and is not reliable gene by gene. Among the
same-complex focal analogs, only `Cox5a` crossed by the target transcript
itself; `Cox4i1` and `Cox6a1` were self-led but still below threshold, and
`Cox11`, `Cox7b`, `Cox8a`, and `Coa8` did not approach a corrected focal hit.
The best integer point estimate is therefore no FDR-0.05 genes rather than a
single Cox6b1 self row.

## Limits

This prediction is extrapolated because the held-out Cox6b1 signature and
target-level count were absent from both declared inputs, and Cox6b1 had no
node in the selected same-experiment graph. The transfer assumes that partial
AAV-CRISPR Cox6b1 loss in recovered 151-class neurons is buffered like nearby
nuclear Complex-IV subunit and assembly perturbations; it could be wrong if the
four Cox6b1 guides uniquely deplete Cox6b1 RNA more efficiently than the
represented Cox targets, if COX6B1 is a more limiting subunit in these thalamic
neurons, or if its perturbation produces a small self-transcript hit without a
downstream response. The Parquet measures survivor-conditioned nuclear RNA
only, not indel rates, protein, Complex-IV assembly, oxygen consumption, ATP,
ROS, or neuronal loss, so zero predicted DEGs should not be read as no
biochemical Complex-IV perturbation.
