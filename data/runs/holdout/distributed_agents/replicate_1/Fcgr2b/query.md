Created the two required files in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Fcgr2b	0
```

I validated that `answer.txt` contains exactly one fenced `tsv` block, the exact required header, exactly the one requested target in manifest order, no duplicate targets, and a non-negative integer `predicted_n_degs`.