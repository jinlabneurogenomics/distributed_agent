Done. I created both required run-local outputs:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The frozen point prediction is:

```tsv
target_name	predicted_n_degs
Actb	0
```

I also ran a mechanical validation that checked:

- `trace.md` and `answer.txt` both exist.
- `answer.txt` contains only a single fenced `tsv` block.
- The TSV header is exactly `target_name	predicted_n_degs`.
- The answer has exactly one row, matching the requested manifest’s single `Actb` row.
- There are no duplicate or extra targets.
- `predicted_n_degs` parses as a non-negative integer.