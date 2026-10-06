Created both required outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Cep164	0
```

I validated that `answer.txt` contains only the single fenced `tsv` block, has exactly the requested header, preserves the requested-target order from `the single-target request`, includes `Cep164` exactly once and no extra targets, and uses a non-negative integer prediction.