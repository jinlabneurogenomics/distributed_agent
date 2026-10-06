Done: I wrote the direct forecast for `Tnfrsf1b`.

- [trace.md]([local file: trace.md]) contains the outcome-blind evidence chain:
  - exact `Tnfrsf1b` focal expression reach: 120 / 23,679 non-target nuclei, `0.336` pseudobulk cpm
  - focal training distribution: 1,205 / 1,674 training perturbations at `n_degs = 0`
  - all available local TNFR / TRAF / NF-kB / REL training perturbations at `n_degs = 0`
  - matched Parquet profile check confirming the six closest available TNF/NF-kB-axis nodes had zero BH-significant genes

- [answer.txt]([local file: answer.txt]) contains exactly:

```tsv
target_name	predicted_n_degs
Tnfrsf1b	0
```

I also sanity-checked that `answer.txt` has exactly the requested two TSV lines.