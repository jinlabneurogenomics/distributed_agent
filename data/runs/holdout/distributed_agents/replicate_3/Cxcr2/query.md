Done: I created the requested outputs in the run directory.

- [trace.md]([local file: trace.md]) contains the dataset checks, Distributed Agents corpus evidence, PubMed-backed CXCR2 biology, target-specific reasoning, and limits.
- [answer.txt]([local file: answer.txt]) contains the required single fenced `tsv` block:

```tsv
target_name	predicted_n_degs
Cxcr2	0
```

I also validated that `answer.txt` has exactly the manifest target in order, no duplicate targets, and a non-negative integer prediction.