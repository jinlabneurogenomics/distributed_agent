Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md]) explains the `Dnajc6` prediction, including the focal training-count calibration, same-experiment Distributed Agents corpus evidence, PubMed-cited auxilin biology, and the limits of the extrapolation.
- [answer.txt]([local file: answer.txt]) contains exactly the required fenced TSV:

```tsv
target_name	predicted_n_degs
Dnajc6	1
```

I also validated that `answer.txt` has no prose outside the single `tsv` fence and exactly one row for `Dnajc6`.