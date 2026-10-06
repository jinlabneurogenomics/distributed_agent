## Target

- Manifest target: `Zbtb11`
- Forecasted endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as the count of measured genes with Wilcoxon `pvals_adj < 0.05`
- Biological identity used for the forecast: the declared bundle maps this perturbation to GeneID 68193 / ENSMUSG00000098274, the `Rpl24` locus historically aliased `Zbtb11`, not to the separate current Zbtb11 transcription-factor locus.

## Evidence Used

### Target biology

- Exact focal reach was adequate for an effect to be observable but not close to universal: in non-target nuclei from `151 TH Prkcd Grin2c Glut`, the target feature was available in 15,795 / 23,679 nuclei, or 66.704675% of cells, with mean CP10K 0.772021 and mean raw UMI 1.246505.
- The perturbation should remove new RPL24 supply but not the pre-edit stock already assembled into mature 60S subunits. The declared functional-stock card adjudicated RPL24 stock as `likely_substantially_depleted` by harvest because neuronal ribosomal-protein renewal averages about 8 days and the 21-28 day assay window spans several renewal intervals, but it explicitly retained partial evidence and a long-lived pre-edit ribosome tail.
- RPL24 is a core cytosolic 60S ribosomal subunit component. The biology therefore supports postnatal neuronal relevance, but it does not specify a particular secondary mRNA state in thalamic recovered nuclei.

### Training counts in the focal class

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 training perturbations. Its distribution is very sparse:

- median = 0
- 75th percentile = 1
- 90th percentile = 2
- 95th percentile = 18
- 99th percentile = 436.48
- maximum = 2,677
- zero fraction = 0.7198

The closest measured ribosome/RNA-biogenesis and translation anchors were low or null at the exact requested `pvals_adj < 0.05` endpoint:

| training set | target counts in `151 TH Prkcd Grin2c Glut` | summary |
| --- | --- | --- |
| Ribosome/RNA-biogenesis adjacent | `Nop56` 25, `Polr3b` 8, `Rbm28` 0, `Las1l` 0, `Taf1b` 0 | mean 6.6, median 0, max 25 |
| Translation-factor adjacent | `Eef2` 9, `Eif4a2` 2, `Eif4g1` 1, `Eif4h` 1, `Eif5a` 0, `Eif2ak4` 0 | mean 2.17, median 1, max 9 |

The huge responses in the same class were from broader stress-essential targets rather than direct ribosomal subunits: for example `Uba5` had 2,677 DEGs, `Tpr` 1,768, `Sin3a` 1,433, `Rnpc3` 868, `Psmb4` 742, and `Hnrnpu` 733.

### Same-experiment corpus and profile checks

I did not query the same-experiment corpus for the held-out `Zbtb11` report. I used packaged summaries and a fresh profile comparison only for measured training perturbations.

- `Nop56` was the best ribosome-biogenesis positive anchor. Packaged findings describe it as a narrow, cell-type-restricted perturbation: all 23 groups were measured at the report threshold, only 4 had any downstream FDR-significant genes, and most were concentrated in `151 TH Prkcd Grin2c Glut`. In the exact `pvals_adj < 0.05` count table its focal count is 25.
- `Rbm28` and `Las1l` were useful lower bounds. `Rbm28` had no downstream FDR response across measured brain groups in its packaged report, and the Rbm28 report explicitly contrasted flat `Rbm28`/`Las1l` with modest `Nop56`, showing that same broad 60S/rRNA-processing biology was not sufficient to make a robust postnatal neuronal mRNA footprint.
- `Polr3b` and `Eef2` supported the same factor-specific pattern. `Polr3b` produced a sparse response rather than a broad Pol III or transcription-production shutdown signature, with 8 DEGs at the requested focal threshold. `Eef2`, despite being a core translation elongation factor with large responses in some other neuronal groups, had only 9 DEGs in the focal thalamic class and belongs to a corpus claim that represented translation-control perturbations did not form a generic shared nuclear mRNA signature.
- A profile comparison over the focal class found the same scale separation. In the comparison cohort, `Nop56` had 25 significant features, `Polr3b` 8, `Eef2` 9, and `Rbm28`, `Las1l`, `Taf1b`, `Eif5a`, and `Eif2ak4` were null, whereas `Uba5` had 2,677. The Nop56-vs-UFMylation/proteasome similarities were partial rather than a scaled copy of the giant stress footprints: `Nop56` versus `Ufc1` had Pearson 0.333 and 11 same-direction significant overlaps, while `Nop56` versus `Hnrnpu` had near-zero whole-profile similarity and 6 significant direction conflicts.

## Synthesis

The target is not a generic low-expression or unreachable case: Rpl24 is detected in two thirds of the focal non-target nuclei, and the 3-4 week window should erode much of the renewable RPL24-bearing ribosome stock. That argues against borrowing the screen-wide median of zero.

At the same time, the best available direct training evidence keeps the forecast far below the high-count stress tail. The available same-class perturbations around ribosome biogenesis, Pol III output, and translation repeatedly show sparse or absent mRNA effects in recovered postnatal neurons. `Nop56` is the strongest close positive at 25 DEGs; `Rbm28`, `Las1l`, and `Taf1b` show that nearby ribosome-production lesions can be completely buffered or survivor-filtered; and `Eef2` shows that a core translation factor can be highly context dependent with only a 9-gene footprint in this thalamic class.

I therefore placed `Zbtb11`/`Rpl24` just below the strongest focal Nop56 anchor and near the 95th percentile of the training distribution: enough for a small real thalamic response from a mature 60S ribosomal-protein lesion, but not enough to treat it like `Uba5`, `Ufc1`, proteasome, or spliceosome perturbations.

Final point prediction: 18 DEGs.
