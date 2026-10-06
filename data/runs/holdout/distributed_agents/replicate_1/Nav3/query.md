Created both requested outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final TSV is:

```tsv
target_name	predicted_n_degs
Nav3	1
```

I also mechanically validated that:

- `trace.md` and `answer.txt` exist.
- `answer.txt` contains only a single fenced `tsv` block.
- The table header is exactly `target_name	predicted_n_degs`.
- There is exactly 1 data row.
- The sole target is `Nav3`, matching the requested-target CSV and preserving order.
- The prediction is a non-negative integer.
- There are no duplicate or extra targets.