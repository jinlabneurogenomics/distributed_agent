Created the required outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

I predicted:

```tsv
target_name	predicted_n_degs
Ddr2	0
```

I also mechanically validated `answer.txt`: it contains exactly one fenced `tsv` block, the required two-column header, exactly one data row, `Ddr2` in the requested manifest order, no duplicates, and a non-negative integer prediction.