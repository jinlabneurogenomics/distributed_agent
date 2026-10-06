Done. I created both required deliverables in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

`answer.txt` contains exactly one fenced `tsv` block with the manifest target in order:

```tsv
target_name	predicted_n_degs
Hspa9	3
```

I also verified the file contract programmatically: the fenced block parses as TSV, includes `Hspa9` exactly once, preserves the held-out manifest order, and uses a non-negative integer prediction.