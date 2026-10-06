Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

Final prediction:

```tsv
target_name	predicted_n_degs
Clip2	1
```

I validated that `answer.txt` contains only one fenced `tsv` block, has the exact required header, includes the single requested target `Clip2` in manifest order, has no duplicate or extra targets, and uses a non-negative integer prediction.