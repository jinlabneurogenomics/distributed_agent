Created both required outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Dalrd3	0
```

I validated that `answer.txt` is exactly one `tsv` fenced block, has the required `target_name`/`predicted_n_degs` columns, contains exactly the one requested target in manifest order, has no duplicate targets, and uses a non-negative integer prediction.