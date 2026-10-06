# DEG-count prediction trace

## Question and endpoint alignment

The requested held-out target list contains one perturbation, `Arsb`, and the
output is a scalar point prediction for the number of Benjamini-Hochberg FDR
0.05 DEGs in `151 TH Prkcd Grin2c Glut` cells.

I treated `n_degs` exactly as it is computed in the supplied training CSV:
all measured genes with `pvals_adj < 0.05` in the focal cell group are counted,
including the perturbed target transcript itself when that row is significant.
The held-out `Arsb` target rows are absent from the training Parquet by
construction, but the measured-gene row `names == "Arsb"` is present in all
1,674 focal-cell training perturbations. Those rows were used only to check
whether Arsb is a recurrent downstream lysosomal-stress marker; they are not
an Arsb knockout signature.

The endpoint is directly observed for the 1,674 non-held-out training
perturbations in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`. For `Arsb` itself the
endpoint is absent, so the prediction is a transfer from the training endpoint
and same-experiment expression surfaces.

## Sources

- Declared DE table:
  `training differential-expression dataset`.
- Declared focal training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared held-out manifest:
  `single-target request for Arsb`.
- Run-local task bindings, coverage, dataset portrait, and measurement
  registry in `codex_runtime/pipeline/`.
- Same-experiment PerturbAI July corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, queried through
  `corpus.findings` for compact reports on training analogs. I used the corpus
  as packaged interpretation of the same experiment, not as independent
  replication.
- PubMed literature for the external ARSB prior:
  Valayannopoulos et al. 2010, DOI `10.1186/1750-1172-5-5`,
  PMID `20385007`; Harmatz and Shediac 2017, DOI `10.2741/4490`,
  PMID `27814620`; Stewart et al. 1997, DOI `10.1038/sj.gt.3300364`,
  PMID `9068797`.

No explicit ranked or partially ranked supervision was supplied. The
ranking-only Perturb-seq feature workbench, graph-review nomination, and
ordering-validation capabilities were therefore not policy-available for this
scalar count task.

## Quantitative checks over the declared inputs

The held-out manifest has one row, `Arsb`, and the target is absent from both
training endpoint targets and `gene_target` values in the Parquet, as required.
The focal training CSV has 1,674 unique targets with `n_degs` ranging from 0 to
2,677. Most focal perturbations are transcriptionally quiet:

| quantity | value |
|---|---:|
| training targets | 1,674 |
| targets with `n_degs == 0` | 1,205 |
| targets with `n_degs == 1` | 276 |
| targets with `n_degs <= 5` | 1,546 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |

I then queried the focal rows for lysosomal hydrolases, lysosomal cofactors,
V-ATPase subunits, and endolysosomal trafficking genes. The strongest useful
training analogs and counterexamples were:

| training target | focal `n_degs` | focal expression-pattern evidence |
|---|---:|---|
| `Gaa` | 1 | the only FDR 0.05 focal hit was `Gaa` itself, logFC -0.709, adjusted p = 8.97e-16 |
| `Psap` | 1 | the only FDR 0.05 focal hit was `Psap` itself, logFC -1.277, adjusted p = 1.70e-28 |
| `Ppt1` | 1 | the only FDR 0.05 focal hit was `Ppt1` itself, logFC -0.536, adjusted p = 1.34e-05 |
| `Ctsb` | 1 | the only FDR 0.05 focal hit was `Ctsb` itself, logFC -1.480, adjusted p = 8.54e-43 |
| `Scarb2` | 1 | the only FDR 0.05 focal hit was `Scarb2` itself, logFC -0.811, adjusted p = 0.00246 |
| `Grn` | 1 | the only FDR 0.05 focal hit was `Grn` itself, logFC -0.770, adjusted p = 5.27e-05 |
| `Lamp2` | 0 | no FDR 0.05 hit; the self row was close but not called, adjusted p = 0.0537 |
| `Manba` | 0 | no downstream or self FDR 0.05 hit |
| `Asah1` | 0 | no downstream or self FDR 0.05 hit |
| `Sort1` | 0 | no downstream or self FDR 0.05 hit |
| `Gnptab` | 0 | no downstream or self FDR 0.05 hit |
| `Atp6v0a1` | 1 | the only FDR 0.05 focal hit was `Atp6v0a1` itself |
| `Atp6v1a` / `Atp6v1b2` / `Atp6v1e1` | 0 / 0 / 0 | V-ATPase subunits did not create a corrected downstream stress state |
| `Atp6ap2` | 2 | one self hit plus one `Atp6v0a1` hit; still no broad lysosomal stress program |
| `Rab7` | 501 | strong counterexample with many late-endosomal, lysosomal, lipid, ISR/autophagy, and synaptic DEGs |
| `Vps35` | 17 | partial endolysosomal/retromer response |
| `Tsc2` | 86 | mTOR-lysosome growth-control counterexample |

`Arsb` itself, when used as a measured gene in the focal rows for other
perturbations, was not part of a recurrent stress module: all nine close
analog perturbations above had `Arsb` adjusted p = 1.0, and `Rab7` left `Arsb`
essentially unchanged in the focal class (`logfoldchanges = -0.029`,
`scores = -0.082`). Across all 1,674 focal training perturbations, the
mean absolute `Arsb` log fold-change was only 0.149.

Across all focal targets, 1,642 training perturbations had a self row and 319
of those self rows were significant at FDR 0.05. The soluble lysosomal
hydrolase/cofactor group most relevant to ARSB was enriched for self-only
outcomes, so the prediction is not a dataset-wide generic zero; it is an
expectation that `Arsb` will, at most, reproduce the one-transcript pattern of
`Gaa`, `Psap`, `Ppt1`, `Ctsb`, `Scarb2`, and `Grn`.

## Target-specific reasoning

### `Arsb`

`Arsb` encodes arylsulfatase B, a lysosomal N-acetylgalactosamine
4-sulfatase needed for dermatan sulfate and chondroitin 4-sulfate
catabolism. Pathogenic human `ARSB` loss causes mucopolysaccharidosis VI
through lysosomal glycosaminoglycan storage
(Valayannopoulos et al. 2010; Harmatz and Shediac 2017). This makes ARSB a
soluble lysosomal hydrolase rather than a trafficking hub or a transcriptional
regulator. MPS VI is also primarily a multisystem connective-tissue and
visceral storage disease; intellectual disability is generally absent, unlike
heparan-sulfate MPS forms (Valayannopoulos et al. 2010). That weakens the
prior for an acute, neuron-intrinsic nuclear stress signature in the
postnatal NeuN-positive setting.

The closest represented training analogs are other individual lysosomal
soluble enzymes and cofactors. `Gaa`, the Pompe-disease lysosomal glycogen
hydrolase, had `n_degs = 1` in the focal cell group and the sole call was its
own transcript. The July same-experiment corpus reports that `Gaa` had no
non-`Gaa` FDR 0.10 downstream genes in any of the 23 recovered neuronal groups
and did not induce canonical lysosomal, autophagy, UPR/ISR, or glycogen
metabolism transcripts (`Gaa:F001`, `Gaa:F002`). This is relevant because GAA,
like ARSB, is a lysosomal lumen enzyme; both should be partially buffered in
a sparse mosaic tissue by residual enzyme and by extracellular enzyme uptake
through mannose-6-phosphate receptor routes, a route demonstrated for
lysosomal enzymes in neural cells by Stewart et al. 1997.

`Psap`, which generates saposins required for lysosomal sphingolipid
catabolism, is an even stronger severity counterexample: complete PSAP loss
causes lethal multi-lipid neurovisceral storage, yet P16 mosaic `Psap`
perturbation produced a self-only focal count of 1 and no downstream FDR 0.10
genes in 20 measured neuronal groups (`Psap:F001`). The packaged report also
found no TFEB/CLEAR, cathepsin, V-ATPase, autophagy, or ISR rebound after
`Psap` loss (`Psap:F002`) and no meaningful dense-signature neighbor
(`Psap:F004`). Thus a soluble lysosomal storage enzyme can be biologically
important while still scoring as only its own mRNA in this assay.

The single hydrolase and lysosomal-cofactor controls point in the same
direction:

- `Ctsb` had `n_degs = 1`, only `Ctsb` itself; its corpus report describes a
  target-only perturbation surface with no non-self downstream FDR 0.10 genes
  in any recovered neuronal group and no TFEB/CLEAR or generic stress
  induction (`Ctsb:F001`, `Ctsb:F002`).
- `Ppt1`, `Grn`, and `Scarb2` each had `n_degs = 1` and only the targeted
  transcript in the focal class.
- `Asah1`, `Manba`, `Sort1`, and `Gnptab` had zero focal FDR 0.05 genes.
- `Lamp2`, a lysosomal membrane/autophagy gene rather than a lumen hydrolase,
  was also effectively flat in the focal class (`n_degs = 0`; self adjusted
  p = 0.0537) and failed to induce a canonical lysosomal, macroautophagy,
  CMA, UPR/ISR, or proteasome program in the corpus (`Lamp2:F001`,
  `Lamp2:F002`).

The appropriate counterexamples are not single lysosomal hydrolases but
central trafficking or signaling perturbations. `Rab7` had 501 focal DEGs and
the corpus reports a broad late-endosomal/lysosomal compensation module plus
sterol, ISR/autophagy, proteasome, and synaptic remodeling (`Rab7:F002` to
`Rab7:F006`). `Vps35`, `Vps54`, and `Tsc2` also produced nontrivial focal
counts. These show that the screen can detect endolysosomal stress when an
acute perturbation reaches a nucleus-visible state, but they sit upstream of
many cargos and compartments. They are poor ARSB count analogs because ARSB
hydrolyzes one glycosaminoglycan substrate branch and should not phenocopy a
global late-endosome motor, retromer, or mTOR-lysosome perturbation.

The zero/nonzero decision is therefore driven mostly by the within-dataset
self-only hydrolase evidence, with external ARSB biology used to choose among
possible lysosomal analogs. I predict no downstream response and one total
DEG, corresponding to a detectable `Arsb` self-transcript decrease but no
secondary FDR 0.05 genes. The estimate is rounded to exactly:

```text
Arsb -> 1
```

## Limits and extrapolation

The major uncertainty is the ARSB self row. Target-mRNA loss is visible for
many, but not all, lysosomal genes: `Lamp2` and `Sort1` were just below FDR
0.05, while `Asah1`, `Manba`, and `Gnptab` were not significant. The actual
`Arsb` guide efficacy, indel spectrum, baseline RNA abundance, and recovered
perturbed-nucleus count are held out, and the Parquet has no raw nuclear UMI
counts to estimate ARSB detectability directly. For that reason a true `0`
would not be surprising.

The predicted absence of downstream DE is more stable than the exact self
call. The same-experiment data repeatedly show acute, sparse, postnatal
neuronal loss of individual lysosomal hydrolases or cofactors being buffered
at the transcriptional level, but this does not exclude lysosomal substrate
accumulation, enzyme activity changes, altered proteostasis, or selective
loss of edited cells below the single-nucleus RNA endpoint. External ARSB/MPS
VI evidence comes mainly from complete germline human deficiency and enzyme
replacement contexts, not from mosaic P16 CRISPR loss in juvenile thalamic
glutamatergic neurons, so it is a mechanistic prior rather than direct
endpoint evidence.
