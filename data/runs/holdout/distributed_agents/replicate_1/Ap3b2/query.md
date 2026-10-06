Created both required deliverables in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The single requested target was `Ap3b2`, and the final point prediction is:

```tsv
target_name	predicted_n_degs
Ap3b2	0
```

I validated that:

- `trace.md` and `answer.txt` both exist.
- `answer.txt` contains only one fenced `tsv` block.
- The TSV header is exactly `target_name	predicted_n_degs`.
- The TSV has exactly one data row.
- The row matches the requested-target CSV order exactly.
- There are no duplicate or extra targets.
- `predicted_n_degs` is a non-negative integer.