# Cox6b1 DEG-count prediction trace

## Question and endpoint

The task is to predict the held-out value of `n_degs` for each target in
`046_Cox6b1.csv`. The manifest contains one requested perturbation:
`Cox6b1`.

I treated `n_degs` exactly as defined by the focal training CSV: the number of
measured genes in `151 TH Prkcd Grin2c Glut` with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05`. This count includes
the perturbed target transcript if that row is measured and passes FDR. In the
training set, for example, `Cox5a`, `Cyc1`, `Ndufa4`, and `Ndufs8` each have
`n_degs = 1`, and the parquet shows that the singleton in this focal cell group
is the target's own transcript.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for the observed focal `n_degs` of held-in perturbations.
- `[local file: training_de_all_cell_groups.parquet]`
  for focal log-fold changes, adjusted p-values, and matched cell counts for
  mechanistic analogs.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`, especially the synthesized
  high-confidence Complex-IV claim and Cox5a/Cox4i1/Ndufa4 finding graph. This
  corpus is an interpretation layer over the same experiment, not independent
  replication.
- PubMed and the biological literature for `Cox6b1`/COX6B1 function:
  mammalian complex-IV structure and NDUFA4 assignment to cytochrome-c oxidase
  (Balsa et al. 2012, PMID:22902835; Zong et al. 2018,
  DOI:10.1038/s41422-018-0071-1), COX6B1 human complex-IV deficiency
  (Abdulhag et al. 2014, DOI:10.1038/ejhg.2014.85, PMID:24781756), COX6B/COA6
  overlap in COX2 biogenesis (Ghosh et al. 2015, DOI:10.1093/hmg/ddv503,
  PMID:26669719), a human COX6B1 knockout/variant analysis showing that COX6B1
  is required for early complex-IV assembly and later stabilization (Cunatova
  et al. 2025, DOI:10.1016/j.jbc.2025.111070, PMID:41419202), and the
  ATF4-centered mammalian mitochondrial-stress response used as the expected
  nuclear transcriptional positive-control program (Quiros et al. 2017,
  DOI:10.1083/jcb.201702058, PMID:28566324).

## Computation over the held-in dataset

I first read the focal count CSV and used its distribution to calibrate count
scale. It is very zero-inflated: among 1,674 held-in targets, the median count
is 0, the 75th percentile is 1, and 95% of targets have 18 or fewer DEGs.

I then selected respiratory-chain and Complex-IV analogs present in the
training set and joined them to their focal counts. In the eight most relevant
Complex-IV structural/assembly perturbations, six were zero and the only two
nonzero values were singleton self-transcript hits:

| target | focal `n_degs` |
|---|---:|
| `Coa8` | 0 |
| `Cox11` | 0 |
| `Cox4i1` | 0 |
| `Cox5a` | 1 |
| `Cox6a1` | 0 |
| `Cox7b` | 0 |
| `Cox8a` | 0 |
| `Ndufa4` | 1 |

Adding nearby respiratory-chain comparators in the Cox5a corpus finding did not
increase the response breadth: `Cyc1 = 1`, `Uqcrfs1 = 0`, `Ndufb7 = 0`, and
`Ndufs8 = 1`. A broader regex panel of 38 `Cox*`, `Coa*`, `Nduf*`, `Uqcr*`,
`Cyc1`, `Sdha`, and `Lrpprc` targets contained 22 zeros and 16 ones, with no
member above one DEG in the focal training-count file.

For expression-pattern evidence, I used `pyarrow.dataset` predicate pushdown to
pull only the `151 TH Prkcd Grin2c Glut` rows for 14 Complex-IV and
respiratory comparators. The filtered table had `14 x 17,259 = 241,626`
measured-gene rows. In the focal group:

- `Cox5a` had one FDR<0.05 row, `Cox5a` itself
  (`log2FC = -1.231`, `p_adj = 5.39e-21`).
- `Ndufa4` had one FDR<0.05 row, `Ndufa4` itself
  (`log2FC = -0.803`, `p_adj = 1.08e-5`).
- `Cox4i1` and `Cox6a1` showed visible but non-significant self-RNA drops
  (`Cox4i1 p_adj = 0.176`; `Cox6a1 p_adj = 0.0726`).
- `Coa8`, `Cox11`, `Cox7b`, `Cox8a`, `Ndufb7`, `Uqcrfs1`, and `Lrpprc` had no
  FDR<0.05 row.
- `Opa1` was a counterexample mitochondrial positive control, with 37 focal
  DEGs headed by ATF4/ISR genes such as `Asns`, `Mars1`, `Chac1`, and `Ddit3`;
  therefore the assay can detect a mitochondrial nuclear-stress program when
  it is triggered in this cell class.

The runtime profile comparison for the held-in Complex-IV cohort
(`Coa8`, `Cox11`, `Cox4i1`, `Cox5a`, `Cox6a1`, `Cox7b`, `Cox8a`, `Ndufa4`)
also reported six nodes with no significant features and two with 1-9
significant features. No pair in the inspected cohort shared a positive or
negative FDR-significant feature in this focal group. The weak whole-vector
similarities therefore mark shared flatness and broad rank-level background,
not a coherent COX-depletion module.

The same-experiment Distributed Agents corpus matched this direct computation. Its
Complex-IV claim states that acute perturbation of represented Complex-IV
structural subunits and assembly genes is buffered at the neuronal nuclear RNA
level, producing flat or singleton responses rather than a coherent
cytochrome-c-oxidase-loss or recurrent mitochondrial-stress program. The Cox5a
finding explicitly compared `Cox4i1`, `Cox6a1`, `Cox7b`, `Cox8a`, `Ndufa4`,
`Cox11`, `Coa8`, `Ndufb7`, `Ndufs8`, `Cyc1`, and `Uqcrfs1`; Ndufa4 and Cox4i1
findings independently bounded the same interpretation.

## Target-specific reasoning

`Cox6b1` encodes the ubiquitous nuclear COX6B subunit of cytochrome-c oxidase.
External data make it a genuine Complex-IV gene rather than a superficial
symbol match: biallelic human COX6B1 mutations can cause isolated complex-IV
deficiency with encephalomyopathy and cardiomyopathy, Cox12/COX6B interacts
genetically and biochemically with COA6/SCO proteins around COX2 biogenesis,
and complete human-cell COX6B1 knockout disrupts both early assembly and late
stabilization of complex IV. Thus the closest held-in analogs are nuclear
Complex-IV members and COX biogenesis factors, not generic mitochondrial genes.

Those closest analogs argue for an approximately null focal snRNA-seq count.
`Cox4i1`, `Cox5a`, `Cox6a1`, `Cox7b`, `Cox8a`, `Ndufa4`, `Cox11`, and `Coa8`
cover structural subunits plus copper/assembly-adjacent COX biology. In the
focal endpoint they produced no downstream shared DEG: six were exactly zero,
and `Cox5a`/`Ndufa4` reached one only through the perturbed transcript itself.
`Cox6b1` was not induced or suppressed by the held-in COX perturbations, so the
dataset did not show a compensatory `Cox6b1` RNA module that would make its own
loss an outlier.

The main counterexample is `Opa1`, because mitochondrial inner-membrane stress
can trigger a detectable ATF4-like program in these thalamic glutamatergic
neurons. I rejected `Opa1` as a quantitative analog for `Cox6b1`: OPA1 controls
mitochondrial inner-membrane fusion and cristae architecture rather than a
single COX holoenzyme subunit, and the corpus specifically notes that Opa1-like
ATF4/ISR activation was not a generic result of perturbing held-in OXPHOS or
Complex-IV targets.

For the final integer I therefore set `Cox6b1` below the FDR detection
threshold. A self-target singleton is possible, as seen for `Cox5a` and
`Ndufa4`, but four of the six other COX structural/assembly genes had no
significant self or downstream row in this exact focal label. The within-dataset
probability mass is on 0 with a tail at 1, and there is no evidence for a broad
positive state. I predict:

| target | predicted `n_degs` |
|---|---:|
| `Cox6b1` | 0 |

## Limits

`Cox6b1` itself is held out, so the prediction extrapolates from related
subunits and assembly factors rather than measuring any Cox6b1 guide. The assay
uses acute, sparse, mosaic AAV-CRISPR in postmitotic neurons; a near-zero
nuclear RNA profile does not rule out loss of cytochrome-c oxidase activity,
impaired ATP production, altered firing, subtle metabolite changes, or
selection before nuclei were recovered. The same-complex comparators also have
heterogeneous guide effectiveness as judged by self-RNA, but self-RNA loss is
not a reliable measure of protein loss. Finally, because the endpoint includes
the target transcript, the difference between 0 and 1 is partly a guide/NMD
question that is not knowable from held-in COX biology alone.
