# Dalrd3 held-out DEG-count prediction

## Question and resolved ambiguities

The requested manifest contained one held-out target:

```tsv
target_name
Dalrd3
```

I interpreted the requested endpoint as the number of measured genes with `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` Wilcoxon result for the acute AAV CRISPR loss-of-function perturbation, not the biological importance of the target and not target RNA knockdown. A value of zero means that no genes are expected to cross this assay-specific BH-FDR threshold.

`Dalrd3` was absent from both the training count table and the DE parquet as a `gene_target`; the closest enzyme partner, `Mettl2`, was also absent from the 1,674 training targets. I therefore used assayed tRNA/RNA-modification relatives as imperfect analogs rather than pretending there was a same-complex measurement.

## Sources used

- `training_de_all_cell_groups.parquet`: focal-cell Wilcoxon `scores`, `logfoldchanges`, and `pvals_adj` for selected assayed tRNA and translation-stress comparators.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: focal `n_degs` values for all non-held-out training targets.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`: curated findings and higher-order claims for `Alkbh8`, `Nsun2`, `Trmt1`, `Cdkal1`, `Elp1`, and `Elp2`, especially the claim that represented non-Elongator tRNA-modification enzymes are largely buffered at the basal mRNA level while Elongator loss selectively induces an ATF4/amino-acid stress program.
- Distributed Agents runtime focal profile artifacts generated in this run:
  - `dalrd3_trna_modifier_neighbors.json`, comparing `Alkbh8`, `Nsun2`, `Trmt1`, `Elp1`, and `Elp2` with all 1,674 eligible training perturbations in `151 TH Prkcd Grin2c Glut`.
  - `dalrd3_trna_modifier_compare.json` and `dalrd3_trna_modifier_compare_inspect.json`, symmetrically comparing the compact RNA/tRNA cohort `Alkbh8`, `Nsun2`, `Trmt1`, `Cdkal1`, `Elp1`, `Elp2`, and `Bdp1`.
- UniProtKB, entry `Q6PJN8`, and NCBI Gene, GeneID `67789`, accessed 2026-09-23: mouse Dalrd3 is annotated as DALR anticodon-binding domain-containing protein 3, involved in recognition and targeting of `tRNA-Arg(CCU)` and `tRNA-Arg(UCU)` for METTL2-dependent N3-methylcytidine modification.
- Literature:
  - Lentini et al. 2020, DOI `10.1038/s41467-020-16321-6`, PMID `32427860`: human DALRD3 forms a complex with METTL2, selects arginine tRNAs for m3C formation, and DALRD3 deficiency causes near-complete loss of m3C in tRNA-Arg species; a homozygous nonsense variant was linked to developmental delay and early-onset epileptic encephalopathy.
  - Zhang et al. 2024, DOI `10.1016/j.xhgg.2024.100377`, PMID `39482881`: an epileptic-encephalopathy DALRD3 R517C variant in the DALR domain reduced METTL2 association and tRNA binding, reinforcing that DALRD3-dependent tRNA modification is relevant to brain development and function.
  - Huang, Johansson and Bystrom 2005, DOI `10.1261/rna.7247705`, PMID `15769872`, and Karlsborn et al. 2014, DOI `10.4161/15476286.2014.992276`, PMID `25607684`: the six-subunit Elongator complex, including ELP1/ELP2/ELP3, performs an early step in wobble U34 tRNA modification.
  - Abbasi-Moheb et al. 2012, DOI `10.1016/j.ajhg.2012.03.021`, PMID `22541559`, and Dewe et al. 2017, DOI `10.1128/MCB.00214-17`, PMID `28784718`: NSUN2 and TRMT1 are tRNA methyltransferases with human neurodevelopmental disease connections, making their flat screen behavior relevant counterevidence rather than irrelevant housekeeping-gene noise.

## Computation over the focal training data

I first read the training count table to place candidate analogs on the focal `n_degs` scale. The distribution was very sparse: among 1,674 training perturbations, the median was `0`, the 75th percentile was `1`, the 95th percentile was `18`, and only 469 perturbations were nonzero. Exact focal counts for the relevant RNA/tRNA comparators were:

```tsv
target_name	n_degs	relevance_to_Dalrd3
Alkbh8	0	wobble tRNA uridine modification enzyme; non-Elongator writer/eraser-like tRNA chemistry
Nsun2	0	tRNA cytosine methyltransferase; known neurodevelopmental tRNA writer
Trmt1	0	tRNA dimethylguanosine methyltransferase; known neurodevelopmental tRNA writer
Cdkal1	0	tRNA modification enzyme contrasted in the Distributed Agents tRNA-modifier corpus neighborhood
Bdp1	8	RNA polymerase III initiation factor; small tRNA-charging/amino-acid stress response
Elp2	150	Elongator subunit; broad positive tRNA U34/ATF4 stress comparator
Elp1	645	Elongator subunit; broad positive tRNA U34/ATF4 stress comparator
Rars2	0	mitochondrial arginyl-tRNA synthetase, a weaker arginine-tRNA counterexample
Fars2	0	mitochondrial phenylalanyl-tRNA synthetase, a weaker translation counterexample
Lars2	0	mitochondrial leucyl-tRNA synthetase, a weaker translation counterexample
Eef2	9	core elongation factor, weak nonspecific translation counterexample
```

Then I filtered the large parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and the tRNA/stress comparator targets:

```python
f = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(targets)
)
```

This extracted 17,259 measured genes per selected target in the focal group. It confirmed that the zero-count tRNA modifiers were not hiding a near-threshold ATF4 module:

```tsv
target	n_q_lt_0.05	n_q_lt_0.10	min_q	best_focal_score
Alkbh8	0	0	1.000	Fez1 score 3.82, q=1
Nsun2	0	0	0.123	Slc39a14 score 4.49, q=0.123
Trmt1	0	0	0.460	Cars score 4.20, q=0.460
Cdkal1	0	0	1.000	Ddx5 score -3.77, q=1
Bdp1	8	10	0.0057	Ddit3 score 5.08, Mars1 score 4.97
Elp2	150	202	3.60e-16	Asns score 9.26, Shmt2 score 8.41
Elp1	645	830	1.53e-28	Cars score 11.92, Chac1 score 11.83
```

For the canonical integrated-stress genes that were strongly induced by Elongator loss, `Alkbh8`, `Nsun2`, and `Trmt1` were all null:

```tsv
gene	Alkbh8 q	Nsun2 q	Trmt1 q	Elp2 q	Elp1 q
Asns	1.0	1.0	1.0	3.60e-16	1.50e-27
Atf4	1.0	1.0	1.0	3.55e-04	4.66e-09
Cars	1.0	1.0	0.460	2.75e-12	1.53e-28
Chac1	1.0	1.0	1.0	7.45e-09	2.28e-28
Ddit3	1.0	1.0	1.0	1.58e-05	3.13e-20
Herpud1	1.0	1.0	1.0	4.38e-13	4.76e-21
Mars1	1.0	1.0	1.0	6.84e-08	1.38e-18
Slc3a2	1.0	1.0	1.0	1.33e-11	1.80e-17
Slc7a5	1.0	1.0	1.0	1.51e-06	5.04e-15
```

The Distributed Agents runtime profile comparison also showed that the flat anchors had no FDR-supported overlap with the small `Bdp1` response or with `Cdkal1`. Their all-gene cosine values against `Bdp1` were only `0.039-0.043`, and against `Cdkal1` only `0.021-0.086`; `Alkbh8` versus `Trmt1` was essentially orthogonal at cosine `0.001`. In contrast, `Bdp1` shared 7 of its 7 positive significant genes with the broad Elongator responses, giving cosines of `0.289` to `Elp1` and `0.244` to `Elp2`. This supports treating `Bdp1` as a weak translation-stress positive, not as evidence that every tRNA-pathway perturbation should receive a small nonzero count.

## Dalrd3-specific reasoning

### Direct biological prior

Dalrd3 is not a generic transcription factor or a central proteostasis factor; its best characterized role is as the tRNA-recognition component of the METTL2/DALRD3 m3C methyltransferase complex for selected arginine tRNAs. Lentini et al. showed that DALRD3-deficient human cells nearly lose m3C in tRNA-Arg species, and Zhang et al. showed that a DALRD3 DALR-domain missense variant impairs both METTL2 association and tRNA binding. Those results make the perturbation mechanistically real and neuron-relevant, but they point to codon/tRNA/protein-level dysregulation rather than to a guaranteed primary nuclear mRNA signature after partial acute postmitotic perturbation.

### Best within-dataset analogs

`Alkbh8`, `Nsun2`, and `Trmt1` are the closest assayed analogs by endpoint logic: all are single tRNA modification enzymes outside the Elongator core, all have plausible neurodevelopmental or stress biology, and all were fully or nearly silent in the same experiment. In `151 TH Prkcd Grin2c Glut`, each had `n_degs = 0`; across the same focal expression signatures, none induced `Asns`, `Atf4`, `Ddit3`, `Chac1`, `Slc7a5`, `Slc3a2`, `Cars`, `Mars1`, or `Herpud1` at FDR 0.05. The Distributed Agents corpus summarizes the same split as a basal-mRNA buffered branch for non-Elongator tRNA modifiers, with `Alkbh8`, `Nsun2`, and `Trmt1` not reproducing the Elongator ATF4/amino-acid program.

`Cdkal1` is a weaker but directionally consistent non-Elongator tRNA-modification comparator: it also had `n_degs = 0` in the focal group and, in the corpus, was explicitly contrasted with `Elp1`/`Elp2` as part of a divergent tRNA-modifier neighborhood.

`Bdp1` is a counterexample at the low positive boundary. It changes RNA polymerase III transcription rather than a tRNA base modification, and it produced only 8 focal DEGs, but those genes overlapped the Elongator aminoacyl-tRNA synthetase arm. This says the assay can detect a tiny tRNA-charging stress state when present. Because `Bdp1` perturbs upstream Pol III transcription more globally than Dalrd3 should, I used it as a weak upper local bound rather than as the expected Dalrd3 center.

`Elp1` and `Elp2` are strong positive controls, not direct Dalrd3 analogs. Both are core Elongator subunits in the conserved six-subunit machinery for wobble U34 modification; in this focal class they had broad ATF4/amino-acid signatures with 645 and 150 DEGs, respectively. Their response demonstrates that the screen and this neuronal class can report translational stress, but the Distributed Agents corpus found this positive state was selective for the Elongator branch and was not phenocopied by `Alkbh8`, `Nsun2`, `Trmt1`, or `Cdkal1`. Dalrd3's METTL2-dependent arginine-tRNA m3C targeting is closer to those single-writer perturbations than to loss of the upstream Elongator scaffold.

### Prediction

The best point estimate for `Dalrd3` is therefore zero DEGs. I considered assigning a small value in the `Bdp1`/`Eef2` range, but the within-dataset nearest biological analogs with single tRNA-modification activity all landed exactly at zero, and even their strongest focal stress-gene shifts had adjusted p-values far above 0.05. The disease literature raises the prior that complete DALRD3 loss matters for the nervous system, yet in this assay that prior is outweighed by the repeated observation that postnatal, partial, mosaic perturbation of non-Elongator tRNA methylation genes is mRNA-buffered.

## Limits

The strongest limitation is that `Mettl2`, the Dalrd3 catalytic partner, was not assayed, so there is no same-complex positive or negative control. The curated Distributed Agents corpus also had no Dalrd3-centered finding, and the Perturb-seq experiment measured nuclear mRNA only: it did not measure indels, DALRD3 protein, tRNA m3C stoichiometry, tRNA charging, ribosome pausing, translation, or neuronal physiology. Human DALRD3 cases are biallelic germline or inherited variants acting through development, whereas this screen was an acute, sparse, P16-to-P37/44 neuronal perturbation with modest average target-RNA downregulation. A one- or two-gene marginal response is therefore hard to exclude. The integer call of `0` should be read as "most likely no genes pass FDR 0.05 in this endpoint", not as evidence that Dalrd3 is dispensable.
