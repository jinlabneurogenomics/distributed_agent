Done.

Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Ccr5	0
```

I also mechanically verified:

- both required files exist
- `answer.txt` contains only one fenced `tsv` block
- the header is exactly `target_name	predicted_n_degs`
- the output has exactly one row
- `Ccr5` is present exactly once
- requested-target order is preserved
- the predicted value is a non-negative integer
- no unrequested target was added