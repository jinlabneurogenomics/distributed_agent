# Tbce DEG-count prediction

## Question and resolved ambiguities

The manifest for this run contains one held-out perturbation, `Tbce`. I therefore made one point prediction: the number of measured genes expected to satisfy `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` nuclei after acute mosaic AAV-CRISPR loss of mouse `Tbce`.

I treated the endpoint as the screen-specific DEG breadth, not as a generic essentiality score. Counts in the focal training CSV are very zero-inflated in this cell group: 1205/1674 assayed training perturbations have no DEG, the median is 0, the 75th percentile is 1, the 95th percentile is 18, and a small tail of RNA-processing, proteostasis, and transcriptional regulators reaches hundreds to thousands of DEGs. I also did not use the absence of target-RNA depletion as a failed-editing call; the prompt explicitly warns against that, and the nearest cofactor analog `Tbcd` itself had no focal self-RNA decrease while still producing 12 DEGs.

## Sources

- Supplied endpoint table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Supplied differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Held-out manifest: `[local file: 232_Tbce.csv]`.
- Internal same-experiment corpus: Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
- Distributed Agents runtime profile comparison over the focal-cell log-fold-change signatures.
- External mechanisms from Reactome, "Post-chaperonin tubulin folding pathway", R-HSA-389977; Nithianantham et al. 2015, DOI `10.7554/eLife.08811`; Francis et al. 2017, PMID `28126905`, DOI `10.1074/jbc.M116.770909`; Kortazar et al. 2006, PMID `17184771`, DOI `10.1016/j.yexcr.2006.09.002`; Martin et al. 2002, PMID `12389029`, DOI `10.1038/ng1016`; Sferra et al. 2016, PMID `27666369`, DOI `10.1016/j.ajhg.2016.08.006`; Gasic et al. 2019, PMID `30964857`, DOI `10.1371/journal.pbio.3000225`; Taheri et al. 2025, PMID `41461644`, DOI `10.1038/s41467-025-68142-0`.

## Computation over the supplied DE data

I read the held-out CSV and found exactly one target:

```text
Tbce
```

I read the training DEG-count CSV to calibrate all candidate perturbations in the exact endpoint being predicted. I then scanned the training target list for direct tubulin-folding, structural tubulin, microtubule, motor, MAP, ARL, and dynactin comparators. The direct and nearby focal-cell counts were:

| training perturbation | `n_degs` in `151 TH Prkcd Grin2c Glut` | role in the prediction |
| --- | ---: | --- |
| `Tbcd` | 12 | Primary TBC cofactor analog. |
| `Tuba1a` | 7 | Detectable alpha-tubulin dosage-response boundary. |
| `Tuba4a` | 2 | Alpha-tubulin paralog counterexample. |
| `Tubb4b` | 1 | Beta-tubulin counterexample. |
| `Tubb5` | 1 | Beta-tubulin counterexample. |
| `Arl2bp` | 0 | Indirect ARL-axis counterexample; `Arl2` itself was not present. |
| `Arl3` | 1 | Small-GTPase/TBC-adjacent boundary, but ciliary rather than TBC-DEG. |
| `Dctn1` | 75 | Detectable microtubule-transport positive control, mechanistically too broad. |
| `Atxn10` | 52 | Detectable cytoskeletal/tubulin-state positive control, mechanistically indirect. |
| `Map1b`, `Mapre2`, `Mapt` | 1 each | MAP/EB/Tau counterexamples. |
| `Kif2a`, `Nin`, `Ttll5`, `Map6`, `Spast` | 0 each | Further microtubule-neighborhood counterexamples. |

Because the all-cell parquet has 616,253,184 rows, I avoided whole-file reads. I first inspected Parquet row-group statistics to locate the row groups containing `151 TH Prkcd Grin2c Glut`, then used a `pyarrow.dataset` filter on both `group_name` and the selected candidate `gene_target` values and retrieved only `names`, `gene_target`, `logfoldchanges`, `pvals_adj`, `scores`, `n_pert_matched`, and `n_ctrl_matched`. This recovered 17,259 measured genes for each selected focal signature.

For `Tbcd`, the 12 FDR<0.05 focal genes were a narrow mixture:

- induced tubulin dosage readouts: `Tuba1a` log2FC `+0.488`, `Tuba1b` `+0.675`;
- induced non-tubulin/adaptation genes: `Ypel4`, `Nfil3`, `Kctd16`, `Satb1`, `Slc25a23`, `Mturn`, `Jun`;
- repressed neuronal/synaptic genes: `Lrrc7`, `Ptprn2`, `Samd5`.

The measured `Tbcd` target transcript itself was not down (`+0.050`, `pvals_adj=1`, 146 matched perturbed nuclei versus 23,679 controls), reinforcing that the 12-gene signature is not an artifact of simply counting self-depletion.

For `Tuba1a`, all 7 DEGs were the target plus alpha/beta-tubulin paralogs: self `Tuba1a` was down `-0.967` and `Tubb3`, `Tubb2a`, `Tuba4a`, `Tubb4a`, `Tubb4b`, and `Tubb5` were induced. `Tuba4a`, `Tubb4b`, `Tubb5`, `Map1b`, `Mapre2`, `Mapt`, `Arl3`, and `Stub1` were self-only or near self-only. `Dctn1` had a broader 75-gene sterol/lipid and neuronal response; its significant genes did not intersect with the positive or negative FDR genes of `Tbcd`.

I also ran a Distributed Agents runtime complete profile comparison of `Tbcd`, `Tuba1a`, `Tuba4a`, `Tubb4b`, `Tubb5`, `Map1b`, `Mapre2`, `Mapt`, `Kif2a`, `Dctn1`, `Map6`, `Atxn10`, and `Spast`. The important result was not a high-confidence phenocopy module but a boundary: `Tbcd` had 9 up and 3 down FDR genes, `Tuba1a` had 6 up and 1 down, and the `Tbcd`-`Tuba1a` profile had zero same-direction significant intersections, with one significant direction conflict. `Tbcd` also had zero same-direction FDR intersections with `Tuba4a`, `Dctn1`, and `Atxn10`. Thus the nonzero count for `Tbce` should be anchored by mechanistic proximity to the TBC cofactor reaction, not by averaging all cytoskeletal signatures.

## Same-experiment corpus evidence

The internal Distributed Agents corpus had no `Tbce` target context, as expected for a held-out perturbation. I therefore queried the measured analogs.

`Tbcd` had seven same-experiment findings. The most relevant were:

- `Tbcd:F001`: `Tbcd` made a sparse but real signature, with `151 TH Prkcd Grin2c Glut` concentrating the response.
- `Tbcd:F002`: alpha-tubulin mRNA induction was the recurrent output of `Tbcd`, with `Tuba1a` up in every responder and `Tuba1b` up in the strongest glutamatergic responders.
- `Tbcd:F006`: `Tuba1a`, `Tuba4a`, and `Arl2bp` did not phenocopy `Tbcd`; `Arl2bp` was only an indirect ARL2-axis proxy, and the closer cofactor perturbations were not represented in training.
- `Tbcd:F007`: `Tbcd` did not induce a broad UPR/ISR, autophagy, lysosome, redox, or proteasome transcriptional collapse.

The corpus-wide microtubule/tubulin claims also emphasized that the assayed MAP, tubulin, EB, dynactin, kinesin, CAMSAP, and MARK perturbations did not form a coherent shared postnatal neuronal mRNA stress module, apart from the narrow `Tuba1a` tubulin-isotype response. That is the main reason I kept `Dctn1` and `Atxn10` as positive controls for detectability rather than as numerical analogs for `Tbce`.

## Biological interpretation for `Tbce`

`Tbce` encodes tubulin folding cofactor E. Reactome R-HSA-389977 places TBCE with TBCA, TBCB, TBCC, TBCD, and ARL2 in the post-chaperonin tubulin folding pathway. Biochemical reconstitution and structural work show that TBCD, TBCE, and ARL2 form a core cage-like chaperone that regulates soluble alpha/beta-tubulin; TBCE extends along alpha-tubulin while TBCD engages beta-tubulin, and TBCC/ARL2-coupled cycling promotes tubulin assembly and turnover (Nithianantham et al. 2015; Taheri et al. 2025). Kortazar et al. 2006 further showed that TBCB and TBCE bind alpha-tubulin and can dissociate tubulin heterodimers. Francis et al. 2017 showed the reciprocal measured side of the reaction for TBCD, ARL2, and beta-tubulin. Gasic et al. 2019 showed that alpha- and beta-tubulin mRNA abundance can be a sensitive readout of microtubule-state changes, making the `Tbcd`-driven `Tuba1a`/`Tuba1b` induction biologically plausible.

Loss of TBCE is therefore much closer to measured `Tbcd` than to loss of a single structural tubulin isoform. Germline/hypomorphic biology supports that TBCE can be limiting for neurons and microtubules: the `pmn` mouse phenotype is caused by a destabilizing `Tbce` missense allele and shows motor-axon microtubule loss (Martin et al. 2002), and human biallelic TBCE mutations can drive early progressive encephalopathy with distal spinal muscular atrophy and reduced polymerized alpha-tubulin in fibroblasts (Sferra et al. 2016).

At the same time, the within-dataset data argue against a large injury response in this P16 mosaic, P37-P44 forebrain/midbrain snRNA assay. Direct structural tubulins produced only 1 to 7 DEGs in the focal group, MAP/EB/motor perturbations were zero or self-only, and the `Tbcd` signature itself was only 12 DEGs and explicitly lacked UPR/ISR/proteasome/autophagy breadth. Also, `Tbce` disease phenotypes include developmental parathyroid/skeletal and long-axon lower-motor-neuron effects; those are imperfectly represented by sparse postnatal CRISPR in thalamic `Prkcd/Grin2c` glutamatergic neurons.

Balancing these facts, I predicted that `Tbce` will be nonzero and close to `Tbcd`, but not as broad as `Dctn1` or `Atxn10`. I chose 10 DEGs: slightly below the 12 observed for `Tbcd` to reflect that the exact focal thalamic adaptation module is not guaranteed to recur from the alpha-tubulin side of the TBC-DEG reaction.

## Limits

The strongest limitation is that `Tbce` itself was fully held out and the training set lacks `Tbca`, `Tbcb`, `Tbcc`, and `Arl2` perturbations, so `Tbcd` is the only direct cofactor anchor. `Arl2bp` is an indirect proxy, not ARL2. Expression-profile correlations among candidate microtubule perturbations were largely uninformative at the significant-gene level because many signatures were zero or self-only. Finally, the prediction is an assay- and power-dependent FDR count in one neuronal group; it cannot be interpreted as the expected size of a chronic neurodegenerative, embryonic tubulinopathy, peripheral motor-neuron, or protein-level microtubule phenotype.
