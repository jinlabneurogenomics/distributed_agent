Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md:1]) with the target-specific assay and biology reasoning for `Avpr2`
- [answer.txt]([local file: answer.txt:1]) with the exact fenced TSV answer

The point prediction is:

```tsv
target_name	predicted_n_degs
Avpr2	0
```

I also validated that `answer.txt` is a single `tsv` fenced block, contains exactly the manifest target in order, has no duplicate targets, and uses a non-negative integer prediction.