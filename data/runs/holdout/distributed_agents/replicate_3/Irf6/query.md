Done: I wrote the required run outputs:

- [trace.md]([local file: trace.md]) with the target-specific evidence and limits
- [answer.txt]([local file: answer.txt]) with the single fenced TSV block

The final point prediction is:

```tsv
target_name	predicted_n_degs
Irf6	0
```

I also validated that `answer.txt` is a single `tsv` fenced block, contains exactly one row, preserves the requested `Irf6` target name, and has a nonnegative integer prediction.