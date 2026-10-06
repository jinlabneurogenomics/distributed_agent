Created the required outputs:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Nme7	0
```

I validated that `answer.txt` is exactly one `tsv` fenced block, has the required `target_name` and `predicted_n_degs` columns, contains the single requested target exactly once in requested order, and uses a non-negative integer prediction.