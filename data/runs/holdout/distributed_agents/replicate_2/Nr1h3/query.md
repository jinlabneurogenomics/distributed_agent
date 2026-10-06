Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

The prediction is:

```tsv
target_name	predicted_n_degs
Nr1h3	0
```

I validated that `answer.txt` is exactly one fenced `tsv` block, preserves the manifest target order, has exactly the single requested row, has no duplicate targets, and uses a non-negative integer prediction. The trace anchors the zero call to the focal raw parquet and training counts, with `Nr1h2`, `Rxra`/`Rxrb`/`Rxrg`, `Abca1`, `Srebf1`, NR1H/PPAR neighbors, and the `Srebf2` 7-DEG sterol-module counterexample as the main calibration points.