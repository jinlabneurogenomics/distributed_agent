Done. I wrote the requested forecast artifacts:

- [answer.txt]([local file: answer.txt]) contains exactly:

```tsv
target_name	predicted_n_degs
Cxcr2	0
```

- [trace.md]([local file: trace.md]) records the evidence behind the zero forecast: exact zero detected `Cxcr2` expression in 23,679 focal non-targeting nuclei, a strongly zero-skewed 151 TH training distribution, and direct parquet checks showing the closest measured chemokine/cytokine/innate-immune comparators were zero or near-zero in the same population.

I also mechanically validated that `answer.txt` has two tab-separated columns, the exact `Cxcr2` row, and no extra rows.