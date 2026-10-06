Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The prediction is:

```tsv
target_name	predicted_n_degs
Hmgb1	0
```

I validated the required mechanics after writing the files:

- both required filenames exist
- `answer.txt` contains only one fenced `tsv` block
- the TSV header is exactly `target_name	predicted_n_degs`
- row count is `1`, matching the requested-target CSV
- `Hmgb1` is present exactly once and in requested order
- `predicted_n_degs` is a non-negative integer
- the requested target has no overlap with the training DEG-count CSV