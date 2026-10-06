Created both requested outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Kdm6a	0
```

I also mechanically validated that `answer.txt` is a single fenced `tsv` block, has exactly the required `target_name` and `predicted_n_degs` columns, preserves the requested-target order, includes the single requested target exactly once, and uses a non-negative integer prediction.