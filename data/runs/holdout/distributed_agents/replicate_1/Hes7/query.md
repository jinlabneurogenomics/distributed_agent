Created both requested outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Hes7	0
```

I validated that `answer.txt` is exactly one fenced `tsv` block, has the required header, contains exactly the one requested target in requested order, has no duplicate or extra targets, and uses a non-negative integer prediction.