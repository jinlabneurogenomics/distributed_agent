# DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and endpoint

The requested held-out perturbation set contains one gene, `Aifm1`, and the target row was absent from both declared training inputs, as expected. I interpreted the task as a scalar point prediction of the total number of `151 TH Prkcd Grin2c Glut` measured genes with `pvals_adj < 0.05` after `Aifm1` CRISPR loss of function.

The target transcript itself counts toward `n_degs` if it passes FDR. I therefore used two related but distinct quantities:

- `n_degs` from `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, which is the directly observed endpoint for non-held-out genes.
- filtered focal-cell rows from `training_de_all_cell_groups.parquet`, to see whether a count of one represented the target transcript alone or a propagated downstream response.

The same-experiment July corpus was used only as packaged interpretation of this screen, not as independent replication. External biological priors were used to decide which visible perturbations are mechanistically relevant to `Aifm1`.

## Sources

- Declared parquet: `training differential-expression dataset`.
- Declared focal training endpoint: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared held-out manifest: `single-target request for Aifm1`.
- Internal semantic corpus: `perturbai-july-260713-sourceguard-1773-v1`, especially the bounded `Ndufa10`, `Ndufs2`, `Ndufs8`, `Ndufa4`, `Opa1`, and `Yme1l1` reports plus a graph query confirming that the `Ndufa10` complex-I comparator report linked the expected `Ndufa*`, `Ndufb*`, `Ndufs*`, `Ndufv*`, and `Ndufaf*` genes. Those graph links were used as navigation and not as scores.
- External literature retrieved through PubMed:
  - Klein et al. 2002, Nature, DOI `10.1038/nature01034`, PMID 12353028: the harlequin mouse mutation downregulates `Aifm1` and causes progressive retinal and cerebellar neurodegeneration with oxidative stress.
  - Vahsen et al. 2004, EMBO Journal, DOI `10.1038/sj.emboj.7600461`, PMID 15526035: AIF deficiency compromises oxidative phosphorylation and complex-I content in cells and in harlequin retina/brain.
  - El Ghouzzi et al. 2007, Journal of Neuropathology and Experimental Neurology, DOI `10.1097/NEN.0b013e318148b822`, PMID 17805014: AIF-deficient harlequin mice develop early mitochondrial degeneration followed by progressive multifocal neuropathology.
  - Perier et al. 2010, Annals of Neurology, DOI `10.1002/ana.22034`, PMID 20695011: AIF-deficient harlequin mice have a complex-I structural deficit that sensitizes dopaminergic neurons to MPTP but is not by itself a broad nigrostriatal degeneration trigger.
  - Reinhardt et al. 2020, BBA Molecular Basis of Disease, DOI `10.1016/j.bbadis.2020.165746`, PMID 32105825: AIFM1 participates in the CHCHD4/MIA40 intermembrane-space import pathway.
  - Herrmann and Riemer 2020, Biological Chemistry, DOI `10.1515/hsz-2020-0254`, PMID 32769219: AIFM1 promotes CHCHD4 import and complex-I assembly in addition to its apoptotic role.
  - Salscheider et al. 2022, EMBO Journal, DOI `10.15252/embj.2022110784`, PMID 35859387: AIFM1 and CHCHD4 form a disulfide-relay module needed for efficient import of the complex-I subunit NDUFS5; AIFM1 loss stalls complex-I assembly.

## Quantitative calibration

I read the 1,674-row focal training CSV, verified all `target_name` values were unique, and inspected the endpoint distribution. The focal class is zero-heavy: 1,205 of 1,674 visible perturbations had `n_degs = 0`; the median was 0, the mean was 14.05, and a small tail reached 2,677 DEGs.

For `Aifm1`, a genome-wide average would be inappropriate because AIFM1 is a mitochondrial oxidoreductase and CHCHD4 partner whose loss should first impair complex-I assembly rather than behave like a transcription factor, spliceosome component, proteasome subunit, or chromatin regulator from the high-count tail. I therefore queried the parquet only for `151 TH Prkcd Grin2c Glut` rows from respiratory-chain and mitochondrial-maintenance perturbations and inspected all rows with `pvals_adj < 0.05`.

The focal complex-I neighborhood was almost entirely silent downstream:

| visible training target | focal `n_degs` | focal FDR<0.05 expression evidence |
| --- | ---: | --- |
| `Ndufa10` | 1 | `Ndufa10` itself was down, logFC -0.650, FDR 4.84e-7; no downstream DEG was present. |
| `Ndufa6` | 1 | `Ndufa6` itself was down, logFC -0.432, FDR 0.00136; no downstream DEG was present. |
| `Ndufs2` | 1 | `Ndufs2` itself was down, logFC -0.728, FDR 8.26e-12; no downstream DEG was present. |
| `Ndufs8` | 1 | `Ndufs8` itself was down, logFC -0.650, FDR 3.06e-8; no downstream DEG was present. |
| `Ndufb10` | 1 | `Ndufb10` itself was down, logFC -0.843, FDR 6.79e-19; no downstream DEG was present. |
| `Ndufb11` | 1 | `Ndufb11` itself was down, logFC -0.563, FDR 0.0207; no downstream DEG was present. |
| `Ndufb8` | 1 | `Ndufb8` itself was down, logFC -0.591, FDR 0.00131; no downstream DEG was present. |
| `Ndufb9` | 1 | `Ndufb9` itself was down, logFC -0.859, FDR 9.53e-5; no downstream DEG was present. |
| `Ndufc2` | 1 | `Ndufc2` itself was down, logFC -0.572, FDR 3.27e-5; no downstream DEG was present. |
| `Ndufv2` | 1 | one off-pathway row, `Cdc40`, was up, FDR 0.0279; the `Ndufv2` self row did not pass FDR. |
| `Ndufa11`, `Ndufa12`, `Ndufa8`, `Ndufa9`, `Ndufaf2`, `Ndufaf4`, `Ndufaf5`, `Ndufb3`, `Ndufb7`, `Ndufs4`, `Ndufs7`, `Ndufv1` | 0 each | no focal-cell row crossed FDR 0.05. |

The broader mitochondrial comparison sharpened the boundary:

- `Opa1` had `n_degs = 37` at FDR 0.05 in the focal class and induced `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Mthfd2`, aminoacyl-tRNA synthetases, and related ATF4/ISR genes. This proves that a mitochondrial lesion can produce a visible nuclear stress signature in this assay, but `Opa1` directly alters inner-membrane fusion and cristae structure and its July report explicitly showed that `Yme1l1`, `Mff`, `Afg3l2`, and `Clpp` did not phenocopy it.
- `Yme1l1`, `Mff`, `Afg3l2`, `Clpp`, `Clpx`, and `Lonp1` all had `n_degs = 0` in the focal training endpoint, arguing that perturbing mitochondrial proteostasis or morphology genes is not sufficient to guarantee an `Opa1`-like ISR in recovered `151` nuclei.
- Complex-IV structural controls were also flat or target-only: `Ndufa4`/`COXFA4` had `n_degs = 1` from its own self row, while `Cox4i1`, `Cox6a1`, `Cox7b`, and `Cox8a` each had zero. `Cox5a` had one self-row DEG.

## Target-specific causal transfer

### `Aifm1`

`Aifm1` encodes mitochondrial apoptosis-inducing factor, an intermembrane-space flavoprotein with a survival role that is separable from caspase-independent cell death. Mechanistically, the best transfer path is:

`Aifm1` CRISPR loss of function -> less functional AIFM1 protein in edited juvenile neurons -> less efficient CHCHD4/MIA40 disulfide-relay import, especially for NDUFS5 -> impaired complex-I assembly or stability -> possible respiratory deficiency and ROS or ATF4/ISR activation -> survival-conditioned nuclei sampled 3-4 weeks later -> Wilcoxon DEGs in `151 TH Prkcd Grin2c Glut`.

The intervention is therefore expected to move in the same broad direction as impairment of limiting complex-I genes, but only if the acute mosaic allele pool depletes enough AIFM1 protein to cross the complex-I stress threshold by harvest. AIFM1 is upstream of one complex-I assembly route rather than itself a stoichiometric NDUF subunit, and the direct complex-I subunits in training were already strongly buffered in this focal class. `Ndufs2`, `Ndufs8`, `Ndufa10`, `Ndufa6`, `Ndufb8`, `Ndufb9`, `Ndufb10`, `Ndufb11`, and `Ndufc2` all reached exactly one FDR<0.05 row in `151`, almost always the self transcript, with no recurrent `Asns`/`Ddit3`/`Chac1` or mitochondrial RNA program. Twelve other NDUF/NDUFAF genes were exactly zero.

The positive counterexample, `Opa1`, does not justify a tens-of-DEGs prediction for `Aifm1`: `Opa1` directly perturbs cristae/fusion and crossed into an ATF4 amino-acid stress state in the focal cell type, whereas AIFM1 maps through complex-I assembly, and the visible complex-I perturbations did not. The harlequin mouse literature supports real AIFM1 neurobiology, retinal/cerebellar vulnerability, and progressive mitochondrial degeneration, but those phenotypes arise from chronic hypomorphic animals or toxin sensitization rather than sparse P16 CRISPR in recovered thalamic neuronal nuclei.

I therefore predict a nonzero but minimal count. The most likely single significant row is `Aifm1` itself; I do not predict a robust downstream mitochondrial ISR, mitophagy, redox, or amino-acid module. The point prediction is:

| target_name | predicted_n_degs |
| --- | ---: |
| `Aifm1` | 1 |

## Limits and uncertainty

- The held-out `Aifm1` perturbation has no expression signature, DEG count, matched-cell count, indel fraction, protein depletion, or complex-I activity measurement in the supplied inputs.
- `Chchd4`, `Ndufs5`, `Aifm2`, and `Aifm3` were not visible focal training perturbations, so the closest AIFM1-specific import branch and paralog branch could not be checked directly.
- The prediction leans heavily on same-pathway complex-I analogs. Those analogs are appropriate for the expected respiratory-chain consequence, but AIFM1 has redox and apoptotic biology outside structural complex I.
- AIFM1 deficiency in mice can produce progressive retinal, cerebellar, thalamic, striatal, and cortical pathology with glial and vascular involvement. The screen under-samples non-neuronal amplification, excludes olfactory bulb and hindbrain, observes nuclear RNA only in recovered NeuN+ nuclei, and was harvested before chronic adult degeneration would be expected.
- A severe early AIFM1 lesion could kill or deplete the most affected cells before sampling and leave a muted survivor signature; this dataset measures the survivor-conditioned transcriptome, not the initial edited-cell denominator.
