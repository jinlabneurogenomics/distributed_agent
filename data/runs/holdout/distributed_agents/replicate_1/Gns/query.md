Created both requested outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Gns	0
```

I also mechanically validated that `answer.txt` contains exactly one fenced `tsv` block, has the required two columns, preserves the requested target order, includes `Gns` exactly once, has no extra targets, and uses a non-negative integer prediction.