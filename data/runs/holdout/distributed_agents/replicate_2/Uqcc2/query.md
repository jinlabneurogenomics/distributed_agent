Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md:1])
- [answer.txt]([local file: answer.txt:1])

The manifest contains only `Uqcc2`, and the final point prediction is:

```tsv
target_name	predicted_n_degs
Uqcc2	1
```

I also validated that `answer.txt` is exactly a single fenced `tsv` block, preserves the requested target order, contains `Uqcc2` exactly once, and has a non-negative integer prediction.