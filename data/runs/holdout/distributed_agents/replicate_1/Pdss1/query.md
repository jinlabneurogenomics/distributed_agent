Created both required outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Pdss1	0
```

I also mechanically checked that:

- `trace.md` and `answer.txt` exist.
- `answer.txt` contains a single `tsv` fenced block and no prose outside it.
- the TSV header is exactly `target_name	predicted_n_degs`.
- there is exactly 1 data row, matching the 1 requested target.
- `Pdss1` appears exactly once and in requested-target order.
- `predicted_n_degs` is a non-negative integer.