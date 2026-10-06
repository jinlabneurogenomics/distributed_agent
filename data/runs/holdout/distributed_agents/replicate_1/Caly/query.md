Created both required outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

Final point prediction:

```tsv
target_name	predicted_n_degs
Caly	0
```

I also mechanically checked `answer.txt` for:

- exactly one `tsv` fenced block
- exact header `target_name	predicted_n_degs`
- one row for the one requested target
- requested target order preserved
- no duplicate, missing, or extra targets
- non-negative integer prediction