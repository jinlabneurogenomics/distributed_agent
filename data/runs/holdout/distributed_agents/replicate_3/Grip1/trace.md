# Grip1 DEG-count prediction

## Question and resolved ambiguity

The requested readout is the number of measured genes with `pvals_adj < 0.05` in the held-out `Grip1` perturbation in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons. The target list in `[local file: 100_Grip1.csv]` contains exactly one target, in this order:

| target_name |
|---|
| Grip1 |

I treated the count as including any significant self-transcript row, because the training endpoint in `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]` counts all FDR-significant measured genes. I did not treat weak or absent self-RNA changes as failed editing: the experiment is an indel-based, sparse, postnatal CRISPR assay in recovered nuclei, and the task asks for the assay-visible FDR burden rather than editing or protein abundance.

## Sources used

- The supplied training count CSV for exact `151 TH Prkcd Grin2c Glut` DEG counts of 1,674 non-held-out perturbations.
- The supplied differential-expression parquet, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` and to GRIP1/AMPAR/PSD-relevant observed perturbations. These rows provided the actual FDR calls, Wilcoxon score profiles, signed log2 fold changes, and matched nucleus counts for each training analog.
- The Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, especially target contexts for `Gria2`, `Cacng2`, `Dlg4`, and `Atad1` and the claims:
  - `claim:a9367c3aeaad95bfae9c`: represented AMPAR-core and AMPAR-trafficking/scaffold perturbations are buffered in basal juvenile neurons.
  - `claim:60396794c5493932dc07`: represented PSD scaffold and synaptic-adhesion perturbations generally do not induce a shared steady-state neuronal RNA module in this P16 screen.
- A run-local profile comparison, `grip1_ampapath_profile_compare.json`, over observed focal-class score vectors for 15 nominated AMPAR/PSD/GRIP1-neighborhood nodes.
- External mechanism literature from PubMed:
  - Wyszynski et al. 1999, DOI `10.1523/JNEUROSCI.19-15-06528.1999`, PMID `10414981`: GRIP1/GRIP2 associate with GluR2/3-containing AMPARs in brain.
  - Setou et al. 2002, DOI `10.1038/nature743`, PMID `11986669`: GRIP1 binds kinesin heavy chains and can steer AMPAR transport to dendrites.
  - Steiner et al. 2005, DOI `10.1038/sj.emboj.7600755`, PMID `16037816`: NEEP21-GRIP1-GluR2 interactions regulate GluR2-containing AMPAR sorting and recycling.
  - Guo and Wang 2007, DOI `10.1016/j.neuroscience.2006.11.042`, PMID `17207582`: glutamate can induce NMDAR/Ca2+-dependent proteasomal degradation of GRIP1 and change surface GluR2.
  - Takamiya et al. 2008, DOI `10.1523/JNEUROSCI.0654-08.2008`, PMID `18509036`: GRIP1 and GRIP2 are partly redundant and the family is required for cerebellar LTD expression.
  - Piard et al. 2018, DOI `10.1093/brain/awx377`, PMID `29390050`: ATAD1/Thorase participates in postsynaptic AMPAR trafficking by disassembling GluA2-GRIP1 complexes.

## Computation over the supplied dataset

I first summarized the training count CSV to calibrate how zero-inflated the endpoint is in this focal class:

- `1674` training perturbations.
- `1205` have `n_degs == 0`.
- Median `n_degs` is `0`; 75th percentile is `1`; 90th percentile is `2`.
- The large right tail is dominated by chromatin, splicing, proteasome, RNA-binding, and proteostasis perturbations such as `Uba5 = 2677`, `Tpr = 1768`, `Sin3a = 1433`, and `Rnpc3 = 868`.

I then filtered the parquet to the focal cell group and a hand-selected GRIP1-relevant cohort. This yielded 17,259 measured genes per target and 23,679 matched controls. Key exact focal-class counts were:

| class | training perturbation | focal `n_degs` | expression-pattern evidence |
|---|---:|---:|---|
| AMPAR core | `Gria1` | 0 | no FDR 0.05 rows; strongest row `Map4k4` had `p_adj = 0.246` |
| AMPAR core, GluA2 | `Gria2` | 0 | no FDR 0.05 or FDR 0.10 rows; all top nominal rows had `p_adj = 1.0` |
| AMPAR core, GluA3 | `Gria3` | 0 | no FDR 0.05 or FDR 0.10 rows; `Gria3` self-row had `p_adj = 0.971` |
| TARP/AMPAR auxiliary | `Cacng2` | 0 | no FDR 0.05 or FDR 0.10 rows; all top nominal rows had `p_adj = 1.0` |
| TARP/AMPAR auxiliary | `Cacng3` | 0 | no FDR 0.05 or FDR 0.10 rows; all top nominal rows had `p_adj = 1.0` |
| core PSD scaffold | `Dlg4` | 1 | the only FDR 0.05 row was its own transcript, `Dlg4` logFC `-0.444`, `p_adj = 1.15e-8`; no downstream row passed |
| GRIP1/AMPAR trafficking | `Nsf` | 0 | no FDR 0.05 or FDR 0.10 rows in the focal group |
| GRIP1/AMPAR trafficking | `Atad1` | 1 | only `Atad1` itself passed FDR 0.05; the leading downstream row, `Smarcd1`, was only a near miss at `p_adj = 0.0676` |
| AMPAR biogenesis/trafficking | `Cpt1c` | 1 | only `Cpt1c` itself passed |
| AMPAR biogenesis/trafficking | `Frrs1l` | 1 | only `Frrs1l` itself passed |
| AMPAR/trafficking boundary | `Ica1` | 0 | no focal DEG |
| AMPAR-ubiquitination boundary | `Rnf220` | 0 | no focal DEG |
| PSD scaffold | `Shank2` | 0 | no FDR 0.05 or FDR 0.10 rows |
| PSD scaffold | `Shank3` | 2 | two sparse rows, one being the self-transcript |
| PSD Ras/Rap scaffold | `Syngap1` | 0 | no focal FDR 0.05 or FDR 0.10 rows; self-row `p_adj = 0.117` |
| PSD/mGluR scaffold | `Homer2` | 0 | no focal FDR 0.05 or FDR 0.10 rows |
| MAGI scaffold | `Magi2` | 0 | no focal FDR 0.05 or FDR 0.10 rows |
| NMDAR core counterexample | `Grin1` | 89 | broad, real thalamic response with 40 positive and 49 negative FDR rows |
| NMDAR subunit counterexample | `Grin2a` | 1 | only `Grin2a` itself passed |
| NMDAR subunit counterexample | `Grin2b` | 2 | self-transcript plus `Pianp` |
| NMDAR boundary | `Grin2d` | 0 | no focal DEG |

The run-local profile comparison over `Gria1`, `Gria2`, `Gria3`, `Cacng2`, `Cacng3`, `Dlg4`, `Nsf`, `Atad1`, `Cpt1c`, `Frrs1l`, `Grin1`, `Shank2`, `Syngap1`, `Homer2`, and `Magi2` gave the same picture at the continuous-profile level:

- 10 of 15 nominated nodes had no FDR 0.05 feature in the focal class.
- Four had only a 1-to-9-gene response, usually a self-transcript.
- `Grin1` alone was in the `at_least_50_significant_features` bin.
- Whole-profile correlations among the near AMPAR/scaffold nodes were noise-scale. For example, among inspected focal pairs, `Gria2` versus its explicit peers had Pearson/cosine values near zero: `Gria1`, `0.0229/0.0209`; `Gria3`, `0.0078/0.0093`; `Cacng3`, `-0.0267/-0.0265`; `Nsf`, `-0.0022/-0.0004`; `Homer2`, `0.0219/0.0235`; `Magi2`, `0.0110/0.0092`.
- FDR-level intersection counts between `Gria2`, `Cacng2`, `Dlg4`, or `Atad1` and their GRIP1-neighborhood peers were zero because the focal signatures were empty or singleton dominated.

## Target-specific reasoning

### Grip1

`Grip1` encodes a multi-PDZ postsynaptic scaffold best known for binding the C termini of GluA2/GluA3 AMPAR subunits. It is mechanistically tied to AMPAR retention and recycling rather than to a nuclear transcription-factor pathway: GRIP1/GRIP2 bind GluR2/3 AMPARs in brain (Wyszynski et al. 1999), GRIP1 can link AMPAR cargo to kinesin for dendritic delivery (Setou et al. 2002), NEEP21-GRIP1-GluR2 complexes regulate endosomal sorting and recycling (Steiner et al. 2005), activity can regulate GRIP1 abundance and surface GluR2 through an NMDAR/Ca2+ pathway (Guo and Wang 2007), and ATAD1/Thorase can disassemble GluA2-GRIP1 complexes (Piard et al. 2018).

The most direct training analogs in this assay were therefore the AMPAR-core and AMPAR-trafficking genes, not the broad chromatin or proteostasis responders that dominate the high-count tail. In the same focal group, `Gria1`, `Gria2`, `Gria3`, `Cacng2`, `Cacng3`, `Nsf`, `Ica1`, and `Rnf220` all had `0` DEGs. `Atad1`, `Cpt1c`, and `Frrs1l` each had `1`, but those singleton responses were their own mRNA rather than a shared AMPAR-loss downstream program. The same-experiment Distributed Agents corpus summarizes the broader pattern as AMPAR-core and AMPAR-trafficking/scaffold perturbations being buffered in basal juvenile neurons; `Gria2:F004`, `Cacng2:F004`, `Cacng3:F003`, `Gria1:F003`, `Gria3:F003`, `Rnf220:F003`, and related findings all point to flat, near-null, or singleton-only surfaces for represented AMPAR components.

`Dlg4`, `Homer2`, `Shank2`, `Syngap1`, `Magi2`, `Nlgn3`, and `Nrxn2` provide a second, postsynaptic-scaffold boundary. They are less directly GRIP1-like than GluA2/TARP/NSF/ATAD1, but they test whether acute P16 loss of a local synaptic scaffold tends to drive compensatory nuclear RNA in recovered neurons. The focal counts were again zero or one for the nearest PSD nodes: `Dlg4 = 1`, `Homer2 = 0`, `Shank2 = 0`, `Syngap1 = 0`, `Magi2 = 0`, and `Nlgn3 = 1`. The corpus `Dlg4:F004` claim found that several represented PSD scaffold or adhesion perturbations converge by shared near-zero DE surfaces, not by a signed DEG program.

The major counterexample is `Grin1`, which gave `89` focal DEGs. I used it as a power and biology boundary rather than as a positive Grip1 analog. Its response shows that thalamic glutamatergic neurons and the P16 sparse CRISPR design can report an ionotropic-glutamate-receptor transcriptional state when the perturbation couples receptor loss to nuclear remodeling. GRIP1 is closer to GluA2/GluA3 trafficking and AMPAR surface localization than to obligate NMDAR channel function, and the observed `Gria1/2/3` and `Cacng2/3` zeros argue that AMPAR-side perturbations usually do not share the `Grin1` response.

On balance, the within-dataset evidence for `Grip1` points to a near-null outcome:

- Grip1 itself was absent as a perturbation, and its closest paralog `Grip2` plus `Pick1`, `Gria4`, `Cnih2/3`, `Shisa6/7/9`, and several TARPs were not in the training target set, so no perfect protein-complex comparator was observed.
- Every available direct AMPAR or GRIP1-trafficking analog was focal-class `0` or target-only `1`.
- The continuous score profiles of the represented analogs had only noise-scale correlations and no shared FDR intersections.
- External GRIP1 biology predicts altered receptor anchoring, endosomal recycling, and synaptic plasticity, which this snRNA-seq endpoint does not directly assay.

I therefore predicted that `Grip1` will behave like `Gria1/2/3`, `Cacng2/3`, `Nsf`, `Homer2`, and `Syngap1` rather than like `Grin1`: no non-self AMPAR program, and no reliable self-transcript singleton in this focal class. The point prediction is `0`.

## Limits

The prediction is an extrapolation because `Grip1`, `Grip2`, and `Pick1` were held out or absent as perturbations, so there is no direct GRIP-family loss signature. GRIP1 has AMPAR-independent roles and may be enriched differently across inhibitory, Purkinje, cortical, and thalamic neurons, so the GluA2/TARP/PSD comparisons are imperfect. A real change in AMPAR surface abundance, endosomal recycling, LTD, dendritic transport, spine physiology, or circuit excitability could occur without any FDR 0.05 nuclear RNA call in the recovered 151 TH cells. Conversely, a self-transcript-only hit would move the true count from 0 to 1 even if all downstream biology remained buffered; the available paralogs and scaffolds did not give enough target-specific evidence to promote that singleton.
