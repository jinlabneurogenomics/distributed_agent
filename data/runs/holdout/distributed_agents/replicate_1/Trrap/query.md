Done. I created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

`answer.txt` contains exactly one fenced `tsv` block with the requested target in manifest order:

```tsv
target_name	predicted_n_degs
Trrap	47
```

I also ran a mechanical validation that checked:

- `trace.md` and `answer.txt` exist and are non-empty
- the requested-target CSV has the expected single `target_name` column
- `answer.txt` has no prose outside the single fenced TSV block
- the TSV header is exactly `target_name	predicted_n_degs`
- there is exactly one data row
- `Trrap` is present exactly once and in the requested order
- `predicted_n_degs` is a non-negative integer