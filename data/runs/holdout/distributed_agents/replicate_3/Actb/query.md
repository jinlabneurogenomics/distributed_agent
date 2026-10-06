Done. I created both required deliverables in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

The held-out manifest contained only `Actb`, and I predicted:

```tsv
target_name	predicted_n_degs
Actb	0
```

I also mechanically validated that `answer.txt` contains exactly one fenced `tsv` block, exactly one row, the manifest target in order, a tab separator, and a non-negative integer prediction.