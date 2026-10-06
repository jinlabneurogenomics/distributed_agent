# DEG-count prediction for Dalrd3 in 151 TH Prkcd Grin2c Glut cells

## Question and endpoint

The task asks for the held-out endpoint `n_degs` for each requested genetic perturbation in `151 TH Prkcd Grin2c Glut` cells. I treated the endpoint as the focal-cell count of measured genes with Scanpy/Wilcoxon Benjamini-Hochberg adjusted `pvals_adj < 0.05`, with each knockout compared against its matched non-targeting or safe-targeting controls. `151 TH Prkcd Grin2c Glut` was interpreted as the thalamic Prkcd/Grin2c glutamatergic neuron class, not as a nucleus count or a dopaminergic label.

There was one requested held-out perturbation:

| target_name |
|---|
| Dalrd3 |

I used the training differential-expression parquet and the focal-cell training DEG-count CSV as the direct quantitative evidence. The same-experiment July 260713 sourceguard corpus was checked by `corpus.calibration`, `corpus.graph`, and `corpus.story-count`, but it had no packaged Findings for `Dalrd3`, `Mettl2`, `Mettl2b`, `Mettl6`, or `Elp1`; it therefore did not add target-specific same-experiment prose. I used PubMed-indexed literature for the function of DALRD3 and nearby tRNA-modification genes.

## Quantitative calibration from the supplied training data

The requested endpoint is directly observed only for non-held-out training perturbations. In the 1,674 supplied training counts for this focal cell group, the response was highly sparse:

| summary | value |
|---|---:|
| mean `n_degs` | 14.05 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| perturbations with `n_degs = 0` | 1,205 / 1,674 |

This made zero the calibrated default for a perturbation without a close measured same-complex analog showing a broad focal-cell response.

I then searched the training count table for targets in or near tRNA methylation and wobble/anticodon-loop modification pathways. The direct DALRD3 methyltransferase partners were not measured in the training endpoint table: `Mettl2`, `Mettl2b`, `Mettl6`, `Mettl8`, and `Dalrd3` were all absent. The relevant measured training perturbations were:

| training perturbation | focal `n_degs` | relationship to Dalrd3 |
|---|---:|---|
| `Alkbh8` | 0 | tRNA wobble-uridine methyltransferase/hydroxylase, including modification of tRNA-Arg(UCG), tRNA-Gly(UCC), and tRNA-Sec |
| `Trmt1` | 0 | tRNA N2,N2-dimethylguanosine methyltransferase |
| `Nsun2` | 0 | cytosolic and mitochondrial tRNA m5C methyltransferase |
| `Elp1` | 645 | core Elongator subunit required for U34 modifications on a broader subset of cytosolic tRNAs |
| `Elp2` | 150 | core Elongator subunit; positive within-complex control for `Elp1` |

For these five genes, I pulled their raw focal-cell rows from `training_de_all_cell_groups.parquet` and recomputed the `pvals_adj < 0.05` counts as a cross-check against the CSV. The parquet counts exactly matched the training CSV: `Elp1 = 645`, `Elp2 = 150`, and `Alkbh8 = Nsun2 = Trmt1 = 0`. Recovered perturbed nuclei in the focal class were not unusually absent for the null analogs: `Alkbh8` had 98, `Nsun2` had 156, and `Trmt1` had 232 matched perturbed nuclei, all compared with 23,679 matched controls.

The `Elp1` and `Elp2` signatures were a biologically coherent positive control rather than a direct expectation for `Dalrd3`. In `151 TH Prkcd Grin2c Glut`, the two Elongator perturbations shared 129 significant genes; top induced genes included `Asns`, `Cars`, `Shmt2`, `Slc3a2`, `Chac1`, and aminoacyl-tRNA synthetases, consistent with an amino-acid or integrated-stress translation program. `Elp1` and `Elp2` therefore show that this cell group can detect a broad transcriptional response when loss of a tRNA-modification factor produces that stress state. The response should not be transferred wholesale to `Dalrd3`: Elongator installs U34 side-chain modifications needed by many tRNAs, while DALRD3 acts as a substrate-recognition factor for a narrower METTL2-dependent m3C32 branch.

The closer null comparators mattered more for the zero/nonzero decision. `Alkbh8`, like `Dalrd3`, affects a limited set of anticodon/wobble modified tRNAs, is linked to neurodevelopmental phenotypes, and touches arginine tRNA biology, yet its acute perturbation produced no focal FDR-significant genes. `Trmt1` and `Nsun2` are also disease-associated tRNA methyltransferases, and both were transcriptionally quiet in the same cell group. These are imperfect because none is the DALRD3/METTL2 complex itself, but together they show that a neuronal disease connection plus loss of a tRNA methylation enzyme is not sufficient in this assay to give even a low double-digit DEG count.

## External biological evidence

DALRD3 encodes a DALR anticodon-binding protein that works with METTL2 to place 3-methylcytosine at position 32 of particular arginine tRNAs. Lentini et al. showed that DALRD3 forms a complex with METTL2, recognizes the arginine tRNAs destined for m3C modification, and that DALRD3-deficient human cells have nearly complete loss of m3C in tRNA-Arg species; they also linked a homozygous DALRD3 nonsense mutation to developmental delay and early-onset epileptic encephalopathy (Lentini et al., 2020, doi:10.1038/s41467-020-16321-6, PMID:32427860). Zhang et al. later identified a homozygous R517C DALRD3 missense variant in the DALR domain, with reduced METTL2 association and impaired substrate-tRNA interaction in patient cells (Zhang et al., 2024, doi:10.1016/j.xhgg.2024.100377, PMID:39482881).

The broader m3C32 literature supports keeping this branch separate from Elongator. METTL2-family enzymes and METTL6 have mutually specialized substrate choices: METTL2A/B methylate tRNA-Arg and tRNA-Thr members, whereas METTL6 methylates serine tRNAs with SerRS as a substrate-selection factor (Xu et al., 2017, doi:10.1074/jbc.M117.798298, PMID:28655767; Ignatova et al., 2020, doi:10.1126/sciadv.aaz4551, PMID:32923617; Mao et al., 2021, doi:10.1093/nar/gkab603, PMID:34268557; Cui et al., 2024, doi:10.1038/s41467-024-50161-y, PMID:38982125; Throll et al., 2024, doi:10.1038/s41594-024-01341-3, PMID:38918637). This makes DALRD3 a selective adaptor, not an obligate subunit of the broad U34 Elongator machinery.

Other disease-associated tRNA-modification genes illustrate why complete developmental loss-of-function literature does not imply a strong acute postnatal snRNA-seq footprint. ALKBH8 is required for mammalian wobble-uridine modifications and affects tRNA-Sec-dependent selenoprotein synthesis (Songe-Moller et al., 2010, doi:10.1128/MCB.01602-09, PMID:20123966); human truncating ALKBH8 variants cause intellectual disability with severe wobble-modification impairment (Monies et al., 2019, doi:10.1016/j.ajhg.2019.03.026, PMID:31079898). TRMT1 loss impairs tRNA dimethylguanosine modification and causes redox/translation defects and neurodevelopmental disease (Dewe et al., 2017, doi:10.1128/MCB.00214-17, PMID:28784718; Zhang et al., 2020, doi:10.1002/humu.23976, PMID:31898845). NSUN2 variants cause an autosomal-recessive intellectual disability syndrome, and NSUN2 installs m5C on nuclear and mitochondrial tRNAs (Khan et al., 2012, doi:10.1016/j.ajhg.2012.03.023, PMID:22541562; Abbasi-Moheb et al., 2012, doi:10.1016/j.ajhg.2012.03.021, PMID:22541559; Van Haute et al., 2019, doi:10.1093/nar/gkz559, PMID:31276587). All three had `n_degs = 0` in the supplied focal-cell DEG counts.

## Target-specific prediction

### Dalrd3

`Dalrd3` loss is expected to reduce METTL2 targeting of a subset of arginine tRNAs and perturb translational decoding subtly. The endpoint chain is:

`Dalrd3` CRISPR loss in postmitotic neurons -> impaired DALRD3/METTL2 recruitment to tRNA-Arg substrates -> partial loss of m3C32 and codon-specific translation changes -> possible proteostatic or stress propagation if the affected translational branch is limiting -> recovery of nuclei 3 to 4 weeks later -> Wilcoxon DE against matched controls in thalamic glutamatergic cells.

The first two mechanistic links are well supported by the DALRD3/METTL2 literature, but the latter links are weak in this experiment. The acute AAV CRISPR perturbation is mosaic and partial on a juvenile postmitotic background, not a congenital biallelic loss in a developing human brain. The direct METTL2 adaptor complex was not measured among training perturbations, so there is no exact within-complex focal response to transfer. More distant tRNA-modification perturbations with disease relevance, `Alkbh8`, `Trmt1`, and `Nsun2`, were all measured as null in this focal cell group. The only broad tRNA-modification signal, `Elp1`/`Elp2`, came from the Elongator U34 pathway and had a distinctive amino-acid-stress signature; broad pathway membership alone is insufficient to assign that 150 to 645 DEG response to the narrower DALRD3 m3C32 arginine-tRNA adaptor.

I therefore predicted that `Dalrd3` would be below the FDR 0.05 detection threshold in `151 TH Prkcd Grin2c Glut` cells:

| target_name | predicted_n_degs |
|---|---:|
| Dalrd3 | 0 |

## Limits and uncertainty

The prediction is extrapolative because the most direct mammalian partners, `Mettl2`, `Mettl2b`, and `Mettl6`, were absent from the training count table and the same-experiment corpus exposed no DALRD3-specific Findings. The null `Alkbh8`/`Trmt1`/`Nsun2` analogs are mechanistically adjacent but not identical: they modify different bases or tRNAs and may have different turnover rates in postmitotic neurons. The `Elp1`/`Elp2` positive counterexamples prove that tRNA-modification defects can be highly visible in this cell class, so a low nonzero `Dalrd3` response is plausible if m3C32 is unexpectedly limiting in thalamic Prkcd/Grin2c neurons. I treated the measured endpoint as assay- and power-dependent response breadth among recovered nuclei and did not interpret a zero prediction as failed editing, lack of biological function, or lack of developmental importance.
