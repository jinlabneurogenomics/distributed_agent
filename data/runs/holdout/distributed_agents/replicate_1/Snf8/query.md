Created both requested deliverables in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Snf8	0
```

I validated that `answer.txt` contains exactly one fenced `tsv` block, has the required `target_name` and `predicted_n_degs` columns, includes the one requested target exactly once in requested order, and uses a non-negative integer prediction.