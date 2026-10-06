Created both requested outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

I predicted:

```tsv
target_name	predicted_n_degs
Gpr12	0
```

I also mechanically checked `answer.txt`: it contains exactly one `tsv` fenced block, the required two-column header, one row, no duplicate target, `Gpr12` in the requested manifest order, and a non-negative integer prediction.