# Held-out DEG-count prediction

## Question and endpoint

The task asks for an integer prediction of `n_degs` for every requested
held-out perturbation in the `151 TH Prkcd Grin2c Glut` focal cell group.
I treated `n_degs` as the exact focal-cell endpoint in the task: the number of
measured genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05`.

There is one requested held-out gene in this run:

| target_name |
|---|
| Dcaf17 |

The held-out `Dcaf17` signature and count are absent from the supplied
differential-expression parquet and from the training count CSV, so the
prediction is necessarily transfer from non-held-out perturbations plus
external gene-function knowledge.

## Sources used

- Declared Perturb-seq differential-expression parquet:
  `training differential-expression dataset`.
  This is direct evidence for measured expression signatures and BH-DEG counts
  of non-held-out perturbations.
- Declared focal-cell training endpoint CSV:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This is direct evidence for `n_degs` of the 1,674 non-held-out perturbations
  in `151 TH Prkcd Grin2c Glut`.
- Declared requested-target CSV:
  `single-target request for Dcaf17`.
- Run-local PerturbAI atlas v5 dataset portrait and measurement registry.
  These were used for experiment semantics: acute postnatal AAV-PHP.eB
  CRISPR-Cas9 loss of function, NeuN+ whole-brain sampling, survivor-conditioned
  snRNA-seq DE, and the warning that measured target RNA loss is not an editing
  efficiency score.
- Internal same-experiment semantic corpus:
  `perturbai-july-260713-sourceguard-1773-v1`. I used its BioKG comparator graph
  only to ask whether the nearest visible DCAF/DDB2 and WD/RNA-processing
  training targets were packaged with explicit comparator links; those links
  were treated as semantic pointers and counterexamples, not as scores.
- PubMed literature:
  - Scrima et al. 2011, FEBS Letters, DOI 10.1016/j.febslet.2011.04.064,
    PMID 21550341. CRL4 is modular: DDB2, CSA, CDT2, and other DDB1-CUL4
    associated factors are substrate receptors that share a CUL4/DDB1 scaffold
    but operate in distinct pathways.
  - Ali et al. 2016, Clinical Genetics, DOI 10.1111/cge.12700, PMID 26612766.
    Human Woodhouse-Sakati syndrome variants include truncating DCAF17 lesions;
    structural analysis of one truncation supported loss of residues needed for
    DDB1 interaction.
  - Ali et al. 2021, American Journal of Medical Genetics A,
    DOI 10.1002/ajmg.a.62501, PMID 34590781. A 58-patient Qatari series
    confirms DCAF17 pathogenic variants as a cause of the neuroendocrine and
    ectodermal Woodhouse-Sakati syndrome, with intellectual disability and
    hearing loss in many patients.
  - Abu-Dawud et al. 2022, Scientific Reports,
    DOI 10.1038/s41598-022-25826-7, PMID 36509865. Mouse Dcaf17 disruption
    alters the testis transcriptome and affects spermatogenic protein
    homeostasis and transcription.
  - Ma et al. 2024, Biology of Reproduction,
    DOI 10.1093/biolre/ioae132, PMID 39239833. A hamster CRISPR model places
    Dcaf17 in early spermatogenic cells and the CRL4 ubiquitin E3 ligase
    receptor family.

## Quantitative calibration over the declared inputs

I used the training count CSV to establish the focal-cell scale:

- training perturbations: 1,674
- median `n_degs`: 0
- 75th percentile: 1
- 95th percentile: 18
- zeros: 1,205 / 1,674
- `n_degs <= 1`: 1,481 / 1,674
- `n_degs > 100`: 42 / 1,674
- maximum: `Uba5`, 2,677 DEGs

That distribution makes zero the dominant prior for perturbations without a
specific high-yield analog.

I then looked for biologically plausible training analogs to `Dcaf17` in the
training endpoint table. The exact CUL4 scaffold genes `Ddb1`, `Cul4a`, `Cul4b`,
`Rbx1`, and `Dda1` were not present as training perturbations. The closest
available DDB1/CUL4/DCAF entries had the following focal counts:

| training target | focal `n_degs` | interpretation |
|---|---:|---|
| Dcaf8 | 0 | another DCAF-labeled substrate-receptor family member, but no BH-significant focal response |
| Ddb2 | 0 | a CUL4-DDB1 substrate receptor for UV-lesion repair; a better CRL4 architectural analog than most WD-repeat genes, but pathway-divergent from Dcaf17 |

I also checked more distant WD-repeat, nucleolar, RNA-helicase, and vesicle
transport counterexamples because DCAF17 has WD/DDB1-adaptor and nucleolar
annotations but no established obligate neuronal partner in the input library:

| training target | focal `n_degs` | why it did not raise the Dcaf17 estimate |
|---|---:|---|
| Wdr37 | 0 | WD-repeat name match only; no focal effect |
| Wdr48 | 0 | WD-repeat/USP partner; no focal effect |
| Ddx39b | 0 | RNA-processing helicase comparator to Ddx3x in the internal corpus; no focal effect |
| Copa | 0 | coatomer trafficking gene, not a Dcaf17 complex member |
| Copg1 | 1 | coatomer trafficking gene; the single DEG was its self transcript |
| Ddx3x | 8 | RNA helicase with mild response, not a CRL4-DCAF17 substrate receptor |
| Wdr26 | 13 | WD-repeat scaffold with small response, not an obligate DCAF17 partner |
| Wdfy3 | 17 | WD-repeat/autophagy scaffold with small response |
| Nop56 | 25 | nucleolar small-nucleolar-RNP protein; modest response but mechanistically too different for count transfer |

For the exact focal-cell expression-pattern check, I filtered the parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and the candidate analog targets,
then recomputed `sum(pvals_adj < 0.05)` and inspected the strongest absolute
Wilcoxon scores. Each selected training target had 17,259 measured rows in this
cell group. The closest CRL4/DCAF entries were flat after BH correction:

| training target | matched perturbed nuclei | focal BH DEGs | minimum focal `pvals_adj` | strongest focal genes by absolute Wilcoxon score |
|---|---:|---:|---:|---|
| Dcaf8 | 165 | 0 | 1.000 | Lrp6, Brox, Npy1r, Nek1 |
| Ddb2 | 215 | 0 | 1.000 | Golm2, Nipa2, Cbx1, Clpp |

The stronger distant examples still had only small focal signatures:

| training target | matched perturbed nuclei | focal BH DEGs | minimum focal `pvals_adj` | strongest focal genes by absolute Wilcoxon score |
|---|---:|---:|---:|---|
| Ddx3x | 138 | 8 | 0.00289 | Ddx3x, Ypel3, Grin2b, Synpo2 |
| Wdr26 | 112 | 13 | 0.000300 | Grin2b, Cyc1, Vmn2r85, Stk25 |
| Wdfy3 | 230 | 17 | 3.24e-09 | Stmn4, Jun, Gpm6a, Gls |
| Nop56 | 206 | 25 | 1.73e-06 | Rsrp1, Ddx17, Chn1, Srsf5 |

I used the same-experiment BioKG comparator graph to check whether those analog
choices were hiding a direct connection from `Dcaf17`. `Dcaf17` was not a
visible `TargetGene` node in the July sourceguard graph; `Dcaf8` and `Ddb2`
were visible. Their comparator links pointed mostly to unrelated low-count
entries, and a few high-count genes appeared only in distant RNA-processing,
proteasome, ufmylation, or beta-catenin stories. Because explicit comparator
mentions do not assert same-endpoint causality, I used those high-count genes
as counterexamples:

| comparator reached through analog reports | focal `n_degs` | Dcaf17 transfer decision |
|---|---:|---|
| Psmb4 | 742 | proteasome core gene; generic protein-turnover similarity is insufficient |
| Psmc1 | 430 | proteasome ATPase; no obligate CRL4-DCAF17 dependency |
| Uba5 | 2,677 | ufmylation pathway; no evidence that acute Dcaf17 KO phenocopies Uba5 |
| Ufc1 | 572 | ufmylation pathway; same issue as Uba5 |
| Ctnnb1 | 383 | Wnt/beta-catenin effector; no directional Dcaf17 link in this setting |
| Hnrnpu | 733 | broad RNA-processing regulator; not a DCAF17 complex member |
| Hnrnpc | 122 | broad RNA-processing regulator; not a DCAF17 complex member |
| Huwe1 | 158 | E3 ligase, but not the same CRL4-DCAF17 limiting function |
| Tnpo3 | 618 | nuclear import factor; Nop56 comparator only, not a Dcaf17 analog |

## Target-specific prediction

### Dcaf17

`Dcaf17` encodes DDB1- and CUL4-associated factor 17, a CRL4 substrate-receptor
family member. Human biallelic loss-of-function variants cause
Woodhouse-Sakati syndrome with endocrine, ectodermal, and neurologic features
(Ali et al. 2021; Ali et al. 2016), and animal Dcaf17 disruption has clear
transcriptional effects in spermatogenesis (Abu-Dawud et al. 2022; Ma et al.
2024). Those data show that Dcaf17 can be biologically important after chronic
or developmental loss in sensitive tissues.

The causal transfer into this experiment is weak:

1. **Intervention:** the atlas perturbation is acute, sparse, postnatal CRISPR
   loss of function in recovered neurons, not germline loss and not a gonadal
   differentiation model.
2. **Direct molecular consequence:** Dcaf17 loss should impair a specific
   CRL4-DCAF17 substrate-receptor branch if the protein is expressed and
   limiting in thalamic glutamatergic neurons.
3. **Propagation:** no in-library obligate partner of DCAF17 was available;
   generic CRL4 membership did not transfer because the available receptor
   `Ddb2` has a different UV-damage recognition role and was BH-null in the
   focal class, while `Dcaf8` was also BH-null.
4. **Exposure/selection and sampling:** a silent recovered signature could miss
   early selection, but the requested endpoint is the survivor-conditioned
   snRNA-seq DEG count, so the closest measured analogs argue for no detectable
   focal transcriptional breadth.

The zero/nonzero decision is driven mainly by the within-dataset training
endpoint: both closest DCAF/DDB2 analogs, `Dcaf8` and `Ddb2`, had `n_degs = 0`
in `151 TH Prkcd Grin2c Glut` and no focal measured gene with adjusted
`pvals_adj < 0.05`. External knowledge keeps `Dcaf17` from being treated as a
random unannotated gene, but it does not provide a specific same-direction,
same-cell-class perturbation that would overcome the strong zero-inflated
training prior. I therefore predict no FDR-significant focal DEGs:

| target_name | predicted_n_degs |
|---|---:|
| Dcaf17 | 0 |

## Limits and uncertainty

- No `Dcaf17` same-experiment DE signature or DEG count was supplied; this is a
  genuine held-out prediction.
- The strongest architectural transfer would be through DDB1/CUL4 core
  components, but `Ddb1`, `Cul4a`, and `Cul4b` were not available training
  perturbations in the focal endpoint CSV.
- `Dcaf8` and `Ddb2` are related only at the CRL4-adaptor level. Scrima et al.
  2011 emphasize that DDB1-CUL4-associated receptors are modular and operate in
  different biological pathways; a `Ddb2` null therefore cannot prove `Dcaf17`
  will be null.
- Mouse and hamster testis Dcaf17 knockouts establish transcriptional
  disruption during spermatogenesis, but that cell state is proliferative and
  developmentally unlike sparse postnatal thalamic glutamatergic neurons.
- A prediction of 0 is only a point estimate for the FDR 0.05 threshold. A
  small response of 1-5 DEGs would be plausible because many weakly responsive
  training perturbations sit on that boundary, but the closest available
  mechanistic anchors landed on the zero side.
