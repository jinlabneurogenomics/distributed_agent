Created the required run outputs:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Pi4ka	1
```

I mechanically validated `answer.txt` against the requested-target CSV: the fenced block is `tsv`, the header is exact, it contains exactly one row, the target is exactly `Pi4ka` in manifest order, there are no duplicates or extras, and `predicted_n_degs` is a nonnegative integer.