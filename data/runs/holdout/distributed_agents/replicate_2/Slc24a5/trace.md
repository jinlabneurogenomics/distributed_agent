# Slc24a5 DEG-count prediction

## Question and resolved ambiguities

The held-out manifest contains one requested perturbation:

| target_name |
| --- |
| Slc24a5 |

I interpreted the requested endpoint as the number of measured genes with `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` focal cell group after acute AAV CRISPR loss of `Slc24a5`. The value to predict is therefore an assay-calibrated focal-cell DEG count, not an estimate of editing rate, viability, developmental importance, or raw effect size.

I kept `Slc24a5` as held out. It is absent from the training-count CSV and from the differential-expression parquet as a `gene_target`, so all same-experiment evidence below comes from other perturbations.

## Sources used

Same-experiment data:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- `[local file: training_de_all_cell_groups.parquet]`
- `[local file: 211_Slc24a5.csv]`
- Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`, queried with `target_context`; this release had no `Slc24a5` Claim, Finding, or explicit target reference, so it did not supply a curated comparator.
- Distributed Agents runtime `profile_compare`, run over focal-cell log fold changes for selected training comparators.

External biological evidence:

- PubMed literature searches for `SLC24A5`, `NCKX5`, melanosomes, pigmentation, and oculocutaneous albinism.
- Lamason et al. 2005, Science, PMID: 16357253, DOI: 10.1126/science.1116238: zebrafish golden encodes `slc24a5`/NCKX5, an intracellular putative cation exchanger required for pigmentation, and the human ortholog is a major pigmentation gene.
- Wei et al. 2013, Journal of Investigative Dermatology, PMID: 23364476, DOI: 10.1038/jid.2013.49: biallelic `SLC24A5` variants cause nonsyndromic OCA6 with immature melanosomes, supporting a melanogenesis/melanosome-maturation role.
- Morice-Picard et al. 2013, Journal of Investigative Dermatology, PMID: 23985994, DOI: 10.1038/jid.2013.360: additional human `SLC24A5` mutations associated with nonsyndromic oculocutaneous albinism.
- Zhang et al. 2019, Journal of Cell Science, PMID: 31201282, DOI: 10.1242/jcs.232009: loss of NCKX5 reduces melanosomal Ca2+ enrichment, PMEL fibril formation, melanosome maturation, and pigment production.
- Lytton 2007, Biochemical Journal, PMID: 17716241, DOI: 10.1042/BJ20070619: review of the SLC8 NCX, SLC24 NCKX, and NCLX exchanger families; the canonical neuronal exchangers are primarily NCKX2/NCKX3/NCKX4 and NCX family members, while NCKX5 is linked to skin, retinal epithelium, and pigmentation.

## Same-experiment computations

I used the training-count CSV to calibrate the focal endpoint distribution:

- 1,674 non-held-out biological targets are present.
- 1,205 / 1,674 have `n_degs = 0`.
- Median `n_degs` is 0.
- The 75th percentile is 1.
- The mean is 14.1 because a small number of large perturbations, such as `Uba5` with 2,677 DEGs and `Tpr` with 1,768 DEGs, create a long right tail.

This zero-inflated calibration makes it important to require a specific mechanistic reason before predicting a positive count for an off-context target.

I searched the training targets for SLC24/SLC8 paralogs and pigmentation genes. No exact `Slc24*` target, no `Slc8*` target, and no `Tyr`, `Oca`, `Pmel`, `Mlana`, or `Mitf` target were present in the focal training-count file. The observed nearby training set therefore consisted of less direct pigment-lineage controls and organellar/ion-transporter controls: `Kit`, `Sox10`, `Trpm3`, `Trpm7`, `Slc9a7`, `Slc9a9`, `Slc12a2`, and `Slc6a17`.

For those candidates I filtered the DE parquet to:

```python
(group_name == "151 TH Prkcd Grin2c Glut") &
gene_target.isin(["Kit", "Sox10", "Trpm3", "Trpm7",
                  "Slc9a7", "Slc9a9", "Slc12a2", "Slc6a17",
                  "Slc7a6os"])
```

and counted `pvals_adj < 0.05` over the 17,259 measured genes per perturbation. The computed counts matched the supplied `n_degs` endpoint.

I also compared the complete signed focal profiles for eight selected analogs with Distributed Agents `profile_compare` using `logfoldchanges` as the signed value and `pvals_adj < 0.05` as the significance threshold. Six of the eight selected profiles had `no_significant_features`; `Slc9a7` and `Slc6a17` had only 1 and 4 significant features, respectively. The profile comparison did not reveal a broader recurrent melanosome or Ca2+-exchange transcriptional module in this cell group.

## Target-specific reasoning

### Slc24a5

Point prediction: **0 DEGs**

`Slc24a5` encodes NCKX5, a K+-dependent Na+/Ca2+ exchanger whose best-established biology is pigmentation: zebrafish `slc24a5` is the golden locus, the human ortholog is a major skin-pigmentation gene, and loss-of-function alleles cause OCA6 by disrupting melanosome maturation and melanin production. That function is in melanocytes and retinal pigment epithelium, not in postmitotic thalamic glutamatergic neurons recovered from NeuN-enriched whole brain. Although NCKX5 belongs to the wider CaCA exchanger family, its mechanism is much less compelling here than loss of known neuronal exchangers such as NCKX2/NCKX3/NCKX4 or NCX family members.

The closest focal training perturbations argue for a null or at most self-only response:

| training perturbation | `n_degs` in `151 TH Prkcd Grin2c Glut` | why it was checked | expression-pattern evidence |
| --- | ---: | --- | --- |
| `Kit` | 0 | melanocyte/neural-crest receptor tyrosine kinase pathway, useful as an off-context pigmentation-lineage comparator | no significant genes; best adjusted p value 0.861 |
| `Sox10` | 0 | glial/neural-crest transcription factor important for melanocyte lineage | no significant genes; best adjusted p value 1.0 |
| `Trpm3` | 0 | cation channel with Ca2+ permeability, not a melanosomal exchanger but a cation-transport stress comparator | no significant genes; best adjusted p value 0.146 |
| `Trpm7` | 0 | broad divalent-cation channel/kinase comparator | no significant genes; best adjusted p value 1.0 |
| `Slc9a7` | 1 | intracellular Na+/H+ exchanger, a weak organellar-pH transporter analog | only the self transcript `Slc9a7` was significant, with log2FC -0.693 and adjusted p value 4.98e-05 |
| `Slc9a9` | 0 | endosomal Na+/H+ exchanger, included to test whether organellar ion exchange itself is activating in this cell group | no significant genes; best adjusted p value 1.0 |
| `Slc12a2` | 0 | neuronal Na/K/Cl ion transporter counterexample for a broadly expressed transporter | no significant genes; best adjusted p value 1.0 |
| `Slc6a17` | 4 | synaptic vesicle neutral amino-acid transporter; a neuronally relevant SLC transporter counterexample | sparse signature: `Slc6a17`, `Jun`, `Stmn4`, and `Kctd16` were significant |
| `Slc7a6os` | 73 | non-analog SLC-named counterexample showing that a shared SLC prefix is not sufficient for pooling | 73 DEGs, with leading genes such as `Snhg11`, `Ptpn3`, and `Ccdc136`; mechanistically too distant from NCKX5 to transfer |

The `Kit` and `Sox10` rows are important because they probe whether a melanocyte/neural-crest program accidentally maps onto this postnatal thalamic glutamatergic DE endpoint. It does not: both are complete nulls. The cation-transporter rows then test the other possible transfer route, ion homeostasis. Those are also quiet in this cell group except for self-target loss in `Slc9a7` and a four-gene `Slc6a17` footprint. Because the training set lacks true SLC24 paralogs, I down-weighted the SLC family label and did not use `Slc7a6os` as a positive analog.

The external mechanism pushes in the same direction. `Slc24a5` loss perturbs melanosome Ca2+ handling, PMEL fibrillogenesis, melanin deposition, and RPE/melanocyte pigmentation; the focal nuclei are NeuN-positive postmitotic neurons from whole brain excluding hindbrain and olfactory bulb. The most likely outcome of acutely knocking out this pigmentation transporter in `151 TH Prkcd Grin2c Glut` cells is therefore no gene reaching FDR 0.05. I set the integer point estimate to zero, rather than one to four, because the one-to-four DEG comparators were either dominated by self-transcript loss or by a different vesicle transporter with a clearer neuronal role.

## Limits and extrapolation

- There is no direct same-experiment `Slc24a5` expression profile and no observed SLC24 paralog profile in the focal training set, so the prediction necessarily extrapolates from pathway and cell-context evidence.
- The Distributed Agents corpus release had no curated `Slc24a5` target card or Finding, leaving the biological grounding to the raw DE tables plus external PubMed literature.
- `Kit` and `Sox10` are pigmentation-lineage controls rather than melanosome ion exchangers; `Slc9a7`, `Slc9a9`, `Slc12a2`, `Trpm3`, `Trpm7`, and `Slc6a17` are ion/transport controls rather than true NCKX5 paralogs.
- A zero prediction only means no measured gene is expected to pass the Scanpy Wilcoxon BH threshold in recovered focal nuclei. It does not assert absent editing, absent protein disruption, or no subthreshold biology.
- The assay is sparse, mosaic, survivor-conditioned, and strongly cell-type/power dependent. A melanocyte or retinal-pigment-epithelium perturbation would not be expected to transfer quantitatively into a NeuN-enriched thalamic neuronal readout.
