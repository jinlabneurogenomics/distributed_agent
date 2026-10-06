Done: wrote the direct forecast artifacts.

- [trace.md]([local file: trace.md]) records the biology and training-count evidence that drove the point estimate.
- [answer.txt]([local file: answer.txt]) contains:

```tsv
target_name	predicted_n_degs
Lrpap1	1
```

I also validated that `answer.txt` parses as exactly the requested one-row TSV with `Lrpap1` and a non-negative integer prediction.