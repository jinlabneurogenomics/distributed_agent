Done. I wrote the direct forecast artifacts:

- [trace.md]([local file: trace.md:1]) records the endpoint-blind Cox6b1 biology, the declared count-table analogs, matched Parquet checks for the complex-IV cohort, and the reasoning that led to a zero-count point forecast.
- [answer.txt]([local file: answer.txt:1]) contains only the requested TSV:

```tsv
target_name	predicted_n_degs
Cox6b1	0
```

I also validated that `answer.txt` has exactly two tab-separated rows, the required header, the exact manifest target `Cox6b1`, and one non-negative integer prediction.