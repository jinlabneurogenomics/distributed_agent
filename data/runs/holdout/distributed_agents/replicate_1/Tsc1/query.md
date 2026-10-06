Created the requested outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Tsc1	80
```

I verified mechanically that:

- both required files exist
- `answer.txt` contains exactly one fenced `tsv` block and no surrounding prose
- the header is exactly `target_name	predicted_n_degs`
- there is exactly one data row
- `Tsc1` matches the requested manifest in order and appears once
- `predicted_n_degs` is a non-negative integer