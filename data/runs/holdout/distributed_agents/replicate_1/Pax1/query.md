Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final point prediction is:

```tsv
target_name	predicted_n_degs
Pax1	0
```

I also mechanically checked that `answer.txt`:

- contains only a single fenced `tsv` block
- has the exact required header
- has exactly one data row
- preserves the requested target order from `the single-target request`
- contains no duplicate or extra targets
- uses a non-negative integer prediction
- is ASCII and newline-terminated