# DEG-count prediction for Apc

## Question and endpoint

The held-out target file contains one requested perturbation, `Apc`, and the required endpoint is the integer number of genes in `151 TH Prkcd Grin2c Glut` cells with Wilcoxon Benjamini-Hochberg adjusted `pvals_adj < 0.05` after acute AAV CRISPR loss of the target. I treated this as a prediction of response breadth in the same assay, not as a prediction of viability, editing efficiency, or biological importance. `151 TH Prkcd Grin2c Glut` was used as the exact focal cell group; `TH` was interpreted as thalamus in the Allen-style cell label, not as tyrosine hydroxylase.

`Apc` is absent from both supplied training inputs, so its count and expression vector are absent from the declared differential-expression matrix. The requested endpoint is directly observed for the 1,674 non-held-out perturbations in `151 TH Prkcd Grin2c Glut`; it is absent for `Apc`. I therefore used the training DEG counts and non-held-out expression signatures as same-experiment evidence and used external APC/Wnt knowledge only to decide which training perturbations were mechanistically transferable.

## Sources used

- Declared training endpoint: `/gpfs/group/jin/asun/bioagents/debug/260901_predict/holdout_task/Inputs/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression matrix: `/gpfs/group/jin/asun/bioagents/debug/260901_predict/holdout_task/Inputs/training_de_all_cell_groups.parquet`.
- Cached declared-Parquet feature summary: `dataset.perturbseq_features summarize` wrote `evidence/features.parquet`, aggregating all 616,253,184 declared rows into 1,674 non-held-out target rows. This was used to confirm the training universe and broad Wnt/catenin response burden across all measured cell groups. A nested `calibrate` run was attempted but is not applicable here because this task supplies an unranked one-column holdout manifest rather than ranked or partially ranked supervision.
- Internal same-experiment corpus: PerturbAI July 260713 sourceguard-1773 v1 Findings/Evidence/References for non-held-out `Ctnnb1`, `Tcf7l2`, and `Gsk3b`. These are interpretations of the same Perturb-seq experiment, not independent replication.
- External literature from PubMed:
  - Stamos and Weis 2013, "The beta-catenin destruction complex", Cold Spring Harbor Perspectives in Biology, DOI 10.1101/cshperspect.a007898, PMID 23169527.
  - Cadigan and Waterman 2012, "TCF/LEFs and Wnt signaling in the nucleus", Cold Spring Harbor Perspectives in Biology, DOI 10.1101/cshperspect.a007906, PMID 23024173.
  - Mohn et al. 2014, "Adenomatous polyposis coli protein deletion leads to cognitive and autism-like disabilities", Molecular Psychiatry, DOI 10.1038/mp.2014.61, PMID 24934177.
  - Pirone et al. 2016, "APC conditional knock-out mouse is a model of infantile spasms with elevated neuronal beta-catenin levels, neonatal spasms, and chronic seizures", Neurobiology of Disease, DOI 10.1016/j.nbd.2016.11.002, PMID 27852007.
  - Lipiec et al. 2020, "TCF7L2 regulates postmitotic differentiation programmes and excitability patterns in the thalamus", Development, DOI 10.1242/dev.190181.

## Quantitative checks over the supplied training data

The focal training endpoint is very sparse. Among 1,674 non-held-out perturbations, 1,205 have zero genes at FDR<0.05, the median count is 0, the 75th percentile is 1, the 90th percentile is 2, the 95th percentile is 18, and only 1% exceed about 436 DEGs. A nonzero prediction for `Apc` therefore requires a close pathway reason; it should not be assigned just because APC is disease-associated or Wnt-related.

I scanned the declared Parquet for `151 TH Prkcd Grin2c Glut` rows of Wnt/catenin training analogs and counted `pvals_adj < 0.05`. The focal counts from the Parquet slice agreed with the training CSV:

| training perturbation | 151 FDR<0.05 genes | 151 FDR<0.10 genes | interpretation for Apc |
|---|---:|---:|---|
| `Ctnnb1` | 383 | 477 | beta-catenin is the direct destruction-complex substrate and nuclear Wnt coactivator; loss moves canonical Wnt/TCF targets opposite to expected APC loss, but gives the best estimate of the size of the thalamic beta-catenin-responsive regulon. |
| `Tcf7l2` | 106 | 140 | downstream TCF/LEF effector expressed in thalamus; it shares a signed 151 program with `Ctnnb1` and bounds a narrower transcription-factor arm. |
| `Csnk2b` | 25 | 42 | Wnt-intersecting kinase-subunit perturbation with only a modest 151 response, arguing that generic Wnt/catenin annotation is not enough. |
| `Gsk3b` | 6 | 9 | a destruction-complex kinase, but isolated `Gsk3b` loss is buffered away from broad beta-catenin activation, likely because GSK3A/GSK3B are partially redundant and GSK3B has beta-catenin-independent branches. |
| `Lrp6` | 4 | 6 | upstream Wnt co-receptor loss touches the Ctnnb1 state weakly but is small, consistent with receptor redundancy and with APC acting downstream of receptors. |
| `Lrp5`, `Fzd2`, `Fzd4`, `Fzd6`, `Fzd9`, `Ctnna2`, `Ctnna3`, `Ctnnd2` | 0-1 in the focal slice | 0-1 | counterexamples showing that paralogy or broad pathway membership does not phenocopy Ctnnb1 in this assay. |

At FDR<0.05, `Ctnnb1` and `Tcf7l2` shared 44 genes in the 151 cell group, 40 with the same log-fold-change sign. The strongest shared genes included `Ramp3`, `Spock3`, `Kcnc2`, `Pcsk2`, `Plekhg1`, `Pcp4`, `Cpe`, `Grin2b`, `Prkcd`, `Lef1`, and `Spon1`. The Ctnnb1 same-experiment report also records canonical Wnt-feedback changes in 151 after beta-catenin loss: `Lef1`, `Vangl1`, `Axin2`, `Notum`, and `Wnt9b` were down, while `Fzd8` and `Wnt3` were up. The Tcf7l2 report records 59 FDR<0.10 genes shared with `Ctnnb1`, 53 same-direction, and places the overlap in thalamic excitability and synaptic genes.

## Causal transfer to Apc

The compact causal model I used was:

`Apc` CRISPR loss -> impaired APC scaffold function in the beta-catenin destruction complex -> reduced beta-catenin degradation and increased beta-catenin/TCF transcription, plus APC cytoskeletal/synaptic roles -> remodeling of thalamic terminal, Wnt-feedback, adhesion, calcium, and excitability transcripts in edited recovered neurons -> a survivor-conditioned `151 TH Prkcd Grin2c Glut` single-nucleus signature -> measured FDR<0.05 DEG count.

APC is a negative regulator upstream of beta-catenin degradation. Stamos and Weis summarize APC as a core scaffold in the AXIN/APC/GSK3/CK1 destruction complex that phosphorylates beta-catenin and promotes beta-TrCP-mediated proteasomal degradation. Cadigan and Waterman summarize beta-catenin as the Wnt-dependent activating cofactor for TCF/LEF nuclear factors. Therefore APC loss should not be same-direction to `Ctnnb1` loss: `Ctnnb1` knockout removed beta-catenin and lowered `Axin2`/`Lef1`, whereas `Apc` loss should stabilize beta-catenin and tend to activate that feedback arm. Direction is opposite for canonical targets, but the endpoint requested here is unsigned DEG burden, so an opposite Wnt-feedback response can still produce many FDR-significant genes.

The transfer is stronger for `Apc` than for `Gsk3b`, `Lrp6`, or single `Fzd` perturbations. A single Wnt receptor does not bypass ligand/receptor redundancy, and `Gsk3b` has a near-null count in 151 despite being annotated to the destruction complex, consistent with buffering by other GSK3 isoforms. APC sits in the same limiting destruction complex but is a nonredundant beta-catenin regulator in many systems; in forebrain-neuron conditional mouse knockouts, APC deletion elevates beta-catenin and changes canonical Wnt target expression and N-cadherin synaptic adhesion complexes (Mohn et al. 2014), and another neuronal APC conditional knockout elevates beta-catenin and increases excitatory synaptic drive with seizures (Pirone et al. 2016). Those phenotypes establish that APC loss can be endpoint-bearing in neurons, but they do not set the exact DEG count because they are germline/Cre conditional models in cortical/hippocampal neurons rather than a sparse P16 whole-brain AAV CRISPR screen in thalamic glutamatergic neurons.

The expected `Apc` breadth should be below `Ctnnb1`'s 383 DEGs. `Ctnnb1` encodes the central Wnt coactivator and an adherens-junction catenin, so its loss combines canonical Wnt suppression with adhesion consequences. APC loss should activate beta-catenin rather than deplete the junctional beta-catenin protein itself, and the screen's modest mosaic CRISPR dosage can under-shoot the complete APC deletions in the external literature. The expected count should also be above `Gsk3b`/`Lrp6`: the focal Ctnnb1/Tcf7l2 module is visibly active in thalamic cells, and APC acts downstream of the receptors that were redundant in the screen. I therefore predicted a moderate-to-broad response near the observed `Tcf7l2` count rather than near the all-training median or the full `Ctnnb1` count.

## Target prediction

- `Apc`: predicted 120 FDR<0.05 genes. The prediction is driven mainly by within-dataset `Ctnnb1` at 383 and `Tcf7l2` at 106 in the same focal cell group, with the 44-gene same-direction FDR<0.05 overlap showing a real beta-catenin/TCF thalamic module. External APC literature changes the causal sign: APC loss should stabilize beta-catenin, so it should perturb an overlapping module in the opposite canonical direction from `Ctnnb1`/`Tcf7l2` loss. The small `Gsk3b`, `Lrp6`, and Frizzled counts pull the estimate down because not every Wnt component is limiting under sparse postnatal neuronal CRISPR. The final value is a point prediction slightly above `Tcf7l2` and well below `Ctnnb1`, reflecting a direct destruction-complex perturbation with partial assay attenuation.

## Limits

There is no directly observed `Apc` signature in the declared inputs. The best within-dataset evidence is from `Ctnnb1` and `Tcf7l2`, which report the amount of Wnt/TCF circuitry detectable in the 151 class, not APC itself. APC loss has the opposite beta-catenin sign from `Ctnnb1` loss and may induce feedback or survival effects that are asymmetric with beta-catenin depletion. No non-held-out perturbation tested the AXIN/APC scaffold itself, and single `Gsk3b` or receptor knockouts are mechanistically informative counterexamples rather than quantitative APC phenocopies. External APC conditional-knockout papers used different brain regions, developmental windows, and stronger Cre-mediated deletion, so they support neuronal relevance but not this exact FDR count.
