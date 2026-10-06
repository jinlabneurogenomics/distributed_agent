Created both requested outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Klrk1	0
```

I validated `answer.txt` mechanically against the requested-target CSV: it has one `tsv` fenced block, the exact required header, exactly one row, exact target membership and order for `Klrk1`, no duplicate targets, and a non-negative integer prediction.