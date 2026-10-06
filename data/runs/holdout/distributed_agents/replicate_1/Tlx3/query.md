Created the two required deliverables:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

I predicted:

```tsv
target_name	predicted_n_degs
Tlx3	0
```

I also mechanically validated `answer.txt` against the requested-target CSV:

- required files exist
- `answer.txt` is exactly one fenced `tsv` block
- header is `target_name	predicted_n_degs`
- exactly 1 data row
- target spelling and order match the manifest exactly: `Tlx3`
- no duplicate target
- `predicted_n_degs` is a non-negative integer