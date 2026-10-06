# Ppargc1b n_degs forecast

Target: `Ppargc1b`

Cell population: `151 TH Prkcd Grin2c Glut`

## Evidence used

- The declared one-row manifest names `Ppargc1b`; it is absent from the 1,674-row
  151-class training count table.
- In the declared biology bundle, `Ppargc1b` is measured in the focal
  non-target population with `mean_raw_umi = 1.022`, `mean_log1p_cp10k = 0.407`,
  `pseudobulk_cpm = 64.058`, and expression in `13,862 / 23,679` nuclei
  (`58.54%`). This makes loss reachable in the assayed population but also
  implies dilution by target-negative or weakly expressing nuclei.
- The same bundle adjudicates PGC-1beta as a dynamic nuclear coactivator rather
  than a long-lived installed structure and calls functional stock at the P37-
  P44 harvest `likely_substantially_depleted` after a P16 edit. The useful
  prior phenotype evidence is mitochondrial and stress-program alteration in
  germline mouse brain; its caveat is that it is not an acute postnatal thalamic
  deletion. Ppargc1a is a plausible buffer, but available evidence makes that
  buffering tissue-dependent rather than complete.
- The focal count table is highly zero-inflated: 1,205 of 1,674 training targets
  have `n_degs = 0`; the median is 0, the 75th percentile is 1, the 90th
  percentile is 2, and the 95th percentile is 18.
- The closest same-family training perturbations in the focal count table were
  quiet: `Ppargc1a = 0`, `Ppara = 0`, `Ppard = 0`, and `Pparg = 0`.
- Direct ERR/NRF mitochondrial-transcription comparators showed that this axis
  can be visible but is not uniformly strong: `Esrra = 57`, `Nrf1 = 138`,
  `Esrrb = 0`, and `Esrrg = 0`.
- Adjacent stress or mTOR-linked comparators were mostly smaller than the direct
  ERR/NRF hits: `Creb1 = 10`, `Crebbp = 8`, `Mtor = 2`, and `Tsc2 = 86`.
- Core respiratory-chain perturbations were usually silent in this cell class:
  35 `Cox*`, `Nduf*`, `Uqcr*`, `Tomm40`, and `Slc25*` targets had mean
  `n_degs = 0.429` and median 0.
- A profile comparison in `151 TH Prkcd Grin2c Glut` confirmed the exact
  Parquet-derived significant-feature counts for the key comparators:
  `Ppargc1a = 0`, `Esrra = 57`, `Nrf1 = 138`, `Tsc2 = 86`, and `Creb1 = 10`.
  `Esrra` and `Nrf1` shared only two significant negative genes and no
  significant positive genes, so I treated them as evidence for observability of
  the broader mitochondrial regulatory axis rather than as a single coherent
  footprint to transfer at full strength.

## Synthesis

`Ppargc1b` is present in enough focal nuclei, and its coactivator stock should
turn over within the 21-28 day editing window, so a pure null forecast would
underuse the biology bundle. But the response should be well below `Nrf1` or
`Esrra`: PGC-1beta is a partially redundant coactivator, not the DNA-binding
ERR/NRF machinery itself; the most direct assayed PGC/PPAR comparators have
zero DEGs; and the mitochondrial structural genes that the pathway regulates
are mostly quiet when perturbed individually in this recovered-cell endpoint.

I therefore forecast a low nonzero burden, close to the weak CREB/stress
comparators and below the 95th percentile of the full training distribution:

`predicted_n_degs = 10`
