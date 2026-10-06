Done. I wrote both required outputs in the run directory:

- [trace.md]([local file: trace.md]) with the dataset queries, same-experiment corpus evidence, PubMed-backed `Tubb3`/tubulin biology, target-specific reasoning, and limits.
- [answer.txt]([local file: answer.txt]) with exactly the required single fenced `tsv` block.

The final point prediction is:

```tsv
target_name	predicted_n_degs
Tubb3	1
```

I also validated that `answer.txt` parses as one TSV fenced block, contains exactly one row, preserves the held-out manifest order, and has a non-negative integer prediction.