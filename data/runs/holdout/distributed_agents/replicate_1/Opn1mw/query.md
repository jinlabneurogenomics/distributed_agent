Created the requested files in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The prediction for the single held-out target is:

```tsv
target_name	predicted_n_degs
Opn1mw	0
```

I validated that `answer.txt` contains exactly one `tsv` fenced block, has the exact required header, preserves the requested target order, includes exactly the one requested target with no duplicates or extras, and uses a non-negative integer prediction.