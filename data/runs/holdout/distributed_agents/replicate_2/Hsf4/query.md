Done. I created the required outputs in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

The held-out manifest contained only `Hsf4`, and the final point prediction is:

```tsv
target_name	predicted_n_degs
Hsf4	0
```

I also validated that `answer.txt` is exactly a single `tsv` fenced block, preserves the requested target order, includes `Hsf4` exactly once, and contains a non-negative integer prediction.