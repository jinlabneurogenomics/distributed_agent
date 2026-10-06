Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md:1]) with the target-specific reasoning for `Avpr2`, including focal training counts, same-experiment Distributed Agents corpus evidence, AVPR2 pathway literature, comparator counts, and limits.
- [answer.txt]([local file: answer.txt:1]) with the single required TSV block:

```tsv
target_name	predicted_n_degs
Avpr2	0
```

I also validated that `answer.txt` has only the fenced `tsv` block, preserves the manifest order, contains exactly one row for the only requested target, has no duplicates, and uses a non-negative integer prediction.