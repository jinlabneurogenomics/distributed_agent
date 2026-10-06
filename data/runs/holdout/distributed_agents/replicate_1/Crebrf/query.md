Created both requested outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

I predicted `Crebrf` as below the focal FDR 0.05 detection threshold:

```tsv
target_name	predicted_n_degs
Crebrf	0
```

Validation passed: `answer.txt` is exactly one fenced `tsv` block, has the required two columns, has exactly one row, preserves the requested manifest order, contains no duplicate or extra targets, and has a non-negative integer prediction.