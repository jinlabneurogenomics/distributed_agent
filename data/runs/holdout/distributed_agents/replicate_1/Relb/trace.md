# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The held-out target list for this run contains one perturbation, `Relb`. I
predicted the integer number of measured genes that would pass
Benjamini-Hochberg FDR 0.05 after acute mosaic CRISPR loss of `Relb` in
`151 TH Prkcd Grin2c Glut` neurons.

I treated the endpoint literally as this assay's `n_degs`: a thresholded
single-nucleus Wilcoxon count among recovered, class-assigned nuclei. The
training-count CSV directly observes this endpoint for non-held-out targets in
the focal class. The Parquet directly observes per-gene differential expression
for non-held-out targets only; `Relb` was completely absent as a perturbation
target and its own focal DEG count was therefore absent from the supplied
inputs. Target self-log-fold-change was not used as editing-efficiency evidence.

## Sources used

- Declared training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression Parquet:
  `training differential-expression dataset`.
- Run-local requested-target manifest:
  `single-target request for Relb`.
- Run-local task metadata: `task_bindings.json`, `coverage.json`,
  `capabilities.json`, and `measurement_registry.json`.
- Internal same-experiment semantic layer: PerturbAI July
  `260713_sourceguard_1773_v1` Findings ledger and BioKG graph. I used it only
  to read packaged interpretations for visible NF-kappaB comparators and to
  check whether a visible report explicitly named `Relb` as a comparator; the
  graph returned no such `Relb` comparator records.
- External literature retrieved through NCBI PubMed:
  Sun 2010, PMID 21173796, DOI 10.1038/cr.2010.177; Dejardin 2006, PMID
  16970925, DOI 10.1016/j.bcp.2006.08.007; Bonizzi et al. 2004, PMID 15470505,
  DOI 10.1038/sj.emboj.7600391; Yilmaz et al. 2003, PMID 12505990, DOI
  10.1093/emboj/cdg004; Weih et al. 1997, PMID 9104822, DOI
  10.1084/jem.185.7.1359; Fusco et al. 2008, PMID 19098713, DOI
  10.1038/embor.2008.227.

## Computations over the declared data

1. I loaded the requested-target CSV and confirmed that it contains exactly
   one target, `Relb`, and that `Relb` is absent from the 1,674-row focal
   training-count table.
2. I summarized the full focal training-count distribution. It is highly
   zero-inflated: 1,205/1,674 visible perturbations have `n_degs = 0`, the
   median is 0, the 75th percentile is 1, the 90th percentile is 2, and the
   high-count tail is dominated by spliceosome, proteasome, transcriptional,
   and protein-homeostasis targets such as `Uba5`, `Tpr`, `Sin3a`, `U2af2`,
   `Psmb4`, and `Psmc1`.
3. I queried the training endpoint for NF-kappaB, TLR, TNF-receptor,
   interferon, and STAT genes represented in the focal training set. The
   endpoint-nearest perturbations were all flat or nearly flat:

   | training perturbation | focal `n_degs` | why it was considered |
   |---|---:|---|
   | `Rel` | 0 | NF-kappaB/Rel transcription-factor paralog; c-Rel can dimerize with p50 |
   | `Nfkb1` | 0 | p105/p50 NF-kappaB subunit and direct c-Rel partner |
   | `Chuk` | 0 | IKKalpha, the kinase used by the noncanonical NIK to p100/p52-RelB pathway |
   | `Traf3` | 0 | TRAF-cIAP/NIK gate for noncanonical NF-kappaB signaling |
   | `Map3k7` | 0 | TAK1 kinase upstream of canonical NF-kappaB/MAPK signaling |
   | `Cd40` | 0 | TNF-family receptor that can induce noncanonical NF-kappaB in responsive immune or stromal cells |
   | `Tnfrsf13c` | 0 | BAFF-R, a noncanonical NF-kappaB-linked receptor |
   | `Tnfrsf1a` | 0 | TNF receptor upstream of canonical NF-kappaB |
   | `Tlr2`, `Tlr3`, `Tlr4`, `Tlr7`, `Tlr8` | 0 each | TLR inputs to canonical NF-kappaB and interferon wiring |
   | `Irf1`, `Irf3`, `Irf5`, `Irf8`, `Irf9` | 0 each | inflammatory/interferon transcriptional comparators |
   | `Stat1` | 1 | interferon-response comparator and a weak counterexample showing only one significant gene |
   | `Stat2`, `Stat3`, `Stat4`, `Stat5b` | 0 each | cytokine/JAK-STAT comparators |

4. I directly scanned the Parquet for selected NF-kappaB analogs across
   neuronal cell groups. `Chuk`, `Nfkb1`, `Rel`, `Traf3`, `Map3k7`, `Tlr4`,
   and `Tnfrsf1a` had 0 genes at FDR 0.05 in `151 TH Prkcd Grin2c Glut`; the
   same query found no FDR 0.05 genes for those selected targets in other
   neuronal groups either. `Stat1` was the only selected inflammatory
   comparator with any signal and had just one focal DEG.
5. I then checked sentinel NF-kappaB output genes in the focal Parquet. Under
   `Rel`, `Nfkb1`, `Chuk`, `Traf3`, `Map3k7`, `Tlr4`, and `Tnfrsf1a`
   perturbation, `Relb`, `Rela`, `Rel`, `Nfkb1`, `Nfkb2`, `Nfkbia`,
   `Tnfaip3`, `Birc3`, `Bcl2l1`, `Ccl2`, `Cxcl10`, `Il6`, `Tnf`, and `Sod2`
   all had `pvals_adj = 1` in the focal cell group. Some lowly detected
   cytokines had huge log-fold-change values from pseudocount behavior, but
   those rows were nonsignificant and I did not treat the magnitudes as
   biological effects.

The July PerturbAI corpus gave the same picture at the FDR 0.10 report level.
`Chuk:F001/F002/F003` report no robust downstream response and no NF-kappaB
feedback/inflammatory panel after `Chuk` loss, with `Nfkb1`, `Rel`, `Traf3`,
and `Tnfrsf1a` also flat. `Nfkb1:F001/F002/F003` report an all-neuronal
`Nfkb1` downstream null, flat represented NF-kappaB/TNF/TLR comparators, and
absence of canonical feedback, cytokine, chemokine, and survival-output genes.
`Rel:F001/F002` report that `Rel` had no robust downstream FDR 0.10 response
and no strong NF-kappaB neighbor. `Traf3:F001/F002/F004` report that `Traf3`
had no neuronal downstream response and did not induce interferon, NF-kappaB,
MAPK, oxidative-stress, or apoptosis sentinels.

## Target-specific prediction

### `Relb`

`Relb` encodes the RelB NF-kappaB transcription factor. Its most diagnostic
canonical setting is the noncanonical NF-kappaB pathway in which receptor
signals stabilize NIK, NIK activates IKKalpha/`Chuk`, and `Nfkb2` p100 is
processed to p52 so p52:RelB can enter the nucleus and regulate kappaB-site
genes. That wiring and its tight TRAF-cIAP/NIK control are established by the
NF-kappaB literature, especially Sun 2010 and Dejardin 2006; LTbetaR-dependent
IKKalpha/p52/RelB promoter use was shown by Bonizzi et al. 2004; Yilmaz et al.
2003 showed p52-RelB induction downstream of LTbetaR, NIK, and IKKalpha; and
Fusco et al. 2008 showed that p52:RelB has a distinct DNA-recognition mode.
Germline `Relb` phenotypes, including multiorgan inflammation and lymphoid
abnormalities with partial p50 compensation, are immune and stromal-system
phenotypes rather than evidence that postnatal thalamic glutamatergic neurons
require RelB tonically at baseline (Weih et al. 1997).

The same-experiment analogs point in the same direction:

- `Chuk` is the closest represented noncanonical activator and had 0 focal
  DEGs. It also failed to move the measured NF-kappaB feedback/output panel
  that included `Relb`, `Nfkb2`, `Nfkbia`, `Tnfaip3`, `Birc3`, cytokines, and
  chemokines.
- `Traf3` loss should release NIK and bias toward p52/RelB if the
  noncanonical machinery and receptors are engaged. It nevertheless had 0
  focal DEGs and no interferon, NF-kappaB, MAPK, stress, or apoptosis sentinel
  induction in the Parquet/corpus.
- `Rel` and `Nfkb1` test nearby nuclear NF-kappaB subunits; both had 0 focal
  DEGs and no significant focal movement of `Relb`, `Nfkb2`, `Nfkbia`,
  `Tnfaip3`, or the cytokine/chemokine sentinels.
- The available upstream receptor and adapter inputs, including `Cd40`,
  `Tnfrsf13c`, `Tnfrsf1a`, `Tlr2`, `Tlr3`, `Tlr4`, and `Map3k7`, were also
  zero at the endpoint in this focal class.

My compact causal model is: acute neuronal `Relb` CRISPR reduces RelB function;
loss of RelB would change a transcriptome only if p52:RelB or another RelB
dimer were an active limiting transcriptional effector in these recovered
postnatal thalamic glutamatergic neurons; the upstream NIK/IKKalpha/TRAF3 and
TNFR/TLR checks show that the pathway is gated off or buffered under the basal
P16-to-P37/44 NeuN+ assay; therefore few or no RelB-dependent secondary
program genes should cross FDR 0.05. I therefore predict the held-out endpoint
at the local null value:

- `Relb`: predicted `n_degs = 0`.

## Limits and uncertainty

The strongest evidence is within-dataset but indirect: `Nfkb2`, `Map3k14`,
`Rela`, `Ikbkb`, `Ikbkg`, `Traf2`, and `Birc2/Birc3` were not represented as
perturbation targets in the training endpoint, so the exact p100/p52:RelB
complex could not be knocked down on both sides. The July corpus is an
interpretation of the same experiment as the Parquet, not independent
replication. External `Relb` literature is dominated by germline, immune,
lymphoid-stromal, and receptor-stimulated contexts, whereas this experiment is
unstimulated sparse CRISPR in juvenile postmitotic neurons. A small RelB
effect, a late injury-gated effect, an effect in absent glia or thymic/immune
cells, or a survival effect lost before nuclei recovery would not be visible as
a focal DEG count here. The point estimate is therefore a calibrated assay
prediction that the FDR-thresholded count remains zero, not a claim that RelB
has no biology in the CNS or in immune cells.
