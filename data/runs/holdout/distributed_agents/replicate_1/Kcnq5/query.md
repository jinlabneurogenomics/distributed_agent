Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

I predicted `Kcnq5` as a one-DEG perturbation in `151 TH Prkcd Grin2c Glut`, driven by transfer from the closest screened neuronal Kv7 analogs:

- `Kcnq2`: focal `n_degs = 1`, the self-transcript only; `Agap2` was just outside the requested FDR cutoff at `pvals_adj = 0.050867`.
- `Kcnq3`: focal `n_degs = 1`, the self-transcript only; no focal downstream gene even at FDR 0.10.
- `Kcnq1`: focal and all-cell null, used as a non-neuronal Kv7 counterexample.
- Most screened voltage-gated K, HCN, and sodium-channel perturbations in the focal class were also 0 or 1 DEG, arguing against promoting `Kcnq5` to a broad transcriptional-response count.

I also validated `answer.txt` mechanically:

- exactly one fenced `tsv` block
- exact header `target_name	predicted_n_degs`
- 1 answer row matching the 1 requested target
- requested order preserved
- no duplicate targets
- non-negative integer prediction
- no prose outside the fenced block