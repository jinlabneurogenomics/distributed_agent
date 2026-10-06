Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

The final TSV predicts:

```tsv
target_name	predicted_n_degs
Prokr2	0
```

I also verified that `answer.txt` exactly contains a single `tsv` fenced block with the header and the one manifest target, and that both output files are ASCII.