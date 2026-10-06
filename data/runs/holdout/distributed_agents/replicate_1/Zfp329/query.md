Created the required deliverables in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

Final point prediction:

```tsv
target_name	predicted_n_degs
Zfp329	0
```

I validated that `answer.txt` contains exactly one `tsv` fenced block, has the required `target_name` and `predicted_n_degs` columns, includes the single requested target exactly once in manifest order, and uses a non-negative integer prediction.