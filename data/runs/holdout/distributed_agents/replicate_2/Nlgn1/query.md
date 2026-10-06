Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

I validated that `answer.txt` is a single fenced `tsv` block, preserves the manifest target order, includes exactly `Nlgn1` once, and contains a non-negative integer prediction:

```tsv
target_name	predicted_n_degs
Nlgn1	1
```