Created both required deliverables in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final TSV prediction is:

```tsv
target_name	predicted_n_degs
Drd3	0
```

I validated that `answer.txt` contains exactly one fenced `tsv` block, preserves the requested target order, has one row for the one requested target, has no duplicates or extra targets, and uses a non-negative integer prediction.