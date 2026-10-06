Created both requested outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final point prediction is:

```tsv
target_name	predicted_n_degs
Pcdh15	0
```

I validated that `answer.txt` contains exactly one `tsv` fenced block, has the exact required `target_name	predicted_n_degs` header, preserves the requested-target manifest order, includes the single requested target exactly once, and uses a non-negative integer prediction.