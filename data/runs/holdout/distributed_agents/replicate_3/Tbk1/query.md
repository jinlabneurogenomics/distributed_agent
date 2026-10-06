Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md]) with the target-specific evidence chain for `Tbk1`
- [answer.txt]([local file: answer.txt]) with the required single fenced `tsv` block

The final point prediction is:

```tsv
target_name	predicted_n_degs
Tbk1	0
```

I also validated that `answer.txt` has exactly one fenced `tsv` block, the exact requested header, one row in the held-out manifest order, no duplicate targets, and a non-negative integer prediction.