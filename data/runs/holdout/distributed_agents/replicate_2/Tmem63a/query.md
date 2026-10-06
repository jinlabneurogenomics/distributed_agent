Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

The final TSV predicts:

```tsv
target_name	predicted_n_degs
Tmem63a	0
```

I also validated that `answer.txt` is a single fenced `tsv` block, has the required header, preserves the manifest target exactly, and contains exactly the one requested row.