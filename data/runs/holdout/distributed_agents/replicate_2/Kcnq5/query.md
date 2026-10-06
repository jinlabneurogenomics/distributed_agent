Done. I wrote both required outputs:

- [trace.md]([local file: trace.md:1]) with the Kcnq5-specific reasoning, same-experiment KCNQ comparisons, focal Parquet/CSV calibration, corpus evidence, PubMed citations, and explicit limitations.
- [answer.txt]([local file: answer.txt:1]) with exactly one fenced TSV row:

```tsv
target_name	predicted_n_degs
Kcnq5	1
```

I also validated that `answer.txt`:

- starts with ` ```tsv `
- has the exact header `target_name	predicted_n_degs`
- preserves the manifest order
- includes `Kcnq5` exactly once
- uses a non-negative integer prediction
- contains no prose outside the fenced block