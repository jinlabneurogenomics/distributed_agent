Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

The final point prediction is:

```tsv
target_name	predicted_n_degs
Ppargc1b	0
```

I also validated that `answer.txt` is exactly one fenced `tsv` block, preserves the requested `Ppargc1b` spelling/order from the manifest, contains no duplicate targets, and uses a non-negative integer prediction.