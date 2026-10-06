Created the requested outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final point prediction is:

```tsv
target_name	predicted_n_degs
Dnajc6	1
```

I also mechanically validated that `answer.txt` contains only one fenced `tsv` block, has the required `target_name` / `predicted_n_degs` header, contains exactly the requested target in requested order, has no duplicates, and parses the prediction as a non-negative integer.