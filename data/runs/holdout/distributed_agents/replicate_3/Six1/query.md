Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md:1]) with the target-specific reasoning for held-out `Six1`
- [answer.txt]([local file: answer.txt:1]) containing exactly the requested fenced TSV

The final point prediction is:

```tsv
target_name	predicted_n_degs
Six1	0
```

I also validated that `answer.txt` is a single `tsv` code block, has the right header, includes `Six1` exactly once, and has `predicted_n_degs = 0` as a non-negative integer.