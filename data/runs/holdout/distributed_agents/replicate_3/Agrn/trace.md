# Agrn DEG-count prediction

## Question and ambiguity resolution

The requested held-out perturbation file contains one target, `Agrn`. I interpreted the requested endpoint as the exact assay endpoint in the prompt: the number of measured genes with `pvals_adj < 0.05` after `Agrn` perturbation in `151 TH Prkcd Grin2c Glut`, where `pvals_adj` is the BH-adjusted Wilcoxon p-value from the matched perturbed nuclei versus matched non-targeting controls. `Agrn` itself was held out as a perturbation target, so I did not have an `Agrn` knockout expression vector or an observed `Agrn` count to inspect.

The endpoint can be positive either because the perturbation causes a multi-gene downstream state or because the targeted RNA itself is significantly depleted. I treated the target-RNA event as real evidence when it appeared in nearby training perturbations, but I did not require it: this CRISPR assay often has weak target-mRNA reduction, and the prompt explicitly warns that target RNA is not a protein-level editing-efficiency readout.

## Sources

- Input manifest: `[local file: 006_Agrn.csv]`.
- Focal training counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Full same-experiment DE table: `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`, especially corpus contexts for `Lrp4`, `Musk`, `Dag1`, and `Ext1`, plus lexical claim search for agrin/LRP4/MuSK, dystroglycan, extracellular-matrix, and heparan-sulfate/proteoglycan comparators.
- Distributed Agents runtime profile tools for focal same-experiment profile comparison among Agrn-adjacent observed perturbations.
- NCBI PubMed E-utilities for external mechanism checks and citations.

## Computation over the training data

The focal count CSV has 1,674 non-held-out training perturbations. The response distribution is very zero-inflated: median `n_degs` is 0, 469/1,674 are nonzero, and the largest positive response is `Uba5` with 2,677 DEGs. `Agrn` is absent from this training count table and absent from the observed `gene_target` universe, as expected.

The parquet has 616,253,184 rows and is sorted by `group_name`. I used Parquet row-group min/max statistics on `group_name` to select the 35 row groups overlapping `151 TH Prkcd Grin2c Glut`, then filtered those rows to mechanistic candidate perturbations. This avoids loading the entire file and uses the same `pvals_adj < 0.05` rule as the focal count CSV.

For the most direct candidates in the focal cell group, the observed counts were:

| candidate class | training perturbations and focal `n_degs` |
| --- | --- |
| canonical agrin receptor/NMJ branch | `Lrp4` 0, `Musk` 0, `Ache` 1, `Chrna1` 0, `Chrnb1` 0, `Chrnd` 0, `Chrne` 0, `Chrng` 0 |
| dystroglycan or matriglycan branch | `Dag1` 0, `Dmd` 0, `Snta1` 0, `Sgcd` 0, `Sgce` 0, `Fktn` 0, `Large1` 1, `Crppa` 0, `Rxylt1` 0 |
| heparan-sulfate/proteoglycan branch | `B3gat3` 0, `Bpnt2` 1, `Ext1` 0, `Ext2` 0, `Glce` 0, `Gpc6` 0, `Hs6st2` 0, `Xylt1` 0 |
| other ECM/synaptic-adhesion comparators | `Fbn1` 0, `Adamts17` 0, `Itgb1` 0, `Itga6` 0, `Itga7` 0, `Nrxn2` 0, `Nrxn3` 0, `Lrrtm3` 0; `Nrxn1` and `Nlgn3` each had one significant self-target row |

The one-DEG calls were not a shared Agrn-adjacent program in `151 TH Prkcd Grin2c Glut`: `Ache`, `Bpnt2`, `Large1`, `Nrxn1`, and `Nlgn3` were each dominated by the targeted transcript itself. Nearby rows that almost reached significance were also isolated, for example `Ext2` self-down at `pvals_adj = 0.0559` and `Sgcd`-linked `Sik2` at `pvals_adj = 0.0536`.

I then used the Distributed Agents runtime profile comparison on 22 observed Agrn-adjacent perturbations in the focal cell group, using Wilcoxon `scores` as the signed profile value and `pvals_adj` as the significance column. Twenty of the 22 profiles had no significant focal features; the two exceptions had singleton responses. In a focused ten-node agrin-receptor/HSPG/ECM cohort (`Lrp4`, `Musk`, `Dag1`, `Ext1`, `B3gat3`, `Ext2`, `Glce`, `Hs6st2`, `Xylt1`, `Gpc6`), 45/45 pairwise comparisons had zero significant-program overlap in both directions. Median top-50 positive-tail and negative-tail overlap coefficients were both 0.0, with maxima of only 0.04. Thus the non-held-out candidates did not hide a coherent low-amplitude Agrn-pathway state below FDR.

As a guard against `Agrn` being a generally invisible transcript in this cell type, I also filtered the focal DE table for rows where `names == "Agrn"` across all 1,674 training perturbations. `Agrn` was significantly moved in 18 broad transcriptional perturbations, led by `U2af2`, `Tpr`, `Rora`, `Tnpo3`, `Zfp423`, and `Wac`. That shows the transcript can be detected and regulated in this cell group, but those drivers are spliceosome/chromatin/nuclear-transport or broad state perturbations, not agrin receptor or extracellular-matrix comparators.

## Target-specific reasoning

### Agrn

**External function.** `Agrn` encodes agrin, an extracellular heparan-sulfate proteoglycan best known as the motor-neuron-derived organizer of acetylcholine-receptor clustering at the neuromuscular junction. Germline agrin loss disrupts postsynaptic AChR aggregates and NMJ differentiation in mouse muscle (Gautam et al. 1996, PMID:8653788, DOI:10.1016/S0092-8674(00)81253-2). The canonical muscle pathway runs through Agrin binding to LRP4 and activation of the MuSK receptor complex (Kim et al. 2008, PMID:18848351, DOI:10.1016/j.cell.2008.10.002). Agrin also binds alpha-dystroglycan and sits in a broader laminin-G-domain extracellular-matrix ligand family: alpha-dystroglycan was identified as an agrin-binding component of the dystrophin-associated glycoprotein complex (Campanelli et al. 1994, PMID:8205616, DOI:10.1016/0092-8674(94)90051-5), and dystroglycan glycosylation controls binding to laminin, neurexin, and agrin in muscle and CNS tissue (Michele et al. 2002, PMID:12140558, DOI:10.1038/nature00837).

Those mechanism priors do not, by themselves, imply a broad acute snRNA-seq response in sparse P16 brain neurons. Several relevant external observations are developmental, peripheral, structural, or electrophysiological rather than nuclear-RNA phenotypes. For example, postnatal neuronal `Ext1` deletion can impair synaptic physiology without gross brain morphogenesis defects (Irie et al. 2012, PMID:22411800, DOI:10.1073/pnas.1117881109), embryonic cultured CNS neurons show selective and context-dependent agrin/Lrp4/MuSK synaptic effects (Handara et al. 2018, PMID:30385274, DOI:10.1016/j.ydbio.2018.10.017), and agrin-deficient cortical cultures can still form functional glutamatergic and GABAergic synapses (Li et al. 1999, PMID:10380076, DOI:10.1002/(SICI)1097-4695(19990615)39:4<547::AID-NEU8>3.0.CO;2-C). The training data therefore get more weight than a generic "agrin is synaptic" prior.

**Same-experiment analogs.** The strongest analogs and counterexamples are all near-null in the focal class:

- `Lrp4` and `Musk`, the direct canonical agrin-receptor branch, both had `n_degs = 0` in `151 TH Prkcd Grin2c Glut`. Distributed Agents corpus context for `Musk` reports that its sampled neuronal response uncoupled from canonical agrin-LRP4-MuSK-Dok7-AChR and Wnt-AChR comparators; the context for `Lrp4` reports that its only robust screen hit was a single `Arglu1` induction outside the focal thalamic class and that `Lrp4` did not converge with `Musk`. The corpus claim spanning `Chrnb1`, `Chrnd`, `Chrne`, `Chrng`, `Lrp4`, and `Musk` states that represented muscle AChR/NMJ pathway genes did not recover a shared muscle-channel or NMJ transcriptional module in postnatal brain neurons.
- `Dag1` had `n_degs = 0` in the focal class and Distributed Agents reports a global FDR-defined neuronal null across its recovered groups. Its obvious DGC and matriglycan comparators were also flat or singleton-sized here: `Dmd` 0, `Snta1` 0, `Fktn` 0, `Crppa` 0, `Rxylt1` 0, `Sgcd` 0, and `Large1` 1. The corpus explicitly summarizes these as represented dystrophin-glycoprotein-complex and alpha-dystroglycan glycosylation perturbations lacking a coherent shared postnatal neuronal nuclear-RNA module.
- The proteoglycan synthesis and modification branch was likewise buffered in the focal endpoint: `Ext1` 0, `Ext2` 0, `B3gat3` 0, `Glce` 0, `Gpc6` 0, `Hs6st2` 0, and `Xylt1` 0. Distributed Agents `Ext1` context states that single-node perturbations of represented GAG/heparan-sulfate/proteoglycan pathway genes did not collapse into a common acute postnatal neuronal transcriptional module.
- Broader ECM and synaptic-adhesion comparators were useful negative controls, not positive analogs. `Fbn1` and `Adamts17` had no focal DEGs, and the Distributed Agents claim over those two targets reports no detectable ECM-linked TGF-beta/BMP-SMAD module in this neuronal screen. `Nrxn2`, `Nrxn3`, `Lrrtm3`, `Itgb1`, `Itga6`, and `Itga7` were also zero in the focal endpoint; the few one-gene `Nrxn1` or `Nlgn3` calls looked like targeted-transcript depletion rather than a shared synaptic-adhesion module.

**Zero/nonzero call.** I predicted `Agrn` as a true zero in this focal endpoint. The decision is driven mainly by the within-dataset receptor and matrix comparators: the screen directly observed `Lrp4`, `Musk`, `Dag1`, `Ext1`, and multiple adjacent NMJ, DGC, and heparan-sulfate genes in the same cell group, and almost all produced no FDR<0.05 genes. The Distributed Agents same-experiment corpus independently summarizes the same boundaries at the pathway level, including no shared neuronal NMJ module and no shared DGC/matriglycan or GAG/HSPG module. External biology explains why those are the right comparators, while the observed Perturb-seq data say that these extracellular and synapse-structural mechanisms usually do not convert into an acute broad nuclear transcriptomic state in postnatal thalamic NeuN+ nuclei.

I considered a singleton prediction to allow for `Agrn` self-mRNA depletion. `Agrn` is measurable in this focal cell group, and training targets such as `Large1`, `Ache`, `Nrxn1`, `Nlgn3`, and `Bpnt2` scored one-DEG focal responses because their own transcript passed FDR. I did not carry that to `Agrn` because the most specific ligands/receptors around it, including `Lrp4`, `Musk`, `Dag1`, and `Ext1`, lacked even a target-RNA FDR row in the focal class; the expected effect size from acute mosaic CRISPR is modest; and there was no same-experiment evidence for an Agrn-neighbor downstream module that could add further genes. The point prediction is therefore 0 rather than 1.

## Limits

The direct `Agrn` perturbation signature was held out, so this is an extrapolation from adjacent perturbations rather than a nearest-neighbor transfer from an observed Agrn profile. `Agrn` is a ligand, secreted matrix protein, HSPG, dystroglycan binder, and NMJ organizer; none of the training perturbations is a perfect substitute for losing agrin itself. The assay also measures nuclear RNA from postmitotic juvenile NeuN+ cells and not agrin protein, matrix deposition, heparan-sulfate chain biochemistry, acetylcholine-receptor clustering, spine structure, or electrophysiology. A real Agrn effect on extracellular architecture could be invisible to this endpoint, and a target-transcript-only DEG remains possible if the hidden guides happen to deplete the captured `Agrn` RNA efficiently. The prediction should be read as "no gene reaches this assay's FDR<0.05 threshold in this focal class", not as evidence that Agrn has no neuronal or synaptic function.

