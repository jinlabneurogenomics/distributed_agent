Created the required deliverables in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Tubb4a	1
```

I validated that `answer.txt` contains only a single `tsv` fenced block, preserves the requested target order, includes exactly the one manifest target once, uses the exact header, and has a non-negative integer `predicted_n_degs`.