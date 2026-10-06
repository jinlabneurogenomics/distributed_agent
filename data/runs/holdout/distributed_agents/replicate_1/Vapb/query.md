Created both required outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Vapb	0
```

I validated that `answer.txt` contains exactly one fenced `tsv` block, uses the required `target_name	predicted_n_degs` header, includes every requested target exactly once in manifest order, contains no extra targets or duplicate rows, and uses a non-negative integer prediction.