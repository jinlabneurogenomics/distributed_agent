Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

I predicted:

```tsv
target_name	predicted_n_degs
Ptcd3	0
```

I also validated that `answer.txt` is exactly one fenced `tsv` block, contains `Ptcd3` exactly once, preserves the manifest target, and uses a non-negative integer prediction.