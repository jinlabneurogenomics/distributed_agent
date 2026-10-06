# Hold-out DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and endpoint

I predicted the held-out `n_degs` for `Sdhb` in `151 TH Prkcd Grin2c Glut` cells. The endpoint is the integer count of measured genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` for an `Sdhb` CRISPR perturbation in the focal cell group. The held-out `Sdhb` perturbation was absent from both declared inputs, so I treated the supplied differential-expression parquet and focal training DEG counts as the direct quantitative evidence for other targets, and external mitochondrial biology as prior knowledge for choosing which visible perturbations can be transferred to `Sdhb`.

One ambiguity is whether the DEG count includes the guide target transcript itself. The focal training CSV counts every measured gene with FDR < 0.05, and the direct parquet slice shows self-transcript rows are included; for example `Sdha` has exactly one focal DEG at FDR < 0.05, the `Sdha` row itself. I therefore predicted the total held-out count including a possible `Sdhb` self row, not downstream genes only.

## Sources used

- Declared input parquet: `training differential-expression dataset`.
- Declared focal training counts: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared requested-target manifest: `single-target request for Sdhb`.
- Run-local dataset portrait, task bindings, compact coverage, capability manifest, and measurement registry under `codex_runtime/pipeline/`.
- Same-experiment internal corpus: PerturbAI July 260713 sourceguard-1773 corpus v1, release `perturbai-july-260713-sourceguard-1773-v1`, release date 2026-09-01. I used the packaged `Sdha` report and `Sdha` Findings, plus a bounded BioKG query to find the comparator genes named by Sdha cross-perturbation Findings. These reports and Findings are interpretations of the same experiment as the parquet, not independent replication.
- Reactome stable identifier `R-HSA-70994` for the curated SDH/complex-II reaction.
- External PubMed literature for SDH and mitochondrial-stress mechanisms: Ackrell 2002, DOI `10.1016/s0098-2997(02)00012-2`, PMID 12231007; Selak et al. 2005, DOI `10.1016/j.ccr.2004.11.022`, PMID 15652751; Letouze et al. 2013, DOI `10.1016/j.ccr.2013.04.018`, PMID 23707781; Fessler et al. 2020, DOI `10.1038/s41586-020-2076-4`, PMID 32132706; Guo et al. 2020, DOI `10.1038/s41586-020-2078-2`, PMID 32132707; Fiorese et al. 2016, DOI `10.1016/j.cub.2016.06.002`, PMID 27426517.

## Quantitative calibration

I first checked the focal training-count distribution. The focal file contains 1,674 training targets; 1,205 have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and only the far right tail reaches hundreds to thousands of DEGs. The focal parquet slice likewise contains 1,674 perturbations x 17,259 measured genes for `151 TH Prkcd Grin2c Glut`.

I then queried the focal parquet for Sdhb-relevant metabolic and respiratory-chain targets. Same-complex direct phenocopies were not available: `Sdhb`, `Sdhc`, `Sdhd`, and `Sdhaf1-4` were not perturbation targets. The best available direct anchor was `Sdha`, the FAD-containing catalytic partner of SDHB in complex II. Its focal signature had one DEG at FDR 0.05:

| training target | focal n_degs at FDR<0.05 | relevant focal expression evidence |
| --- | ---: | --- |
| `Sdha` | 1 | the only FDR<0.05 hit was self, `Sdha` log2FC -0.781, adjusted p=2.11e-12; the possible downstream `Edem2` response was subthreshold at adjusted p=0.0646 |
| `Idh3a` | 1 | self-only, `Idh3a` log2FC -0.817, adjusted p=9.27e-11 |
| `Cox5a` | 1 | self-only, `Cox5a` log2FC -1.231, adjusted p=5.39e-21 |
| `Ndufa10` | 1 | self-only, `Ndufa10` log2FC -0.650, adjusted p=4.84e-7 |
| `Ndufb8` | 1 | self-only, `Ndufb8` log2FC -0.591, adjusted p=0.00131 |
| `Ndufs2` | 1 | self-only, `Ndufs2` log2FC -0.728, adjusted p=8.26e-12 |
| `Uqcrc2` | 1 | self-only, `Uqcrc2` log2FC -0.576, adjusted p=0.00299 |
| `Mdh2` | 1 | self-only, `Mdh2` log2FC -0.840, adjusted p=7.37e-5 |
| `Uqcrq` | 1 | one non-self hit, `Gpr180` log2FC -0.466, adjusted p=0.0429 |
| `Dlst`, `Ogdh`, `Suclg1` | 0 each | TCA-cycle comparators in the same focal cell group were FDR-null |
| complex I/III/IV structural genes matching `Nduf*`, `Uqcr*`, `Cox*` | 0-1 each in the focal group | the queried mitochondrial TCA, respiratory-chain, and assembly targets all had focal `n_degs` of 0 or 1 |

The expression-pattern evidence also argued against a shared large mitochondrial transcriptional module. In the Sdha packaged report, the two subthreshold-or-weak downstream genes across all 23 cell groups were `Ndrg4` and `Edem2`, the canonical HIF/pseudohypoxia, ATF4/ATF5 integrated-stress, UPRmt, ER-UPR, and NRF2/redox markers were absent, and TCA/OXPHOS comparators did not reproduce the Sdha events. In my focal return-to-data query, none of `Cox5a`, `Dlst`, `Idh3a`, `Ndufa10`, `Ndufb8`, `Ndufs2`, `Ogdh`, `Suclg1`, `Uqcrc2`, or `Uqcrq` moved `Edem2` or the measured SDH subunit and assembly-factor transcripts to FDR significance in `151`. Signed-Wilcoxon-score correlations between `Sdha` and the measured focal TCA/OXPHOS comparators were also near zero, with `Ndufb8` the highest at only 0.094 and `Uqcrq` the lowest at -0.047; I treated those as checks for nonconvergence, not as scores.

## Sdhb causal transfer and prediction

`Sdhb` encodes the iron-sulfur catalytic subunit of succinate dehydrogenase/respiratory complex II. Together, SDHA and SDHB make the matrix catalytic dimer that oxidizes succinate to fumarate and passes electrons through Fe-S clusters toward the ubiquinone site in the SDHC/SDHD membrane anchor; Reactome curates this reaction as the SDH complex dehydrogenating succinate, and Ackrell's complex-II review describes the same four-subunit complex. This makes `Sdha`, not a generic complex-I or complex-III gene, the most appropriate within-dataset analog for `Sdhb`.

The causal chain I used was:

`Sdhb` CRISPR loss of function -> reduced SDHB protein and impaired complex-II electron transfer from SDHA-bound FAD through Fe-S centers -> possible succinate accumulation, altered TCA/ETC flux, and secondary pseudohypoxia or mitochondrial stress -> survival and recovery of postmitotic thalamic glutamatergic nuclei under sparse P16 AAV perturbation -> Wilcoxon DEGs among recovered nuclei.

The external prior says a deep SDH lesion can be severe: SDH inhibition can accumulate succinate and stabilize HIF-alpha by inhibiting prolyl hydroxylases (Selak et al. 2005), SDHx tumors can acquire succinate-associated hypermethylation (Letouze et al. 2013), and mitochondrial dysfunction can be relayed to ATF4 through the OMA1-DELE1-HRI integrated-stress pathway or through ATF5-linked UPRmt programs (Fessler et al. 2020; Guo et al. 2020; Fiorese et al. 2016). That prior raised the probability of a nonzero effect for `Sdhb` relative to a random held-out target.

However, the same-experiment evidence bounded the count downward. `Sdha` directly impairs the same obligate complex-II function yet produced only its self transcript at focal FDR<0.05, with `Edem2` stopping at FDR 0.0646 and no HIF, ISR/UPRmt, broad ER, or redox program in any measured neuronal group. The available TCA and OXPHOS comparators were also sparse in the focal group: most had either a self-only hit or no hit, and `Uqcrq` had a single idiosyncratic `Gpr180` hit rather than a canonical ETC-stress program. Therefore I do not expect the held-out `Sdhb` perturbation to cross from the `0-1 DEG` regime into even the modest 90th-percentile regime of three or more focal DEGs.

I predict that `Sdhb` will be nonzero but minimal, specifically one DEG. The one predicted DEG is most likely the target transcript itself, by analogy to `Sdha` and several other mitochondrial enzymes where the perturbation self row was the only focal FDR<0.05 call. I do not predict a robust downstream thalamic expression program because the Sdha report and the focal comparator queries failed to recover one after the closest available complex-II perturbation or after nearby TCA/OXPHOS structural perturbations.

## Limits

- This is an extrapolation across SDH subunits: `Sdhb`, `Sdhc`, `Sdhd`, and SDHAF assembly factors were absent as training perturbations, so `Sdha` is the only same-complex anchor.
- The primary biochemical endpoint was not observed. The dataset contains survivor-conditioned nuclear RNA contrasts, not SDH activity, succinate/fumarate, HIF-alpha protein, ROS, membrane potential, indel rate, or SDHB protein abundance.
- A stronger, biallelic or tissue-specific `Sdhb` knockout could produce pseudohypoxia, hypermethylation, or mitochondrial ISR programs that the acute mosaic postnatal neuronal screen did not force.
- The difference between one and zero DEGs is mostly a threshold prediction about the held-out self-transcript row. The broad biological call is more stable than the exact count: `Sdhb` is expected to be sparse in this assay, with no canonical complex-II stress state recovered.
