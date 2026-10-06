Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Sp4	2
```

I also mechanically validated that:

- `answer.txt` contains exactly one fenced `tsv` block and no prose outside it.
- The header is exactly `target_name	predicted_n_degs`.
- The requested target order is preserved.
- `Sp4` appears exactly once and no extra targets are present.
- `predicted_n_degs` is a non-negative integer.