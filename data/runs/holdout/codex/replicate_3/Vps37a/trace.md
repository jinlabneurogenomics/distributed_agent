# Vps37a 151 TH Prkcd Grin2c Glut DEG-count forecast

## Target and direct endpoint

- Target: `Vps37a`, from the declared one-row holdout manifest.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The count table contains 1,674 visible training perturbations for this cell class. Its distribution is very sparse: 1,205/1,674 targets are zero, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the 95th percentile is 18.

## Biology bundle used

`Vps37a` is well expressed in the focal non-target population: 23,163/23,679 nuclei express the target, mean raw UMI is 5.12, and mean CP10K is 3.29. This makes the target present in the assayed class, although target RNA abundance is not an editing-efficiency readout.

The biology-only bundle supports reachable postnatal biology but with imperfect assay matching. VPS37A is a renewable ESCRT-I family subunit with a separable UEVL-dependent autophagosome-closure role; the functional-stock adjudication judged VPS37A-specific stock likely substantially depleted after the 21-28 day P16-to-harvest interval. The closest in vivo timing evidence is the Vps37a UEVL-domain mouse mutant, where postnatal neurological and brain pathology emerged by about two weeks, but that model is germline/systemic and not a P16 thalamic neuron null. Other VPS37-family subunits can occupy ESCRT-I, and no matched thalamic-neuron compensation test is available.

## Training perturbations selected and measured

I used typed gene-analog nomination against the exact 1,674-gene training universe. It found 1,080 training-available Vps37a analogs, but only one non-fallback ESCRT candidate:

| candidate | relationship to Vps37a | 151 `n_degs` |
|---|---|---:|
| Chmp4b | Reactome ESCRT member plus STRING physical relationship | 0 |
| Vps54 | broad vacuole/membrane-trafficking annotation | 31 |
| Vps41 | broad late-endosome/vacuole annotation | 0 |
| Rab7 | broad late-endosome/endocytosis annotation | 501 |
| Vps35 | broad endocytosis/retromer context | 17 |
| Dctn1 | graph-supported trafficking context | 75 |
| Wdfy3 | autophagy-adjacent broad context | 17 |
| Cltc | endocytosis context | 3 |
| Atg16l1 / Atg5 / Becn1 / Lamp2 | autophagy/lysosome checks | 0 / 0 / 0 / 0 |
| Sqstm1 | autophagy/lysosome check | 1 |

The 151-class parquet rows for these candidates all had 17,259 measured features. The matched perturbed-nucleus counts for the closest scale anchors were adequate for this table (`Chmp4b` 129, `Vps41` 159, `Vps54` 161, `Vps35` 133, `Dctn1` 182, `Rab7` 215). Among the 21 endolysosomal/autophagy candidates profiled symmetrically, the response activity buckets were: 14 with no significant genes, 2 with 1-9, 3 with 10-49, and 2 with at least 50. Thus the local training evidence is dominated by null or small responses, with `Rab7` as a broad upper-tail outlier rather than a direct ESCRT donor.

## Same-experiment interpretation of the measured comparators

The packaged Findings support the same separation seen in the count table:

- `Chmp4b` did not form a robust recurrent ESCRT/autophagy/cargo signature with data-driven or literature-obvious comparators, and its only FDR-level output in the corpus was a one-gene event outside the focal thalamic class.
- `Rab7` induced a strong late-endosomal/lysosomal compensation program plus a sterol/lipid branch; this establishes that the 151 class can show large endolysosomal stress, but `Rab7` is a hub GTPase failure with a far broader state than Vps37a should be assigned by default.
- `Vps35` and `Vps54` were thalamus-biased, modest endomembrane-trafficking responses. `Vps35` lacked a bulk lysosomal program, and `Vps54` lacked the UPR/ISR, proteasome, lysosomal hydrolase, and sphingolipid transcripts seen in severe late-endosomal stress.
- Explicit Finding-reference topology over the top 20 nominated analogs left `Chmp4b` isolated, while `Rab7`, `Vps35`, `Vps41`, `Vps54`, and `Dctn1` occupied a connected trafficking cluster. That topology makes the broad cluster useful as scale context, not as evidence that the ESCRT candidate should inherit the full Rab7 response.

## Synthesis

I placed `Vps37a` above the table median because the target is present in almost every focal neuron and the biology bundle argues that an acute disruptive edit should deplete a VPS37A-specific ESCRT/autophagosome-closure function within the experimental window. I placed it well below `Rab7` and below `Dctn1` because the nearest visible ESCRT perturbation was flat in 151, basal autophagy/lysosomal checks were mostly flat, and the modest `Vps35`/`Vps54` states are the better scale references for partial endomembrane trafficking stress.

The resulting point forecast is a modest, just-sub-95th-percentile response close to the `Vps35`/`Wdfy3`/`Vps54` range:

`predicted_n_degs = 18`
