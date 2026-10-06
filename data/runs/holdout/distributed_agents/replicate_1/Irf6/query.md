Created both requested deliverables in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final point prediction is:

```tsv
target_name	predicted_n_degs
Irf6	0
```

I also mechanically validated the output contract:

- `trace.md` exists.
- `answer.txt` exists.
- `answer.txt` contains exactly one fenced `tsv` block and no outside prose.
- Header is exactly `target_name	predicted_n_degs`.
- Row count matches the requested-target CSV: `1`.
- Target order is preserved: `Irf6`.
- No duplicate or extra targets are present.
- `predicted_n_degs` is a non-negative integer.