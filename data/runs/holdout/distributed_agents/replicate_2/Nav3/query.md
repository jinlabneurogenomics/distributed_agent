Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md]) with the `Nav3`-specific reasoning, focal training-count calibration, same-experiment Distributed Agents corpus evidence for the comparator genes, external NAV3 literature, and the limits around extrapolating from actin/guidance/microtubule neighbors.
- [answer.txt]([local file: answer.txt]) with only the required fenced TSV.

The point prediction is:

```tsv
target_name	predicted_n_degs
Nav3	0
```

I also validated that `answer.txt` is a single `tsv` fenced block, has the exact header, contains exactly one row, preserves the manifest order, and uses a non-negative integer prediction.