Done: I created the required [trace.md]([local file: trace.md]) and [answer.txt]([local file: answer.txt]).

The held-out manifest had one target, `Ap3b2`, and I predicted:

```tsv
target_name	predicted_n_degs
Ap3b2	0
```

I also validated that `answer.txt` is exactly one fenced `tsv` block, preserves the manifest order, contains the expected header, has one row for `Ap3b2`, and has a non-negative integer prediction.