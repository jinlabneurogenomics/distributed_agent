Created both requested outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Nfkb2	0
```

I validated the output contract mechanically:

- `trace.md` exists.
- `answer.txt` contains exactly one fenced `tsv` block.
- The table header is exactly `target_name	predicted_n_degs`.
- It has exactly one data row, matching the one requested target.
- `Nfkb2` is emitted once, in requested-target order.
- `predicted_n_degs` is a non-negative integer.