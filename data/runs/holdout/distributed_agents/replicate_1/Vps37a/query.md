Created both required outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Vps37a	0
```

I also mechanically validated that `answer.txt` is a single fenced `tsv` block, has exactly the two required columns, contains exactly one row, preserves the requested manifest order, has no duplicate targets, and uses a non-negative integer prediction.