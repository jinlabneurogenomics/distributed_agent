Created both requested files in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Rara	0
```

I validated that:

- `answer.txt` contains only one fenced `tsv` block.
- Its header is exactly `target_name	predicted_n_degs`.
- It has exactly one data row.
- The row matches the requested manifest exactly and preserves order: `Rara`.
- The prediction is a non-negative integer.
- There are no duplicate or extra targets.
- Both `trace.md` and `answer.txt` are present and ASCII-only.