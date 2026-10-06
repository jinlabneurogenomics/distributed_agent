Created both requested outputs:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final point prediction is:

```tsv
target_name	predicted_n_degs
Atp6v0c	1
```

I also mechanically validated that `answer.txt` is exactly one fenced `tsv` block, has the required header, preserves the requested-target order, contains exactly one row for the one requested held-out gene, has no duplicate or extra targets, and uses a nonnegative integer prediction.