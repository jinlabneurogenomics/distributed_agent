Created the required deliverables in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Kmt2b	18
```

I also mechanically validated `answer.txt`:

- exactly one fenced `tsv` block
- no prose outside the block
- required columns: `target_name`, `predicted_n_degs`
- exactly one row, matching the requested-target CSV
- requested order preserved
- no duplicate targets
- non-negative integer prediction