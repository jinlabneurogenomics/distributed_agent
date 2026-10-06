Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

I also validated that `answer.txt`:

- contains only a single fenced `tsv` block
- has the exact header `target_name	predicted_n_degs`
- includes `Xpo1` exactly once, matching the manifest order
- uses a non-negative integer prediction
- is ASCII-only

The point prediction written was:

```tsv
target_name	predicted_n_degs
Xpo1	520
```