Done. I created both required files in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

I validated that `answer.txt` is exactly one fenced `tsv` block, preserves the manifest target order, includes `Prokr2` exactly once, and contains a non-negative integer prediction:

```tsv
target_name	predicted_n_degs
Prokr2	0
```