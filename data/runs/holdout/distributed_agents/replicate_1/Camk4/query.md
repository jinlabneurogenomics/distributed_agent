Created both requested outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Camk4	8
```

I validated the required output shape mechanically:

- `answer.txt` contains exactly one fenced `tsv` block and no extra prose.
- The header is exactly `target_name	predicted_n_degs`.
- It has exactly one data row, matching the sole requested target `Camk4`.
- Requested order is preserved.
- There are no duplicate or extra targets.
- `predicted_n_degs` is a non-negative integer.