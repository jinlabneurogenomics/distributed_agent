# Question and endpoint

I predicted the held-out `n_degs` for the one requested perturbation, `Slc24a5`, in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons.  The target was held out as a perturbation, so I treated the endpoint itself as absent from the supplied matrices and used the focal-cell training DEG counts as directly observed calibration for non-held-out genes.  A predicted value of `0` means that no measured gene is expected to pass Wilcoxon Benjamini-Hochberg FDR 0.05 in this cell group.

The task is a scalar response-breadth prediction rather than a ranked list.  I therefore did not use the unavailable ranked-supervision workbench or unavailable bounded predictive-graph review.  I queried the declared parquet directly with DuckDB for focal-cell rows and used PubMed/NCBI E-utilities for external mechanism checks.  I also used the run-local PerturbAI atlas dataset portrait, task bindings, measurement registry, and coverage/capability manifests.  A bounded query to the July 260713 sourceguard BioKG only checked whether weak solute-carrier comparators were visible TargetGene nodes; no graph topology or Finding multiplicity was used as endpoint evidence.

# Dataset calibration

The requested-target CSV contained exactly:

| target_name |
|---|
| Slc24a5 |

`Slc24a5` had 0 rows as `gene_target` in the declared parquet, confirming the intended holdout.

The focal training count table had 1,674 non-held-out perturbations.  Its `n_degs` distribution was sparse and zero-inflated: median 0, 75th percentile 1, 90th percentile 2, 95th percentile 18, and 469/1,674 targets had any focal-cell DEG.  Large footprints existed but were exceptional: `Uba5` 2677, `Tpr` 1768, `Sin3a` 1433, and `Rnpc3` 868 were among the largest responses.

For focal-cell expression evidence, I counted, for named training perturbations, rows satisfying:

```sql
select gene_target, count(*) as measured_genes, sum(pvals_adj < 0.05) as fdr05
from read_parquet(training_de_all_cell_groups.parquet)
where group_name = '151 TH Prkcd Grin2c Glut'
  and gene_target in (...)
group by gene_target;
```

The closest direct checks were null: there was no non-held-out `gene_target` beginning with `Slc24`, and no `Slc45a2`, `Oca2`, `Tyr`, `Tyrp1`, `Mitf`, `Pmel`, or `Trpm1` pigmentation-pathway perturbation in the parquet.  `Slc24a5` was present as a measured transcript, but in the focal cell group its adjusted p-value was 1.0 for all 1,674 training perturbations and never approached significance; with no raw expression matrix this is not a quantitative baseline-expression estimate, but it is consistent with the gene being effectively uninformative in this neuronal population.

# Target-specific reasoning

## Slc24a5

### Within-dataset analogs

No close NCKX-family or melanogenesis perturbation was measured in the focal training set, so there was no high-confidence same-family expression signature to transfer.  I instead used weak analogs as counters to an over-broad solute-transporter or organelle-acidification argument:

| training perturbation | focal `n_degs` | expression-pattern evidence | interpretation for `Slc24a5` |
|---|---:|---|---|
| `Slc25a12` | 1 | one focal DEG, the self transcript `Slc25a12` | A neuronal mitochondrial carrier can be edited yet produce only a self-transcript footprint in this assay; it is only a weak analog because SLC25A12 is mitochondrial rather than a melanosomal/TGN NCKX exchanger. |
| `Slc25a13` | 0 | no FDR 0.05 focal genes | Another mitochondrial carrier null; weak evidence that solute-carrier status alone is not enough to expect a broad DEG response. |
| `Slc25a26` | 0 | no focal DEGs | Same weak counterexample. |
| `Slc25a27` | 0 | no focal DEGs | Same weak counterexample. |
| `Slc25a36` | 0 | no focal DEGs | Same weak counterexample. |
| `Slc25a4` | 1 | one focal DEG, the self transcript `Slc25a4` | Weak cation/solute-carrier counterexample; not a same-pathway analog. |
| `Slc25a46` | 1 | one focal DEG, the self transcript `Slc25a46` | Weak cation/solute-carrier counterexample; not a same-pathway analog. |
| `Rab27a` | 0 | no focal DEGs | A pigment-vesicle-associated trafficking gene did not give a recovered thalamic signature; it is not an obligate `Slc24a5` partner but is directionally consistent with the melanocyte-specific branch being inactive here. |
| `Dtnbp1` | 0 | no focal DEGs | Hermansky-Pudlak/BLOC lysosome-related-organelle biology is a closer organelle analogy than generic transport, and it was null in this focal group. |
| `Ap3b1` | 0 | no focal DEGs | AP-3 lysosome-related-organelle trafficking was null; again this is a weak counterexample rather than an NCKX-specific surrogate. |
| `Atp2c1` | 1 | only the self transcript passed FDR | Golgi Ca/Mn transport can be perturbed with no broad focal response. |
| `Atp6ap2` | 2 | self transcript plus `Atp6v0a1` | A lysosomal/vacuolar acidification component gave only two DEGs. |
| `Atp6v0a1` | 1 | only the self transcript passed FDR | Another acidification-related perturbation with a self-only footprint. |

I also treated `Rab7` and `Vps35` as counterexamples.  `Rab7` has a large focal footprint of 501 DEGs and `Vps35` has 17, showing that endolysosomal dysfunction can be visible in `151 TH Prkcd Grin2c Glut` cells.  Their biology is much broader than SLC24A5: late endosome/autophagy and retromer traffic are core neuronal processes, whereas the established SLC24A5 phenotype is cation exchange in the pigment-organelle/TGN pathway.  They therefore argue against calling all organelle-ion genes silent, but they do not create a same-outcome prior for `Slc24a5`.

### External mechanism evidence

SLC24A5/NCKX5 was discovered as the gene mutated in zebrafish `golden`, an intracellular-membrane cation exchanger controlling melanosome number, size, and density; the human ortholog rescues the zebrafish phenotype and the A111T allele is associated with lighter human pigmentation (Lamason et al. 2005, DOI: 10.1126/science.1116238, PMID: 16357253).  In cultured human and mouse melanocytes, siRNA loss of SLC24A5 reduced melanin production, and Ginger et al. showed that NCKX5 has potassium-dependent Na/Ca exchange activity and partial trans-Golgi localization (Ginger et al. 2007, DOI: 10.1074/jbc.M707521200, PMID: 18166528).  Later cell-biological work localized NCKX5 to the TGN or mitochondria of pigment cells and linked its loss to defective melanosome Ca handling, PMEL fibril formation, melanosome maturation, and pigment production (Zhang et al. 2019, DOI: 10.1242/jcs.232009, PMID: 31201282).  Human SLC24A5 variants cause oculocutaneous albinism type 6, and a zebrafish slc24a5 knockout has reduced melanin and pigmentation (Yousaf et al. 2020, DOI: 10.1111/pcmr.12879, PMID: 32274888); a mouse G200R knock-in likewise decreased hair, skin, and retinal pigment, especially in retinal pigment epithelium (Saito et al. 2021, DOI: 10.1111/pcmr.13024, PMID: 34870899).

The causal chain for transfer is therefore: `Slc24a5` loss of function -> altered NCKX5 cation exchange in the TGN/mitochondria of pigment cells -> abnormal melanosome maturation and pigmentation -> ocular/skin/hair pigment phenotypes.  The requested experiment perturbs sparse postmitotic NeuN-positive thalamic glutamatergic neurons and reads survivor-conditioned nuclear RNA after 3-4 weeks.  The chain breaks at the exposure/limiting-function step: these neurons do not have melanosomes or a known SLC24A5-dependent pigment-organelle maturation program, and there is no training perturbation of a direct NCKX5 partner showing that a hidden SLC24A5-dependent calcium pathway is active in this cell group.

### Prediction

I predict `Slc24a5` will be non-differential in this focal group:

| target_name | predicted_n_degs |
|---|---:|
| `Slc24a5` | 0 |

The zero is driven primarily by external gene-function specificity and by negative within-dataset calibration of only weakly related transport or lysosome-related-organelle genes.  It is not based on measured self-knockdown, because the dataset portrait warns that self-transcript loss is not a reliable editing-efficiency measure.

# Limits

The prediction is an extrapolation because the training data contain no `Slc24` perturbation and no canonical SLC24A5 melanogenesis neighbor.  The negative solute-carrier, Golgi-calcium, AP-3/BLOC, and Rab27a training perturbations are directionally useful but not same-complex evidence, so they cannot prove that `Slc24a5` is inert.  Conversely, `Rab7` and `Vps35` show that broad endolysosomal biology can be visible in the focal thalamic neurons, but their neuronal housekeeping roles are not specific counterevidence to the pigment-cell SLC24A5 chain.  Finally, the endpoint is a BH-thresholded count with finite matched-cell power; a small transcriptional shift under `Slc24a5` loss could exist without crossing FDR 0.05 in this held-out assay.
