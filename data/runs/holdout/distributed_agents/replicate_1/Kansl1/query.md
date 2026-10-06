Created the requested deliverables in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Kansl1	0
```

I validated the required output shape mechanically:

- `trace.md` and `answer.txt` both exist.
- `answer.txt` contains exactly one fenced `tsv` block and no prose.
- The TSV has the exact header `target_name	predicted_n_degs`.
- It has exactly one row, matching the one requested target.
- `Kansl1` is present exactly once and in requested-manifest order.
- `predicted_n_degs` is a non-negative integer.