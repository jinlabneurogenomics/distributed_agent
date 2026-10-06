Done. I created the required outputs:

- [trace.md]([local file: trace.md]) with the target-specific evidence and rationale for `Vps37a`
- [answer.txt]([local file: answer.txt]) with the single fenced TSV block

I validated that `answer.txt` is exactly one `tsv` fenced block, preserves the manifest order, contains `Vps37a` exactly once, and uses a non-negative integer prediction:

```tsv
target_name	predicted_n_degs
Vps37a	0
```