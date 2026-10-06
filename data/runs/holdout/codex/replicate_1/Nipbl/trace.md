# Nipbl forecast trace

## Target and endpoint

- Holdout manifest target: `Nipbl`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Predicted endpoint: `n_degs`, the count of measured genes in this class with Wilcoxon `pvals_adj < 0.05`.

## Evidence used

- The declared canonical `Nipbl` biology bundle reports no target outcome and no labeled neighbors. Its exact focal-population expression row shows `Nipbl` is measured in the assay and broadly reachable in matched non-target nuclei: 20,373 of 23,679 nuclei expressed `Nipbl` in `151 TH Prkcd Grin2c Glut` (`86.0%`), with mean raw UMI `2.34` and pseudobulk CPM `146.6`.
- The same bundle adjudicates NIPBL as a dynamic cohesin loader/ATPase activator whose functional stock should clear inside the P16-to-P37/P44 screen window. Acute degradation evidence supports loss of many NIPBL-dependent loops within hours, and no close mammalian replacement loader was found in the bounded source-card search. This makes a realized post-edit effect plausible rather than expression-limited.
- The selected same-experiment corpus had no `Nipbl` Findings, Claims, or explicit references, so no held-out `Nipbl` profile information was exposed from the report layer.
- The declared training count table contains 1,674 measured training perturbations for this exact class. It is sparse: 1,205 targets have `0` DEGs, only 106 have at least 10, 69 have at least 25, and 59 have at least 50; the mean is `14.05` but the distribution is strongly right-skewed.
- Closest measured cohesin comparators are limited but informative at the exact endpoint:
  - `Smc1a`: `24` DEGs.
  - `Stag2`: `37` DEGs.
  - `Stag1`, `Pds5a`, `Hdac8`, and `Ncapd3`: `0` DEGs at this `pvals_adj < 0.05` endpoint.
  - `Mau2`, `Rad21`, `Smc3`, and `Wapl` are absent from the training-count table and were treated as missing rather than zero.
- Parquet profile inspection over the selected training cohort confirmed that `Smc1a` and `Stag2` are small but real, down-biased signatures rather than broad stress states: `Smc1a` has 24 significant genes, 21 down and 3 up; `Stag2` has 37 significant genes, 29 down and 8 up. They are each other's strongest whole-profile match within the selected cohort, with Pearson `0.264`, cosine `0.266`, 8 shared significant down-regulated genes, and 1 shared significant up-regulated gene.
- Packaged Findings for the represented cohesin axis agree with the direct profile read: `Smc1a` and `Stag2` share a restricted same-direction thalamic module, while `Stag1`, `Pds5a`, `Hdac8`, and `Ncapd3` are flat or divergent in the same context. The same Findings note that `Ctcf`, `Brd4`, `Ctnnb1`, `Psmb4`, `Uba5`, and `Sin3a` can overlap slices of the `Smc1a`/`Stag2` module but each carries hundreds to thousands of DEGs in this class, so they are broad upper-scale context rather than close NIPBL scale donors.

## Synthesis

NIPBL loss should be visible if editing removes protein in cells that survive recovery: the gene is expressed across most matched thalamic glutamatergic nuclei, the operative protein stock is dynamic, and the target is the upstream loader for cohesin complexes rather than a weak late accessory step. That made a strict zero forecast too low.

The measured profile neighborhood, however, argues against projecting a `Ctcf`-, `Brd4`-, or proteostasis-sized response. The closest on-cohesin training perturbations with a real 151 signal, `Smc1a` and `Stag2`, sit at only 24 and 37 DEGs, and several pathway-near perturbations are exact endpoint nulls. I therefore treated the `Smc1a`/`Stag2` 24 to 37 range as the main quantitative bracket, with the null relatives as a downward boundary and the high `Nipbl` reach/no-replacement prior as a modest upward bearing within that bracket.

The arithmetic midpoint of the two active core-cohesin counts is 30.5. After rounding and leaving the opposing high-reach and null-boundary bearings essentially balanced, my point prediction is:

`predicted_n_degs = 31`
