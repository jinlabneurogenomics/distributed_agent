Created the required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

Final point prediction:

```tsv
target_name	predicted_n_degs
Cep83	0
```

I verified that `answer.txt` contains exactly one `tsv` fenced block, the header is `target_name	predicted_n_degs`, it has exactly one data row, `Cep83` matches the requested-target manifest in order, there are no duplicate targets, and `predicted_n_degs` is a non-negative integer.