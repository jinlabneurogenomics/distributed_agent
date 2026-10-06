Created the two required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Zfp799	0
```

I verified `answer.txt` mechanically:

- single fenced `tsv` block
- exact header `target_name	predicted_n_degs`
- exactly one row
- `Zfp799` matches the requested-target CSV and preserves its order
- no duplicate targets
- `predicted_n_degs` is a non-negative integer
- no prose outside the fenced block