Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md:1])
- [answer.txt]([local file: answer.txt:1])

I predicted:

```tsv
target_name	predicted_n_degs
Trio	0
```

I also validated that `answer.txt` is a single fenced `tsv` block, preserves the manifest order, contains exactly the one requested target, and has a non-negative integer prediction.