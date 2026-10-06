Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md:1]) with the target-specific evidence and rationale for `Adrb1`
- [answer.txt]([local file: answer.txt:1]) with the required single fenced TSV block

The point prediction is:

```tsv
target_name	predicted_n_degs
Adrb1	0
```

I validated that `answer.txt` has exactly one manifest target, preserves the requested order, has no duplicates or extra prose, and uses a non-negative integer prediction.