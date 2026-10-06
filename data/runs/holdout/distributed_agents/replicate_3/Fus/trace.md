# Prediction trace

## Question and resolved ambiguities

The held-out target list for this run contains one perturbation, `Fus`. I interpreted the task as a point prediction of the number of measured genes with `pvals_adj < 0.05` in the focal `151 TH Prkcd Grin2c Glut` cell group after acute AAV CRISPR loss of the mouse gene `Fus`.

`Fus` was absent from the supplied training DEG-count CSV and as a `gene_target` in the differential-expression parquet, so there is no `Fus` expression signature to correlate directly. I therefore used the focal-cell DEG counts and focal-cell DE vectors of mechanistically related non-held-out perturbations to set the scale, and used external knowledge of FUS as a FET-family RNA/DNA-binding protein to choose which observed perturbations were fair analogs.

## Sources used

Internal same-experiment sources:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`: exact training `n_degs` values in the focal cell group.
- `[local file: training_de_all_cell_groups.parquet]`: per-gene Wilcoxon statistics used to inspect focal-cell significant genes and selected RBP/spliceosome pairwise expression-pattern overlap.
- Distributed Agents runtime profile comparison, run-local artifact `fus_rbp_profile_compare.json`: pairwise focal-cell comparisons for a cohort of observed RNA-binding and splicing perturbations.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`: structured findings for `Tardbp`, `Matr3`, `Hnrnpa2b1`, and related RBP/splicing comparators. The corpus had no `Fus` entry in this release, so it was used only for non-held-out analogs and boundaries.

External biological sources:

- Lagier-Tourenne et al. 2012, Nature Neuroscience, DOI `10.1038/nn.3230`, PMID `23023293`: FUS/TLS binds >5,500 RNAs in mouse and human brain, depletion of FUS/TLS in adult nervous system altered abundance or splicing of >950 mRNAs, and FUS and TDP-43 showed both divergent regulation and a small shared class of long neuronal mRNAs.
- Rogelj et al. 2012, Scientific Reports, DOI `10.1038/srep00603`, PMID `22934129`: iCLIP in mouse brain showed broad FUS binding along nascent RNAs and a role for FUS in alternative splicing.
- Honda et al. 2013, FEBS Open Bio, DOI `10.1016/j.fob.2013.11.001`, PMID `24319651`: primary cortical-neuron loss-of-function data found partial overlap between TDP-43- and FUS-regulated gene-expression and splicing outputs.
- Blechingberg et al. 2012, PLOS ONE, DOI `10.1371/journal.pone.0046251`, PMID `23049996`: RNAi comparisons of the FET paralogs found FUS- and TAF15-reduction expression responses to be more similar than EWS/EWSR1 reduction, but also supported nonredundant FET-family functions.
- Schwartz, Cech & Parker 2014, Annual Review of Biochemistry, DOI `10.1146/annurev-biochem-060614-034325`, PMID `25494299`: FUS, EWSR1, and TAF15 are the FET RNA-binding proteins and act in transcription, RNA processing, mRNA fate, and DNA-related regulation.

## Computations over the training data

I first read the exact focal-cell count CSV and searched for mechanistic analogs. The focal endpoint is sparse: 1,205 of 1,674 training perturbations are exact zeros, 363 are 1-9 DEGs, 63 are 10-99, and only 43 are >=100.

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for a hand-built RBP/splicing cohort and retained rows with `pvals_adj < 0.05`. This recovered exact per-analog focal signatures without touching held-out `Fus`. The main focal-cell counts were:

| training target | focal `n_degs` | relevance |
|---|---:|---|
| `Rnpc3` | 868 | minor spliceosome component; positive bound for disabling a core splicing apparatus |
| `U2af2` | 828 | spliceosome factor; positive bound |
| `Hnrnpu` | 733 | broad hnRNP/nuclear RBP response |
| `Prpf6` | 454 | spliceosome factor; positive bound |
| `Snrnp70` | 213 | spliceosomal snRNP factor; positive bound |
| `Tardbp` | 210 | closest observed ALS-linked nuclear RBP |
| `Matr3` | 149 | ALS-linked nuclear DNA/RNA-binding protein |
| `Hnrnpc` | 122 | hnRNP comparator |
| `Hnrnpa2b1` | 11 | ALS/MSP-linked hnRNP with a weak focal response |
| `Atxn2` | 8 | ALS modifier/stress-granule RNA regulator; weak |
| `Ddx3x` | 8 | RNA helicase; weak |
| `Hnrnph2` | 4 | hnRNP; weak |
| `Hnrnpdl` | 1 | hnRNP; essentially flat |
| `Ddx39b`, `Fmr1`, `Msi1`, `Rbm28`, `Taf1b`, `Tia1` | 0 | RBP/stress-granule counterexamples |

For the same focal group I compared the signed `logfoldchanges` vectors of these genes with `mcp__distributed_agents_runtime.profile_compare`, using `pvals_adj < 0.05` only to count significant-program overlaps. I treated the FDR-level intersections as the useful part of the comparison, because the full ranked vectors can share extreme pseudocount-driven tails among otherwise flat profiles.

The profile comparison emphasized three things.

1. `Tardbp` is a real focal-cell RBP response, not a generic broad-spliceosome failure: it had 131 positive and 79 negative significant genes. In the significant rows, `Tardbp` itself was down (`log2FC = -1.414`, `q = 1.6e-39`), `Uggt2` was strongly up (`+1.359`, `q = 7.4e-32`), `Snrnp70` was down (`-0.587`, `q = 5.1e-20`), and `Fus` itself was down (`-0.379`, `q = 9.5e-06`).
2. `Tardbp` and `Matr3` were only partial analogs. In `151 TH Prkcd Grin2c Glut`, `Tardbp` shared 6 positive and 2 negative FDR genes with `Matr3`, versus 210 and 149 total genes respectively. This matches the Distributed Agents corpus finding that `Matr3` and `Tardbp` share only a weak part of a proteostasis/RBP state rather than being interchangeable ALS-gene phenocopies.
3. ALS/RBP membership alone is not enough. `Hnrnpa2b1` had only 11 focal DEGs, `Atxn2` 8, and `Tia1` 0, and the corpus explicitly reports that these were flat or divergent relative to `Tardbp`/`Matr3` at FDR level. Conversely, core spliceosome perturbations such as `Rnpc3`, `U2af2`, `Prpf6`, and `Snrnp70` were much broader than an auxiliary RBP should be expected to be.

Direct FET-family paralogs would have been the best internal controls, but `Ewsr1` and `Taf15` were not present in the training count CSV for this split. That absence is important: the prediction is extrapolated from TDP-43/Matrin3/hnRNP/spliceosome behavior, not from a measured FUS paralog.

## Target-specific reasoning

### `Fus`

Within-dataset evidence for a nonzero response:

- The closest measured disease/mechanism analog, `Tardbp`, was a strong focal responder with 210 DEGs. Its same-experiment corpus report described a compact RNA-processing response, repeated `Snrnp70` down-regulation, alteration of `Fus`, `Hnrnpm`, `Srsf`-family factors, `Prpf39`, `Tcerg1`, `Drosha`, and `Rbmx`, and same-direction links to `U2af2`, `Prpf6`, and `Cdk13`.
- `Matr3`, another nuclear ALS-linked RNA/DNA-binding protein, had 149 focal DEGs. Its recurrent `Rsrp1` down / `Uggt2` up / ER-quality-control state argues that the assay can detect nuclear RBP perturbations outside the core spliceosome.
- `Hnrnpc` and `Hnrnpu` had 122 and 733 focal DEGs, respectively. They are not FUS paralogs, but their large counts reject a generic claim that postnatal neuronal snRNA-seq cannot see broad hnRNP/RBP loss-of-function states.
- The strongest `Tardbp` signature significantly repressed endogenous `Fus` mRNA in the same focal group. I did not use that as a quantitative surrogate for FUS loss, but it places `Fus` within the measured RNP compensation program.

External evidence for a nonzero response:

- FUS is a nuclear FET protein that binds nascent pre-mRNAs and regulates splicing in the brain; ASO depletion of FUS/TLS in the adult nervous system changed the abundance or splicing of more than 950 mRNAs (Lagier-Tourenne et al. 2012; Rogelj et al. 2012).
- FUS and TDP-43 are functionally related ALS/FTD RBPs, and primary cortical neurons showed >25% overlap in differential-expression outputs after TDP-43 versus FUS perturbation (Honda et al. 2013).

Counterevidence limiting the count:

- FUS is not a core spliceosome component. Training perturbations that directly crippled spliceosomal machinery reached 454-868 focal DEGs, and I treated that as an upper bound rather than as the scale for `Fus`.
- The `Tardbp` same-experiment corpus separated `Tardbp` from `Matr3`, `Hnrnpa2b1`, `Atxn2`, and `Tia1`: those disease/RBP comparators shared little or no FDR-level signal. The focal counts reproduce that boundary: 149, 11, 8, and 0 DEGs. So FUS being ALS-linked and stress-granule-capable should not automatically make it `Tardbp`-like.
- FET paralogs have partly redundant and partly nonredundant functions. FUS and TAF15 knockdown are more similar to each other than to EWSR1 knockdown in cell lines, but the absent `Taf15` and `Ewsr1` training perturbations make the family-specific scale uncertain.
- This assay measures whole-gene nuclear abundance after sparse acute editing. FUS biology is rich in exon choice, long-intron processing, RNA localization, and cytoplasmic mRNA fate, much of which would not appear as a whole-gene Wilcoxon DEG.

I therefore predicted a medium, clearly nonzero `Fus` response: lower than `Tardbp` and `Matr3`, higher than `Hnrnpa2b1`/`Atxn2`, and far below the `Rnpc3`/`U2af2`/`Hnrnpu` broad-response tier. My point estimate was `64` DEGs.

## Limits

The weakest point is the missing direct FET-family calibration: neither `Taf15` nor `Ewsr1` was in the training endpoint, and the Distributed Agents same-experiment corpus had no released `Fus` finding. The profile comparison among observed RBPs is therefore a scale-setting exercise, not a claim that `Tardbp` or `Matr3` is a FUS phenocopy. Whole-gene snRNA-seq will also miss cryptic exons and many FUS-dependent splice changes, so a biologically real FUS response could land below the FDR threshold, especially with sparse AAV editing and surviving, class-assigned nuclei only. Conversely, if FUS loss in thalamic glutamatergic neurons causes a secondary stress state, the actual count could approach the `Tardbp`/`Matr3` range.
