Done. I created the required outputs in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

The final point prediction is:

```tsv
target_name	predicted_n_degs
Dock7	0
```

I also validated that `answer.txt` contains exactly one fenced `tsv` block, preserves the manifest target order, includes exactly the one requested target, and uses a non-negative integer prediction.