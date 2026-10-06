Created the requested outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Pdhb	1
```

I validated that `answer.txt` is exactly one `tsv` fenced block, has the required `target_name` / `predicted_n_degs` header, contains exactly one row, preserves the requested manifest order for `Pdhb`, has no duplicate or extraneous targets, and uses a non-negative integer prediction.