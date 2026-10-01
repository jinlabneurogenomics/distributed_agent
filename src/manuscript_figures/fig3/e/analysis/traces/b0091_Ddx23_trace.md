# Held-out DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and endpoint

I predicted the held-out endpoint `n_degs` for each requested genetic perturbation in `151 TH Prkcd Grin2c Glut` neurons. The endpoint is the integer count of measured genes with `pvals_adj < 0.05` in the focal cell group after acute P16 AAV-PHP.eB CRISPR-Cas9 loss of function, sampled 3-4 weeks later by snRNA-seq. The only requested held-out target in this run was `Ddx23`.

I treated the training focal-cell CSV as the direct endpoint for visible perturbations and the parquet as direct evidence for the focal expression signatures of those visible perturbations. `Ddx23` itself was held out from both supplied files, so its point estimate is an extrapolation from biologically matched visible perturbations. The same-experiment July PerturbAI Findings/Reports corpus was used only as a packaged interpretation of this experiment, not as an independent replicate. External literature was used to identify what DDX23 does and which visible training perturbations were close enough to transfer from.

## Sources

- Direct endpoint table: `/gpfs/group/jin/asun/bioagents/debug/260901_predict/holdout_task/Inputs/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Direct differential-expression table: `/gpfs/group/jin/asun/bioagents/debug/260901_predict/holdout_task/Inputs/training_de_all_cell_groups.parquet`.
- Requested targets: `/gpfs/group/jin/asun/bioagents/runs/holdout-prediction/july-260713-adaptive-seed-260901/prepared/manifests/deg-count/bs001/b0091.csv`.
- Internal same-experiment corpus: `perturbai-july-260713-sourceguard-1773-v1` Findings/Reports, including packaged `Prpf6`, `Snrnp70`, `U2af2`, `Cdc40`, `Rnpc3`, `Thoc1`, `Tpr`, and `Ddx39b` interpretations.
- External literature from PubMed:
  - Teigelkamp et al. 1997, PMID 9409622: identified human U5-100K/DDX23 as an RS-domain U5 snRNP DEAD-box protein homologous to yeast Prp28.
  - Mathew et al. 2008, DOI 10.1038/nsmb.1415, PMID 18425142: showed phosphorylation-dependent PRP28/DDX23 association with the U4/U6.U5 tri-snRNP and requirement for stable B-complex assembly.
  - Mohlmann et al. 2014, DOI 10.1107/S1399004714006439, PMID 24914973, and Boesler et al. 2016, DOI 10.1038/ncomms11997, PMID 27377154: connected human PRP28 ATPase activity to the pre-B to B transition, U1/5-prime-splice-site release, and stable tri-snRNP binding.
  - Zhan et al. 2018, DOI 10.1038/s41422-018-0094-7, PMID 30315277, and Charenton et al. 2019, DOI 10.1126/science.aax3289, PMID 30975767: structurally placed Prp28 at the human pre-B/B transition where the 5-prime splice site is transferred from U1 to U6 during spliceosome activation.
  - Segovia et al. 2024, DOI 10.1073/pnas.2322974121, PMID 38743621: found a direct SRSF1-DDX23 interaction and supported the importance of DDX23's N-terminal RS-like region for spliceosome incorporation.
  - Makarov et al. 2000, DOI 10.1006/jmbi.2000.3685, PMID 10788320: established PRPF6 as the human U5-102K homolog that bridges U5 with U4/U6 during tri-snRNP formation.
  - Kondo et al. 2015, DOI 10.7554/eLife.04986, PMID 25555158; Kaida et al. 2010, DOI 10.1038/nature09479, PMID 20881964; Berg et al. 2012, DOI 10.1016/j.cell.2012.05.029, PMID 22770214: established U1/SNRNP70 as a 5-prime-splice-site snRNP component and a regulator of premature cleavage/polyadenylation.
  - Wilkinson et al. 2019, DOI 10.1146/annurev-biochem-091719-064225, PMID 31794245: review of U1/U2 recruitment, U4/U6.U5 tri-snRNP joining, and spliceosome activation.

## Dataset calculations

From the focal training-count CSV, 469 of 1,674 visible biological targets were nonzero; the median count was 0 and the 99th percentile was 436.5. `Ddx23` is therefore not assumed to be nonzero just because it is an essential RNA-processing gene.

I queried the parquet for `151 TH Prkcd Grin2c Glut` rows of spliceosome and RNA-processing perturbations represented in the training universe. I used the count CSV to obtain the exact FDR<0.05 endpoint and the parquet rows to inspect top focal DE genes, matched perturbed nuclei, and same-direction log-fold-change overlap between related visible perturbations.

Relevant focal training counts were:

| Training perturbation | n_degs at FDR<0.05 in 151 | n_pert_matched in parquet | Interpretation for Ddx23 |
| --- | ---: | ---: | --- |
| `Prpf6` | 454 | 72 | Closest visible same-particle analog. PRPF6/U5-102K is a U5 snRNP scaffold bridging U5 to U4/U6, and loss in the corpus induced RNA-processing, proteostasis, and synaptic down-shift modules. |
| `Snrnp70` | 213 | 135 | Mechanistically connected 5-prime-splice-site/U1 comparator. DDX23/PRP28 promotes release of U1 from the 5-prime splice site, but SNRNP70 is not a U5 tri-snRNP subunit. |
| `Cdc40` | 624 | 159 | Strong, later spliceosome comparator that converged with `Prpf6`, `U2af2`, and `Snrnp70` in the same-experiment corpus. |
| `U2af2` | 828 | 222 | Strong 3-prime-splice-site comparator that shared many same-direction `Prpf6` and `Snrnp70` focal genes but acts earlier/differently from U5/PRP28. |
| `Rnpc3` | 868 | 149 | Minor-spliceosome comparator with a very broad focal effect; useful evidence that spliceosome perturbations can be large, but U12 machinery is not a direct DDX23 analog. |
| `Thoc1` | 303 | 121 | mRNA-export/TREX comparator; shares RNA-biogenesis stress output but not spliceosome assembly chemistry. |
| `Tpr` | 1768 | 114 | High-end nuclear-basket/export/proteostasis counterpoint; too indirect and much larger than direct U5/U1 analogs, so it was not used as the center of the estimate. |
| `Ddx39b` | 0 | 48 | DEAD-box helicase and TREX/splicing counterexample; it was silent in this focal cell group, showing that the RNA-helicase label alone is not predictive. |
| `Ddx3x` | 8 | 138 | Neurodevelopmental DEAD-box counterexample with a very small focal signature. |
| `Snrpb` | 0 | 179 | Sm-core snRNP counterexample; same broad snRNP membership was insufficient to phenocopy `Snrnp70` in the internal corpus. |

Expression-pattern checks in the focal class were consistent with a shared but not identical RNA-biogenesis state. On the union of FDR<0.05 genes across selected RNA-processing perturbations, signed log-fold-change correlations were positive for `Prpf6` versus `Snrnp70` and `U2af2`:

- `Prpf6` versus `Snrnp70`: Pearson 0.434, cosine 0.439, 46 genes significant in both and 45/46 in the same direction. Shared genes included `Gtf2f1`, `Cherp`, `Rsrp1`, `Snhg11`, and `Snrnp70`.
- `Prpf6` versus `U2af2`: Pearson 0.424, cosine 0.429, 121 genes significant in both and 113/121 in the same direction. Shared genes included `Rsrp1`, `Nprl2`, `Pcsk2`, `Gtf2f1`, `Ddx41`, `Wsb1`, `Snhg11`, and `Agrn`.
- `Snrnp70` versus `U2af2`: Pearson 0.422, cosine 0.438, 76 genes significant in both and 68/76 in the same direction.

In contrast, `Ddx39b` and `Snrpb` had 0 focal FDR<0.05 DEGs and shared no significant focal genes with `Prpf6`, `Snrnp70`, or `U2af2`. `Ddx23` is closer to `Prpf6` than to either of those negative controls because it is a U5/tri-snRNP PRP factor, not just a generic DEAD-box or generic Sm-core component.

## Target-specific reasoning

### `Ddx23`

The intervention is acute Cas9 loss of `Ddx23`, a mouse ortholog of human PRP28/U5-100K. The direct molecular consequence should be reduced PRP28 function in the U5/tri-snRNP spliceosome assembly pathway. PRP28 acts when the U4/U6.U5 tri-snRNP joins the U1/U2-bound pre-spliceosome, promoting U1 release and transfer of the 5-prime splice site to U6; ATPase-defective PRP28 stalls a pre-B-like intermediate. The primary molecular phenotype is therefore expected to be impaired spliceosome activation, not necessarily a simple change in steady-state `Ddx23` nuclear RNA.

The most appropriate same-experiment transfer is `Prpf6`: both perturbations impair the limiting U5/tri-snRNP machinery in the same direction. The `Prpf6` knockout produced 454 DEGs at FDR<0.05 in the requested focal class, and the packaged July report showed that its broader FDR<0.10 response repeatedly induced RNA-processing genes, proteostasis genes, and a p53-like branch while reducing mature synaptic/ion-handling transcripts. Since DDX23 acts in the same complex and at the U1-to-U6 handoff, the expected propagation is `Ddx23` loss -> defective U5/tri-snRNP spliceosome assembly -> secondary RNA-processing/proteostasis stress in recovered thalamic glutamatergic neurons -> hundreds of whole-gene abundance changes. This supports a nonzero count of the same order as `Prpf6`.

`Snrnp70`, `Cdc40`, `U2af2`, and `Rnpc3` keep the estimate nonzero. They are not same-complex DDX23 analogs, but they perturb connected spliceosome entry or catalytic pathways and were visible in the same focal group with 213, 624, 828, and 868 DEGs. The internal corpus independently found that `Prpf6`, `U2af2`, `Snrnp70`, and `Cdc40` converged with one another in the same thalamic and midbrain groups, validating that several spliceosome lesions collapse onto a common postmitotic response.

I did not copy the highest counts. `Tpr` at 1,768 and the proteasome perturbations `Psmb4`/`Psmc1` at 742/430 shared secondary stress signatures with spliceosome perturbations, but they start from different direct molecular lesions. `Rnpc3` and `U2af2` were broader than `Prpf6` in this focal group and have distinct splice-site or minor-spliceosome biology. `Snrpb`, the only represented Sm-core snRNP subunit near the U1 query set, had 0 DEGs, and `Ddx39b` had 0 despite belonging to mRNP export/RNA-helicase biology. Those negative comparators argue against treating DDX23 as automatically equivalent to every large RNA-processing target.

I therefore predicted a broad, clearly nonzero response, slightly below the observed `Prpf6` count but above `Snrnp70` and `Thoc1`. The point estimate is 380 DEGs. It is driven primarily by within-dataset `Prpf6`/`Snrnp70`/`Cdc40`/`U2af2` evidence and externally by DDX23's assignment to the PRP28 U5/tri-snRNP activation step.

## Limits

The prediction is uncertain because no direct `Ddx23` rows, splice-junction counts, intron-retention measures, DNA-indel calls, or PRP28 protein measurements are present in the supplied inputs. The closest visible U5 targets `Prpf8`, `Snrnp200`, `Eftud2`, `Prpf3`, `Prpf4`, and `Prpf31` were absent from the training perturbation universe, leaving `Prpf6` as a single close structural analog. The visible endpoints are also power-sensitive: `Prpf6` had only 72 focal perturbed nuclei, while some broader comparators had more. Finally, the parquet and the July corpus are derived from the same PerturbAI experiment; agreement between them strengthens interpretation of that experiment but is not independent replication.
