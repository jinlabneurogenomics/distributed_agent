Created the requested deliverables in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Slc12a5	1
```

I validated that `answer.txt` contains exactly one fenced `tsv` block, preserves the requested manifest order, includes the single requested target exactly once, and has a non-negative integer `predicted_n_degs`.