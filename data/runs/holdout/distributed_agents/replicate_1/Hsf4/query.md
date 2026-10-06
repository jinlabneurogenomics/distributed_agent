Created the requested prediction outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final point prediction is:

```tsv
target_name	predicted_n_degs
Hsf4	0
```

I also mechanically checked the answer format against the requested-target manifest:

- both required files exist
- `answer.txt` contains exactly one fenced `tsv` block and no surrounding prose
- header is exactly `target_name	predicted_n_degs`
- row count is `1`, matching the manifest
- target order is preserved: `Hsf4`
- no duplicate or extra targets
- `predicted_n_degs` is a non-negative integer