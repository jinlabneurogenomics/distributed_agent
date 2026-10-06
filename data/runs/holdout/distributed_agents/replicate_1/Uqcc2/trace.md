# Uqcc2 DEG-count prediction

## Question and endpoint

The requested held-out perturbation was `Uqcc2`. I interpreted the endpoint as
the exact `151 TH Prkcd Grin2c Glut` DEG count that would have been produced by
the same Scanpy Wilcoxon test used in the training table: the number of measured
genes, including the perturbed transcript itself if it passes correction, with
`pvals_adj < 0.05` in perturbed versus matched control nuclei.

The held-out `Uqcc2` readout and its expression signature are absent from both
inputs, so the endpoint is not directly observed for the target. The endpoint is
directly observed for the training perturbations in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, and the parquet provides the
gene-level focal signatures used to distinguish a one-gene self-transcript
effect from a broad downstream response.

## Sources used

- Declared training DEG counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This table has 1,674 non-held-out perturbations; 1,205 have `n_degs = 0`, the
  median is 0, the 75th percentile is 1, and the 95th percentile is 18.
- Declared differential-expression parquet:
  `training differential-expression dataset`.
  I filtered it to `group_name == "151 TH Prkcd Grin2c Glut"` and to complex
  III, respiratory-chain, and mitochondrial-stress comparators to inspect which
  measured genes reached FDR in the focal cell group.
- Internal same-experiment interpretation corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, queried through the Findings
  ledger for `Cyc1`, `Ttc19`, `Uqcrc2`, `Uqcrb`, `Uqcrfs1`, `Uqcrh`, `Uqcrq`,
  and `Opa1`. This is a curated representation of the same Perturb-seq
  experiment, not independent replication.
- External biological literature, used only to place the training analogs on the
  complex III assembly pathway:
  Tucker et al. 2013, PLoS Genetics, DOI 10.1371/journal.pgen.1004034, PMID
  24385928; Wanschers et al. 2014, Human Molecular Genetics, DOI
  10.1093/hmg/ddu357, PMID 25008109; Feichtinger et al. 2017, Oxidative
  Medicine and Cellular Longevity, DOI 10.1155/2017/7202589, PMID 28804536;
  Dennerlein et al. 2021, eLife, DOI 10.7554/eLife.68213, PMID 34969438; Liang
  et al. 2022, Cell Reports, DOI 10.1016/j.celrep.2022.111204, PMID 35977508;
  Bottani et al. 2017, Molecular Cell, DOI 10.1016/j.molcel.2017.06.001, PMID
  28673544.

## Local quantitative calibration

`Uqcc2` was absent from the training count table. The nearest exact assembly
factors were not available either: `Uqcc1`, `Uqcc3`, and `Bcs1l` were absent
from the focal training-count CSV. I therefore used the complex III structural
subunits and the later complex III maturation factor `Ttc19` that were measured
in the training set.

| training target | role relative to Uqcc2 | focal observed `n_degs` | focal FDR<0.05 genes |
| --- | --- | ---: | --- |
| `Cyc1` | nuclear structural subunit of complex III | 1 | `Cyc1` self-transcript only |
| `Ttc19` | complex III maturation/turnover factor acting after `Uqcrfs1` incorporation | 1 | `Ttc19` self-transcript only |
| `Uqcrc2` | complex III core subunit | 1 | `Uqcrc2` self-transcript only |
| `Uqcrq` | complex III structural subunit | 1 | `Gpr180`, a singleton private downstream hit |
| `Uqcrb` | complex III structural subunit | 0 | none |
| `Uqcrfs1` | Rieske iron-sulfur complex III subunit | 0 | none; even the self transcript had focal `pvals_adj = 0.199` |
| `Uqcrh` | complex III structural subunit | 0 | none |

These seven same-complex perturbations had counts `[1, 1, 1, 1, 0, 0, 0]`,
with no recurrent downstream gene set in the focal class. I also inspected
several respiratory-chain and mitochondrial positive or boundary controls:
`Cox5a`, `Ndufa10`, and `Sdha` each had one DEG in the focal class, all their
own transcripts, whereas the broader mitochondrial-dynamics perturbation `Opa1`
had 37 DEGs and the upstream respiratory regulator `Nrf1` had 138. Thus this
cell group and test can detect a mitochondrial stress or respiratory-axis
program when a perturbation crosses the transcriptional threshold, but partial
complex III subunit loss usually did not.

The same-experiment Findings corpus was concordant with the parquet summaries.
It reported that `Uqcrc2` produced no robust downstream single-gene DE in any
measured neuronal group and lacked canonical ATF4/ISR, UPRmt-like, redox, or
mitophagy transcriptional sentinels; `Uqcrfs1` and `Uqcrh` likewise lacked
detectable mitochondrial-stress programs; `Uqcrq`, `Uqcrb`, `Cyc1`, and
`Ttc19` had only private singleton hits or self hits. The corpus explicitly
contrasted those nearly flat complex III surfaces with the `Opa1` ATF4/ISR-like
response, supporting the interpretation that the complex III null or one-gene
pattern was not a generic assay failure.

## Biological transfer to Uqcc2

External complex III assembly work places UQCC2 in the earliest cytochrome-b
biogenesis machinery. Tucker et al. showed that UQCC2 interacts with UQCC1 and
that UQCC2-mutant fibroblasts have defective synthesis or stability of the
mitochondrial DNA-encoded cytochrome b subunit. Wanschers et al. placed UQCC3
downstream of UQCC1/UQCC2 in the same assembly path. Dennerlein et al. and
Liang et al. subsequently described UQCC1/2-containing early complex III
biogenesis modules that coordinate nascent cytochrome-b translation and
stabilization. Feichtinger et al. showed that human UQCC2 deficiency can present
as severe neonatal disease with combined complex I and III defects, consistent
with loss of assembled complex III destabilizing respiratory supercomplexes.

The causal transfer chain for this experiment is:

`Uqcc2` CRISPR loss of function -> weaker early cytochrome-b biogenesis and
complex III assembly -> possible defects in CIII/respirasome activity -> either
buffering below the ATF4/ISR threshold in 3-4 week postmitotic mosaic neurons or
survivor-conditioned loss of the most damaged cells -> FDR-level nuclear RNA
hits counted in recovered `151 TH Prkcd Grin2c Glut` nuclei.

The same molecular lesion is upstream of the represented structural subunits, so
the prior is same-direction for CIII impairment. It is not a same-sign prior for
the isolated `Gpr180`, `Cfl1`, `Map7`, or `Gnb1` singleton readouts, because
those were private to individual structural subunits and not a shared complex
III program. It is also not enough to transfer the large `Opa1` count: `Opa1`
loss perturbs inner-membrane fusion/cristae organization and triggered a
detectable ATF4-like ISR in this dataset, whereas the CIII subunit and `Ttc19`
perturbations did not. Therefore the endpoint-bearing same-experiment evidence
points to a nearly flat CIII response, with at most a self-transcript or private
singleton DEG, rather than to tens or hundreds of DEGs.

## Prediction

I predict `Uqcc2` will be nonzero but only barely:

- The nonzero side is supported by the median of the exact complex III/Ttc19
  analogs being one focal DEG, usually the perturbed transcript itself.
- I do not predict a larger downstream response because six represented
  structural complex III relatives and `Ttc19` failed to produce a recurrent
  mitochondrial ISR, UPRmt-like, OXPHOS-compensatory, or redox program in this
  experiment.
- The chosen point, 1, should be read as "one isolated FDR hit at most" rather
  than evidence that cytochrome-b assembly necessarily produces a downstream
  thalamic transcriptional state in recovered nuclei.

## Limits

The closest UQCC assembly factors, `Uqcc1` and `Uqcc3`, and the Rieske-loading
factor `Bcs1l` were not in the visible training table, so the transfer uses
structural CIII genes and `Ttc19` as imperfect analogs. The parquet does not
measure indels, UQCC2 protein, cytochrome-b abundance, oxygen consumption,
complex III activity, ROS, ATP, cell survival before FACS, or guide-exposure
denominators. A severe biallelic `Uqcc2` disease state in fibroblasts or
neonates can therefore be real while a sparse P16 neuronal CRISPR perturbation
remains transcriptionally quiet in surviving nuclei. The exact distinction
between 0 and 1 DEG is particularly uncertain because in several analogs the
sole focal DEG was the target transcript, and target-RNA loss is not a stable
quantitative readout of editing efficiency or downstream impact.
