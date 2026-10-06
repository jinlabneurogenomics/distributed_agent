Created both required outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Prdm12	0
```

I also mechanically validated `answer.txt` against the requested-target manifest: the fenced TSV is the only content, the header is exact, there is exactly one data row, `Prdm12` appears once in the requested order, and `0` parses as a non-negative integer.