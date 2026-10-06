Created both required outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Rbfox1	8
```

I mechanically checked that:

- `trace.md` and `answer.txt` both exist.
- `answer.txt` contains only a single fenced `tsv` code block.
- The TSV header is exactly `target_name	predicted_n_degs`.
- There is exactly one data row.
- `Rbfox1` appears exactly as in the requested-target CSV and in the same order.
- There are no duplicate or extra targets.
- `predicted_n_degs` is a non-negative integer.