Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

I predicted:

```tsv
target_name	predicted_n_degs
Hoxc13	0
```

I also validated that `answer.txt` contains exactly one fenced `tsv` block, preserves the requested manifest order, includes `Hoxc13` exactly once, and uses a non-negative integer prediction.