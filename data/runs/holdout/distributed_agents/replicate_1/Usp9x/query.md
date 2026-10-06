Created both requested outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Usp9x	5
```

I validated the answer file mechanically:

- `answer.txt` contains exactly one fenced `tsv` block and no prose outside it.
- Header is exactly `target_name	predicted_n_degs`.
- It has exactly one data row, matching the one requested target.
- Target order matches `the single-target request`.
- No duplicate targets are present.
- `predicted_n_degs` is a non-negative integer.
- `trace.md` was written and is nonempty.