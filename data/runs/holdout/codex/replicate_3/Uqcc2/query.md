Done. I wrote the direct forecast artifacts:

- [trace.md]([local file: trace.md]) records the biology prior, comparator measurements, profile evidence, and why the point forecast lands at one DEG.
- [answer.txt]([local file: answer.txt]) contains only:

```tsv
target_name	predicted_n_degs
Uqcc2	1
```

I also validated the TSV shape so `answer.txt` is exactly the requested header plus the single `Uqcc2	1` row.