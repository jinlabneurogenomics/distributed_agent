Created both required outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final point prediction is:

```tsv
target_name	predicted_n_degs
Syn3	0
```

I validated that `answer.txt` is a single `tsv` fenced block, has exactly the required header, preserves the requested target order from `the single-target request`, contains exactly one row for `Syn3`, has no duplicate or extra targets, and uses a non-negative integer prediction.