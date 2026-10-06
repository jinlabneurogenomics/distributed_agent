Created both required outputs in the run directory:

- [trace.md](./trace.md) contains the target-specific reasoning for `Prokr2`, including the focal-cell training-count distribution, within-dataset GPCR/GnRH-development analogs and counterexamples, expression evidence from the declared parquet, PubMed-cited `PROK2`/`PROKR2` biology, and the uncertainty around transferring developmental or SCN phenotypes into an acute postnatal thalamic Perturb-seq DEG count.

- [answer.txt](./answer.txt) contains exactly the requested single fenced `tsv` block:
  `Prokr2	0`

I also mechanically validated `answer.txt` against the requested-target CSV: 1 requested row, 1 answer row, exact `target_name` spelling/order preserved, no duplicates, required `target_name	predicted_n_degs` header, and a non-negative integer prediction.