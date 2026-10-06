Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

I also validated that `answer.txt` is exactly one fenced `tsv` block, preserves the requested manifest order, contains `Pcyt2` exactly once, and uses a single non-negative integer prediction:

```tsv
target_name	predicted_n_degs
Pcyt2	4
```