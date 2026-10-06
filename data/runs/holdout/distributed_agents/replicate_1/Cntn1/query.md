Created both requested run-local outputs:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Cntn1	1
```

I verified mechanically that `answer.txt` contains exactly one fenced `tsv` block, the exact header `target_name	predicted_n_degs`, one row, requested-target order preservation, no duplicate targets, and a non-negative integer prediction.