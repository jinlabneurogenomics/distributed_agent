Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

The prediction is:

```tsv
target_name	predicted_n_degs
Nlgn2	1
```

I also validated that `answer.txt` is exactly a single `tsv` fenced block, contains the requested `Nlgn2` row once, preserves the manifest order, and uses a non-negative integer prediction.