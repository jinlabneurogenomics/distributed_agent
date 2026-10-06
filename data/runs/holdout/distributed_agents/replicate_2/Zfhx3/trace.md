# Zfhx3 prediction trace

## Question and resolved ambiguities

The requested held-out perturbation file contains one target, `Zfhx3`. The task is to predict the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` after `Zfhx3` perturbation in `151 TH Prkcd Grin2c Glut` cells; I treated this as the assay-defined integer endpoint in the supplied training CSV, not as a generic measure of gene essentiality or of how much target RNA was knocked down. Self-DE of the targeted transcript would count if it crossed FDR 0.05, but failure of the target transcript to cross FDR was not interpreted as failed editing because the experiment reports only modest average mRNA down-regulation per gRNA.

The exact focal label used in the parquet and endpoint CSV is `151 TH Prkcd Grin2c Glut`. `Zfhx3` was not present as an observed perturbation in either input, so all focal evidence below is transferred from other training perturbations.

## Sources used

- `training_de_all_cell_groups.parquet`: per-gene signed log2 fold changes and adjusted Wilcoxon p-values for all non-held-out perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed `151` DEG counts for the 1,674 training perturbations.
- `267_Zfhx3.csv`: the held-out manifest.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`: same-experiment claims and target-centered reports. `target_context` returned no direct `Zfhx3` finding or claim in this release, so I used it for assayed paralogs, BAF/mSWI/SNF members, TALE/homeobox comparators, and circadian comparators.
- Distributed Agents runtime profile tools: focal-cell log-fold-change comparisons among candidate observed perturbations and to the 1,674-member eligible training universe.
- PubMed for external biology:
  - Perez Baca et al. 2024, DOI `10.1016/j.ajhg.2024.01.013`, showed human ZFHX3 loss of function causes syndromic intellectual disability, ZFHX3 accumulates during neuronal differentiation, binds promoters of nervous-system development genes, and interacts with BRG1/BRM-associated factor and cleavage/polyadenylation complexes.
  - Parsons et al. 2015, DOI `10.1016/j.cell.2015.06.060`, identified the mouse `Zfhx3` short-circuit mutation as an SCN transcriptional defect that alters circadian neuropeptide outputs through AT-motif regulation with little effect on core clock genes.
  - Wilcox et al. 2017, DOI `10.1177/0748730417722631`, used inducible adult mouse knockout to show an ongoing requirement for `Zfhx3` in SCN circadian rhythmicity.
  - Zhang et al. 2019, DOI `10.1016/j.expneurol.2019.113055`, showed `Zfhx3` is required during embryonic/perinatal late-born D1 medium-spiny-neuron differentiation and survival.
  - Hughes et al. 2021, DOI `10.1096/fj.202100563R`, showed the `Zfhx3` short-circuit allele also affects retinal light responsiveness.

## Computational checks

I first inspected the training endpoint distribution in `151`. It is very sparse: 1,205 of 1,674 training perturbations have `n_degs = 0`; the median is 0, the 75th percentile is 1, and only the top 5% exceed 18 DEGs. The focal cell type is therefore capable of very large responses, but the prior for an arbitrary perturbation is zero or singleton.

To avoid scanning the whole 8.3 GB parquet, I read parquet row-group statistics for `group_name`, found the row groups spanning `151 TH Prkcd Grin2c Glut` (`546` through `580`), and then pulled only `names`, `gene_target`, `logfoldchanges`, and `pvals_adj` for the candidate comparators. I counted `pvals_adj < 0.05` in that slice and compared these counts with the endpoint CSV. This gave exact focal counts and top focal genes for ZFHX-family, BAF/mSWI/SNF, homeobox/TALE, and circadian candidates.

I also ran `profile_compare` over a 20-perturbation candidate cohort in the `151` context with `logfoldchanges` as the signed profile value and `pvals_adj < 0.05` as the significance call. The cohort contained `Zfhx2`, `Meis1`, `Meis2`, `Pbx1`, `Pbx3`, `Pknox2`, ten BAF/mSWI/SNF-related targets, and `Bmal1`/`Nr1d1`/`Clock`/`Cry2`. Nine of these 20 biologically selected nodes had no significant focal feature at all, only four had at least 50, and the Distributed Agents topology split the cohort into BAF, circadian, and TALE/homeobox components with `Zfhx2` isolated. That supports treating each biological lane separately instead of pooling all transcription or chromatin regulators into one average.

## Held-out target reasoning

### Zfhx3

**Closest within-dataset paralog and family evidence.** The closest assayed family member was `Zfhx2`, and it had `0` DEGs in `151`; its own transcript had `log2FC = -0.064`, `p_adj = 1.0`. The Distributed Agents same-experiment context for `Zfhx2` describes a central-brain null or near-null: the only curated positive event was one weak `Nt5c3` hit in `009 L2-3 IT PIR AON ENT Glut`, while expected nociceptor biology was absent from sampled central neurons and the global score-neighbor search found only near-zero relationships. The corpus also found no `Zfhx3` mRNA rebound after `Zfhx2` loss, so the ZFHX-family evidence points to sparse or absent postnatal central-neuron RNA consequences rather than a broad acute regulon.

**Homeobox/developmental-transcription-factor counterexamples.** `Zfhx3` is a zinc-finger homeobox transcription factor, so I compared it with observed TALE/homeobox and HOX cofactors that should be active if this assay commonly recovered retained developmental homeobox programs. In `151`, `Meis1`, `Meis2`, `Pbx1`, `Pbx3`, `Pknox2`, `Dlx3`, `Dlx6`, `Lhx3`, `Lhx4`, `Hoxa1`, `Hoxa3`, `Hoxa13`, `Hoxb8`, `Hoxd10`, and `Hoxd13` each had `0` DEGs. The Distributed Agents corpus summarizes the same pattern across matched neuronal groups: represented MEIS/PBX/PKNOX/HOX perturbations were transcriptionally buffered in the P16 neuronal screen and did not produce a shared homeobox-cofactor module. This is a good mechanistic boundary because it says that a developmental DNA-binding annotation alone is a weak reason to expect a `151` response after juvenile sparse CRISPR.

**BAF/mSWI/SNF lane.** External ZFHX3 biology gives a real connection to chromatin machinery: Perez Baca et al. reported physical interaction of ZFHX3 with BRG1/BRM-associated factor complexes in human neuronal differentiation. The local data showed that this cell group can report a BAF-sensitive state, but that it is strongly subunit-selective:

- `Smarcc2`: `185` DEGs; top focal genes included `Ptpn3` (`log2FC = -0.982`, `p_adj = 6.9e-24`), `Reep2` (`-0.681`, `2.0e-20`), `Tiam1`, `C1qtnf4`, and `Prkcd`.
- `Arid2`: `56` DEGs; top focal genes included `Rsrp1`, `Stxbp2`, `Kcnj9`, `Prkcd`, `L1cam`, and `Abhd12b`.
- `Arid1a`: `22` DEGs; top focal genes included `Clstn2`, `Begain`, `Kcnq2`, `Ptpn3`, and `Rasa4`.
- `Smarce1`: `11` DEGs and overlapped the BAF module on negative `Reep2`, `Ptpn3`, `Prkcd`, `Abhd12b`, `Begain`, and `Lrrc7`.
- In contrast, `Arid1b`, `Smarca2`, and `Smarcd1` each had only one DEG, and `Smarca4`/BRG1, `Smarcc1`, and `Smarcad1` had `0`.

The Distributed Agents corpus has a high-confidence same-experiment claim that the `151` BAF/mSWI/SNF module converges most clearly through `Smarcc2`, `Smarce1`, and `Arid1a`, with partial `Arid2`, while `Smarca4`, `Smarca2`, `Smarcc1`, `Bicra`, and `Arid1b` are flat, weak, or divergent rather than interchangeable phenocopies. The relevant point for `Zfhx3` is that even a core ATPase, `Smarca4`, did not produce the module. Therefore a ZFHX3-BAF physical association is not enough to transfer the `Smarcc2` or `Arid2` count to `Zfhx3`.

**Circadian and SCN lane.** Mouse `Zfhx3` has well-supported SCN circadian functions, and the focal `151` group did show circadian-node responses: `Bmal1` had `103` DEGs, `Nr1d1` had `116`, while `Clock` and `Cry2` each had `3`, and `Nr1d2` had `1`. Distributed Agents reports a shared `Bmal1`/`Nr1d1` `151` state involving extracellular-remodeling genes such as `Pdgfa`, `Col4a1`, and `Col4a2`, but also a high-confidence boundary that circadian, ROR, and REV-ERB perturbations were not transcriptionally interchangeable. Parsons et al. found that `Zfhx3` acts in SCN mainly through AT-motif-driven neuropeptide/intercellular-signaling genes with minimal effects on core clock genes, while Wilcox et al. confirmed a behavioral SCN requirement after adult knockout. The assayed cell group here is a thalamic `Prkcd`/`Grin2c` glutamatergic group rather than SCN, retina, or striatal progenitors, so the `Bmal1`/`Nr1d1` signature is best treated as a counterexample showing pathway specificity, not as a reason to predict a hundred `Zfhx3` DEGs.

**External function versus assay context.** ZFHX3 is not biologically inert: human ZFHX3 haploinsufficiency causes neurodevelopmental disease; mouse `Zfhx3` is needed for late embryonic/perinatal D1 MSN production; and SCN/retinal phenotypes are clear. Those phenotypes either involve developmental windows before P16, specialized SCN/retinal circuits, heterozygous missense effects, or behavioral/electrophysiologic outputs that need not map to broad nuclear mRNA changes in a sparse P16-to-P37/44 thalamic perturbation assay.

**Prediction.** The strongest matched evidence is the zero `Zfhx2` result, the broad null for postnatal homeobox/TALE comparators, and the subunit selectivity that prevents moving BAF-module counts onto every BAF-associated factor. I therefore predict that `Zfhx3` will fall in the no-detectable-DEG class in `151 TH Prkcd Grin2c Glut`.

## Limits and uncertainty

This is an extrapolation because the held-out `Zfhx3` expression signature is absent by construction, and Distributed Agents had no direct `Zfhx3` claim in the frozen same-experiment release. `Zfhx2` is the best assayed paralog but not a functional equivalent: `Zfhx3` has SCN, retinal, striatal-developmental, and disease links that `Zfhx2` does not share. The BAF comparison is also imperfect because a DNA-binding transcription factor that recruits or cooperates with BAF can regulate only a locus subset, and the experiment did not measure BAF occupancy or ZFHX3 protein. Finally, a prediction of zero means "no measured gene crosses BH FDR 0.05 in this assay and cell group"; it does not mean that editing had no molecular consequence, that ZFHX3 is unimportant, or that earlier developmental or SCN-specific perturbation would be flat.
