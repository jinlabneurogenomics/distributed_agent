Created the required deliverables in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Vps13d	0
```

I mechanically validated `answer.txt` against the requested-target CSV: exact header, exactly one row, `Vps13d` included once and in manifest order, no extra targets, and a non-negative integer `predicted_n_degs`.