Created both required outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Dock7	0
```

I validated the deliverable mechanics after writing:

- `trace.md` exists and is non-empty.
- `answer.txt` contains only one fenced `tsv` block.
- The TSV header is exactly `target_name	predicted_n_degs`.
- It has exactly one data row, matching the single requested target `Dock7`.
- The requested-target order is preserved.
- `Dock7` is unique.
- `predicted_n_degs` is a non-negative integer.