# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The task asks for the held-out focal-cell differential-expression breadth caused by acute sparse CRISPR loss of `Foxc1`: the number of measured genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`. I treated zero as the literal prediction that no measured gene crosses the same FDR 0.05 threshold used for the supplied training CSV, not as a claim that the gene is biologically irrelevant.

The requested CSV contains one held-out target, `Foxc1`. It is absent from both the focal DEG-count CSV and the Parquet DE table, so all evidence has to transfer from non-held-out perturbations and from external biology.

## Sources used

- Direct training inputs:
  - `[local file: training_de_all_cell_groups.parquet]`
  - `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  - `[local file: 078_Foxc1.csv]`
- Same-experiment interpretation layer: Distributed Agents PerturbAI corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`. The corpus contained no `Foxc1` Findings or Claims, but did contain curated `Foxc2`, `Foxa2`, `Foxp2`, `Tbx6`, and Notch/vascular-pathway summaries.
- External literature searched through PubMed:
  - Kume et al. 2001, *Genes & Development*, DOI `10.1101/gad.907301`, PMID 11562355.
  - Hayashi and Kume 2008, *PLOS ONE*, DOI `10.1371/journal.pone.0002401`, PMID 18545664.
  - Aldinger et al. 2009, *Nature Genetics*, DOI `10.1038/ng.422`, PMID 19668217.
  - Siegenthaler et al. 2009, *Cell*, DOI `10.1016/j.cell.2009.10.004`, PMID 19879845.
  - Norrmen et al. 2009, *Journal of Cell Biology*, DOI `10.1083/jcb.200901104`, PMID 19398761.
  - Mishra et al. 2016, *Developmental Biology*, DOI `10.1016/j.ydbio.2016.09.019`, PMID 27671872.
  - Norden et al. 2020, *eLife*, DOI `10.7554/eLife.53814`, PMID 32510325.
  - Gillnas et al. 2022, *Biology Open*, DOI `10.1242/bio.059431`, PMID 35876806.

## Computational checks over the training data

I first confirmed the held-out and training split:

- Manifest order: `Foxc1`.
- The focal training CSV has 1,674 non-held-out targets; 1,205 are zero in `151 TH Prkcd Grin2c Glut`.
- `Foxc1` has 0 rows in the Parquet under `gene_target` and 0 rows in the training-count CSV, consistent with the holdout.

The Parquet is sorted by `group_name`, so I scanned only the 35 row groups intersecting `151 TH Prkcd Grin2c Glut` and recomputed

```sql
COUNT(*) FILTER (WHERE pvals_adj < 0.05)
```

per `gene_target`. The recomputed counts exactly matched all 1,674 rows of `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, so no alternate threshold or self-target exclusion had to be inferred.

## Relevant non-held-out perturbations

| Comparator set | Focal observed `n_degs` at FDR 0.05 | Why it mattered for `Foxc1` |
| --- | ---: | --- |
| `Foxc2` | 0 | Closest available FOXC paralog and strongest internal analog. In the focal group, `Foxc2` had 277 perturbed nuclei, 0 genes at FDR 0.05 or 0.10, and a minimum adjusted P value of 0.809. In the corpus, `Foxc2` was pan-null across all 23 recovered neuronal groups and did not move the arterial VEGF-Dll4/Notch-Hey2, CXCR4, PROX1, lymphatic NFATc1/ITGA9, or RhoA/ROCK cytoskeletal programs nominated from its endothelial biology. |
| Other forkhead TFs: `Foxa2`, `Foxe3`, `Foxi1`, `Foxj3`, `Foxk2`, `Foxl1`, `Foxl2`, `Foxn1`, `Foxp2`, `Foxp3` | all 0 | This was a family-level negative control. Every represented forkhead perturbation was zero in the focal cell group; their focal minimum FDR values were either 1.0 or far above threshold (`Foxk2`, whose best row was its own transcript, still stopped at FDR 0.146). The curated same-experiment reports for `Foxa2`, `Foxn1`, `Foxp2`, and `Foxp3` similarly found no broad neuronal forkhead signature, even for Fox genes with real developmental or immune transcriptional roles. |
| FOXC/vascular/Notch/TGF-beta relatives: `Acvr1`, `Acvr2a`, `Acvr2b`, `Acvrl1`, `Bmpr1a`, `Bmpr1b`, `Bmpr2`, `Cxcr4`, `Dll1`, `Ephb4`, `Flt4`, `Itga9`, `Kdr`, `Map2k2`, `Notch1`, `Notch2`, `Notch4`, `Nrp1`, `Pdgfrb`, `Pik3cb`, `Pik3r1`, `Pik3r2`, `Prickle1`, `Smad3`, `Tgfbr1`, `Tgfbr2`, `Tgfbr3` | all 0 | FOXC1/FOXC2 biology intersects VEGF, Dll4/Notch, endothelial, lymphatic-valve, TGF/BMP, and somitic Notch-Delta programs in the literature. Nearly all represented members of those pathways were exactly zero in `151 TH`, and the corpus Claims for Notch receptors and vascular/lymphatic VEGF/neuropilin/Sox18 modules found no shared postmitotic neuronal module. |
| `Map2k1`, `Mesp2` | 4, 1 | These are positive but tiny pathway counterexamples from the broader FOXC2 report, not close analogs. They show that a represented non-neuronal developmental pathway member can occasionally produce a focal singleton/few-gene state, but not a FOXC-like expression program. |
| `Prox1` | 50 | The main counterexample. `Prox1` is lymphatic-related externally and produced a moderate focal response, but `Foxc2` itself, `Flt4`, `Kdr`, `Itga9`, Notch receptors, BMP/TGF-beta receptors, and PI3K nodes did not phenocopy it; the FOXC2 corpus report specifically treated `Prox1` as a divergent comparator rather than a same-state neighbor. |
| Developmental TFs near Foxc1 biology: `Tbx6`, `Pitx2`, `Lmx1b`, `Pax6`, plus `Fgfr1` and `Fgfr2` | all 0 | These bound the embryonic patterning extrapolation. `Tbx6` and canonical T-box/Notch/FGF somitogenesis comparators failed to engage their expected embryonic program in postnatal neurons; `Pitx2`, `Lmx1b`, `Pax6`, `Fgfr1`, and `Fgfr2` were also flat in the focal cell group. |

## Foxc1-specific biological reasoning

The best transfer target is `Foxc2`, not a broad chromatin regulator or a generic transcription factor. `Foxc1` and `Foxc2` encode closely related forkhead/winged-helix factors with overlapping embryonic expression in somites, head mesoderm, and endothelial/mesenchymal cells. In mouse compound mutants, Kume et al. showed dose-sensitive cooperation in cardiovascular development, branchial-arch patterning, early vessel remodeling, and anterior presomitic-mesoderm segmentation through a Notch/Delta/Mesp loop. Hayashi and Kume then placed FOXC1/FOXC2 in endothelial VEGF-Dll4-Notch-Hey2 transcriptional regulation. Norden et al. showed postnatal lymphatic-valve cytoskeletal roles for both FOXC1 and FOXC2. These relationships all point to strong Foxc biology, but in mesenchymal or vascular lineages rather than NeuN-enriched thalamic glutamatergic neurons.

The strongest `Foxc1` brain literature is also displaced from the assayed cell state. Aldinger et al. linked human FOXC1 dosage to Dandy-Walker/cerebellar vermis malformations and showed that Foxc1-null mice have embryonic rhombic-lip defects secondary to loss of mesenchyme-secreted signals. Siegenthaler et al. used Foxc1 meningeal mutants to show that dorsal forebrain meninges supply retinoic acid for embryonic corticogenesis, and Mishra et al. found that Foxc1 expression in neural-crest-derived meninges and brain pericytes, rather than endothelial cells, supports normal neocortical vascular development through meningeal retinoic acid, WNT, and VEGF-A. Gillnas et al. similarly emphasized a developmental meninges-neural-tissue interaction for cerebellar formation.

Those mechanisms predict that a germline or embryonic meningeal/pericyte `Foxc1` loss can alter neurons indirectly. They do not predict a cell-autonomous transcriptional collapse after a sparse P16 AAV CRISPR edit in already postmitotic `151 TH Prkcd Grin2c Glut` neurons, and the screen largely excludes the meningeal, pericyte, endothelial, lymphatic, and choroid/vascular compartments where FOXC programs would be most interpretable.

The within-dataset tests support that displacement. The closest represented paralog, `Foxc2`, had no FDR-supported focal signature despite 277 focal perturbed nuclei and no FOXC endothelial/lymphatic target-gene response anywhere in the same-experiment corpus. Direct perturbation of most same-pathway targets was also zero in the focal group. The `Prox1` focal response prevents a blanket claim that all lymphatic-development genes are silent in `151 TH`, but it did not define a FOXC state because the direct `Foxc2`, receptor, Notch, VEGF, BMP/TGF-beta, and PI3K comparators were flat.

Prediction for `Foxc1`: `0` DEGs. I am making a zero/nonzero call of "zero" because the held-out gene is expected to behave like `Foxc2` and the off-lineage forkhead/developmental TF cluster in this specific juvenile thalamic neuronal assay, not like the few broad chromatin perturbations that generated tens to thousands of DEGs.

## Limits

- There is no measured `Foxc1` profile in the supplied Parquet and the same-experiment corpus has no `Foxc1`-local report, so the prediction is extrapolation from `Foxc2` and pathway relatives.
- The acute AAV experiment did not sequence indels. Zero DEGs for `Foxc2` or other analogs cannot prove failed editing or successful editing; it only shows the recovered nuclear RNA state.
- Germline and embryonic Foxc1 phenotypes are partly indirect, through meninges, pericytes, vasculature, retinoic acid, WNT, and VEGF-A. Those lineages are not sampled here, so their transcriptional effects could be large in another assay and still absent in `151 TH` neurons.
- `Prox1` demonstrates that some lymphatic/developmental factors can make a focal thalamic signature, so the zero prediction is not a pure pathway-membership rule. I down-weighted `Prox1` because the closer FOXC2 and direct VEGF/Notch/TGF-beta comparators did not share that state.
