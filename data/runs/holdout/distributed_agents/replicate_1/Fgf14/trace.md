# Fgf14 DEG-count prediction

## Question and endpoint

I interpreted the requested value as a point prediction for the number of genes,
including the perturbed gene itself when it passes the same test, with
`pvals_adj < 0.05` after Wilcoxon differential expression in the held-out
`Fgf14` contrast in `151 TH Prkcd Grin2c Glut` neurons. `Fgf14` was absent as a
training `gene_target`, so its own differential-expression vector and its
observed `n_degs` were not available. The focal endpoint is directly observed
for the non-held-out perturbations in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; those counts are therefore
the quantitative calibration. The full Parquet gives same-experiment
expression-pattern evidence for those training perturbations. External FGF/FHF
and NaV biology was used only to decide which represented perturbations were
valid analogs or counterexamples.

## Sources

- Declared endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
- Declared differential-expression table:
  `training differential-expression dataset`
- Declared held-out manifest:
  `single-target request for Fgf14`
- Internal same-experiment interpretation corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, using `corpus.findings`,
  `corpus.calibration`, and `corpus.report_evidence` records for `Fgf12`,
  `Fgf13`, `Scn2a`, `Scn8a`, and `Cacna1g`.
- External biological references: Mouse Genome Informatics for FHF mouse-gene
  annotations as packaged in the same-experiment corpus; Pablo and Pitt 2016,
  The Neuroscientist, doi:10.1177/1073858414562217, PMID:25492945; Goldfarb
  et al. 2007, Neuron, doi:10.1016/j.neuron.2007.07.006, PMID:17678857; Wang
  et al. 2002, Neuron, doi:10.1016/S0896-6273(02)00744-4, PMID:12123606; Lou
  et al. 2005, Journal of Physiology, doi:10.1113/jphysiol.2005.097220,
  PMID:16166153; Pablo et al. 2016, PNAS,
  doi:10.1073/pnas.1521194113, PMID:27044086.

The Parquet, endpoint CSV, and the same-experiment report corpus are different
representations of the same Perturb-seq experiment, not independent
replicates.

## Dataset calibration

The focal training set had 1,674 perturbations. Its endpoint was heavily
zero-inflated:

- 1,205/1,674 training perturbations had `n_degs = 0`;
- the median was 0 and the 75th percentile was 1;
- the 90th percentile was 2, the 95th percentile was 18, and only 17
  perturbations exceeded 436 DEGs;
- the strongest broad responses were spliceosome, chromatin, proteostasis, and
  trafficking targets such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, `Psmb4`, and
  `Ufc1`, not channel-accessory genes.

I used the full Parquet only for focal-cell rows from mechanistic analogs and
counterexamples, filtering to `group_name == "151 TH Prkcd Grin2c Glut"` and
counting genes with `pvals_adj < 0.05`. This checked which significant genes
underlay each analog's training count and inspected the leading subthreshold
score genes when the FDR count was zero. The relevant represented comparators
were:

| training perturbation | focal `n_degs` | significant focal genes and interpretation |
|---|---:|---|
| `Fgf12` | 0 | The nearest represented FHF paralog was an exact focal null; its top absolute-score genes all had `pvals_adj = 1`. In the internal corpus `Fgf12` was almost fully buffered across the atlas, with only a singleton `Nmnat2` result in `145 MH-LH TH Glut` at the looser FDR<0.10 threshold. |
| `Fgf13` | 2 | `Fgf13` itself was down (`logFC = -0.894`, adjusted p `4.39e-12`) and `Rell2` was down (`logFC = -0.374`, adjusted p `0.0398`). The same-experiment report found no robust FDR-level convergence between `Fgf13` and `Fgf12`, receptor-FGF genes, or represented NaV genes. |
| `Scn1a` | 1 | The only focal hit was the self transcript (`logFC = -1.075`, adjusted p `5.87e-38`). |
| `Scn1b` | 2 | The self transcript was the dominant hit (`logFC = -1.436`, adjusted p `7.36e-70`) plus `Jun` up (`logFC = 0.518`, adjusted p `0.0156`). |
| `Scn2a` | 1 | The only focal hit was the self transcript (`logFC = -0.401`, adjusted p `6.46e-06`). Internal comparison records reported only three FDR<0.10 downstream genes across 22 measured cell groups, none forming a broad shared NaV program. |
| `Scn3a` | 0 | No focal hit. |
| `Scn8a` | 1 | The only focal hit was the self transcript (`logFC = -0.458`, adjusted p `1.34e-05`). The internal report found Scn8a to be downstream-buffered across the screen despite visible self-RNA changes in several classes. |
| `Fgf1`, `Fgfr1`, `Fgfr2`, `Fgfr3`, `Fgfrl1` | 0 each | Receptor FGF signaling controls were focal nulls; this fits FGF14 being an intracellular FHF rather than a secreted FGFR ligand. |
| `Cacna1g` | 12 | This was a counterexample showing that the focal thalamic class can mount a narrow channel-linked transcriptional response. Its response was not copied by FHF/NaV genes and therefore supported detectability, not promotion of `Fgf14` to a 10-plus DEG call. |
| `Cacna1a`, `Kcna1`, `Kcnc1`, `Kcnd3` | 0 each | Other excitability genes were focal nulls or self-only neighbors; broad channel membership alone was not predictive. |

These comparisons made a high DEG count for `Fgf14` unlikely. The closest
single-gene FHF analog, `Fgf13`, reached two focal DEGs because the assayed
target RNA itself crossed FDR and only one other transcript, `Rell2`, followed.
`Fgf12` was still quieter, and the represented sodium-channel subunits that
FGF14 binds or functionally regulates were zero, self-only, or self-plus-one in
the focal class.

## Biological transfer to Fgf14

FGF14 is FHF4, one of the intracellular FGF11-FGF14 proteins. Unlike canonical
secreted FGFs, FHFs do not primarily signal through FGFR tyrosine kinases; they
bind intracellular domains of voltage-gated sodium channels and control channel
gating, axonal localization, and excitability (Pablo and Pitt 2016;
Goldfarb et al. 2007). FGF14 has especially direct NaV biology: FGF14 protein
interacts with multiple NaV alpha subunits and localizes with endogenous NaV
channels at the axon initial segment in differentiated neurons (Lou et al.
2005), and FGF13 and FGF14 have complementary actions on polarized NaV
localization in hippocampal neurons (Pablo et al. 2016). Whole-animal loss of
`Fgf14` causes ataxia and paroxysmal dyskinesia in mice while leaving mice
viable, fertile, and grossly anatomically normal (Wang et al. 2002), consistent
with a neuronal signaling and axonal function rather than an obligatory broad
transcriptional viability program.

The experiment assayed a sparse, acute postnatal CRISPR loss of function in
neurons that survived to nuclear profiling. In that causal chain, `Fgf14`
editing should impair an intracellular FHF protein, propagate mostly through
NaV channel localization/gating and firing or synaptic physiology, and only
then potentially alter nuclear RNA abundance. The training perturbations show
that this transfer attenuates strongly at the electrophysiology-to-nuclear-RNA
step: direct FHF and NaV losses were not large DEG producers in the same focal
thalamic class. `Cacna1g` demonstrates that the class was capable of recording
a thalamic channel perturbation, but Cav3.1 is a different limiting channel
with a small 12-gene state, so it is not a close count template for FGF14.

I therefore treated `Fgf14` as a near-null endpoint. I predicted one DEG rather
than zero because FGF14 is a neuronal FHF with thalamic expression in public
mouse-brain atlases and because the best focal analog, `Fgf13`, as well as
`Scn1a`, `Scn2a`, and `Scn8a`, often crossed the focal FDR threshold only for
their own targeted transcript. I did not extrapolate to the `Fgf13` downstream
`Rell2` hit, to the `Scn1b` `Jun` hit, or to the `Cacna1g` Ptprn/Stmn4/Cpne7
signature, because the same-experiment comparator records showed that these
were target-specific singleton or narrow thalamic states rather than a generic
FHF-NaV transcriptional module.

## Point prediction

The final point prediction for `Fgf14` is `1` DEG.

## Limits

This is an extrapolation: no `Fgf14` perturbation signature was present in the
declared inputs. The most relevant measured relatives were `Fgf12`, `Fgf13`,
and NaV-channel genes, but FGF14 is not redundant with any single one of them,
and FGF14 protein can have cell-type- and isoform-specific effects that a
thalamic snRNA-seq DEG count may miss. The endpoint also counts the target
transcript when it passes FDR, so the prediction is sensitive to baseline
`Fgf14` expression and nonsense-mediated decay in this focal class, quantities
not directly given in the DE summary. Finally, electrophysiological impairment
or altered axon-initial-segment localization can be real without a persistent
FDR-significant nuclear RNA response in recovered postnatal neurons.
