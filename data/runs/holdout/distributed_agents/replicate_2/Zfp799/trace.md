# Held-out perturbation

## Question and interpretation

The requested target list for this run contained one held-out perturbation:

```tsv
target_name
Zfp799
```

I interpreted the requested endpoint as the exact `151 TH Prkcd Grin2c Glut` count of measured coding genes with `pvals_adj < 0.05`, where `pvals_adj` is the Benjamini-Hochberg-adjusted Wilcoxon p-value in the Perturb-seq differential-expression table. `Zfp799` is absent from both the focal-cell training count CSV and the full non-held-out DE parquet as a perturbation target, so no Zfp799 signature or count was used directly.

I treated `151 TH Prkcd Grin2c Glut` as the Allen thalamic glutamatergic group from the supplied dataset context, not as a dopaminergic or tyrosine-hydroxylase label. I also treated the endpoint as an assay-specific response-breadth count after acute mosaic AAV-CRISPR perturbation in postmitotic juvenile neurons, not as a measure of essentiality or embryonic knockout phenotype.

## Sources

Dataset-local sources:

- `training_de_all_cell_groups.parquet`, using `group_name == "151 TH Prkcd Grin2c Glut"` for mechanistic comparators.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, the observed `n_degs` endpoint for 1,674 non-held-out perturbations.
- Distributed Agents same-experiment corpus release `perturbai-july-260713-sourceguard-1773-v1`, especially KRAB/SCAN/C2H2 zinc-finger claims and Setdb1/KRAB-adjacent findings.
- Distributed Agents run-local `profile_compare` / `profile_cohort` over focal-cell log2 fold-change profiles for nominated zinc-finger and chromatin perturbations.
- Run-local dataset context for the experimental design and DEG-count calibration.

External sources:

- NCBI Gene, GeneID `240064`, updated 2026-09-10; MGI marker `MGI:2443934`; Ensembl `ENSMUSG00000095253`; UniProtKB unreviewed entries including `Q8BHK4`; and InterPro protein annotation for `Q8BHK4`.
- PubMed searches for Zfp799/ZNF799 and KRAB-ZFP biology. I found no Zfp799-specific mouse neuronal publication; PubMed hits for `ZNF799` were unrelated string matches or non-orthologous zinc-finger genes.
- Frietze et al. 2010, DOI `10.1371/journal.pone.0015082`, PMID `21170338`, for the KRAB-ZNF/KAP1/SETDB1 recruitment model at sequence-specific genomic sites.
- Tie et al. 2018, DOI `10.15252/embr.201745000`, PMID `30061100`, for KAP1/TRIM28-dependent repression of endogenous retroviruses and ZNF genes through KRAB zinc-finger proteins in differentiated human cells.

## Computational checks

1. I read the manifest and confirmed that it contains exactly `Zfp799`.

2. I summarized the training endpoint distribution for the focal cell group. The 1,674 training perturbations are extremely sparse: 1,205 have `n_degs = 0`; the median is 0; the 75th percentile is 1; the 90th percentile is 2; the 95th percentile is 18; and a small set of outliers such as `Uba5`, `Tpr`, `Sin3a`, and `Rnpc3` account for counts in the hundreds or thousands.

3. I enumerated represented `Zfp*`, `Zkscan*`, and `Zscan*` targets from the focal training counts:

```tsv
target_name	n_degs
Zfp1	0
Zfp106	0
Zfp148	8
Zfp160	0
Zfp182	0
Zfp236	19
Zfp266	0
Zfp280c	0
Zfp280d	0
Zfp292	0
Zfp322a	0
Zfp341	0
Zfp397	0
Zfp423	150
Zfp451	0
Zfp462	0
Zfp521	0
Zfp536	0
Zfp609	0
Zfp612	1
Zfp644	0
Zfp654	0
Zfp664	0
Zfp692	1
Zfp804a	0
Zfp846	0
Zfp949	0
Zfp950	0
Zfp961	0
Zfpm2	0
Zkscan1	0
Zkscan16	0
Zscan26	0
```

The simple symbol prefix is not the biology: some zinc-finger transcription factors such as `Zfp423` are developmental transcription factors and were treated as counterexamples, not primary analogs. The KRAB/SCAN/C2H2 factors named by the same-experiment corpus were the closer analog set.

4. I used the parquet metadata to restrict raw DE reads to the 35 row groups containing `151 TH Prkcd Grin2c Glut`, then pulled focal signatures for the nominated same-family and H3K9/chromatin comparators. In that focal cell group, the most relevant observed counts were:

```tsv
target_name	n_degs	n_pert_matched	leading_FDR_genes
Zfp1	0	194	none; all adjusted p-values 1.0 among the strongest positive log2FC rows
Zfp397	0	147	none; all adjusted p-values 1.0 among the strongest positive log2FC rows
Zfp612	1	252	Notum up, log2FC 1.014, FDR 1.56e-7
Zfp664	0	222	none; all adjusted p-values 1.0 among the strongest positive log2FC rows
Zfp846	0	183	no FDR<0.05 genes; the smallest FDR was 0.500 for Zbtb18
Zfp950	0	202	no FDR<0.05 genes; the smallest FDR was 0.949
Zkscan1	0	180	none; all adjusted p-values 1.0 among the strongest positive log2FC rows
Zkscan16	0	247	none; all adjusted p-values 1.0 among the strongest positive log2FC rows
Zscan26	0	246	none; all adjusted p-values 1.0 among the strongest positive log2FC rows
Setdb1	22	113	Tasor, Ccdc84, Pmvk, Atf7ip, Abhd12b, Nin, Pcdhga8 among the leading FDR genes
Smchd1	0	152	no FDR<0.05 genes; smallest FDRs were Acox1 0.181 and Vwa8 0.350
Champ1	0	194	none
Dcaf8	0	165	none
Dnmt3a	0	209	no FDR<0.05 genes; smallest FDRs were Dnmt3a/Fbxl17 0.173
Mecp2	16	167	Nap1l5, Ache, Focad, Tnr, Ptprm among the leading FDR genes
Chd4	100	163	Begain, Cpne7, Zfp467, Ramp3, Pygm among the leading FDR genes
```

5. I compared full focal log2 fold-change vectors for `Zfp1`, `Zfp397`, `Zfp612`, `Zfp664`, `Zfp846`, `Zfp950`, `Zkscan1`, `Zkscan16`, `Zscan26`, `Setdb1`, `Smchd1`, `Champ1`, `Dcaf8`, `Dnmt3a`, `Mecp2`, and `Chd4`. The activity summary was four non-flat profiles out of sixteen: `Chd4` had at least 50 significant features, `Setdb1` and `Mecp2` had 10-49, `Zfp612` had 1-9, and the other twelve nominated perturbations had no significant feature. Top-tail overlap among the KRAB/SCAN/C2H2 factors was weak and mostly involved non-significant tails rather than shared FDR-level genes, so the individual ZFP perturbations did not support a transferable positive DEG count.

## Biological reasoning for Zfp799

`Zfp799` is a protein-coding mouse gene on chromosome 17 with official MGI marker `MGI:2443934` and Ensembl gene `ENSMUSG00000095253`. NCBI Gene/Alliance predict nuclear DNA-binding, RNA-polymerase-II transcription-factor activity. UniProtKB has only unreviewed proteins for the gene, but InterPro annotates the 648-aa Q8BHK4 isoform with a KRAB domain at the N terminus and 16 C2H2 zinc-finger domains across the C-terminal half. Mechanistically, KRAB-ZFP proteins often bind sequence-specific DNA through their C2H2 arrays and can recruit KAP1/TRIM28, which in turn nucleates SETDB1/H3K9me3 repressive chromatin; ZNF274 is an example of such a locus-specific KRAB factor recruiting KAP1 and SETDB1 (Frietze et al. 2010), and the KAP1/KRAB-ZNF axis can repress endogenous retroviral elements in differentiated human cells (Tie et al. 2018).

That general KRAB biology argued for checking, but not simply copying, `Setdb1`. The same-experiment corpus explicitly warns that the Setdb1-sensitive neuronal response was not a generic KRAB-ZFP output in this screen:

- Claim `ec2ff963b6ed7e22bcb3`: represented SCAN/C2H2/KRAB-associated zinc-finger perturbations did not define an interchangeable shared neuronal transcriptomic regulon.
- Claim `340c7e3bcac13675d574`: individual KRAB/C2H2 perturbations `Zfp1`, `Zfp950`, and `Zfp846` were not rate-limiting for the Setdb1-sensitive neuronal repressive transcriptomic response.
- Claim `68384b3b4cce631738fa`: the Setdb1-sensitive protocadherin/Atf7ip/Tasor response was detectable but was not reproduced by assayed KRAB-ZFPs, `Smchd1`, `Dnmt3a`, `Dcaf8` relatives, or `Champ1` heterochromatin relatives.

The focal-cell counts matched those claims. `Setdb1` itself was detectable but modest in this endpoint, with 22 DEGs in `151 TH Prkcd Grin2c Glut` and leading up-regulation of `Tasor`, `Atf7ip`, and gamma-protocadherin-associated genes. None of the closest assayed KRAB/SCAN/C2H2 comparators reproduced that: `Zfp1`, `Zfp397`, `Zfp664`, `Zfp846`, `Zfp950`, `Zkscan1`, `Zkscan16`, and `Zscan26` were all exact zeros, and `Zfp612` had one isolated DEG (`Notum`) rather than a broad repressive-chromatin module. I therefore treated the detectable `Setdb1`, `Mecp2`, and `Chd4` signatures as proof that this cell type had power to show some chromatin-factor effects, but the same-family KRAB-ZFP data as the more specific calibration for an uncharacterized KRAB-ZFP.

`Zfp799` has no direct same-experiment corpus finding, no PubMed evidence tying it to a postnatal neuronal gene program, and no external annotation pointing to a known thalamic or neurotransmission-specific effector module. The most parsimonious transfer is that an acute sparse knockout of this single KRAB-ZFP will, like most assayed KRAB/SCAN/C2H2 zinc-finger targets, leave no measured coding gene below FDR 0.05 in the recovered `151 TH Prkcd Grin2c Glut` nuclei. I predict a true zero rather than a one-gene weak response because eight of the nine closest represented KRAB/SCAN/C2H2 analogs had exactly zero focal DEGs, the lone one-gene response was idiosyncratic, and `Zfp799` lacks target-specific evidence that would push it into the small nonzero tail.

**Prediction:** `Zfp799 -> 0`

## Limits and uncertainty

The prediction is an extrapolation from domain architecture and from other individual KRAB/SCAN/C2H2 factors, not from a Zfp799 binding map. KRAB-ZFP proteins are highly sequence-specific, and the genome contains many repeats and poorly annotated loci that are not measured or not well powered in this coding-gene Wilcoxon endpoint. `Trim28/Kap1`, `Atf7ip`, and `Tasor` were not available as focal training perturbations here, so I could not directly test loss of the core KRAB-H3K9 machinery. Finally, a narrow Zfp799-specific target in thalamic neurons could cross FDR in the held-out data, but the supplied same-experiment evidence makes a broad Setdb1-like or Chd4-like response unlikely.
