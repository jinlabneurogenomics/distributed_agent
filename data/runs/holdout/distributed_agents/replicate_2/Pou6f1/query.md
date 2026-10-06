Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

The prediction is:

```tsv
target_name	predicted_n_degs
Pou6f1	0
```

I also validated `answer.txt` against `182_Pou6f1.csv`: it is a single `tsv` fenced block, preserves the requested target order, has exactly one `Pou6f1` row, and contains a non-negative integer prediction.