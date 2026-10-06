Created both requested outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Bbip1	0
```

I validated that `answer.txt`:

- contains only a single fenced `tsv` block,
- has exactly the required `target_name` and `predicted_n_degs` columns,
- contains exactly one row,
- preserves the requested target order,
- has no duplicate targets,
- uses the exact requested `Bbip1` spelling,
- and reports a non-negative integer prediction.