Done. I created both required outputs in the working run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

I predicted:

```tsv
target_name	predicted_n_degs
Tfap2a	0
```

I also validated that `answer.txt` has exactly one fenced `tsv` block, preserves the manifest order, includes only `Tfap2a`, and uses a non-negative integer prediction.