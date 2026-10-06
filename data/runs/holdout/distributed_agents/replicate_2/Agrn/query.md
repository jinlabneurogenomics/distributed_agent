Done. I wrote the two required outputs in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

The point prediction is:

```tsv
target_name	predicted_n_degs
Agrn	0
```

I validated that `answer.txt` is exactly one fenced `tsv` block, contains the manifest target `Agrn` exactly once in the requested order, and has a non-negative integer prediction.