Created the required outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Thoc2	303
```

I validated that `answer.txt` contains exactly one fenced `tsv` block, the required header, exactly one row matching the requested-target manifest in order, no duplicate targets, and a non-negative integer prediction.