Created the required outputs:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final point prediction is:

```tsv
target_name	predicted_n_degs
Srrm2	260
```

I mechanically validated that `answer.txt` contains exactly one fenced `tsv` block, preserves the requested-target order, has exactly the one requested `Srrm2` row, has no duplicate or extra targets, and uses a non-negative integer prediction.