## Target and endpoint

- Holdout target: `Tacr1`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- The expression Parquet and the `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` count table are training-only for this target; the held-out `Tacr1` response was not consulted.

## Biology used

The canonical Tacr1 biology bundle identifies the perturbed product as NK1, a substance-P-activated membrane GPCR. The functional-stock card adjudicates the P16-to-P37/P44 loss-of-function as likely to deplete signaling-competent receptor in successfully edited cells: existing receptors are not directly inactivated by a DNA edit, but NK1 is dynamically trafficked rather than an installed durable product, and adult neuron-specific Tacr1 CRISPR outside thalamus can nearly abolish the substance-P firing response.

That supports possible target engagement, but the exact focal-population reach is very small. In matched non-target `151 TH Prkcd Grin2c Glut` nuclei, `Tacr1` had:

- `n_cells_expressing = 628` of `23,679`
- `pct_cells_expressing = 2.6521`
- `mean_raw_umi = 0.0331`
- `mean_cp10k = 0.0215`
- `pseudobulk_cpm = 2.0724`

So any cell-autonomous Tacr1 loss should be diluted across a largely Tacr1-negative thalamic aggregate unless it propagates through a recurrent network state. I did not find a same-experiment Tacr1 Finding or Claim in the July corpus that would establish such a propagated state.

## Training measurements used

The blinded same-cell training count table contained 1,674 perturbations:

- median `n_degs = 0`
- mean `n_degs = 14.05`
- 1,205 / 1,674 had zero DEGs
- 1,546 / 1,674 had at most five DEGs
- the right tail was dominated by broad regulators such as `Uba5`, `Tpr`, `Sin3a`, spliceosome/proteasome factors, chromatin regulators, and core trafficking/metabolic genes

I treated that full-table tail as a poor quantitative match for Tacr1 because Tacr1 is a sparsely expressed modulatory receptor, not a ubiquitous essential or nuclear regulatory factor.

For a focused receptor-class comparison, I checked the count table and exact `151 TH Prkcd Grin2c Glut` Parquet rows for 50 training perturbations covering tachykinin, somatostatin, neuropeptide-Y, serotonin, dopamine, adrenergic, CCK, opioid, neurotensin, metabotropic glutamate, GABA-B, GABA-A, and nicotinic receptor genes. In the Parquet each had the full 17,259 measured-gene focal signature and the same 23,679 matched non-target controls. Their DEG counts were:

- 42 / 50 were zero
- six were one-DEG self-transcript hits only: `Chrnb2`, `Gabbr1`, `Gabbr2`, `Gabra1`, `Grm1`, `Grm7`
- `Chrna4` had two DEGs, its own transcript plus `Cyp46a1`
- `Gabrb2` had four DEGs, its own transcript plus `Nr4a1`, `Vgf`, and `Nalf1`
- the maximum among these selected receptor comparators was therefore four

The closest tachykinin-family measured comparator, `Tacr3`, had zero DEGs in the focal class; other neuropeptide receptors with zero included `Sstr5`, `Npy1r`, `Npy2r`, `Npy5r`, `Cckar`, `Cckbr`, `Oprd1`, `Oprk1`, `Oprl1`, `Oprm1`, and `Ntsr1`.

## Synthesis

The biology bundle makes a functional Tacr1 perturbation plausible in edited Tacr1-positive cells, so I did not force a structural no-effect prior. The forecast is nevertheless anchored near the receptor-comparator mode because the assay averages sparse, mosaic perturbations over the whole recovered thalamic class. With only 2.65% of non-target nuclei expressing detectable Tacr1 at baseline, a cell-autonomous signature would likely be present in too few perturbed nuclei to clear BH FDR unless Tacr1 loss created a broader activity or paracrine state; the biology bundle and the corpus supplied no direct evidence for that broader state in this thalamic endpoint.

Most analogous receptor perturbations were exactly zero, and the few one-DEG receptor cases were usually significant self-knockdown rows. Tacr1's very low focal expression makes even a self-transcript hit less likely than for those broader receptor subunits. I therefore predict no FDR-significant measured genes:

`predicted_n_degs = 0`
