Created both requested outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The single held-out target was `Foxp1`, and the final point prediction is:

```tsv
target_name	predicted_n_degs
Foxp1	0
```

I verified the required mechanics:

- `trace.md` exists.
- `answer.txt` exists.
- `answer.txt` contains only one fenced `tsv` block.
- The TSV header is exactly `target_name	predicted_n_degs`.
- It has exactly one data row, matching the one requested target.
- Requested target order is preserved.
- There are no duplicate or extra targets.
- `predicted_n_degs` is a non-negative integer.