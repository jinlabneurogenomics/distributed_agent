Done. I created both required files in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

The final TSV is:

```tsv
target_name	predicted_n_degs
Rab28	0
```

I validated that `answer.txt` is exactly one `tsv` fenced block, preserves the manifest order, contains `Rab28` exactly once, and has a non-negative integer prediction.