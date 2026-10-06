# Pnpt1 DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The task is to predict the held-out `n_degs` for each requested genetic perturbation in `151 TH Prkcd Grin2c Glut` cells. I interpreted `n_degs` exactly as the supplied endpoint: the count of measured genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in the focal cell group after acute mosaic AAV-CRISPR loss of the requested mouse gene. The requested target list contains one held-out perturbation, `Pnpt1`, and its DE rows and training count are absent by construction.

I treated the training count CSV as a direct observation of this endpoint for non-held-out targets. The Parquet DE rows are direct measurements of per-gene expression changes for those same training perturbations, but not for `Pnpt1`. The same-experiment July 260713 SourceGuard 1773 v1 PerturbAI corpus was used only as packaged interpretation of the same Parquet-derived experiment, not as independent replication. External PubMed literature was used as prior knowledge to decide which represented mitochondrial perturbations are biologically relevant analogs for `Pnpt1`.

## Computations over the declared inputs

I read:

- `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
- `training differential-expression dataset`
- `single-target request for Pnpt1`

The training endpoint covered 1,674 non-held-out perturbations. Its focal-cell distribution was highly zero-inflated: median `0`, 75th percentile `1`, 90th percentile `2`, 95th percentile `18`, 99th percentile `436`, and maximum `2,677` DEGs. Thus a generic non-held-out target, even in this high-yield cell type, usually produced no FDR-significant genes.

For mechanistic analogs I first searched the training targets for mitochondrial RNA, translation, protease, OXPHOS, transporter, and dynamics genes. I then pulled the focal Parquet rows for those targets and counted `pvals_adj < 0.05`, confirming the training counts and identifying whether the significant row was only the edited target transcript. For the direct mitochondrial RNA/translation analog set in `151 TH Prkcd Grin2c Glut`:

| training perturbation | focal `n_degs` | focal interpretation |
|---|---:|---|
| `Lrpprc` | 0 | mitochondrial mRNA stabilization/polyadenylation analog, fully FDR-flat |
| `Gfm2` | 0 | mitochondrial ribosome-recycling/translation analog, FDR-flat |
| `Fars2` | 0 | mitochondrial phenylalanyl-tRNA synthetase, FDR-flat |
| `Lars2` | 0 | mitochondrial leucyl-tRNA synthetase, FDR-flat |
| `Rars2` | 0 | mitochondrial arginyl-tRNA synthetase, FDR-flat |
| `Clpp` | 0 | mitochondrial ClpP protease, focal FDR-flat |
| `Clpx` | 0 | mitochondrial ClpP unfoldase, FDR-flat |
| `Lonp1` | 0 | mitochondrial matrix protease, focal FDR-flat |
| `Yme1l1` | 0 | inner-membrane AAA protease, FDR-flat |
| `Mff` | 0 | mitochondrial fission factor, FDR-flat |
| `Micos13` | 0 | MICOS inner-membrane component, FDR-flat |
| `Dap3` | 1 | only `Dap3` itself significant |
| `Sucla2` | 1 | only `Sucla2` itself significant |
| `Pdha1` | 1 | only `Pdha1` itself significant |
| `Slc25a4` | 1 | only `Slc25a4` itself significant |
| `Park7` | 1 | only `Park7` itself significant |
| `Opa1` | 37 | a real focal mitochondrial-stress response |

For a stress-program counterexample, I checked the focal log-fold changes and adjusted p-values for the `Opa1` ISR/mitochondrial RNA panel across `Clpp`, `Dap3`, `Fars2`, `Gfm2`, `Lars2`, `Lonp1`, `Lrpprc`, `Mff`, `Rars2`, and `Yme1l1`. In the `Pnpt1`-proximal buffered analogs, `Asns`, `Chac1`, `Ddit3`, `Mars1`, `Mthfd2`, `Slc7a5`, `mt-Co2`, `Hspd1`, `Hspe1`, `Clpp`, `Stat1`, `Isg15`, and `Psmb8` were all non-significant in the focal cell group, generally with adjusted `p = 1.0`. By contrast, focal `Opa1` loss had significant `Asns` logFC `0.713`, `Mars1` `0.505`, `Chac1` `1.878`, `Ddit3` `0.873`, `Mthfd2` `1.557`, `Slc7a5` `1.380`, `mt-Co2` `-0.606`, and `Grm7` `-0.244`, showing that this screen and cell group could detect a mitochondrial retrograde/ISR state when a perturbation crossed the threshold to make one.

I also counted significant genes for the same analogs across all measured cell groups. `Opa1` produced significant DEGs in 9 groups, including 47 in `155 MB Glut`, 45 in `191 MB P MY GABA`, and 37 in the focal group. `Lonp1` had 2 to 3 DEGs only in `155 MB Glut` and `217 P MY Pineal Glut`, with none in the focal group. `Dap3`, `Sucla2`, `Slc25a4`, `Pdha1`, `Park7`, and `Clpp` produced only isolated one-gene hits. `Lrpprc`, `Gfm2`, `Fars2`, `Lars2`, `Rars2`, `Clpx`, `Yme1l1`, `Mff`, `Micos13`, `Micu1`, `Mpc1`, and `Mecr` had no FDR-significant focal-cell hits.

## Same-experiment corpus evidence

I inspected the July 260713 SourceGuard 1773 v1 Findings/Evidence ledgers for the relevant training perturbations. The important same-experiment summaries were:

- `Lrpprc`: acute P16 `Lrpprc` CRISPR yielded a pan-measured neuronal transcriptional null, with 0 downstream FDR<0.10 genes in 21 recovered cell groups, and expected mtDNA mRNA, ATF4/ATF5/CHOP/ISR, chaperone, `Clpp`, and `Lonp1` marker programs absent.
- `Fars2`, `Lars2`, `Rars2`, and `Gfm2`: mitochondrial tRNA synthetase or mitochondrial ribosome-recycling perturbations were flat or singleton across the screen and did not recover an ATF4/ISR, OXPHOS, or mitochondrial translation state. The corpus explicitly rejected shared membership in mitochondrial tRNA charging or translation as sufficient to create a convergent acute neuronal snRNA-seq signature.
- `Dap3`: despite being a mitochondrial small-subunit GTPase, `Dap3` had no robust downstream transcriptome and did not activate the `Opa1`-like ISR module.
- `Clpp`, `Clpx`, `Lonp1`, and `Yme1l1`: mitochondrial protease branches were not interchangeable. `Clpp` and `Clpx` lacked a focal ISR/UPR-mt response, and `Lonp1` generated only a very narrow stress response in other cell groups.
- `Opa1`: the focal `Opa1` response was a recurrent amino-acid/ISR state with `Asns`, `Chac1`, `Ddit3`, `Cars`, `Mars1`, `Slc7a5`, one-carbon genes, and some mitochondrial-encoded respiratory transcript decreases. It was the useful positive control demonstrating that a mitochondrial stress program is visible in the screen.

These corpus records are derived from the same experiment as the Parquet, so they calibrate and explain analog choice but do not add an independent biological replicate.

## External biology used for `Pnpt1`

`Pnpt1` encodes mitochondrial polynucleotide phosphorylase, PNPase. PNPase is an imported mitochondrial ribonuclease localized to the intermembrane space/peripheral mitochondrial membrane complex and is required for mitochondrial homeostasis; experimental PNPase reduction impaired membrane potential, respiratory-chain activity, ATP synthase stability, ATP production, and mitochondrial morphology in cultured cells (Chen et al., 2006, DOI `10.1128/MCB.01002-06`, PMID `16966381`).

The clearest molecular route places PNPase in mitochondrial RNA surveillance and processing. hSUV3 and PNPase participate in mitochondrial RNA turnover and degradosome biology (Szczesny et al., 2009, DOI `10.1093/nar/gkp903`, PMID `19864255`), SUV3-PNPase-mtPAP can tune mitochondrial mRNA poly(A)-tail length in response to energetic state (Wang et al., 2014, DOI `10.1074/jbc.M113.536540`, PMID `24770417`), and pathogenic PNPT1 variants cause defective mitochondrial RNA processing and combined respiratory-chain deficiency, including Leigh syndrome (Matilainen et al., 2017, DOI `10.1093/hmg/ddx221`, PMID `28645153`). Bi-allelic human PNPT1 disease shows variable respiratory-chain defects and increased interferon response in blood (Rius et al., 2019, DOI `10.3390/jcm8112020`, PMID `31752325`). Mechanistically, PNPase and SUV3 also restrain mitochondrial double-stranded RNA; loss of either enzyme can let mt-dsRNA escape and activate MDA5/type-I interferon signaling (Dhir et al., 2018, DOI `10.1038/s41586-018-0363-0`, PMID `30046113`).

Those priors make `Lrpprc` the closest direct training analog because it is the represented perturbation whose expected first-order consequence is most proximal to mitochondrial mRNA stability. The mitochondrial tRNA synthetase and ribosome-recycling genes test whether impaired mitochondrial gene expression becomes a strong nuclear DEG-count phenotype in recovered neurons. `Opa1` and `Lonp1` test the main alternative that any mitochondrial dysfunction that lowers respiratory capacity should trigger a CHOP/ATF4 stress program in these neurons.

## Target-specific prediction

### `Pnpt1`

**Causal model.** The intended intervention is acute mosaic CRISPR loss of PNPase beginning at P16. If enough PNPase activity is lost, the direct molecular effect should be altered mitochondrial RNA processing/degradation, possible accumulation or escape of mt-dsRNA, and secondary respiratory-chain dysfunction. That could propagate to an ATF4/CHOP amino-acid ISR, mitochondrial-encoded transcript changes, or a type-I-interferon program. The measured endpoint is FDR-significant nuclear and mitochondrial transcript shifts only among recovered NeuN+ thalamic glutamatergic nuclei 3 to 4 weeks later.

**Training analogs.** The endpoint-bearing internal analogs mostly support a null or one-gene prediction:

- `Lrpprc`, the nearest represented mitochondrial mRNA-homeostasis comparator, had `n_degs = 0` in the focal cell group and 0 downstream genes at FDR<0.10 in all 21 groups reviewed in the corpus. Its expected mtDNA mRNA and secondary ISR/UPR-mt markers were measured but absent. This is the strongest within-dataset argument that perturbing mitochondrial RNA metabolism does not necessarily generate a broad survivor snRNA-seq phenotype here.
- `Gfm2`, `Fars2`, `Lars2`, and `Rars2` had focal `n_degs` of `0`, `0`, `0`, and `0`. These are slightly more downstream than `Pnpt1`: they compromise mitochondrial translation rather than RNA degradation/import. Their common flatness argues that postnatal neurons in this assay frequently buffer partial mitochondrial gene-expression lesions or lose the most severely perturbed cells before the survivor-conditioned transcriptome is measured.
- `Dap3` had focal `n_degs = 1`, but the only FDR<0.05 hit was the `Dap3` transcript itself, so it does not predict a downstream `Pnpt1` program.
- `Clpp`, `Clpx`, `Yme1l1`, `Mff`, `Micos13`, and `Lonp1` were all focal-count `0` despite mitochondrial proteostasis, morphology, or inner-membrane roles. They are counterexamples to assigning DEGs from generic mitochondrial annotation.
- `Opa1` is the main nonzero mitochondrial counterexample, with focal `n_degs = 37`. However, OPA1 acts at inner-membrane fusion and cristae morphology, and in this dataset its same-experiment relatives `Yme1l1`, `Mff`, and `Clpp` did not phenocopy it. I therefore did not transfer the full `Opa1` count to a mitochondrial RNA exonuclease.

The stress-marker panel gave the same sign. If `Pnpt1` behaved like `Opa1`, the focal cell group should show elevated `Asns`, `Chac1`, `Ddit3`, `Mars1`, `Mthfd2`, and `Slc7a5` and lower `mt-Co2`. The closest RNA/translation analogs did not move those genes to FDR significance. If loss of PNPase behaved through mt-dsRNA escape, an interferon module could have raised `Stat1`, `Isg15`, or `Psmb8`; the represented `Lrpprc`, `Fars2`, `Gfm2`, `Lars2`, `Rars2`, `Dap3`, `Clpp`, `Lonp1`, `Mff`, and `Yme1l1` focal rows did not show a significant interferon response either.

**Prediction.** I predict `0` DEGs for `Pnpt1` in `151 TH Prkcd Grin2c Glut`. The zero call is driven primarily by the within-dataset focal counts for `Lrpprc`, mt-aaRS/mitochondrial-translation genes, and mitochondrial quality-control genes. External PNPT1 biology argues that the perturbation is real and can be severe, but in this acute sparse postnatal neuronal screen the closest measured mitochondrial RNA and translation lesions were transcriptionally buffered among recovered nuclei. A one-gene self-hit is plausible, as seen for `Dap3`, `Pdha1`, `Sucla2`, `Slc25a4`, and `Park7`, but the held-out endpoint counts every FDR row and `Pnpt1` has no evidence here for a broad downstream module; with focal median `0` and nearly all direct analogs at `0`, the integer point estimate is `0`.

## Limits and uncertainty

This is an extrapolation from related training perturbations because `Pnpt1` itself was held out. The exact PNPase-SUV3 degradosome was not represented by a `Supv3l1`/SUV3 perturbation in the training count table, and no Polrmt, Tfam, Tfb2m, Mterf, Fastkd, Ptcd, or ELAC2 targets were available for a denser mitochondrial RNA-processing panel. The screen measured steady-state nuclear RNA in recovered nuclei, not PNPase protein, mtRNA poly(A) tails, mt-dsRNA localization, respiratory-chain assembly, ATP production, membrane potential, or pre-assay depletion. Severe `Pnpt1` edits could therefore be missed if they killed cells, prevented recovery, produced a biochemical defect without a steady-state RNA footprint, or required a metabolic/immune challenge. Conversely, PNPase-specific mt-dsRNA escape could in principle activate an interferon program not seen after `Lrpprc` or the mt-aaRS genes, because broad mitochondrial pathway co-membership is not a same-mechanism guarantee. The prediction is therefore a low-count, weak-effect expectation for this exact assay rather than a claim that PNPT1 is biologically dispensable.
