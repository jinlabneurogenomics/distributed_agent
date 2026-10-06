# Prediction trace

## Question and scope

I need to predict the held-out `n_degs` endpoint for the requested perturbations in `151 TH Prkcd Grin2c Glut` cells. Here `n_degs` is the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` for the perturbation versus matched controls in that focal thalamic glutamatergic class.

The requested-target manifest contains one held-out target:

| target_name |
|---|
| Eef1a2 |

`Eef1a2` is absent from both the focal-cell training count CSV and the DE parquet, so I treated all observations for other perturbations as calibration or analogy, not as a measured `Eef1a2` response.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`: exact FDR<0.05 DEG counts for 1,674 non-held-out perturbations in `151 TH Prkcd Grin2c Glut`.
- `[local file: training_de_all_cell_groups.parquet]`: per-gene log2 fold changes and adjusted Wilcoxon p values for non-held-out perturbations.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`: curated within-experiment findings and literature-grounded reports for observed training perturbations.
- PubMed literature:
  - Chambers, Peters, and Abbott 1998, `PMID:9539760`, DOI `10.1073/pnas.95.8.4463`: the mouse `wasted` deletion abolishes `Eef1a2` expression and shows the postnatal requirement for a tissue-specific eEF1A isoform.
  - Pan, Ruest, Xu, and Wang 2004, `PMID:15013623`, DOI `10.1016/j.devbrainres.2003.10.011`: brain undergoes an early-postnatal switch from eEF1A1 to eEF1A2; eEF1A2 protein is restricted to mature terminally differentiated neurons, and wasted mutant neurons lack detectable elongation factor 1A after the switch.
  - Newbery et al. 2007, `PMID:17640869`, DOI `10.1074/jbc.M703962200`: eEF1A2 is essential for post-weaning mouse survival and the wasted phenotype is due to loss of eEF1A2 function.
  - Griffiths et al. 2012, `PMID:22848658`, DOI `10.1371/journal.pone.0041917`: aged `+/wst` mice with reduced eEF1A2 did not show neuromuscular deficits or spinal-cord pathology, supporting substantial tolerance of partial Eef1a2 dose reduction.
  - Lam et al. 2016, `PMID:27441201`, DOI `10.1002/mgg3.219`; Carvill et al. 2020, `PMID:32196822`, DOI `10.1002/humu.24015`; Mohamed and Klann 2023, `PMID:37695913`, DOI `10.1073/pnas.2307704120`: human `EEF1A2` variants cause epilepsy/neurodevelopmental disease, and common missense alleles perturb translation elongation and actin bundling. These data confirm neuronal sensitivity but are not direct calibrators for acute CRISPR loss in mouse thalamic neurons.

## Computational evidence from the training data

I first read the focal-cell count CSV and inspected perturbations in translation, RNA-helicase, mTOR, MAPK, and proteostasis neighborhoods. The focal endpoint is highly sparse: 1,205 of 1,674 training targets, 72.0%, have zero DEGs; the median is 0, the 90th percentile is 2, and only 43 targets have at least 100 DEGs.

I then queried the parquet in the exact focal cell group for the most relevant within-dataset comparators:

```sql
select gene_target, names, logfoldchanges, pvals_adj
from read_parquet(:training_de_parquet)
where group_name = '151 TH Prkcd Grin2c Glut'
  and gene_target in (...)
  and pvals_adj < 0.05
order by gene_target, pvals_adj, abs(logfoldchanges) desc;
```

This returned the following focal response sizes.

| training perturbation | focal n_degs | pattern in 151 TH Prkcd Grin2c Glut |
|---|---:|---|
| `Eef2` | 9 | Elongation-factor perturbation; 6 up and 3 down FDR hits, including `Ranbp2`, `Mul1`, `Prkcsh`, `Tnfrsf12a`, `Chd8` up and `Ufd1`, `Fbxo9`, `Atl1` down. |
| `Hspa8` | 9 | Cytosolic Hsc70 loss; heat-shock/chaperonin induction with `Dnaja1`, `Hspa4l`, `Hsp90aa1`, `Cct6a`, and `Syt4` up. |
| `Ddx3x` | 8 | RNA-helicase perturbation; a weak mixed signature including self-reduction, `Ypel3`/`Tmsb10` up, and `Grin2b`, `Tcea2`, `Ccdc136` down. |
| `Hspa5` | 5 | ER chaperone/UPR branch, with `Hsp90b1`, `Nfe2l1`, `Pdia4`, and `Derl3` up. |
| `Mtor` | 2 | Very small mixed signature, `Rims3` up and `Tmed8` down. |
| `Eif4a2` | 2 | Self-reduction plus `Cadm4` down. |
| `Eif4g1` | 1 | Self-reduction only. |
| `Eif4h` | 1 | One positive hit, `Hexim1`. |
| `Eif5a` | 0 | No focal FDR<0.05 genes. |
| `Eif2ak4` | 0 | No focal FDR<0.05 genes. |
| `Ddx39b` | 0 | No focal FDR<0.05 genes. |
| `Rptor` | 0 | No focal FDR<0.05 genes. |
| `Tsc2` | 86 | Broad mTORC1/sterol/lysosome/PI3K-feedback response, including `Pik3r3`, `Cyp51`, `Slc2a6`, `Hmgcr`, `Ldlr`, `Ddit4`, `Rragd`, `Grn`, and `Lamp2`. |

Using Distributed Agents runtime `profile_compare`, I compared these 13 focal signatures over the 17,259 features measured for all selected nodes. The selected translation-initiation genes, `Mtor`, `Rptor`, `Hspa5`, `Hspa8`, and `Tsc2` did not share any FDR<0.05 focal genes with the `Eef2` signature; their whole-profile correlations were dominated by the many non-significant genes. Thus the focal data do not show a single generic translation- or stress-response signature that I should copy to `Eef1a2`.

The same-experiment corpus supported that interpretation:

- `Eef2:F009` concluded that the `Eef2` response was not a generic feature of perturbing translation-factor or mTORC1-coupled genes: `Eif5a`, `Eif2ak4`, `Eif4a2`, `Eif4g1`, `Eif4h`, `Mtor`, and `Rptor` were flat or nearly flat, while `Tsc2` was broad but nonconvergent.
- `Mtor:F006` reported that `Mtor` loss did not recover selected translation-initiation, sterol/SREBP, lysosome-autophagy, or UPR/ISR RNA programs at FDR<0.10, even though such secondary programs were visible after loss of upstream mTORC1 inhibitors.
- `Tsc2:F007` showed pathway-position uncoupling: `Tsc2` activated a sterol/lysosome/mTOR-feedback branch in several cells, whereas `Mtor`, `Rptor`, `Igf1r`, `Irs1`, and `Akt3` did not form a robust matched FDR-overlap neighborhood.
- `Hspa8:F001` reported a small but real response restricted to four cell groups, with a maximum 9-gene signature in the focal group.

## Target-specific reasoning

### Eef1a2

`Eef1a2` encodes the mature neuronal and muscle isoform of eukaryotic elongation factor 1A. Mechanistically it is the closest held-out analog to the represented elongation factor `Eef2`: eEF1A delivers aminoacyl-tRNAs to the A site of the ribosome, while eEF2 catalyzes ribosomal translocation during elongation. External mouse genetics argue that loss of `Eef1a2` is not benign in postnatal neurons. `Eef1a2` is reciprocal with `Eef1a1`; eEF1A2 takes over after birth; and homozygous wasted mice, in which `Eef1a2` is abolished, develop tremor, motor-neuron degeneration, muscle wasting, and death around weaning. The Perturb-seq experiment perturbed at P16 and harvested at P37-P44, after the reported developmental switch, so the broad developmental timing favors a detectable neuronal consequence rather than a redundant embryonic isoform masking the hit completely.

The training data nevertheless argue against assigning `Eef1a2` a large Tsc2-, Uba5-, or spliceosome-scale response. `Eef2`, the only focal training perturbation in the elongation core, produced only 9 FDR<0.05 genes in `151 TH Prkcd Grin2c Glut`, and the Distributed Agents corpus found it did not converge with the represented initiation factors or mTORC1-coupled regulators. The initiation arm itself was almost silent in the focal cells: `Eif5a` and `Eif2ak4` had 0 DEGs, `Eif4g1` and `Eif4h` had 1, and `Eif4a2` had 2. `Mtor` and `Rptor` were similarly weak or null despite their canonical protein-synthesis role. `Tsc2` is a counterexample with 86 DEGs, but its signature was a derepressed mTORC1/sterol/lysosomal feedback state that is not the expected direction for direct loss of an elongation factor.

I therefore called `Eef1a2` nonzero, because mature thalamic neurons should depend on the Eef1a2 isoform at this age and complete biallelic loss in recovered cells is plausibly sensed. I kept the count in the weak class rather than the medium class because partial mosaic acute CRISPR loss is milder than germline homozygous wasted loss; heterozygous `wst/+` mice tolerate reduced eEF1A2; no direct EF1 paralog or EF1B exchange-factor knockout is represented in the focal training set; and the observed training perturbations show that disrupting cytoplasmic translation machinery usually did not yield a shared broad nuclear RNA response in this assay.

Point prediction: **7 DEGs**.

## Limits of the prediction

- The most direct paralog and complex comparators, `Eef1a1`, `Eef1b2`, `Eef1d`, `Eef1g`, and `Vars1`, were not in the focal training-count table, so the prediction extrapolates from `Eef2` and translation-initiation counterexamples instead of an EF1-complex series.
- Wasted-mouse phenotypes are germline, homozygous, organism-level null phenotypes enriched for lower motor neuron and muscle readouts; the assay here is sparse AAV CRISPR loss in recovered NeuN+ brain nuclei and the focal class is thalamic glutamatergic, not spinal motor neurons.
- The held-out `Eef1a2` profile has no recovered perturbed-nucleus count in the provided data. The true FDR count will be power-sensitive, and several training targets with convincing biology had only weak or null signatures when recovered nuclei were sparse.
- I did not infer editing success from target mRNA loss. Same-experiment `Eef2` reached many downstream DEGs despite FDR=1.0 for its own transcript in all measured groups, and the dataset notes that self-knockdown is not a reliable quantitative proxy for functional editing.
