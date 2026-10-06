Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Pdhx	0
```

I mechanically validated that `answer.txt` contains a single fenced `tsv` block, uses the exact required header, includes the sole requested manifest target `Pdhx` exactly once in order, and has a non-negative integer prediction.