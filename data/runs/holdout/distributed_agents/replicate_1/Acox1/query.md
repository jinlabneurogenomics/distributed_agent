Created the two required run outputs:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Acox1	0
```

I validated that `answer.txt` contains exactly one fenced `tsv` block, the required header, exactly one row, the exact held-out target `Acox1` in requested order, no duplicate or extra targets, and a non-negative integer prediction.