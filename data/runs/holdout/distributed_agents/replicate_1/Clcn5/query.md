Created the two required deliverables in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Clcn5	0
```

I validated that `answer.txt` contains exactly one fenced `tsv` block, exactly the requested target in the requested order, no duplicate or extra targets, and a non-negative integer `predicted_n_degs`.