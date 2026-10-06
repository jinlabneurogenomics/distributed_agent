Created both requested outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

I used `Tbcd` as the primary held-in analog for `Tbce`, with focal-cell tubulin, MAP, kinesin, and `Dctn1` perturbations as scale-setting counterexamples, and wrote the final prediction as:

```tsv
target_name	predicted_n_degs
Tbce	12
```

I also mechanically validated that `answer.txt` is exactly one fenced `tsv` block, contains the required two columns, has one row, preserves the requested `Tbce` order, has no duplicate or extra targets, and uses a non-negative integer prediction.