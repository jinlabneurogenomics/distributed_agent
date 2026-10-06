Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

The final prediction is:

```tsv
target_name	predicted_n_degs
Prdm12	0
```

I also validated that `answer.txt` is a single `tsv` fenced block, has exactly the requested header, preserves the manifest order, includes only `Prdm12`, and uses a non-negative integer prediction.