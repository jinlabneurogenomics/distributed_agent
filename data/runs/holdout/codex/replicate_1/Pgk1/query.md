Done: I wrote the forecast trace and the TSV answer.

- [trace.md]([local file: trace.md]) records the `Pgk1` biology, the central-glycolysis training anchors, the expression-parquet check that the 1-DEG glycolytic counts were self-only, and the reason for excluding larger off-axis metabolic signatures such as `Gfpt1`, `Mdh1`, `Nrf1`, and `Tsc2` from the main scale.
- [answer.txt]([local file: answer.txt]) contains exactly:

```tsv
target_name	predicted_n_degs
Pgk1	1
```

I also verified `answer.txt` is two lines, tab-delimited, uses the exact manifest target, and has a non-negative integer prediction.